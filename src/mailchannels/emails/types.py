"""Email request and response types."""

from __future__ import annotations

import logging
from typing import Any, Literal, NotRequired, TypedDict

from pydantic import BaseModel, ConfigDict, Field

logger = logging.getLogger(__name__)


class EmailAddressDict(TypedDict, total=False):
    """Dictionary form of a MailChannels email address."""

    email: str
    name: str


class ContentDict(TypedDict):
    """Dictionary form of a MailChannels content part."""

    type: str
    value: str


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
    headers: NotRequired[dict[str, str]]
    substitutions: NotRequired[dict[str, str]]


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
    headers: dict[str, str]
    attachments: list[AttachmentDict]


class EmailAddress(BaseModel):
    """Email address used for senders and recipients."""

    model_config = ConfigDict(populate_by_name=True)

    email: str
    name: str | None = None


class Content(BaseModel):
    """Email body content part."""

    type: Literal["text/plain", "text/html"] | str
    value: str


class Attachment(BaseModel):
    """Email attachment encoded for the MailChannels API."""

    content: str
    filename: str
    type: str | None = None
    disposition: str | None = None
    content_id: str | None = None


class Personalization(BaseModel):
    """Recipient-specific message customization."""

    to: list[EmailAddress] = Field(default_factory=list)
    cc: list[EmailAddress] | None = None
    bcc: list[EmailAddress] | None = None
    headers: dict[str, str] | None = None
    substitutions: dict[str, str] | None = None


class EmailParams(BaseModel):
    """Validated MailChannels email send payload."""

    model_config = ConfigDict(populate_by_name=True)

    personalizations: list[Personalization]
    from_: EmailAddress = Field(alias="from")
    subject: str
    content: list[Content]
    reply_to: EmailAddress | None = Field(default=None, alias="reply_to")
    headers: dict[str, str] | None = None
    attachments: list[Attachment] | None = None

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
