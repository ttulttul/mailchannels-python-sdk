"""Configure and verify MailChannels webhooks."""

from __future__ import annotations

import logging
import os
from typing import Any

import mailchannels

logger = logging.getLogger(__name__)


def configure_webhook(client: mailchannels.Client, endpoint: str) -> dict[str, Any]:
    """Enroll an endpoint for MailChannels webhook events."""
    logger.info("Configuring example webhook endpoint=%s", endpoint)
    return client.webhooks.create(endpoint)


def validate_webhooks(client: mailchannels.Client) -> dict[str, Any]:
    """Ask MailChannels to send validation events to enrolled webhooks."""
    logger.info("Validating example webhooks")
    return client.webhooks.validate(request_id="example_validation")


def inspect_failed_batches(client: mailchannels.Client) -> dict[str, Any]:
    """Retrieve webhook batches with failure-like statuses."""
    logger.info("Inspecting failed webhook batches")
    return client.webhooks.batches(statuses=["4xx", "5xx", "no_response"], limit=50)


def verify_webhook_metadata(
    headers: dict[str, str],
    body: bytes,
    public_key: str | bytes | dict[str, object],
) -> str:
    """Verify webhook authenticity and return the signing key ID."""
    parameters = mailchannels.parse_signature_input(headers["Signature-Input"])
    if not mailchannels.Webhooks.verify(headers, body, public_key):
        logger.error("MailChannels webhook signature failed verification")
        raise ValueError("Invalid MailChannels webhook signature.")
    if parameters.key_id is None:
        logger.error("MailChannels webhook signature is missing a key ID")
        raise ValueError("Missing MailChannels webhook key ID.")
    return parameters.key_id


def main() -> None:
    """Run the webhook configuration example from environment configuration."""
    client = mailchannels.Client(api_key=os.environ["MAILCHANNELS_API_KEY"])
    print(configure_webhook(client, os.environ["WEBHOOK_ENDPOINT"]))


if __name__ == "__main__":
    main()
