"""Email request and response types."""

from __future__ import annotations

import logging
from typing import Any, Literal, NotRequired, TypedDict

from pydantic import BaseModel, ConfigDict, Field

logger = logging.getLogger(__name__)

UNSUBSCRIBE_URL_PLACEHOLDER = "{{mc-unsubscribe-url}}"
EmailHeaders = dict[str, str]


class EmailAddressDict(TypedDict, total=False):
    """Dictionary form of a MailChannels email address."""

    email: str
    name: str


class ContentDict(TypedDict, total=False):
    """Dictionary form of a MailChannels content part."""

    type: str
    value: str
    template_type: Literal["mustache"]


class AttachmentDict(TypedDict, total=False):
    """Dictionary form of a MailChannels attachment."""

    content: str
    filename: str
    type: str
    disposition: str
    content_id: str


class PersonalizationDict(TypedDict, total=False):
    """Dictionary form of a MailChannels personalization."""

    to: list[EmailAddressDict]
    cc: NotRequired[list[EmailAddressDict]]
    bcc: NotRequired[list[EmailAddressDict]]
    subject: NotRequired[str]
    from_: NotRequired[EmailAddressDict]
    reply_to: NotRequired[EmailAddressDict]
    headers: NotRequired[EmailHeaders]
    substitutions: NotRequired[dict[str, str]]
    dynamic_template_data: NotRequired[dict[str, Any]]
    dkim_domain: NotRequired[str]
    dkim_private_key: NotRequired[str]
    dkim_selector: NotRequired[str]


class SendParams(TypedDict, total=False):
    """Resend-style or MailChannels-style email parameters."""

    from_: EmailAddressDict
    from_email: EmailAddressDict
    from_address: EmailAddressDict
    from_field: EmailAddressDict
    from_name: str
    from_display_name: str
    subject: str
    personalizations: list[PersonalizationDict]
    to: list[EmailAddressDict] | EmailAddressDict | list[str] | str
    cc: list[EmailAddressDict] | EmailAddressDict | list[str] | str
    bcc: list[EmailAddressDict] | EmailAddressDict | list[str] | str
    reply_to: EmailAddressDict | str
    content: list[ContentDict]
    text: str
    html: str
    headers: EmailHeaders
    attachments: list[AttachmentDict]
    transactional: bool
    dkim_domain: str
    dkim_private_key: str
    dkim_selector: str


class EmailAddress(BaseModel):
    """Email address used for senders and recipients."""

    model_config = ConfigDict(populate_by_name=True)

    email: str
    name: str | None = None


class Content(BaseModel):
    """Email body content part."""

    type: Literal["text/plain", "text/html"] | str
    value: str
    template_type: Literal["mustache"] | None = None


class Attachment(BaseModel):
    """Email attachment encoded for the MailChannels API."""

    content: str
    filename: str
    type: str | None = None
    disposition: str | None = None
    content_id: str | None = None


class Personalization(BaseModel):
    """Recipient-specific message customization."""

    model_config = ConfigDict(populate_by_name=True)

    to: list[EmailAddress] = Field(default_factory=list)
    cc: list[EmailAddress] | None = None
    bcc: list[EmailAddress] | None = None
    subject: str | None = None
    from_: EmailAddress | None = Field(default=None, alias="from")
    reply_to: EmailAddress | None = Field(default=None, alias="reply_to")
    headers: EmailHeaders | None = None
    substitutions: dict[str, str] | None = None
    dynamic_template_data: dict[str, Any] | None = None
    dkim_domain: str | None = None
    dkim_private_key: str | None = None
    dkim_selector: str | None = None


class EmailParams(BaseModel):
    """Validated MailChannels email send payload."""

    model_config = ConfigDict(populate_by_name=True)

    personalizations: list[Personalization]
    from_: EmailAddress = Field(alias="from")
    subject: str
    content: list[Content]
    reply_to: EmailAddress | None = Field(default=None, alias="reply_to")
    headers: EmailHeaders | None = None
    attachments: list[Attachment] | None = None
    transactional: bool | None = None
    dkim_domain: str | None = None
    dkim_private_key: str | None = None
    dkim_selector: str | None = None

    def to_payload(self) -> dict[str, Any]:
        """Convert this email model to a MailChannels API payload."""
        logger.debug("Serializing EmailParams subject=%s", self.subject)
        return self.model_dump(by_alias=True, exclude_none=True)


class SendResponse(BaseModel):
    """Response returned by MailChannels email send endpoints."""

    model_config = ConfigDict(extra="allow")


class QueuedSendResponse(BaseModel):
    """Response returned when MailChannels queues an email for async processing."""

    model_config = ConfigDict(extra="allow")
