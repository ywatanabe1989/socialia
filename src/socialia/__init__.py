"""Socialia - Unified social media management: posting, analytics, and insights."""

__version__ = "0.1.1"

from .base import BasePoster
from .twitter import TwitterPoster
from .linkedin import LinkedInPoster
from .reddit import RedditPoster
from .analytics import GoogleAnalytics
from .youtube import YouTubePoster

__all__ = [
    "BasePoster",
    "TwitterPoster",
    "LinkedInPoster",
    "RedditPoster",
    "GoogleAnalytics",
    "YouTubePoster",
    "__version__",
]
