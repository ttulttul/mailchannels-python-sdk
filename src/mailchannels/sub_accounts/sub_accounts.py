"""Sub-account resource implementation."""

from __future__ import annotations

import logging
from typing import Any

from ..query import pagination_query
from .types import compact_payload

logger = logging.getLogger(__name__)


class SubAccountApiKeysResource:
    """Client-bound sub-account API key operations."""

    def __init__(self, client: Any) -> None:
        """Create a sub-account API key resource bound to a client."""
        self._client = client

    def create(self, handle: str) -> dict[str, Any]:
        """Create an API key for a sub-account."""
        logger.info("Creating MailChannels sub-account API key handle=%s", handle)
        return self._client.request("POST", f"/sub-account/{handle}/api-key")

    async def create_async(self, handle: str) -> dict[str, Any]:
        """Create an API key for a sub-account using async HTTP."""
        logger.info(
            "Creating MailChannels sub-account API key using async HTTP handle=%s",
            handle,
        )
        return await self._client.request_async(
            "POST",
            f"/sub-account/{handle}/api-key",
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


class SubAccountSmtpPasswordsResource:
    """Client-bound sub-account SMTP password operations."""

    def __init__(self, client: Any) -> None:
        """Create a sub-account SMTP password resource bound to a client."""
        self._client = client

    def create(self, handle: str) -> dict[str, Any]:
        """Create an SMTP password for a sub-account."""
        logger.info("Creating MailChannels sub-account SMTP password handle=%s", handle)
        return self._client.request("POST", f"/sub-account/{handle}/smtp-password")

    async def create_async(self, handle: str) -> dict[str, Any]:
        """Create an SMTP password for a sub-account using async HTTP."""
        logger.info(
            "Creating MailChannels sub-account SMTP password using async HTTP "
            "handle=%s",
            handle,
        )
        return await self._client.request_async(
            "POST",
            f"/sub-account/{handle}/smtp-password",
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


class SubAccountLimitsResource:
    """Client-bound sub-account sending limit operations."""

    def __init__(self, client: Any) -> None:
        """Create a sub-account limits resource bound to a client."""
        self._client = client

    def set(self, handle: str, *, monthly_limit: int) -> dict[str, Any]:
        """Set the monthly sending limit for a sub-account."""
        logger.info(
            "Setting MailChannels sub-account limit handle=%s monthly_limit=%s",
            handle,
            monthly_limit,
        )
        return self._client.request(
            "POST",
            f"/sub-account/{handle}/limits",
            json={"monthly_limit": monthly_limit},
        )

    async def set_async(self, handle: str, *, monthly_limit: int) -> dict[str, Any]:
        """Set the monthly sending limit for a sub-account using async HTTP."""
        logger.info(
            "Setting MailChannels sub-account limit using async HTTP handle=%s "
            "monthly_limit=%s",
            handle,
            monthly_limit,
        )
        return await self._client.request_async(
            "POST",
            f"/sub-account/{handle}/limits",
            json={"monthly_limit": monthly_limit},
        )

    def retrieve(self, handle: str) -> dict[str, Any]:
        """Retrieve the sending limit for a sub-account."""
        logger.info("Retrieving MailChannels sub-account limit handle=%s", handle)
        return self._client.request("GET", f"/sub-account/{handle}/limits")

    async def retrieve_async(self, handle: str) -> dict[str, Any]:
        """Retrieve the sending limit for a sub-account using async HTTP."""
        logger.info(
            "Retrieving MailChannels sub-account limit using async HTTP handle=%s",
            handle,
        )
        return await self._client.request_async("GET", f"/sub-account/{handle}/limits")

    def delete(self, handle: str) -> dict[str, Any]:
        """Delete the sending limit for a sub-account."""
        logger.info("Deleting MailChannels sub-account limit handle=%s", handle)
        return self._client.request("DELETE", f"/sub-account/{handle}/limits")

    async def delete_async(self, handle: str) -> dict[str, Any]:
        """Delete the sending limit for a sub-account using async HTTP."""
        logger.info(
            "Deleting MailChannels sub-account limit using async HTTP handle=%s",
            handle,
        )
        return await self._client.request_async(
            "DELETE",
            f"/sub-account/{handle}/limits",
        )


class SubAccountsResource:
    """Client-bound sub-account operations."""

    def __init__(self, client: Any) -> None:
        """Create a sub-account resource bound to a client."""
        self._client = client
        self.api_keys = SubAccountApiKeysResource(client)
        self.smtp_passwords = SubAccountSmtpPasswordsResource(client)
        self.limits = SubAccountLimitsResource(client)

    def create(
        self,
        *,
        company_name: str | None = None,
        handle: str | None = None,
    ) -> dict[str, Any]:
        """Create a sub-account under the parent account."""
        logger.info("Creating MailChannels sub-account handle=%s", handle)
        payload = compact_payload({"company_name": company_name, "handle": handle})
        return self._client.request("POST", "/sub-account", json=payload)

    async def create_async(
        self,
        *,
        company_name: str | None = None,
        handle: str | None = None,
    ) -> dict[str, Any]:
        """Create a sub-account under the parent account using async HTTP."""
        logger.info(
            "Creating MailChannels sub-account using async HTTP handle=%s",
            handle,
        )
        payload = compact_payload({"company_name": company_name, "handle": handle})
        return await self._client.request_async("POST", "/sub-account", json=payload)

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

    def retrieve_usage(self, handle: str) -> dict[str, Any]:
        """Retrieve usage statistics for a sub-account."""
        logger.info("Retrieving MailChannels sub-account usage handle=%s", handle)
        return self._client.request("GET", f"/sub-account/{handle}/usage")

    async def retrieve_usage_async(self, handle: str) -> dict[str, Any]:
        """Retrieve usage statistics for a sub-account using async HTTP."""
        logger.info(
            "Retrieving MailChannels sub-account usage using async HTTP handle=%s",
            handle,
        )
        return await self._client.request_async("GET", f"/sub-account/{handle}/usage")

    def suspend(self, handle: str) -> dict[str, Any]:
        """Suspend a sub-account."""
        logger.warning("Suspending MailChannels sub-account handle=%s", handle)
        return self._client.request("POST", f"/sub-account/{handle}/suspend")

    async def suspend_async(self, handle: str) -> dict[str, Any]:
        """Suspend a sub-account using async HTTP."""
        logger.warning(
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
        logger.warning("Deleting MailChannels sub-account handle=%s", handle)
        return self._client.request("DELETE", f"/sub-account/{handle}")

    async def delete_async(self, handle: str) -> dict[str, Any]:
        """Delete a sub-account using async HTTP."""
        logger.warning(
            "Deleting MailChannels sub-account using async HTTP handle=%s",
            handle,
        )
        return await self._client.request_async("DELETE", f"/sub-account/{handle}")


class _ApiKeysProxy:
    """Module-level proxy for sub-account API key operations."""

    @classmethod
    def create(cls, handle: str) -> dict[str, Any]:
        """Create an API key for a sub-account."""
        from ..client import get_default_client

        return get_default_client().sub_accounts.api_keys.create(handle)

    @classmethod
    async def create_async(cls, handle: str) -> dict[str, Any]:
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
    def create(cls, handle: str) -> dict[str, Any]:
        """Create an SMTP password for a sub-account."""
        from ..client import get_default_client

        return get_default_client().sub_accounts.smtp_passwords.create(handle)

    @classmethod
    async def create_async(cls, handle: str) -> dict[str, Any]:
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
    def set(cls, handle: str, *, monthly_limit: int) -> dict[str, Any]:
        """Set the monthly sending limit for a sub-account."""
        from ..client import get_default_client

        return get_default_client().sub_accounts.limits.set(
            handle,
            monthly_limit=monthly_limit,
        )

    @classmethod
    async def set_async(cls, handle: str, *, monthly_limit: int) -> dict[str, Any]:
        """Set the monthly sending limit for a sub-account using async HTTP."""
        from ..client import get_default_client

        return await get_default_client().sub_accounts.limits.set_async(
            handle,
            monthly_limit=monthly_limit,
        )

    @classmethod
    def retrieve(cls, handle: str) -> dict[str, Any]:
        """Retrieve the sending limit for a sub-account."""
        from ..client import get_default_client

        return get_default_client().sub_accounts.limits.retrieve(handle)

    @classmethod
    async def retrieve_async(cls, handle: str) -> dict[str, Any]:
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
    ) -> dict[str, Any]:
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
    ) -> dict[str, Any]:
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
    def retrieve_usage(cls, handle: str) -> dict[str, Any]:
        """Retrieve usage statistics for a sub-account."""
        from ..client import get_default_client

        return get_default_client().sub_accounts.retrieve_usage(handle)

    @classmethod
    async def retrieve_usage_async(cls, handle: str) -> dict[str, Any]:
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
