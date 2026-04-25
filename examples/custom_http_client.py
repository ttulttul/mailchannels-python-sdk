"""Use a custom HTTP transport with the MailChannels SDK."""

from __future__ import annotations

import logging
import os
from typing import Any

import mailchannels

logger = logging.getLogger(__name__)


class InstrumentedHTTPClient:
    """Custom synchronous transport that wraps another SDK transport."""

    def __init__(self, delegate: mailchannels.SyncHTTPClient | None = None) -> None:
        """Create an instrumented transport."""
        self.delegate = delegate or mailchannels.RequestsClient()
        self.calls: list[dict[str, str]] = []

    def request(
        self,
        method: str,
        url: str,
        *,
        headers: dict[str, str],
        json: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
    ) -> mailchannels.SDKResponse:
        """Record request metadata before delegating to the real transport."""
        logger.info("Custom transport request method=%s url=%s", method, url)
        self.calls.append({"method": method, "url": url})
        return self.delegate.request(
            method,
            url,
            headers=headers,
            json=json,
            params=params,
        )


def build_client(api_key: str) -> mailchannels.Client:
    """Build a MailChannels client using the custom transport."""
    return mailchannels.Client(
        api_key=api_key,
        http_client=InstrumentedHTTPClient(),
    )


def main() -> None:
    """Run the custom HTTP client example from environment configuration."""
    client = build_client(os.environ["MAILCHANNELS_API_KEY"])
    print(client.usage.retrieve())


if __name__ == "__main__":
    main()
