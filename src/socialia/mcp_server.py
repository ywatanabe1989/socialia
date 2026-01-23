#!/usr/bin/env python3
"""
Socialia MCP Server - Social Media Automation with Platform-Specific Strategies.

Provides MCP tools for posting to Twitter/X, LinkedIn, Reddit, and YouTube.
All MCP tool calls can be reproduced via CLI commands.

## PLATFORM CONTENT STRATEGIES

When composing posts, follow these platform-specific strategies for engagement:

### Twitter/X (280 chars)
- **Hook first**: Lead with curiosity, controversy, or value (not announcements)
- **Format**: Short sentences. Line breaks. Visual hierarchy.
- **Emoji**: Use at least 1 emoji per tweet for visual appeal (🔧 🚀 ✨ 💡 🎯)
- **Links**: ALWAYS include GitHub/project URL for discoverability
- **Hashtags**: 3-5 for SEO, ALWAYS at the end, never mid-sentence
  - Mix broad + specific for reach: #Python #OpenSource #DevTools #CLI #Automation
  - More hashtags = better discoverability on Twitter/X
- **Avoid**: "Just released", "Check out", "New version" - boring intros

BAD:  "SciTeX v2.15.0 released! New audio relay for remote AI agents. pip install scitex[audio] #Python #AI"
GOOD: "Your AI agent on a remote server can now speak to you locally.

Audio relay in SciTeX bridges the gap.

pip install scitex[audio]

#AIAgents #Python"

Templates:
- Problem → Solution: "Tired of X? Now you can Y. #hashtag"
- Curiosity gap: "The one thing most developers miss about X... #hashtag"
- Counter-intuitive: "Why X is actually better than Y #hashtag"
- Tutorial teaser: "How to X in 3 steps (thread): #hashtag"

### LinkedIn (3,000 chars)
- **Hook**: First 2 lines visible before "see more" - make them count
- **Format**: Short paragraphs (1-2 sentences). Lots of whitespace.
- **Tone**: Professional but human. Share learnings, not just announcements.
- **Hashtags**: 3-5 at the very end, after content. Use industry terms.
  - #ArtificialIntelligence #MachineLearning #SoftwareDevelopment #OpenSource #TechInnovation
- **CTA**: Ask a question or invite discussion at the end

BAD:  "Excited to announce SciTeX v2.15.0 with new audio features!"
GOOD: "Remote AI development has a UX problem.

When your agent runs on a server, you lose audio feedback entirely.

We solved this with audio relay - your remote agent speaks to your local machine.

Here's what we learned building it:
• Challenge 1...
• Challenge 2...

What's the biggest UX gap you face with remote AI tools?

#ArtificialIntelligence #RemoteDevelopment #Python #OpenSource"

### Reddit
- **Title is everything**: Descriptive, specific, follows subreddit culture
- **Body**: Provide value first. Self-promotion last (10:1 rule).
- **Tone**: Authentic, not corporate. Redditors detect marketing.
- **Subreddit rules**: Check sidebar before posting

BAD Title:  "Check out my new Python package!"
GOOD Title: "I built a Python tool that lets remote AI agents play audio on your local machine"

### YouTube
- **Title**: Keyword-rich, curiosity-driven, under 60 chars ideal
- **Description**: First 2 lines matter (shown in search). Keywords naturally.
- **Tags**: Relevant, mix of broad and specific

Environment Variables:
    SOCIALIA_ENV_FILE: Path to .env file to load (optional)
    Or set individual SOCIALIA_* env vars (see socialia setup)
"""

import os
import subprocess
import sys
import json
from pathlib import Path
from typing import Any


def load_env_file(env_file: str) -> None:
    """Load environment variables from a file."""
    path = Path(os.path.expandvars(env_file)).expanduser()
    if not path.exists():
        print(f"Warning: SOCIALIA_ENV_FILE not found: {path}", file=sys.stderr)
        return

    with open(path) as f:
        for line in f:
            line = line.strip()
            # Skip comments and empty lines
            if not line or line.startswith("#"):
                continue
            # Handle 'export VAR=value' or 'VAR=value'
            if line.startswith("export "):
                line = line[7:]
            if "=" in line:
                key, _, value = line.partition("=")
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                # Expand $HOME and other vars
                value = os.path.expandvars(value)
                os.environ[key] = value


# Load env file if specified
if env_file := os.environ.get("SOCIALIA_ENV_FILE"):
    load_env_file(env_file)

try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import Tool, TextContent, Resource, TextResourceContents

    HAS_MCP = True
except ImportError:
    HAS_MCP = False


# Platform content strategies - exposed via MCP resource and tool descriptions
PLATFORM_STRATEGIES = """
## PLATFORM CONTENT STRATEGIES

### Twitter/X (280 chars)
- Hook first: Lead with curiosity, controversy, or value (NOT announcements)
- Format: Short sentences. Line breaks. Visual hierarchy.
- Hashtags: 1-2 at the END. Niche > generic (#AIAgents not #AI)
  - Tech: #Python #OpenSource #DevTools #MachineLearning #AIAgents
- Avoid: "Just released", "Check out", "New version"

BAD:  "SciTeX v2.15.0 released! New audio relay. pip install scitex[audio] #Python #AI"
GOOD: "Your AI agent on a remote server can now speak to you locally.

Audio relay in SciTeX bridges the gap.

pip install scitex[audio]

#AIAgents #Python"

### LinkedIn (3,000 chars)
- Hook: First 2 lines visible before "see more" - make them count
- Format: Short paragraphs. Lots of whitespace.
- Hashtags: 3-5 at the END. Industry terms.
  - #ArtificialIntelligence #MachineLearning #SoftwareDevelopment #OpenSource
- CTA: End with a question

### Reddit
- Title is everything: Descriptive, specific, subreddit culture
- NO hashtags. Authentic tone. Value first, self-promo last.

### YouTube
- Title: Keyword-rich, <60 chars, curiosity-driven
- Hashtags: 3-5 in description
"""


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

    @server.list_resources()
    async def list_resources() -> list[Resource]:
        """List available resources."""
        return [
            Resource(
                uri="socialia://strategies",
                name="Platform Content Strategies",
                description="Content strategies for Twitter, LinkedIn, Reddit, YouTube",
                mimeType="text/plain",
            ),
        ]

    @server.read_resource()
    async def read_resource(uri: str) -> str:
        """Read a resource by URI."""
        if uri == "socialia://strategies":
            return PLATFORM_STRATEGIES
        raise ValueError(f"Unknown resource: {uri}")

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        """List available tools."""
        return [
            Tool(
                name="social_post",
                description=(
                    "Post content to social media. CLI: socialia post <platform> <text>\n\n"
                    "PLATFORM STRATEGIES:\n"
                    "- twitter: 280 chars. Hook first, not announcements. 1-2 hashtags at end.\n"
                    "- linkedin: 3000 chars. First 2 lines critical. Short paragraphs. End with question.\n"
                    "- reddit: Title is key. Value first, self-promo last. Check subreddit rules.\n"
                    "- youtube: Keyword-rich title <60 chars. First 2 description lines shown in search."
                ),
                inputSchema={
                    "type": "object",
                    "properties": {
                        "platform": {
                            "type": "string",
                            "enum": ["twitter", "linkedin", "reddit", "youtube"],
                            "description": (
                                "Target platform. "
                                "twitter=280 chars, hook-driven; "
                                "linkedin=professional, whitespace; "
                                "reddit=community-first; "
                                "youtube=SEO-focused"
                            ),
                        },
                        "text": {
                            "type": "string",
                            "description": "Content to post. Follow platform strategy from module docstring.",
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
            Tool(
                name="analytics_realtime",
                description="Get realtime active users from Google Analytics. CLI: socialia analytics realtime",
                inputSchema={
                    "type": "object",
                    "properties": {},
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

        elif name == "analytics_realtime":
            result = run_cli("analytics", "realtime")

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
