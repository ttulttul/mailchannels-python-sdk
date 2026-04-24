"""Metrics request and response types."""

from __future__ import annotations

from datetime import date, datetime
from typing import Any, Literal, TypedDict

from pydantic import BaseModel, ConfigDict

MetricsInterval = Literal["hour", "day", "week", "month"]
MetricsSenderType = Literal["campaigns", "sub-accounts"]
MetricsSortOrder = Literal["asc", "desc"]
MetricsTime = str | date | datetime


class MetricsQueryParams(TypedDict, total=False):
    """Query parameters shared by time-series metrics endpoints."""

    start_time: MetricsTime
    end_time: MetricsTime
    campaign_id: str
    interval: MetricsInterval


class MetricsSenderQueryParams(TypedDict, total=False):
    """Query parameters for sender metrics endpoints."""

    start_time: MetricsTime
    end_time: MetricsTime
    limit: int
    offset: int
    sort_order: MetricsSortOrder


class MetricsBucket(BaseModel):
    """One time bucket in a metrics response."""

    count: int
    period_start: str


class MetricsEngagement(BaseModel):
    """Engagement metrics response model."""

    model_config = ConfigDict(extra="allow")

    open: int
    open_tracking_delivered: int
    click: int
    click_tracking_delivered: int
    buckets: dict[str, list[MetricsBucket]]


class MetricsPerformance(BaseModel):
    """Performance metrics response model."""

    model_config = ConfigDict(extra="allow")

    processed: int
    delivered: int
    bounced: int
    buckets: dict[str, list[MetricsBucket]]


class MetricsRecipientBehaviour(BaseModel):
    """Recipient behaviour metrics response model."""

    model_config = ConfigDict(extra="allow")

    unsubscribed: int
    unsubscribe_delivered: int
    buckets: dict[str, list[MetricsBucket]]


class MetricsVolume(BaseModel):
    """Volume metrics response model."""

    model_config = ConfigDict(extra="allow")

    processed: int
    delivered: int
    dropped: int
    buckets: dict[str, list[MetricsBucket]]


class MetricsSender(BaseModel):
    """One sender row in a sender metrics response."""

    name: str
    processed: int
    delivered: int
    dropped: int
    bounced: int


class MetricsSenderResponse(BaseModel):
    """Sender metrics response model."""

    model_config = ConfigDict(extra="allow")

    limit: int
    offset: int
    total: int
    senders: list[MetricsSender]


def compact_query(values: dict[str, Any]) -> dict[str, Any]:
    """Remove unset query values and serialize dates for HTTP requests."""
    return {
        key: _query_value(value)
        for key, value in values.items()
        if value is not None
    }


def _query_value(value: Any) -> Any:
    """Serialize a metrics query value."""
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, date):
        return value.isoformat()
    return value
