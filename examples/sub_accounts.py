"""Manage MailChannels sub-accounts."""

from __future__ import annotations

import logging
import os
from typing import Any

import mailchannels

logger = logging.getLogger(__name__)


def create_sub_account(
    client: mailchannels.Client,
    handle: str,
    company_name: str,
) -> dict[str, Any]:
    """Create a sub-account for an isolated tenant."""
    logger.info("Creating example sub-account handle=%s", handle)
    return client.sub_accounts.create(handle=handle, company_name=company_name)


def create_sub_account_api_key(
    client: mailchannels.Client,
    handle: str,
) -> dict[str, Any]:
    """Create an API key for a sub-account."""
    logger.info("Creating example sub-account API key handle=%s", handle)
    return client.sub_accounts.api_keys.create(handle)


def set_sub_account_limit(
    client: mailchannels.Client,
    handle: str,
    sends: int,
) -> dict[str, Any]:
    """Set a monthly sending limit for a sub-account."""
    logger.info("Setting example sub-account limit handle=%s sends=%s", handle, sends)
    return client.sub_accounts.limits.set(handle, sends=sends)


def retrieve_sub_account_usage(
    client: mailchannels.Client,
    handle: str,
) -> dict[str, Any]:
    """Retrieve usage for a sub-account."""
    logger.info("Retrieving example sub-account usage handle=%s", handle)
    return client.sub_accounts.retrieve_usage(handle)


def main() -> None:
    """Run the sub-account example from environment configuration."""
    client = mailchannels.Client(api_key=os.environ["MAILCHANNELS_API_KEY"])
    handle = os.environ.get("MAILCHANNELS_SUB_ACCOUNT_HANDLE", "clienta")
    print(create_sub_account(client, handle, "Client A"))


if __name__ == "__main__":
    main()
