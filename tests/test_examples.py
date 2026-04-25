"""Tests for documented examples."""

from __future__ import annotations

import base64
import hashlib
import importlib.util
from pathlib import Path
from types import ModuleType

from conftest import FakeHTTPXClient, FakeRequestsClient

from mailchannels.client import Client
from mailchannels.response import SDKResponse

ROOT = Path(__file__).resolve().parents[1]


def _load_example(name: str) -> ModuleType:
    """Load an example module from the repository examples directory."""
    path = ROOT / "examples" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(f"examples.{name}", path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load example module: {name}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


async_email = _load_example("async_email")
attachments = _load_example("attachments")
custom_http_client = _load_example("custom_http_client")
domain_checks = _load_example("domain_checks")
error_handling = _load_example("error_handling")
suppressions = _load_example("suppressions")
usage = _load_example("usage")
webhooks = _load_example("webhooks")


async def test_async_email_example_queues_message() -> None:
    """It exercises the async email example without real network I/O."""
    transport = FakeHTTPXClient(SDKResponse(202, {"id": "queued_async"}, "{}"))
    client = Client(api_key="test-key", async_http_client=transport)

    result = await async_email.queue_async_email(client)

    assert result.id == "queued_async"
    assert transport.calls[0]["url"] == "https://api.mailchannels.net/tx/v1/send-async"


def test_attachment_example_builds_and_queues_payload(tmp_path: Path) -> None:
    """It exercises attachment example helpers."""
    attachment_path = tmp_path / "report.txt"
    attachment_path.write_text("hello", encoding="utf-8")
    transport = FakeRequestsClient(SDKResponse(202, {"id": "queued"}, "{}"))
    client = Client(api_key="test-key", http_client=transport)

    message = attachments.build_attachment_message(attachment_path)
    inline = attachments.build_inline_image_message(attachment_path)
    result = attachments.queue_attachment(client, attachment_path)

    assert message["attachments"][0].content == "aGVsbG8="
    assert inline["attachments"][0].disposition == "inline"
    assert result.id == "queued"
    assert transport.calls[0]["json"]["attachments"][0]["filename"] == "report.txt"


def test_suppressions_example_uses_expected_endpoints() -> None:
    """It exercises suppression example helpers."""
    transport = FakeRequestsClient(SDKResponse(200, {"suppression_list": []}, "{}"))
    client = Client(api_key="test-key", http_client=transport)

    suppressions.create_suppression(client, "recipient@example.net")
    suppressions.list_api_suppressions(client)
    suppressions.delete_suppression(client, "recipient@example.net")

    assert [call["method"] for call in transport.calls] == ["POST", "GET", "DELETE"]
    assert transport.calls[1]["params"] == {"source": "api", "limit": 100, "offset": 0}


def test_webhook_example_configures_and_verifies_metadata(monkeypatch) -> None:
    """It exercises webhook example helpers."""
    transport = FakeRequestsClient(SDKResponse(200, {"ok": True}, "{}"))
    client = Client(api_key="test-key", http_client=transport)
    body = b'[{"event":"delivered"}]'
    digest = base64.b64encode(hashlib.sha256(body).digest()).decode("ascii")
    headers = {
        "Content-Digest": f"sha-256=:{digest}:",
        "Signature-Input": 'sig=("content-digest");created=1;keyid="mckey"',
    }
    monkeypatch.setattr(webhooks.mailchannels, "signature_is_fresh", lambda _: True)

    webhooks.configure_webhook(client, "https://example.com/events")
    webhooks.validate_webhooks(client)
    webhooks.inspect_failed_batches(client)
    key_id = webhooks.verify_webhook_metadata(headers, body)

    assert key_id == "mckey"
    assert transport.calls[2]["params"] == {
        "statuses": "4xx,5xx,no_response",
        "limit": 50,
    }


def test_usage_example_retrieves_parent_and_sub_account_usage() -> None:
    """It exercises usage example helpers."""
    transport = FakeRequestsClient(SDKResponse(200, {"total_usage": 10}, "{}"))
    client = Client(api_key="test-key", http_client=transport)

    parent = usage.retrieve_account_usage(client)
    child = usage.retrieve_sub_account_usage(client, "clienta")

    assert parent.total_usage == 10
    assert child.total_usage == 10
    assert [call["url"] for call in transport.calls] == [
        "https://api.mailchannels.net/tx/v1/usage",
        "https://api.mailchannels.net/tx/v1/sub-account/clienta/usage",
    ]


def test_domain_check_example_checks_configuration() -> None:
    """It exercises domain check example helpers."""
    transport = FakeRequestsClient(SDKResponse(200, {"references": []}, "{}"))
    client = Client(api_key="test-key", http_client=transport)

    domain_checks.check_domain_configuration(client, "example.com")
    domain_checks.check_domain_with_dkim_selector(client, "example.com", "mcdkim")

    assert [call["url"] for call in transport.calls] == [
        "https://api.mailchannels.net/tx/v1/check-domain",
        "https://api.mailchannels.net/tx/v1/check-domain",
    ]
    assert transport.calls[1]["json"] == {
        "domain": "example.com",
        "dkim_settings": [
            {"dkim_domain": "example.com", "dkim_selector": "mcdkim"}
        ],
    }


def test_custom_http_client_example_wraps_delegate_transport() -> None:
    """It exercises the custom HTTP client example."""
    delegate = FakeRequestsClient(SDKResponse(200, {"total_usage": 5}, "{}"))
    transport = custom_http_client.InstrumentedHTTPClient(delegate=delegate)
    client = Client(api_key="test-key", http_client=transport)

    result = client.usage.retrieve()

    assert result.total_usage == 5
    assert transport.calls == [
        {"method": "GET", "url": "https://api.mailchannels.net/tx/v1/usage"}
    ]


def test_error_handling_example_returns_none_on_sdk_error() -> None:
    """It exercises the structured error-handling example."""
    transport = FakeRequestsClient(
        SDKResponse(
            413,
            {"message": "Too large"},
            "Too large",
            headers={"X-Request-ID": "req_example"},
        )
    )
    client = Client(api_key="test-key", http_client=transport)

    result = error_handling.queue_with_error_handling(
        client,
        {
            "from": {"email": "sender@example.com"},
            "to": "recipient@example.net",
            "subject": "Example",
            "text": "Hello",
        },
    )

    assert result is None
