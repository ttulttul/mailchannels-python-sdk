"""Webhook resource implementation and verification helpers."""

from __future__ import annotations

import base64
import binascii
import hashlib
import logging
import re
import time
from builtins import list as list_type
from typing import Any

from ..query import compact_query, pagination_query
from .types import (
    SignatureParameters,
    WebhookBatchResult,
    WebhookBatchStatus,
    WebhookPublicKey,
    WebhookValidationResults,
)

logger = logging.getLogger(__name__)

_SIGNATURE_INPUT_RE = re.compile(
    r"^(?P<name>[^=]+)=\((?P<covered>[^)]*)\)(?P<params>.*)$"
)
_PARAM_RE = re.compile(r";(?P<key>[a-zA-Z0-9_-]+)=(?P<value>\"[^\"]*\"|[^;]+)")
_DIGEST_RE = re.compile(r"sha-256=:(?P<digest>[^:]+):")


class WebhooksResource:
    """Client-bound webhook operations."""

    def __init__(self, client: Any) -> None:
        """Create a webhook resource bound to a client."""
        self._client = client

    def list(self) -> dict[str, Any]:
        """Retrieve configured webhook endpoints."""
        logger.info("Listing MailChannels webhooks")
        return self._client.request("GET", "/webhook")

    async def list_async(self) -> dict[str, Any]:
        """Retrieve configured webhook endpoints using async HTTP."""
        logger.info("Listing MailChannels webhooks using async HTTP")
        return await self._client.request_async("GET", "/webhook")

    def create(self, endpoint: str) -> dict[str, Any]:
        """Enroll a webhook endpoint for delivery events."""
        logger.info("Creating MailChannels webhook endpoint=%s", endpoint)
        return self._client.request(
            "POST",
            "/webhook",
            params={"endpoint": endpoint},
        )

    async def create_async(self, endpoint: str) -> dict[str, Any]:
        """Enroll a webhook endpoint for delivery events using async HTTP."""
        logger.info(
            "Creating MailChannels webhook using async HTTP endpoint=%s",
            endpoint,
        )
        return await self._client.request_async(
            "POST",
            "/webhook",
            params={"endpoint": endpoint},
        )

    def delete(self) -> dict[str, Any]:
        """Delete all configured webhook endpoints."""
        logger.warning("Deleting all MailChannels webhooks")
        return self._client.request("DELETE", "/webhook")

    async def delete_async(self) -> dict[str, Any]:
        """Delete all configured webhook endpoints using async HTTP."""
        logger.warning("Deleting all MailChannels webhooks using async HTTP")
        return await self._client.request_async("DELETE", "/webhook")

    def batches(
        self,
        *,
        created_after: str | None = None,
        created_before: str | None = None,
        statuses: list_type[WebhookBatchStatus] | None = None,
        webhook: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> dict[str, Any]:
        """Retrieve webhook delivery batches."""
        logger.info("Listing MailChannels webhook batches")
        return self._client.request(
            "GET",
            "/webhook-batch",
            params=pagination_query(
                limit=limit,
                offset=offset,
                created_after=created_after,
                created_before=created_before,
                statuses=statuses,
                webhook=webhook,
            )
            or None,
            response_model=WebhookBatchResult,
        )

    async def batches_async(
        self,
        *,
        created_after: str | None = None,
        created_before: str | None = None,
        statuses: list_type[WebhookBatchStatus] | None = None,
        webhook: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> dict[str, Any]:
        """Retrieve webhook delivery batches using async HTTP."""
        logger.info("Listing MailChannels webhook batches using async HTTP")
        return await self._client.request_async(
            "GET",
            "/webhook-batch",
            params=pagination_query(
                limit=limit,
                offset=offset,
                created_after=created_after,
                created_before=created_before,
                statuses=statuses,
                webhook=webhook,
            )
            or None,
            response_model=WebhookBatchResult,
        )

    def resend_batch(self, batch_id: int, *, customer_handle: str) -> dict[str, Any]:
        """Synchronously resend one webhook batch."""
        logger.warning(
            "Resending MailChannels webhook batch batch_id=%s customer_handle=%s",
            batch_id,
            customer_handle,
        )
        return self._client.request(
            "POST",
            f"/webhook-batch/{batch_id}/resend",
            extra_headers={"X-Customer-Handle": customer_handle},
            require_api_key=False,
        )

    async def resend_batch_async(
        self,
        batch_id: int,
        *,
        customer_handle: str,
    ) -> dict[str, Any]:
        """Synchronously resend one webhook batch using async HTTP."""
        logger.warning(
            "Resending MailChannels webhook batch using async HTTP batch_id=%s "
            "customer_handle=%s",
            batch_id,
            customer_handle,
        )
        return await self._client.request_async(
            "POST",
            f"/webhook-batch/{batch_id}/resend",
            extra_headers={"X-Customer-Handle": customer_handle},
            require_api_key=False,
        )

    def public_key(self, key_id: str) -> dict[str, Any]:
        """Retrieve a webhook public signing key by ID."""
        logger.info("Retrieving MailChannels webhook public key key_id=%s", key_id)
        return self._client.request(
            "GET",
            "/webhook/public-key",
            params={"id": key_id},
            require_api_key=False,
            response_model=WebhookPublicKey,
        )

    async def public_key_async(self, key_id: str) -> dict[str, Any]:
        """Retrieve a webhook public signing key by ID using async HTTP."""
        logger.info(
            "Retrieving MailChannels webhook public key using async HTTP key_id=%s",
            key_id,
        )
        return await self._client.request_async(
            "GET",
            "/webhook/public-key",
            params={"id": key_id},
            require_api_key=False,
            response_model=WebhookPublicKey,
        )

    def validate(self, *, request_id: str | None = None) -> dict[str, Any]:
        """Validate enrolled webhook endpoints with a test event."""
        logger.info("Validating MailChannels webhooks request_id=%s", request_id)
        return self._client.request(
            "POST",
            "/webhook/validate",
            json=compact_query({"request_id": request_id}) or None,
            response_model=WebhookValidationResults,
        )

    async def validate_async(self, *, request_id: str | None = None) -> dict[str, Any]:
        """Validate enrolled webhook endpoints with a test event using async HTTP."""
        logger.info(
            "Validating MailChannels webhooks using async HTTP request_id=%s",
            request_id,
        )
        return await self._client.request_async(
            "POST",
            "/webhook/validate",
            json=compact_query({"request_id": request_id}) or None,
            response_model=WebhookValidationResults,
        )


class Webhooks:
    """Module-level webhook operations using global SDK configuration."""

    @classmethod
    def list(cls) -> dict[str, Any]:
        """Retrieve configured webhook endpoints."""
        from ..client import get_default_client

        return get_default_client().webhooks.list()

    @classmethod
    async def list_async(cls) -> dict[str, Any]:
        """Retrieve configured webhook endpoints using async HTTP."""
        from ..client import get_default_client

        return await get_default_client().webhooks.list_async()

    @classmethod
    def create(cls, endpoint: str) -> dict[str, Any]:
        """Enroll a webhook endpoint for delivery events."""
        from ..client import get_default_client

        return get_default_client().webhooks.create(endpoint)

    @classmethod
    async def create_async(cls, endpoint: str) -> dict[str, Any]:
        """Enroll a webhook endpoint for delivery events using async HTTP."""
        from ..client import get_default_client

        return await get_default_client().webhooks.create_async(endpoint)

    @classmethod
    def delete(cls) -> dict[str, Any]:
        """Delete all configured webhook endpoints."""
        from ..client import get_default_client

        return get_default_client().webhooks.delete()

    @classmethod
    async def delete_async(cls) -> dict[str, Any]:
        """Delete all configured webhook endpoints using async HTTP."""
        from ..client import get_default_client

        return await get_default_client().webhooks.delete_async()

    @classmethod
    def batches(
        cls,
        *,
        created_after: str | None = None,
        created_before: str | None = None,
        statuses: list_type[WebhookBatchStatus] | None = None,
        webhook: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> dict[str, Any]:
        """Retrieve webhook delivery batches."""
        from ..client import get_default_client

        return get_default_client().webhooks.batches(
            created_after=created_after,
            created_before=created_before,
            statuses=statuses,
            webhook=webhook,
            limit=limit,
            offset=offset,
        )

    @classmethod
    async def batches_async(
        cls,
        *,
        created_after: str | None = None,
        created_before: str | None = None,
        statuses: list_type[WebhookBatchStatus] | None = None,
        webhook: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> dict[str, Any]:
        """Retrieve webhook delivery batches using async HTTP."""
        from ..client import get_default_client

        return await get_default_client().webhooks.batches_async(
            created_after=created_after,
            created_before=created_before,
            statuses=statuses,
            webhook=webhook,
            limit=limit,
            offset=offset,
        )

    @classmethod
    def resend_batch(cls, batch_id: int, *, customer_handle: str) -> dict[str, Any]:
        """Synchronously resend one webhook batch."""
        from ..client import get_default_client

        return get_default_client().webhooks.resend_batch(
            batch_id,
            customer_handle=customer_handle,
        )

    @classmethod
    async def resend_batch_async(
        cls,
        batch_id: int,
        *,
        customer_handle: str,
    ) -> dict[str, Any]:
        """Synchronously resend one webhook batch using async HTTP."""
        from ..client import get_default_client

        return await get_default_client().webhooks.resend_batch_async(
            batch_id,
            customer_handle=customer_handle,
        )

    @classmethod
    def public_key(cls, key_id: str) -> dict[str, Any]:
        """Retrieve a webhook public signing key by ID."""
        from ..client import get_default_client

        return get_default_client().webhooks.public_key(key_id)

    @classmethod
    async def public_key_async(cls, key_id: str) -> dict[str, Any]:
        """Retrieve a webhook public signing key by ID using async HTTP."""
        from ..client import get_default_client

        return await get_default_client().webhooks.public_key_async(key_id)

    @classmethod
    def validate(cls, *, request_id: str | None = None) -> dict[str, Any]:
        """Validate enrolled webhook endpoints with a test event."""
        from ..client import get_default_client

        return get_default_client().webhooks.validate(request_id=request_id)

    @classmethod
    async def validate_async(cls, *, request_id: str | None = None) -> dict[str, Any]:
        """Validate enrolled webhook endpoints with a test event using async HTTP."""
        from ..client import get_default_client

        return await get_default_client().webhooks.validate_async(request_id=request_id)

    @staticmethod
    def parse_signature_input(value: str) -> SignatureParameters:
        """Parse a MailChannels RFC 9421 Signature-Input header value."""
        return parse_signature_input(value)

    @staticmethod
    def verify_content_digest(headers: dict[str, str], body: bytes | str) -> bool:
        """Verify the webhook Content-Digest header against the raw body."""
        return verify_content_digest(headers, body)

    @staticmethod
    def signature_key_id(headers: dict[str, str]) -> str | None:
        """Extract the signing key ID from webhook headers."""
        return signature_key_id(headers)

    @staticmethod
    def signature_is_fresh(
        parameters: SignatureParameters,
        *,
        tolerance_seconds: int = 300,
        now: int | None = None,
    ) -> bool:
        """Return whether a signature timestamp is within the allowed age."""
        return signature_is_fresh(
            parameters,
            tolerance_seconds=tolerance_seconds,
            now=now,
        )


def parse_signature_input(value: str) -> SignatureParameters:
    """Parse a MailChannels RFC 9421 Signature-Input header value."""
    match = _SIGNATURE_INPUT_RE.match(value.strip())
    if not match:
        logger.error("Invalid MailChannels Signature-Input header")
        raise ValueError("Invalid Signature-Input header.")

    covered = [
        component.strip().strip('"')
        for component in match.group("covered").split()
        if component.strip()
    ]
    parameters = {
        param.group("key"): _unquote(param.group("value"))
        for param in _PARAM_RE.finditer(match.group("params"))
    }
    created = parameters.get("created")
    return SignatureParameters(
        signature_name=match.group("name").strip(),
        covered_components=covered,
        created=int(created) if created and created.isdigit() else None,
        algorithm=parameters.get("alg"),
        key_id=parameters.get("keyid"),
        raw=value,
    )


def signature_key_id(headers: dict[str, str]) -> str | None:
    """Extract the signing key ID from webhook headers."""
    signature_input = _header(headers, "Signature-Input")
    if signature_input is None:
        logger.warning("Webhook request is missing Signature-Input header")
        return None
    return parse_signature_input(signature_input).key_id


def signature_is_fresh(
    parameters: SignatureParameters,
    *,
    tolerance_seconds: int = 300,
    now: int | None = None,
) -> bool:
    """Return whether a signature timestamp is within the allowed age."""
    if parameters.created is None:
        logger.warning("Webhook signature is missing created timestamp")
        return False
    reference = now if now is not None else int(time.time())
    age = abs(reference - parameters.created)
    fresh = age <= tolerance_seconds
    logger.debug("Webhook signature age=%s fresh=%s", age, fresh)
    return fresh


def verify_content_digest(headers: dict[str, str], body: bytes | str) -> bool:
    """Verify the webhook Content-Digest header against the raw request body."""
    digest_header = _header(headers, "Content-Digest")
    if digest_header is None:
        logger.warning("Webhook request is missing Content-Digest header")
        return False
    match = _DIGEST_RE.search(digest_header)
    if not match:
        logger.warning("Webhook Content-Digest header is not sha-256 encoded")
        return False
    raw_body = body.encode("utf-8") if isinstance(body, str) else body
    try:
        expected = base64.b64decode(match.group("digest"), validate=True)
    except binascii.Error:
        logger.warning("Webhook Content-Digest header is not valid base64")
        return False
    actual = hashlib.sha256(raw_body).digest()
    verified = expected == actual
    logger.debug("Webhook content digest verified=%s", verified)
    return verified


def _header(headers: dict[str, str], name: str) -> str | None:
    """Read an HTTP header case-insensitively."""
    lowered = name.lower()
    for key, value in headers.items():
        if key.lower() == lowered:
            return value
    return None


def _unquote(value: str) -> str:
    """Remove optional HTTP structured field quotes."""
    stripped = value.strip()
    if stripped.startswith('"') and stripped.endswith('"'):
        return stripped[1:-1]
    return stripped
