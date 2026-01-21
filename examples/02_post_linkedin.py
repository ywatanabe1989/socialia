#!/usr/bin/env python3
"""
Example 02: Post to LinkedIn

Demonstrates:
- LinkedIn posting via Python API
- Token validation
- Different visibility options

Usage:
    python 02_post_linkedin.py --dry-run   # Preview without posting
    python 02_post_linkedin.py             # Real post (requires token)

Environment:
    SOCIALIA_LINKEDIN_ACCESS_TOKEN
"""

import argparse

from socialia import LinkedIn


def main():
    parser = argparse.ArgumentParser(description="Post to LinkedIn")
    parser.add_argument(
        "--dry-run", action="store_true", help="Preview without posting"
    )
    parser.add_argument(
        "--visibility",
        choices=["PUBLIC", "CONNECTIONS"],
        default="PUBLIC",
        help="Post visibility",
    )
    args = parser.parse_args()

    # Create client
    linkedin = LinkedIn()

    # Check credentials
    if not linkedin.validate_credentials():
        print("ERROR: LinkedIn credentials not configured")
        print("Set environment variable:")
        print("  SOCIALIA_LINKEDIN_ACCESS_TOKEN")
        return 1

    # Content to post
    text = """Professional update from Socialia!

Testing the LinkedIn API integration. This tool helps automate social media management for research and development teams.

#automation #python #api"""

    if args.dry_run:
        print("=== DRY RUN ===")
        print("Platform: LinkedIn")
        print(f"Visibility: {args.visibility}")
        print(f"Text ({len(text)} chars):")
        print(text[:200] + "..." if len(text) > 200 else text)
        print("Credentials: Valid")
        return 0

    # Post
    result = linkedin.post(text, visibility=args.visibility)

    if result["success"]:
        print("Posted successfully!")
        print(f"ID: {result['id']}")
        print(f"URL: {result['url']}")
        return 0
    else:
        print(f"ERROR: {result['error']}")
        return 1


if __name__ == "__main__":
    exit(main())
