#!/usr/bin/env python3
"""
Example 03: Post a Twitter Thread

Demonstrates:
- Thread posting (multiple connected tweets)
- Handling partial failures
- Thread content from file

Usage:
    python 03_thread_twitter.py --dry-run   # Preview without posting
    python 03_thread_twitter.py             # Real post (requires credentials)

Environment:
    SOCIALIA_X_CONSUMER_KEY
    SOCIALIA_X_CONSUMER_KEY_SECRET
    SOCIALIA_X_ACCESSTOKEN
    SOCIALIA_X_ACCESSTOKEN_SECRET
"""

import argparse

from socialia import Twitter


def main():
    parser = argparse.ArgumentParser(description="Post a Twitter thread")
    parser.add_argument(
        "--dry-run", action="store_true", help="Preview without posting"
    )
    args = parser.parse_args()

    # Create client
    twitter = Twitter()

    # Check credentials
    if not twitter.validate_credentials():
        print("ERROR: Twitter credentials not configured")
        return 1

    # Thread content
    tweets = [
        "1/3 Thread about Socialia - a unified social media management tool",
        "2/3 Features:\n- Multi-platform posting (Twitter, LinkedIn)\n- Thread support\n- CLI and Python API\n- MCP server for AI integration",
        "3/3 Built for researchers and developers who need programmatic social media access.\n\nGitHub: https://github.com/ywatanabe1989/socialia",
    ]

    if args.dry_run:
        print("=== DRY RUN (Thread) ===")
        print("Platform: Twitter")
        print(f"Posts: {len(tweets)}")
        for i, tweet in enumerate(tweets, 1):
            print(f"\n--- Tweet {i} ({len(tweet)} chars) ---")
            print(tweet)
        return 0

    # Post thread
    result = twitter.post_thread(tweets)

    if result["success"]:
        print(f"Thread posted! ({len(result['ids'])} tweets)")
        for url in result["urls"]:
            print(f"  {url}")
        return 0
    else:
        print(f"ERROR: {result['error']}")
        if "partial_ids" in result:
            print(f"Partial success: {len(result['partial_ids'])} tweets posted")
        return 1


if __name__ == "__main__":
    exit(main())
