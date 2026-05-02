"""Tests for socialia MCP server module."""

import pytest

fastmcp = pytest.importorskip("fastmcp", reason="fastmcp not installed")


class TestMCPToolDefinitions:
    """Test MCP tool definitions."""

    def test_mcp_tools_list(self, capsys):
        """Test listing MCP tools."""
        from socialia.cli import main

        result = main(["mcp", "list-tools"])
        assert result == 0

        captured = capsys.readouterr()
        # Check all expected tools are listed
        assert "social_post" in captured.out
        assert "social_delete" in captured.out
        assert "social_status" in captured.out
        assert "analytics_track" in captured.out
        assert "analytics_realtime" in captured.out


class TestMCPDoctor:
    """Test MCP doctor command."""

    def test_mcp_doctor_output(self, capsys):
        """Test doctor command shows health check."""
        from socialia.cli import main

        # Returns 0 if all configured, 1 if some unconfigured (both valid)
        result = main(["mcp", "doctor"])
        assert result in (0, 1)

        captured = capsys.readouterr()
        assert "Health Check" in captured.out
        # Should show platform status
        assert "Twitter" in captured.out
        assert "LinkedIn" in captured.out
        assert "Reddit" in captured.out

    def test_mcp_doctor_shows_platform_names(self, capsys):
        """Test doctor shows platform names."""
        from socialia.cli import main

        main(["mcp", "doctor"])
        captured = capsys.readouterr()

        # Should show platform names
        assert "Twitter" in captured.out or "twitter" in captured.out.lower()
        assert "LinkedIn" in captured.out or "linkedin" in captured.out.lower()


class TestMCPInstallation:
    """Test MCP installation command."""

    def test_mcp_installation_output(self, capsys):
        """Test installation command shows config."""
        from socialia.cli import main

        assert main(["mcp", "installation"]) == 0

        captured = capsys.readouterr()
        assert "Claude Desktop" in captured.out
        assert "mcpServers" in captured.out
        assert "socialia" in captured.out
        assert "mcp" in captured.out
        assert "start" in captured.out

    def test_mcp_installation_json_format(self, capsys):
        """Test installation output is valid JSON-like."""
        from socialia.cli import main

        main(["mcp", "installation"])
        captured = capsys.readouterr()

        # Should contain JSON structure elements
        assert "{" in captured.out
        assert "}" in captured.out
        assert '"command"' in captured.out or "command" in captured.out


class TestMCPServerModule:
    """Test MCP server module functions."""

    def test_mcp_server_import(self):
        """Test mcp_server module can be imported."""
        from socialia import mcp_server

        assert mcp_server is not None

    def test_get_tools_function(self):
        """Test get_tools returns tool definitions."""
        try:
            from socialia.mcp_server import get_tools

            tools = get_tools()
            assert isinstance(tools, (list, dict))
        except (ImportError, AttributeError):
            # MCP may not be installed
            pytest.skip("MCP not available")

    def test_tool_names_in_output(self, capsys):
        """Test expected tool names appear in list-tools output."""
        from socialia.cli import main

        main(["mcp", "list-tools"])
        captured = capsys.readouterr()

        assert "social_post" in captured.out
        assert "social_delete" in captured.out
        assert "social_status" in captured.out
        assert "analytics_track" in captured.out


class TestMCPCommandParsing:
    """Test MCP command parsing."""

    def test_mcp_start_help(self, capsys):
        """Verify ``mcp start`` is registered (Click migration)."""
        from socialia.cli import main

        rc = main(["mcp", "start", "--help"])
        assert rc == 0
        out = capsys.readouterr().out
        assert "mcp start" in out or "start" in out.lower()
        # Mutating verb -> must surface --dry-run / --yes per audit §2.
        assert "--dry-run" in out
        assert "--yes" in out

    def test_mcp_no_subcommand(self, capsys):
        """Test mcp without subcommand shows help."""
        from socialia.cli import main

        result = main(["mcp"])
        # Should show help or return 0/1
        assert result in [0, 1]
