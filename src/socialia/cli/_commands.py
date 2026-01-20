#!/usr/bin/env python3
"""CLI command handlers for socialia."""

import json
import sys

from .. import __version__
from ..twitter import TwitterPoster
from ..linkedin import LinkedInPoster
from ..reddit import RedditPoster
from ..analytics import GoogleAnalytics
from ..youtube import YouTubePoster


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
            print(
                f"Title: {getattr(args, 'title', None) or text.split(chr(10))[0][:100]}"
            )
            print(f"Privacy: {getattr(args, 'privacy', 'public')}")
        print(
            f"Text ({len(text)} chars): {text[:100]}{'...' if len(text) > 100 else ''}"
        )
        return 0

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
            thumbnail_path=str(getattr(args, "thumbnail", None))
            if getattr(args, "thumbnail", None)
            else None,
        )
    else:
        result = poster.post(text)

    if output_json:
        print(json.dumps(result, indent=2))
    elif result["success"]:
        print("Posted successfully!")
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

    if args.dry_run:
        print("=== DRY RUN (Thread) ===")
        print(f"Platform: {args.platform}")
        print(f"Posts: {len(tweets)}")
        for i, t in enumerate(tweets, 1):
            print(f"\n--- Post {i} ({len(t)} chars) ---")
            print(t[:200] + ("..." if len(t) > 200 else ""))
        return 0

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
        print(
            "Error: Specify analytics subcommand (track, realtime, pageviews, sources)",
            file=sys.stderr,
        )
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
                print(
                    f"  {page['path']}: {page['page_views']} views, {page['users']} users"
                )
        elif args.analytics_command == "sources":
            print(f"Traffic sources ({result['date_range']}):")
            for src in result.get("sources", [])[:10]:
                print(f"  {src['source']}/{src['medium']}: {src['sessions']} sessions")
    else:
        print(f"Error: {result['error']}", file=sys.stderr)
        return 1

    return 0


def cmd_status(output_json: bool = False) -> int:
    """Show configuration and environment status."""
    import os

    env_vars = {
        "twitter": {
            "SCITEX_X_CONSUMER_KEY": os.environ.get("SCITEX_X_CONSUMER_KEY"),
            "SCITEX_X_CONSUMER_KEY_SECRET": os.environ.get(
                "SCITEX_X_CONSUMER_KEY_SECRET"
            ),
            "SCITEX_X_ACCESSTOKEN": os.environ.get("SCITEX_X_ACCESSTOKEN"),
            "SCITEX_X_ACCESSTOKEN_SECRET": os.environ.get(
                "SCITEX_X_ACCESSTOKEN_SECRET"
            ),
        },
        "linkedin": {
            "LINKEDIN_ACCESS_TOKEN": os.environ.get("LINKEDIN_ACCESS_TOKEN"),
        },
        "reddit": {
            "REDDIT_CLIENT_ID": os.environ.get("REDDIT_CLIENT_ID"),
            "REDDIT_CLIENT_SECRET": os.environ.get("REDDIT_CLIENT_SECRET"),
            "REDDIT_USERNAME": os.environ.get("REDDIT_USERNAME"),
            "REDDIT_PASSWORD": os.environ.get("REDDIT_PASSWORD"),
        },
        "youtube": {
            "YOUTUBE_CLIENT_SECRETS_FILE": os.environ.get(
                "YOUTUBE_CLIENT_SECRETS_FILE"
            ),
        },
        "analytics": {
            "GA_MEASUREMENT_ID": os.environ.get("GA_MEASUREMENT_ID"),
            "GA_API_SECRET": os.environ.get("GA_API_SECRET"),
            "GA_PROPERTY_ID": os.environ.get("GA_PROPERTY_ID"),
        },
    }

    status = {}
    for platform, vars_dict in env_vars.items():
        configured = all(v is not None for v in vars_dict.values())
        partial = any(v is not None for v in vars_dict.values())
        status[platform] = {
            "configured": configured,
            "partial": partial and not configured,
            "vars": {k: "set" if v else "missing" for k, v in vars_dict.items()},
        }

    if output_json:
        print(json.dumps({"version": __version__, "platforms": status}, indent=2))
    else:
        print(f"Socialia v{__version__}")
        print("=" * 40)
        for platform, info in status.items():
            if info["configured"]:
                mark = "[OK]"
            elif info["partial"]:
                mark = "[PARTIAL]"
            else:
                mark = "[NOT SET]"
            print(f"\n{platform.upper():12} {mark}")
            for var, state in info["vars"].items():
                indicator = "+" if state == "set" else "-"
                print(f"  {indicator} {var}")

    return 0


def cmd_mcp(args) -> int:
    """Handle MCP command."""
    if args.mcp_command == "run":
        import asyncio
        from ..mcp_server import main as mcp_main, HAS_MCP

        if not HAS_MCP:
            print(
                "Error: MCP package not installed. Run: pip install mcp",
                file=sys.stderr,
            )
            return 1
        asyncio.run(mcp_main())
        return 0

    elif args.mcp_command == "info":
        print("Socialia MCP Server")
        print("=" * 40)
        print()
        print("Available tools:")
        for tool_name in [
            "social_post",
            "social_delete",
            "analytics_track",
            "analytics_pageviews",
            "analytics_sources",
        ]:
            print(f"  - {tool_name}")
        print()
        print("Usage:")
        print("  socialia mcp run")
        print("  python -m socialia.mcp_server")
        return 0

    else:
        print("Error: Specify mcp subcommand (run, info)", file=sys.stderr)
        return 1
