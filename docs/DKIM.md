# DKIM And DNS

MailChannels supports both hosted DKIM private keys and customer-managed DKIM
private keys in send payloads.

## Hosted DKIM Keys

MailChannels can generate and store DKIM private keys for your account. This is
the easiest way to avoid handling private key material in your own application:
create a key pair with the DKIM API, publish the returned public DNS record, and
then reference the selector when sending.

```python
key = mailchannels.Dkim.create(
    "example.com",
    selector="mcdkim",
    algorithm="rsa",
    key_length=2048,
)

for record in key.get("dkim_dns_records", []):
    print(record["name"], record["type"], record["value"])
```

MailChannels hosts the private key used for signing. It does not host DKIM
public keys for your domain; you must copy the returned public DKIM TXT record
into your own DNS zone. The TXT record name will look like
`mcdkim._domainkey.example.com`.

After the DNS record is published, send mail with the selector. If
`dkim_domain` is omitted, MailChannels can derive it from the `from` address,
but setting it explicitly keeps the signing intent obvious.

```python
mailchannels.Emails.queue(
    {
        "from": {"email": "sender@example.com"},
        "to": [{"email": "recipient@example.net"}],
        "subject": "DKIM signed message",
        "text": "This message is signed by a MailChannels-hosted DKIM key.",
        "dkim_domain": "example.com",
        "dkim_selector": "mcdkim",
    }
)
```

## Rotate Hosted Keys

You can retrieve keys, include the suggested DNS record in the response, update
key status, and rotate active keys. Rotation creates a replacement key and
returns the DNS record you need to publish before switching all signing traffic
to the new selector.

```python
keys = mailchannels.Dkim.list("example.com", include_dns_record=True)
rotated = mailchannels.Dkim.rotate(
    "example.com",
    "mcdkim",
    new_selector="mcdkim2",
)
mailchannels.Dkim.update_status("example.com", "mcdkim", status="rotated")
```

## Customer-Managed Private Keys

If you manage your own DKIM keys, pass `dkim_domain`, `dkim_selector`, and the
Base64-encoded `dkim_private_key` in the send payload. Values set inside a
personalization override root-level DKIM values for that recipient.

## Publish DKIM Records With Cloudflare

If your DNS is hosted in Cloudflare, you can publish the returned DKIM TXT
record with Cloudflare's official Python SDK. The example below uses
`CLOUDFLARE_API_TOKEN` from the environment, finds the zone, updates an existing
TXT record when it is present, and creates it when it is missing.

```bash
uv add cloudflare
export CLOUDFLARE_API_TOKEN="your_cloudflare_api_token"
```

```python
from cloudflare import Cloudflare

import mailchannels


DOMAIN = "example.com"
SELECTOR = "mcdkim"

mailchannels.api_key = "YOUR-MAILCHANNELS-API-KEY"
cloudflare = Cloudflare()


def publish_mailchannels_dkim_record() -> None:
    """Create a MailChannels DKIM key and publish its public key in Cloudflare."""
    key = mailchannels.Dkim.create(
        DOMAIN,
        selector=SELECTOR,
        algorithm="rsa",
        key_length=2048,
    )
    dns_record = key["dkim_dns_records"][0]

    zones = cloudflare.zones.list(name=DOMAIN)
    zone = next(iter(zones), None)
    if zone is None:
        raise RuntimeError(f"Cloudflare zone not found: {DOMAIN}")

    records = cloudflare.dns.records.list(
        zone_id=zone.id,
        type="TXT",
        name=dns_record["name"],
    )
    existing_record = next(iter(records), None)

    if existing_record is None:
        updated_record = cloudflare.dns.records.create(
            zone_id=zone.id,
            type="TXT",
            name=dns_record["name"],
            content=dns_record["value"],
            ttl=1,
        )
    else:
        updated_record = cloudflare.dns.records.update(
            existing_record.id,
            zone_id=zone.id,
            type="TXT",
            name=dns_record["name"],
            content=dns_record["value"],
            ttl=1,
        )

    print(f"Published DKIM record: {updated_record.name}")


publish_mailchannels_dkim_record()
```

The Cloudflare token needs permission to read the zone and edit DNS records. In
Cloudflare's dashboard, grant at least `Zone: Read` and `DNS: Edit` for the
zone that owns the sending domain.
