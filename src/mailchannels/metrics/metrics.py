"""Metrics resource implementation."""

from __future__ import annotations

import logging
from typing import Any

from ..query import compact_query
from .types import (
    MetricsInterval,
    MetricsSenderType,
    MetricsSortOrder,
    MetricsTime,
)

logger = logging.getLogger(__name__)


class MetricsResource:
    """Client-bound metrics operations."""

    def __init__(self, client: Any) -> None:
        """Create a metrics resource bound to a client."""
        self._client = client

    def engagement(
        self,
        *,
        start_time: MetricsTime | None = None,
        end_time: MetricsTime | None = None,
        campaign_id: str | None = None,
        interval: MetricsInterval | None = None,
    ) -> dict[str, Any]:
        """Retrieve engagement metrics."""
        logger.info("Retrieving MailChannels engagement metrics")
        return self._client.request(
            "GET",
            "/metrics/engagement",
            params=_time_series_query(start_time, end_time, campaign_id, interval),
        )

    async def engagement_async(
        self,
        *,
        start_time: MetricsTime | None = None,
        end_time: MetricsTime | None = None,
        campaign_id: str | None = None,
        interval: MetricsInterval | None = None,
    ) -> dict[str, Any]:
        """Retrieve engagement metrics using async HTTP."""
        logger.info("Retrieving MailChannels engagement metrics using async HTTP")
        return await self._client.request_async(
            "GET",
            "/metrics/engagement",
            params=_time_series_query(start_time, end_time, campaign_id, interval),
        )

    def performance(
        self,
        *,
        start_time: MetricsTime | None = None,
        end_time: MetricsTime | None = None,
        campaign_id: str | None = None,
        interval: MetricsInterval | None = None,
    ) -> dict[str, Any]:
        """Retrieve performance metrics."""
        logger.info("Retrieving MailChannels performance metrics")
        return self._client.request(
            "GET",
            "/metrics/performance",
            params=_time_series_query(start_time, end_time, campaign_id, interval),
        )

    async def performance_async(
        self,
        *,
        start_time: MetricsTime | None = None,
        end_time: MetricsTime | None = None,
        campaign_id: str | None = None,
        interval: MetricsInterval | None = None,
    ) -> dict[str, Any]:
        """Retrieve performance metrics using async HTTP."""
        logger.info("Retrieving MailChannels performance metrics using async HTTP")
        return await self._client.request_async(
            "GET",
            "/metrics/performance",
            params=_time_series_query(start_time, end_time, campaign_id, interval),
        )

    def recipient_behaviour(
        self,
        *,
        start_time: MetricsTime | None = None,
        end_time: MetricsTime | None = None,
        campaign_id: str | None = None,
        interval: MetricsInterval | None = None,
    ) -> dict[str, Any]:
        """Retrieve recipient behaviour metrics."""
        logger.info("Retrieving MailChannels recipient behaviour metrics")
        return self._client.request(
            "GET",
            "/metrics/recipient-behaviour",
            params=_time_series_query(start_time, end_time, campaign_id, interval),
        )

    async def recipient_behaviour_async(
        self,
        *,
        start_time: MetricsTime | None = None,
        end_time: MetricsTime | None = None,
        campaign_id: str | None = None,
        interval: MetricsInterval | None = None,
    ) -> dict[str, Any]:
        """Retrieve recipient behaviour metrics using async HTTP."""
        logger.info(
            "Retrieving MailChannels recipient behaviour metrics using async HTTP"
        )
        return await self._client.request_async(
            "GET",
            "/metrics/recipient-behaviour",
            params=_time_series_query(start_time, end_time, campaign_id, interval),
        )

    def recipient_behavior(
        self,
        *,
        start_time: MetricsTime | None = None,
        end_time: MetricsTime | None = None,
        campaign_id: str | None = None,
        interval: MetricsInterval | None = None,
    ) -> dict[str, Any]:
        """Retrieve recipient behaviour metrics using US spelling."""
        return self.recipient_behaviour(
            start_time=start_time,
            end_time=end_time,
            campaign_id=campaign_id,
            interval=interval,
        )

    async def recipient_behavior_async(
        self,
        *,
        start_time: MetricsTime | None = None,
        end_time: MetricsTime | None = None,
        campaign_id: str | None = None,
        interval: MetricsInterval | None = None,
    ) -> dict[str, Any]:
        """Retrieve recipient behaviour metrics using US spelling and async HTTP."""
        return await self.recipient_behaviour_async(
            start_time=start_time,
            end_time=end_time,
            campaign_id=campaign_id,
            interval=interval,
        )

    def volume(
        self,
        *,
        start_time: MetricsTime | None = None,
        end_time: MetricsTime | None = None,
        campaign_id: str | None = None,
        interval: MetricsInterval | None = None,
    ) -> dict[str, Any]:
        """Retrieve volume metrics."""
        logger.info("Retrieving MailChannels volume metrics")
        return self._client.request(
            "GET",
            "/metrics/volume",
            params=_time_series_query(start_time, end_time, campaign_id, interval),
        )

    async def volume_async(
        self,
        *,
        start_time: MetricsTime | None = None,
        end_time: MetricsTime | None = None,
        campaign_id: str | None = None,
        interval: MetricsInterval | None = None,
    ) -> dict[str, Any]:
        """Retrieve volume metrics using async HTTP."""
        logger.info("Retrieving MailChannels volume metrics using async HTTP")
        return await self._client.request_async(
            "GET",
            "/metrics/volume",
            params=_time_series_query(start_time, end_time, campaign_id, interval),
        )

    def senders(
        self,
        sender_type: MetricsSenderType,
        *,
        start_time: MetricsTime | None = None,
        end_time: MetricsTime | None = None,
        limit: int | None = None,
        offset: int | None = None,
        sort_order: MetricsSortOrder | None = None,
    ) -> dict[str, Any]:
        """Retrieve sender metrics grouped by campaigns or sub-accounts."""
        logger.info("Retrieving MailChannels sender metrics type=%s", sender_type)
        params = compact_query(
            {
                "start_time": start_time,
                "end_time": end_time,
                "limit": limit,
                "offset": offset,
                "sort_order": sort_order,
            }
        )
        return self._client.request(
            "GET",
            f"/metrics/senders/{sender_type}",
            params=params or None,
        )

    async def senders_async(
        self,
        sender_type: MetricsSenderType,
        *,
        start_time: MetricsTime | None = None,
        end_time: MetricsTime | None = None,
        limit: int | None = None,
        offset: int | None = None,
        sort_order: MetricsSortOrder | None = None,
    ) -> dict[str, Any]:
        """Retrieve sender metrics using async HTTP."""
        logger.info(
            "Retrieving MailChannels sender metrics using async HTTP type=%s",
            sender_type,
        )
        params = compact_query(
            {
                "start_time": start_time,
                "end_time": end_time,
                "limit": limit,
                "offset": offset,
                "sort_order": sort_order,
            }
        )
        return await self._client.request_async(
            "GET",
            f"/metrics/senders/{sender_type}",
            params=params or None,
        )


class Metrics:
    """Module-level metrics operations using global SDK configuration."""

    @classmethod
    def engagement(
        cls,
        *,
        start_time: MetricsTime | None = None,
        end_time: MetricsTime | None = None,
        campaign_id: str | None = None,
        interval: MetricsInterval | None = None,
    ) -> dict[str, Any]:
        """Retrieve engagement metrics."""
        from ..client import get_default_client

        return get_default_client().metrics.engagement(
            start_time=start_time,
            end_time=end_time,
            campaign_id=campaign_id,
            interval=interval,
        )

    @classmethod
    async def engagement_async(
        cls,
        *,
        start_time: MetricsTime | None = None,
        end_time: MetricsTime | None = None,
        campaign_id: str | None = None,
        interval: MetricsInterval | None = None,
    ) -> dict[str, Any]:
        """Retrieve engagement metrics using async HTTP."""
        from ..client import get_default_client

        return await get_default_client().metrics.engagement_async(
            start_time=start_time,
            end_time=end_time,
            campaign_id=campaign_id,
            interval=interval,
        )

    @classmethod
    def performance(
        cls,
        *,
        start_time: MetricsTime | None = None,
        end_time: MetricsTime | None = None,
        campaign_id: str | None = None,
        interval: MetricsInterval | None = None,
    ) -> dict[str, Any]:
        """Retrieve performance metrics."""
        from ..client import get_default_client

        return get_default_client().metrics.performance(
            start_time=start_time,
            end_time=end_time,
            campaign_id=campaign_id,
            interval=interval,
        )

    @classmethod
    async def performance_async(
        cls,
        *,
        start_time: MetricsTime | None = None,
        end_time: MetricsTime | None = None,
        campaign_id: str | None = None,
        interval: MetricsInterval | None = None,
    ) -> dict[str, Any]:
        """Retrieve performance metrics using async HTTP."""
        from ..client import get_default_client

        return await get_default_client().metrics.performance_async(
            start_time=start_time,
            end_time=end_time,
            campaign_id=campaign_id,
            interval=interval,
        )

    @classmethod
    def recipient_behaviour(
        cls,
        *,
        start_time: MetricsTime | None = None,
        end_time: MetricsTime | None = None,
        campaign_id: str | None = None,
        interval: MetricsInterval | None = None,
    ) -> dict[str, Any]:
        """Retrieve recipient behaviour metrics."""
        from ..client import get_default_client

        return get_default_client().metrics.recipient_behaviour(
            start_time=start_time,
            end_time=end_time,
            campaign_id=campaign_id,
            interval=interval,
        )

    @classmethod
    async def recipient_behaviour_async(
        cls,
        *,
        start_time: MetricsTime | None = None,
        end_time: MetricsTime | None = None,
        campaign_id: str | None = None,
        interval: MetricsInterval | None = None,
    ) -> dict[str, Any]:
        """Retrieve recipient behaviour metrics using async HTTP."""
        from ..client import get_default_client

        return await get_default_client().metrics.recipient_behaviour_async(
            start_time=start_time,
            end_time=end_time,
            campaign_id=campaign_id,
            interval=interval,
        )

    @classmethod
    def recipient_behavior(
        cls,
        *,
        start_time: MetricsTime | None = None,
        end_time: MetricsTime | None = None,
        campaign_id: str | None = None,
        interval: MetricsInterval | None = None,
    ) -> dict[str, Any]:
        """Retrieve recipient behaviour metrics using US spelling."""
        return cls.recipient_behaviour(
            start_time=start_time,
            end_time=end_time,
            campaign_id=campaign_id,
            interval=interval,
        )

    @classmethod
    async def recipient_behavior_async(
        cls,
        *,
        start_time: MetricsTime | None = None,
        end_time: MetricsTime | None = None,
        campaign_id: str | None = None,
        interval: MetricsInterval | None = None,
    ) -> dict[str, Any]:
        """Retrieve recipient behaviour metrics using US spelling and async HTTP."""
        return await cls.recipient_behaviour_async(
            start_time=start_time,
            end_time=end_time,
            campaign_id=campaign_id,
            interval=interval,
        )

    @classmethod
    def volume(
        cls,
        *,
        start_time: MetricsTime | None = None,
        end_time: MetricsTime | None = None,
        campaign_id: str | None = None,
        interval: MetricsInterval | None = None,
    ) -> dict[str, Any]:
        """Retrieve volume metrics."""
        from ..client import get_default_client

        return get_default_client().metrics.volume(
            start_time=start_time,
            end_time=end_time,
            campaign_id=campaign_id,
            interval=interval,
        )

    @classmethod
    async def volume_async(
        cls,
        *,
        start_time: MetricsTime | None = None,
        end_time: MetricsTime | None = None,
        campaign_id: str | None = None,
        interval: MetricsInterval | None = None,
    ) -> dict[str, Any]:
        """Retrieve volume metrics using async HTTP."""
        from ..client import get_default_client

        return await get_default_client().metrics.volume_async(
            start_time=start_time,
            end_time=end_time,
            campaign_id=campaign_id,
            interval=interval,
        )

    @classmethod
    def senders(
        cls,
        sender_type: MetricsSenderType,
        *,
        start_time: MetricsTime | None = None,
        end_time: MetricsTime | None = None,
        limit: int | None = None,
        offset: int | None = None,
        sort_order: MetricsSortOrder | None = None,
    ) -> dict[str, Any]:
        """Retrieve sender metrics grouped by campaigns or sub-accounts."""
        from ..client import get_default_client

        return get_default_client().metrics.senders(
            sender_type,
            start_time=start_time,
            end_time=end_time,
            limit=limit,
            offset=offset,
            sort_order=sort_order,
        )

    @classmethod
    async def senders_async(
        cls,
        sender_type: MetricsSenderType,
        *,
        start_time: MetricsTime | None = None,
        end_time: MetricsTime | None = None,
        limit: int | None = None,
        offset: int | None = None,
        sort_order: MetricsSortOrder | None = None,
    ) -> dict[str, Any]:
        """Retrieve sender metrics using async HTTP."""
        from ..client import get_default_client

        return await get_default_client().metrics.senders_async(
            sender_type,
            start_time=start_time,
            end_time=end_time,
            limit=limit,
            offset=offset,
            sort_order=sort_order,
        )


def _time_series_query(
    start_time: MetricsTime | None,
    end_time: MetricsTime | None,
    campaign_id: str | None,
    interval: MetricsInterval | None,
) -> dict[str, Any] | None:
    """Build query parameters for time-series metrics endpoints."""
    params = compact_query(
        {
            "start_time": start_time,
            "end_time": end_time,
            "campaign_id": campaign_id,
            "interval": interval,
        }
    )
    return params or None
