"""Queue an email with the MailChannels /send-async endpoint."""

from __future__ import annotations

import os

import mailchannels


def main() -> None:
    """Queue a simple email for asynchronous MailChannels processing."""
    mailchannels.api_key = os.environ["MAILCHANNELS_API_KEY"]
    result = mailchannels.Emails.queue(
        {
            "from": {"email": "sender@example.com"},
            "to": "recipient@example.net",
            "subject": "Queued message",
            "html": "<strong>Hello from MailChannels</strong>",
        }
    )
    print(result)


if __name__ == "__main__":
    main()
