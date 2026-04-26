"""Send MailChannels mustache template messages."""

from __future__ import annotations

import logging
import os
from typing import Any

import mailchannels

logger = logging.getLogger(__name__)


def build_template_message() -> dict[str, Any]:
    """Build a mustache template email with recipient-specific data."""
    logger.info("Building template email example message")
    return {
        "from": {"email": "sender@example.com"},
        "personalizations": [
            {
                "to": [{"email": "jane@example.net"}],
                "dynamic_template_data": {"name": "Jane Doe"},
            },
            {
                "to": [{"email": "john@example.net"}],
                "dynamic_template_data": {"name": "John Smith"},
            },
        ],
        "subject": "Template example",
        "content": [
            {
                "type": "text/plain",
                "value": "Hello {{name}}",
                "template_type": "mustache",
            }
        ],
    }


def preview_template(client: mailchannels.Client) -> dict[str, Any]:
    """Dry-run a template email without delivering it."""
    return client.emails.send(build_template_message(), dry_run=True)


def main() -> None:
    """Run the template example from environment configuration."""
    client = mailchannels.Client(api_key=os.environ["MAILCHANNELS_API_KEY"])
    print(preview_template(client))


if __name__ == "__main__":
    main()
