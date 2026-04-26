"""Webhook request, response, and helper types."""

from __future__ import annotations

from typing import Any, Literal, TypedDict

from pydantic import BaseModel, ConfigDict

WebhookBatchStatus = Literal["1xx", "2xx", "3xx", "4xx", "5xx", "no_response"]
WebhookEvent = Literal[
    "open",
    "click",
    "processed",
    "delivered",
    "dropped",
    "hard-bounced",
    "soft-bounced",
    "unsubscribed",
    "complained",
    "test",
]


class Webhook(BaseModel):
    """A configured MailChannels webhook endpoint."""

    model_config = ConfigDict(extra="allow")

    webhook: str


class WebhookBatchDuration(BaseModel):
    """Duration metadata for a webhook batch delivery attempt."""

    model_config = ConfigDict(extra="allow")

    value: int
    unit: Literal["milliseconds"]


class WebhookBatch(BaseModel):
    """One MailChannels webhook batch delivery attempt."""

    model_config = ConfigDict(extra="allow")

    batch_id: int
    customer_handle: str
    webhook: str
    status: str
    created_at: str
    event_count: int
    duration: WebhookBatchDuration | None = None
    status_code: int | None = None


class WebhookBatchResult(BaseModel):
    """Paged webhook batch result."""

    model_config = ConfigDict(extra="allow")

    webhook_batches: list[WebhookBatch]


class WebhookValidationRequest(TypedDict, total=False):
    """Request body used to validate enrolled webhooks."""

    request_id: str


class WebhookValidationResponse(BaseModel):
    """HTTP response returned by a validated webhook endpoint."""

    model_config = ConfigDict(extra="allow")

    status: int
    body: str | None = None


class WebhookValidationResult(BaseModel):
    """Validation result for one webhook endpoint."""

    model_config = ConfigDict(extra="allow")

    webhook: str
    result: Literal["passed", "failed"]
    response: WebhookValidationResponse | None = None


class WebhookValidationResults(BaseModel):
    """Validation results for enrolled webhook endpoints."""

    model_config = ConfigDict(extra="allow")

    all_passed: bool
    results: list[WebhookValidationResult]


class WebhookPublicKey(BaseModel):
    """Webhook public signing key returned by MailChannels."""

    model_config = ConfigDict(extra="allow")

    id: str
    key: str


class WebhookEventPayload(BaseModel):
    """Common fields present on MailChannels delivery event payloads."""

    model_config = ConfigDict(extra="allow")

    email: str | None = None
    customer_handle: str
    timestamp: int
    event: WebhookEvent | str
    request_id: str | None = None
    smtp_id: str | None = None
    recipients: list[str] | None = None
    status: str | None = None
    reason: str | None = None


class SignatureParameters(BaseModel):
    """Parsed metadata from a MailChannels Signature-Input header."""

    model_config = ConfigDict(extra="allow")

    signature_name: str
    covered_components: list[str]
    created: int | None = None
    algorithm: str | None = None
    key_id: str | None = None
    raw: str


WebhookHeaders = dict[str, str]
WebhookPayload = list[dict[str, Any]]
