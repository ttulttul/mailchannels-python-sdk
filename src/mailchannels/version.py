"""Version metadata for the MailChannels SDK."""

from __future__ import annotations

__version__ = "0.1.0"


def get_version() -> str:
    """Return the installed MailChannels SDK version string."""
    return __version__


def user_agent() -> str:
    """Return the SDK User-Agent header value."""
    return f"mailchannels-python/{get_version()}"
