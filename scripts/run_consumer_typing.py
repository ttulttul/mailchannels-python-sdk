"""Run mypy against a small external-consumer typing fixture."""

from __future__ import annotations

import logging
import subprocess
from pathlib import Path

logger = logging.getLogger(__name__)

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "typing_tests" / "consumer_project.py"


def main() -> int:
    """Run the consumer typing fixture through mypy."""
    command = [
        "mypy",
        "--strict",
        "--show-error-codes",
        "--python-version",
        "3.9",
        str(FIXTURE),
    ]
    logger.info("Running consumer typing check: %s", " ".join(command))
    completed = subprocess.run(command, cwd=ROOT, check=False)
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
