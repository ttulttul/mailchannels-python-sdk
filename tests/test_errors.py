"""Tests for API error handling."""

from __future__ import annotations

import pytest
from conftest import FakeRequestsClient

from mailchannels.client import Client
from mailchannels.exceptions import ConflictError, ForbiddenError, PayloadTooLargeError
from mailchannels.response import SDKResponse


def test_forbidden_response_raises_forbidden_error() -> None:
    """It maps 403 responses to ForbiddenError."""
    client = Client(
        api_key="test-key",
        http_client=FakeRequestsClient(
            SDKResponse(403, {"message": "Forbidden"}, "Forbidden"),
        ),
    )

    with pytest.raises(ForbiddenError):
        client.sub_accounts.create(handle="clienta")


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

    with pytest.raises(PayloadTooLargeError):
        client.emails.queue(
            {
                "from": {"email": "sender@example.com"},
                "to": "recipient@example.net",
                "subject": "Hello",
                "text": "Plain text",
            }
        )
