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
    ) -> None:
        """Initialize a MailChannels error."""
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.code = code
        self.response = response
        logger.debug(
            "Initialized MailChannelsError code=%s status=%s",
            code,
            status_code,
        )


class ConfigurationError(MailChannelsError):
    """Raised when SDK configuration is missing or invalid."""


class AuthenticationError(MailChannelsError):
    """Raised when MailChannels rejects authentication."""


class ForbiddenError(MailChannelsError):
    """Raised when an account cannot access a requested feature."""


class ConflictError(MailChannelsError):
    """Raised when MailChannels reports a resource conflict."""


class PayloadTooLargeError(MailChannelsError):
    """Raised when a request payload exceeds MailChannels limits."""


class BadGatewayError(MailChannelsError):
    """Raised when MailChannels returns a bad gateway response."""


class ApiError(MailChannelsError):
    """Raised for generic MailChannels API failures."""


class AsyncClientNotConfigured(ConfigurationError):
    """Raised when async support is requested without an async HTTP client."""
