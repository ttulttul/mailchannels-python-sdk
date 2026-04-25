"""SDK route declarations used for API conformance checks."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Literal

logger = logging.getLogger(__name__)

HTTPMethod = Literal["DELETE", "GET", "PATCH", "POST", "PUT"]


@dataclass(frozen=True)
class SDKRoute:
    """One MailChannels API route supported by the SDK."""

    method: HTTPMethod
    path: str
    resource: str
    operation: str


SDK_ROUTES: tuple[SDKRoute, ...] = (
    SDKRoute("POST", "/check-domain", "DomainChecks", "check"),
    SDKRoute("POST", "/send", "Emails", "send"),
    SDKRoute("POST", "/send-async", "Emails", "queue"),
    SDKRoute("POST", "/domains/{domain}/dkim-keys", "Dkim", "create"),
    SDKRoute("GET", "/domains/{domain}/dkim-keys", "Dkim", "list"),
    SDKRoute(
        "PATCH",
        "/domains/{domain}/dkim-keys/{selector}",
        "Dkim",
        "update_status",
    ),
    SDKRoute(
        "POST",
        "/domains/{domain}/dkim-keys/{selector}/rotate",
        "Dkim",
        "rotate",
    ),
    SDKRoute("GET", "/metrics/engagement", "Metrics", "engagement"),
    SDKRoute("GET", "/metrics/performance", "Metrics", "performance"),
    SDKRoute(
        "GET",
        "/metrics/recipient-behaviour",
        "Metrics",
        "recipient_behaviour",
    ),
    SDKRoute("GET", "/metrics/volume", "Metrics", "volume"),
    SDKRoute("GET", "/metrics/senders/{sender_type}", "Metrics", "senders"),
    SDKRoute("POST", "/sub-account", "SubAccounts", "create"),
    SDKRoute("GET", "/sub-account", "SubAccounts", "list"),
    SDKRoute("DELETE", "/sub-account/{handle}", "SubAccounts", "delete"),
    SDKRoute("POST", "/sub-account/{handle}/activate", "SubAccounts", "activate"),
    SDKRoute("POST", "/sub-account/{handle}/api-key", "SubAccounts.ApiKeys", "create"),
    SDKRoute("GET", "/sub-account/{handle}/api-key", "SubAccounts.ApiKeys", "list"),
    SDKRoute(
        "DELETE",
        "/sub-account/{handle}/api-key/{id}",
        "SubAccounts.ApiKeys",
        "delete",
    ),
    SDKRoute("PUT", "/sub-account/{handle}/limit", "SubAccounts.Limits", "set"),
    SDKRoute("GET", "/sub-account/{handle}/limit", "SubAccounts.Limits", "retrieve"),
    SDKRoute("DELETE", "/sub-account/{handle}/limit", "SubAccounts.Limits", "delete"),
    SDKRoute(
        "POST",
        "/sub-account/{handle}/smtp-password",
        "SubAccounts.SmtpPasswords",
        "create",
    ),
    SDKRoute(
        "GET",
        "/sub-account/{handle}/smtp-password",
        "SubAccounts.SmtpPasswords",
        "list",
    ),
    SDKRoute(
        "DELETE",
        "/sub-account/{handle}/smtp-password/{id}",
        "SubAccounts.SmtpPasswords",
        "delete",
    ),
    SDKRoute("POST", "/sub-account/{handle}/suspend", "SubAccounts", "suspend"),
    SDKRoute("GET", "/sub-account/{handle}/usage", "SubAccounts", "retrieve_usage"),
    SDKRoute("POST", "/suppression-list", "Suppressions", "create"),
    SDKRoute("GET", "/suppression-list", "Suppressions", "list"),
    SDKRoute(
        "DELETE",
        "/suppression-list/recipients/{recipient}",
        "Suppressions",
        "delete",
    ),
    SDKRoute("GET", "/usage", "Usage", "retrieve"),
    SDKRoute("POST", "/webhook", "Webhooks", "create"),
    SDKRoute("GET", "/webhook", "Webhooks", "list"),
    SDKRoute("DELETE", "/webhook", "Webhooks", "delete"),
    SDKRoute("GET", "/webhook-batch", "Webhooks", "batches"),
    SDKRoute("POST", "/webhook-batch/{batch_id}/resend", "Webhooks", "resend_batch"),
    SDKRoute("GET", "/webhook/public-key", "Webhooks", "public_key"),
    SDKRoute("POST", "/webhook/validate", "Webhooks", "validate"),
)


def sdk_route_keys() -> set[tuple[str, str]]:
    """Return method/path pairs for all declared SDK routes."""
    logger.debug("Collected %s SDK route declarations.", len(SDK_ROUTES))
    return {(route.method, route.path) for route in SDK_ROUTES}
