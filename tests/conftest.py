"""Shared pytest fixtures and fakes."""

from __future__ import annotations

import os
from typing import Any

import pytest

from mailchannels.http_client import RequestsClient
from mailchannels.http_client_async import HTTPXClient
from mailchannels.response import SDKResponse


def pytest_addoption(parser: pytest.Parser) -> None:
    """Add command-line options for the test suite."""
    parser.addoption(
        "--online",
        action="store_true",
        default=False,
        help="Run tests that call the live MailChannels Email API.",
    )


def pytest_collection_modifyitems(
    config: pytest.Config,
    items: list[pytest.Item],
) -> None:
    """Skip online tests unless explicitly enabled and configured."""
    if config.getoption("--online") and os.environ.get("MAILCHANNELS_API_KEY"):
        return

    reason = (
        "set MAILCHANNELS_API_KEY and pass --online to run live MailChannels API tests"
    )
    skip_online = pytest.mark.skip(reason=reason)
    for item in items:
        if "online" in item.keywords:
            item.add_marker(skip_online)


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
