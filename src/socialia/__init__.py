"""Socialia - Unified social media management: posting, analytics, and insights."""

__version__ = "0.1.5"

from .base import BasePoster
from .twitter import Twitter
from .linkedin import LinkedIn
from .reddit import Reddit
from .analytics import GoogleAnalytics
from .youtube import YouTube

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
    "YouTube",
    "GoogleAnalytics",
    # Backward compatibility aliases
    "TwitterPoster",
    "LinkedInPoster",
    "RedditPoster",
    "YouTubePoster",
    # Version
    "__version__",
]
