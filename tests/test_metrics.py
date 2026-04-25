"""Tests for metrics resources."""

from __future__ import annotations

from datetime import date, datetime, timezone

import pytest
from conftest import FakeHTTPXClient, FakeRequestsClient

import mailchannels
from mailchannels.client import Client
from mailchannels.response import SDKResponse


def test_engagement_metrics_uses_expected_path_and_query() -> None:
    """It retrieves engagement metrics with time range and campaign filters."""
    transport = FakeRequestsClient(
        SDKResponse(
            200,
            {
                "open": 1,
                "open_tracking_delivered": 2,
                "click": 3,
                "click_tracking_delivered": 4,
                "buckets": {
                    "open": [],
                    "open_tracking_delivered": [],
                    "click": [],
                    "click_tracking_delivered": [],
                },
            },
            "{}",
        )
    )
    client = Client(api_key="test-key", http_client=transport)

    result = client.metrics.engagement(
        start_time=date(2026, 4, 1),
        end_time=datetime(2026, 4, 24, 12, 30, tzinfo=timezone.utc),
        campaign_id="newsletter",
        interval="day",
    )

    assert result["open"] == 1
    assert transport.calls[0]["method"] == "GET"
    assert transport.calls[0]["url"] == (
        "https://api.mailchannels.net/tx/v1/metrics/engagement"
    )
    assert transport.calls[0]["params"] == {
        "start_time": "2026-04-01",
        "end_time": "2026-04-24T12:30:00+00:00",
        "campaign_id": "newsletter",
        "interval": "day",
    }


def test_metrics_time_series_endpoints_use_documented_paths() -> None:
    """It exposes performance, recipient behaviour, and volume endpoints."""
    transport = FakeRequestsClient(SDKResponse(200, {"ok": True}, "{}"))
    client = Client(api_key="test-key", http_client=transport)

    client.metrics.performance(start_time="2026-04-01", interval="week")
    client.metrics.recipient_behaviour(campaign_id="newsletter")
    client.metrics.recipient_behavior(campaign_id="newsletter-us")
    client.metrics.volume(end_time="2026-04-24T00:00:00Z")

    assert [call["url"] for call in transport.calls] == [
        "https://api.mailchannels.net/tx/v1/metrics/performance",
        "https://api.mailchannels.net/tx/v1/metrics/recipient-behaviour",
        "https://api.mailchannels.net/tx/v1/metrics/recipient-behaviour",
        "https://api.mailchannels.net/tx/v1/metrics/volume",
    ]
    assert transport.calls[0]["params"] == {
        "start_time": "2026-04-01",
        "interval": "week",
    }
    assert transport.calls[1]["params"] == {"campaign_id": "newsletter"}
    assert transport.calls[2]["params"] == {"campaign_id": "newsletter-us"}
    assert transport.calls[3]["params"] == {"end_time": "2026-04-24T00:00:00Z"}


def test_sender_metrics_uses_sender_type_path_and_pagination_query() -> None:
    """It retrieves sender metrics grouped by campaign or sub-account."""
    transport = FakeRequestsClient(
        SDKResponse(
            200,
            {
                "senders": [
                    {
                        "name": "campaign_123",
                        "processed": 10,
                        "delivered": 9,
                        "dropped": 0,
                        "bounced": 1,
                    }
                ],
                "limit": 50,
                "offset": 0,
                "total": 1,
            },
            "{}",
        )
    )
    client = Client(api_key="test-key", http_client=transport)

    result = client.metrics.senders(
        "campaigns",
        start_time="2026-04-01",
        end_time="2026-04-24",
        limit=50,
        offset=0,
        sort_order="desc",
    )

    assert result["total"] == 1
    assert transport.calls[0]["url"] == (
        "https://api.mailchannels.net/tx/v1/metrics/senders/campaigns"
    )
    assert transport.calls[0]["params"] == {
        "start_time": "2026-04-01",
        "end_time": "2026-04-24",
        "limit": 50,
        "offset": 0,
        "sort_order": "desc",
    }


def test_module_level_metrics_api_uses_global_configuration(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """It supports module-level metrics calls."""
    transport = FakeRequestsClient(SDKResponse(200, {"processed": 1}, "{}"))
    monkeypatch.setattr(mailchannels, "api_key", "module-key")
    monkeypatch.setattr(mailchannels, "default_http_client", transport)

    mailchannels.Metrics.volume(campaign_id="newsletter")

    assert transport.calls[0]["headers"]["X-Api-Key"] == "module-key"
    assert transport.calls[0]["url"] == (
        "https://api.mailchannels.net/tx/v1/metrics/volume"
    )
    assert transport.calls[0]["params"] == {"campaign_id": "newsletter"}


async def test_metrics_async_methods_use_async_transport() -> None:
    """It exposes async metrics operations."""
    transport = FakeHTTPXClient(SDKResponse(200, {"processed": 1}, "{}"))
    client = Client(api_key="test-key", async_http_client=transport)

    await client.metrics.volume_async(campaign_id="newsletter")

    assert transport.calls[0]["method"] == "GET"
    assert transport.calls[0]["url"] == (
        "https://api.mailchannels.net/tx/v1/metrics/volume"
    )
    assert transport.calls[0]["params"] == {"campaign_id": "newsletter"}
