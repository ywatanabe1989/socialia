#!/usr/bin/env python3
"""Scheduler for delayed/scheduled posts."""

import json
import time
import uuid
from datetime import datetime
from pathlib import Path

SCHEDULE_DIR = Path.home() / ".socialia"
SCHEDULE_FILE = SCHEDULE_DIR / "scheduled.json"


def _ensure_schedule_file():
    """Ensure schedule directory and file exist."""
    SCHEDULE_DIR.mkdir(parents=True, exist_ok=True)
    if not SCHEDULE_FILE.exists():
        SCHEDULE_FILE.write_text("[]")


def _load_schedule() -> list:
    """Load scheduled jobs."""
    _ensure_schedule_file()
    try:
        return json.loads(SCHEDULE_FILE.read_text())
    except (json.JSONDecodeError, FileNotFoundError):
        return []


def _save_schedule(jobs: list):
    """Save scheduled jobs."""
    _ensure_schedule_file()
    SCHEDULE_FILE.write_text(json.dumps(jobs, indent=2))


def parse_schedule_time(time_str: str) -> datetime:
    """
    Parse schedule time string.

    Supports:
        - "10:00" - today at 10:00 (or tomorrow if past)
        - "2026-01-23 10:00" - specific date and time
        - "+1h" - 1 hour from now
        - "+30m" - 30 minutes from now
    """
    now = datetime.now()

    # Relative time (+1h, +30m)
    if time_str.startswith("+"):
        amount = int(time_str[1:-1])
        unit = time_str[-1]
        if unit == "h":
            return datetime.fromtimestamp(now.timestamp() + amount * 3600)
        elif unit == "m":
            return datetime.fromtimestamp(now.timestamp() + amount * 60)
        else:
            raise ValueError(f"Unknown time unit: {unit} (use 'h' or 'm')")

    # Full datetime
    if "-" in time_str and " " in time_str:
        return datetime.strptime(time_str, "%Y-%m-%d %H:%M")

    # Time only (today or tomorrow)
    if ":" in time_str and "-" not in time_str:
        target = datetime.strptime(time_str, "%H:%M")
        target = target.replace(year=now.year, month=now.month, day=now.day)
        if target <= now:
            # Schedule for tomorrow
            target = target.replace(day=now.day + 1)
        return target

    raise ValueError(f"Cannot parse time: {time_str}")


def schedule_post(
    platform: str,
    text: str,
    schedule_time: str,
    **kwargs,
) -> dict:
    """
    Schedule a post for later.

    Args:
        platform: Target platform (twitter, linkedin, etc.)
        text: Post content
        schedule_time: When to post (see parse_schedule_time)
        **kwargs: Additional arguments (subreddit, title, etc.)

    Returns:
        dict with 'success', 'job_id', 'scheduled_for'
    """
    try:
        scheduled_dt = parse_schedule_time(schedule_time)
    except ValueError as e:
        return {"success": False, "error": str(e)}

    job = {
        "id": str(uuid.uuid4())[:8],
        "platform": platform,
        "text": text,
        "scheduled_for": scheduled_dt.isoformat(),
        "created_at": datetime.now().isoformat(),
        "status": "pending",
        "kwargs": kwargs,
    }

    jobs = _load_schedule()
    jobs.append(job)
    _save_schedule(jobs)

    return {
        "success": True,
        "job_id": job["id"],
        "scheduled_for": scheduled_dt.strftime("%Y-%m-%d %H:%M"),
    }


def list_scheduled() -> list:
    """List all scheduled jobs."""
    jobs = _load_schedule()
    # Filter to pending only and sort by time
    pending = [j for j in jobs if j.get("status") == "pending"]
    return sorted(pending, key=lambda j: j.get("scheduled_for", ""))


def cancel_scheduled(job_id: str) -> dict:
    """Cancel a scheduled job."""
    jobs = _load_schedule()
    for job in jobs:
        if job["id"] == job_id:
            job["status"] = "cancelled"
            _save_schedule(jobs)
            return {"success": True, "cancelled": job_id}
    return {"success": False, "error": f"Job not found: {job_id}"}


def run_due_jobs() -> list:
    """Run all jobs that are due. Returns list of results."""
    from .twitter import Twitter
    from .linkedin import LinkedIn
    from .reddit import Reddit
    from .youtube import YouTube

    def get_client(platform):
        if platform == "twitter":
            return Twitter()
        elif platform == "linkedin":
            return LinkedIn()
        elif platform == "reddit":
            return Reddit()
        elif platform == "youtube":
            return YouTube()
        raise ValueError(f"Unknown platform: {platform}")

    jobs = _load_schedule()
    results = []
    now = datetime.now()

    for job in jobs:
        if job.get("status") != "pending":
            continue

        scheduled = datetime.fromisoformat(job["scheduled_for"])
        if scheduled <= now:
            # Job is due
            try:
                client = get_client(job["platform"])
                kwargs = job.get("kwargs", {})
                result = client.post(job["text"], **kwargs)
                job["status"] = "completed" if result.get("success") else "failed"
                job["result"] = result
                job["executed_at"] = now.isoformat()
                results.append({"job_id": job["id"], **result})
            except Exception as e:
                job["status"] = "failed"
                job["error"] = str(e)
                results.append({"job_id": job["id"], "success": False, "error": str(e)})

    _save_schedule(jobs)
    return results


def run_daemon(interval: int = 60):
    """Run scheduler daemon that checks for due jobs."""
    print(f"Scheduler daemon started (checking every {interval}s)")
    print(f"Schedule file: {SCHEDULE_FILE}")
    print("Press Ctrl+C to stop")

    try:
        while True:
            results = run_due_jobs()
            for r in results:
                status = "✅" if r.get("success") else "❌"
                print(f"{status} Job {r['job_id']}: {r}")
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\nDaemon stopped")
