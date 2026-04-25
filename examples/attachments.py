"""Send messages with MailChannels attachment helpers."""

from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import Any

import mailchannels

logger = logging.getLogger(__name__)


def build_attachment_message(path: str | Path) -> dict[str, Any]:
    """Build an email payload with a local file attachment."""
    logger.info("Building attachment example message path=%s", path)
    return {
        "from": {"email": "sender@example.com"},
        "to": [{"email": "recipient@example.net"}],
        "subject": "Attachment example",
        "text": "The requested file is attached.",
        "attachments": [mailchannels.Attachment.from_file(path)],
    }


def build_inline_image_message(path: str | Path) -> dict[str, Any]:
    """Build an email payload with an inline image attachment."""
    logger.info("Building inline image example message path=%s", path)
    return {
        "from": {"email": "sender@example.com"},
        "to": [{"email": "recipient@example.net"}],
        "subject": "Inline image example",
        "html": "<img src='cid:example-image' alt='Example image'>",
        "attachments": [
            mailchannels.Attachment.inline_file(path, content_id="example-image")
        ],
    }


def queue_attachment(client: mailchannels.Client, path: str | Path) -> dict[str, Any]:
    """Queue an email with a local file attachment."""
    return client.emails.queue(build_attachment_message(path))


def main() -> None:
    """Run the attachment example from environment configuration."""
    client = mailchannels.Client(api_key=os.environ["MAILCHANNELS_API_KEY"])
    result = queue_attachment(client, os.environ["ATTACHMENT_PATH"])
    print(result)


if __name__ == "__main__":
    main()
