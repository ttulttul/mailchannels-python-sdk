"""Sub-account resource implementation."""

from __future__ import annotations

import logging
from typing import Any, Generic, Literal, TypeVar, overload

from ..query import pagination_query
from ..response import MailChannelsResponse
from .types import (
    ApiKey,
    SmtpPassword,
    SubAccount,
    SubAccountLimit,
    UsageStats,
    compact_payload,
    limit_payload,
)

logger = logging.getLogger(__name__)
StrictResponses = TypeVar("StrictResponses", bound=bool)


class SubAccountApiKeysResource(Generic[StrictResponses]):
    """Client-bound sub-account API key operations."""

    def __init__(self, client: Any) -> None:
        """Create a sub-account API key resource bound to a client."""
        self._client = client

    @overload
    def create(
        self: SubAccountApiKeysResource[Literal[True]],
        handle: str,
    ) -> ApiKey: ...

    @overload
    def create(
        self: SubAccountApiKeysResource[Literal[False]],
        handle: str,
    ) -> MailChannelsResponse: ...

    @overload
    def create(self, handle: str) -> ApiKey | MailChannelsResponse: ...

    def create(self, handle: str) -> ApiKey | MailChannelsResponse:
        """Create an API key for a sub-account."""
        logger.info("Creating MailChannels sub-account API key handle=%s", handle)
        return self._client.request(
            "POST",
            f"/sub-account/{handle}/api-key",
            response_model=ApiKey,
        )

    @overload
    async def create_async(
        self: SubAccountApiKeysResource[Literal[True]],
        handle: str,
    ) -> ApiKey: ...

    @overload
    async def create_async(
        self: SubAccountApiKeysResource[Literal[False]],
        handle: str,
    ) -> MailChannelsResponse: ...

    @overload
    async def create_async(self, handle: str) -> ApiKey | MailChannelsResponse: ...

    async def create_async(self, handle: str) -> ApiKey | MailChannelsResponse:
        """Create an API key for a sub-account using async HTTP."""
        logger.info(
            "Creating MailChannels sub-account API key using async HTTP handle=%s",
            handle,
        )
        return await self._client.request_async(
            "POST",
            f"/sub-account/{handle}/api-key",
            response_model=ApiKey,
        )

    def list(self, handle: str) -> dict[str, Any]:
        """Retrieve API keys for a sub-account."""
        logger.info("Listing MailChannels sub-account API keys handle=%s", handle)
        return self._client.request("GET", f"/sub-account/{handle}/api-key")

    async def list_async(self, handle: str) -> dict[str, Any]:
        """Retrieve API keys for a sub-account using async HTTP."""
        logger.info(
            "Listing MailChannels sub-account API keys using async HTTP handle=%s",
            handle,
        )
        return await self._client.request_async(
            "GET",
            f"/sub-account/{handle}/api-key",
        )

    def delete(self, handle: str, key_id: str) -> dict[str, Any]:
        """Delete an API key from a sub-account."""
        logger.info(
            "Deleting MailChannels sub-account API key handle=%s key_id=%s",
            handle,
            key_id,
        )
        return self._client.request("DELETE", f"/sub-account/{handle}/api-key/{key_id}")

    async def delete_async(self, handle: str, key_id: str) -> dict[str, Any]:
        """Delete an API key from a sub-account using async HTTP."""
        logger.info(
            "Deleting MailChannels sub-account API key using async HTTP handle=%s "
            "key_id=%s",
            handle,
            key_id,
        )
        return await self._client.request_async(
            "DELETE",
            f"/sub-account/{handle}/api-key/{key_id}",
        )


class SubAccountSmtpPasswordsResource(Generic[StrictResponses]):
    """Client-bound sub-account SMTP password operations."""

    def __init__(self, client: Any) -> None:
        """Create a sub-account SMTP password resource bound to a client."""
        self._client = client

    @overload
    def create(
        self: SubAccountSmtpPasswordsResource[Literal[True]],
        handle: str,
    ) -> SmtpPassword: ...

    @overload
    def create(
        self: SubAccountSmtpPasswordsResource[Literal[False]],
        handle: str,
    ) -> MailChannelsResponse: ...

    @overload
    def create(self, handle: str) -> SmtpPassword | MailChannelsResponse: ...

    def create(self, handle: str) -> SmtpPassword | MailChannelsResponse:
        """Create an SMTP password for a sub-account."""
        logger.info("Creating MailChannels sub-account SMTP password handle=%s", handle)
        return self._client.request(
            "POST",
            f"/sub-account/{handle}/smtp-password",
            response_model=SmtpPassword,
        )

    @overload
    async def create_async(
        self: SubAccountSmtpPasswordsResource[Literal[True]],
        handle: str,
    ) -> SmtpPassword: ...

    @overload
    async def create_async(
        self: SubAccountSmtpPasswordsResource[Literal[False]],
        handle: str,
    ) -> MailChannelsResponse: ...

    @overload
    async def create_async(
        self,
        handle: str,
    ) -> SmtpPassword | MailChannelsResponse: ...

    async def create_async(self, handle: str) -> SmtpPassword | MailChannelsResponse:
        """Create an SMTP password for a sub-account using async HTTP."""
        logger.info(
            "Creating MailChannels sub-account SMTP password using async HTTP "
            "handle=%s",
            handle,
        )
        return await self._client.request_async(
            "POST",
            f"/sub-account/{handle}/smtp-password",
            response_model=SmtpPassword,
        )

    def list(self, handle: str) -> dict[str, Any]:
        """Retrieve SMTP passwords for a sub-account."""
        logger.info("Listing MailChannels sub-account SMTP passwords handle=%s", handle)
        return self._client.request("GET", f"/sub-account/{handle}/smtp-password")

    async def list_async(self, handle: str) -> dict[str, Any]:
        """Retrieve SMTP passwords for a sub-account using async HTTP."""
        logger.info(
            "Listing MailChannels sub-account SMTP passwords using async HTTP "
            "handle=%s",
            handle,
        )
        return await self._client.request_async(
            "GET",
            f"/sub-account/{handle}/smtp-password",
        )

    def delete(self, handle: str, password_id: str) -> dict[str, Any]:
        """Delete an SMTP password from a sub-account."""
        logger.info(
            "Deleting MailChannels sub-account SMTP password handle=%s password_id=%s",
            handle,
            password_id,
        )
        return self._client.request(
            "DELETE",
            f"/sub-account/{handle}/smtp-password/{password_id}",
        )

    async def delete_async(self, handle: str, password_id: str) -> dict[str, Any]:
        """Delete an SMTP password from a sub-account using async HTTP."""
        logger.info(
            "Deleting MailChannels sub-account SMTP password using async HTTP "
            "handle=%s password_id=%s",
            handle,
            password_id,
        )
        return await self._client.request_async(
            "DELETE",
            f"/sub-account/{handle}/smtp-password/{password_id}",
        )


class SubAccountLimitsResource(Generic[StrictResponses]):
    """Client-bound sub-account sending limit operations."""

    def __init__(self, client: Any) -> None:
        """Create a sub-account limits resource bound to a client."""
        self._client = client

    @overload
    def set(
        self: SubAccountLimitsResource[Literal[True]],
        handle: str,
        *,
        sends: int | None = None,
        monthly_limit: int | None = None,
    ) -> SubAccountLimit: ...

    @overload
    def set(
        self: SubAccountLimitsResource[Literal[False]],
        handle: str,
        *,
        sends: int | None = None,
        monthly_limit: int | None = None,
    ) -> MailChannelsResponse: ...

    @overload
    def set(
        self,
        handle: str,
        *,
        sends: int | None = None,
        monthly_limit: int | None = None,
    ) -> SubAccountLimit | MailChannelsResponse: ...

    def set(
        self,
        handle: str,
        *,
        sends: int | None = None,
        monthly_limit: int | None = None,
    ) -> SubAccountLimit | MailChannelsResponse:
        """Set the monthly sending limit for a sub-account."""
        payload = limit_payload(sends=sends, monthly_limit=monthly_limit)
        logger.info(
            "Setting MailChannels sub-account limit handle=%s sends=%s",
            handle,
            payload["sends"],
        )
        return self._client.request(
            "PUT",
            f"/sub-account/{handle}/limit",
            json=payload,
            response_model=SubAccountLimit,
        )

    @overload
    async def set_async(
        self: SubAccountLimitsResource[Literal[True]],
        handle: str,
        *,
        sends: int | None = None,
        monthly_limit: int | None = None,
    ) -> SubAccountLimit: ...

    @overload
    async def set_async(
        self: SubAccountLimitsResource[Literal[False]],
        handle: str,
        *,
        sends: int | None = None,
        monthly_limit: int | None = None,
    ) -> MailChannelsResponse: ...

    @overload
    async def set_async(
        self,
        handle: str,
        *,
        sends: int | None = None,
        monthly_limit: int | None = None,
    ) -> SubAccountLimit | MailChannelsResponse: ...

    async def set_async(
        self,
        handle: str,
        *,
        sends: int | None = None,
        monthly_limit: int | None = None,
    ) -> SubAccountLimit | MailChannelsResponse:
        """Set the monthly sending limit for a sub-account using async HTTP."""
        payload = limit_payload(sends=sends, monthly_limit=monthly_limit)
        logger.info(
            "Setting MailChannels sub-account limit using async HTTP "
            "handle=%s sends=%s",
            handle,
            payload["sends"],
        )
        return await self._client.request_async(
            "PUT",
            f"/sub-account/{handle}/limit",
            json=payload,
            response_model=SubAccountLimit,
        )

    @overload
    def retrieve(
        self: SubAccountLimitsResource[Literal[True]],
        handle: str,
    ) -> SubAccountLimit: ...

    @overload
    def retrieve(
        self: SubAccountLimitsResource[Literal[False]],
        handle: str,
    ) -> MailChannelsResponse: ...

    @overload
    def retrieve(self, handle: str) -> SubAccountLimit | MailChannelsResponse: ...

    def retrieve(self, handle: str) -> SubAccountLimit | MailChannelsResponse:
        """Retrieve the sending limit for a sub-account."""
        logger.info("Retrieving MailChannels sub-account limit handle=%s", handle)
        return self._client.request(
            "GET",
            f"/sub-account/{handle}/limit",
            response_model=SubAccountLimit,
        )

    @overload
    async def retrieve_async(
        self: SubAccountLimitsResource[Literal[True]],
        handle: str,
    ) -> SubAccountLimit: ...

    @overload
    async def retrieve_async(
        self: SubAccountLimitsResource[Literal[False]],
        handle: str,
    ) -> MailChannelsResponse: ...

    @overload
    async def retrieve_async(
        self,
        handle: str,
    ) -> SubAccountLimit | MailChannelsResponse: ...

    async def retrieve_async(
        self,
        handle: str,
    ) -> SubAccountLimit | MailChannelsResponse:
        """Retrieve the sending limit for a sub-account using async HTTP."""
        logger.info(
            "Retrieving MailChannels sub-account limit using async HTTP handle=%s",
            handle,
        )
        return await self._client.request_async(
            "GET",
            f"/sub-account/{handle}/limit",
            response_model=SubAccountLimit,
        )

    def delete(self, handle: str) -> dict[str, Any]:
        """Delete the sending limit for a sub-account."""
        logger.info("Deleting MailChannels sub-account limit handle=%s", handle)
        return self._client.request("DELETE", f"/sub-account/{handle}/limit")

    async def delete_async(self, handle: str) -> dict[str, Any]:
        """Delete the sending limit for a sub-account using async HTTP."""
        logger.info(
            "Deleting MailChannels sub-account limit using async HTTP handle=%s",
            handle,
        )
        return await self._client.request_async(
            "DELETE",
            f"/sub-account/{handle}/limit",
        )


class SubAccountsResource(Generic[StrictResponses]):
    """Client-bound sub-account operations."""

    def __init__(self, client: Any) -> None:
        """Create a sub-account resource bound to a client."""
        self._client = client
        self.api_keys: SubAccountApiKeysResource[StrictResponses] = (
            SubAccountApiKeysResource(client)
        )
        self.smtp_passwords: SubAccountSmtpPasswordsResource[StrictResponses] = (
            SubAccountSmtpPasswordsResource(client)
        )
        self.limits: SubAccountLimitsResource[StrictResponses] = (
            SubAccountLimitsResource(client)
        )

    @overload
    def create(
        self: SubAccountsResource[Literal[True]],
        *,
        company_name: str | None = None,
        handle: str | None = None,
    ) -> SubAccount: ...

    @overload
    def create(
        self: SubAccountsResource[Literal[False]],
        *,
        company_name: str | None = None,
        handle: str | None = None,
    ) -> MailChannelsResponse: ...

    @overload
    def create(
        self,
        *,
        company_name: str | None = None,
        handle: str | None = None,
    ) -> SubAccount | MailChannelsResponse: ...

    def create(
        self,
        *,
        company_name: str | None = None,
        handle: str | None = None,
    ) -> SubAccount | MailChannelsResponse:
        """Create a sub-account under the parent account."""
        logger.info("Creating MailChannels sub-account handle=%s", handle)
        payload = compact_payload({"company_name": company_name, "handle": handle})
        return self._client.request(
            "POST",
            "/sub-account",
            json=payload,
            response_model=SubAccount,
        )

    @overload
    async def create_async(
        self: SubAccountsResource[Literal[True]],
        *,
        company_name: str | None = None,
        handle: str | None = None,
    ) -> SubAccount: ...

    @overload
    async def create_async(
        self: SubAccountsResource[Literal[False]],
        *,
        company_name: str | None = None,
        handle: str | None = None,
    ) -> MailChannelsResponse: ...

    @overload
    async def create_async(
        self,
        *,
        company_name: str | None = None,
        handle: str | None = None,
    ) -> SubAccount | MailChannelsResponse: ...

    async def create_async(
        self,
        *,
        company_name: str | None = None,
        handle: str | None = None,
    ) -> SubAccount | MailChannelsResponse:
        """Create a sub-account under the parent account using async HTTP."""
        logger.info(
            "Creating MailChannels sub-account using async HTTP handle=%s",
            handle,
        )
        payload = compact_payload({"company_name": company_name, "handle": handle})
        return await self._client.request_async(
            "POST",
            "/sub-account",
            json=payload,
            response_model=SubAccount,
        )

    def list(
        self,
        *,
        limit: int | None = None,
        offset: int | None = None,
    ) -> dict[str, Any]:
        """Retrieve sub-accounts for the parent account."""
        logger.info("Listing MailChannels sub-accounts")
        return self._client.request(
            "GET",
            "/sub-account",
            params=pagination_query(limit=limit, offset=offset) or None,
        )

    async def list_async(
        self,
        *,
        limit: int | None = None,
        offset: int | None = None,
    ) -> dict[str, Any]:
        """Retrieve sub-accounts for the parent account using async HTTP."""
        logger.info("Listing MailChannels sub-accounts using async HTTP")
        return await self._client.request_async(
            "GET",
            "/sub-account",
            params=pagination_query(limit=limit, offset=offset) or None,
        )

    @overload
    def retrieve_usage(
        self: SubAccountsResource[Literal[True]],
        handle: str,
    ) -> UsageStats: ...

    @overload
    def retrieve_usage(
        self: SubAccountsResource[Literal[False]],
        handle: str,
    ) -> MailChannelsResponse: ...

    @overload
    def retrieve_usage(self, handle: str) -> UsageStats | MailChannelsResponse: ...

    def retrieve_usage(self, handle: str) -> UsageStats | MailChannelsResponse:
        """Retrieve usage statistics for a sub-account."""
        logger.info("Retrieving MailChannels sub-account usage handle=%s", handle)
        return self._client.request(
            "GET",
            f"/sub-account/{handle}/usage",
            response_model=UsageStats,
        )

    @overload
    async def retrieve_usage_async(
        self: SubAccountsResource[Literal[True]],
        handle: str,
    ) -> UsageStats: ...

    @overload
    async def retrieve_usage_async(
        self: SubAccountsResource[Literal[False]],
        handle: str,
    ) -> MailChannelsResponse: ...

    @overload
    async def retrieve_usage_async(
        self,
        handle: str,
    ) -> UsageStats | MailChannelsResponse: ...

    async def retrieve_usage_async(
        self,
        handle: str,
    ) -> UsageStats | MailChannelsResponse:
        """Retrieve usage statistics for a sub-account using async HTTP."""
        logger.info(
            "Retrieving MailChannels sub-account usage using async HTTP handle=%s",
            handle,
        )
        return await self._client.request_async(
            "GET",
            f"/sub-account/{handle}/usage",
            response_model=UsageStats,
        )

    def suspend(self, handle: str) -> dict[str, Any]:
        """Suspend a sub-account."""
        logger.info("Suspending MailChannels sub-account handle=%s", handle)
        return self._client.request("POST", f"/sub-account/{handle}/suspend")

    async def suspend_async(self, handle: str) -> dict[str, Any]:
        """Suspend a sub-account using async HTTP."""
        logger.info(
            "Suspending MailChannels sub-account using async HTTP handle=%s",
            handle,
        )
        return await self._client.request_async(
            "POST",
            f"/sub-account/{handle}/suspend",
        )

    def activate(self, handle: str) -> dict[str, Any]:
        """Activate a suspended sub-account."""
        logger.info("Activating MailChannels sub-account handle=%s", handle)
        return self._client.request("POST", f"/sub-account/{handle}/activate")

    async def activate_async(self, handle: str) -> dict[str, Any]:
        """Activate a suspended sub-account using async HTTP."""
        logger.info(
            "Activating MailChannels sub-account using async HTTP handle=%s",
            handle,
        )
        return await self._client.request_async(
            "POST",
            f"/sub-account/{handle}/activate",
        )

    def delete(self, handle: str) -> dict[str, Any]:
        """Delete a sub-account."""
        logger.info("Deleting MailChannels sub-account handle=%s", handle)
        return self._client.request("DELETE", f"/sub-account/{handle}")

    async def delete_async(self, handle: str) -> dict[str, Any]:
        """Delete a sub-account using async HTTP."""
        logger.info(
            "Deleting MailChannels sub-account using async HTTP handle=%s",
            handle,
        )
        return await self._client.request_async("DELETE", f"/sub-account/{handle}")


class _ApiKeysProxy:
    """Module-level proxy for sub-account API key operations."""

    @classmethod
    def create(cls, handle: str) -> ApiKey | MailChannelsResponse:
        """Create an API key for a sub-account."""
        from ..client import get_default_client

        return get_default_client().sub_accounts.api_keys.create(handle)

    @classmethod
    async def create_async(cls, handle: str) -> ApiKey | MailChannelsResponse:
        """Create an API key for a sub-account using async HTTP."""
        from ..client import get_default_client

        return await get_default_client().sub_accounts.api_keys.create_async(handle)

    @classmethod
    def list(cls, handle: str) -> dict[str, Any]:
        """Retrieve API keys for a sub-account."""
        from ..client import get_default_client

        return get_default_client().sub_accounts.api_keys.list(handle)

    @classmethod
    async def list_async(cls, handle: str) -> dict[str, Any]:
        """Retrieve API keys for a sub-account using async HTTP."""
        from ..client import get_default_client

        return await get_default_client().sub_accounts.api_keys.list_async(handle)

    @classmethod
    def delete(cls, handle: str, key_id: str) -> dict[str, Any]:
        """Delete an API key from a sub-account."""
        from ..client import get_default_client

        return get_default_client().sub_accounts.api_keys.delete(handle, key_id)

    @classmethod
    async def delete_async(cls, handle: str, key_id: str) -> dict[str, Any]:
        """Delete an API key from a sub-account using async HTTP."""
        from ..client import get_default_client

        return await get_default_client().sub_accounts.api_keys.delete_async(
            handle,
            key_id,
        )


class _SmtpPasswordsProxy:
    """Module-level proxy for sub-account SMTP password operations."""

    @classmethod
    def create(cls, handle: str) -> SmtpPassword | MailChannelsResponse:
        """Create an SMTP password for a sub-account."""
        from ..client import get_default_client

        return get_default_client().sub_accounts.smtp_passwords.create(handle)

    @classmethod
    async def create_async(cls, handle: str) -> SmtpPassword | MailChannelsResponse:
        """Create an SMTP password for a sub-account using async HTTP."""
        from ..client import get_default_client

        return await get_default_client().sub_accounts.smtp_passwords.create_async(
            handle
        )

    @classmethod
    def list(cls, handle: str) -> dict[str, Any]:
        """Retrieve SMTP passwords for a sub-account."""
        from ..client import get_default_client

        return get_default_client().sub_accounts.smtp_passwords.list(handle)

    @classmethod
    async def list_async(cls, handle: str) -> dict[str, Any]:
        """Retrieve SMTP passwords for a sub-account using async HTTP."""
        from ..client import get_default_client

        return await get_default_client().sub_accounts.smtp_passwords.list_async(handle)

    @classmethod
    def delete(cls, handle: str, password_id: str) -> dict[str, Any]:
        """Delete an SMTP password from a sub-account."""
        from ..client import get_default_client

        return get_default_client().sub_accounts.smtp_passwords.delete(
            handle,
            password_id,
        )

    @classmethod
    async def delete_async(cls, handle: str, password_id: str) -> dict[str, Any]:
        """Delete an SMTP password from a sub-account using async HTTP."""
        from ..client import get_default_client

        return await get_default_client().sub_accounts.smtp_passwords.delete_async(
            handle,
            password_id,
        )


class _LimitsProxy:
    """Module-level proxy for sub-account limit operations."""

    @classmethod
    def set(
        cls,
        handle: str,
        *,
        sends: int | None = None,
        monthly_limit: int | None = None,
    ) -> SubAccountLimit | MailChannelsResponse:
        """Set the monthly sending limit for a sub-account."""
        from ..client import get_default_client

        return get_default_client().sub_accounts.limits.set(
            handle,
            sends=sends,
            monthly_limit=monthly_limit,
        )

    @classmethod
    async def set_async(
        cls,
        handle: str,
        *,
        sends: int | None = None,
        monthly_limit: int | None = None,
    ) -> SubAccountLimit | MailChannelsResponse:
        """Set the monthly sending limit for a sub-account using async HTTP."""
        from ..client import get_default_client

        return await get_default_client().sub_accounts.limits.set_async(
            handle,
            sends=sends,
            monthly_limit=monthly_limit,
        )

    @classmethod
    def retrieve(cls, handle: str) -> SubAccountLimit | MailChannelsResponse:
        """Retrieve the sending limit for a sub-account."""
        from ..client import get_default_client

        return get_default_client().sub_accounts.limits.retrieve(handle)

    @classmethod
    async def retrieve_async(
        cls,
        handle: str,
    ) -> SubAccountLimit | MailChannelsResponse:
        """Retrieve the sending limit for a sub-account using async HTTP."""
        from ..client import get_default_client

        return await get_default_client().sub_accounts.limits.retrieve_async(handle)

    @classmethod
    def delete(cls, handle: str) -> dict[str, Any]:
        """Delete the sending limit for a sub-account."""
        from ..client import get_default_client

        return get_default_client().sub_accounts.limits.delete(handle)

    @classmethod
    async def delete_async(cls, handle: str) -> dict[str, Any]:
        """Delete the sending limit for a sub-account using async HTTP."""
        from ..client import get_default_client

        return await get_default_client().sub_accounts.limits.delete_async(handle)


class SubAccounts:
    """Module-level sub-account operations using global SDK configuration."""

    ApiKeys = _ApiKeysProxy
    SmtpPasswords = _SmtpPasswordsProxy
    Limits = _LimitsProxy

    @classmethod
    def create(
        cls,
        *,
        company_name: str | None = None,
        handle: str | None = None,
    ) -> SubAccount | MailChannelsResponse:
        """Create a sub-account under the parent account."""
        from ..client import get_default_client

        return get_default_client().sub_accounts.create(
            company_name=company_name,
            handle=handle,
        )

    @classmethod
    async def create_async(
        cls,
        *,
        company_name: str | None = None,
        handle: str | None = None,
    ) -> SubAccount | MailChannelsResponse:
        """Create a sub-account under the parent account using async HTTP."""
        from ..client import get_default_client

        return await get_default_client().sub_accounts.create_async(
            company_name=company_name,
            handle=handle,
        )

    @classmethod
    def list(
        cls,
        *,
        limit: int | None = None,
        offset: int | None = None,
    ) -> dict[str, Any]:
        """Retrieve sub-accounts for the parent account."""
        from ..client import get_default_client

        return get_default_client().sub_accounts.list(limit=limit, offset=offset)

    @classmethod
    async def list_async(
        cls,
        *,
        limit: int | None = None,
        offset: int | None = None,
    ) -> dict[str, Any]:
        """Retrieve sub-accounts for the parent account using async HTTP."""
        from ..client import get_default_client

        return await get_default_client().sub_accounts.list_async(
            limit=limit,
            offset=offset,
        )

    @classmethod
    def retrieve_usage(cls, handle: str) -> UsageStats | MailChannelsResponse:
        """Retrieve usage statistics for a sub-account."""
        from ..client import get_default_client

        return get_default_client().sub_accounts.retrieve_usage(handle)

    @classmethod
    async def retrieve_usage_async(
        cls,
        handle: str,
    ) -> UsageStats | MailChannelsResponse:
        """Retrieve usage statistics for a sub-account using async HTTP."""
        from ..client import get_default_client

        return await get_default_client().sub_accounts.retrieve_usage_async(handle)

    @classmethod
    def suspend(cls, handle: str) -> dict[str, Any]:
        """Suspend a sub-account."""
        from ..client import get_default_client

        return get_default_client().sub_accounts.suspend(handle)

    @classmethod
    async def suspend_async(cls, handle: str) -> dict[str, Any]:
        """Suspend a sub-account using async HTTP."""
        from ..client import get_default_client

        return await get_default_client().sub_accounts.suspend_async(handle)

    @classmethod
    def activate(cls, handle: str) -> dict[str, Any]:
        """Activate a suspended sub-account."""
        from ..client import get_default_client

        return get_default_client().sub_accounts.activate(handle)

    @classmethod
    async def activate_async(cls, handle: str) -> dict[str, Any]:
        """Activate a suspended sub-account using async HTTP."""
        from ..client import get_default_client

        return await get_default_client().sub_accounts.activate_async(handle)

    @classmethod
    def delete(cls, handle: str) -> dict[str, Any]:
        """Delete a sub-account."""
        from ..client import get_default_client

        return get_default_client().sub_accounts.delete(handle)

    @classmethod
    async def delete_async(cls, handle: str) -> dict[str, Any]:
        """Delete a sub-account using async HTTP."""
        from ..client import get_default_client

        return await get_default_client().sub_accounts.delete_async(handle)
