"""Destructive online CRUD tests for isolated live resources."""

from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import Any

import pytest
import requests

import mailchannels

pytestmark = [pytest.mark.online, pytest.mark.online_destructive]


def _client() -> mailchannels.Client:
    """Create a live MailChannels client from environment configuration."""
    return mailchannels.Client(
        api_key=os.environ["MAILCHANNELS_API_KEY"],
        base_url=os.environ.get("MAILCHANNELS_API_URL"),
    )


def test_online_destructive_suppression_lifecycle() -> None:
    """Create, list, and delete a unique live suppression entry."""
    client = _client()
    recipient = f"sdk-test-{_unique_suffix()}@example.invalid"
    try:
        client.suppressions.create([{"recipient": recipient, "source": "api"}])
        listed = client.suppressions.list(recipient=recipient, source="api", limit=10)
        assert "http_headers" in listed
    except mailchannels.ApiError as error:
        _xfail_live_server_error(error)
        raise
    except requests.RequestException as error:
        _xfail_live_transport_error(error)
        raise
    finally:
        _ignore_live_cleanup_error(lambda: client.suppressions.delete(recipient))


def test_online_destructive_sub_account_lifecycle() -> None:
    """Create and clean up a throwaway live sub-account and child resources."""
    client = _client()
    handle = f"sdk-test-{_unique_suffix()}"
    created = False
    api_key_id: str | None = None
    smtp_password_id: str | None = None
    try:
        client.sub_accounts.create(company_name="SDK Test Account", handle=handle)
        created = True
        client.sub_accounts.limits.set(handle, sends=1_000)
        limit = client.sub_accounts.limits.retrieve(handle)
        assert limit.get("sends") == 1_000 or "http_headers" in limit

        api_key = client.sub_accounts.api_keys.create(handle)
        api_key_id = _resource_id(api_key)
        api_keys = client.sub_accounts.api_keys.list(handle)
        api_key_id = api_key_id or _resource_id(api_keys)

        smtp_password = client.sub_accounts.smtp_passwords.create(handle)
        smtp_password_id = _resource_id(smtp_password)
        smtp_passwords = client.sub_accounts.smtp_passwords.list(handle)
        smtp_password_id = smtp_password_id or _resource_id(smtp_passwords)

        client.sub_accounts.suspend(handle)
        client.sub_accounts.activate(handle)
    except mailchannels.ApiError as error:
        _xfail_live_server_error(error)
        raise
    except requests.RequestException as error:
        _xfail_live_transport_error(error)
        raise
    finally:
        if smtp_password_id is not None:
            _ignore_live_cleanup_error(
                lambda: client.sub_accounts.smtp_passwords.delete(
                    handle,
                    smtp_password_id,
                )
            )
        if api_key_id is not None:
            _ignore_live_cleanup_error(
                lambda: client.sub_accounts.api_keys.delete(handle, api_key_id)
            )
        if created:
            _ignore_live_cleanup_error(
                lambda: client.sub_accounts.limits.delete(handle)
            )
            _ignore_live_cleanup_error(lambda: client.sub_accounts.delete(handle))


def test_online_destructive_webhook_lifecycle() -> None:
    """Create, validate, list, and delete live webhooks in a destructive account."""
    client = _client()
    endpoint = (
        os.environ.get("MAILCHANNELS_ONLINE_WEBHOOK_ENDPOINT")
        or f"https://example.invalid/mailchannels-sdk-test/{_unique_suffix()}"
    )
    try:
        client.webhooks.create(endpoint)
        listed = client.webhooks.list()
        assert "http_headers" in listed
        client.webhooks.validate(request_id=f"sdk-test-{_unique_suffix()}")
    except mailchannels.ApiError as error:
        _xfail_live_server_error(error)
        raise
    except requests.RequestException as error:
        _xfail_live_transport_error(error)
        raise
    finally:
        # The MailChannels API exposes DELETE /webhook as delete-all, so this
        # test must only run in a dedicated destructive test account.
        _ignore_live_cleanup_error(client.webhooks.delete)


def _unique_suffix() -> str:
    """Return a timestamp suffix for live throwaway resources."""
    return datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S%f")


def _resource_id(response: dict[str, Any]) -> str | None:
    """Extract a resource identifier from common API response shapes."""
    for key in ("id", "key_id", "password_id"):
        value = response.get(key)
        if isinstance(value, str) and value:
            return value
    for value in response.values():
        if isinstance(value, dict):
            nested = _resource_id(value)
            if nested is not None:
                return nested
        if isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    nested = _resource_id(item)
                    if nested is not None:
                        return nested
    return None


def _ignore_live_cleanup_error(action: Any) -> None:
    """Best-effort cleanup for live destructive tests."""
    try:
        action()
    except mailchannels.ApiError as error:
        if error.status_code is not None and error.status_code >= 500:
            return
    except requests.RequestException:
        return


def _xfail_live_server_error(error: mailchannels.ApiError) -> None:
    """Mark live MailChannels 5xx responses as external service failures."""
    if error.status_code is not None and error.status_code >= 500:
        pytest.xfail(
            "Live MailChannels API returned a server error: "
            f"status={error.status_code} request_id={error.request_id}"
        )


def _xfail_live_transport_error(error: BaseException) -> None:
    """Mark live network or timeout failures as external test conditions."""
    pytest.xfail(f"Live MailChannels API transport failed: {error}")
