"""Compatibility exports for the documented `/check-domain` endpoint."""

from mailchannels.domain_checks import (
    CheckDomain,
    CheckDomainParams,
    CheckDomainResource,
    CheckDomainResult,
    CheckResults,
    DkimResult,
    DkimSetting,
    DomainChecks,
    DomainChecksResource,
    DomainCheckVerdict,
    LockdownResult,
    SenderDomainResult,
    SpfResult,
)

__all__ = [
    "CheckDomain",
    "CheckDomainParams",
    "CheckDomainResource",
    "CheckDomainResult",
    "CheckResults",
    "DkimResult",
    "DkimSetting",
    "DomainCheckVerdict",
    "DomainChecks",
    "DomainChecksResource",
    "LockdownResult",
    "SenderDomainResult",
    "SpfResult",
]
