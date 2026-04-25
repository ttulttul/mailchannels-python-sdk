"""Suppression list resource implementation."""

from __future__ import annotations

import logging
from builtins import list as list_type
from typing import Any

from ..query import compact_query, pagination_query
from .types import (
    SuppressionDeleteSource,
    SuppressionEntryParams,
    SuppressionSource,
)

logger = logging.getLogger(__name__)


class SuppressionsResource:
    """Client-bound suppression list operations."""

    def __init__(self, client: Any) -> None:
        """Create a suppression resource bound to a client."""
        self._client = client

    def list(
        self,
        *,
        recipient: str | None = None,
        source: SuppressionSource | None = None,
        created_before: str | None = None,
        created_after: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> dict[str, Any]:
        """Retrieve suppression entries."""
        logger.info("Listing MailChannels suppression entries")
        return self._client.request(
            "GET",
            "/suppression-list",
            params=pagination_query(
                limit=limit,
                offset=offset,
                recipient=recipient,
                source=source,
                created_before=created_before,
                created_after=created_after,
            )
            or None,
        )

    async def list_async(
        self,
        *,
        recipient: str | None = None,
        source: SuppressionSource | None = None,
        created_before: str | None = None,
        created_after: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> dict[str, Any]:
        """Retrieve suppression entries using async HTTP."""
        logger.info("Listing MailChannels suppression entries using async HTTP")
        return await self._client.request_async(
            "GET",
            "/suppression-list",
            params=pagination_query(
                limit=limit,
                offset=offset,
                recipient=recipient,
                source=source,
                created_before=created_before,
                created_after=created_after,
            )
            or None,
        )

    def create(
        self,
        entries: list_type[SuppressionEntryParams],
        *,
        add_to_sub_accounts: bool | None = None,
    ) -> dict[str, Any]:
        """Create suppression entries."""
        logger.info("Creating MailChannels suppression entries count=%s", len(entries))
        return self._client.request(
            "POST",
            "/suppression-list",
            json=_compact(
                {
                    "suppression_entries": entries,
                    "add_to_sub_accounts": add_to_sub_accounts,
                }
            ),
        )

    async def create_async(
        self,
        entries: list_type[SuppressionEntryParams],
        *,
        add_to_sub_accounts: bool | None = None,
    ) -> dict[str, Any]:
        """Create suppression entries using async HTTP."""
        logger.info(
            "Creating MailChannels suppression entries using async HTTP count=%s",
            len(entries),
        )
        return await self._client.request_async(
            "POST",
            "/suppression-list",
            json=_compact(
                {
                    "suppression_entries": entries,
                    "add_to_sub_accounts": add_to_sub_accounts,
                }
            ),
        )

    def delete(
        self,
        recipient: str,
        *,
        source: SuppressionDeleteSource | None = None,
    ) -> dict[str, Any]:
        """Delete suppression entries for a recipient."""
        logger.warning("Deleting MailChannels suppression recipient=%s", recipient)
        return self._client.request(
            "DELETE",
            f"/suppression-list/recipients/{recipient}",
            params=compact_query({"source": source}) or None,
        )

    async def delete_async(
        self,
        recipient: str,
        *,
        source: SuppressionDeleteSource | None = None,
    ) -> dict[str, Any]:
        """Delete suppression entries for a recipient using async HTTP."""
        logger.warning(
            "Deleting MailChannels suppression using async HTTP recipient=%s",
            recipient,
        )
        return await self._client.request_async(
            "DELETE",
            f"/suppression-list/recipients/{recipient}",
            params=compact_query({"source": source}) or None,
        )


class Suppressions:
    """Module-level suppression list operations."""

    @classmethod
    def list(cls, **kwargs: Any) -> dict[str, Any]:
        """Retrieve suppression entries."""
        from ..client import get_default_client

        return get_default_client().suppressions.list(**kwargs)

    @classmethod
    async def list_async(cls, **kwargs: Any) -> dict[str, Any]:
        """Retrieve suppression entries using async HTTP."""
        from ..client import get_default_client

        return await get_default_client().suppressions.list_async(**kwargs)

    @classmethod
    def create(
        cls,
        entries: list_type[SuppressionEntryParams],
        *,
        add_to_sub_accounts: bool | None = None,
    ) -> dict[str, Any]:
        """Create suppression entries."""
        from ..client import get_default_client

        return get_default_client().suppressions.create(
            entries,
            add_to_sub_accounts=add_to_sub_accounts,
        )

    @classmethod
    async def create_async(
        cls,
        entries: list_type[SuppressionEntryParams],
        *,
        add_to_sub_accounts: bool | None = None,
    ) -> dict[str, Any]:
        """Create suppression entries using async HTTP."""
        from ..client import get_default_client

        return await get_default_client().suppressions.create_async(
            entries,
            add_to_sub_accounts=add_to_sub_accounts,
        )

    @classmethod
    def delete(
        cls,
        recipient: str,
        *,
        source: SuppressionDeleteSource | None = None,
    ) -> dict[str, Any]:
        """Delete suppression entries for a recipient."""
        from ..client import get_default_client

        return get_default_client().suppressions.delete(recipient, source=source)

    @classmethod
    async def delete_async(
        cls,
        recipient: str,
        *,
        source: SuppressionDeleteSource | None = None,
    ) -> dict[str, Any]:
        """Delete suppression entries for a recipient using async HTTP."""
        from ..client import get_default_client

        return await get_default_client().suppressions.delete_async(
            recipient,
            source=source,
        )


def _compact(values: dict[str, Any]) -> dict[str, Any]:
    """Remove unset values."""
    return {key: value for key, value in values.items() if value is not None}
