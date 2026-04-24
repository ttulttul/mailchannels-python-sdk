"""Send an email with the MailChannels Python SDK."""

from __future__ import annotations

import os

import mailchannels


def main() -> None:
    """Send a simple plain text email."""
    mailchannels.api_key = os.environ["MAILCHANNELS_API_KEY"]
    result = mailchannels.Emails.send(
        {
            "from": {"email": "sender@example.com", "name": "Priya Patel"},
            "to": [{"email": "recipient@example.net", "name": "Sakura Tanaka"}],
            "subject": "Testing Email API",
            "text": "Hi Sakura. This is just a test from Priya.",
        }
    )
    print(result)


if __name__ == "__main__":
    main()
