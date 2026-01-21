#!/usr/bin/env python3
"""Feed and check CLI command handlers for socialia."""

import json
import sys

from .. import __version__
from ..twitter import Twitter
from ..linkedin import LinkedIn
from ..reddit import Reddit
from ..youtube import YouTube


def get_client(platform: str):
    """Get platform client instance."""
    if platform == "twitter":
        return Twitter()
    elif platform == "linkedin":
        return LinkedIn()
    elif platform == "reddit":
        return Reddit()
    elif platform == "youtube":
        return YouTube()
    else:
        raise ValueError(f"Unsupported platform: {platform}")


def cmd_feed(args, output_json: bool = False) -> int:
    """Handle feed command - get recent posts from platforms."""
    platforms = []
    if hasattr(args, "platform") and args.platform:
        platforms = [args.platform]
    else:
        # Check all configured platforms
        platforms = ["twitter", "linkedin", "reddit", "youtube"]

    limit = getattr(args, "limit", 5)
    mentions_only = getattr(args, "mentions", False)
    results = {}

    for platform in platforms:
        client = get_client(platform)
        if not client.validate_credentials():
            results[platform] = {"success": False, "error": "Not configured"}
            continue

        if mentions_only:
            result = client.mentions(limit=limit)
        else:
            result = client.feed(limit=limit)
        results[platform] = result

    if output_json:
        print(json.dumps(results, indent=2))
    else:
        for platform, result in results.items():
            print(f"\n{platform.upper()}")
            print("─" * 40)
            if not result.get("success"):
                print(f"  ⚠️  {result.get('error', 'Unknown error')}")
                continue

            # Get posts/tweets/mentions
            items = (
                result.get("posts")
                or result.get("tweets")
                or result.get("mentions")
                or []
            )
            if not items:
                print("  No recent posts")
                continue

            for item in items[:limit]:
                text = item.get("text", item.get("title", ""))[:80]
                text = text.replace("\n", " ")
                if len(text) > 77:
                    text = text[:77] + "..."
                likes = item.get("likes", item.get("score", ""))
                created = (
                    item.get("created_at", "")[:10] if item.get("created_at") else ""
                )
                print(f"  • {text}")
                if likes or created:
                    print(f"    {created} {'❤️ ' + str(likes) if likes else ''}")

    return 0


def cmd_check(args, output_json: bool = False) -> int:
    """Handle check command - verify connections to all platforms."""
    platforms = []
    if hasattr(args, "platform") and args.platform:
        platforms = [args.platform]
    else:
        platforms = ["twitter", "linkedin", "reddit", "youtube"]

    results = {}
    for platform in platforms:
        client = get_client(platform)
        results[platform] = client.check()

    if output_json:
        print(json.dumps(results, indent=2))
    else:
        print(f"Socialia v{__version__} - Connection Check")
        print("=" * 50)
        for platform, result in results.items():
            status = result.get("status", "unknown")
            if status == "connected":
                user = result.get("user", {})
                name = user.get("name") or user.get("username") or user.get("title", "")
                print(f"\n✅ {platform.upper()}: Connected")
                if name:
                    print(f"   User: {name}")
                url = user.get("url", "")
                if url:
                    print(f"   URL: {url}")
            elif status == "not_configured":
                print(f"\n⚪ {platform.upper()}: Not configured")
            else:
                error = result.get("error", "Unknown error")
                print(f"\n❌ {platform.upper()}: Error")
                print(f"   {error}")

    return 0


def cmd_me(args, output_json: bool = False) -> int:
    """Handle me command - get user info for a platform."""
    client = get_client(args.platform)
    result = client.me()

    if output_json:
        print(json.dumps(result, indent=2))
    elif result.get("success"):
        print(f"{args.platform.upper()} User Info")
        print("─" * 30)
        for key, value in result.items():
            if key != "success":
                print(f"  {key}: {value}")
    else:
        print(f"Error: {result.get('error')}", file=sys.stderr)
        return 1

    return 0
