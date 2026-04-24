"""Email resource exports."""

from .emails import Emails, EmailsResource, normalize_email_params
from .types import (
    UNSUBSCRIBE_URL_PLACEHOLDER,
    Attachment,
    AttachmentDict,
    Content,
    ContentDict,
    EmailAddress,
    EmailAddressDict,
    EmailHeaders,
    EmailParams,
    Personalization,
    PersonalizationDict,
    QueuedSendResponse,
    SendParams,
    SendResponse,
)

__all__ = [
    "Attachment",
    "AttachmentDict",
    "Content",
    "ContentDict",
    "EmailAddress",
    "EmailAddressDict",
    "EmailHeaders",
    "EmailParams",
    "Emails",
    "EmailsResource",
    "Personalization",
    "PersonalizationDict",
    "QueuedSendResponse",
    "SendParams",
    "SendResponse",
    "UNSUBSCRIBE_URL_PLACEHOLDER",
    "normalize_email_params",
]
