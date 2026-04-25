"""Tests for the OpenAPI drift checker."""

from __future__ import annotations

import importlib.util
from pathlib import Path
from types import ModuleType

from pytest import MonkeyPatch

from mailchannels.routes import SDKRoute

ROOT = Path(__file__).resolve().parents[1]


def _load_drift_script() -> ModuleType:
    """Load the OpenAPI drift checker script as a test module."""
    path = ROOT / "scripts" / "check_openapi_drift.py"
    spec = importlib.util.spec_from_file_location("check_openapi_drift", path)
    if spec is None or spec.loader is None:
        raise ImportError("Could not load OpenAPI drift checker script.")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


drift = _load_drift_script()


def test_spec_route_keys_extracts_methods() -> None:
    """It extracts HTTP method and path pairs from an OpenAPI document."""
    spec = {
        "paths": {
            "/send": {"post": {"summary": "Send"}, "parameters": []},
            "/usage": {"get": {"summary": "Usage"}},
        }
    }

    assert drift._spec_route_keys(spec) == {("POST", "/send"), ("GET", "/usage")}


def test_missing_routes_reports_absent_sdk_routes(monkeypatch: MonkeyPatch) -> None:
    """It reports SDK routes not present in the supplied OpenAPI routes."""
    monkeypatch.setattr(
        drift,
        "SDK_ROUTES",
        (
            SDKRoute("POST", "/send", "Emails", "send"),
            SDKRoute("POST", "/missing", "Missing", "missing"),
        ),
    )

    missing = drift._missing_routes({("POST", "/send")})

    assert missing == [SDKRoute("POST", "/missing", "Missing", "missing")]
