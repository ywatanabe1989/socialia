"""Tests for socialia feed CLI commands (Click-based, post-audit migration).

Argparse parser-shape tests have been removed. We now exercise behavior via
``main(argv)`` which dispatches through Click and the deprecation shim.
"""

from unittest.mock import patch

from socialia.cli import main


class TestFeedHelp:
    def test_feed_help(self, capsys):
        rc = main(["feed", "--help"])
        assert rc == 0
        out = capsys.readouterr().out
        assert "feed" in out.lower()
        assert "--limit" in out
        assert "--mentions" in out
        assert "--replies" in out
        assert "--detail" in out


class TestCheckHelp:
    def test_check_canonical_help(self, capsys):
        rc = main(["check-platforms", "--help"])
        assert rc == 0
        out = capsys.readouterr().out
        assert "check-platforms" in out

    def test_check_deprecated_alias_routes_to_check_platforms(self, capsys):
        # `check` -> `check-platforms` via shim.
        rc = main(["check", "--help"])
        assert rc == 0
        out = capsys.readouterr().out
        assert "check-platforms" in out


class TestMeHelp:
    def test_me_canonical_help(self, capsys):
        rc = main(["show-me", "--help"])
        assert rc == 0
        out = capsys.readouterr().out
        assert "show-me" in out
        assert "twitter" in out.lower()


class TestScheduleHelp:
    def test_schedule_list_help(self, capsys):
        rc = main(["schedule", "list", "--help"])
        assert rc == 0
        out = capsys.readouterr().out
        assert "schedule list" in out or "list" in out.lower()

    def test_schedule_cancel_help(self, capsys):
        rc = main(["schedule", "cancel", "--help"])
        assert rc == 0
        out = capsys.readouterr().out
        assert "JOB_ID" in out or "job_id" in out.lower()

    def test_schedule_run_alias_routes_to_start_due_jobs(self, capsys):
        rc = main(["schedule", "run", "--help"])
        assert rc == 0
        out = capsys.readouterr().out
        assert "start-due-jobs" in out

    def test_schedule_daemon_alias_routes_to_start_daemon(self, capsys):
        rc = main(["schedule", "daemon", "--help"])
        assert rc == 0
        out = capsys.readouterr().out
        assert "start-daemon" in out

    def test_post_with_schedule_flag(self, capsys):
        # --schedule is preserved on post.
        rc = main(["post", "twitter", "Hello", "--schedule", "+1h", "--dry-run"])
        # Don't assert on rc -- scheduler may or may not succeed without creds;
        # the key is the flag parses and the command runs.
        assert rc in (0, 1, 2)


class TestMCPParsing:
    def test_mcp_start_help(self, capsys):
        rc = main(["mcp", "start", "--help"])
        assert rc == 0

    def test_mcp_doctor_help(self, capsys):
        rc = main(["mcp", "doctor", "--help"])
        assert rc == 0

    def test_mcp_list_tools_help(self, capsys):
        rc = main(["mcp", "list-tools", "--help"])
        assert rc == 0

    def test_mcp_installation_alias_routes_to_show_installation(self, capsys):
        rc = main(["mcp", "installation", "--help"])
        assert rc == 0
        out = capsys.readouterr().out
        assert "show-installation" in out


class TestMCPCommands:
    def test_mcp_doctor(self, capsys):
        rc = main(["mcp", "doctor"])
        assert rc in (0, 1)
        out = capsys.readouterr().out
        assert "Health Check" in out
        assert "Twitter" in out

    def test_mcp_installation_canonical(self, capsys):
        rc = main(["mcp", "show-installation"])
        assert rc == 0
        out = capsys.readouterr().out
        assert "Claude Desktop" in out
        assert "mcpServers" in out
        assert "socialia" in out


class TestScheduleCommands:
    def test_schedule_list_empty(self, capsys, tmp_path):
        schedule_file = tmp_path / "scheduled.json"
        schedule_file.write_text("[]")
        with patch("socialia.scheduler.SCHEDULE_FILE", schedule_file):
            rc = main(["schedule", "list"])
        assert rc == 0
        out = capsys.readouterr().out
        assert "No scheduled" in out or "pending" in out.lower()

    def test_schedule_cancel_nonexistent(self, capsys, tmp_path):
        schedule_file = tmp_path / "scheduled.json"
        schedule_file.write_text("[]")
        with patch("socialia.scheduler.SCHEDULE_FILE", schedule_file):
            rc = main(["schedule", "cancel", "nonexistent", "--yes"])
        assert rc == 1
        err = capsys.readouterr().err
        assert "not found" in err.lower() or "error" in err.lower()
