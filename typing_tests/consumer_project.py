"""Consumer typing fixture for the public MailChannels SDK API."""

from __future__ import annotations

from typing_extensions import reveal_type

import mailchannels
from mailchannels import Client, InvalidRequestError, RateLimitError, ServerError
from mailchannels.emails import Content, EmailAddress, EmailParams, Personalization

client = Client(api_key="test-key")
strict_client = Client(api_key="test-key", strict_responses=True)
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
strict_queued = strict_client.emails.queue(params)
strict_sent = strict_client.emails.send(params, dry_run=True)
strict_domain_result = strict_client.check_domain.check("example.com")
strict_usage = strict_client.usage.retrieve()
strict_metrics = strict_client.metrics.volume()
strict_dkim = strict_client.dkim.create("example.com", selector="mcdkim")
strict_suppressions = strict_client.suppressions.list()
strict_webhook_key = strict_client.webhooks.public_key("mckey")
strict_webhook_validation = strict_client.webhooks.validate(request_id="req_123")
strict_sub_account = strict_client.sub_accounts.create(handle="clienta")
strict_sub_account_limit = strict_client.sub_accounts.limits.retrieve("clienta")
strict_api_key = strict_client.sub_accounts.api_keys.create("clienta")
strict_smtp_password = strict_client.sub_accounts.smtp_passwords.create("clienta")
rate_limit_error = RateLimitError("Slow down")
invalid_request_error = InvalidRequestError("Bad request")
server_error = ServerError("Server failed")

strict_request_id: str = strict_queued.request_id
strict_send_data: list[str] | None = strict_sent.data
strict_references: list[str] | None = strict_domain_result.references
strict_total_usage: int = strict_usage.total_usage
strict_processed: int = strict_metrics.processed
strict_dkim_selector: str = strict_dkim.selector
strict_suppression_count: int = len(strict_suppressions.suppression_list)
strict_key_id: str = strict_webhook_key.id
strict_validation_passed: bool = strict_webhook_validation.all_passed
strict_sub_account_handle: str | None = strict_sub_account.handle
strict_limit_sends: int | None = strict_sub_account_limit.sends

reveal_type(client)
reveal_type(strict_client)
reveal_type(params)
reveal_type(queued)
reveal_type(sent)
reveal_type(domain_result)
reveal_type(usage)
reveal_type(strict_queued)
reveal_type(strict_sent)
reveal_type(strict_domain_result)
reveal_type(strict_usage)
reveal_type(strict_metrics)
reveal_type(strict_dkim)
reveal_type(strict_suppressions)
reveal_type(strict_webhook_key)
reveal_type(strict_webhook_validation)
reveal_type(strict_sub_account)
reveal_type(strict_sub_account_limit)
reveal_type(strict_api_key)
reveal_type(strict_smtp_password)
reveal_type(rate_limit_error)
reveal_type(invalid_request_error)
reveal_type(server_error)
