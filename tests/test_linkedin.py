"""Tests for LinkedIn poster."""

import pytest
from unittest.mock import MagicMock, patch
from socialia.linkedin import LinkedInPoster


class TestLinkedInPoster:
    """Test LinkedInPoster class."""

    def test_init_with_token(self, linkedin_credentials):
        """Test initialization with explicit token."""
        poster = LinkedInPoster(**linkedin_credentials)
        assert poster.access_token == "test_linkedin_token"

    def test_init_from_environment(self, monkeypatch):
        """Test initialization from environment variables."""
        monkeypatch.setenv("LINKEDIN_ACCESS_TOKEN", "env_token")
        poster = LinkedInPoster()
        assert poster.access_token == "env_token"

    def test_validate_credentials_valid(self, linkedin_credentials):
        """Test credential validation with valid token."""
        poster = LinkedInPoster(**linkedin_credentials)
        assert poster.validate_credentials() is True

    def test_validate_credentials_missing(self):
        """Test credential validation with missing token."""
        poster = LinkedInPoster()
        assert poster.validate_credentials() is False

    def test_post_missing_credentials(self):
        """Test post fails with missing credentials."""
        poster = LinkedInPoster()
        result = poster.post("Test")
        assert result["success"] is False
        assert "token" in result["error"].lower()

    @patch("socialia.linkedin.requests")
    def test_get_user_urn_success(self, mock_requests, linkedin_credentials):
        """Test successful user URN retrieval."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"id": "user123"}
        mock_requests.get.return_value = mock_response

        poster = LinkedInPoster(**linkedin_credentials)
        user_urn = poster._get_user_urn()

        assert user_urn == "urn:li:person:user123"

    @patch("socialia.linkedin.requests")
    def test_post_success(self, mock_requests, linkedin_credentials):
        """Test successful post."""
        # Mock user URN call
        mock_user_response = MagicMock()
        mock_user_response.status_code = 200
        mock_user_response.json.return_value = {"id": "user123"}

        # Mock post call
        mock_post_response = MagicMock()
        mock_post_response.status_code = 201
        mock_post_response.headers = {"X-RestLi-Id": "share123"}
        mock_post_response.json.return_value = {}

        mock_requests.get.return_value = mock_user_response
        mock_requests.post.return_value = mock_post_response

        poster = LinkedInPoster(**linkedin_credentials)
        result = poster.post("Hello LinkedIn!")

        assert result["success"] is True
        assert result["id"] == "share123"

    @patch("socialia.linkedin.requests")
    def test_post_failure(self, mock_requests, linkedin_credentials):
        """Test failed post."""
        # Mock user URN call
        mock_user_response = MagicMock()
        mock_user_response.status_code = 200
        mock_user_response.json.return_value = {"id": "user123"}

        # Mock failed post call
        mock_post_response = MagicMock()
        mock_post_response.status_code = 401
        mock_post_response.text = "Unauthorized"

        mock_requests.get.return_value = mock_user_response
        mock_requests.post.return_value = mock_post_response

        poster = LinkedInPoster(**linkedin_credentials)
        result = poster.post("Test post")

        assert result["success"] is False
        assert "401" in result["error"]

    @patch("socialia.linkedin.requests")
    def test_delete_success(self, mock_requests, linkedin_credentials):
        """Test successful delete."""
        mock_response = MagicMock()
        mock_response.status_code = 204

        mock_requests.delete.return_value = mock_response

        poster = LinkedInPoster(**linkedin_credentials)
        result = poster.delete("share123")

        assert result["success"] is True
        assert result["deleted"] is True

    @patch("socialia.linkedin.requests")
    def test_delete_failure(self, mock_requests, linkedin_credentials):
        """Test failed delete."""
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.text = "Not Found"

        mock_requests.delete.return_value = mock_response

        poster = LinkedInPoster(**linkedin_credentials)
        result = poster.delete("invalid_id")

        assert result["success"] is False
        assert "404" in result["error"]
