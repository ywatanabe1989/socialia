#!/usr/bin/env python3
"""
Example 01: Post to Twitter/X

Demonstrates:
- Basic posting via Python API
- Credential validation
- Dry-run mode for testing

Usage:
    python 01_post_twitter.py --dry-run   # Preview without posting
    python 01_post_twitter.py             # Real post (requires credentials)

Environment:
    SCITEX_X_CONSUMER_KEY
    SCITEX_X_CONSUMER_KEY_SECRET
    SCITEX_X_ACCESSTOKEN
    SCITEX_X_ACCESSTOKEN_SECRET
"""

import argparse
from socialia import TwitterPoster


def main():
    parser = argparse.ArgumentParser(description="Post to Twitter/X")
    parser.add_argument("--dry-run", action="store_true", help="Preview without posting")
    args = parser.parse_args()

    # Create poster
    twitter = TwitterPoster()

    # Check credentials
    if not twitter.validate_credentials():
        print("ERROR: Twitter credentials not configured")
        print("Set environment variables:")
        print("  SCITEX_X_CONSUMER_KEY")
        print("  SCITEX_X_CONSUMER_KEY_SECRET")
        print("  SCITEX_X_ACCESSTOKEN")
        print("  SCITEX_X_ACCESSTOKEN_SECRET")
        return 1

    # Content to post
    text = "Hello from Socialia! Testing the Python API."

    if args.dry_run:
        print("=== DRY RUN ===")
        print(f"Platform: Twitter")
        print(f"Text ({len(text)} chars): {text}")
        print("Credentials: Valid")
        return 0

    # Post
    result = twitter.post(text)

    if result["success"]:
        print(f"Posted successfully!")
        print(f"ID: {result['id']}")
        print(f"URL: {result['url']}")
        return 0
    else:
        print(f"ERROR: {result['error']}")
        return 1


if __name__ == "__main__":
    exit(main())
