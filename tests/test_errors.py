"""Tests for API error handling."""

from __future__ import annotations

import pytest
from conftest import FakeRequestsClient

from mailchannels.client import Client
from mailchannels.exceptions import (
    ApiError,
    AuthenticationError,
    BadGatewayError,
    ConflictError,
    ForbiddenError,
    InvalidRequestError,
    MailChannelsError,
    PayloadTooLargeError,
    RateLimitError,
    ServerError,
)
from mailchannels.response import SDKResponse, raise_for_status


def test_forbidden_response_raises_forbidden_error() -> None:
    """It maps 403 responses to ForbiddenError."""
    client = Client(
        api_key="test-key",
        http_client=FakeRequestsClient(
            SDKResponse(403, {"message": "Forbidden"}, "Forbidden"),
        ),
    )

    with pytest.raises(ForbiddenError) as error:
        client.sub_accounts.create(handle="clienta")

    assert error.value.status_code == 403
    assert error.value.error_type == "permission_error"
    assert error.value.suggested_action == (
        "Confirm the API key has access to this MailChannels resource."
    )


def test_conflict_response_raises_conflict_error() -> None:
    """It maps sub-account conflicts to ConflictError."""
    client = Client(
        api_key="test-key",
        http_client=FakeRequestsClient(
            SDKResponse(409, {"message": "Exists"}, "Exists"),
        ),
    )

    with pytest.raises(ConflictError):
        client.sub_accounts.create(handle="clienta")


def test_payload_too_large_response_raises_specific_error() -> None:
    """It maps 413 responses to PayloadTooLargeError."""
    client = Client(
        api_key="test-key",
        http_client=FakeRequestsClient(
            SDKResponse(413, {"message": "Too large"}, "Too large"),
        ),
    )

    with pytest.raises(PayloadTooLargeError) as error:
        client.emails.queue(
            {
                "from": {"email": "sender@example.com"},
                "to": "recipient@example.net",
                "subject": "Hello",
                "text": "Plain text",
            }
        )

    assert error.value.suggested_action == (
        "Reduce message size or attachment payload before retrying."
    )


def test_api_error_includes_headers_and_request_metadata() -> None:
    """It preserves headers, request IDs, and retry hints on API errors."""
    client = Client(
        api_key="test-key",
        http_client=FakeRequestsClient(
            SDKResponse(
                429,
                {"message": "Slow down"},
                "Slow down",
                headers={"X-Request-ID": "req_123", "Retry-After": "30"},
            ),
        ),
    )

    with pytest.raises(RateLimitError) as error:
        client.metrics.volume()

    assert isinstance(error.value, ApiError)
    assert error.value.status_code == 429
    assert error.value.headers == {"X-Request-ID": "req_123", "Retry-After": "30"}
    assert error.value.request_id == "req_123"
    assert error.value.retry_after == "30"
    assert error.value.error_type == "rate_limit_error"
    assert error.value.to_dict()["suggested_action"] == (
        "Back off before retrying; inspect Retry-After if present."
    )


def test_null_error_body_uses_status_fallback_message() -> None:
    """It does not expose JSON null as the user-facing error message."""
    client = Client(
        api_key="test-key",
        http_client=FakeRequestsClient(SDKResponse(500, None, "null\n")),
    )

    with pytest.raises(ServerError) as error:
        client.usage.retrieve()

    assert str(error.value) == "MailChannels API request failed with status 500."


@pytest.mark.parametrize(
    ("status_code", "error_class", "error_type"),
    [
        (400, InvalidRequestError, "invalid_request_error"),
        (401, AuthenticationError, "authentication_error"),
        (404, InvalidRequestError, "invalid_request_error"),
        (422, InvalidRequestError, "invalid_request_error"),
        (429, RateLimitError, "rate_limit_error"),
        (500, ServerError, "server_error"),
        (502, BadGatewayError, "server_error"),
    ],
)
def test_error_status_code_mappings(
    status_code: int,
    error_class: type[MailChannelsError],
    error_type: str,
) -> None:
    """It maps common HTTP status codes to stable SDK error metadata."""
    response = SDKResponse(
        status_code,
        {"message": f"status {status_code} failed"},
        f"status {status_code} failed",
    )

    with pytest.raises(error_class) as error:
        raise_for_status(response)

    assert error.value.status_code == status_code
    assert error.value.error_type == error_type
    assert str(error.value) == f"status {status_code} failed"
    assert isinstance(error.value, ApiError)


@pytest.mark.parametrize(
    ("body", "text", "message"),
    [
        ({"error": "error field"}, "", "error field"),
        ({"detail": "detail field"}, "", "detail field"),
        ({"title": "title field"}, "", "title field"),
        ({}, "plain text fallback", "plain text fallback"),
        ({}, "", "MailChannels API request failed with status 400."),
    ],
)
def test_error_message_extraction(
    body: dict[str, str],
    text: str,
    message: str,
) -> None:
    """It extracts the most useful message from API error responses."""
    with pytest.raises(InvalidRequestError) as error:
        raise_for_status(SDKResponse(400, body, text))

    assert str(error.value) == message


@pytest.mark.parametrize(
    "header_name",
    [
        "X-Request-ID",
        "X-Request-Id",
        "Request-ID",
        "X-Correlation-ID",
        "X-Amzn-Trace-Id",
    ],
)
def test_request_id_header_variants(header_name: str) -> None:
    """It recognizes common request ID response headers."""
    with pytest.raises(ServerError) as error:
        raise_for_status(
            SDKResponse(
                500,
                {"message": "Server failed"},
                "Server failed",
                headers={header_name: "req_variant"},
            )
        )

    assert error.value.request_id == "req_variant"
