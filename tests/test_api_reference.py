"""Tests for API reference generation."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType
from typing import Literal, Optional, TypedDict, Union

import pytest

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
        "dry_run: bool = False) -> SendResponse | MailChannelsResponse`"
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


def test_generic_alias_exports_are_not_rendered_as_classes(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """It renders built-in generic aliases consistently across Python versions."""
    original_isclass = reference.inspect.isclass

    def version_variant_isclass(value: object) -> bool:
        """Simulate Python versions where generic aliases appear class-like."""
        if value is mailchannels.EmailHeaders:
            return True
        return original_isclass(value)

    monkeypatch.setattr(reference.inspect, "isclass", version_variant_isclass)

    assert reference._kind(mailchannels.EmailHeaders) == "value"
    assert (
        reference._summary(
            mailchannels.EmailHeaders,
            qualified_name="mailchannels.EmailHeaders",
        )
        == "Custom email header mapping accepted by send payloads."
    )
    assert reference._signature(mailchannels.EmailHeaders) == ""


def test_value_exports_have_summary_overrides() -> None:
    """It documents important value exports that do not have docstrings."""
    report = reference.render_reference()

    expected_rows = [
        (
            "| `API_SPEC_COMPATIBILITY` | `value` | "
            "MailChannels OpenAPI document metadata targeted by this SDK release. |"
        ),
        (
            "| `UNSUBSCRIBE_URL_PLACEHOLDER` | `constant` | "
            "Mustache placeholder for MailChannels-hosted one-click "
            "unsubscribe URLs. |"
        ),
        (
            "| `strict_responses` | `value` | "
            "Module-level flag that enables strict Pydantic response models. |"
        ),
    ]

    for row in expected_rows:
        assert row in report


def test_format_annotation_normalizes_older_typing_forms() -> None:
    """It keeps rendered annotations stable across Python versions."""
    assert reference._format_annotation(Optional[str]) == "str | None"
    assert reference._format_annotation(Literal["passed", "failed"]) == "Literal"
    assert reference._format_annotation(Union[Literal["open"], str]) == "Union"


def test_pydantic_fields_render_source_annotations() -> None:
    """It avoids Python-version-specific evaluated Pydantic annotations."""
    fields = reference._pydantic_model_fields(mailchannels.EmailParams)

    assert "| `headers` | `EmailHeaders \\| None` | no | `None` |" in fields


def test_api_reference_file_is_current() -> None:
    """The checked-in API reference matches the generator output."""
    expected = reference.render_reference()
    actual = (ROOT / "docs" / "API_REFERENCE.md").read_text(encoding="utf-8")

    assert actual == expected
