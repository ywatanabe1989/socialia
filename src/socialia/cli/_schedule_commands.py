#!/usr/bin/env python3
"""Schedule CLI command handlers for socialia."""

import json
import sys


def cmd_schedule(args, output_json: bool = False) -> int:
    """Handle schedule command."""
    from ..scheduler import (
        list_scheduled,
        cancel_scheduled,
        run_due_jobs,
        run_daemon,
        SCHEDULE_FILE,
    )

    cmd = getattr(args, "schedule_command", None)

    if cmd == "list":
        jobs = list_scheduled()
        if output_json:
            print(json.dumps(jobs, indent=2))
        elif not jobs:
            print("No scheduled posts")
        else:
            print(f"Scheduled posts ({len(jobs)}):")
            print("─" * 50)
            for job in jobs:
                scheduled = job.get("scheduled_for", "")[:16].replace("T", " ")
                print(f"  [{job['id']}] {job['platform']} @ {scheduled}")
                text = job.get("text", "")[:60]
                if len(job.get("text", "")) > 60:
                    text += "..."
                print(f"         {text}")
                print()
        return 0

    elif cmd == "cancel":
        result = cancel_scheduled(args.job_id)
        if output_json:
            print(json.dumps(result, indent=2))
        elif result["success"]:
            print(f"Cancelled job: {args.job_id}")
        else:
            print(f"Error: {result['error']}", file=sys.stderr)
            return 1
        return 0

    elif cmd == "run":
        results = run_due_jobs()
        if output_json:
            print(json.dumps(results, indent=2))
        elif not results:
            print("No jobs due")
        else:
            for r in results:
                status = "✅" if r.get("success") else "❌"
                print(f"{status} Job {r['job_id']}")
                if r.get("url"):
                    print(f"   URL: {r['url']}")
                if r.get("error"):
                    print(f"   Error: {r['error']}")
        return 0

    elif cmd == "daemon":
        print(f"Schedule file: {SCHEDULE_FILE}")
        run_daemon(interval=args.interval)
        return 0

    else:
        print("Usage: socialia schedule {list|cancel|run|daemon}", file=sys.stderr)
        return 1
