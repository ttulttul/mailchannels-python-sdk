"""Synchronous HTTP transport for the MailChannels SDK."""

from __future__ import annotations

import logging
from typing import Any

import requests

from .response import SDKResponse

logger = logging.getLogger(__name__)


class RequestsClient:
    """Synchronous HTTP client backed by requests."""

    def __init__(self, *, timeout: float = 30.0) -> None:
        """Create a requests-backed HTTP client."""
        self.timeout = timeout

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
        logger.info("Sending MailChannels request method=%s url=%s", method, url)
        response = requests.request(
            method,
            url,
            headers=headers,
            json=json,
            params=params,
            timeout=self.timeout,
        )
        try:
            data: Any = response.json()
        except requests.JSONDecodeError:
            logger.debug(
                "MailChannels response was not JSON status=%s",
                response.status_code,
            )
            data = None
        return SDKResponse(
            status_code=response.status_code,
            data=data,
            text=response.text,
        )
