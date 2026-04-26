"""Publish MailChannels DKIM DNS records through Cloudflare."""

from __future__ import annotations

import logging
import os
from typing import Any, Protocol

import mailchannels

logger = logging.getLogger(__name__)


class CloudflareClient(Protocol):
    """Minimal Cloudflare SDK surface used by this example."""

    zones: Any
    dns: Any


def create_mailchannels_dkim_record(
    client: mailchannels.Client,
    domain: str,
    selector: str,
) -> dict[str, Any]:
    """Create a MailChannels DKIM key and return the first DNS record."""
    logger.info(
        "Creating MailChannels DKIM DNS record example domain=%s selector=%s",
        domain,
        selector,
    )
    key = client.dkim.create(
        domain,
        selector=selector,
        algorithm="rsa",
        key_length=2048,
    )
    records = key.get("dkim_dns_records", [])
    if not records:
        raise RuntimeError("MailChannels did not return a DKIM DNS record.")
    return dict(records[0])


def publish_dkim_record(
    cloudflare: CloudflareClient,
    domain: str,
    dns_record: dict[str, str],
) -> Any:
    """Create or update a Cloudflare TXT record for a MailChannels DKIM key."""
    logger.info("Publishing DKIM record in Cloudflare domain=%s", domain)
    zones = cloudflare.zones.list(name=domain)
    zone = next(iter(zones), None)
    if zone is None:
        raise RuntimeError(f"Cloudflare zone not found: {domain}")

    records = cloudflare.dns.records.list(
        zone_id=zone.id,
        type="TXT",
        name=dns_record["name"],
    )
    existing_record = next(iter(records), None)
    payload = {
        "zone_id": zone.id,
        "type": "TXT",
        "name": dns_record["name"],
        "content": dns_record["value"],
        "ttl": 1,
    }
    if existing_record is None:
        return cloudflare.dns.records.create(**payload)
    return cloudflare.dns.records.update(existing_record.id, **payload)


def create_and_publish_dkim_record(
    client: mailchannels.Client,
    cloudflare: CloudflareClient,
    domain: str,
    selector: str,
) -> Any:
    """Create a MailChannels DKIM key and publish its DNS record."""
    dns_record = create_mailchannels_dkim_record(client, domain, selector)
    return publish_dkim_record(cloudflare, domain, dns_record)


def main() -> None:
    """Run the Cloudflare DKIM publication example from environment variables."""
    from cloudflare import Cloudflare

    client = mailchannels.Client(api_key=os.environ["MAILCHANNELS_API_KEY"])
    domain = os.environ["MAILCHANNELS_DOMAIN"]
    selector = os.environ.get("MAILCHANNELS_DKIM_SELECTOR", "mcdkim")
    cloudflare = Cloudflare()
    print(create_and_publish_dkim_record(client, cloudflare, domain, selector))


if __name__ == "__main__":
    main()
