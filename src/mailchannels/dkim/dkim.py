"""DKIM resource implementation."""

from __future__ import annotations

import logging
from typing import Any, Generic, Literal, TypeVar, overload

from ..query import pagination_query
from ..response import MailChannelsResponse
from .types import (
    DkimAlgorithm,
    DkimKeyInfo,
    DkimKeyList,
    DkimKeyStatus,
    DkimRotateResponse,
    DkimUpdateStatus,
)

logger = logging.getLogger(__name__)
StrictResponses = TypeVar("StrictResponses", bound=bool)


class DkimResource(Generic[StrictResponses]):
    """Client-bound DKIM key management operations."""

    def __init__(self, client: Any) -> None:
        """Create a DKIM resource bound to a client."""
        self._client = client

    @overload
    def create(
        self: DkimResource[Literal[True]],
        domain: str,
        *,
        selector: str,
        algorithm: DkimAlgorithm | None = None,
        key_length: int | None = None,
    ) -> DkimKeyInfo: ...

    @overload
    def create(
        self: DkimResource[Literal[False]],
        domain: str,
        *,
        selector: str,
        algorithm: DkimAlgorithm | None = None,
        key_length: int | None = None,
    ) -> MailChannelsResponse: ...

    @overload
    def create(
        self,
        domain: str,
        *,
        selector: str,
        algorithm: DkimAlgorithm | None = None,
        key_length: int | None = None,
    ) -> DkimKeyInfo | MailChannelsResponse: ...

    def create(
        self,
        domain: str,
        *,
        selector: str,
        algorithm: DkimAlgorithm | None = None,
        key_length: int | None = None,
    ) -> DkimKeyInfo | MailChannelsResponse:
        """Create a MailChannels-hosted DKIM key pair for a domain."""
        logger.info(
            "Creating MailChannels DKIM key pair domain=%s selector=%s",
            domain,
            selector,
        )
        payload = _compact(
            {
                "selector": selector,
                "algorithm": algorithm,
                "key_length": key_length,
            }
        )
        return self._client.request(
            "POST",
            f"/domains/{domain}/dkim-keys",
            json=payload,
            response_model=DkimKeyInfo,
        )

    @overload
    async def create_async(
        self: DkimResource[Literal[True]],
        domain: str,
        *,
        selector: str,
        algorithm: DkimAlgorithm | None = None,
        key_length: int | None = None,
    ) -> DkimKeyInfo: ...

    @overload
    async def create_async(
        self: DkimResource[Literal[False]],
        domain: str,
        *,
        selector: str,
        algorithm: DkimAlgorithm | None = None,
        key_length: int | None = None,
    ) -> MailChannelsResponse: ...

    @overload
    async def create_async(
        self,
        domain: str,
        *,
        selector: str,
        algorithm: DkimAlgorithm | None = None,
        key_length: int | None = None,
    ) -> DkimKeyInfo | MailChannelsResponse: ...

    async def create_async(
        self,
        domain: str,
        *,
        selector: str,
        algorithm: DkimAlgorithm | None = None,
        key_length: int | None = None,
    ) -> DkimKeyInfo | MailChannelsResponse:
        """Create a MailChannels-hosted DKIM key pair using async HTTP."""
        logger.info(
            "Creating MailChannels DKIM key pair using async HTTP domain=%s "
            "selector=%s",
            domain,
            selector,
        )
        payload = _compact(
            {
                "selector": selector,
                "algorithm": algorithm,
                "key_length": key_length,
            }
        )
        return await self._client.request_async(
            "POST",
            f"/domains/{domain}/dkim-keys",
            json=payload,
            response_model=DkimKeyInfo,
        )

    @overload
    def list(
        self: DkimResource[Literal[True]],
        domain: str,
        *,
        selector: str | None = None,
        status: DkimKeyStatus | None = None,
        offset: int | None = None,
        limit: int | None = None,
        include_dns_record: bool | None = None,
    ) -> DkimKeyList: ...

    @overload
    def list(
        self: DkimResource[Literal[False]],
        domain: str,
        *,
        selector: str | None = None,
        status: DkimKeyStatus | None = None,
        offset: int | None = None,
        limit: int | None = None,
        include_dns_record: bool | None = None,
    ) -> MailChannelsResponse: ...

    @overload
    def list(
        self,
        domain: str,
        *,
        selector: str | None = None,
        status: DkimKeyStatus | None = None,
        offset: int | None = None,
        limit: int | None = None,
        include_dns_record: bool | None = None,
    ) -> DkimKeyList | MailChannelsResponse: ...

    def list(
        self,
        domain: str,
        *,
        selector: str | None = None,
        status: DkimKeyStatus | None = None,
        offset: int | None = None,
        limit: int | None = None,
        include_dns_record: bool | None = None,
    ) -> DkimKeyList | MailChannelsResponse:
        """Retrieve MailChannels-hosted DKIM keys for a domain."""
        logger.info("Listing MailChannels DKIM keys domain=%s", domain)
        params = pagination_query(
            limit=limit,
            offset=offset,
            selector=selector,
            status=status,
            include_dns_record=include_dns_record,
        )
        return self._client.request(
            "GET",
            f"/domains/{domain}/dkim-keys",
            params=params or None,
            response_model=DkimKeyList,
        )

    @overload
    async def list_async(
        self: DkimResource[Literal[True]],
        domain: str,
        *,
        selector: str | None = None,
        status: DkimKeyStatus | None = None,
        offset: int | None = None,
        limit: int | None = None,
        include_dns_record: bool | None = None,
    ) -> DkimKeyList: ...

    @overload
    async def list_async(
        self: DkimResource[Literal[False]],
        domain: str,
        *,
        selector: str | None = None,
        status: DkimKeyStatus | None = None,
        offset: int | None = None,
        limit: int | None = None,
        include_dns_record: bool | None = None,
    ) -> MailChannelsResponse: ...

    @overload
    async def list_async(
        self,
        domain: str,
        *,
        selector: str | None = None,
        status: DkimKeyStatus | None = None,
        offset: int | None = None,
        limit: int | None = None,
        include_dns_record: bool | None = None,
    ) -> DkimKeyList | MailChannelsResponse: ...

    async def list_async(
        self,
        domain: str,
        *,
        selector: str | None = None,
        status: DkimKeyStatus | None = None,
        offset: int | None = None,
        limit: int | None = None,
        include_dns_record: bool | None = None,
    ) -> DkimKeyList | MailChannelsResponse:
        """Retrieve MailChannels-hosted DKIM keys using async HTTP."""
        logger.info("Listing MailChannels DKIM keys using async HTTP domain=%s", domain)
        params = pagination_query(
            limit=limit,
            offset=offset,
            selector=selector,
            status=status,
            include_dns_record=include_dns_record,
        )
        return await self._client.request_async(
            "GET",
            f"/domains/{domain}/dkim-keys",
            params=params or None,
            response_model=DkimKeyList,
        )

    def update_status(
        self,
        domain: str,
        selector: str,
        *,
        status: DkimUpdateStatus,
    ) -> dict[str, Any]:
        """Update the status of a MailChannels-hosted DKIM key pair."""
        logger.warning(
            "Updating MailChannels DKIM key status domain=%s selector=%s status=%s",
            domain,
            selector,
            status,
        )
        return self._client.request(
            "PATCH",
            f"/domains/{domain}/dkim-keys/{selector}",
            json={"status": status},
        )

    async def update_status_async(
        self,
        domain: str,
        selector: str,
        *,
        status: DkimUpdateStatus,
    ) -> dict[str, Any]:
        """Update the status of a MailChannels-hosted DKIM key pair using async HTTP."""
        logger.warning(
            "Updating MailChannels DKIM key status using async HTTP domain=%s "
            "selector=%s status=%s",
            domain,
            selector,
            status,
        )
        return await self._client.request_async(
            "PATCH",
            f"/domains/{domain}/dkim-keys/{selector}",
            json={"status": status},
        )

    @overload
    def rotate(
        self: DkimResource[Literal[True]],
        domain: str,
        selector: str,
        *,
        new_selector: str,
    ) -> DkimRotateResponse: ...

    @overload
    def rotate(
        self: DkimResource[Literal[False]],
        domain: str,
        selector: str,
        *,
        new_selector: str,
    ) -> MailChannelsResponse: ...

    @overload
    def rotate(
        self,
        domain: str,
        selector: str,
        *,
        new_selector: str,
    ) -> DkimRotateResponse | MailChannelsResponse: ...

    def rotate(
        self,
        domain: str,
        selector: str,
        *,
        new_selector: str,
    ) -> DkimRotateResponse | MailChannelsResponse:
        """Rotate a MailChannels-hosted DKIM key pair."""
        logger.warning(
            "Rotating MailChannels DKIM key domain=%s selector=%s new_selector=%s",
            domain,
            selector,
            new_selector,
        )
        return self._client.request(
            "POST",
            f"/domains/{domain}/dkim-keys/{selector}/rotate",
            json={"new_key": {"selector": new_selector}},
            response_model=DkimRotateResponse,
        )

    @overload
    async def rotate_async(
        self: DkimResource[Literal[True]],
        domain: str,
        selector: str,
        *,
        new_selector: str,
    ) -> DkimRotateResponse: ...

    @overload
    async def rotate_async(
        self: DkimResource[Literal[False]],
        domain: str,
        selector: str,
        *,
        new_selector: str,
    ) -> MailChannelsResponse: ...

    @overload
    async def rotate_async(
        self,
        domain: str,
        selector: str,
        *,
        new_selector: str,
    ) -> DkimRotateResponse | MailChannelsResponse: ...

    async def rotate_async(
        self,
        domain: str,
        selector: str,
        *,
        new_selector: str,
    ) -> DkimRotateResponse | MailChannelsResponse:
        """Rotate a MailChannels-hosted DKIM key pair using async HTTP."""
        logger.warning(
            "Rotating MailChannels DKIM key using async HTTP domain=%s "
            "selector=%s new_selector=%s",
            domain,
            selector,
            new_selector,
        )
        return await self._client.request_async(
            "POST",
            f"/domains/{domain}/dkim-keys/{selector}/rotate",
            json={"new_key": {"selector": new_selector}},
            response_model=DkimRotateResponse,
        )


class Dkim:
    """Module-level DKIM key management using global SDK configuration."""

    @classmethod
    def create(
        cls,
        domain: str,
        *,
        selector: str,
        algorithm: DkimAlgorithm | None = None,
        key_length: int | None = None,
    ) -> DkimKeyInfo | MailChannelsResponse:
        """Create a MailChannels-hosted DKIM key pair for a domain."""
        from ..client import get_default_client

        return get_default_client().dkim.create(
            domain,
            selector=selector,
            algorithm=algorithm,
            key_length=key_length,
        )

    @classmethod
    async def create_async(
        cls,
        domain: str,
        *,
        selector: str,
        algorithm: DkimAlgorithm | None = None,
        key_length: int | None = None,
    ) -> DkimKeyInfo | MailChannelsResponse:
        """Create a MailChannels-hosted DKIM key pair using async HTTP."""
        from ..client import get_default_client

        return await get_default_client().dkim.create_async(
            domain,
            selector=selector,
            algorithm=algorithm,
            key_length=key_length,
        )

    @classmethod
    def list(
        cls,
        domain: str,
        *,
        selector: str | None = None,
        status: DkimKeyStatus | None = None,
        offset: int | None = None,
        limit: int | None = None,
        include_dns_record: bool | None = None,
    ) -> DkimKeyList | MailChannelsResponse:
        """Retrieve MailChannels-hosted DKIM keys for a domain."""
        from ..client import get_default_client

        return get_default_client().dkim.list(
            domain,
            selector=selector,
            status=status,
            offset=offset,
            limit=limit,
            include_dns_record=include_dns_record,
        )

    @classmethod
    async def list_async(
        cls,
        domain: str,
        *,
        selector: str | None = None,
        status: DkimKeyStatus | None = None,
        offset: int | None = None,
        limit: int | None = None,
        include_dns_record: bool | None = None,
    ) -> DkimKeyList | MailChannelsResponse:
        """Retrieve MailChannels-hosted DKIM keys using async HTTP."""
        from ..client import get_default_client

        return await get_default_client().dkim.list_async(
            domain,
            selector=selector,
            status=status,
            offset=offset,
            limit=limit,
            include_dns_record=include_dns_record,
        )

    @classmethod
    def update_status(
        cls,
        domain: str,
        selector: str,
        *,
        status: DkimUpdateStatus,
    ) -> dict[str, Any]:
        """Update the status of a MailChannels-hosted DKIM key pair."""
        from ..client import get_default_client

        return get_default_client().dkim.update_status(
            domain,
            selector,
            status=status,
        )

    @classmethod
    async def update_status_async(
        cls,
        domain: str,
        selector: str,
        *,
        status: DkimUpdateStatus,
    ) -> dict[str, Any]:
        """Update the status of a MailChannels-hosted DKIM key pair using async HTTP."""
        from ..client import get_default_client

        return await get_default_client().dkim.update_status_async(
            domain,
            selector,
            status=status,
        )

    @classmethod
    def rotate(
        cls,
        domain: str,
        selector: str,
        *,
        new_selector: str,
    ) -> DkimRotateResponse | MailChannelsResponse:
        """Rotate a MailChannels-hosted DKIM key pair."""
        from ..client import get_default_client

        return get_default_client().dkim.rotate(
            domain,
            selector,
            new_selector=new_selector,
        )

    @classmethod
    async def rotate_async(
        cls,
        domain: str,
        selector: str,
        *,
        new_selector: str,
    ) -> DkimRotateResponse | MailChannelsResponse:
        """Rotate a MailChannels-hosted DKIM key pair using async HTTP."""
        from ..client import get_default_client

        return await get_default_client().dkim.rotate_async(
            domain,
            selector,
            new_selector=new_selector,
        )


def _compact(values: dict[str, Any]) -> dict[str, Any]:
    """Remove unset request values."""
    return {key: value for key, value in values.items() if value is not None}
