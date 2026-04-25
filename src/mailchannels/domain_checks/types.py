"""Domain configuration check request and response types."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

DomainCheckVerdict = Literal["passed", "failed"]


class DkimSetting(BaseModel):
    """DKIM settings used by the domain check endpoint."""

    dkim_domain: str | None = None
    dkim_selector: str | None = None
    dkim_private_key: str | None = None


class CheckDomainParams(BaseModel):
    """Request body for `/check-domain`."""

    domain: str
    sender_id: str | None = None
    dkim_settings: list[DkimSetting | dict[str, str]] | None = Field(
        default=None,
        max_length=10,
    )


class DkimResult(BaseModel):
    """One DKIM result returned by the domain check endpoint."""

    model_config = ConfigDict(extra="allow")

    dkim_domain: str | None = None
    dkim_selector: str | None = None
    dkim_key_status: str | None = None
    reason: str | None = None
    verdict: DomainCheckVerdict | None = None


class LockdownResult(BaseModel):
    """Domain Lockdown check result."""

    model_config = ConfigDict(extra="allow")

    reason: str | None = None
    verdict: DomainCheckVerdict | None = None


class SpfResult(BaseModel):
    """SPF check result."""

    model_config = ConfigDict(extra="allow")

    reason: str | None = None
    spfRecord: str | None = None
    spfRecordError: str | None = None
    verdict: DomainCheckVerdict | None = None


class SenderDomainRecordResult(BaseModel):
    """A or MX record check result for sender-domain validation."""

    model_config = ConfigDict(extra="allow")

    reason: str | None = None
    verdict: DomainCheckVerdict | None = None


class SenderDomainResult(BaseModel):
    """Sender-domain DNS check result."""

    model_config = ConfigDict(extra="allow")

    a: SenderDomainRecordResult | None = None
    mx: SenderDomainRecordResult | None = None
    verdict: DomainCheckVerdict | None = None


class CheckResults(BaseModel):
    """Grouped check results returned by `/check-domain`."""

    model_config = ConfigDict(extra="allow")

    dkim: list[DkimResult] | None = None
    domain_lockdown: LockdownResult | None = None
    sender_domain: SenderDomainResult | None = None
    spf: SpfResult | None = None


class CheckDomainResult(BaseModel):
    """Domain configuration check response model."""

    model_config = ConfigDict(extra="allow")

    check_results: CheckResults | None = None
    references: list[str] | None = None
