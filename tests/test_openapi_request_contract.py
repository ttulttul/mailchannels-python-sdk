"""Operation-level request contracts for documented OpenAPI routes."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any
from urllib.parse import urlparse

import pytest
from conftest import FakeRequestsClient

from mailchannels.client import Client
from mailchannels.routes import sdk_route_keys

BASE_PATH = "/tx/v1"
DEFAULT_HEADERS = frozenset({"Content-Type", "User-Agent", "X-Api-Key"})


@dataclass(frozen=True)
class OperationContract:
    """Expected request shape for one SDK-supported OpenAPI operation."""

    method: str
    path_template: str
    call: Callable[[Client], None]
    path: str | None = None
    json_required: frozenset[str] = field(default_factory=frozenset)
    json_allowed: frozenset[str] = field(default_factory=frozenset)
    json_forbidden: frozenset[str] = field(default_factory=frozenset)
    query_required: frozenset[str] = field(default_factory=frozenset)
    query_allowed: frozenset[str] = field(default_factory=frozenset)
    headers_required: frozenset[str] = DEFAULT_HEADERS
    headers_forbidden: frozenset[str] = field(default_factory=frozenset)

    @property
    def key(self) -> tuple[str, str]:
        """Return the SDK route key covered by this contract."""
        return (self.method, self.path_template)

    @property
    def expected_path(self) -> str:
        """Return the concrete path expected in the outgoing request."""
        return self.path or self.path_template


def _sample_email() -> dict[str, Any]:
    """Return a minimal valid MailChannels send payload."""
    return {
        "from": {"email": "sender@example.com"},
        "to": "recipient@example.net",
        "subject": "Contract test",
        "text": "Hello from the request contract test.",
    }


def _suppression_entry() -> dict[str, str]:
    """Return a minimal suppression-list entry."""
    return {"recipient": "recipient@example.net", "source": "api"}


ROUTE_CONTRACTS: tuple[OperationContract, ...] = (
    OperationContract(
        "POST",
        "/check-domain",
        lambda client: client.check_domain.check(
            "example.com",
            sender_id="sender-123",
            dkim_settings=[{"dkim_selector": "mcdkim"}],
        ),
        json_required=frozenset({"domain"}),
        json_allowed=frozenset({"domain", "sender_id", "dkim_settings"}),
    ),
    OperationContract(
        "POST",
        "/send",
        lambda client: client.emails.send(_sample_email(), dry_run=True),
        json_required=frozenset({"from", "personalizations", "subject", "content"}),
        json_allowed=frozenset({"from", "personalizations", "subject", "content"}),
        query_required=frozenset({"dry-run"}),
        query_allowed=frozenset({"dry-run"}),
    ),
    OperationContract(
        "POST",
        "/send-async",
        lambda client: client.emails.queue(_sample_email()),
        json_required=frozenset({"from", "personalizations", "subject", "content"}),
        json_allowed=frozenset({"from", "personalizations", "subject", "content"}),
    ),
    OperationContract(
        "POST",
        "/domains/{domain}/dkim-keys",
        lambda client: client.dkim.create(
            "example.com",
            selector="mcdkim",
            algorithm="rsa",
            key_length=2048,
        ),
        path="/domains/example.com/dkim-keys",
        json_required=frozenset({"selector"}),
        json_allowed=frozenset({"selector", "algorithm", "key_length"}),
    ),
    OperationContract(
        "GET",
        "/domains/{domain}/dkim-keys",
        lambda client: client.dkim.list(
            "example.com",
            selector="mcdkim",
            status="active",
            limit=10,
            offset=0,
            include_dns_record=True,
        ),
        path="/domains/example.com/dkim-keys",
        query_required=frozenset(
            {"selector", "status", "limit", "offset", "include_dns_record"}
        ),
        query_allowed=frozenset(
            {"selector", "status", "limit", "offset", "include_dns_record"}
        ),
    ),
    OperationContract(
        "PATCH",
        "/domains/{domain}/dkim-keys/{selector}",
        lambda client: client.dkim.update_status(
            "example.com",
            "mcdkim",
            status="inactive",
        ),
        path="/domains/example.com/dkim-keys/mcdkim",
        json_required=frozenset({"status"}),
        json_allowed=frozenset({"status"}),
    ),
    OperationContract(
        "POST",
        "/domains/{domain}/dkim-keys/{selector}/rotate",
        lambda client: client.dkim.rotate(
            "example.com",
            "mcdkim",
            new_selector="mcdkim2",
        ),
        path="/domains/example.com/dkim-keys/mcdkim/rotate",
        json_required=frozenset({"new_key"}),
        json_allowed=frozenset({"new_key"}),
    ),
    OperationContract(
        "GET",
        "/metrics/engagement",
        lambda client: client.metrics.engagement(
            start_time="2026-04-01",
            end_time="2026-04-24",
            campaign_id="newsletter",
            interval="day",
        ),
        query_required=frozenset(
            {"start_time", "end_time", "campaign_id", "interval"}
        ),
        query_allowed=frozenset(
            {"start_time", "end_time", "campaign_id", "interval"}
        ),
    ),
    OperationContract(
        "GET",
        "/metrics/performance",
        lambda client: client.metrics.performance(
            start_time="2026-04-01",
            end_time="2026-04-24",
            campaign_id="newsletter",
            interval="day",
        ),
        query_required=frozenset(
            {"start_time", "end_time", "campaign_id", "interval"}
        ),
        query_allowed=frozenset(
            {"start_time", "end_time", "campaign_id", "interval"}
        ),
    ),
    OperationContract(
        "GET",
        "/metrics/recipient-behaviour",
        lambda client: client.metrics.recipient_behaviour(
            start_time="2026-04-01",
            end_time="2026-04-24",
            campaign_id="newsletter",
            interval="day",
        ),
        query_required=frozenset(
            {"start_time", "end_time", "campaign_id", "interval"}
        ),
        query_allowed=frozenset(
            {"start_time", "end_time", "campaign_id", "interval"}
        ),
    ),
    OperationContract(
        "GET",
        "/metrics/volume",
        lambda client: client.metrics.volume(
            start_time="2026-04-01",
            end_time="2026-04-24",
            campaign_id="newsletter",
            interval="day",
        ),
        query_required=frozenset(
            {"start_time", "end_time", "campaign_id", "interval"}
        ),
        query_allowed=frozenset(
            {"start_time", "end_time", "campaign_id", "interval"}
        ),
    ),
    OperationContract(
        "GET",
        "/metrics/senders/{sender_type}",
        lambda client: client.metrics.senders(
            "campaigns",
            start_time="2026-04-01",
            end_time="2026-04-24",
            limit=50,
            offset=0,
            sort_order="desc",
        ),
        path="/metrics/senders/campaigns",
        query_required=frozenset(
            {"start_time", "end_time", "limit", "offset", "sort_order"}
        ),
        query_allowed=frozenset(
            {"start_time", "end_time", "limit", "offset", "sort_order"}
        ),
    ),
    OperationContract(
        "POST",
        "/sub-account",
        lambda client: client.sub_accounts.create(
            company_name="Client A",
            handle="clienta",
        ),
        json_required=frozenset({"company_name", "handle"}),
        json_allowed=frozenset({"company_name", "handle"}),
    ),
    OperationContract(
        "GET",
        "/sub-account",
        lambda client: client.sub_accounts.list(limit=25, offset=5),
        query_required=frozenset({"limit", "offset"}),
        query_allowed=frozenset({"limit", "offset"}),
    ),
    OperationContract(
        "DELETE",
        "/sub-account/{handle}",
        lambda client: client.sub_accounts.delete("clienta"),
        path="/sub-account/clienta",
    ),
    OperationContract(
        "POST",
        "/sub-account/{handle}/activate",
        lambda client: client.sub_accounts.activate("clienta"),
        path="/sub-account/clienta/activate",
    ),
    OperationContract(
        "POST",
        "/sub-account/{handle}/api-key",
        lambda client: client.sub_accounts.api_keys.create("clienta"),
        path="/sub-account/clienta/api-key",
    ),
    OperationContract(
        "GET",
        "/sub-account/{handle}/api-key",
        lambda client: client.sub_accounts.api_keys.list("clienta"),
        path="/sub-account/clienta/api-key",
    ),
    OperationContract(
        "DELETE",
        "/sub-account/{handle}/api-key/{id}",
        lambda client: client.sub_accounts.api_keys.delete("clienta", "key_123"),
        path="/sub-account/clienta/api-key/key_123",
    ),
    OperationContract(
        "PUT",
        "/sub-account/{handle}/limit",
        lambda client: client.sub_accounts.limits.set("clienta", sends=100_000),
        path="/sub-account/clienta/limit",
        json_required=frozenset({"sends"}),
        json_allowed=frozenset({"sends"}),
        json_forbidden=frozenset({"monthly_limit"}),
    ),
    OperationContract(
        "GET",
        "/sub-account/{handle}/limit",
        lambda client: client.sub_accounts.limits.retrieve("clienta"),
        path="/sub-account/clienta/limit",
    ),
    OperationContract(
        "DELETE",
        "/sub-account/{handle}/limit",
        lambda client: client.sub_accounts.limits.delete("clienta"),
        path="/sub-account/clienta/limit",
    ),
    OperationContract(
        "POST",
        "/sub-account/{handle}/smtp-password",
        lambda client: client.sub_accounts.smtp_passwords.create("clienta"),
        path="/sub-account/clienta/smtp-password",
    ),
    OperationContract(
        "GET",
        "/sub-account/{handle}/smtp-password",
        lambda client: client.sub_accounts.smtp_passwords.list("clienta"),
        path="/sub-account/clienta/smtp-password",
    ),
    OperationContract(
        "DELETE",
        "/sub-account/{handle}/smtp-password/{id}",
        lambda client: client.sub_accounts.smtp_passwords.delete(
            "clienta",
            "smtp_123",
        ),
        path="/sub-account/clienta/smtp-password/smtp_123",
    ),
    OperationContract(
        "POST",
        "/sub-account/{handle}/suspend",
        lambda client: client.sub_accounts.suspend("clienta"),
        path="/sub-account/clienta/suspend",
    ),
    OperationContract(
        "GET",
        "/sub-account/{handle}/usage",
        lambda client: client.sub_accounts.retrieve_usage("clienta"),
        path="/sub-account/clienta/usage",
    ),
    OperationContract(
        "POST",
        "/suppression-list",
        lambda client: client.suppressions.create(
            [_suppression_entry()],
            add_to_sub_accounts=True,
        ),
        json_required=frozenset({"suppression_entries", "add_to_sub_accounts"}),
        json_allowed=frozenset({"suppression_entries", "add_to_sub_accounts"}),
    ),
    OperationContract(
        "GET",
        "/suppression-list",
        lambda client: client.suppressions.list(
            recipient="recipient@example.net",
            source="api",
            created_before="2026-04-24T00:00:00Z",
            created_after="2026-04-01T00:00:00Z",
            limit=100,
            offset=0,
        ),
        query_required=frozenset(
            {
                "recipient",
                "source",
                "created_before",
                "created_after",
                "limit",
                "offset",
            }
        ),
        query_allowed=frozenset(
            {
                "recipient",
                "source",
                "created_before",
                "created_after",
                "limit",
                "offset",
            }
        ),
    ),
    OperationContract(
        "DELETE",
        "/suppression-list/recipients/{recipient}",
        lambda client: client.suppressions.delete(
            "recipient@example.net",
            source="api",
        ),
        path="/suppression-list/recipients/recipient@example.net",
        query_required=frozenset({"source"}),
        query_allowed=frozenset({"source"}),
    ),
    OperationContract("GET", "/usage", lambda client: client.usage.retrieve()),
    OperationContract(
        "POST",
        "/webhook",
        lambda client: client.webhooks.create("https://example.com/mailchannels"),
        query_required=frozenset({"endpoint"}),
        query_allowed=frozenset({"endpoint"}),
    ),
    OperationContract("GET", "/webhook", lambda client: client.webhooks.list()),
    OperationContract("DELETE", "/webhook", lambda client: client.webhooks.delete()),
    OperationContract(
        "GET",
        "/webhook-batch",
        lambda client: client.webhooks.batches(
            created_after="2026-04-01T00:00:00Z",
            created_before="2026-04-24T00:00:00Z",
            statuses=["4xx", "5xx"],
            webhook="https://example.com/mailchannels",
            limit=25,
            offset=5,
        ),
        query_required=frozenset(
            {
                "created_after",
                "created_before",
                "statuses",
                "webhook",
                "limit",
                "offset",
            }
        ),
        query_allowed=frozenset(
            {
                "created_after",
                "created_before",
                "statuses",
                "webhook",
                "limit",
                "offset",
            }
        ),
    ),
    OperationContract(
        "POST",
        "/webhook-batch/{batch_id}/resend",
        lambda client: client.webhooks.resend_batch(123, customer_handle="clienta"),
        path="/webhook-batch/123/resend",
        headers_required=frozenset(
            {"Content-Type", "User-Agent", "X-Customer-Handle"}
        ),
        headers_forbidden=frozenset({"X-Api-Key"}),
    ),
    OperationContract(
        "GET",
        "/webhook/public-key",
        lambda client: client.webhooks.public_key("mckey"),
        query_required=frozenset({"id"}),
        query_allowed=frozenset({"id"}),
        headers_required=frozenset({"Content-Type", "User-Agent"}),
        headers_forbidden=frozenset({"X-Api-Key"}),
    ),
    OperationContract(
        "POST",
        "/webhook/validate",
        lambda client: client.webhooks.validate(request_id="test_request_1"),
        json_required=frozenset({"request_id"}),
        json_allowed=frozenset({"request_id"}),
    ),
)


def test_operation_contracts_cover_every_sdk_route() -> None:
    """Every declared SDK route should have an executable request contract."""
    assert {contract.key for contract in ROUTE_CONTRACTS} == sdk_route_keys()


@pytest.mark.parametrize(
    "contract",
    ROUTE_CONTRACTS,
    ids=lambda item: " ".join(item.key),
)
def test_sdk_requests_match_openapi_operation_contract(
    contract: OperationContract,
) -> None:
    """SDK calls should emit the documented OpenAPI request shape."""
    transport = FakeRequestsClient()
    client = Client(api_key="test-key", http_client=transport)

    contract.call(client)

    assert len(transport.calls) == 1
    call = transport.calls[0]
    assert call["method"] == contract.method
    assert _request_path(call["url"]) == contract.expected_path
    _assert_json_contract(call["json"], contract)
    _assert_query_contract(call["params"], contract)
    _assert_header_contract(call["headers"], contract)


def _request_path(url: str) -> str:
    """Return the API path without the configured base prefix."""
    path = urlparse(url).path
    if not path.startswith(BASE_PATH):
        raise AssertionError(f"Unexpected API base path in URL: {url}")
    return path.removeprefix(BASE_PATH)


def _assert_json_contract(
    payload: dict[str, Any] | None,
    contract: OperationContract,
) -> None:
    """Assert the outgoing JSON payload matches the operation contract."""
    if not contract.json_allowed and not contract.json_required:
        assert payload is None
        return
    assert payload is not None
    keys = set(payload)
    assert contract.json_required <= keys
    assert keys <= contract.json_allowed
    assert keys.isdisjoint(contract.json_forbidden)


def _assert_query_contract(
    params: dict[str, Any] | None,
    contract: OperationContract,
) -> None:
    """Assert outgoing query parameters match the operation contract."""
    if not contract.query_allowed and not contract.query_required:
        assert params is None
        return
    assert params is not None
    keys = set(params)
    assert contract.query_required <= keys
    assert keys <= contract.query_allowed


def _assert_header_contract(
    headers: dict[str, str],
    contract: OperationContract,
) -> None:
    """Assert required and forbidden operation headers."""
    keys = set(headers)
    assert contract.headers_required <= keys
    assert keys.isdisjoint(contract.headers_forbidden)
