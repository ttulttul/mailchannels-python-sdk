"""Manage MailChannels-hosted DKIM keys."""

from __future__ import annotations

import logging
import os
from typing import Any

import mailchannels

logger = logging.getLogger(__name__)


def create_hosted_dkim_key(
    client: mailchannels.Client,
    domain: str,
    selector: str,
) -> dict[str, Any]:
    """Create a MailChannels-hosted DKIM key pair."""
    logger.info("Creating example DKIM key domain=%s selector=%s", domain, selector)
    return client.dkim.create(
        domain,
        selector=selector,
        algorithm="rsa",
        key_length=2048,
    )


def list_hosted_dkim_keys(
    client: mailchannels.Client,
    domain: str,
) -> dict[str, Any]:
    """List MailChannels-hosted DKIM keys including DNS record suggestions."""
    logger.info("Listing example DKIM keys domain=%s", domain)
    return client.dkim.list(domain, include_dns_record=True)


def rotate_hosted_dkim_key(
    client: mailchannels.Client,
    domain: str,
    selector: str,
    new_selector: str,
) -> dict[str, Any]:
    """Rotate a MailChannels-hosted DKIM key pair."""
    logger.warning(
        "Rotating example DKIM key domain=%s selector=%s new_selector=%s",
        domain,
        selector,
        new_selector,
    )
    return client.dkim.rotate(domain, selector, new_selector=new_selector)


def main() -> None:
    """Run the DKIM example from environment configuration."""
    client = mailchannels.Client(api_key=os.environ["MAILCHANNELS_API_KEY"])
    domain = os.environ["MAILCHANNELS_DOMAIN"]
    selector = os.environ.get("MAILCHANNELS_DKIM_SELECTOR", "mcdkim")
    print(create_hosted_dkim_key(client, domain, selector))


if __name__ == "__main__":
    main()
