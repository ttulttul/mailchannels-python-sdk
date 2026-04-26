"""Retrieve MailChannels traffic metrics."""

from __future__ import annotations

import logging
import os
from typing import Any

import mailchannels
from mailchannels.metrics import MetricsSenderType

logger = logging.getLogger(__name__)


def retrieve_engagement_metrics(
    client: mailchannels.Client,
    *,
    start_time: str,
    end_time: str,
    campaign_id: str | None = None,
) -> dict[str, Any]:
    """Retrieve engagement metrics for a time window."""
    logger.info("Retrieving example engagement metrics")
    return client.metrics.engagement(
        start_time=start_time,
        end_time=end_time,
        campaign_id=campaign_id,
        interval="day",
    )


def retrieve_sender_metrics(
    client: mailchannels.Client,
    sender_type: MetricsSenderType,
) -> dict[str, Any]:
    """Retrieve sender metrics grouped by campaign or sub-account."""
    logger.info("Retrieving example sender metrics sender_type=%s", sender_type)
    return client.metrics.senders(
        sender_type,
        limit=50,
        offset=0,
        sort_order="desc",
    )


def main() -> None:
    """Run the metrics example from environment configuration."""
    client = mailchannels.Client(api_key=os.environ["MAILCHANNELS_API_KEY"])
    start_time = os.environ.get("MAILCHANNELS_METRICS_START", "2026-04-01")
    end_time = os.environ.get("MAILCHANNELS_METRICS_END", "2026-04-24T00:00:00Z")
    print(
        retrieve_engagement_metrics(
            client,
            start_time=start_time,
            end_time=end_time,
        )
    )


if __name__ == "__main__":
    main()
