"""HTTP response helpers for the MailChannels SDK."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any

from .exceptions import (
    ApiError,
    AuthenticationError,
    BadGatewayError,
    ConflictError,
    ForbiddenError,
    PayloadTooLargeError,
)

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class SDKResponse:
    """Normalized HTTP response returned by SDK transports."""

    status_code: int
    data: Any
    text: str
    headers: dict[str, str] | None = None


class MailChannelsResponse(dict[str, Any]):
    """Dict response that also supports attribute-style access."""

    def __getattr__(self, name: str) -> Any:
        """Return a response value as an attribute."""
        try:
            return self[name]
        except KeyError as error:
            raise AttributeError(
                f"'{type(self).__name__}' object has no attribute '{name}'"
            ) from error


def response_data(response: SDKResponse) -> MailChannelsResponse:
    """Convert an SDK response into the public response object."""
    headers = dict(response.headers or {})
    if isinstance(response.data, dict):
        data = MailChannelsResponse(response.data)
        data["http_headers"] = headers
        return data
    if isinstance(response.data, list):
        return MailChannelsResponse({"data": response.data, "http_headers": headers})
    return MailChannelsResponse({"http_headers": headers})


def raise_for_status(response: SDKResponse) -> None:
    """Raise a typed SDK exception for non-success API responses."""
    if 200 <= response.status_code < 300:
        logger.debug(
            "MailChannels API response accepted status=%s",
            response.status_code,
        )
        return

    message = _error_message(response)
    logger.error(
        "MailChannels API request failed status=%s message=%s",
        response.status_code,
        message,
    )

    if response.status_code in {401, 403}:
        if response.status_code == 401:
            raise AuthenticationError(
                message,
                status_code=response.status_code,
                response=response.data,
                headers=response.headers,
            )
        raise ForbiddenError(
            message,
            status_code=response.status_code,
            response=response.data,
            headers=response.headers,
        )
    if response.status_code == 409:
        raise ConflictError(
            message,
            status_code=response.status_code,
            response=response.data,
            headers=response.headers,
        )
    if response.status_code == 413:
        raise PayloadTooLargeError(
            message,
            status_code=response.status_code,
            response=response.data,
            headers=response.headers,
        )
    if response.status_code == 502:
        raise BadGatewayError(
            message,
            status_code=response.status_code,
            response=response.data,
            headers=response.headers,
        )

    raise ApiError(
        message,
        status_code=response.status_code,
        response=response.data,
        headers=response.headers,
    )


def _error_message(response: SDKResponse) -> str:
    """Extract a useful message from a MailChannels response."""
    if isinstance(response.data, dict):
        for key in ("message", "error", "detail", "title"):
            value = response.data.get(key)
            if isinstance(value, str) and value:
                return value
    if response.text:
        return response.text
    return f"MailChannels API request failed with status {response.status_code}."
