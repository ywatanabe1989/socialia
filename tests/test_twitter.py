"""Tests for Twitter poster."""

from unittest.mock import MagicMock
from socialia.twitter import TwitterPoster


class TestTwitterPoster:
    """Test TwitterPoster class."""

    def test_init_with_credentials(self, twitter_credentials):
        """Test initialization with explicit credentials."""
        poster = TwitterPoster(**twitter_credentials)
        assert poster.consumer_key == "test_consumer_key"
        assert poster.consumer_secret == "test_consumer_secret"
        assert poster.access_token == "test_access_token"
        assert poster.access_token_secret == "test_access_token_secret"

    def test_init_from_environment(self, monkeypatch):
        """Test initialization from environment variables."""
        monkeypatch.setenv("SCITEX_X_CONSUMER_KEY", "env_consumer_key")
        monkeypatch.setenv("SCITEX_X_CONSUMER_KEY_SECRET", "env_consumer_secret")
        monkeypatch.setenv("SCITEX_X_ACCESSTOKEN", "env_access_token")
        monkeypatch.setenv("SCITEX_X_ACCESSTOKEN_SECRET", "env_access_secret")

        poster = TwitterPoster()
        assert poster.consumer_key == "env_consumer_key"
        assert poster.consumer_secret == "env_consumer_secret"

    def test_validate_credentials_valid(self, twitter_credentials):
        """Test credential validation with valid credentials."""
        poster = TwitterPoster(**twitter_credentials)
        assert poster.validate_credentials() is True

    def test_validate_credentials_missing(self, monkeypatch):
        """Test credential validation with missing credentials."""
        # Clear environment variables
        monkeypatch.delenv("SCITEX_X_CONSUMER_KEY", raising=False)
        monkeypatch.delenv("SCITEX_X_CONSUMER_KEY_SECRET", raising=False)
        monkeypatch.delenv("SCITEX_X_ACCESSTOKEN", raising=False)
        monkeypatch.delenv("SCITEX_X_ACCESSTOKEN_SECRET", raising=False)
        poster = TwitterPoster(consumer_key="only_one")
        assert poster.validate_credentials() is False

    def test_post_missing_credentials(self, monkeypatch):
        """Test post fails with missing credentials."""
        # Clear environment variables
        monkeypatch.delenv("SCITEX_X_CONSUMER_KEY", raising=False)
        monkeypatch.delenv("SCITEX_X_CONSUMER_KEY_SECRET", raising=False)
        monkeypatch.delenv("SCITEX_X_ACCESSTOKEN", raising=False)
        monkeypatch.delenv("SCITEX_X_ACCESSTOKEN_SECRET", raising=False)
        poster = TwitterPoster()
        result = poster.post("Test")
        assert result["success"] is False
        assert "credentials" in result["error"].lower()

    def test_post_success(self, twitter_credentials, mock_oauth_session):
        """Test successful post."""
        mock_oauth_session.post.return_value = MagicMock(
            status_code=201,
            json=lambda: {"data": {"id": "12345"}},
        )

        poster = TwitterPoster(**twitter_credentials)
        result = poster.post("Hello World!")

        assert result["success"] is True
        assert result["id"] == "12345"
        assert "x.com" in result["url"]

    def test_post_failure(self, twitter_credentials, mock_oauth_session):
        """Test failed post."""
        mock_oauth_session.post.return_value = MagicMock(
            status_code=403,
            text="Forbidden",
        )

        poster = TwitterPoster(**twitter_credentials)
        result = poster.post("Hello World!")

        assert result["success"] is False
        assert "403" in result["error"]

    def test_post_with_reply(self, twitter_credentials, mock_oauth_session):
        """Test post with reply_to."""
        mock_oauth_session.post.return_value = MagicMock(
            status_code=201,
            json=lambda: {"data": {"id": "67890"}},
        )

        poster = TwitterPoster(**twitter_credentials)
        result = poster.post("Reply text", reply_to="12345")

        assert result["success"] is True
        call_args = mock_oauth_session.post.call_args
        assert "reply" in call_args.kwargs["json"]

    def test_delete_success(self, twitter_credentials, mock_oauth_session):
        """Test successful delete."""
        mock_oauth_session.delete.return_value = MagicMock(status_code=200)

        poster = TwitterPoster(**twitter_credentials)
        result = poster.delete("12345")

        assert result["success"] is True
        assert result["deleted"] is True

    def test_delete_failure(self, twitter_credentials, mock_oauth_session):
        """Test failed delete."""
        mock_oauth_session.delete.return_value = MagicMock(
            status_code=404,
            text="Not Found",
        )

        poster = TwitterPoster(**twitter_credentials)
        result = poster.delete("invalid_id")

        assert result["success"] is False
        assert "404" in result["error"]

    def test_post_thread_success(self, twitter_credentials, mock_oauth_session):
        """Test successful thread posting."""
        mock_oauth_session.post.side_effect = [
            MagicMock(status_code=201, json=lambda: {"data": {"id": "1"}}),
            MagicMock(status_code=201, json=lambda: {"data": {"id": "2"}}),
            MagicMock(status_code=201, json=lambda: {"data": {"id": "3"}}),
        ]

        poster = TwitterPoster(**twitter_credentials)
        result = poster.post_thread(["First", "Second", "Third"])

        assert result["success"] is True
        assert len(result["ids"]) == 3
        assert len(result["urls"]) == 3

    def test_post_thread_partial_failure(self, twitter_credentials, mock_oauth_session):
        """Test thread posting with partial failure."""
        mock_oauth_session.post.side_effect = [
            MagicMock(status_code=201, json=lambda: {"data": {"id": "1"}}),
            MagicMock(status_code=403, text="Rate limited"),
        ]

        poster = TwitterPoster(**twitter_credentials)
        result = poster.post_thread(["First", "Second", "Third"])

        assert result["success"] is False
        assert "partial_ids" in result
        assert len(result["partial_ids"]) == 1
