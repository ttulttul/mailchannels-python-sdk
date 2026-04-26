"""Exceptions raised by the MailChannels SDK."""

from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger(__name__)


class MailChannelsError(Exception):
    """Base class for MailChannels SDK errors."""

    def __init__(
        self,
        message: str,
        *,
        status_code: int | None = None,
        code: str | None = None,
        response: Any | None = None,
        headers: dict[str, str] | None = None,
        error_type: str | None = None,
        request_id: str | None = None,
        suggested_action: str | None = None,
    ) -> None:
        """Initialize a MailChannels error."""
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.code = code
        self.response = response
        self.headers = dict(headers or {})
        self.error_type = error_type or _error_type(code, status_code)
        self.request_id = request_id or _request_id(self.headers)
        self.retry_after = self.headers.get("Retry-After")
        self.suggested_action = suggested_action or _suggested_action(
            code,
            status_code,
        )
        logger.debug(
            "Initialized MailChannelsError code=%s status=%s request_id=%s",
            code,
            status_code,
            self.request_id,
        )

    def to_dict(self) -> dict[str, Any]:
        """Return structured metadata for logging or diagnostics."""
        return {
            "message": self.message,
            "status_code": self.status_code,
            "code": self.code,
            "error_type": self.error_type,
            "request_id": self.request_id,
            "retry_after": self.retry_after,
            "suggested_action": self.suggested_action,
            "headers": self.headers,
            "response": self.response,
        }


class ConfigurationError(MailChannelsError):
    """Raised when SDK configuration is missing or invalid."""


class ApiError(MailChannelsError):
    """Raised for MailChannels API failures."""


class AuthenticationError(ApiError):
    """Raised when MailChannels rejects authentication."""


class ForbiddenError(ApiError):
    """Raised when an account cannot access a requested feature."""


class ConflictError(ApiError):
    """Raised when MailChannels reports a resource conflict."""


class PayloadTooLargeError(ApiError):
    """Raised when a request payload exceeds MailChannels limits."""


class RateLimitError(ApiError):
    """Raised when MailChannels asks the caller to slow down."""


class InvalidRequestError(ApiError):
    """Raised when MailChannels rejects request parameters or payload shape."""


class ServerError(ApiError):
    """Raised when MailChannels returns a server-side failure."""


class BadGatewayError(ServerError):
    """Raised when MailChannels returns a bad gateway response."""


class ResponseValidationError(MailChannelsError):
    """Raised when strict response validation fails."""


class AsyncClientNotConfigured(ConfigurationError):
    """Raised when async support is requested without an async HTTP client."""


def _request_id(headers: dict[str, str]) -> str | None:
    """Extract a request identifier from response headers."""
    request_id_headers = (
        "X-Request-ID",
        "X-Request-Id",
        "Request-ID",
        "X-Correlation-ID",
        "X-Amzn-Trace-Id",
    )
    lowered = {key.lower(): value for key, value in headers.items()}
    for header in request_id_headers:
        value = lowered.get(header.lower())
        if value:
            return value
    return None


def _error_type(code: str | None, status_code: int | None) -> str | None:
    """Return a stable error type for diagnostics."""
    if code == "ResponseValidationError":
        return "response_validation_error"
    if code:
        return code
    if status_code is None:
        return None
    if status_code == 401:
        return "authentication_error"
    if status_code == 403:
        return "permission_error"
    if status_code == 409:
        return "conflict_error"
    if status_code == 413:
        return "payload_too_large"
    if status_code == 429:
        return "rate_limit_error"
    if 500 <= status_code:
        return "server_error"
    if 400 <= status_code:
        return "invalid_request_error"
    return "api_error"


def _suggested_action(code: str | None, status_code: int | None) -> str | None:
    """Return a concise remediation hint for common failures."""
    if code == "MissingApiKey":
        return "Configure MAILCHANNELS_API_KEY or pass api_key to Client."
    if status_code == 401:
        return "Check that the MailChannels API key is valid."
    if status_code == 403:
        return "Confirm the API key has access to this MailChannels resource."
    if status_code == 409:
        return "Use the existing resource or retry with a unique identifier."
    if status_code == 413:
        return "Reduce message size or attachment payload before retrying."
    if code == "ResponseValidationError":
        return "Inspect the API response shape and SDK response model."
    if status_code == 429:
        return "Back off before retrying; inspect Retry-After if present."
    if status_code is not None and 500 <= status_code:
        return "Retry later or contact MailChannels support with the request ID."
    return None
