"""Sub-account request and response types."""

from __future__ import annotations

from typing import Any, TypedDict

from pydantic import BaseModel, ConfigDict
from typing_extensions import NotRequired

from ..exceptions import MailChannelsError


class CreateSubAccountParams(TypedDict, total=False):
    """Parameters for creating a MailChannels sub-account."""

    company_name: NotRequired[str]
    handle: NotRequired[str]


class SetLimitParams(TypedDict):
    """Parameters for setting a sub-account sending limit."""

    sends: int


class SubAccount(BaseModel):
    """MailChannels sub-account response model."""

    model_config = ConfigDict(extra="allow")

    handle: str | None = None
    company_name: str | None = None


class SubAccountLimit(BaseModel):
    """MailChannels sub-account sending limit response model."""

    model_config = ConfigDict(extra="allow")

    sends: int | None = None
    monthly_limit: int | None = None


class UsageStats(BaseModel):
    """MailChannels usage response model."""

    model_config = ConfigDict(extra="allow")


class ApiKey(BaseModel):
    """MailChannels sub-account API key response model."""

    model_config = ConfigDict(extra="allow")


class SmtpPassword(BaseModel):
    """MailChannels sub-account SMTP password response model."""

    model_config = ConfigDict(extra="allow")


def compact_payload(values: dict[str, Any]) -> dict[str, Any]:
    """Remove unset values from a request payload."""
    return {key: value for key, value in values.items() if value is not None}


def limit_payload(
    *,
    sends: int | None = None,
    monthly_limit: int | None = None,
) -> dict[str, int]:
    """Build the documented sub-account limit payload."""
    if sends is not None and monthly_limit is not None:
        raise MailChannelsError(
            "Pass either `sends` or `monthly_limit`, not both.",
            code="InvalidLimitParameters",
        )
    if sends is None and monthly_limit is None:
        raise MailChannelsError(
            "Pass `sends` to set a sub-account limit.",
            code="MissingLimitParameter",
        )
    limit = sends if sends is not None else monthly_limit
    if limit is None:
        raise MailChannelsError(
            "Pass `sends` to set a sub-account limit.",
            code="MissingLimitParameter",
        )
    return {"sends": limit}
