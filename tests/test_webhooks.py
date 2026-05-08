"""Tests for webhook resources and helpers."""

from __future__ import annotations

import base64
import hashlib
import logging

import pytest
from conftest import FakeHTTPXClient, FakeRequestsClient
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat

from mailchannels.client import Client
from mailchannels.response import SDKResponse
from mailchannels.version import user_agent
from mailchannels.webhooks import (
    parse_signature_input,
    signature_is_fresh,
    signature_key_id,
    verify_content_digest,
    verify_webhook_signature,
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
        "User-Agent": user_agent(),
        "X-Customer-Handle": "customer_123",
    }


def test_webhook_destructive_operations_log_at_info(
    caplog: pytest.LogCaptureFixture,
) -> None:
    """It logs intentional webhook mutations at info level."""
    transport = FakeRequestsClient(SDKResponse(200, {"ok": True}, "{}"))
    client = Client(api_key="test-key", http_client=transport)

    with caplog.at_level(logging.INFO, logger="mailchannels.webhooks.webhooks"):
        client.webhooks.delete()
        client.webhooks.resend_batch(123, customer_handle="customer_123")

    records = [
        record
        for record in caplog.records
        if record.name == "mailchannels.webhooks.webhooks"
    ]
    assert [record.levelno for record in records] == [logging.INFO, logging.INFO]


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


def test_webhook_signature_verification_accepts_valid_ed25519_signature() -> None:
    """It verifies a complete MailChannels webhook signature."""
    private_key = Ed25519PrivateKey.generate()
    public_key = private_key.public_key().public_bytes(
        encoding=Encoding.Raw,
        format=PublicFormat.Raw,
    )
    body = b'[{"event":"delivered","customer_handle":"customer_123"}]'
    digest = base64.b64encode(hashlib.sha256(body).digest()).decode("ascii")
    signature_input = (
        'sig=("content-digest");created=1738868393;alg="ed25519";keyid="mckey"'
    )
    signature_base = (
        f'"content-digest": sha-256=:{digest}:\n'
        f'"@signature-params": {signature_input.split("=", maxsplit=1)[1]}'
    ).encode()
    signature = base64.b64encode(private_key.sign(signature_base)).decode("ascii")
    headers = {
        "Content-Digest": f"sha-256=:{digest}:",
        "Signature-Input": signature_input,
        "Signature": f"sig=:{signature}:",
    }

    assert verify_webhook_signature(
        headers,
        body,
        {"key": base64.b64encode(public_key).decode("ascii")},
        now=1738868400,
    )


def test_webhooks_static_verify_accepts_public_key_model_response() -> None:
    """It exposes full signature verification from the Webhooks namespace."""
    private_key = Ed25519PrivateKey.generate()
    public_key = private_key.public_key().public_bytes(
        encoding=Encoding.Raw,
        format=PublicFormat.Raw,
    )
    body = b'{"event":"processed"}'
    digest = base64.b64encode(hashlib.sha256(body).digest()).decode("ascii")
    signature_input = 'sig=("content-digest");created=10;keyid="mckey"'
    signature_base = (
        f'"content-digest": sha-256=:{digest}:\n'
        f'"@signature-params": {signature_input.split("=", maxsplit=1)[1]}'
    ).encode()
    signature = base64.b64encode(private_key.sign(signature_base)).decode("ascii")
    headers = {
        "content-digest": f"sha-256=:{digest}:",
        "signature-input": signature_input,
        "signature": f"sig=:{signature}:",
    }

    assert Client(api_key="test-key").webhooks.verify(
        headers,
        body,
        base64.b64encode(public_key).decode("ascii"),
        now=12,
    )


def test_webhook_content_digest_missing_header_returns_false() -> None:
    """It rejects webhook requests without a Content-Digest header."""
    assert not verify_content_digest({}, b"{}")


def test_webhook_signature_verification_rejects_bad_signature() -> None:
    """It rejects forged webhook signatures even when the digest matches."""
    private_key = Ed25519PrivateKey.generate()
    other_key = Ed25519PrivateKey.generate().public_key().public_bytes(
        encoding=Encoding.Raw,
        format=PublicFormat.Raw,
    )
    body = b"{}"
    digest = base64.b64encode(hashlib.sha256(body).digest()).decode("ascii")
    signature_input = 'sig=("content-digest");created=10;keyid="mckey"'
    signature_base = (
        f'"content-digest": sha-256=:{digest}:\n'
        f'"@signature-params": {signature_input.split("=", maxsplit=1)[1]}'
    ).encode()
    signature = base64.b64encode(private_key.sign(signature_base)).decode("ascii")

    assert not verify_webhook_signature(
        {
            "Content-Digest": f"sha-256=:{digest}:",
            "Signature-Input": signature_input,
            "Signature": f"sig=:{signature}:",
        },
        body,
        base64.b64encode(other_key).decode("ascii"),
        now=12,
    )


def test_webhook_signature_verification_rejects_missing_signature_header() -> None:
    """It rejects requests that only include a matching content digest."""
    body = b"{}"
    digest = base64.b64encode(hashlib.sha256(body).digest()).decode("ascii")

    assert not verify_webhook_signature(
        {
            "Content-Digest": f"sha-256=:{digest}:",
            "Signature-Input": 'sig=("content-digest");created=10;keyid="mckey"',
        },
        body,
        "x" * 44,
        now=12,
    )


def test_webhook_content_digest_wrong_digest_returns_false() -> None:
    """It rejects webhook bodies that do not match the supplied digest."""
    digest = base64.b64encode(hashlib.sha256(b"expected").digest()).decode("ascii")

    assert not verify_content_digest({"Content-Digest": f"sha-256=:{digest}:"}, b"bad")


@pytest.mark.parametrize(
    "digest_header",
    [
        "sha-512=:abc:",
        "sha-256=abc",
        "not-a-digest",
    ],
)
def test_webhook_content_digest_malformed_header_returns_false(
    digest_header: str,
) -> None:
    """It rejects malformed Content-Digest headers without crashing."""
    assert not verify_content_digest({"Content-Digest": digest_header}, b"{}")


def test_webhook_content_digest_non_base64_returns_false() -> None:
    """It rejects invalid base64 digest values without crashing."""
    assert not verify_content_digest({"Content-Digest": "sha-256=:%%%%:"}, b"{}")


def test_webhook_content_digest_header_lookup_is_case_insensitive() -> None:
    """It accepts case variations in webhook digest headers."""
    body = b'{"event":"delivered"}'
    digest = base64.b64encode(hashlib.sha256(body).digest()).decode("ascii")

    assert verify_content_digest({"content-digest": f"sha-256=:{digest}:"}, body)


def test_webhook_signature_key_id_missing_header_returns_none() -> None:
    """It returns None when Signature-Input is absent."""
    assert signature_key_id({}) is None


def test_webhook_signature_key_id_header_lookup_is_case_insensitive() -> None:
    """It accepts case variations in webhook signature headers."""
    headers = {
        "signature-input": (
            'sig=("content-digest");created=1738868393;'
            'alg="ed25519";keyid="mckey"'
        )
    }

    assert signature_key_id(headers) == "mckey"


def test_webhook_signature_key_id_malformed_header_raises_value_error() -> None:
    """It raises ValueError for malformed Signature-Input headers."""
    with pytest.raises(ValueError):
        signature_key_id({"Signature-Input": "not a structured signature input"})


def test_webhook_signature_missing_created_is_not_fresh() -> None:
    """It treats signatures without created timestamps as stale."""
    parameters = parse_signature_input('sig=("content-digest");keyid="mckey"')

    assert parameters.created is None
    assert not signature_is_fresh(parameters, now=1738868400)


def test_webhook_signature_created_outside_tolerance_is_not_fresh() -> None:
    """It rejects signatures older than the allowed tolerance."""
    parameters = parse_signature_input(
        'sig=("content-digest");created=1738860000;keyid="mckey"'
    )

    assert not signature_is_fresh(parameters, now=1738868400, tolerance_seconds=300)


def test_webhook_signature_tolerance_alias_controls_max_age() -> None:
    """It keeps tolerance_seconds as a compatibility alias for max age."""
    parameters = parse_signature_input(
        'sig=("content-digest");created=1738868000;keyid="mckey"'
    )

    assert not signature_is_fresh(parameters, now=1738868400)
    assert signature_is_fresh(parameters, now=1738868400, tolerance_seconds=500)


def test_webhook_signature_small_future_skew_is_fresh() -> None:
    """It accepts a small forward clock skew."""
    parameters = parse_signature_input(
        'sig=("content-digest");created=1738868425;keyid="mckey"'
    )

    assert signature_is_fresh(parameters, now=1738868400)


def test_webhook_signature_future_within_age_but_outside_skew_is_not_fresh() -> None:
    """It rejects future signatures even when inside the stale-age window."""
    parameters = parse_signature_input(
        'sig=("content-digest");created=1738868460;keyid="mckey"'
    )

    assert not signature_is_fresh(parameters, now=1738868400)
    assert signature_is_fresh(
        parameters,
        now=1738868400,
        max_skew_seconds=60,
    )


def test_webhook_signature_future_created_outside_tolerance_is_not_fresh() -> None:
    """It rejects signatures created too far in the future."""
    parameters = parse_signature_input(
        'sig=("content-digest");created=1738872000;keyid="mckey"'
    )

    assert not signature_is_fresh(parameters, now=1738868400, tolerance_seconds=300)
