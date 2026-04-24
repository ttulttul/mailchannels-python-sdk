"""MailChannels API client."""

from __future__ import annotations

import logging
import sys
from typing import Any
from urllib.parse import urljoin

from .exceptions import ConfigurationError
from .http_client import RequestsClient
from .http_client_async import HTTPXClient
from .response import raise_for_status

logger = logging.getLogger(__name__)

DEFAULT_BASE_URL = "https://api.mailchannels.net/tx/v1"


class Client:
    """Client for the MailChannels Email API."""

    def __init__(
        self,
        *,
        api_key: str | None = None,
        base_url: str = DEFAULT_BASE_URL,
        http_client: RequestsClient | None = None,
        async_http_client: HTTPXClient | None = None,
    ) -> None:
        """Create a MailChannels API client."""
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.http_client = http_client or RequestsClient()
        self.async_http_client = async_http_client or HTTPXClient()

        from .emails import EmailsResource
        from .sub_accounts import SubAccountsResource

        self.emails = EmailsResource(self)
        self.sub_accounts = SubAccountsResource(self)

    def request(
        self,
        method: str,
        path: str,
        *,
        json: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Send a synchronous API request."""
        response = self.http_client.request(
            method,
            self._url(path),
            headers=self._headers(),
            json=json,
            params=params,
        )
        raise_for_status(response)
        return response.data if isinstance(response.data, dict) else {}

    async def request_async(
        self,
        method: str,
        path: str,
        *,
        json: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Send an asynchronous API request."""
        response = await self.async_http_client.request(
            method,
            self._url(path),
            headers=self._headers(),
            json=json,
            params=params,
        )
        raise_for_status(response)
        return response.data if isinstance(response.data, dict) else {}

    def _headers(self) -> dict[str, str]:
        """Build API request headers."""
        api_key = self.api_key or _module_attr("api_key")
        if not api_key:
            logger.error("MailChannels API key is not configured")
            raise ConfigurationError(
                "Set `mailchannels.api_key` or pass `api_key` to "
                "`mailchannels.Client`.",
                code="MissingApiKey",
            )
        return {
            "X-Api-Key": str(api_key),
            "Content-Type": "application/json",
            "User-Agent": "mailchannels-python/0.1.0",
        }

    def _url(self, path: str) -> str:
        """Resolve an API path against this client's base URL."""
        base_url = str(_module_attr("base_url") or self.base_url).rstrip("/") + "/"
        resolved = urljoin(base_url, path.lstrip("/"))
        logger.debug("Resolved MailChannels URL path=%s url=%s", path, resolved)
        return resolved


def get_default_client() -> Client:
    """Create a client from module-level SDK configuration."""
    module_http_client = _module_attr("default_http_client")
    module_async_http_client = _module_attr("default_async_http_client")
    return Client(
        api_key=_module_attr("api_key"),
        base_url=str(_module_attr("base_url") or DEFAULT_BASE_URL),
        http_client=(
            module_http_client
            if isinstance(module_http_client, RequestsClient)
            else None
        ),
        async_http_client=(
            module_async_http_client
            if isinstance(module_async_http_client, HTTPXClient)
            else None
        ),
    )


def _module_attr(name: str) -> Any:
    """Read a mutable attribute from the top-level mailchannels module."""
    module = sys.modules.get("mailchannels")
    if module is None:
        return None
    return getattr(module, name, None)
