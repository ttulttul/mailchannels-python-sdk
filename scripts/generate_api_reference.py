"""Generate the MailChannels SDK API reference."""

from __future__ import annotations

import argparse
import inspect
import re
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from types import ModuleType
from typing import Any

from pydantic import BaseModel

import mailchannels
import mailchannels.check_domain
import mailchannels.dkim
import mailchannels.domain_checks
import mailchannels.emails
import mailchannels.metrics
import mailchannels.sub_accounts
import mailchannels.suppressions
import mailchannels.usage
import mailchannels.webhooks

DEFAULT_OUTPUT_PATH = Path("docs/API_REFERENCE.md")
PUBLIC_MODULES = (
    mailchannels,
    mailchannels.emails,
    mailchannels.domain_checks,
    mailchannels.check_domain,
    mailchannels.dkim,
    mailchannels.metrics,
    mailchannels.sub_accounts,
    mailchannels.suppressions,
    mailchannels.usage,
    mailchannels.webhooks,
)
METHOD_EXAMPLES = {
    "mailchannels.Emails.send": (
        'mailchannels.Emails.send({"from": {"email": "sender@example.com"}, '
        '"to": "recipient@example.net", "subject": "Hello", "text": "Hello"})'
    ),
    "mailchannels.Emails.queue": (
        'mailchannels.Emails.queue({"from": {"email": "sender@example.com"}, '
        '"to": "recipient@example.net", "subject": "Queued", "text": "Hello"})'
    ),
    "mailchannels.CheckDomain.check": (
        'mailchannels.CheckDomain.check("example.com")'
    ),
    "mailchannels.Dkim.create": (
        'mailchannels.Dkim.create("example.com", selector="mcdkim")'
    ),
    "mailchannels.Metrics.volume": (
        'mailchannels.Metrics.volume(start_time="2026-04-01", interval="day")'
    ),
    "mailchannels.SubAccounts.create": (
        'mailchannels.SubAccounts.create(company_name="Client A", handle="clienta")'
    ),
    "mailchannels.Suppressions.list": (
        'mailchannels.Suppressions.list(source="api", limit=100)'
    ),
    "mailchannels.Usage.retrieve": "mailchannels.Usage.retrieve()",
    "mailchannels.Webhooks.list": "mailchannels.Webhooks.list()",
}


@dataclass(frozen=True)
class PublicObject:
    """One object exported from a public SDK module."""

    module: ModuleType
    name: str
    value: Any

    @property
    def qualified_name(self) -> str:
        """Return the fully qualified export name."""
        return f"{self.module.__name__}.{self.name}"


@dataclass(frozen=True)
class PublicMethod:
    """One public method on a public class."""

    name: str
    signature: str
    doc: str
    kind: str


def main() -> int:
    """Generate the API reference Markdown file."""
    args = _parser().parse_args()
    reference = render_reference(PUBLIC_MODULES)
    args.output.write_text(reference, encoding="utf-8")
    print(f"Wrote API reference to {args.output}")
    return 0


def render_reference(modules: Iterable[ModuleType] = PUBLIC_MODULES) -> str:
    """Render the public API reference as Markdown."""
    objects = _public_objects(modules)
    lines = [
        "# MailChannels Python SDK API Reference",
        "",
        "This reference is generated from public SDK exports, type hints, "
        "Pydantic models, and docstrings in `src/mailchannels`.",
        "",
        "For task-oriented examples, start with the README. This file is the "
        "formal public surface reference.",
        "",
        f"- SDK version: `{mailchannels.get_version()}`",
        f"- Top-level exports: `{len(mailchannels.__all__)}`",
        f"- Documented public module exports: `{len(objects)}`",
        "",
        "## Top-Level Exports",
        "",
        "| Name | Kind | Summary |",
        "| --- | --- | --- |",
    ]
    for name in sorted(mailchannels.__all__):
        value = getattr(mailchannels, name)
        lines.append(
            f"| `{name}` | `{_kind(value)}` | {_escape_table(_summary(value))} |"
        )
    lines.extend(["", "## Quick Examples", ""])
    lines.extend(_quick_examples())
    lines.extend(["", "## Public Modules", ""])
    for module in modules:
        lines.extend(_module_section(module, objects))
    lines.append("")
    return "\n".join(lines)


def _parser() -> argparse.ArgumentParser:
    """Build the command-line parser."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT_PATH,
        help="Markdown reference path to write.",
    )
    return parser


def _public_objects(modules: Iterable[ModuleType]) -> list[PublicObject]:
    """Return public exports from modules with `__all__` declarations."""
    objects: list[PublicObject] = []
    seen: set[tuple[str, str]] = set()
    for module in modules:
        names = getattr(module, "__all__", ())
        for name in sorted(names):
            value = getattr(module, name)
            key = (module.__name__, name)
            if key in seen:
                continue
            seen.add(key)
            objects.append(PublicObject(module, name, value))
    return objects


def _module_section(module: ModuleType, objects: list[PublicObject]) -> list[str]:
    """Render one public module section."""
    module_objects = [item for item in objects if item.module is module]
    lines = [
        f"### `{module.__name__}`",
        "",
        _summary(module),
        "",
    ]
    if not module_objects:
        lines.append("No public exports.")
        lines.append("")
        return lines
    for item in module_objects:
        lines.extend(_object_section(item))
    return lines


def _object_section(item: PublicObject) -> list[str]:
    """Render one public object section."""
    value = item.value
    heading = f"#### `{item.qualified_name}`"
    lines = [
        heading,
        "",
        f"- Kind: `{_kind(value)}`",
        f"- Summary: {_summary(value)}",
    ]
    signature = _signature(value)
    if signature:
        lines.append(f"- Signature: `{item.qualified_name}{signature}`")
    if inspect.isclass(value):
        lines.extend(_class_details(item.qualified_name, value))
    elif inspect.isfunction(value):
        example = METHOD_EXAMPLES.get(item.qualified_name)
        if example:
            lines.extend(["", "Example:", "", f"```python\n{example}\n```"])
    lines.append("")
    return lines


def _class_details(qualified_name: str, value: type[Any]) -> list[str]:
    """Render class-specific fields and methods."""
    lines: list[str] = []
    if issubclass(value, BaseModel):
        lines.extend(_pydantic_model_fields(value))
    elif _is_typed_dict(value):
        lines.extend(_typed_dict_fields(value))
    methods = _public_methods(value)
    if methods:
        lines.extend(
            [
                "",
                "Methods:",
                "",
                "| Method | Signature | Summary |",
                "| --- | --- | --- |",
            ]
        )
        for method in methods:
            lines.append(
                "| "
                f"`{method.name}` | "
                f"`{method.signature}` | "
                f"{_escape_table(method.doc)} |"
            )
        for method in methods:
            example = METHOD_EXAMPLES.get(f"{qualified_name}.{method.name}")
            if example:
                lines.extend(
                    [
                        "",
                        f"Example for `{method.name}`:",
                        "",
                        f"```python\n{example}\n```",
                    ]
                )
    return lines


def _pydantic_model_fields(value: type[BaseModel]) -> list[str]:
    """Render Pydantic model fields."""
    lines = [
        "",
        "Fields:",
        "",
        "| Field | Type | Required | Default |",
        "| --- | --- | --- | --- |",
    ]
    for name, field in value.model_fields.items():
        annotation = _format_annotation(field.annotation)
        required = "yes" if field.is_required() else "no"
        default = "" if field.is_required() else _format_default(field.default)
        lines.append(
            "| "
            f"`{name}` | `{_escape_table(annotation)}` | {required} | "
            f"`{_escape_table(default)}` |"
        )
    return lines


def _typed_dict_fields(value: type[Any]) -> list[str]:
    """Render TypedDict fields."""
    hints = getattr(value, "__annotations__", {})
    required = set(getattr(value, "__required_keys__", set()))
    lines = ["", "Fields:", "", "| Field | Type | Required |", "| --- | --- | --- |"]
    for name, annotation in sorted(hints.items()):
        is_required = "yes" if name in required else "no"
        lines.append(
            f"| `{name}` | `{_escape_table(_format_annotation(annotation))}` | "
            f"{is_required} |"
        )
    return lines


def _public_methods(value: type[Any]) -> list[PublicMethod]:
    """Return public methods defined directly on a class."""
    methods: list[PublicMethod] = []
    for name, raw in sorted(value.__dict__.items()):
        if name.startswith("_"):
            continue
        kind = "method"
        function: Any
        if isinstance(raw, classmethod):
            kind = "classmethod"
            function = raw.__func__
        elif isinstance(raw, staticmethod):
            kind = "staticmethod"
            function = raw.__func__
        elif inspect.isfunction(raw):
            function = raw
        else:
            continue
        signature = _method_signature(function)
        methods.append(
            PublicMethod(
                name=name,
                signature=f"{name}{signature}",
                doc=_summary(function),
                kind=kind,
            )
        )
    return methods


def _method_signature(function: Any) -> str:
    """Return a function signature without `self` or `cls`."""
    signature = inspect.signature(function)
    parameters = [
        parameter
        for parameter in signature.parameters.values()
        if parameter.name not in {"self", "cls"}
    ]
    clean_signature = signature.replace(parameters=parameters)
    return _stringify_signature(clean_signature)


def _signature(value: Any) -> str:
    """Return a public callable signature when available."""
    if inspect.isclass(value) and issubclass(value, BaseModel):
        parts = [
            f"{field.alias or name}: {_format_annotation(field.annotation)}"
            for name, field in value.model_fields.items()
        ]
        return f"({', '.join(parts)})"
    if inspect.isclass(value):
        init = value.__dict__.get("__init__")
        if init is None:
            return ""
        return _method_signature(init)
    if inspect.isfunction(value):
        return _stringify_signature(inspect.signature(value))
    return ""


def _stringify_signature(signature: inspect.Signature) -> str:
    """Return a compact, Markdown-safe signature string."""
    text = str(signature)
    text = re.sub(r": '([^']+)'", r": \1", text)
    return re.sub(r" -> '([^']+)'", r" -> \1", text)


def _kind(value: Any) -> str:
    """Return a concise public object kind."""
    if _is_protocol(value):
        return "protocol"
    if inspect.isclass(value):
        if issubclass(value, BaseModel):
            return "Pydantic model"
        if _is_typed_dict(value):
            return "TypedDict"
        if issubclass(value, Exception):
            return "exception"
        return "class"
    if inspect.isfunction(value):
        return "function"
    if isinstance(value, str):
        return "constant"
    return "value"


def _summary(value: Any) -> str:
    """Return the first sentence of an object's docstring."""
    if not (
        inspect.ismodule(value)
        or inspect.isclass(value)
        or inspect.isroutine(value)
    ):
        return ""
    doc = inspect.getdoc(value) or ""
    if not doc:
        return ""
    first_line = doc.strip().splitlines()[0]
    return first_line.rstrip(".") + "."


def _quick_examples() -> list[str]:
    """Render short examples for common SDK entry points."""
    examples = [
        (
            "Send a dry-run email",
            "mailchannels.Emails.send(\n"
            "    {\n"
            '        "from": {"email": "sender@example.com"},\n'
            '        "to": "recipient@example.net",\n'
            '        "subject": "Hello",\n'
            '        "text": "Hello from MailChannels.",\n'
            "    },\n"
            "    dry_run=True,\n"
            ")",
        ),
        ("Retrieve usage", "mailchannels.Usage.retrieve()"),
        ("List volume metrics", 'mailchannels.Metrics.volume(interval="day")'),
        ("List webhooks", "mailchannels.Webhooks.list()"),
    ]
    lines: list[str] = []
    for title, code in examples:
        lines.extend([f"### {title}", "", f"```python\n{code}\n```", ""])
    return lines


def _format_annotation(value: Any) -> str:
    """Return a readable annotation string."""
    if value is None:
        return "None"
    forward_arg = getattr(value, "__forward_arg__", None)
    if isinstance(forward_arg, str):
        return forward_arg.strip("'\"")
    text = getattr(value, "__name__", None)
    if isinstance(text, str):
        return text
    return str(value).replace("typing.", "").replace("types.", "")


def _format_default(value: Any) -> str:
    """Return a readable default value."""
    if str(value).startswith("PydanticUndefined"):
        return ""
    if value is None:
        return "None"
    return repr(value)


def _escape_table(value: str) -> str:
    """Escape text for Markdown table cells."""
    return value.replace("|", "\\|").replace("\n", " ")


def _is_typed_dict(value: Any) -> bool:
    """Return whether a class is a TypedDict definition."""
    return bool(
        getattr(value, "__total__", None) is not None
        and hasattr(value, "__annotations__")
    )


def _is_protocol(value: Any) -> bool:
    """Return whether a value is a typing protocol class."""
    return bool(getattr(value, "_is_protocol", False))


if __name__ == "__main__":
    raise SystemExit(main())
