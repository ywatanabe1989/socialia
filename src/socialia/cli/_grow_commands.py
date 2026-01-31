#!/usr/bin/env python3
"""CLI commands for Twitter growth - discover and follow users."""

import json
import sys

from ..twitter import Twitter


def cmd_grow(args, output_json: bool = False) -> int:
    """Handle grow command - discover and follow users."""
    if args.platform != "twitter":
        print(
            f"Error: grow command only supports twitter (got: {args.platform})",
            file=sys.stderr,
        )
        return 1

    client = Twitter()

    if args.grow_command == "discover":
        result = client.discover_users(
            args.query,
            limit=args.limit,
            min_followers=args.min_followers,
        )
        if output_json:
            print(json.dumps(result, indent=2))
        elif result["success"]:
            print(f"Found {result['count']} users for: {args.query}\n")
            for user in result.get("users", []):
                print(f"@{user['username']} ({user['followers']} followers)")
                if user.get("description"):
                    desc = user["description"][:80]
                    print(
                        f"  {desc}{'...' if len(user.get('description', '')) > 80 else ''}"
                    )
                print()
        else:
            print(f"Error: {result['error']}", file=sys.stderr)
            return 1

    elif args.grow_command == "follow":
        # Handle scheduled follow
        schedule_time = getattr(args, "schedule", None)
        repeat_interval = getattr(args, "repeat", None)

        if schedule_time:
            from ..scheduler import schedule_grow

            result = schedule_grow(
                platform=args.platform,
                query=args.query,
                schedule_time=schedule_time,
                limit=args.limit,
                min_followers=args.min_followers,
                repeat_interval=repeat_interval,
            )
            if output_json:
                print(json.dumps(result, indent=2))
            elif result["success"]:
                print(f"Scheduled grow job for {result['scheduled_for']}")
                print(f"  Query: {args.query}")
                print(f"  Limit: {args.limit} users")
                print(f"  Job ID: {result['job_id']}")
                if repeat_interval:
                    print(f"  Repeats: every {repeat_interval}")
                print("\nRun 'socialia schedule daemon' to start the scheduler")
            else:
                print(f"Error: {result['error']}", file=sys.stderr)
                return 1
            return 0

        # Immediate follow
        result = client.grow(
            args.query,
            limit=args.limit,
            min_followers=args.min_followers,
            dry_run=args.dry_run,
        )
        if output_json:
            print(json.dumps(result, indent=2))
        elif result["success"]:
            if result["dry_run"]:
                print(
                    f"=== DRY RUN === Would follow {result['discovered_count']} users:\n"
                )
                for user in result.get("discovered", []):
                    print(f"  @{user['username']} ({user['followers']} followers)")
                print("\nRun without --dry-run to actually follow.")
            else:
                print(f"Followed {result['followed_count']} users:")
                for user in result.get("followed", []):
                    print(f"  @{user['username']}")
                if result.get("rate_limited"):
                    print("\n[Rate limited] Wait ~15 min before following more.")
                if result.get("skipped"):
                    print(f"\nSkipped {len(result['skipped'])}:")
                    for user in result["skipped"][:3]:  # Show first 3 only
                        print(f"  @{user['username']}: {user.get('error')}")
                    if len(result["skipped"]) > 3:
                        print(f"  ... and {len(result['skipped']) - 3} more")
        else:
            print(f"Error: {result['error']}", file=sys.stderr)
            return 1

    elif args.grow_command == "user":
        result = client.get_user(args.username)
        if output_json:
            print(json.dumps(result, indent=2))
        elif result["success"]:
            print(f"@{result['username']} ({result['name']})")
            print(f"  Followers: {result['followers']}")
            print(f"  Following: {result['following']}")
            print(f"  Tweets: {result['tweets']}")
            if result.get("description"):
                print(f"  Bio: {result['description']}")
        else:
            print(f"Error: {result['error']}", file=sys.stderr)
            return 1

    elif args.grow_command == "follow-user":
        if args.dry_run:
            print(f"=== DRY RUN === Would follow @{args.username}")
            return 0
        result = client.follow_by_username(args.username)
        if output_json:
            print(json.dumps(result, indent=2))
        elif result["success"]:
            user = result.get("user", {})
            print(f"Followed @{user.get('username', args.username)}")
        else:
            print(f"Error: {result['error']}", file=sys.stderr)
            return 1

    elif args.grow_command == "search":
        result = client.search_tweets(args.query, limit=args.limit)
        if output_json:
            print(json.dumps(result, indent=2))
        elif result["success"]:
            print(f"Found {result['count']} tweets for: {args.query}\n")
            for tweet in result.get("tweets", []):
                print(f"@{tweet['author_username']}:")
                text = tweet["text"][:200]
                print(f"  {text}{'...' if len(tweet['text']) > 200 else ''}")
                print(f"  Likes: {tweet['likes']} | RTs: {tweet['retweets']}")
                print(f"  {tweet['url']}\n")
        else:
            print(f"Error: {result['error']}", file=sys.stderr)
            return 1

    elif args.grow_command == "auto":
        from ..scheduler import schedule_grow

        queries = args.queries
        interval = args.interval
        limit = args.limit
        min_followers = args.min_followers

        # Schedule jobs with staggered start times
        scheduled = []
        for i, query in enumerate(queries):
            # Stagger start: first one in 1 min, then interval apart
            if i == 0:
                start_time = "+1m"
            else:
                # Parse interval to get minutes/hours, multiply by index
                start_time = f"+{i}h" if "h" in interval else f"+{i * 30}m"

            result = schedule_grow(
                platform=args.platform,
                query=query,
                schedule_time=start_time,
                limit=limit,
                min_followers=min_followers,
                repeat_interval=interval,
            )
            if result["success"]:
                scheduled.append({"query": query, "job_id": result["job_id"]})

        if output_json:
            print(json.dumps({"success": True, "scheduled": scheduled}, indent=2))
        else:
            print(f"Scheduled {len(scheduled)} recurring grow jobs:\n")
            for s in scheduled:
                print(f'  [{s["job_id"]}] "{s["query"]}"')
            print(f"\nInterval: {interval}")
            print(f"Limit: {limit} users per job")
            print("\nRun 'socialia schedule daemon' to start")

    else:
        print(
            "Error: Specify grow subcommand (discover, follow, user, follow-user, search, auto)",
            file=sys.stderr,
        )
        return 1

    return 0


def add_grow_parser(subparsers):
    """Add grow command parser."""
    grow_parser = subparsers.add_parser(
        "grow",
        help="Discover and follow users (Twitter)",
        description="Find relevant users and grow your following",
    )
    grow_parser.add_argument(
        "platform",
        choices=["twitter"],
        help="Platform (only twitter supported)",
    )
    grow_sub = grow_parser.add_subparsers(dest="grow_command", help="Growth operations")

    # discover subcommand
    discover_parser = grow_sub.add_parser(
        "discover",
        help="Find users by search query",
        description="Search tweets and extract unique users",
    )
    discover_parser.add_argument(
        "query", help="Search query (e.g., 'scientific python')"
    )
    discover_parser.add_argument(
        "-l", "--limit", type=int, default=20, help="Max users to find (default: 20)"
    )
    discover_parser.add_argument(
        "--min-followers",
        type=int,
        default=0,
        help="Minimum follower count filter",
    )

    # follow subcommand (batch follow from search)
    follow_parser = grow_sub.add_parser(
        "follow",
        help="Find and follow users by search query",
        description="Search for users and follow them",
    )
    follow_parser.add_argument("query", help="Search query")
    follow_parser.add_argument(
        "-l", "--limit", type=int, default=10, help="Max users to follow (default: 10)"
    )
    follow_parser.add_argument(
        "--min-followers",
        type=int,
        default=0,
        help="Minimum follower count filter",
    )
    follow_parser.add_argument(
        "-n", "--dry-run", action="store_true", help="Show users without following"
    )
    follow_parser.add_argument(
        "-S",
        "--schedule",
        help="Schedule for later (e.g., '+20m', '+1h', '10:00')",
    )
    follow_parser.add_argument(
        "-R",
        "--repeat",
        help="Repeat interval (e.g., '+1h', '+30m') - requires --schedule",
    )

    # auto subcommand (set up recurring growth)
    auto_parser = grow_sub.add_parser(
        "auto",
        help="Set up automatic recurring growth",
        description="Schedule recurring grow jobs with multiple queries",
    )
    auto_parser.add_argument(
        "queries",
        nargs="+",
        help="Search queries to rotate through",
    )
    auto_parser.add_argument(
        "-i",
        "--interval",
        default="+1h",
        help="Interval between jobs (default: +1h)",
    )
    auto_parser.add_argument(
        "-l", "--limit", type=int, default=10, help="Max users per job (default: 10)"
    )
    auto_parser.add_argument(
        "--min-followers",
        type=int,
        default=0,
        help="Minimum follower count filter",
    )

    # user subcommand (lookup single user)
    user_parser = grow_sub.add_parser(
        "user",
        help="Get user info by username",
        description="Look up a user's profile",
    )
    user_parser.add_argument("username", help="Twitter username (with or without @)")

    # follow-user subcommand (follow single user)
    follow_user_parser = grow_sub.add_parser(
        "follow-user",
        help="Follow a single user by username",
        description="Follow a specific user",
    )
    follow_user_parser.add_argument("username", help="Twitter username to follow")
    follow_user_parser.add_argument(
        "-n", "--dry-run", action="store_true", help="Show user without following"
    )

    # search subcommand (search tweets)
    search_parser = grow_sub.add_parser(
        "search",
        help="Search recent tweets",
        description="Search for tweets matching a query",
    )
    search_parser.add_argument("query", help="Search query")
    search_parser.add_argument(
        "-l", "--limit", type=int, default=10, help="Max tweets (default: 10)"
    )

    return grow_parser
