#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Timestamp: 2026-01-27
# File: src/socialia/_mcp/tools/analytics.py

"""Analytics MCP tools for Google Analytics."""

from __future__ import annotations

from typing import Optional

from fastmcp import FastMCP

from ..handlers import analytics_pageviews as _analytics_pageviews
from ..handlers import analytics_realtime as _analytics_realtime
from ..handlers import analytics_sources as _analytics_sources
from ..handlers import analytics_track as _analytics_track


def register_tools(mcp: FastMCP) -> None:
    """Register analytics tools."""

    @mcp.tool()
    def social_analytics_track(
        event_name: str,
        params: Optional[dict] = None,
    ) -> dict:
        """[social] Track custom event in Google Analytics. CLI: socialia analytics track <event_name>"""
        return _analytics_track(event_name, params)

    @mcp.tool()
    def social_analytics_pageviews(
        start_date: str = "7daysAgo",
        end_date: str = "today",
        path: Optional[str] = None,
    ) -> dict:
        """[social] Get page view metrics from Google Analytics. CLI: socialia analytics pageviews"""
        return _analytics_pageviews(start_date, end_date, path)

    @mcp.tool()
    def social_analytics_sources(
        start_date: str = "7daysAgo",
        end_date: str = "today",
    ) -> dict:
        """[social] Get traffic sources from Google Analytics. CLI: socialia analytics sources"""
        return _analytics_sources(start_date, end_date)

    @mcp.tool()
    def social_analytics_realtime() -> dict:
        """[social] Get realtime active users from Google Analytics. CLI: socialia analytics realtime"""
        return _analytics_realtime()


# EOF
