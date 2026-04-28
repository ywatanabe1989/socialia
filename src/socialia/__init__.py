"""Socialia - Unified social media management: posting, analytics, and insights."""

try:
    from importlib.metadata import version as _v, PackageNotFoundError
    try:
        __version__ = _v("socialia")
    except PackageNotFoundError:
        __version__ = "0.0.0+local"
    del _v, PackageNotFoundError
except ImportError:  # pragma: no cover — only on ancient Pythons
    __version__ = "0.0.0+local"
from .twitter import Twitter
from .linkedin import LinkedIn
from .reddit import Reddit
from .slack import Slack
from .analytics import GoogleAnalytics
from .youtube import YouTube
from .org_files import move_to_scheduled, move_to_posted, ensure_project_dirs

try:
    from ._server import PLATFORM_STRATEGIES
except ImportError:
    PLATFORM_STRATEGIES = {}

__all__ = [
    # Platform clients
    "Twitter",
    "LinkedIn",
    "Reddit",
    "Slack",
    "YouTube",
    "GoogleAnalytics",
    # File management
    "move_to_scheduled",
    "move_to_posted",
    "ensure_project_dirs",
    # MCP/Content strategies
    "PLATFORM_STRATEGIES",
    # Version
    "__version__",
]
