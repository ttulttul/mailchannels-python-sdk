"""Usage resource implementation."""

from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger(__name__)


class UsageResource:
    """Client-bound parent-account usage operations."""

    def __init__(self, client: Any) -> None:
        """Create a usage resource bound to a client."""
        self._client = client

    def retrieve(self) -> dict[str, Any]:
        """Retrieve parent-account usage for the current billing period."""
        logger.info("Retrieving MailChannels account usage")
        return self._client.request("GET", "/usage")

    async def retrieve_async(self) -> dict[str, Any]:
        """Retrieve parent-account usage using async HTTP."""
        logger.info("Retrieving MailChannels account usage using async HTTP")
        return await self._client.request_async("GET", "/usage")


class Usage:
    """Module-level parent-account usage operations."""

    @classmethod
    def retrieve(cls) -> dict[str, Any]:
        """Retrieve parent-account usage for the current billing period."""
        from ..client import get_default_client

        return get_default_client().usage.retrieve()

    @classmethod
    async def retrieve_async(cls) -> dict[str, Any]:
        """Retrieve parent-account usage using async HTTP."""
        from ..client import get_default_client

        return await get_default_client().usage.retrieve_async()
