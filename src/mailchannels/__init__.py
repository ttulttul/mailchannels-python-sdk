"""Python SDK for the MailChannels Email API."""

from __future__ import annotations

import os

from .client import DEFAULT_BASE_URL, Client
from .dkim import Dkim
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
from .http_protocols import AsyncHTTPClient, SyncHTTPClient
from .metrics import Metrics
from .response import SDKResponse
from .sub_accounts import SubAccounts
from .suppressions import Suppressions
from .usage import Usage, UsageStats
from .version import __version__, get_version
from .webhooks import (
    SignatureParameters,
    WebhookEventPayload,
    Webhooks,
    parse_signature_input,
    signature_is_fresh,
    signature_key_id,
    verify_content_digest,
)

api_key: str | None = os.environ.get("MAILCHANNELS_API_KEY")
base_url: str = os.environ.get("MAILCHANNELS_API_URL", DEFAULT_BASE_URL)
default_http_client: RequestsClient | None = None
default_async_http_client: HTTPXClient | None = None

__all__ = [
    "ApiError",
    "AsyncHTTPClient",
    "AsyncClientNotConfigured",
    "Attachment",
    "AuthenticationError",
    "BadGatewayError",
    "Client",
    "ConfigurationError",
    "ConflictError",
    "Content",
    "Dkim",
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
    "SDKResponse",
    "SignatureParameters",
    "SubAccounts",
    "Suppressions",
    "SyncHTTPClient",
    "UNSUBSCRIBE_URL_PLACEHOLDER",
    "Usage",
    "UsageStats",
    "WebhookEventPayload",
    "Webhooks",
    "__version__",
    "api_key",
    "base_url",
    "default_async_http_client",
    "default_http_client",
    "get_version",
    "parse_signature_input",
    "signature_is_fresh",
    "signature_key_id",
    "verify_content_digest",
]
