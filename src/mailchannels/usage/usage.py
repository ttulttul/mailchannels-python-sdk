"""Usage resource implementation."""

from __future__ import annotations

import logging
from typing import Any, Generic, Literal, TypeVar, overload

from ..response import MailChannelsResponse
from .types import UsageStats

logger = logging.getLogger(__name__)
StrictResponses = TypeVar("StrictResponses", bound=bool)


class UsageResource(Generic[StrictResponses]):
    """Client-bound parent-account usage operations."""

    def __init__(self, client: Any) -> None:
        """Create a usage resource bound to a client."""
        self._client = client

    @overload
    def retrieve(self: UsageResource[Literal[True]]) -> UsageStats: ...

    @overload
    def retrieve(self: UsageResource[Literal[False]]) -> MailChannelsResponse: ...

    @overload
    def retrieve(self) -> UsageStats | MailChannelsResponse: ...

    def retrieve(self) -> UsageStats | MailChannelsResponse:
        """Retrieve parent-account usage for the current billing period."""
        logger.info("Retrieving MailChannels account usage")
        return self._client.request("GET", "/usage", response_model=UsageStats)

    @overload
    async def retrieve_async(self: UsageResource[Literal[True]]) -> UsageStats: ...

    @overload
    async def retrieve_async(
        self: UsageResource[Literal[False]],
    ) -> MailChannelsResponse: ...

    @overload
    async def retrieve_async(self) -> UsageStats | MailChannelsResponse: ...

    async def retrieve_async(self) -> UsageStats | MailChannelsResponse:
        """Retrieve parent-account usage using async HTTP."""
        logger.info("Retrieving MailChannels account usage using async HTTP")
        return await self._client.request_async(
            "GET",
            "/usage",
            response_model=UsageStats,
        )


class Usage:
    """Module-level parent-account usage operations."""

    @classmethod
    def retrieve(cls) -> UsageStats | MailChannelsResponse:
        """Retrieve parent-account usage for the current billing period."""
        from ..client import get_default_client

        return get_default_client().usage.retrieve()

    @classmethod
    async def retrieve_async(cls) -> UsageStats | MailChannelsResponse:
        """Retrieve parent-account usage using async HTTP."""
        from ..client import get_default_client

        return await get_default_client().usage.retrieve_async()
