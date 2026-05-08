"""MailChannels API client."""

from __future__ import annotations

import logging
import os
import sys
from typing import Any, Generic, Literal, TypeVar, overload
from urllib.parse import urljoin

from .exceptions import ConfigurationError
from .http_client import RequestsClient
from .http_client_async import HTTPXClient
from .http_protocols import AsyncHTTPClient, SyncHTTPClient
from .response import (
    ResponseModel,
    raise_for_status,
    response_data,
    response_model_data,
)
from .version import user_agent

logger = logging.getLogger(__name__)

DEFAULT_BASE_URL = "https://api.mailchannels.net/tx/v1"
StrictResponses = TypeVar("StrictResponses", bound=bool)


class Client(Generic[StrictResponses]):
    """Client for the MailChannels Email API."""

    @overload
    def __init__(
        self: Client[Literal[False]],
        *,
        api_key: str | None = None,
        base_url: str | None = None,
        http_client: SyncHTTPClient | None = None,
        async_http_client: AsyncHTTPClient | None = None,
        strict_responses: Literal[False] = False,
    ) -> None: ...

    @overload
    def __init__(
        self: Client[Literal[True]],
        *,
        api_key: str | None = None,
        base_url: str | None = None,
        http_client: SyncHTTPClient | None = None,
        async_http_client: AsyncHTTPClient | None = None,
        strict_responses: Literal[True],
    ) -> None: ...

    @overload
    def __init__(
        self: Client[bool],
        *,
        api_key: str | None = None,
        base_url: str | None = None,
        http_client: SyncHTTPClient | None = None,
        async_http_client: AsyncHTTPClient | None = None,
        strict_responses: bool,
    ) -> None: ...

    def __init__(
        self,
        *,
        api_key: str | None = None,
        base_url: str | None = None,
        http_client: SyncHTTPClient | None = None,
        async_http_client: AsyncHTTPClient | None = None,
        strict_responses: bool = False,
    ) -> None:
        """Create a MailChannels API client."""
        self.api_key = api_key
        self.base_url = (base_url or _configured_base_url()).rstrip("/")
        self.http_client = http_client or RequestsClient()
        self.async_http_client = async_http_client or HTTPXClient()
        self.strict_responses = strict_responses

        from .dkim import DkimResource
        from .domain_checks import DomainChecksResource
        from .emails import EmailsResource
        from .metrics import MetricsResource
        from .sub_accounts import SubAccountsResource
        from .suppressions import SuppressionsResource
        from .usage import UsageResource
        from .webhooks import WebhooksResource

        self.dkim: DkimResource[StrictResponses] = DkimResource(self)
        self.domain_checks: DomainChecksResource[StrictResponses] = (
            DomainChecksResource(self)
        )
        self.check_domain = self.domain_checks
        self.emails: EmailsResource[StrictResponses] = EmailsResource(self)
        self.metrics: MetricsResource[StrictResponses] = MetricsResource(self)
        self.suppressions: SuppressionsResource[StrictResponses] = (
            SuppressionsResource(self)
        )
        self.sub_accounts: SubAccountsResource[StrictResponses] = SubAccountsResource(
            self
        )
        self.usage: UsageResource[StrictResponses] = UsageResource(self)
        self.webhooks: WebhooksResource[StrictResponses] = WebhooksResource(self)

    def request(
        self,
        method: str,
        path: str,
        *,
        json: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        extra_headers: dict[str, str] | None = None,
        require_api_key: bool = True,
        response_model: type[ResponseModel] | None = None,
    ) -> Any:
        """Send a synchronous API request."""
        response = self.http_client.request(
            method,
            self._url(path),
            headers=self._headers(
                extra_headers=extra_headers,
                require_api_key=require_api_key,
            ),
            json=json,
            params=params,
        )
        raise_for_status(response)
        if self.strict_responses and response_model is not None:
            return response_model_data(response, response_model)
        return response_data(response)

    async def request_async(
        self,
        method: str,
        path: str,
        *,
        json: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        extra_headers: dict[str, str] | None = None,
        require_api_key: bool = True,
        response_model: type[ResponseModel] | None = None,
    ) -> Any:
        """Send an asynchronous API request."""
        response = await self.async_http_client.request(
            method,
            self._url(path),
            headers=self._headers(
                extra_headers=extra_headers,
                require_api_key=require_api_key,
            ),
            json=json,
            params=params,
        )
        raise_for_status(response)
        if self.strict_responses and response_model is not None:
            return response_model_data(response, response_model)
        return response_data(response)

    def _headers(
        self,
        *,
        extra_headers: dict[str, str] | None = None,
        require_api_key: bool = True,
    ) -> dict[str, str]:
        """Build API request headers."""
        api_key = self.api_key or _module_attr("api_key") or os.environ.get(
            "MAILCHANNELS_API_KEY"
        )
        if require_api_key and not api_key:
            logger.error("MailChannels API key is not configured")
            raise ConfigurationError(
                "Set `mailchannels.api_key` or pass `api_key` to "
                "`mailchannels.Client`.",
                code="MissingApiKey",
            )
        headers = {
            "Content-Type": "application/json",
            "User-Agent": user_agent(),
        }
        if require_api_key and api_key:
            headers["X-Api-Key"] = str(api_key)
        if extra_headers:
            headers.update(extra_headers)
        return headers

    def _url(self, path: str) -> str:
        """Resolve an API path against this client's base URL."""
        base_url = self.base_url.rstrip("/") + "/"
        resolved = urljoin(base_url, path.lstrip("/"))
        logger.debug("Resolved MailChannels URL path=%s url=%s", path, resolved)
        return resolved

    def close(self) -> None:
        """Close owned synchronous transport resources when supported."""
        close = getattr(self.http_client, "close", None)
        if callable(close):
            logger.debug("Closing MailChannels sync transport")
            close()

    async def aclose(self) -> None:
        """Close owned asynchronous transport resources when supported."""
        aclose = getattr(self.async_http_client, "aclose", None)
        if callable(aclose):
            logger.debug("Closing MailChannels async transport")
            await aclose()

    def __enter__(self) -> Client:
        """Enter a synchronous client context."""
        return self

    def __exit__(self, *args: object) -> None:
        """Close sync transport resources when leaving a client context."""
        self.close()

    async def __aenter__(self) -> Client:
        """Enter an asynchronous client context."""
        return self

    async def __aexit__(self, *args: object) -> None:
        """Close async transport resources when leaving a client context."""
        await self.aclose()


def get_default_client() -> Client[bool]:
    """Create a client from module-level SDK configuration."""
    module_http_client = _module_attr("default_http_client")
    module_async_http_client = _module_attr("default_async_http_client")
    return Client(
        api_key=_module_attr("api_key") or os.environ.get("MAILCHANNELS_API_KEY"),
        base_url=str(_module_attr("base_url") or _configured_base_url()),
        http_client=module_http_client if _has_request(module_http_client) else None,
        async_http_client=(
            module_async_http_client if _has_request(module_async_http_client) else None
        ),
        strict_responses=bool(_module_attr("strict_responses")),
    )


def _module_attr(name: str) -> Any:
    """Read a mutable attribute from the top-level mailchannels module."""
    module = sys.modules.get("mailchannels")
    if module is None:
        return None
    return getattr(module, name, None)


def _configured_base_url() -> str:
    """Return the configured MailChannels API base URL."""
    return os.environ.get("MAILCHANNELS_API_URL", DEFAULT_BASE_URL)


def _has_request(value: Any) -> bool:
    """Return whether a value has the request method required by transports."""
    return value is not None and callable(getattr(value, "request", None))
