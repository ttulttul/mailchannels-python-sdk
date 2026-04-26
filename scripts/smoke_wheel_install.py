"""Smoke-test the built wheel in clean virtual environments."""

from __future__ import annotations

import argparse
import logging
import os
import subprocess
import sys
import tempfile
import textwrap
import zipfile
from pathlib import Path

logger = logging.getLogger(__name__)

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    """Run wheel installation smoke tests."""
    args = _parser().parse_args()
    wheel = _wheel_path(args.wheel)
    _assert_py_typed(wheel)
    with tempfile.TemporaryDirectory(prefix="mailchannels-wheel-smoke-") as tmp:
        tmp_path = Path(tmp)
        _run_sync_smoke(wheel, tmp_path / "sync")
        _run_async_extra_smoke(wheel, tmp_path / "async")
    return 0


def _parser() -> argparse.ArgumentParser:
    """Build the command-line parser."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--wheel",
        type=Path,
        help="Wheel path to test. Defaults to the newest dist/*.whl.",
    )
    return parser


def _wheel_path(path: Path | None) -> Path:
    """Resolve the wheel path to smoke-test."""
    if path is not None:
        return path.resolve()
    wheels = sorted(
        (ROOT / "dist").glob("*.whl"),
        key=lambda item: item.stat().st_mtime,
    )
    if not wheels:
        raise FileNotFoundError("No wheel found in dist/. Run `uv build` first.")
    return wheels[-1].resolve()


def _assert_py_typed(wheel: Path) -> None:
    """Assert the wheel includes the PEP 561 marker."""
    logger.info("Checking py.typed marker in %s", wheel)
    with zipfile.ZipFile(wheel) as archive:
        names = set(archive.namelist())
    if "mailchannels/py.typed" not in names:
        raise AssertionError("Wheel is missing mailchannels/py.typed.")


def _run_sync_smoke(wheel: Path, environment: Path) -> None:
    """Install the base wheel and run sync-only smoke checks."""
    _venv(environment)
    _pip(environment, "install", str(wheel))
    _python(
        environment,
        textwrap.dedent(
            """
            import asyncio
            import builtins

            import mailchannels
            from mailchannels import Client

            client = Client(api_key="test-key")
            assert mailchannels.Client is Client
            assert mailchannels.__version__

            original_import = builtins.__import__

            def fake_import(name, *args, **kwargs):
                if name == "httpx":
                    raise ImportError("No module named httpx")
                return original_import(name, *args, **kwargs)

            builtins.__import__ = fake_import
            try:
                try:
                    asyncio.run(
                        client.async_http_client.request(
                            "GET",
                            "https://example.test",
                            headers={},
                        )
                    )
                except mailchannels.AsyncClientNotConfigured as error:
                    assert 'mailchannels[async]' in str(error)
                else:
                    raise AssertionError("Expected AsyncClientNotConfigured")
            finally:
                builtins.__import__ = original_import
            """
        ),
    )


def _run_async_extra_smoke(wheel: Path, environment: Path) -> None:
    """Install the wheel with the async extra and run async import smoke checks."""
    _venv(environment)
    _pip(environment, "install", f"{wheel}[async]")
    _python(
        environment,
        textwrap.dedent(
            """
            import httpx
            import mailchannels

            client = mailchannels.Client(api_key="test-key")
            assert isinstance(client.async_http_client, mailchannels.HTTPXClient)
            assert httpx.AsyncClient is not None
            """
        ),
    )


def _venv(path: Path) -> None:
    """Create a virtual environment."""
    logger.info("Creating virtual environment at %s", path)
    subprocess.run([sys.executable, "-m", "venv", str(path)], check=True)


def _pip(environment: Path, *args: str) -> None:
    """Run pip in a virtual environment."""
    command = [str(_bin(environment, "pip")), *args]
    logger.info("Running %s", " ".join(command))
    subprocess.run(command, check=True)


def _python(environment: Path, code: str) -> None:
    """Run Python code in a virtual environment."""
    command = [str(_bin(environment, "python")), "-c", code]
    logger.info("Running installed package smoke test in %s", environment)
    subprocess.run(command, check=True, cwd=ROOT)


def _bin(environment: Path, name: str) -> Path:
    """Return a virtual environment executable path."""
    directory = "Scripts" if os.name == "nt" else "bin"
    return environment / directory / name


if __name__ == "__main__":
    raise SystemExit(main())
