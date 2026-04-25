"""Manage MailChannels suppression-list entries."""

from __future__ import annotations

import logging
import os
from typing import Any

import mailchannels

logger = logging.getLogger(__name__)


def create_suppression(client: mailchannels.Client, recipient: str) -> dict[str, Any]:
    """Create a non-transactional suppression entry."""
    logger.info("Creating example suppression recipient=%s", recipient)
    return client.suppressions.create(
        [
            {
                "recipient": recipient,
                "suppression_types": ["non-transactional"],
                "notes": "Example preference-center opt-out.",
            }
        ],
        add_to_sub_accounts=True,
    )


def list_api_suppressions(client: mailchannels.Client) -> dict[str, Any]:
    """List API-created suppression entries."""
    logger.info("Listing example API suppressions")
    return client.suppressions.list(source="api", limit=100, offset=0)


def delete_suppression(client: mailchannels.Client, recipient: str) -> dict[str, Any]:
    """Delete all suppression entries for one recipient."""
    logger.info("Deleting example suppression recipient=%s", recipient)
    return client.suppressions.delete(recipient, source="all")


def main() -> None:
    """Run the suppression example from environment configuration."""
    client = mailchannels.Client(api_key=os.environ["MAILCHANNELS_API_KEY"])
    recipient = os.environ["SUPPRESSION_RECIPIENT"]
    create_suppression(client, recipient)
    print(list_api_suppressions(client))


if __name__ == "__main__":
    main()
