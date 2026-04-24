"""Shared pytest fixtures and fakes."""

from __future__ import annotations

from typing import Any

from mailchannels.http_client import RequestsClient
from mailchannels.http_client_async import HTTPXClient
from mailchannels.response import SDKResponse


class FakeRequestsClient(RequestsClient):
    """Fake sync transport for tests."""

    def __init__(self, response: SDKResponse | None = None) -> None:
        """Create a fake sync transport."""
        super().__init__()
        self.response = response or SDKResponse(202, {"id": "queued_123"}, "{}")
        self.calls: list[dict[str, Any]] = []

    def request(
        self,
        method: str,
        url: str,
        *,
        headers: dict[str, str],
        json: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
    ) -> SDKResponse:
        """Record a request and return the configured response."""
        self.calls.append(
            {
                "method": method,
                "url": url,
                "headers": headers,
                "json": json,
                "params": params,
            }
        )
        return self.response


class FakeHTTPXClient(HTTPXClient):
    """Fake async transport for tests."""

    def __init__(self, response: SDKResponse | None = None) -> None:
        """Create a fake async transport."""
        super().__init__()
        self.response = response or SDKResponse(202, {"id": "queued_123"}, "{}")
        self.calls: list[dict[str, Any]] = []

    async def request(
        self,
        method: str,
        url: str,
        *,
        headers: dict[str, str],
        json: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
    ) -> SDKResponse:
        """Record an async request and return the configured response."""
        self.calls.append(
            {
                "method": method,
                "url": url,
                "headers": headers,
                "json": json,
                "params": params,
            }
        )
        return self.response
