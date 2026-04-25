"""Asynchronous HTTP transport for the MailChannels SDK."""

from __future__ import annotations

import logging
from typing import Any

from .exceptions import AsyncClientNotConfigured
from .response import SDKResponse

logger = logging.getLogger(__name__)


class HTTPXClient:
    """Asynchronous HTTP client backed by httpx.

    Custom asynchronous transports should implement the same async `request()`
    method described by `mailchannels.AsyncHTTPClient`.
    """

    def __init__(self, *, timeout: float = 30.0) -> None:
        """Create an httpx-backed async HTTP client."""
        self.timeout = timeout

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
        try:
            import httpx
        except ImportError as error:
            logger.error("httpx is required for async MailChannels requests")
            raise AsyncClientNotConfigured(
                'Install async support with `pip install "mailchannels[async]"`.',
                code="AsyncClientNotConfigured",
            ) from error

        logger.info("Sending async MailChannels request method=%s url=%s", method, url)
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.request(
                method,
                url,
                headers=headers,
                json=json,
                params=params,
            )
        try:
            data: Any = response.json()
        except ValueError:
            logger.debug(
                "MailChannels async response was not JSON status=%s",
                response.status_code,
            )
            data = None
        return SDKResponse(
            status_code=response.status_code,
            data=data,
            text=response.text,
            headers=dict(response.headers),
        )
