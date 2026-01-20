#!/usr/bin/env python3
"""
Socialia CLI - Unified social media management from command line.

Usage:
    socialia post twitter "Hello World!"
    socialia delete twitter 1234567890
    socialia thread twitter --file thread.txt
    socialia --help
"""

import argparse
import sys
import json
from pathlib import Path

from . import __version__
from .twitter import TwitterPoster
from .linkedin import LinkedInPoster
from .reddit import RedditPoster
from .analytics import GoogleAnalytics
from .youtube import YouTubePoster


def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser with all subcommands."""
    parser = argparse.ArgumentParser(
        prog="socialia",
        description="Unified social media management CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  socialia post twitter "Hello World!"
  socialia post twitter --file tweet.txt
  socialia delete twitter 1234567890
  socialia thread twitter --file thread.txt
  socialia help-recursive

Environment Variables:
  SCITEX_X_CONSUMER_KEY         Twitter API consumer key
  SCITEX_X_CONSUMER_KEY_SECRET  Twitter API consumer secret
  SCITEX_X_ACCESSTOKEN          Twitter access token
  SCITEX_X_ACCESSTOKEN_SECRET   Twitter access token secret
  LINKEDIN_ACCESS_TOKEN         LinkedIn OAuth access token
  REDDIT_CLIENT_ID              Reddit app client ID
  REDDIT_CLIENT_SECRET          Reddit app client secret
  REDDIT_USERNAME               Reddit username
  REDDIT_PASSWORD               Reddit password
""",
    )
    parser.add_argument(
        "-v", "--version", action="version", version=f"%(prog)s {__version__}"
    )
    parser.add_argument("--json", action="store_true", help="Output results as JSON")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # post command
    post_parser = subparsers.add_parser(
        "post",
        help="Post content to a platform",
        description="Post content to a social media platform",
    )
    post_parser.add_argument("platform", choices=["twitter", "linkedin", "reddit", "youtube"], help="Target platform")
    post_parser.add_argument("text", nargs="?", help="Content to post")
    post_parser.add_argument("-f", "--file", type=Path, help="Read content from file")
    post_parser.add_argument("--reply-to", help="Post ID to reply to (Twitter)")
    post_parser.add_argument("--quote", help="Post ID to quote (Twitter)")
    post_parser.add_argument("--subreddit", "-s", default="test", help="Target subreddit (Reddit)")
    post_parser.add_argument("--title", "-t", help="Post title (Reddit/YouTube)")
    post_parser.add_argument("--video", "-V", type=Path, help="Video file path (YouTube)")
    post_parser.add_argument("--thumbnail", type=Path, help="Thumbnail image (YouTube)")
    post_parser.add_argument("--tags", help="Comma-separated tags (YouTube)")
    post_parser.add_argument("--privacy", choices=["public", "private", "unlisted"], default="public", help="Privacy status (YouTube)")
    post_parser.add_argument(
        "-n", "--dry-run", action="store_true", help="Print without posting"
    )

    # delete command
    delete_parser = subparsers.add_parser(
        "delete", help="Delete a post", description="Delete a post by ID"
    )
    delete_parser.add_argument("platform", choices=["twitter", "linkedin", "reddit", "youtube"], help="Target platform")
    delete_parser.add_argument("post_id", help="Post ID to delete")

    # thread command
    thread_parser = subparsers.add_parser(
        "thread", help="Post a thread", description="Post a thread of connected posts"
    )
    thread_parser.add_argument("platform", choices=["twitter", "linkedin", "reddit", "youtube"], help="Target platform")
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
    analytics_sub = analytics_parser.add_subparsers(dest="analytics_command", help="Analytics operations")

    # analytics track
    track_parser = analytics_sub.add_parser(
        "track", help="Track a custom event", description="Send event to Google Analytics"
    )
    track_parser.add_argument("event_name", help="Event name")
    track_parser.add_argument("--param", "-p", action="append", nargs=2, metavar=("KEY", "VALUE"),
                              help="Event parameter (can be repeated)")

    # analytics realtime
    analytics_sub.add_parser(
        "realtime", help="Get realtime active users", description="Query realtime user count"
    )

    # analytics pageviews
    pageviews_parser = analytics_sub.add_parser(
        "pageviews", help="Get page view metrics", description="Query page view data"
    )
    pageviews_parser.add_argument("--start", default="7daysAgo", help="Start date (default: 7daysAgo)")
    pageviews_parser.add_argument("--end", default="today", help="End date (default: today)")
    pageviews_parser.add_argument("--path", help="Filter by page path")

    # analytics sources
    sources_parser = analytics_sub.add_parser(
        "sources", help="Get traffic sources", description="Query traffic source breakdown"
    )
    sources_parser.add_argument("--start", default="7daysAgo", help="Start date (default: 7daysAgo)")
    sources_parser.add_argument("--end", default="today", help="End date (default: today)")

    # help-recursive command
    subparsers.add_parser(
        "help-recursive",
        help="Show help for all commands",
        description="Display comprehensive help for all commands and subcommands",
    )

    return parser


def get_poster(platform: str):
    """Get poster instance for platform."""
    if platform == "twitter":
        return TwitterPoster()
    elif platform == "linkedin":
        return LinkedInPoster()
    elif platform == "reddit":
        return RedditPoster()
    elif platform == "youtube":
        return YouTubePoster()
    else:
        raise ValueError(f"Unsupported platform: {platform}")


def cmd_post(args, output_json: bool = False) -> int:
    """Handle post command."""
    # Get text content
    if args.file:
        if not args.file.exists():
            print(f"Error: File not found: {args.file}", file=sys.stderr)
            return 1
        text = args.file.read_text().strip()
    elif args.text:
        text = args.text
    else:
        print("Error: Provide text or --file", file=sys.stderr)
        return 1

    # Dry run
    if args.dry_run:
        print("=== DRY RUN ===")
        print(f"Platform: {args.platform}")
        if args.platform == "reddit":
            print(f"Subreddit: r/{getattr(args, 'subreddit', 'test')}")
            title = getattr(args, "title", None) or text.split("\n")[0][:100]
            print(f"Title: {title}")
        elif args.platform == "youtube":
            video = getattr(args, "video", None)
            print(f"Video: {video or 'None (community post)'}")
            print(f"Title: {getattr(args, 'title', None) or text.split(chr(10))[0][:100]}")
            print(f"Privacy: {getattr(args, 'privacy', 'public')}")
        print(
            f"Text ({len(text)} chars): {text[:100]}{'...' if len(text) > 100 else ''}"
        )
        return 0

    # Post
    poster = get_poster(args.platform)
    if args.platform == "twitter":
        result = poster.post(
            text,
            reply_to=getattr(args, "reply_to", None),
            quote_tweet_id=getattr(args, "quote", None),
        )
    elif args.platform == "reddit":
        result = poster.post(
            text,
            subreddit=getattr(args, "subreddit", "test"),
            title=getattr(args, "title", None),
        )
    elif args.platform == "youtube":
        video_path = getattr(args, "video", None)
        tags = getattr(args, "tags", None)
        result = poster.post(
            text,
            video_path=str(video_path) if video_path else None,
            title=getattr(args, "title", None),
            tags=tags.split(",") if tags else None,
            privacy_status=getattr(args, "privacy", "public"),
            thumbnail_path=str(getattr(args, "thumbnail", None)) if getattr(args, "thumbnail", None) else None,
        )
    else:
        result = poster.post(text)

    if output_json:
        print(json.dumps(result, indent=2))
    elif result["success"]:
        print(f"Posted successfully!")
        print(f"ID: {result['id']}")
        print(f"URL: {result['url']}")
    else:
        print(f"Error: {result['error']}", file=sys.stderr)
        return 1

    return 0


def cmd_delete(args, output_json: bool = False) -> int:
    """Handle delete command."""
    poster = get_poster(args.platform)
    result = poster.delete(args.post_id)

    if output_json:
        print(json.dumps(result, indent=2))
    elif result["success"]:
        print(f"Deleted: {args.post_id}")
    else:
        print(f"Error: {result['error']}", file=sys.stderr)
        return 1

    return 0


def cmd_thread(args, output_json: bool = False) -> int:
    """Handle thread command."""
    if not args.file.exists():
        print(f"Error: File not found: {args.file}", file=sys.stderr)
        return 1

    content = args.file.read_text()
    tweets = [t.strip() for t in content.split("---") if t.strip()]

    if not tweets:
        print("Error: No content found in file", file=sys.stderr)
        return 1

    # Dry run
    if args.dry_run:
        print("=== DRY RUN (Thread) ===")
        print(f"Platform: {args.platform}")
        print(f"Posts: {len(tweets)}")
        for i, t in enumerate(tweets, 1):
            print(f"\n--- Post {i} ({len(t)} chars) ---")
            print(t[:200] + ("..." if len(t) > 200 else ""))
        return 0

    # Post thread
    poster = get_poster(args.platform)
    result = poster.post_thread(tweets)

    if output_json:
        print(json.dumps(result, indent=2))
    elif result["success"]:
        print(f"Thread posted! ({len(result['ids'])} posts)")
        for url in result["urls"]:
            print(f"  {url}")
    else:
        print(f"Error: {result['error']}", file=sys.stderr)
        return 1

    return 0


def cmd_analytics(args, output_json: bool = False) -> int:
    """Handle analytics command."""
    ga = GoogleAnalytics()

    if args.analytics_command == "track":
        params = {}
        if args.param:
            for key, value in args.param:
                params[key] = value
        result = ga.track_event(args.event_name, params)

    elif args.analytics_command == "realtime":
        result = ga.get_realtime_users()

    elif args.analytics_command == "pageviews":
        result = ga.get_page_views(
            start_date=args.start,
            end_date=args.end,
            page_path=getattr(args, "path", None),
        )

    elif args.analytics_command == "sources":
        result = ga.get_traffic_sources(
            start_date=args.start,
            end_date=args.end,
        )

    else:
        print("Error: Specify analytics subcommand (track, realtime, pageviews, sources)", file=sys.stderr)
        return 1

    if output_json:
        print(json.dumps(result, indent=2))
    elif result["success"]:
        if args.analytics_command == "track":
            print(f"Event tracked: {args.event_name}")
        elif args.analytics_command == "realtime":
            print(f"Active users: {result.get('active_users', 0)}")
        elif args.analytics_command == "pageviews":
            print(f"Page views ({result['date_range']}):")
            for page in result.get("pages", [])[:10]:
                print(f"  {page['path']}: {page['page_views']} views, {page['users']} users")
        elif args.analytics_command == "sources":
            print(f"Traffic sources ({result['date_range']}):")
            for src in result.get("sources", [])[:10]:
                print(f"  {src['source']}/{src['medium']}: {src['sessions']} sessions")
    else:
        print(f"Error: {result['error']}", file=sys.stderr)
        return 1

    return 0


def cmd_help_recursive(parser: argparse.ArgumentParser) -> int:
    """Show help for all commands."""
    print("=" * 60)
    print("SOCIALIA - Complete Command Reference")
    print("=" * 60)
    print()

    # Main help
    parser.print_help()
    print()

    # Subcommand help
    for action in parser._subparsers._actions:
        if isinstance(action, argparse._SubParsersAction):
            for name, subparser in action.choices.items():
                if name != "help-recursive":
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

    if args.command is None:
        parser.print_help()
        return 0

    if args.command == "help-recursive":
        return cmd_help_recursive(parser)
    elif args.command == "post":
        return cmd_post(args, output_json=args.json)
    elif args.command == "delete":
        return cmd_delete(args, output_json=args.json)
    elif args.command == "thread":
        return cmd_thread(args, output_json=args.json)
    elif args.command == "analytics":
        return cmd_analytics(args, output_json=args.json)
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
