"""DKIM resource exports."""

from .dkim import Dkim, DkimResource
from .types import (
    DkimAlgorithm,
    DkimCreateParams,
    DkimDnsRecord,
    DkimKeyInfo,
    DkimKeyList,
    DkimKeyStatus,
    DkimListParams,
    DkimRotateResponse,
    DkimUpdateStatus,
)

__all__ = [
    "Dkim",
    "DkimAlgorithm",
    "DkimCreateParams",
    "DkimDnsRecord",
    "DkimKeyInfo",
    "DkimKeyList",
    "DkimKeyStatus",
    "DkimListParams",
    "DkimResource",
    "DkimRotateResponse",
    "DkimUpdateStatus",
]
