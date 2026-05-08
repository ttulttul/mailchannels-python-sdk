"""Domain configuration check resource implementation."""

from __future__ import annotations

import logging
from typing import Any, Generic, Literal, TypeVar, overload

from pydantic import ValidationError

from ..exceptions import MailChannelsError
from ..response import MailChannelsResponse
from .types import CheckDomainParams, CheckDomainResult, DkimSetting

logger = logging.getLogger(__name__)
StrictResponses = TypeVar("StrictResponses", bound=bool)


class DomainChecksResource(Generic[StrictResponses]):
    """Client-bound domain configuration check operations."""

    def __init__(self, client: Any) -> None:
        """Create a domain checks resource bound to a client."""
        self._client = client

    @overload
    def check(
        self: DomainChecksResource[Literal[True]],
        domain: str,
        *,
        sender_id: str | None = None,
        dkim_settings: list[DkimSetting | dict[str, str]] | None = None,
    ) -> CheckDomainResult: ...

    @overload
    def check(
        self: DomainChecksResource[Literal[False]],
        domain: str,
        *,
        sender_id: str | None = None,
        dkim_settings: list[DkimSetting | dict[str, str]] | None = None,
    ) -> MailChannelsResponse: ...

    @overload
    def check(
        self,
        domain: str,
        *,
        sender_id: str | None = None,
        dkim_settings: list[DkimSetting | dict[str, str]] | None = None,
    ) -> CheckDomainResult | MailChannelsResponse: ...

    def check(
        self,
        domain: str,
        *,
        sender_id: str | None = None,
        dkim_settings: list[DkimSetting | dict[str, str]] | None = None,
    ) -> CheckDomainResult | MailChannelsResponse:
        """Check DKIM, SPF, sender-domain DNS, and Domain Lockdown status."""
        payload = _check_domain_payload(
            domain,
            sender_id=sender_id,
            dkim_settings=dkim_settings,
        )
        logger.info("Checking MailChannels domain configuration domain=%s", domain)
        return self._client.request(
            "POST",
            "/check-domain",
            json=payload,
            response_model=CheckDomainResult,
        )

    @overload
    async def check_async(
        self: DomainChecksResource[Literal[True]],
        domain: str,
        *,
        sender_id: str | None = None,
        dkim_settings: list[DkimSetting | dict[str, str]] | None = None,
    ) -> CheckDomainResult: ...

    @overload
    async def check_async(
        self: DomainChecksResource[Literal[False]],
        domain: str,
        *,
        sender_id: str | None = None,
        dkim_settings: list[DkimSetting | dict[str, str]] | None = None,
    ) -> MailChannelsResponse: ...

    @overload
    async def check_async(
        self,
        domain: str,
        *,
        sender_id: str | None = None,
        dkim_settings: list[DkimSetting | dict[str, str]] | None = None,
    ) -> CheckDomainResult | MailChannelsResponse: ...

    async def check_async(
        self,
        domain: str,
        *,
        sender_id: str | None = None,
        dkim_settings: list[DkimSetting | dict[str, str]] | None = None,
    ) -> CheckDomainResult | MailChannelsResponse:
        """Check domain configuration status using async HTTP."""
        payload = _check_domain_payload(
            domain,
            sender_id=sender_id,
            dkim_settings=dkim_settings,
        )
        logger.info(
            "Checking MailChannels domain configuration using async HTTP domain=%s",
            domain,
        )
        return await self._client.request_async(
            "POST",
            "/check-domain",
            json=payload,
            response_model=CheckDomainResult,
        )


class DomainChecks:
    """Module-level domain configuration check operations."""

    @classmethod
    def check(
        cls,
        domain: str,
        *,
        sender_id: str | None = None,
        dkim_settings: list[DkimSetting | dict[str, str]] | None = None,
    ) -> CheckDomainResult | MailChannelsResponse:
        """Check DKIM, SPF, sender-domain DNS, and Domain Lockdown status."""
        from ..client import get_default_client

        return get_default_client().domain_checks.check(
            domain,
            sender_id=sender_id,
            dkim_settings=dkim_settings,
        )

    @classmethod
    async def check_async(
        cls,
        domain: str,
        *,
        sender_id: str | None = None,
        dkim_settings: list[DkimSetting | dict[str, str]] | None = None,
    ) -> CheckDomainResult | MailChannelsResponse:
        """Check domain configuration status using async HTTP."""
        from ..client import get_default_client

        return await get_default_client().domain_checks.check_async(
            domain,
            sender_id=sender_id,
            dkim_settings=dkim_settings,
        )


CheckDomainResource = DomainChecksResource
CheckDomain = DomainChecks


def _check_domain_payload(
    domain: str,
    *,
    sender_id: str | None = None,
    dkim_settings: list[DkimSetting | dict[str, str]] | None = None,
) -> dict[str, Any]:
    """Build and validate a `/check-domain` request payload."""
    try:
        params = CheckDomainParams(
            domain=domain,
            sender_id=sender_id,
            dkim_settings=dkim_settings,
        )
    except ValidationError as error:
        logger.error("Invalid MailChannels domain check parameters: %s", error)
        raise MailChannelsError(
            "Invalid domain check parameters.",
            code="InvalidDomainCheckParameters",
        ) from error
    return params.model_dump(exclude_none=True)
