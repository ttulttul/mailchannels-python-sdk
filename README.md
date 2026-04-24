# MailChannels Python SDK

Typed Python SDK for the MailChannels Email API.

## Install

```bash
uv add mailchannels
```

For async HTTP support:

```bash
uv add "mailchannels[async]"
```

## Send An Email

```python
import mailchannels

mailchannels.api_key = "YOUR-API-KEY"

email = mailchannels.Emails.send(
    {
        "from": {"email": "sender@example.com", "name": "Priya Patel"},
        "to": [{"email": "recipient@example.net", "name": "Sakura Tanaka"}],
        "subject": "Testing Email API",
        "text": "Hi Sakura. This is just a test from Priya.",
    }
)

print(email)
```

## Queue An Email

MailChannels has a first-class asynchronous processing endpoint. Use `queue` to
submit to `/send-async` and return as soon as MailChannels accepts the request.

```python
queued = mailchannels.Emails.queue(
    {
        "from": {"email": "sender@example.com"},
        "to": [{"email": "recipient@example.net"}],
        "subject": "Queued message",
        "html": "<strong>Hello</strong>",
    }
)
```

## Async Python

```python
import asyncio
import mailchannels

mailchannels.api_key = "YOUR-API-KEY"


async def main() -> None:
    queued = await mailchannels.Emails.queue_async(
        {
            "from": {"email": "sender@example.com"},
            "to": [{"email": "recipient@example.net"}],
            "subject": "Queued message",
            "text": "Hello",
        }
    )
    print(queued)


asyncio.run(main())
```

## Sub-Accounts

Sub-account management is a top-level SDK concern because it is a core
MailChannels feature.

```python
sub_account = mailchannels.SubAccounts.create(
    company_name="Client A",
    handle="clienta",
)

api_key = mailchannels.SubAccounts.ApiKeys.create("clienta")
mailchannels.SubAccounts.Limits.set("clienta", monthly_limit=100_000)
usage = mailchannels.SubAccounts.retrieve_usage("clienta")
```

Use a separate client when sending with a sub-account API key:

```python
client = mailchannels.Client(api_key="SUB-ACCOUNT-API-KEY")
client.emails.queue(
    {
        "from": {"email": "sender@client.example"},
        "to": [{"email": "recipient@example.net"}],
        "subject": "Client message",
        "text": "Hello",
    }
)
```

## Development

```bash
uv sync --extra async --extra dev
uv run pytest
```

Current uv releases do not expose `uv pytest` as a native subcommand; use
`uv run pytest` for the portable pytest harness.

Run the suite in SmolVM before committing:

```bash
tar --exclude .venv --exclude .git -cf /tmp/mailchannels-python-sdk.tar .
smolvm machine create mc-sdk-tests --net --image python:3.13-slim
smolvm machine start --name mc-sdk-tests
smolvm machine cp /tmp/mailchannels-python-sdk.tar mc-sdk-tests:/workspace/mailchannels-python-sdk.tar
smolvm machine exec --name mc-sdk-tests -- sh -lc 'cd /workspace && mkdir -p mailchannels-python-sdk && tar -xf mailchannels-python-sdk.tar -C mailchannels-python-sdk && cd mailchannels-python-sdk && pip install uv && uv sync --extra async --extra dev && uv run pytest'
smolvm machine stop --name mc-sdk-tests
```

## License

MIT License. See [LICENSE](LICENSE).
