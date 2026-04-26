"""Tests for client configuration and response ergonomics."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

import pytest
from conftest import FakeRequestsClient

import mailchannels
from mailchannels.client import Client
from mailchannels.dkim.types import DkimKeyInfo, DkimKeyList, DkimRotateResponse
from mailchannels.domain_checks.types import CheckDomainResult
from mailchannels.emails.types import QueuedSendResponse, SendResponse
from mailchannels.metrics.types import (
    MetricsEngagement,
    MetricsPerformance,
    MetricsRecipientBehaviour,
    MetricsSenderResponse,
    MetricsVolume,
)
from mailchannels.response import SDKResponse
from mailchannels.sub_accounts.types import (
    ApiKey,
    SmtpPassword,
    SubAccount,
    SubAccountLimit,
)
from mailchannels.sub_accounts.types import UsageStats as SubAccountUsageStats
from mailchannels.suppressions.types import SuppressionListResponse
from mailchannels.usage import UsageStats
from mailchannels.webhooks.types import (
    WebhookBatchResult,
    WebhookPublicKey,
    WebhookValidationResults,
)


@dataclass(frozen=True)
class StrictResponseCase:
    """One strict response model test case."""

    name: str
    call: Callable[[Client], Any]
    model: type[Any]
    valid: dict[str, Any]
    missing_required: dict[str, Any] | None = None
    invalid_type: dict[str, Any] | None = None


def _dkim_key(selector: str = "mcdkim") -> dict[str, Any]:
    """Build a valid DKIM key response body."""
    return {
        "domain": "example.com",
        "selector": selector,
        "public_key": "public-key",
        "status": "active",
        "algorithm": "rsa",
        "dkim_dns_records": [
            {
                "name": f"{selector}._domainkey.example.com",
                "type": "TXT",
                "value": "v=DKIM1; p=public",
            }
        ],
    }


def _bucket_metrics(*, extra: dict[str, Any]) -> dict[str, Any]:
    """Build a metrics response with one bucket."""
    return {
        **extra,
        "buckets": {
            "day": [
                {
                    "count": 1,
                    "period_start": "2026-04-01T00:00:00Z",
                }
            ]
        },
    }


STRICT_RESPONSE_CASES = (
    StrictResponseCase(
        "emails-send",
        lambda client: client.emails.send(
            {
                "from": {"email": "sender@example.com"},
                "to": "recipient@example.net",
                "subject": "Hello",
                "text": "Hello",
            }
        ),
        SendResponse,
        {"id": "sent_123"},
    ),
    StrictResponseCase(
        "emails-queue",
        lambda client: client.emails.queue(
            {
                "from": {"email": "sender@example.com"},
                "to": "recipient@example.net",
                "subject": "Hello",
                "text": "Hello",
            }
        ),
        QueuedSendResponse,
        {"id": "queued_123"},
    ),
    StrictResponseCase(
        "usage",
        lambda client: client.usage.retrieve(),
        UsageStats,
        {"total_usage": 42},
        missing_required={"period_start_date": "2026-04-01"},
        invalid_type={"total_usage": "not-an-int"},
    ),
    StrictResponseCase(
        "domain-check",
        lambda client: client.check_domain.check("example.com"),
        CheckDomainResult,
        {
            "check_results": {"spf": {"verdict": "passed"}},
            "references": ["https://example.com/docs"],
        },
        invalid_type={"references": "not-a-list"},
    ),
    StrictResponseCase(
        "dkim-create",
        lambda client: client.dkim.create("example.com", selector="mcdkim"),
        DkimKeyInfo,
        _dkim_key(),
        missing_required={"selector": "mcdkim"},
        invalid_type={**_dkim_key(), "dkim_dns_records": [{"name": "missing"}]},
    ),
    StrictResponseCase(
        "dkim-list",
        lambda client: client.dkim.list("example.com"),
        DkimKeyList,
        {"keys": [_dkim_key()]},
        missing_required={"items": []},
        invalid_type={"keys": [{"selector": "missing-required-fields"}]},
    ),
    StrictResponseCase(
        "dkim-rotate",
        lambda client: client.dkim.rotate(
            "example.com",
            "mcdkim",
            new_selector="mcdkim2",
        ),
        DkimRotateResponse,
        {"new_key": _dkim_key("mcdkim2"), "rotated_key": _dkim_key()},
        missing_required={"new_key": _dkim_key("mcdkim2")},
        invalid_type={"new_key": _dkim_key("mcdkim2"), "rotated_key": {}},
    ),
    StrictResponseCase(
        "metrics-engagement",
        lambda client: client.metrics.engagement(),
        MetricsEngagement,
        _bucket_metrics(
            extra={
                "open": 1,
                "open_tracking_delivered": 2,
                "click": 3,
                "click_tracking_delivered": 4,
            }
        ),
        missing_required={"open": 1},
        invalid_type=_bucket_metrics(
            extra={
                "open": "bad",
                "open_tracking_delivered": 2,
                "click": 3,
                "click_tracking_delivered": 4,
            }
        ),
    ),
    StrictResponseCase(
        "metrics-performance",
        lambda client: client.metrics.performance(),
        MetricsPerformance,
        _bucket_metrics(extra={"processed": 1, "delivered": 2, "bounced": 3}),
        missing_required={"processed": 1},
        invalid_type=_bucket_metrics(
            extra={"processed": "bad", "delivered": 2, "bounced": 3}
        ),
    ),
    StrictResponseCase(
        "metrics-recipient-behaviour",
        lambda client: client.metrics.recipient_behaviour(),
        MetricsRecipientBehaviour,
        _bucket_metrics(extra={"unsubscribed": 1, "unsubscribe_delivered": 2}),
        missing_required={"unsubscribed": 1},
        invalid_type=_bucket_metrics(
            extra={"unsubscribed": "bad", "unsubscribe_delivered": 2}
        ),
    ),
    StrictResponseCase(
        "metrics-volume",
        lambda client: client.metrics.volume(),
        MetricsVolume,
        _bucket_metrics(extra={"processed": 1, "delivered": 2, "dropped": 3}),
        missing_required={"processed": 1},
        invalid_type=_bucket_metrics(
            extra={"processed": "bad", "delivered": 2, "dropped": 3}
        ),
    ),
    StrictResponseCase(
        "metrics-senders",
        lambda client: client.metrics.senders("sub-accounts"),
        MetricsSenderResponse,
        {
            "limit": 50,
            "offset": 0,
            "total": 1,
            "senders": [
                {
                    "name": "clienta",
                    "processed": 1,
                    "delivered": 1,
                    "dropped": 0,
                    "bounced": 0,
                }
            ],
        },
        missing_required={"limit": 50},
        invalid_type={"limit": 50, "offset": 0, "total": 1, "senders": [{}]},
    ),
    StrictResponseCase(
        "sub-account-create",
        lambda client: client.sub_accounts.create(handle="clienta"),
        SubAccount,
        {"handle": "clienta", "company_name": "Client A"},
    ),
    StrictResponseCase(
        "sub-account-limit-set",
        lambda client: client.sub_accounts.limits.set("clienta", sends=100),
        SubAccountLimit,
        {"sends": 100},
        invalid_type={"sends": "bad"},
    ),
    StrictResponseCase(
        "sub-account-limit-retrieve",
        lambda client: client.sub_accounts.limits.retrieve("clienta"),
        SubAccountLimit,
        {"sends": 100},
        invalid_type={"sends": "bad"},
    ),
    StrictResponseCase(
        "sub-account-usage",
        lambda client: client.sub_accounts.retrieve_usage("clienta"),
        SubAccountUsageStats,
        {"total_usage": 10},
    ),
    StrictResponseCase(
        "sub-account-api-key",
        lambda client: client.sub_accounts.api_keys.create("clienta"),
        ApiKey,
        {"id": "key_123", "api_key": "secret"},
    ),
    StrictResponseCase(
        "sub-account-smtp-password",
        lambda client: client.sub_accounts.smtp_passwords.create("clienta"),
        SmtpPassword,
        {"id": "smtp_123", "password": "secret"},
    ),
    StrictResponseCase(
        "suppressions-list",
        lambda client: client.suppressions.list(),
        SuppressionListResponse,
        {
            "suppression_list": [
                {
                    "recipient": "recipient@example.net",
                    "suppression_types": ["non-transactional"],
                    "source": "api",
                }
            ]
        },
        missing_required={"items": []},
        invalid_type={"suppression_list": [{"suppression_types": ["bad"]}]},
    ),
    StrictResponseCase(
        "webhook-batches",
        lambda client: client.webhooks.batches(),
        WebhookBatchResult,
        {
            "webhook_batches": [
                {
                    "batch_id": 123,
                    "customer_handle": "customer_123",
                    "webhook": "https://example.com/events",
                    "status": "2xx",
                    "created_at": "2026-04-01T00:00:00Z",
                    "event_count": 1,
                    "duration": {"value": 10, "unit": "milliseconds"},
                }
            ]
        },
        missing_required={"items": []},
        invalid_type={"webhook_batches": [{"batch_id": "bad"}]},
    ),
    StrictResponseCase(
        "webhook-public-key",
        lambda client: client.webhooks.public_key("mckey"),
        WebhookPublicKey,
        {"id": "mckey", "key": "public-key"},
        missing_required={"id": "mckey"},
        invalid_type={"id": 123, "key": "public-key"},
    ),
    StrictResponseCase(
        "webhook-validation",
        lambda client: client.webhooks.validate(request_id="req_123"),
        WebhookValidationResults,
        {
            "all_passed": True,
            "results": [
                {
                    "webhook": "https://example.com/events",
                    "result": "passed",
                    "response": {"status": 200, "body": "ok"},
                }
            ],
        },
        missing_required={"all_passed": True},
        invalid_type={"all_passed": "yes", "results": [{"result": "unknown"}]},
    ),
)


def test_client_reads_environment_configuration(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """It reads API key and API URL from environment variables."""
    monkeypatch.setenv("MAILCHANNELS_API_KEY", "env-key")
    monkeypatch.setenv("MAILCHANNELS_API_URL", "https://example.test/api")
    monkeypatch.setattr(mailchannels, "api_key", None)
    monkeypatch.setattr(mailchannels, "base_url", "")
    transport = FakeRequestsClient()

    client = Client(http_client=transport)
    client.emails.queue(
        {
            "from": {"email": "sender@example.com"},
            "to": "recipient@example.net",
            "subject": "Hello",
            "text": "Hello",
        }
    )

    assert transport.calls[0]["headers"]["X-Api-Key"] == "env-key"
    assert transport.calls[0]["url"] == "https://example.test/api/send-async"


def test_response_supports_headers_and_attribute_access() -> None:
    """It exposes response body keys as attributes and preserves HTTP headers."""
    transport = FakeRequestsClient(
        SDKResponse(
            202,
            {"id": "queued_123"},
            "{}",
            headers={"X-Request-ID": "req_123"},
        )
    )
    client = Client(api_key="test-key", http_client=transport)

    result = client.emails.queue(
        {
            "from": {"email": "sender@example.com"},
            "to": "recipient@example.net",
            "subject": "Hello",
            "text": "Hello",
        }
    )

    assert result.id == "queued_123"
    assert result["id"] == "queued_123"
    assert result.http_headers["X-Request-ID"] == "req_123"


def test_non_strict_responses_keep_dict_ergonomics() -> None:
    """It keeps dict-like responses by default even when a response model exists."""
    transport = FakeRequestsClient(SDKResponse(200, {"total_usage": 42}, "{}"))
    client = Client(api_key="test-key", http_client=transport)

    result = client.usage.retrieve()

    assert isinstance(result, dict)
    assert result.total_usage == 42


def test_strict_responses_return_pydantic_models() -> None:
    """It returns typed response models when strict response parsing is enabled."""
    transport = FakeRequestsClient(
        SDKResponse(
            200,
            {"total_usage": 42},
            "{}",
            headers={"X-Request-ID": "req_123"},
        )
    )
    client = Client(
        api_key="test-key",
        http_client=transport,
        strict_responses=True,
    )

    result = client.usage.retrieve()

    assert isinstance(result, UsageStats)
    assert result.total_usage == 42
    assert result.http_headers == {"X-Request-ID": "req_123"}


def test_strict_responses_raise_validation_errors() -> None:
    """It raises a structured SDK error when a typed response cannot be parsed."""
    transport = FakeRequestsClient(SDKResponse(200, {"period_start_date": "x"}, "{}"))
    client = Client(
        api_key="test-key",
        http_client=transport,
        strict_responses=True,
    )

    with pytest.raises(mailchannels.ResponseValidationError) as error:
        client.usage.retrieve()

    assert error.value.code == "ResponseValidationError"
    assert error.value.error_type == "response_validation_error"
    assert error.value.response["period_start_date"] == "x"


def test_module_level_strict_response_configuration(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """It supports strict response models through module-level configuration."""
    transport = FakeRequestsClient(SDKResponse(200, {"total_usage": 7}, "{}"))
    monkeypatch.setattr(mailchannels, "api_key", "module-key")
    monkeypatch.setattr(mailchannels, "default_http_client", transport)
    monkeypatch.setattr(mailchannels, "strict_responses", True)

    result = mailchannels.Usage.retrieve()

    assert isinstance(result, UsageStats)
    assert result.total_usage == 7


@pytest.mark.parametrize(
    "case",
    STRICT_RESPONSE_CASES,
    ids=[case.name for case in STRICT_RESPONSE_CASES],
)
def test_strict_response_models_parse_valid_api_bodies(
    case: StrictResponseCase,
) -> None:
    """Every wired strict response model parses valid API bodies with headers."""
    transport = FakeRequestsClient(
        SDKResponse(
            200,
            {**case.valid, "extra_field": "kept"},
            "{}",
            headers={"X-Request-ID": "req_strict"},
        )
    )
    client = Client(
        api_key="test-key",
        http_client=transport,
        strict_responses=True,
    )

    result = case.call(client)

    assert isinstance(result, case.model)
    assert result.http_headers == {"X-Request-ID": "req_strict"}
    assert result.extra_field == "kept"


@pytest.mark.parametrize(
    "case",
    [case for case in STRICT_RESPONSE_CASES if case.missing_required is not None],
    ids=[
        case.name
        for case in STRICT_RESPONSE_CASES
        if case.missing_required is not None
    ],
)
def test_strict_response_models_reject_missing_required_fields(
    case: StrictResponseCase,
) -> None:
    """Strict response models fail when stable required fields are absent."""
    transport = FakeRequestsClient(SDKResponse(200, case.missing_required, "{}"))
    client = Client(
        api_key="test-key",
        http_client=transport,
        strict_responses=True,
    )

    with pytest.raises(mailchannels.ResponseValidationError):
        case.call(client)


@pytest.mark.parametrize(
    "case",
    [case for case in STRICT_RESPONSE_CASES if case.invalid_type is not None],
    ids=[case.name for case in STRICT_RESPONSE_CASES if case.invalid_type is not None],
)
def test_strict_response_models_reject_invalid_field_types(
    case: StrictResponseCase,
) -> None:
    """Strict response models fail when API fields have invalid types."""
    transport = FakeRequestsClient(SDKResponse(200, case.invalid_type, "{}"))
    client = Client(
        api_key="test-key",
        http_client=transport,
        strict_responses=True,
    )

    with pytest.raises(mailchannels.ResponseValidationError):
        case.call(client)


def test_user_agent_uses_exported_version() -> None:
    """It builds the User-Agent from exported package version metadata."""
    transport = FakeRequestsClient()
    client = Client(api_key="test-key", http_client=transport)

    client.emails.queue(
        {
            "from": {"email": "sender@example.com"},
            "to": "recipient@example.net",
            "subject": "Hello",
            "text": "Hello",
        }
    )

    assert mailchannels.__version__ == "0.1.0"
    assert mailchannels.get_version() == mailchannels.__version__
    assert transport.calls[0]["headers"]["User-Agent"] == (
        f"mailchannels-python/{mailchannels.__version__}"
    )


def test_module_level_api_accepts_custom_http_client(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """It accepts any sync transport matching the public protocol."""

    class CustomTransport:
        """Custom transport that satisfies SyncHTTPClient."""

        def __init__(self) -> None:
            """Create a custom test transport."""
            self.calls: list[dict[str, object]] = []

        def request(
            self,
            method: str,
            url: str,
            *,
            headers: dict[str, str],
            json: dict[str, object] | None = None,
            params: dict[str, object] | None = None,
        ) -> SDKResponse:
            """Record a request and return a successful response."""
            self.calls.append(
                {
                    "method": method,
                    "url": url,
                    "headers": headers,
                    "json": json,
                    "params": params,
                }
            )
            return SDKResponse(202, {"id": "custom_123"}, "{}")

    transport = CustomTransport()
    monkeypatch.setattr(mailchannels, "api_key", "module-key")
    monkeypatch.setattr(mailchannels, "default_http_client", transport)

    result = mailchannels.Emails.queue(
        {
            "from": {"email": "sender@example.com"},
            "to": "recipient@example.net",
            "subject": "Hello",
            "text": "Hello",
        }
    )

    assert result.id == "custom_123"
    assert transport.calls[0]["headers"]["X-Api-Key"] == "module-key"
