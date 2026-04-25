"""Handle MailChannels SDK exceptions with structured metadata."""

from __future__ import annotations

import logging
import os
from typing import Any

import mailchannels

logger = logging.getLogger(__name__)


def queue_with_error_handling(
    client: mailchannels.Client,
    message: dict[str, Any],
) -> dict[str, Any] | None:
    """Queue an email and log structured error metadata when it fails."""
    try:
        return client.emails.queue(message)
    except mailchannels.PayloadTooLargeError as error:
        logger.error("Message is too large metadata=%s", error.to_dict())
    except mailchannels.ForbiddenError as error:
        logger.error("MailChannels permission error metadata=%s", error.to_dict())
    except mailchannels.MailChannelsError as error:
        logger.error("MailChannels API error metadata=%s", error.to_dict())
    return None


def main() -> None:
    """Run the error-handling example from environment configuration."""
    client = mailchannels.Client(api_key=os.environ["MAILCHANNELS_API_KEY"])
    result = queue_with_error_handling(
        client,
        {
            "from": {"email": "sender@example.com"},
            "to": "recipient@example.net",
            "subject": "Error handling example",
            "text": "This message demonstrates structured error handling.",
        },
    )
    print(result)


if __name__ == "__main__":
    main()
