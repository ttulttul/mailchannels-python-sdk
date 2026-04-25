"""Email request and response types."""

from __future__ import annotations

import base64
import logging
import mimetypes
from pathlib import Path
from typing import Any, Literal, NotRequired, TypedDict
from urllib.parse import urlparse

import requests
from pydantic import BaseModel, ConfigDict, Field

from ..exceptions import MailChannelsError

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
    attachments: list[AttachmentDict | Attachment]
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

    @classmethod
    def from_bytes(
        cls,
        data: bytes,
        *,
        filename: str,
        content_type: str | None = None,
        disposition: str = "attachment",
        content_id: str | None = None,
    ) -> Attachment:
        """Build an attachment from bytes."""
        logger.debug(
            "Encoding MailChannels attachment from bytes filename=%s",
            filename,
        )
        return cls(
            content=_base64_content(data),
            filename=filename,
            type=content_type or _guess_content_type(filename),
            disposition=disposition,
            content_id=content_id,
        )

    @classmethod
    def from_file(
        cls,
        path: str | Path,
        *,
        filename: str | None = None,
        content_type: str | None = None,
        disposition: str = "attachment",
        content_id: str | None = None,
    ) -> Attachment:
        """Build an attachment from a local file."""
        file_path = Path(path)
        attachment_name = filename or file_path.name
        logger.info("Encoding MailChannels attachment from file path=%s", file_path)
        return cls.from_bytes(
            file_path.read_bytes(),
            filename=attachment_name,
            content_type=content_type or _guess_content_type(attachment_name),
            disposition=disposition,
            content_id=content_id,
        )

    @classmethod
    def from_url(
        cls,
        url: str,
        *,
        filename: str | None = None,
        content_type: str | None = None,
        disposition: str = "attachment",
        content_id: str | None = None,
        timeout: float = 30.0,
    ) -> Attachment:
        """Fetch a remote URL and build an attachment from its bytes."""
        logger.info("Fetching MailChannels attachment from URL url=%s", url)
        try:
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()
        except requests.RequestException as error:
            logger.error("Unable to fetch attachment URL url=%s error=%s", url, error)
            raise MailChannelsError(
                "Unable to fetch attachment URL.",
                code="AttachmentFetchError",
            ) from error

        attachment_name = filename or _filename_from_url(url)
        return cls.from_bytes(
            response.content,
            filename=attachment_name,
            content_type=content_type
            or _content_type_from_header(response.headers.get("Content-Type"))
            or _guess_content_type(attachment_name),
            disposition=disposition,
            content_id=content_id,
        )

    @classmethod
    def inline_file(
        cls,
        path: str | Path,
        *,
        content_id: str,
        filename: str | None = None,
        content_type: str | None = None,
    ) -> Attachment:
        """Build an inline attachment from a local file."""
        return cls.from_file(
            path,
            filename=filename,
            content_type=content_type,
            disposition="inline",
            content_id=content_id,
        )


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


def _base64_content(data: bytes) -> str:
    """Return Base64-encoded attachment content."""
    return base64.b64encode(data).decode("ascii")


def _guess_content_type(filename: str) -> str:
    """Infer a MIME type for an attachment filename."""
    return mimetypes.guess_type(filename)[0] or "application/octet-stream"


def _filename_from_url(url: str) -> str:
    """Infer an attachment filename from a URL path."""
    parsed = urlparse(url)
    return Path(parsed.path).name or "attachment"


def _content_type_from_header(value: str | None) -> str | None:
    """Extract a MIME type from a Content-Type header."""
    if value is None:
        return None
    return value.split(";", maxsplit=1)[0].strip() or None
