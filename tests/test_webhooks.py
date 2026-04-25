"""Tests for webhook resources and helpers."""

from __future__ import annotations

import base64
import hashlib

from conftest import FakeHTTPXClient, FakeRequestsClient

from mailchannels.client import Client
from mailchannels.response import SDKResponse
from mailchannels.webhooks import (
    parse_signature_input,
    signature_is_fresh,
    signature_key_id,
    verify_content_digest,
)


def test_webhook_management_uses_documented_paths() -> None:
    """It manages webhook endpoints through the documented resource."""
    transport = FakeRequestsClient(SDKResponse(201, None, ""))
    client = Client(api_key="test-key", http_client=transport)

    client.webhooks.create("https://example.com/mailchannels")
    client.webhooks.list()
    client.webhooks.delete()
    client.webhooks.validate(request_id="test_request_1")

    assert [call["method"] for call in transport.calls] == [
        "POST",
        "GET",
        "DELETE",
        "POST",
    ]
    assert [call["url"] for call in transport.calls] == [
        "https://api.mailchannels.net/tx/v1/webhook",
        "https://api.mailchannels.net/tx/v1/webhook",
        "https://api.mailchannels.net/tx/v1/webhook",
        "https://api.mailchannels.net/tx/v1/webhook/validate",
    ]
    assert transport.calls[0]["params"] == {
        "endpoint": "https://example.com/mailchannels"
    }
    assert transport.calls[3]["json"] == {"request_id": "test_request_1"}


def test_webhook_batches_public_key_and_resend() -> None:
    """It exposes webhook batch, public-key, and resend endpoints."""
    transport = FakeRequestsClient(SDKResponse(200, {"ok": True}, "{}"))
    client = Client(api_key="test-key", http_client=transport)

    client.webhooks.batches(statuses=["4xx", "5xx"], limit=25, offset=5)
    client.webhooks.public_key("mckey")
    client.webhooks.resend_batch(123, customer_handle="customer_123")

    assert transport.calls[0]["url"] == (
        "https://api.mailchannels.net/tx/v1/webhook-batch"
    )
    assert transport.calls[0]["params"] == {
        "statuses": "4xx,5xx",
        "limit": 25,
        "offset": 5,
    }
    assert "X-Api-Key" not in transport.calls[1]["headers"]
    assert transport.calls[1]["url"] == (
        "https://api.mailchannels.net/tx/v1/webhook/public-key"
    )
    assert transport.calls[1]["params"] == {"id": "mckey"}
    assert transport.calls[2]["headers"] == {
        "Content-Type": "application/json",
        "User-Agent": "mailchannels-python/0.1.0",
        "X-Customer-Handle": "customer_123",
    }


async def test_webhook_async_methods_use_async_transport() -> None:
    """It exposes async webhook operations."""
    transport = FakeHTTPXClient(SDKResponse(200, {"webhook_batches": []}, "{}"))
    client = Client(api_key="test-key", async_http_client=transport)

    await client.webhooks.batches_async(statuses=["no_response"])

    assert transport.calls[0]["method"] == "GET"
    assert transport.calls[0]["params"] == {"statuses": "no_response"}


def test_webhook_signature_helpers() -> None:
    """It parses signature metadata and verifies the content digest."""
    body = b'[{"event":"delivered","customer_handle":"customer_123"}]'
    digest = base64.b64encode(hashlib.sha256(body).digest()).decode("ascii")
    headers = {
        "Content-Digest": f"sha-256=:{digest}:",
        "Signature-Input": (
            'sig_1738775282=("content-digest");created=1738868393;'
            'alg="ed25519";keyid="mckey"'
        ),
    }

    parameters = parse_signature_input(headers["Signature-Input"])

    assert parameters.signature_name == "sig_1738775282"
    assert parameters.covered_components == ["content-digest"]
    assert parameters.algorithm == "ed25519"
    assert parameters.key_id == "mckey"
    assert signature_key_id(headers) == "mckey"
    assert signature_is_fresh(parameters, now=1738868400)
    assert verify_content_digest(headers, body)
