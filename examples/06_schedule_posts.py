#!/usr/bin/env python3
"""
Example 06: Schedule Posts

Demonstrates:
- Scheduling posts for later
- Listing pending scheduled posts
- Cancelling scheduled posts
- Running the scheduler daemon

Usage:
    python 06_schedule_posts.py               # Demo schedule workflow
    python 06_schedule_posts.py --list        # List scheduled posts
    python 06_schedule_posts.py --cancel ID   # Cancel a scheduled post

CLI Equivalents:
    socialia post twitter "Hello!" --schedule "10:00"
    socialia post twitter "Hello!" --schedule "+1h"
    socialia post twitter "Hello!" --schedule "2026-01-25 14:30"
    socialia schedule list
    socialia schedule cancel <job_id>
    socialia schedule daemon --interval 60
"""

import argparse
from datetime import datetime, timedelta

from socialia.scheduler import (
    schedule_post,
    list_scheduled,
    cancel_scheduled,
)


def main():
    parser = argparse.ArgumentParser(description="Schedule posts demo")
    parser.add_argument("--list", action="store_true", help="List scheduled posts")
    parser.add_argument("--cancel", metavar="ID", help="Cancel a scheduled post")
    parser.add_argument(
        "--demo", action="store_true", help="Demo scheduling (creates test job)"
    )
    args = parser.parse_args()

    if args.cancel:
        # Cancel a scheduled post
        result = cancel_scheduled(args.cancel)
        if result["success"]:
            print(f"Cancelled: {args.cancel}")
        else:
            print(f"ERROR: {result['error']}")
        return 0 if result["success"] else 1

    if args.list:
        # List scheduled posts
        jobs = list_scheduled()
        if not jobs:
            print("No scheduled posts pending.")
            return 0

        print("=== Scheduled Posts ===")
        for job in jobs:
            print(f"\nID: {job['id']}")
            print(f"  Platform: {job['platform']}")
            print(f"  Scheduled: {job['scheduled_for']}")
            print(f"  Text: {job['text'][:50]}{'...' if len(job['text']) > 50 else ''}")
            if job.get("kwargs"):
                for k, v in job["kwargs"].items():
                    if v:
                        print(f"  {k}: {v}")

        print(f"\nTotal: {len(jobs)} pending")
        return 0

    if args.demo:
        # Demo: Schedule a post for 5 minutes from now
        future_time = datetime.now() + timedelta(minutes=5)
        time_str = future_time.strftime("%Y-%m-%d %H:%M")

        print("=== Schedule Demo ===")
        print(f"Scheduling test post for: {time_str}")
        print()

        result = schedule_post(
            platform="twitter",
            text="[TEST] Scheduled post from Socialia example script.",
            schedule_time=time_str,
        )

        if result["success"]:
            print("Scheduled successfully!")
            print(f"  Job ID: {result['job_id']}")
            print(f"  Time: {result['scheduled_for']}")
            print()
            print("To execute scheduled posts, run:")
            print("  socialia schedule daemon")
            print()
            print("To cancel this test post:")
            print(f"  socialia schedule cancel {result['job_id']}")
            print("  # or")
            print(f"  python 06_schedule_posts.py --cancel {result['job_id']}")
            return 0
        else:
            print(f"ERROR: {result['error']}")
            return 1

    # Default: Show help
    print("Schedule Posts Example")
    print("======================")
    print()
    print("Available time formats:")
    print('  "10:00"              - Today at 10:00 (or tomorrow if passed)')
    print('  "2026-01-25 14:30"   - Specific date and time')
    print('  "+1h"                - 1 hour from now')
    print('  "+30m"               - 30 minutes from now')
    print()
    print("Commands:")
    print("  --demo     Create a test scheduled post")
    print("  --list     List all pending scheduled posts")
    print("  --cancel   Cancel a scheduled post by ID")
    print()
    print("CLI usage:")
    print('  socialia post twitter "Hello!" --schedule "+1h"')
    print("  socialia schedule list")
    print("  socialia schedule daemon  # Run to execute scheduled posts")

    return 0


if __name__ == "__main__":
    exit(main())
