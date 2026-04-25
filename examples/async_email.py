"""Queue email with the async MailChannels client."""

from __future__ import annotations

import asyncio
import logging
import os
from typing import Any

import mailchannels

logger = logging.getLogger(__name__)


async def queue_async_email(client: mailchannels.Client) -> dict[str, Any]:
    """Queue a message using the async MailChannels transport."""
    logger.info("Queueing example email with async client")
    return await client.emails.queue_async(
        {
            "from": {"email": "sender@example.com"},
            "to": [{"email": "recipient@example.net"}],
            "subject": "Async MailChannels example",
            "text": "This message was queued with the async SDK.",
        }
    )


async def main_async() -> None:
    """Run the async email example from environment configuration."""
    client = mailchannels.Client(api_key=os.environ["MAILCHANNELS_API_KEY"])
    result = await queue_async_email(client)
    print(result)


def main() -> None:
    """Run the async example with asyncio."""
    asyncio.run(main_async())


if __name__ == "__main__":
    main()
