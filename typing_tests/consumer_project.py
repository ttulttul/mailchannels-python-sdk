"""Consumer typing fixture for the public MailChannels SDK API."""

from __future__ import annotations

from typing_extensions import reveal_type

import mailchannels
from mailchannels import Client, InvalidRequestError, RateLimitError, ServerError
from mailchannels.emails import Content, EmailAddress, EmailParams, Personalization

client = Client(api_key="test-key")
params = EmailParams.model_validate(
    {
        "from": EmailAddress(email="sender@example.com"),
        "personalizations": [
            Personalization(to=[EmailAddress(email="recipient@example.net")])
        ],
        "subject": "Hello",
        "content": [Content(type="text/plain", value="Hi")],
    }
)

queued = client.emails.queue(params)
sent = mailchannels.Emails.send(params, dry_run=True)
domain_result = client.check_domain.check("example.com")
usage = client.usage.retrieve()
rate_limit_error = RateLimitError("Slow down")
invalid_request_error = InvalidRequestError("Bad request")
server_error = ServerError("Server failed")

reveal_type(client)
reveal_type(params)
reveal_type(queued)
reveal_type(sent)
reveal_type(domain_result)
reveal_type(usage)
reveal_type(rate_limit_error)
reveal_type(invalid_request_error)
reveal_type(server_error)
