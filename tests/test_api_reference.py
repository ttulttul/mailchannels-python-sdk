"""Tests for API reference generation."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType
from typing import TypedDict

import mailchannels

ROOT = Path(__file__).resolve().parents[1]


def _load_generator_script() -> ModuleType:
    """Load the API reference generator script as a test module."""
    path = ROOT / "scripts" / "generate_api_reference.py"
    spec = importlib.util.spec_from_file_location("generate_api_reference", path)
    if spec is None or spec.loader is None:
        raise ImportError("Could not load API reference generator script.")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


reference = _load_generator_script()


def test_render_reference_includes_all_top_level_exports() -> None:
    """It documents every name exported from the top-level package."""
    report = reference.render_reference()

    for name in mailchannels.__all__:
        assert f"| `{name}` |" in report


def test_render_reference_includes_models_methods_and_examples() -> None:
    """It renders fields, method signatures, and practical examples."""
    report = reference.render_reference()

    assert "#### `mailchannels.EmailParams`" in report
    assert "| `personalizations` |" in report
    assert "#### `mailchannels.Emails`" in report
    assert (
        "`send(params: SendParamsType | EmailParams, *, "
        "dry_run: bool = False) -> dict[str, Any]`"
    ) in report
    assert "Example for `send`:" in report
    assert "mailchannels.Emails.send(" in report


def test_typed_dict_fields_do_not_evaluate_annotations() -> None:
    """It renders TypedDict annotations without evaluating version-specific syntax."""

    class FutureTypedDict(TypedDict):
        """TypedDict with an annotation that must remain unevaluated."""

        payload: str

    FutureTypedDict.__annotations__["payload"] = "list[str] | MissingRuntimeName"

    fields = reference._typed_dict_fields(FutureTypedDict)

    assert "| `payload` | `list[str] \\| MissingRuntimeName` | yes |" in fields


def test_api_reference_file_is_current() -> None:
    """The checked-in API reference matches the generator output."""
    expected = reference.render_reference()
    actual = (ROOT / "docs" / "API_REFERENCE.md").read_text(encoding="utf-8")

    assert actual == expected
