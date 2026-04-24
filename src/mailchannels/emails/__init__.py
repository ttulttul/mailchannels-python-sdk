"""Email resource exports."""

from .emails import Emails, EmailsResource, normalize_email_params
from .types import (
    Attachment,
    AttachmentDict,
    Content,
    ContentDict,
    EmailAddress,
    EmailAddressDict,
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
    "EmailParams",
    "Emails",
    "EmailsResource",
    "Personalization",
    "PersonalizationDict",
    "QueuedSendResponse",
    "SendParams",
    "SendResponse",
    "normalize_email_params",
]
