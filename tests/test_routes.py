"""Tests for SDK route declarations."""

from __future__ import annotations

from mailchannels.routes import SDK_ROUTES, sdk_route_keys


def test_sdk_routes_are_unique() -> None:
    """Route declarations should not contain duplicate method/path pairs."""
    assert len(sdk_route_keys()) == len(SDK_ROUTES)


def test_sdk_routes_include_recent_conformance_fixes() -> None:
    """Route declarations include endpoints that previously drifted or were missing."""
    routes = sdk_route_keys()

    assert ("PUT", "/sub-account/{handle}/limit") in routes
    assert ("GET", "/sub-account/{handle}/limit") in routes
    assert ("DELETE", "/sub-account/{handle}/limit") in routes
    assert ("POST", "/check-domain") in routes
    assert ("POST", "/sub-account/{handle}/limits") not in routes
