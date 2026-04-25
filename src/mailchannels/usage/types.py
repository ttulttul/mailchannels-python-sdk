"""Usage response types."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class UsageStats(BaseModel):
    """MailChannels usage statistics for the current billing period."""

    model_config = ConfigDict(extra="allow")

    total_usage: int
    period_start_date: str | None = None
    period_end_date: str | None = None
