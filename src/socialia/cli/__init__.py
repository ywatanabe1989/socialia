#!/usr/bin/env python3
"""
Socialia CLI - Unified social media management from command line.

Usage:
    socialia post twitter "Hello World!"
    socialia delete twitter 1234567890
    socialia thread twitter --file thread.txt
    socialia status
    socialia mcp run
    socialia --help
"""

import argparse
import sys
from pathlib import Path

from .. import __version__
from ._commands import (
    cmd_post,
    cmd_delete,
    cmd_thread,
    cmd_analytics,
    cmd_status,
    cmd_mcp,
    cmd_setup,
)
from ._feed_commands import (
    cmd_feed,
    cmd_check,
    cmd_me,
)

PLATFORMS = ["twitter", "linkedin", "reddit", "youtube"]


def _get_epilog() -> str:
    """Generate epilog with branded env var names."""
    from .._branding import get_env_var_name

    return f"""
Examples:
  socialia post twitter "Hello World!"
  socialia post twitter --file tweet.txt
  socialia delete twitter 1234567890
  socialia thread twitter --file thread.txt
  socialia status
  socialia mcp run
  socialia --help-recursive

Environment Variables:
  {get_env_var_name("X_CONSUMER_KEY"):36} Twitter API consumer key
  {get_env_var_name("X_CONSUMER_KEY_SECRET"):36} Twitter API consumer secret
  {get_env_var_name("X_ACCESSTOKEN"):36} Twitter access token
  {get_env_var_name("X_ACCESSTOKEN_SECRET"):36} Twitter access token secret
  {get_env_var_name("LINKEDIN_ACCESS_TOKEN"):36} LinkedIn OAuth access token
  {get_env_var_name("REDDIT_CLIENT_ID"):36} Reddit app client ID
  {get_env_var_name("REDDIT_CLIENT_SECRET"):36} Reddit app client secret
  {get_env_var_name("REDDIT_USERNAME"):36} Reddit username
  {get_env_var_name("REDDIT_PASSWORD"):36} Reddit password
  {get_env_var_name("GOOGLE_ANALYTICS_MEASUREMENT_ID"):36} Google Analytics measurement ID
  {get_env_var_name("GOOGLE_ANALYTICS_API_SECRET"):36} Google Analytics API secret
"""


def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser with all subcommands."""
    parser = argparse.ArgumentParser(
        prog="socialia",
        description="Unified social media management CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=_get_epilog(),
    )
    parser.add_argument(
        "-v", "--version", action="version", version=f"%(prog)s {__version__}"
    )
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    parser.add_argument(
        "--help-recursive", action="store_true", help="Show help for all commands"
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # post command
    post_parser = subparsers.add_parser(
        "post",
        help="Post content to a platform",
        description="Post content to a social media platform",
    )
    post_parser.add_argument("platform", choices=PLATFORMS, help="Target platform")
    post_parser.add_argument("text", nargs="?", help="Content to post")
    post_parser.add_argument("-f", "--file", type=Path, help="Read content from file")
    post_parser.add_argument("--reply-to", help="Post ID to reply to (Twitter)")
    post_parser.add_argument("--quote", help="Post ID to quote (Twitter)")
    post_parser.add_argument(
        "--subreddit", "-s", default="test", help="Target subreddit (Reddit)"
    )
    post_parser.add_argument("--title", "-t", help="Post title (Reddit/YouTube)")
    post_parser.add_argument(
        "--video", "-V", type=Path, help="Video file path (YouTube)"
    )
    post_parser.add_argument("--thumbnail", type=Path, help="Thumbnail image (YouTube)")
    post_parser.add_argument("--tags", help="Comma-separated tags (YouTube)")
    post_parser.add_argument(
        "--privacy",
        choices=["public", "private", "unlisted"],
        default="public",
        help="Privacy status (YouTube)",
    )
    post_parser.add_argument(
        "-n", "--dry-run", action="store_true", help="Print without posting"
    )

    # delete command
    delete_parser = subparsers.add_parser(
        "delete", help="Delete a post", description="Delete a post by ID"
    )
    delete_parser.add_argument("platform", choices=PLATFORMS, help="Target platform")
    delete_parser.add_argument("post_id", help="Post ID to delete")

    # thread command
    thread_parser = subparsers.add_parser(
        "thread", help="Post a thread", description="Post a thread of connected posts"
    )
    thread_parser.add_argument("platform", choices=PLATFORMS, help="Target platform")
    thread_parser.add_argument(
        "-f",
        "--file",
        type=Path,
        required=True,
        help="File with thread content (separate posts with ---)",
    )
    thread_parser.add_argument(
        "-n", "--dry-run", action="store_true", help="Print without posting"
    )

    # analytics command
    analytics_parser = subparsers.add_parser(
        "analytics",
        help="Google Analytics operations",
        description="Track events and retrieve analytics data",
    )
    analytics_sub = analytics_parser.add_subparsers(
        dest="analytics_command", help="Analytics operations"
    )

    track_parser = analytics_sub.add_parser(
        "track",
        help="Track a custom event",
        description="Send event to Google Analytics",
    )
    track_parser.add_argument("event_name", help="Event name")
    track_parser.add_argument(
        "--param",
        "-p",
        action="append",
        nargs=2,
        metavar=("KEY", "VALUE"),
        help="Event parameter (can be repeated)",
    )

    analytics_sub.add_parser(
        "realtime",
        help="Get realtime active users",
        description="Query realtime user count",
    )

    pageviews_parser = analytics_sub.add_parser(
        "pageviews", help="Get page view metrics", description="Query page view data"
    )
    pageviews_parser.add_argument("--start", default="7daysAgo", help="Start date")
    pageviews_parser.add_argument("--end", default="today", help="End date")
    pageviews_parser.add_argument("--path", help="Filter by page path")

    sources_parser = analytics_sub.add_parser(
        "sources",
        help="Get traffic sources",
        description="Query traffic source breakdown",
    )
    sources_parser.add_argument("--start", default="7daysAgo", help="Start date")
    sources_parser.add_argument("--end", default="today", help="End date")

    # status command
    subparsers.add_parser(
        "status",
        help="Show configuration and environment status",
        description="Display current configuration and environment variable status",
    )

    # mcp command
    mcp_parser = subparsers.add_parser(
        "mcp",
        help="MCP server commands",
        description="Model Context Protocol server operations",
    )
    mcp_sub = mcp_parser.add_subparsers(dest="mcp_command", help="MCP operations")
    mcp_sub.add_parser(
        "run", help="Run the MCP server", description="Start the MCP server"
    )
    mcp_sub.add_parser(
        "info",
        help="Show MCP server info",
        description="Display MCP server information",
    )

    # setup command
    setup_parser = subparsers.add_parser(
        "setup",
        help="Show platform setup instructions",
        description="Display API setup guide for platforms",
    )
    setup_parser.add_argument(
        "platform",
        nargs="?",
        choices=["twitter", "linkedin", "reddit", "youtube", "analytics", "all"],
        default="all",
        help="Platform to show setup for (default: all)",
    )

    # feed command - READ recent posts
    feed_parser = subparsers.add_parser(
        "feed",
        help="Get recent posts from platforms",
        description="Fetch and display recent posts from configured platforms",
    )
    feed_parser.add_argument(
        "platform",
        nargs="?",
        choices=PLATFORMS,
        help="Platform to check (default: all configured)",
    )
    feed_parser.add_argument(
        "-l", "--limit", type=int, default=5, help="Number of posts per platform"
    )
    feed_parser.add_argument(
        "-m", "--mentions", action="store_true", help="Show mentions instead of posts"
    )

    # check command - verify connections
    check_parser = subparsers.add_parser(
        "check",
        help="Verify connections to all platforms",
        description="Test API connections and show account info",
    )
    check_parser.add_argument(
        "platform",
        nargs="?",
        choices=PLATFORMS,
        help="Platform to check (default: all)",
    )

    # me command - get user info
    me_parser = subparsers.add_parser(
        "me",
        help="Get authenticated user info",
        description="Display user profile information for a platform",
    )
    me_parser.add_argument("platform", choices=PLATFORMS, help="Target platform")

    return parser


def cmd_help_recursive(parser: argparse.ArgumentParser) -> int:
    """Show help for all commands."""
    print("=" * 60)
    print("SOCIALIA - Complete Command Reference")
    print("=" * 60)
    print()

    parser.print_help()
    print()

    for action in parser._subparsers._actions:
        if isinstance(action, argparse._SubParsersAction):
            for name, subparser in action.choices.items():
                print("-" * 60)
                print(f"Command: {name}")
                print("-" * 60)
                subparser.print_help()
                print()

    return 0


def main(argv: list[str] = None) -> int:
    """Main entry point."""
    parser = create_parser()
    args = parser.parse_args(argv)

    if args.help_recursive:
        return cmd_help_recursive(parser)

    if args.command is None:
        parser.print_help()
        return 0

    if args.command == "post":
        return cmd_post(args, output_json=args.json)
    elif args.command == "delete":
        return cmd_delete(args, output_json=args.json)
    elif args.command == "thread":
        return cmd_thread(args, output_json=args.json)
    elif args.command == "analytics":
        return cmd_analytics(args, output_json=args.json)
    elif args.command == "status":
        return cmd_status(output_json=args.json)
    elif args.command == "mcp":
        return cmd_mcp(args)
    elif args.command == "setup":
        return cmd_setup(args)
    elif args.command == "feed":
        return cmd_feed(args, output_json=args.json)
    elif args.command == "check":
        return cmd_check(args, output_json=args.json)
    elif args.command == "me":
        return cmd_me(args, output_json=args.json)
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
