"""Socialia - Unified social media management: posting, analytics, and insights."""

__version__ = "0.3.3"

from .base import BasePoster
from .twitter import Twitter
from .linkedin import LinkedIn
from .reddit import Reddit
from .slack import Slack
from .analytics import GoogleAnalytics
from .youtube import YouTube
from .org import OrgParser, OrgDraft, OrgDraftManager
from .org_files import move_to_scheduled, move_to_posted, ensure_project_dirs
from ._server import PLATFORM_STRATEGIES

# Backward compatibility aliases
TwitterPoster = Twitter
LinkedInPoster = LinkedIn
RedditPoster = Reddit
YouTubePoster = YouTube

__all__ = [
    # Base
    "BasePoster",
    # Platform clients (new names)
    "Twitter",
    "LinkedIn",
    "Reddit",
    "Slack",
    "YouTube",
    "GoogleAnalytics",
    # Org mode
    "OrgParser",
    "OrgDraft",
    "OrgDraftManager",
    # File management
    "move_to_scheduled",
    "move_to_posted",
    "ensure_project_dirs",
    # Backward compatibility aliases
    "TwitterPoster",
    "LinkedInPoster",
    "RedditPoster",
    "YouTubePoster",
    # MCP/Content strategies
    "PLATFORM_STRATEGIES",
    # Version
    "__version__",
]
