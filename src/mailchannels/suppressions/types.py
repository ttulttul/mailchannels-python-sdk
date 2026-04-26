"""Suppression list request and response types."""

from __future__ import annotations

from typing import Literal, TypedDict

from pydantic import BaseModel, ConfigDict

SuppressionSource = Literal[
    "api",
    "unsubscribe_link",
    "list_unsubscribe",
    "hard_bounce",
    "spam_complaint",
]
SuppressionDeleteSource = Literal[
    "api",
    "unsubscribe_link",
    "list_unsubscribe",
    "hard_bounce",
    "spam_complaint",
    "all",
]
SuppressionType = Literal["transactional", "non-transactional"]


class SuppressionEntryParams(TypedDict, total=False):
    """One suppression entry to create."""

    recipient: str
    suppression_types: list[SuppressionType]
    notes: str | None


class SuppressionEntry(BaseModel):
    """Suppression entry returned by MailChannels."""

    model_config = ConfigDict(extra="allow")

    recipient: str
    suppression_types: list[SuppressionType] | None = None
    notes: str | None = None
    source: SuppressionSource | None = None
    sender: str | None = None
    created_at: str | None = None


class SuppressionListResponse(BaseModel):
    """Response model for suppression list retrieval."""

    model_config = ConfigDict(extra="allow")

    suppression_list: list[SuppressionEntry]
