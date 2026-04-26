"""Tests for API coverage report generation."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType

from pytest import MonkeyPatch

from mailchannels.routes import SDKRoute

ROOT = Path(__file__).resolve().parents[1]


def _load_generator_script() -> ModuleType:
    """Load the API coverage generator script as a test module."""
    path = ROOT / "scripts" / "generate_api_coverage.py"
    spec = importlib.util.spec_from_file_location("generate_api_coverage", path)
    if spec is None or spec.loader is None:
        raise ImportError("Could not load API coverage generator script.")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


coverage = _load_generator_script()


def test_spec_operations_extracts_sorted_operation_rows() -> None:
    """It extracts sorted operation rows from an OpenAPI document."""
    spec = {
        "paths": {
            "/usage": {"get": {"summary": "Usage"}},
            "/send": {"post": {"summary": "Send"}, "parameters": []},
        }
    }

    operations = coverage._spec_operations(spec)

    assert [operation.key for operation in operations] == [
        ("POST", "/send"),
        ("GET", "/usage"),
    ]
    assert operations[0].summary == "Send"


def test_render_report_marks_supported_and_pending_routes(
    monkeypatch: MonkeyPatch,
) -> None:
    """It renders supported SDK routes and pending OpenAPI operations."""
    monkeypatch.setattr(
        coverage,
        "SDK_ROUTES",
        (SDKRoute("POST", "/send", "Emails", "send"),),
    )
    spec = {
        "openapi": "3.0.0",
        "info": {"title": "MailChannels Email API", "version": "1.2.3"},
        "paths": {
            "/send": {"post": {"summary": "Send"}},
            "/future": {"get": {"summary": "Future"}},
        },
    }

    report = coverage.render_report(
        spec=spec,
        source="fixture.yaml",
        spec_hash="abc123",
        generated_at="2026-04-26T00:00:00+00:00",
    )

    assert "- SDK-supported operations: `1`" in report
    assert "- Pending OpenAPI operations: `1`" in report
    assert "| `POST` | `/send` | Send | `mailchannels.Emails.send()` |" in report
    assert (
        "| `GET` | `/future` | Future | pending | no | no | no | none | pending |"
        in report
    )
    assert "- OpenAPI version: `1.2.3`" in report


def test_render_report_lists_stale_sdk_routes(monkeypatch: MonkeyPatch) -> None:
    """It reports SDK routes that are absent from the OpenAPI document."""
    monkeypatch.setattr(
        coverage,
        "SDK_ROUTES",
        (SDKRoute("POST", "/stale", "Stale", "call"),),
    )
    spec = {
        "openapi": "3.0.0",
        "info": {"title": "MailChannels Email API", "version": "1.2.3"},
        "paths": {},
    }

    report = coverage.render_report(
        spec=spec,
        source="fixture.yaml",
        spec_hash="abc123",
        generated_at="2026-04-26T00:00:00+00:00",
    )

    assert "- SDK routes absent from OpenAPI: `1`" in report
    assert "## SDK Routes Absent From OpenAPI" in report
    assert "| `POST` | `/stale` | `mailchannels.Stale.call()` |" in report
