"""OpenAPI compatibility metadata for the MailChannels SDK."""

from __future__ import annotations

import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class ApiSpecCompatibility:
    """MailChannels OpenAPI document targeted by this SDK release."""

    source_url: str
    openapi_version: str
    sha256: str
    checked_at: str
    sdk_version: str

    def to_dict(self) -> dict[str, str]:
        """Return compatibility metadata as a plain dictionary."""
        logger.debug(
            "Serializing OpenAPI compatibility metadata for SDK %s.",
            self.sdk_version,
        )
        return {
            "source_url": self.source_url,
            "openapi_version": self.openapi_version,
            "sha256": self.sha256,
            "checked_at": self.checked_at,
            "sdk_version": self.sdk_version,
        }


API_SPEC_COMPATIBILITY = ApiSpecCompatibility(
    source_url="https://docs.mailchannels.net/email-api.yaml",
    openapi_version="0.21.0",
    sha256="f637ea36aa2c45b86bb88608e5a38d6c25bfd783e4368967456e32a293b0e0a9",
    checked_at="2026-04-26T19:12:40+00:00",
    sdk_version="0.1.0",
)
