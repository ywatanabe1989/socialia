#!/usr/bin/env python3
"""
Socialia MCP Server.

Provides MCP tools that delegate to CLI commands for reproducibility.
All MCP tool calls can be reproduced via CLI commands.
"""

import subprocess
import sys
import json
from typing import Any

try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import Tool, TextContent

    HAS_MCP = True
except ImportError:
    HAS_MCP = False


def run_cli(*args: str) -> dict[str, Any]:
    """
    Run socialia CLI command and return result.

    This ensures all MCP operations are reproducible via CLI.
    """
    cmd = [sys.executable, "-m", "socialia.cli", "--json", *args]
    result = subprocess.run(cmd, capture_output=True, text=True)

    cli_command = f"socialia {' '.join(args)}"

    if result.returncode == 0:
        try:
            data = json.loads(result.stdout)
            data["cli_command"] = cli_command
            return data
        except json.JSONDecodeError:
            return {
                "success": True,
                "output": result.stdout,
                "cli_command": cli_command,
            }
    else:
        return {
            "success": False,
            "error": result.stderr or result.stdout,
            "cli_command": cli_command,
        }


def create_server() -> "Server":
    """Create and configure the MCP server."""
    if not HAS_MCP:
        raise ImportError("MCP package not installed. Run: pip install mcp")

    server = Server("socialia")

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        """List available tools."""
        return [
            Tool(
                name="social_post",
                description="Post content to social media. CLI: socialia post <platform> <text>",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "platform": {
                            "type": "string",
                            "enum": ["twitter", "linkedin", "reddit", "youtube"],
                            "description": "Target platform",
                        },
                        "text": {
                            "type": "string",
                            "description": "Content to post",
                        },
                        "reply_to": {
                            "type": "string",
                            "description": "Post ID to reply to (optional)",
                        },
                        "dry_run": {
                            "type": "boolean",
                            "description": "Preview without posting",
                            "default": False,
                        },
                    },
                    "required": ["platform", "text"],
                },
            ),
            Tool(
                name="social_delete",
                description="Delete a social media post. CLI: socialia delete <platform> <post_id>",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "platform": {
                            "type": "string",
                            "enum": ["twitter", "linkedin", "reddit", "youtube"],
                            "description": "Target platform",
                        },
                        "post_id": {
                            "type": "string",
                            "description": "Post ID to delete",
                        },
                    },
                    "required": ["platform", "post_id"],
                },
            ),
            Tool(
                name="analytics_track",
                description="Track custom event in Google Analytics. CLI: socialia analytics track <event_name>",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "event_name": {
                            "type": "string",
                            "description": "Event name to track",
                        },
                        "params": {
                            "type": "object",
                            "description": "Event parameters (key-value pairs)",
                        },
                    },
                    "required": ["event_name"],
                },
            ),
            Tool(
                name="analytics_pageviews",
                description="Get page view metrics from Google Analytics. CLI: socialia analytics pageviews",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "start_date": {
                            "type": "string",
                            "description": "Start date (YYYY-MM-DD or '7daysAgo')",
                            "default": "7daysAgo",
                        },
                        "end_date": {
                            "type": "string",
                            "description": "End date (YYYY-MM-DD or 'today')",
                            "default": "today",
                        },
                        "path": {
                            "type": "string",
                            "description": "Optional page path filter",
                        },
                    },
                },
            ),
            Tool(
                name="analytics_sources",
                description="Get traffic sources from Google Analytics. CLI: socialia analytics sources",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "start_date": {
                            "type": "string",
                            "description": "Start date (YYYY-MM-DD or '7daysAgo')",
                            "default": "7daysAgo",
                        },
                        "end_date": {
                            "type": "string",
                            "description": "End date (YYYY-MM-DD or 'today')",
                            "default": "today",
                        },
                    },
                },
            ),
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict) -> list[TextContent]:
        """Handle tool calls by delegating to CLI."""
        if name == "social_post":
            args = ["post", arguments["platform"], arguments["text"]]
            if arguments.get("reply_to"):
                args.extend(["--reply-to", arguments["reply_to"]])
            if arguments.get("dry_run"):
                args.append("--dry-run")
            result = run_cli(*args)

        elif name == "social_delete":
            result = run_cli("delete", arguments["platform"], arguments["post_id"])

        elif name == "analytics_track":
            args = ["analytics", "track", arguments["event_name"]]
            params = arguments.get("params", {})
            for key, value in params.items():
                args.extend(["--param", key, str(value)])
            result = run_cli(*args)

        elif name == "analytics_pageviews":
            args = ["analytics", "pageviews"]
            if arguments.get("start_date"):
                args.extend(["--start", arguments["start_date"]])
            if arguments.get("end_date"):
                args.extend(["--end", arguments["end_date"]])
            if arguments.get("path"):
                args.extend(["--path", arguments["path"]])
            result = run_cli(*args)

        elif name == "analytics_sources":
            args = ["analytics", "sources"]
            if arguments.get("start_date"):
                args.extend(["--start", arguments["start_date"]])
            if arguments.get("end_date"):
                args.extend(["--end", arguments["end_date"]])
            result = run_cli(*args)

        else:
            result = {"success": False, "error": f"Unknown tool: {name}"}

        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    return server


async def main():
    """Run the MCP server."""
    if not HAS_MCP:
        print("Error: MCP package not installed. Run: pip install mcp", file=sys.stderr)
        sys.exit(1)

    server = create_server()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream, write_stream, server.create_initialization_options()
        )


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
