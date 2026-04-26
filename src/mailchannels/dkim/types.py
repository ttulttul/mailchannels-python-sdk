"""DKIM request and response types."""

from __future__ import annotations

from typing import Literal, TypedDict

from pydantic import BaseModel, ConfigDict

DkimAlgorithm = Literal["rsa"]
DkimKeyStatus = Literal["active", "retired", "revoked", "rotated"]
DkimUpdateStatus = Literal["retired", "revoked", "rotated"]


class DkimCreateParams(TypedDict, total=False):
    """Parameters for creating a DKIM key pair."""

    selector: str
    algorithm: DkimAlgorithm
    key_length: int


class DkimListParams(TypedDict, total=False):
    """Query parameters for retrieving DKIM key pairs."""

    selector: str
    status: DkimKeyStatus
    offset: int
    limit: int
    include_dns_record: bool


class DkimDnsRecord(BaseModel):
    """Suggested DKIM DNS record returned by MailChannels."""

    model_config = ConfigDict(extra="allow")

    name: str
    type: str
    value: str


class DkimKeyInfo(BaseModel):
    """MailChannels-hosted DKIM key metadata."""

    model_config = ConfigDict(extra="allow")

    domain: str
    selector: str
    public_key: str
    status: DkimKeyStatus
    algorithm: str
    key_length: int | None = None
    dkim_dns_records: list[DkimDnsRecord] | None = None


class DkimKeyList(BaseModel):
    """Response model for listing MailChannels-hosted DKIM keys."""

    model_config = ConfigDict(extra="allow")

    keys: list[DkimKeyInfo]


class DkimRotateResponse(BaseModel):
    """Response model for DKIM key rotation."""

    model_config = ConfigDict(extra="allow")

    new_key: DkimKeyInfo
    rotated_key: DkimKeyInfo
