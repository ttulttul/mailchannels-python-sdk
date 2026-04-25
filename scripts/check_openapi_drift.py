"""Check SDK route declarations against the MailChannels OpenAPI spec."""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path
from typing import Any
from urllib.request import urlopen

import yaml

from mailchannels.routes import SDK_ROUTES, SDKRoute

DEFAULT_SPEC_URL = "https://docs.mailchannels.net/email-api.yaml"
HTTP_METHODS = {"delete", "get", "patch", "post", "put"}
logger = logging.getLogger(__name__)


def main() -> int:
    """Run the OpenAPI drift check."""
    args = _parser().parse_args()
    spec = _load_spec(url=args.spec_url, path=args.spec_path)
    spec_routes = _spec_route_keys(spec)
    missing = _missing_routes(spec_routes)
    if missing:
        _print_missing_routes(missing)
        return 1
    print(f"OpenAPI drift check passed for {len(SDK_ROUTES)} SDK routes.")
    return 0


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
    return parser


def _load_spec(*, url: str, path: Path | None) -> dict[str, Any]:
    """Load an OpenAPI document from a local path or URL."""
    if path is not None:
        logger.info("Loading OpenAPI spec from %s.", path)
        with path.open("r", encoding="utf-8") as spec_file:
            data = yaml.safe_load(spec_file)
    else:
        logger.info("Fetching OpenAPI spec from %s.", url)
        with urlopen(url, timeout=30) as response:
            data = yaml.safe_load(response.read())
    if not isinstance(data, dict):
        raise TypeError("OpenAPI spec must parse to a mapping.")
    return data


def _spec_route_keys(spec: dict[str, Any]) -> set[tuple[str, str]]:
    """Return method/path pairs declared by an OpenAPI document."""
    paths = spec.get("paths")
    if not isinstance(paths, dict):
        raise TypeError("OpenAPI spec is missing a `paths` mapping.")
    routes: set[tuple[str, str]] = set()
    for path, operations in paths.items():
        if not isinstance(path, str) or not isinstance(operations, dict):
            continue
        for method in operations:
            if isinstance(method, str) and method.lower() in HTTP_METHODS:
                routes.add((method.upper(), path))
    return routes


def _missing_routes(spec_routes: set[tuple[str, str]]) -> list[SDKRoute]:
    """Return SDK routes that are not present in the OpenAPI spec."""
    missing = [
        route
        for route in SDK_ROUTES
        if (route.method, route.path) not in spec_routes
    ]
    logger.debug("Found %s SDK routes missing from the OpenAPI spec.", len(missing))
    return missing


def _print_missing_routes(missing: list[SDKRoute]) -> None:
    """Print a readable missing-route report."""
    logger.error("OpenAPI drift detected for %s SDK routes.", len(missing))
    print("OpenAPI drift detected. SDK routes missing from the spec:", file=sys.stderr)
    for route in missing:
        print(
            f"- {route.method} {route.path} "
            f"({route.resource}.{route.operation})",
            file=sys.stderr,
        )


if __name__ == "__main__":
    raise SystemExit(main())
