"""Send messages with custom email headers."""

from __future__ import annotations

import logging
import os
from typing import Any

import mailchannels

logger = logging.getLogger(__name__)


def build_global_headers_message() -> dict[str, Any]:
    """Build a message with headers applied to the whole email."""
    logger.info("Building global custom-header example message")
    return {
        "from": {"email": "sender@example.com"},
        "to": [{"email": "recipient@example.net"}],
        "subject": "Custom Header Example",
        "text": "This email includes custom headers.",
        "headers": {
            "List-Unsubscribe": "<mailto:unsubscribe@example.com>",
            "X-Campaign-ID": "newsletter-123",
        },
    }


def build_personalized_headers_message() -> dict[str, Any]:
    """Build a message with recipient-specific custom headers."""
    logger.info("Building per-personalization custom-header example message")
    return {
        "from": {"email": "sender@example.com"},
        "subject": "Bananas Are On Sale",
        "personalizations": [
            {
                "to": [{"email": "banana-lover@example.net"}],
                "headers": {
                    "List-Unsubscribe": "<mailto:unsubscribe@bananas.example>",
                    "X-Custom-Header": "BananaFan123",
                },
            }
        ],
        "content": [
            {
                "type": "text/plain",
                "value": "This email includes custom headers.",
            }
        ],
    }


def send_with_custom_headers(client: mailchannels.Client) -> dict[str, Any]:
    """Send the global custom-header example as a dry run."""
    return client.emails.send(build_global_headers_message(), dry_run=True)


def main() -> None:
    """Run the custom-header example from environment configuration."""
    client = mailchannels.Client(api_key=os.environ["MAILCHANNELS_API_KEY"])
    print(send_with_custom_headers(client))


if __name__ == "__main__":
    main()
