"""Pytest fixtures for socialia tests."""

import pytest
from unittest.mock import MagicMock, patch


@pytest.fixture
def mock_oauth_session():
    """Mock OAuth1Session for Twitter tests."""
    with patch("socialia.twitter.OAuth1Session") as mock:
        session = MagicMock()
        mock.return_value = session
        yield session


@pytest.fixture
def mock_requests():
    """Mock requests for LinkedIn tests."""
    with patch("socialia.linkedin.requests") as mock:
        yield mock


@pytest.fixture
def twitter_credentials():
    """Provide test Twitter credentials."""
    return {
        "consumer_key": "test_consumer_key",
        "consumer_secret": "test_consumer_secret",
        "access_token": "test_access_token",
        "access_token_secret": "test_access_token_secret",
    }


@pytest.fixture
def linkedin_credentials():
    """Provide test LinkedIn credentials."""
    return {
        "access_token": "test_linkedin_token",
    }
