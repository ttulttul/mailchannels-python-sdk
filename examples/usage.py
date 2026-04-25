"""Retrieve MailChannels account usage."""

from __future__ import annotations

import logging
import os
from typing import Any

import mailchannels

logger = logging.getLogger(__name__)


def retrieve_account_usage(client: mailchannels.Client) -> dict[str, Any]:
    """Retrieve parent-account usage for the current billing period."""
    logger.info("Retrieving example parent-account usage")
    return client.usage.retrieve()


def retrieve_sub_account_usage(
    client: mailchannels.Client,
    handle: str,
) -> dict[str, Any]:
    """Retrieve usage for one sub-account handle."""
    logger.info("Retrieving example sub-account usage handle=%s", handle)
    return client.sub_accounts.retrieve_usage(handle)


def main() -> None:
    """Run the usage example from environment configuration."""
    client = mailchannels.Client(api_key=os.environ["MAILCHANNELS_API_KEY"])
    print(retrieve_account_usage(client))


if __name__ == "__main__":
    main()
