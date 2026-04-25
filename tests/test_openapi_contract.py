"""Contract tests for SDK routes documented in the MailChannels OpenAPI spec."""

from __future__ import annotations

from mailchannels.routes import SDK_ROUTES, sdk_route_keys

OPENAPI_ROUTE_SNAPSHOT: set[tuple[str, str]] = {
    ("DELETE", "/sub-account/{handle}"),
    ("DELETE", "/sub-account/{handle}/api-key/{id}"),
    ("DELETE", "/sub-account/{handle}/limit"),
    ("DELETE", "/sub-account/{handle}/smtp-password/{id}"),
    ("DELETE", "/suppression-list/recipients/{recipient}"),
    ("DELETE", "/webhook"),
    ("GET", "/domains/{domain}/dkim-keys"),
    ("GET", "/metrics/engagement"),
    ("GET", "/metrics/performance"),
    ("GET", "/metrics/recipient-behaviour"),
    ("GET", "/metrics/senders/{sender_type}"),
    ("GET", "/metrics/volume"),
    ("GET", "/sub-account"),
    ("GET", "/sub-account/{handle}/api-key"),
    ("GET", "/sub-account/{handle}/limit"),
    ("GET", "/sub-account/{handle}/smtp-password"),
    ("GET", "/sub-account/{handle}/usage"),
    ("GET", "/suppression-list"),
    ("GET", "/usage"),
    ("GET", "/webhook"),
    ("GET", "/webhook-batch"),
    ("GET", "/webhook/public-key"),
    ("PATCH", "/domains/{domain}/dkim-keys/{selector}"),
    ("POST", "/check-domain"),
    ("POST", "/domains/{domain}/dkim-keys"),
    ("POST", "/domains/{domain}/dkim-keys/{selector}/rotate"),
    ("POST", "/send"),
    ("POST", "/send-async"),
    ("POST", "/sub-account"),
    ("POST", "/sub-account/{handle}/activate"),
    ("POST", "/sub-account/{handle}/api-key"),
    ("POST", "/sub-account/{handle}/smtp-password"),
    ("POST", "/sub-account/{handle}/suspend"),
    ("POST", "/suppression-list"),
    ("POST", "/webhook"),
    ("POST", "/webhook-batch/{batch_id}/resend"),
    ("POST", "/webhook/validate"),
    ("PUT", "/sub-account/{handle}/limit"),
}


def test_sdk_routes_match_openapi_route_snapshot() -> None:
    """Every SDK route should appear in the OpenAPI route snapshot."""
    assert sdk_route_keys() <= OPENAPI_ROUTE_SNAPSHOT


def test_openapi_route_snapshot_covers_every_declared_sdk_route() -> None:
    """The route snapshot should stay aligned with the SDK route registry."""
    assert len(OPENAPI_ROUTE_SNAPSHOT) == len(SDK_ROUTES)


def test_contract_includes_domain_check_endpoint() -> None:
    """The `/check-domain` endpoint should be part of the public API contract."""
    assert ("POST", "/check-domain") in OPENAPI_ROUTE_SNAPSHOT
    assert ("POST", "/check-domain") in sdk_route_keys()


def test_contract_uses_singular_sub_account_limit_endpoint() -> None:
    """Sub-account limits should use singular `/limit` and PUT for writes."""
    assert ("PUT", "/sub-account/{handle}/limit") in OPENAPI_ROUTE_SNAPSHOT
    assert ("GET", "/sub-account/{handle}/limit") in OPENAPI_ROUTE_SNAPSHOT
    assert ("DELETE", "/sub-account/{handle}/limit") in OPENAPI_ROUTE_SNAPSHOT
    assert ("POST", "/sub-account/{handle}/limits") not in OPENAPI_ROUTE_SNAPSHOT
    assert ("POST", "/sub-account/{handle}/limits") not in sdk_route_keys()
