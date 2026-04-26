"""Tests for documented examples."""

from __future__ import annotations

import base64
import hashlib
import importlib.util
from pathlib import Path
from types import ModuleType, SimpleNamespace
from typing import Any

from conftest import FakeHTTPXClient, FakeRequestsClient

import mailchannels
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
cloudflare_dkim = _load_example("cloudflare_dkim")
custom_headers = _load_example("custom_headers")
custom_http_client = _load_example("custom_http_client")
dkim = _load_example("dkim")
domain_checks = _load_example("domain_checks")
error_handling = _load_example("error_handling")
metrics = _load_example("metrics")
sub_accounts = _load_example("sub_accounts")
suppressions = _load_example("suppressions")
templates = _load_example("templates")
unsubscribe = _load_example("unsubscribe")
usage = _load_example("usage")
webhooks = _load_example("webhooks")


class FakeCloudflareRecords:
    """Fake Cloudflare DNS records resource for examples."""

    def __init__(self, existing_record: Any | None = None) -> None:
        """Create a fake records resource."""
        self.existing_record = existing_record
        self.created: list[dict[str, Any]] = []
        self.updated: list[dict[str, Any]] = []

    def list(self, **kwargs: Any) -> list[Any]:
        """Return existing DNS records."""
        self.last_list = kwargs
        return [] if self.existing_record is None else [self.existing_record]

    def create(self, **kwargs: Any) -> Any:
        """Record a DNS record creation."""
        self.created.append(kwargs)
        return SimpleNamespace(name=kwargs["name"])

    def update(self, record_id: str, **kwargs: Any) -> Any:
        """Record a DNS record update."""
        self.updated.append({"record_id": record_id, **kwargs})
        return SimpleNamespace(name=kwargs["name"])


class FakeCloudflare:
    """Fake Cloudflare client for DKIM publication examples."""

    def __init__(self, existing_record: Any | None = None) -> None:
        """Create a fake Cloudflare client."""
        self.zones = SimpleNamespace(
            list=lambda **_: [SimpleNamespace(id="zone_123")]
        )
        self.records = FakeCloudflareRecords(existing_record)
        self.dns = SimpleNamespace(records=self.records)


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


def test_template_example_builds_dry_run_payload() -> None:
    """It exercises the template example."""
    transport = FakeRequestsClient(SDKResponse(202, {"id": "previewed"}, "{}"))
    client = Client(api_key="test-key", http_client=transport)

    result = templates.preview_template(client)

    assert result.id == "previewed"
    assert transport.calls[0]["url"] == "https://api.mailchannels.net/tx/v1/send"
    assert transport.calls[0]["params"] == {"dry-run": "true"}
    assert transport.calls[0]["json"]["content"][0]["template_type"] == "mustache"
    assert transport.calls[0]["json"]["personalizations"][0][
        "dynamic_template_data"
    ] == {"name": "Jane Doe"}


def test_unsubscribe_example_builds_placeholder_and_list_header_payloads() -> None:
    """It exercises the unsubscribe example."""
    transport = FakeRequestsClient(SDKResponse(202, {"id": "queued"}, "{}"))
    client = Client(api_key="test-key", http_client=transport)

    one_click = unsubscribe.build_one_click_unsubscribe_message()
    list_unsubscribe = unsubscribe.build_list_unsubscribe_message()
    result = unsubscribe.queue_unsubscribe_message(client)

    assert result.id == "queued"
    assert mailchannels.UNSUBSCRIBE_URL_PLACEHOLDER in one_click["content"][0]["value"]
    assert one_click["content"][0]["template_type"] == "mustache"
    assert list_unsubscribe["transactional"] is False
    assert list_unsubscribe["personalizations"][0]["dkim_selector"] == "mailchannels"


def test_custom_headers_example_preserves_global_and_personalized_headers() -> None:
    """It exercises the custom-header example."""
    transport = FakeRequestsClient(SDKResponse(202, {"id": "sent"}, "{}"))
    client = Client(api_key="test-key", http_client=transport)

    global_message = custom_headers.build_global_headers_message()
    personalized_message = custom_headers.build_personalized_headers_message()
    custom_headers.send_with_custom_headers(client)

    assert global_message["headers"]["X-Campaign-ID"] == "newsletter-123"
    assert personalized_message["personalizations"][0]["headers"] == {
        "List-Unsubscribe": "<mailto:unsubscribe@bananas.example>",
        "X-Custom-Header": "BananaFan123",
    }
    assert transport.calls[0]["params"] == {"dry-run": "true"}
    assert transport.calls[0]["json"]["headers"]["X-Campaign-ID"] == "newsletter-123"


def test_dkim_example_uses_hosted_dkim_endpoints() -> None:
    """It exercises the DKIM example."""
    transport = FakeRequestsClient(
        SDKResponse(
            200,
            {
                "domain": "example.com",
                "selector": "mcdkim",
                "public_key": "public",
                "status": "active",
                "algorithm": "rsa",
                "dkim_dns_records": [],
            },
            "{}",
        )
    )
    client = Client(api_key="test-key", http_client=transport)

    dkim.create_hosted_dkim_key(client, "example.com", "mcdkim")
    dkim.list_hosted_dkim_keys(client, "example.com")
    dkim.rotate_hosted_dkim_key(client, "example.com", "mcdkim", "mcdkim2")

    assert [call["method"] for call in transport.calls] == ["POST", "GET", "POST"]
    assert transport.calls[0]["json"] == {
        "selector": "mcdkim",
        "algorithm": "rsa",
        "key_length": 2048,
    }
    assert transport.calls[1]["params"] == {"include_dns_record": True}
    assert transport.calls[2]["url"].endswith(
        "/domains/example.com/dkim-keys/mcdkim/rotate"
    )
    assert transport.calls[2]["json"] == {"new_key": {"selector": "mcdkim2"}}


def test_cloudflare_dkim_example_creates_or_updates_txt_record() -> None:
    """It exercises the Cloudflare DKIM publication example without Cloudflare."""
    dns_record = {
        "name": "mcdkim._domainkey.example.com",
        "type": "TXT",
        "value": "v=DKIM1; p=public",
    }
    transport = FakeRequestsClient(
        SDKResponse(
            200,
            {
                "domain": "example.com",
                "selector": "mcdkim",
                "public_key": "public",
                "status": "active",
                "algorithm": "rsa",
                "dkim_dns_records": [dns_record],
            },
            "{}",
        )
    )
    client = Client(api_key="test-key", http_client=transport)
    cloudflare = FakeCloudflare()

    created_record = cloudflare_dkim.create_and_publish_dkim_record(
        client,
        cloudflare,
        "example.com",
        "mcdkim",
    )

    assert created_record.name == "mcdkim._domainkey.example.com"
    assert cloudflare.records.created[0] == {
        "zone_id": "zone_123",
        "type": "TXT",
        "name": "mcdkim._domainkey.example.com",
        "content": "v=DKIM1; p=public",
        "ttl": 1,
    }
    assert transport.calls[0]["url"].endswith("/domains/example.com/dkim-keys")

    existing = SimpleNamespace(id="record_123")
    update_cloudflare = FakeCloudflare(existing)
    updated_record = cloudflare_dkim.publish_dkim_record(
        update_cloudflare,
        "example.com",
        dns_record,
    )

    assert updated_record.name == "mcdkim._domainkey.example.com"
    assert update_cloudflare.records.updated[0]["record_id"] == "record_123"


def test_sub_accounts_example_uses_account_lifecycle_endpoints() -> None:
    """It exercises the sub-account example."""
    transport = FakeRequestsClient(SDKResponse(200, {"handle": "clienta"}, "{}"))
    client = Client(api_key="test-key", http_client=transport)

    sub_accounts.create_sub_account(client, "clienta", "Client A")
    sub_accounts.create_sub_account_api_key(client, "clienta")
    sub_accounts.set_sub_account_limit(client, "clienta", 100_000)
    sub_accounts.retrieve_sub_account_usage(client, "clienta")

    assert [call["method"] for call in transport.calls] == [
        "POST",
        "POST",
        "PUT",
        "GET",
    ]
    assert transport.calls[0]["json"] == {
        "company_name": "Client A",
        "handle": "clienta",
    }
    assert transport.calls[2]["url"].endswith("/sub-account/clienta/limit")
    assert transport.calls[2]["json"] == {"sends": 100_000}


def test_metrics_example_retrieves_time_series_and_sender_metrics() -> None:
    """It exercises the metrics example."""
    transport = FakeRequestsClient(SDKResponse(200, {"buckets": {}}, "{}"))
    client = Client(api_key="test-key", http_client=transport)

    metrics.retrieve_engagement_metrics(
        client,
        start_time="2026-04-01",
        end_time="2026-04-24T00:00:00Z",
        campaign_id="newsletter",
    )
    metrics.retrieve_sender_metrics(client, "sub-accounts")

    assert transport.calls[0]["url"].endswith("/metrics/engagement")
    assert transport.calls[0]["params"] == {
        "start_time": "2026-04-01",
        "end_time": "2026-04-24T00:00:00Z",
        "campaign_id": "newsletter",
        "interval": "day",
    }
    assert transport.calls[1]["url"].endswith("/metrics/senders/sub-accounts")
    assert transport.calls[1]["params"] == {
        "limit": 50,
        "offset": 0,
        "sort_order": "desc",
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
