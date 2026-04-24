"""Python SDK for the MailChannels Email API."""

from __future__ import annotations

from .client import DEFAULT_BASE_URL, Client
from .emails import (
    UNSUBSCRIBE_URL_PLACEHOLDER,
    Attachment,
    Content,
    EmailAddress,
    EmailHeaders,
    EmailParams,
    Emails,
    Personalization,
    QueuedSendResponse,
    SendParams,
    SendResponse,
)
from .exceptions import (
    ApiError,
    AsyncClientNotConfigured,
    AuthenticationError,
    BadGatewayError,
    ConfigurationError,
    ConflictError,
    ForbiddenError,
    MailChannelsError,
    PayloadTooLargeError,
)
from .http_client import RequestsClient
from .http_client_async import HTTPXClient
from .metrics import Metrics
from .sub_accounts import SubAccounts

api_key: str | None = None
base_url: str = DEFAULT_BASE_URL
default_http_client: RequestsClient | None = None
default_async_http_client: HTTPXClient | None = None

__all__ = [
    "ApiError",
    "AsyncClientNotConfigured",
    "Attachment",
    "AuthenticationError",
    "BadGatewayError",
    "Client",
    "ConfigurationError",
    "ConflictError",
    "Content",
    "EmailAddress",
    "EmailHeaders",
    "EmailParams",
    "Emails",
    "ForbiddenError",
    "HTTPXClient",
    "MailChannelsError",
    "Metrics",
    "PayloadTooLargeError",
    "Personalization",
    "QueuedSendResponse",
    "RequestsClient",
    "SendParams",
    "SendResponse",
    "SubAccounts",
    "UNSUBSCRIBE_URL_PLACEHOLDER",
    "api_key",
    "base_url",
    "default_async_http_client",
    "default_http_client",
]
