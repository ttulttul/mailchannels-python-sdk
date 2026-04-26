"""Generate the MailChannels SDK API coverage report."""

from __future__ import annotations

import argparse
import hashlib
import logging
from collections.abc import Hashable, Mapping
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, cast
from urllib.request import urlopen

import yaml
from openapi_spec_validator import validate

from mailchannels import get_version
from mailchannels.routes import SDK_ROUTES, SDKRoute

DEFAULT_SPEC_URL = "https://docs.mailchannels.net/email-api.yaml"
DEFAULT_OUTPUT_PATH = Path("docs/API_COVERAGE.md")
HTTP_METHODS = {"delete", "get", "patch", "post", "put"}
ROUTINE_ONLINE_ROUTES = frozenset(
    {
        ("POST", "/check-domain"),
        ("POST", "/send"),
        ("GET", "/domains/{domain}/dkim-keys"),
        ("GET", "/metrics/volume"),
        ("GET", "/sub-account"),
        ("GET", "/suppression-list"),
        ("GET", "/usage"),
        ("GET", "/webhook"),
    }
)
DESTRUCTIVE_ONLINE_ROUTES = frozenset(
    {
        ("POST", "/sub-account"),
        ("DELETE", "/sub-account/{handle}"),
        ("POST", "/sub-account/{handle}/activate"),
        ("POST", "/sub-account/{handle}/api-key"),
        ("GET", "/sub-account/{handle}/api-key"),
        ("DELETE", "/sub-account/{handle}/api-key/{id}"),
        ("PUT", "/sub-account/{handle}/limit"),
        ("GET", "/sub-account/{handle}/limit"),
        ("DELETE", "/sub-account/{handle}/limit"),
        ("POST", "/sub-account/{handle}/smtp-password"),
        ("GET", "/sub-account/{handle}/smtp-password"),
        ("DELETE", "/sub-account/{handle}/smtp-password/{id}"),
        ("POST", "/sub-account/{handle}/suspend"),
        ("POST", "/suppression-list"),
        ("GET", "/suppression-list"),
        ("DELETE", "/suppression-list/recipients/{recipient}"),
        ("POST", "/webhook"),
        ("GET", "/webhook"),
        ("DELETE", "/webhook"),
        ("POST", "/webhook/validate"),
    }
)
logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class SpecOperation:
    """One operation declared by the OpenAPI document."""

    method: str
    path: str
    summary: str

    @property
    def key(self) -> tuple[str, str]:
        """Return the method/path key for this operation."""
        return (self.method, self.path)


def main() -> int:
    """Generate the API coverage Markdown report."""
    args = _parser().parse_args()
    source, spec_bytes = _load_spec_bytes(url=args.spec_url, path=args.spec_path)
    spec = _parse_spec(spec_bytes)
    _validate_openapi_spec(spec)
    report = render_report(
        spec=spec,
        source=source,
        spec_hash=_sha256(spec_bytes),
        generated_at=_generated_at(),
    )
    args.output.write_text(report, encoding="utf-8")
    print(f"Wrote API coverage report to {args.output}")
    return 0


def render_report(
    *,
    spec: dict[str, Any],
    source: str,
    spec_hash: str,
    generated_at: str,
) -> str:
    """Render the API coverage report as Markdown."""
    operations = _spec_operations(spec)
    sdk_routes: dict[tuple[str, str], SDKRoute] = {
        (route.method, route.path): route for route in SDK_ROUTES
    }
    covered = [operation for operation in operations if operation.key in sdk_routes]
    pending = [operation for operation in operations if operation.key not in sdk_routes]
    stale = [
        route
        for route in SDK_ROUTES
        if (route.method, route.path) not in {operation.key for operation in operations}
    ]
    lines = [
        "# MailChannels API Coverage",
        "",
        "This report is generated from the MailChannels OpenAPI document and the "
        "SDK route registry.",
        "",
        f"- SDK version: `{get_version()}`",
        f"- OpenAPI source: `{source}`",
        f"- OpenAPI version: `{_spec_version(spec)}`",
        f"- OpenAPI SHA-256: `{spec_hash}`",
        f"- Generated at: `{generated_at}`",
        "",
        "## Summary",
        "",
        f"- OpenAPI operations: `{len(operations)}`",
        f"- SDK-supported operations: `{len(covered)}`",
        f"- Pending OpenAPI operations: `{len(pending)}`",
        f"- SDK routes absent from OpenAPI: `{len(stale)}`",
        "",
        "## Coverage Matrix",
        "",
        "| Method | Path | Summary | SDK surface | Sync | Async | "
        "Contract test | Online test | Status |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for operation in operations:
        route = sdk_routes.get(operation.key)
        lines.append(_coverage_row(operation, route))
    if stale:
        lines.extend(
            [
                "",
                "## SDK Routes Absent From OpenAPI",
                "",
                "| Method | Path | SDK surface |",
                "| --- | --- | --- |",
            ]
        )
        for route in sorted(stale, key=lambda item: (item.path, item.method)):
            lines.append(
                "| "
                f"`{route.method}` | `{route.path}` | "
                f"`{_sdk_surface(route)}` |"
            )
    lines.extend(
        [
            "",
            "## Notes",
            "",
            "- `Contract test` is `yes` because "
            "`tests/test_openapi_request_contract.py` asserts that every SDK "
            "route has an executable request contract.",
            "- `Online test` is `routine` for non-mutating manual live tests, "
            "`destructive` for manually gated lifecycle tests, and `none` when "
            "only local contract coverage exists.",
            "- This report intentionally tracks endpoint coverage first. "
            "Request-field and response-field coverage can be added after "
            "strict response model coverage is complete.",
            "",
        ]
    )
    return "\n".join(lines)


def _parser() -> argparse.ArgumentParser:
    """Build the command-line parser."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--spec-url",
        default=DEFAULT_SPEC_URL,
        help="OpenAPI YAML URL to fetch when --spec-path is not provided.",
    )
    parser.add_argument(
        "--spec-path",
        type=Path,
        help="Local OpenAPI YAML path, used instead of fetching --spec-url.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT_PATH,
        help="Markdown report path to write.",
    )
    return parser


def _load_spec_bytes(*, url: str, path: Path | None) -> tuple[str, bytes]:
    """Load raw OpenAPI bytes from a local path or URL."""
    if path is not None:
        logger.info("Loading OpenAPI spec from %s.", path)
        return str(path), path.read_bytes()
    logger.info("Fetching OpenAPI spec from %s.", url)
    with urlopen(url, timeout=30) as response:
        return url, response.read()


def _parse_spec(spec_bytes: bytes) -> dict[str, Any]:
    """Parse OpenAPI YAML bytes into a mapping."""
    data = yaml.safe_load(spec_bytes)
    if not isinstance(data, dict):
        raise TypeError("OpenAPI spec must parse to a mapping.")
    return data


def _validate_openapi_spec(spec: dict[str, Any]) -> None:
    """Validate that the loaded document is structurally valid OpenAPI."""
    validate(cast(Mapping[Hashable, Any], spec))


def _spec_operations(spec: dict[str, Any]) -> list[SpecOperation]:
    """Return operations declared by an OpenAPI document."""
    paths = spec.get("paths")
    if not isinstance(paths, dict):
        raise TypeError("OpenAPI spec is missing a `paths` mapping.")
    operations: list[SpecOperation] = []
    for path, path_item in paths.items():
        if not isinstance(path, str) or not isinstance(path_item, dict):
            continue
        for method, operation in path_item.items():
            if not isinstance(method, str) or method.lower() not in HTTP_METHODS:
                continue
            summary = ""
            if isinstance(operation, dict):
                summary_value = operation.get("summary") or operation.get(
                    "operationId"
                )
                summary = str(summary_value) if summary_value is not None else ""
            operations.append(
                SpecOperation(
                    method=method.upper(),
                    path=path,
                    summary=summary,
                )
            )
    return sorted(operations, key=lambda item: (item.path, item.method))


def _coverage_row(operation: SpecOperation, route: SDKRoute | None) -> str:
    """Render one coverage matrix row."""
    if route is None:
        return (
            "| "
            f"`{operation.method}` | `{operation.path}` | "
            f"{_markdown_text(operation.summary)} | pending | no | no | no | "
            "none | pending |"
        )
    online = _online_coverage(operation.key)
    return (
        "| "
        f"`{operation.method}` | `{operation.path}` | "
        f"{_markdown_text(operation.summary)} | `{_sdk_surface(route)}` | "
        f"yes | yes | yes | {online} | supported |"
    )


def _sdk_surface(route: SDKRoute) -> str:
    """Return a public SDK surface label for a route."""
    return f"mailchannels.{route.resource}.{route.operation}()"


def _online_coverage(key: tuple[str, str]) -> str:
    """Return the live-test coverage category for an operation."""
    labels: list[str] = []
    if key in ROUTINE_ONLINE_ROUTES:
        labels.append("routine")
    if key in DESTRUCTIVE_ONLINE_ROUTES:
        labels.append("destructive")
    return ", ".join(labels) if labels else "none"


def _spec_version(spec: dict[str, Any]) -> str:
    """Return the OpenAPI document version."""
    info = spec.get("info")
    if isinstance(info, dict):
        version = info.get("version")
        if version is not None:
            return str(version)
    return "unknown"


def _sha256(data: bytes) -> str:
    """Return a SHA-256 hex digest for bytes."""
    return hashlib.sha256(data).hexdigest()


def _generated_at() -> str:
    """Return the current UTC timestamp for the generated report."""
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _markdown_text(value: str) -> str:
    """Escape table-sensitive characters in Markdown text."""
    return value.replace("|", "\\|") if value else ""


if __name__ == "__main__":
    raise SystemExit(main())
