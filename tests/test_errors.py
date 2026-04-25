"""Tests for API error handling."""

from __future__ import annotations

import pytest
from conftest import FakeRequestsClient

from mailchannels.client import Client
from mailchannels.exceptions import (
    ApiError,
    ConflictError,
    ForbiddenError,
    PayloadTooLargeError,
)
from mailchannels.response import SDKResponse


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

    with pytest.raises(ApiError) as error:
        client.metrics.volume()

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

    with pytest.raises(ApiError) as error:
        client.usage.retrieve()

    assert str(error.value) == "MailChannels API request failed with status 500."
