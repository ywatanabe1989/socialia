"""Tests for socialia CLI (Click-based, post-audit migration).

Parser-shape tests (argparse-only) have been removed. Behavior is tested via
the public ``main(argv)`` entry point, which now wraps Click + a backward-compat
argv-rewrite shim so deprecated subcommand names still work.
"""

import pytest
from socialia.cli import main


class TestCLIDryRun:
    """Test CLI dry-run functionality."""

    def test_post_dry_run_twitter(self, capsys):
        result = main(["post", "twitter", "Test message", "--dry-run"])
        assert result == 0
        captured = capsys.readouterr()
        assert "DRY RUN" in captured.out
        assert "twitter" in captured.out.lower()

    def test_post_dry_run_linkedin(self, capsys):
        result = main(["post", "linkedin", "Test message", "--dry-run"])
        assert result == 0
        captured = capsys.readouterr()
        assert "DRY RUN" in captured.out
        assert "linkedin" in captured.out.lower()


class TestCLIMain:
    """Test CLI main function."""

    def test_no_command_shows_help(self, capsys):
        result = main([])
        assert result == 0
        captured = capsys.readouterr()
        assert "usage:" in captured.out.lower() or "socialia" in captured.out.lower()

    def test_help_recursive(self, capsys):
        result = main(["--help-recursive"])
        assert result == 0
        captured = capsys.readouterr()
        # Click renders usage with "Usage:" prefix; subcommands are visible too.
        assert "post" in captured.out.lower()
        assert "delete-post" in captured.out.lower()

    def test_status_command_canonical(self, capsys):
        # Canonical name.
        result = main(["show-status"])
        assert result == 0
        captured = capsys.readouterr()
        assert "Socialia" in captured.out or "socialia" in captured.out.lower()

    def test_status_command_deprecated_alias(self, capsys):
        # Deprecated `status` alias still routes to show-status.
        result = main(["status"])
        assert result == 0

    def test_mcp_list_tools_command(self, capsys):
        pytest.importorskip("fastmcp", reason="fastmcp not installed")
        result = main(["mcp", "list-tools"])
        assert result == 0
        captured = capsys.readouterr()
        assert "MCP" in captured.out or "Tools" in captured.out


class TestCLICompletion:
    """Test CLI completion commands."""

    def test_completion_bash_canonical(self, capsys):
        # Canonical: top-level show-completion-bash.
        result = main(["show-completion-bash"])
        assert result == 0
        captured = capsys.readouterr()
        assert "argcomplete" in captured.out.lower() or "compdef" in captured.out

    def test_completion_bash_deprecated_alias(self, capsys):
        # `completion bash` still works via shim.
        result = main(["completion", "bash"])
        assert result == 0

    def test_completion_zsh_canonical(self, capsys):
        result = main(["show-completion-zsh"])
        assert result == 0
        captured = capsys.readouterr()
        assert "compdef" in captured.out or "bashcompinit" in captured.out

    def test_completion_status(self, capsys):
        # Deprecated `completion status` is rewritten to top-level
        # show-completion-status.
        result = main(["completion", "status"])
        assert result == 0
        captured = capsys.readouterr()
        assert "Completion Status" in captured.out


class TestCLIDeprecationAliases:
    """Verify backward-compat shim covers the renamed subcommands."""

    @pytest.mark.parametrize(
        "argv",
        [
            ["delete", "twitter", "123", "--dry-run"],
            ["setup"],
            ["check", "twitter"],
            ["me", "twitter"],
            ["analytics", "realtime"],
            ["analytics", "pageviews"],
            ["analytics", "sources"],
            ["mcp", "installation"],
            ["schedule", "run"],
            ["schedule", "daemon", "--dry-run"],
            ["completion", "bash"],
            ["completion", "zsh"],
            ["completion", "status"],
            ["org", "status", "/tmp/nonexistent.org"],
            ["youtube", "config", "--scitex"],
            ["grow", "twitter", "auto", "test", "--dry-run"],
            ["grow", "twitter", "user", "ywatanabe"],
        ],
    )
    def test_deprecated_alias_does_not_crash(self, argv):
        # We don't assert on exit code (some require live creds / files);
        # only that argv rewriting doesn't raise an unexpected exception.
        try:
            main(argv)
        except SystemExit:
            pass
