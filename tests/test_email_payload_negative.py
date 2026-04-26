"""Negative tests for email payload validation and API rejection handling."""

from __future__ import annotations

import os
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

import pytest
import requests
from conftest import FakeRequestsClient

import mailchannels
from mailchannels.client import Client
from mailchannels.emails import Attachment, normalize_email_params
from mailchannels.response import SDKResponse


@dataclass(frozen=True)
class InvalidEmailCase:
    """One invalid SDK email payload case."""

    name: str
    payload: dict[str, Any]
    message: str


@dataclass(frozen=True)
class RawApiRejectionCase:
    """One raw send payload expected to be rejected by the API."""

    name: str
    build_payload: Callable[[str, str], dict[str, Any]]


class _Http404AttachmentResponse:
    """Fake response that fails like a remote attachment 404."""

    content = b"not found"
    headers = {"Content-Type": "text/plain"}

    def raise_for_status(self) -> None:
        """Raise the same request exception family as requests."""
        raise requests.HTTPError("404 Client Error: Not Found")


INVALID_EMAIL_CASES = (
    InvalidEmailCase(
        "missing-from",
        {
            "to": "recipient@example.net",
            "subject": "Hello",
            "text": "Hello",
        },
        "`from`",
    ),
    InvalidEmailCase(
        "missing-recipient",
        {
            "from": {"email": "sender@example.com"},
            "subject": "Hello",
            "text": "Hello",
        },
        "`to`",
    ),
    InvalidEmailCase(
        "missing-subject",
        {
            "from": {"email": "sender@example.com"},
            "to": "recipient@example.net",
            "text": "Hello",
        },
        "Invalid email parameters",
    ),
    InvalidEmailCase(
        "missing-content",
        {
            "from": {"email": "sender@example.com"},
            "to": "recipient@example.net",
            "subject": "Hello",
        },
        "`content`, `text`, or `html`",
    ),
    InvalidEmailCase(
        "empty-recipient-list",
        {
            "from": {"email": "sender@example.com"},
            "to": [],
            "subject": "Hello",
            "text": "Hello",
        },
        "Invalid email parameters",
    ),
    InvalidEmailCase(
        "invalid-from-address",
        {
            "from": {"email": "not-an-email"},
            "to": "recipient@example.net",
            "subject": "Hello",
            "text": "Hello",
        },
        "Invalid email parameters",
    ),
    InvalidEmailCase(
        "reserved-root-header",
        {
            "from": {"email": "sender@example.com"},
            "to": "recipient@example.net",
            "subject": "Hello",
            "text": "Hello",
            "headers": {"Subject": "legacy header"},
        },
        "Invalid email parameters",
    ),
    InvalidEmailCase(
        "reserved-personalization-header",
        {
            "from": {"email": "sender@example.com"},
            "personalizations": [
                {
                    "to": [{"email": "recipient@example.net"}],
                    "headers": {"To": "legacy header"},
                }
            ],
            "subject": "Hello",
            "text": "Hello",
        },
        "Invalid email parameters",
    ),
)

RAW_API_REJECTION_CASES = (
    RawApiRejectionCase(
        "missing-from",
        lambda _from_address, to_address: {
            "personalizations": [{"to": [{"email": to_address}]}],
            "subject": "Invalid dry-run payload",
            "content": [{"type": "text/plain", "value": "Hello"}],
        },
    ),
    RawApiRejectionCase(
        "missing-recipient",
        lambda from_address, _to_address: {
            "from": {"email": from_address},
            "personalizations": [],
            "subject": "Invalid dry-run payload",
            "content": [{"type": "text/plain", "value": "Hello"}],
        },
    ),
    RawApiRejectionCase(
        "missing-subject",
        lambda from_address, to_address: {
            "from": {"email": from_address},
            "personalizations": [{"to": [{"email": to_address}]}],
            "content": [{"type": "text/plain", "value": "Hello"}],
        },
    ),
    RawApiRejectionCase(
        "missing-content",
        lambda from_address, to_address: {
            "from": {"email": from_address},
            "personalizations": [{"to": [{"email": to_address}]}],
            "subject": "Invalid dry-run payload",
        },
    ),
)


@pytest.mark.parametrize(
    "case",
    INVALID_EMAIL_CASES,
    ids=[case.name for case in INVALID_EMAIL_CASES],
)
def test_invalid_email_payloads_fail_before_transport(case: InvalidEmailCase) -> None:
    """Invalid SDK email payloads raise validation errors before HTTP."""
    transport = FakeRequestsClient()
    client = Client(api_key="test-key", http_client=transport)

    with pytest.raises(mailchannels.MailChannelsError) as error:
        client.emails.send(case.payload, dry_run=True)

    assert case.message in str(error.value)
    assert error.value.code == "ValidationError"
    assert transport.calls == []


def test_empty_attachments_list_is_preserved_cleanly() -> None:
    """An explicit empty attachments list remains deterministic and valid."""
    payload = normalize_email_params(
        {
            "from": {"email": "sender@example.com"},
            "to": "recipient@example.net",
            "subject": "Hello",
            "text": "Hello",
            "attachments": [],
        }
    )

    assert payload["attachments"] == []


def test_missing_attachment_file_raises_clear_sdk_error(tmp_path) -> None:
    """Missing local attachment files raise a specific SDK error."""
    missing_file = tmp_path / "missing.pdf"

    with pytest.raises(mailchannels.MailChannelsError) as error:
        Attachment.from_file(missing_file)

    assert error.value.code == "AttachmentReadError"
    assert "Unable to read attachment file" in str(error.value)


def test_remote_attachment_404_raises_clear_sdk_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Remote attachment fetch failures are wrapped with a stable SDK code."""

    def fake_get(url: str, *, timeout: float) -> _Http404AttachmentResponse:
        """Return a response object that raises during status validation."""
        assert url == "https://example.com/missing.pdf"
        assert timeout == 30.0
        return _Http404AttachmentResponse()

    monkeypatch.setattr(requests, "get", fake_get)

    with pytest.raises(mailchannels.MailChannelsError) as error:
        Attachment.from_url("https://example.com/missing.pdf")

    assert error.value.code == "AttachmentFetchError"
    assert "Unable to fetch attachment URL" in str(error.value)


def test_url_attachment_without_filename_uses_fallback(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Remote attachment URLs without path names use a deterministic fallback."""

    class FakeAttachmentResponse:
        """Successful remote attachment response."""

        content = b"remote-data"
        headers = {"Content-Type": "application/pdf"}

        def raise_for_status(self) -> None:
            """Simulate a successful HTTP response."""

    def fake_get(url: str, *, timeout: float) -> FakeAttachmentResponse:
        """Return a successful fake attachment response."""
        assert url == "https://example.com"
        assert timeout == 30.0
        return FakeAttachmentResponse()

    monkeypatch.setattr(requests, "get", fake_get)

    attachment = Attachment.from_url("https://example.com")

    assert attachment.filename == "attachment"
    assert attachment.type == "application/pdf"
    assert attachment.content == "cmVtb3RlLWRhdGE="


def test_native_content_and_personalizations_win_over_shortcuts() -> None:
    """Conflicting shortcut/native fields resolve toward native API fields."""
    payload = normalize_email_params(
        {
            "from": {"email": "sender@example.com"},
            "to": "shortcut@example.net",
            "personalizations": [{"to": [{"email": "native@example.net"}]}],
            "subject": "Hello",
            "text": "Shortcut text",
            "content": [{"type": "text/plain", "value": "Native text"}],
        }
    )

    assert payload["personalizations"] == [
        {"to": [{"email": "native@example.net"}]}
    ]
    assert payload["content"] == [{"type": "text/plain", "value": "Native text"}]


@pytest.mark.parametrize(
    "case",
    RAW_API_REJECTION_CASES,
    ids=[case.name for case in RAW_API_REJECTION_CASES],
)
def test_mocked_api_rejects_raw_invalid_send_payloads(
    case: RawApiRejectionCase,
) -> None:
    """Fake transport tests exercise raw invalid-payload API error handling."""
    payload = case.build_payload("sender@example.com", "recipient@example.net")
    transport = FakeRequestsClient(
        SDKResponse(
            400,
            {"errors": [{"message": f"{case.name} is invalid"}]},
            "{}",
            headers={"X-Request-ID": f"req_{case.name}"},
        )
    )
    client = Client(api_key="test-key", http_client=transport)

    with pytest.raises(mailchannels.InvalidRequestError) as error:
        client.request("POST", "/send", json=payload, params={"dry-run": "true"})

    assert error.value.status_code == 400
    assert error.value.request_id == f"req_{case.name}"
    assert transport.calls[0]["json"] == payload
    assert transport.calls[0]["params"] == {"dry-run": "true"}


@pytest.mark.online
@pytest.mark.parametrize(
    "case",
    RAW_API_REJECTION_CASES,
    ids=[case.name for case in RAW_API_REJECTION_CASES],
)
def test_online_api_rejects_raw_invalid_send_payloads(
    case: RawApiRejectionCase,
) -> None:
    """Live dry-run tests verify the API rejects the same raw invalid payloads."""
    from_address = os.environ.get("MAILCHANNELS_ONLINE_FROM")
    to_address = os.environ.get("MAILCHANNELS_ONLINE_TO")
    if not from_address or not to_address:
        pytest.skip(
            "set MAILCHANNELS_ONLINE_FROM and MAILCHANNELS_ONLINE_TO to run "
            "online negative send-payload tests"
        )

    payload = case.build_payload(from_address, to_address)
    client = mailchannels.Client(
        api_key=os.environ["MAILCHANNELS_API_KEY"],
        base_url=os.environ.get("MAILCHANNELS_API_URL"),
    )

    try:
        with pytest.raises(mailchannels.InvalidRequestError) as error:
            client.request("POST", "/send", json=payload, params={"dry-run": "true"})
    except mailchannels.ApiError as error:
        _xfail_live_server_error(error)
        raise
    except requests.RequestException as error:
        pytest.xfail(f"Live MailChannels API transport failed: {error}")

    assert error.value.status_code == 400


def _xfail_live_server_error(error: mailchannels.ApiError) -> None:
    """Mark live MailChannels 5xx responses as external service failures."""
    if error.status_code is not None and error.status_code >= 500:
        pytest.xfail(
            "Live MailChannels API returned a server error: "
            f"status={error.status_code} request_id={error.request_id}"
        )
