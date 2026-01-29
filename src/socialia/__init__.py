"""Socialia - Unified social media management: posting, analytics, and insights."""

__version__ = "0.4.0"

from .twitter import Twitter
from .linkedin import LinkedIn
from .reddit import Reddit
from .slack import Slack
from .analytics import GoogleAnalytics
from .youtube import YouTube
from .org_files import move_to_scheduled, move_to_posted, ensure_project_dirs
from ._server import PLATFORM_STRATEGIES

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

# Clean up module namespace - hide internal submodules
del twitter, linkedin, reddit, slack, analytics, youtube, org_files, _server
