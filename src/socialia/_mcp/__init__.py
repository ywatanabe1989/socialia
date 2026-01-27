#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Timestamp: 2026-01-27
# File: src/socialia/_mcp/__init__.py

"""
Socialia MCP module.

Provides register_all_tools for thin wrapper delegation.
For mcp instance and run_server, import from socialia._server directly.
"""

from .tools import register_all_tools

__all__ = [
    "register_all_tools",
]

# EOF
