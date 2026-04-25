"""HTTP transport protocols for custom MailChannels clients."""

from __future__ import annotations

from typing import Any, Protocol

from .response import SDKResponse


class SyncHTTPClient(Protocol):
    """Protocol implemented by synchronous MailChannels HTTP transports."""

    def request(
        self,
        method: str,
        url: str,
        *,
        headers: dict[str, str],
        json: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
    ) -> SDKResponse:
        """Send an HTTP request and return a normalized SDK response."""


class AsyncHTTPClient(Protocol):
    """Protocol implemented by asynchronous MailChannels HTTP transports."""

    async def request(
        self,
        method: str,
        url: str,
        *,
        headers: dict[str, str],
        json: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
    ) -> SDKResponse:
        """Send an async HTTP request and return a normalized SDK response."""
