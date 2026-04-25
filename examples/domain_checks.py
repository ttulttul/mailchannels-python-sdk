"""Check domain authentication configuration."""

from __future__ import annotations

import logging
import os
from typing import Any

import mailchannels

logger = logging.getLogger(__name__)


def check_domain_configuration(
    client: mailchannels.Client,
    domain: str,
) -> dict[str, Any]:
    """Check DKIM, SPF, sender-domain DNS, and Domain Lockdown for a domain."""
    logger.info("Checking example domain configuration domain=%s", domain)
    return client.domain_checks.check(domain)


def check_domain_with_dkim_selector(
    client: mailchannels.Client,
    domain: str,
    selector: str,
) -> dict[str, Any]:
    """Check a domain using one stored MailChannels DKIM selector."""
    logger.info(
        "Checking example domain configuration with DKIM selector domain=%s "
        "selector=%s",
        domain,
        selector,
    )
    return client.domain_checks.check(
        domain,
        dkim_settings=[
            mailchannels.DkimSetting(
                dkim_domain=domain,
                dkim_selector=selector,
            )
        ],
    )


def main() -> None:
    """Run the domain check example from environment configuration."""
    client = mailchannels.Client(api_key=os.environ["MAILCHANNELS_API_KEY"])
    domain = os.environ["MAILCHANNELS_DOMAIN"]
    print(check_domain_configuration(client, domain))


if __name__ == "__main__":
    main()
