"""Executable checks for Python snippets embedded in the README."""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pytest
from conftest import FakeHTTPXClient, FakeRequestsClient

import mailchannels
import mailchannels.client as client_module
from mailchannels.response import SDKResponse

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"

FENCE_PATTERN = re.compile(r"^```(?P<language>\w+)?\n(?P<code>.*?)^```", re.M | re.S)
EXECUTION_SKIP_MARKERS = {
    "from cloudflare import Cloudflare": (
        "Cloudflare DNS publishing requires the external Cloudflare SDK and "
        "real DNS side effects."
    ),
}


@dataclass(frozen=True)
class CodeBlock:
    """A fenced README code block."""

    language: str
    code: str
    start_line: int

    @property
    def id(self) -> str:
        """Return a stable pytest identifier for this block."""
        return f"README.md:{self.start_line}"


def _readme_code_blocks(language: str) -> list[CodeBlock]:
    """Extract fenced code blocks for a language from the README."""
    text = README.read_text(encoding="utf-8")
    blocks: list[CodeBlock] = []
    for match in FENCE_PATTERN.finditer(text):
        block_language = match.group("language") or ""
        if block_language != language:
            continue
        start_line = text.count("\n", 0, match.start()) + 1
        blocks.append(
            CodeBlock(
                language=block_language,
                code=match.group("code"),
                start_line=start_line,
            )
        )
    return blocks


PYTHON_BLOCKS = _readme_code_blocks("python")
PYTHON_BLOCK_IDS = [block.id for block in PYTHON_BLOCKS]


def _example_response() -> SDKResponse:
    """Build a broad fake response that satisfies README example reads."""
    data: dict[str, Any] = {
        "id": "example-id",
        "total_usage": 10,
        "period_start_date": "2026-04-01",
        "period_end_date": "2026-04-30",
        "handle": "clienta",
        "company_name": "Client A",
        "sends": 100_000,
        "check_results": {"spf": {"verdict": "passed"}},
        "references": [],
        "dkim_dns_records": [
            {
                "name": "mcdkim._domainkey.example.com",
                "type": "TXT",
                "value": "v=DKIM1; p=example",
            }
        ],
        "keys": [],
        "suppression_list": [],
        "webhook_batches": [],
        "all_passed": True,
        "results": [],
        "key": "public-key",
        "open": 0,
        "open_tracking_delivered": 0,
        "click": 0,
        "click_tracking_delivered": 0,
        "processed": 0,
        "delivered": 0,
        "bounced": 0,
        "dropped": 0,
        "unsubscribed": 0,
        "unsubscribe_delivered": 0,
        "buckets": {},
        "limit": 50,
        "offset": 0,
        "total": 0,
        "senders": [],
    }
    return SDKResponse(200, data, "{}", headers={"X-Request-ID": "readme-test"})


def _execution_skip_reason(code: str) -> str | None:
    """Return why a README snippet should not be executed, if applicable."""
    for marker, reason in EXECUTION_SKIP_MARKERS.items():
        if marker in code:
            return reason
    return None


def _execution_namespace() -> dict[str, Any]:
    """Build globals used to run README snippets without real network calls."""
    message = {
        "from": {"email": "sender@example.com"},
        "to": [{"email": "recipient@example.net"}],
        "subject": "README smoke test",
        "text": "Hello from the README test.",
    }
    return {
        "__name__": "__readme_example__",
        "logger": logging.getLogger("tests.readme_examples"),
        "mailchannels": mailchannels,
        "message": message,
    }


@pytest.fixture()
def readme_snippet_environment(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> dict[str, Any]:
    """Configure sample files and fake SDK transports for README snippets."""
    monkeypatch.chdir(tmp_path)
    (tmp_path / "invoice.pdf").write_bytes(b"invoice")
    (tmp_path / "logo.png").write_bytes(b"logo")

    response = _example_response()
    sync_transport = FakeRequestsClient(response)
    async_transport = FakeHTTPXClient(response)
    monkeypatch.setattr(client_module, "RequestsClient", lambda: sync_transport)
    monkeypatch.setattr(client_module, "HTTPXClient", lambda: async_transport)
    monkeypatch.setattr(mailchannels, "api_key", "README-TEST-KEY")
    monkeypatch.setattr(mailchannels, "base_url", "https://api.mailchannels.net/tx/v1")
    monkeypatch.setattr(mailchannels, "default_http_client", sync_transport)
    monkeypatch.setattr(mailchannels, "default_async_http_client", async_transport)
    monkeypatch.setattr(mailchannels, "strict_responses", False)
    return _execution_namespace()


@pytest.mark.parametrize("block", PYTHON_BLOCKS, ids=PYTHON_BLOCK_IDS)
def test_readme_python_snippets_compile(block: CodeBlock) -> None:
    """Every README Python snippet remains syntactically valid."""
    compile(block.code, block.id, "exec")


@pytest.mark.parametrize("block", PYTHON_BLOCKS, ids=PYTHON_BLOCK_IDS)
def test_readme_python_snippets_execute_when_safe(
    block: CodeBlock,
    readme_snippet_environment: dict[str, Any],
) -> None:
    """Runnable README Python snippets work with fake SDK transports."""
    skip_reason = _execution_skip_reason(block.code)
    if skip_reason is not None:
        pytest.skip(skip_reason)

    exec(compile(block.code, block.id, "exec"), readme_snippet_environment)
