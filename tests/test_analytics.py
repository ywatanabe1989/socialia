"""Tests for socialia analytics module."""

from unittest.mock import patch, MagicMock

from socialia.analytics import GoogleAnalytics


class TestGoogleAnalyticsInit:
    """Test GoogleAnalytics initialization."""

    def test_init_without_credentials(self):
        """Test initialization without credentials."""
        with patch.dict("os.environ", {}, clear=True):
            ga = GoogleAnalytics()
            assert ga.measurement_id is None
            assert ga.api_secret is None

    def test_init_with_credentials(self):
        """Test initialization with credentials from env."""
        env_vars = {
            "SOCIALIA_GOOGLE_ANALYTICS_MEASUREMENT_ID": "G-TEST123",
            "SOCIALIA_GOOGLE_ANALYTICS_API_SECRET": "secret123",
        }
        with patch.dict("os.environ", env_vars, clear=True):
            ga = GoogleAnalytics()
            assert ga.measurement_id == "G-TEST123"
            assert ga.api_secret == "secret123"

    def test_init_with_scitex_prefix(self, monkeypatch):
        """Test initialization with SCITEX_ prefix."""
        # Clear branding and set to SCITEX prefix
        monkeypatch.setenv("SOCIALIA_ENV_PREFIX", "SCITEX")
        env_vars = {
            "SOCIALIA_ENV_PREFIX": "SCITEX",
            "SCITEX_GOOGLE_ANALYTICS_MEASUREMENT_ID": "G-SCITEX",
            "SCITEX_GOOGLE_ANALYTICS_API_SECRET": "scitex_secret",
        }

        # Reload branding module to pick up new prefix
        import importlib
        from socialia import _branding

        importlib.reload(_branding)

        with patch.dict("os.environ", env_vars, clear=True):
            ga = GoogleAnalytics()
            assert ga.measurement_id == "G-SCITEX"
            assert ga.api_secret == "scitex_secret"


class TestGoogleAnalyticsValidation:
    """Test GoogleAnalytics validation methods."""

    def test_validate_no_credentials(self):
        """Test validate_credentials returns false when no credentials."""
        with patch.dict("os.environ", {}, clear=True):
            ga = GoogleAnalytics()
            result = ga.validate_credentials()
            assert result["measurement_protocol"] is False

    def test_validate_with_credentials(self):
        """Test validate_credentials with valid credentials format."""
        env_vars = {
            "SOCIALIA_GOOGLE_ANALYTICS_MEASUREMENT_ID": "G-TEST123",
            "SOCIALIA_GOOGLE_ANALYTICS_API_SECRET": "secret123",
        }
        with patch.dict("os.environ", env_vars, clear=True):
            ga = GoogleAnalytics()
            result = ga.validate_credentials()
            assert result["measurement_protocol"] is True


class TestGoogleAnalyticsTrackEvent:
    """Test GoogleAnalytics track_event method."""

    def test_track_event_no_credentials(self):
        """Test track_event without credentials."""
        with patch.dict("os.environ", {}, clear=True):
            ga = GoogleAnalytics()
            result = ga.track_event("test_event")
            assert result["success"] is False
            assert "error" in result

    @patch("requests.post")
    def test_track_event_success(self, mock_post):
        """Test successful event tracking."""
        mock_response = MagicMock()
        mock_response.status_code = 204
        mock_post.return_value = mock_response

        env_vars = {
            "SOCIALIA_GOOGLE_ANALYTICS_MEASUREMENT_ID": "G-TEST123",
            "SOCIALIA_GOOGLE_ANALYTICS_API_SECRET": "secret123",
        }
        with patch.dict("os.environ", env_vars, clear=True):
            ga = GoogleAnalytics()
            result = ga.track_event("test_event", {"key": "value"})
            assert result["success"] is True
            mock_post.assert_called_once()

    @patch("requests.post")
    def test_track_event_failure(self, mock_post):
        """Test failed event tracking."""
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.text = "Bad Request"
        mock_post.return_value = mock_response

        env_vars = {
            "SOCIALIA_GOOGLE_ANALYTICS_MEASUREMENT_ID": "G-TEST123",
            "SOCIALIA_GOOGLE_ANALYTICS_API_SECRET": "secret123",
        }
        with patch.dict("os.environ", env_vars, clear=True):
            ga = GoogleAnalytics()
            result = ga.track_event("test_event")
            assert result["success"] is False


class TestAnalyticsCLI:
    """Test analytics CLI commands (Click-based, post-audit migration).

    The argparse `create_parser()` API was removed; behavior is now exercised
    via the public ``main(argv)`` Click entry point and the deprecation shim.
    """

    def test_analytics_track_help(self, capsys):
        from socialia.cli import main

        rc = main(["analytics", "track", "--help"])
        assert rc == 0
        out = capsys.readouterr().out
        assert "EVENT_NAME" in out or "event_name" in out.lower()

    def test_analytics_track_with_params_help(self, capsys):
        from socialia.cli import main

        rc = main(["analytics", "track", "--help"])
        assert rc == 0
        out = capsys.readouterr().out
        assert "--param" in out

    def test_analytics_realtime_alias(self, capsys):
        # Deprecated `analytics realtime` -> `analytics show-realtime`.
        from socialia.cli import main

        rc = main(["analytics", "realtime", "--help"])
        assert rc == 0
        out = capsys.readouterr().out
        assert "show-realtime" in out

    def test_analytics_pageviews_alias(self, capsys):
        from socialia.cli import main

        rc = main(["analytics", "pageviews", "--help"])
        assert rc == 0
        out = capsys.readouterr().out
        assert "show-pageviews" in out
        assert "--start" in out
        assert "--end" in out

    def test_analytics_sources_alias(self, capsys):
        from socialia.cli import main

        rc = main(["analytics", "sources", "--help"])
        assert rc == 0
        out = capsys.readouterr().out
        assert "show-sources" in out
