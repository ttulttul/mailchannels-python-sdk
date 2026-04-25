"""Tests for shared query helpers."""

from __future__ import annotations

from datetime import date, datetime, timezone

from mailchannels.query import compact_query, pagination_query


def test_compact_query_serializes_dates_and_lists() -> None:
    """It removes unset values and serializes common query types."""
    query = compact_query(
        {
            "created_after": date(2026, 4, 1),
            "created_before": datetime(2026, 4, 24, 12, 30, tzinfo=timezone.utc),
            "statuses": ["4xx", "5xx"],
            "unused": None,
        }
    )

    assert query == {
        "created_after": "2026-04-01",
        "created_before": "2026-04-24T12:30:00+00:00",
        "statuses": "4xx,5xx",
    }


def test_pagination_query_adds_limit_and_offset() -> None:
    """It combines filters with common pagination fields."""
    query = pagination_query(limit=100, offset=10, source="api")

    assert query == {"source": "api", "limit": 100, "offset": 10}
