"""Send messages with MailChannels unsubscribe support."""

from __future__ import annotations

import logging
import os
from typing import Any

import mailchannels

logger = logging.getLogger(__name__)


def build_one_click_unsubscribe_message() -> dict[str, Any]:
    """Build a mustache message with MailChannels' hosted unsubscribe URL."""
    logger.info("Building one-click unsubscribe example message")
    return {
        "from": {"email": "sender@example.com"},
        "personalizations": [{"to": [{"email": "recipient@example.net"}]}],
        "subject": "Newsletter",
        "content": [
            {
                "type": "text/html",
                "value": (
                    "<p>Hello</p>"
                    f"<a href='{mailchannels.UNSUBSCRIBE_URL_PLACEHOLDER}'>"
                    "unsubscribe</a>"
                ),
                "template_type": "mustache",
            }
        ],
    }


def build_list_unsubscribe_message() -> dict[str, Any]:
    """Build a message that asks MailChannels to add List-Unsubscribe headers."""
    logger.info("Building automatic List-Unsubscribe example message")
    return {
        "from": {"email": "sender@example.com"},
        "personalizations": [
            {
                "to": [{"email": "recipient@example.net"}],
                "dkim_domain": "example.com",
                "dkim_selector": "mailchannels",
                "dkim_private_key": "-----BEGIN PRIVATE KEY-----...",
            }
        ],
        "subject": "Newsletter",
        "text": "Hello",
        "transactional": False,
    }


def queue_unsubscribe_message(client: mailchannels.Client) -> dict[str, Any]:
    """Queue a one-click unsubscribe example message."""
    return client.emails.queue(build_one_click_unsubscribe_message())


def main() -> None:
    """Run the unsubscribe example from environment configuration."""
    client = mailchannels.Client(api_key=os.environ["MAILCHANNELS_API_KEY"])
    print(queue_unsubscribe_message(client))


if __name__ == "__main__":
    main()
