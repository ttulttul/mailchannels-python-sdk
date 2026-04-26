"""Tests for webhook resources and helpers."""

from __future__ import annotations

import base64
import hashlib

import pytest
from conftest import FakeHTTPXClient, FakeRequestsClient

from mailchannels.client import Client
from mailchannels.response import SDKResponse
from mailchannels.version import user_agent
from mailchannels.webhooks import (
    parse_signature_input,
    signature_is_fresh,
    signature_key_id,
    verify_content_digest,
)


def test_webhook_management_uses_documented_paths() -> None:
    """It manages webhook endpoints through the documented resource."""
    transport = FakeRequestsClient(SDKResponse(201, None, ""))
    client = Client(api_key="test-key", http_client=transport)

    client.webhooks.create("https://example.com/mailchannels")
    client.webhooks.list()
    client.webhooks.delete()
    client.webhooks.validate(request_id="test_request_1")

    assert [call["method"] for call in transport.calls] == [
        "POST",
        "GET",
        "DELETE",
        "POST",
    ]
    assert [call["url"] for call in transport.calls] == [
        "https://api.mailchannels.net/tx/v1/webhook",
        "https://api.mailchannels.net/tx/v1/webhook",
        "https://api.mailchannels.net/tx/v1/webhook",
        "https://api.mailchannels.net/tx/v1/webhook/validate",
    ]
    assert transport.calls[0]["params"] == {
        "endpoint": "https://example.com/mailchannels"
    }
    assert transport.calls[3]["json"] == {"request_id": "test_request_1"}


def test_webhook_batches_public_key_and_resend() -> None:
    """It exposes webhook batch, public-key, and resend endpoints."""
    transport = FakeRequestsClient(SDKResponse(200, {"ok": True}, "{}"))
    client = Client(api_key="test-key", http_client=transport)

    client.webhooks.batches(statuses=["4xx", "5xx"], limit=25, offset=5)
    client.webhooks.public_key("mckey")
    client.webhooks.resend_batch(123, customer_handle="customer_123")

    assert transport.calls[0]["url"] == (
        "https://api.mailchannels.net/tx/v1/webhook-batch"
    )
    assert transport.calls[0]["params"] == {
        "statuses": "4xx,5xx",
        "limit": 25,
        "offset": 5,
    }
    assert "X-Api-Key" not in transport.calls[1]["headers"]
    assert transport.calls[1]["url"] == (
        "https://api.mailchannels.net/tx/v1/webhook/public-key"
    )
    assert transport.calls[1]["params"] == {"id": "mckey"}
    assert transport.calls[2]["headers"] == {
        "Content-Type": "application/json",
        "User-Agent": user_agent(),
        "X-Customer-Handle": "customer_123",
    }


async def test_webhook_async_methods_use_async_transport() -> None:
    """It exposes async webhook operations."""
    transport = FakeHTTPXClient(SDKResponse(200, {"webhook_batches": []}, "{}"))
    client = Client(api_key="test-key", async_http_client=transport)

    await client.webhooks.batches_async(statuses=["no_response"])

    assert transport.calls[0]["method"] == "GET"
    assert transport.calls[0]["params"] == {"statuses": "no_response"}


def test_webhook_signature_helpers() -> None:
    """It parses signature metadata and verifies the content digest."""
    body = b'[{"event":"delivered","customer_handle":"customer_123"}]'
    digest = base64.b64encode(hashlib.sha256(body).digest()).decode("ascii")
    headers = {
        "Content-Digest": f"sha-256=:{digest}:",
        "Signature-Input": (
            'sig_1738775282=("content-digest");created=1738868393;'
            'alg="ed25519";keyid="mckey"'
        ),
    }

    parameters = parse_signature_input(headers["Signature-Input"])

    assert parameters.signature_name == "sig_1738775282"
    assert parameters.covered_components == ["content-digest"]
    assert parameters.algorithm == "ed25519"
    assert parameters.key_id == "mckey"
    assert signature_key_id(headers) == "mckey"
    assert signature_is_fresh(parameters, now=1738868400)
    assert verify_content_digest(headers, body)


def test_webhook_content_digest_missing_header_returns_false() -> None:
    """It rejects webhook requests without a Content-Digest header."""
    assert not verify_content_digest({}, b"{}")


def test_webhook_content_digest_wrong_digest_returns_false() -> None:
    """It rejects webhook bodies that do not match the supplied digest."""
    digest = base64.b64encode(hashlib.sha256(b"expected").digest()).decode("ascii")

    assert not verify_content_digest({"Content-Digest": f"sha-256=:{digest}:"}, b"bad")


@pytest.mark.parametrize(
    "digest_header",
    [
        "sha-512=:abc:",
        "sha-256=abc",
        "not-a-digest",
    ],
)
def test_webhook_content_digest_malformed_header_returns_false(
    digest_header: str,
) -> None:
    """It rejects malformed Content-Digest headers without crashing."""
    assert not verify_content_digest({"Content-Digest": digest_header}, b"{}")


def test_webhook_content_digest_non_base64_returns_false() -> None:
    """It rejects invalid base64 digest values without crashing."""
    assert not verify_content_digest({"Content-Digest": "sha-256=:%%%%:"}, b"{}")


def test_webhook_content_digest_header_lookup_is_case_insensitive() -> None:
    """It accepts case variations in webhook digest headers."""
    body = b'{"event":"delivered"}'
    digest = base64.b64encode(hashlib.sha256(body).digest()).decode("ascii")

    assert verify_content_digest({"content-digest": f"sha-256=:{digest}:"}, body)


def test_webhook_signature_key_id_missing_header_returns_none() -> None:
    """It returns None when Signature-Input is absent."""
    assert signature_key_id({}) is None


def test_webhook_signature_key_id_header_lookup_is_case_insensitive() -> None:
    """It accepts case variations in webhook signature headers."""
    headers = {
        "signature-input": (
            'sig=("content-digest");created=1738868393;'
            'alg="ed25519";keyid="mckey"'
        )
    }

    assert signature_key_id(headers) == "mckey"


def test_webhook_signature_key_id_malformed_header_raises_value_error() -> None:
    """It raises ValueError for malformed Signature-Input headers."""
    with pytest.raises(ValueError):
        signature_key_id({"Signature-Input": "not a structured signature input"})


def test_webhook_signature_missing_created_is_not_fresh() -> None:
    """It treats signatures without created timestamps as stale."""
    parameters = parse_signature_input('sig=("content-digest");keyid="mckey"')

    assert parameters.created is None
    assert not signature_is_fresh(parameters, now=1738868400)


def test_webhook_signature_created_outside_tolerance_is_not_fresh() -> None:
    """It rejects signatures older than the allowed tolerance."""
    parameters = parse_signature_input(
        'sig=("content-digest");created=1738860000;keyid="mckey"'
    )

    assert not signature_is_fresh(parameters, now=1738868400, tolerance_seconds=300)


def test_webhook_signature_future_created_outside_tolerance_is_not_fresh() -> None:
    """It rejects signatures created too far in the future."""
    parameters = parse_signature_input(
        'sig=("content-digest");created=1738872000;keyid="mckey"'
    )

    assert not signature_is_fresh(parameters, now=1738868400, tolerance_seconds=300)
