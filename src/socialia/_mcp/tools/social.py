#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Timestamp: 2026-01-27
# File: src/socialia/_mcp/tools/social.py

"""Social media MCP tools."""

from __future__ import annotations

from typing import Literal, Optional

from fastmcp import FastMCP

from ..handlers import social_delete as _social_delete
from ..handlers import social_post as _social_post
from ..handlers import social_status as _social_status


def register_tools(mcp: FastMCP) -> None:
    """Register social media tools."""

    @mcp.tool()
    def social_post(
        platform: Literal["twitter", "linkedin", "reddit", "slack", "youtube"],
        text: str,
        reply_to: Optional[str] = None,
        dry_run: bool = False,
    ) -> dict:
        """
        Post content to social media. CLI: socialia post <platform> <text>

        PLATFORM STRATEGIES:
        - twitter: 280 chars. Hook first, not announcements. 1-2 hashtags at end.
        - linkedin: 3000 chars. First 2 lines critical. Short paragraphs. End with question.
        - reddit: Title is key. Value first, self-promo last. Check subreddit rules.
        - slack: Use channel mentions @here/@channel sparingly. Code blocks for technical content.
        - youtube: Keyword-rich title <60 chars. First 2 description lines shown in search.
        """
        return _social_post(platform, text, reply_to, dry_run)

    @mcp.tool()
    def social_delete(
        platform: Literal["twitter", "linkedin", "reddit", "slack", "youtube"],
        post_id: str,
    ) -> dict:
        """Delete a social media post. CLI: socialia delete <platform> <post_id>"""
        return _social_delete(platform, post_id)

    @mcp.tool()
    def social_status(
        platform: Literal["twitter", "linkedin", "reddit", "slack", "youtube"],
    ) -> dict:
        """Check authentication status for a platform. CLI: socialia status <platform>"""
        return _social_status(platform)


# EOF
