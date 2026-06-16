"""Tests for the optional GetXAPI Twitter read backend."""

from socialia._twitter_read_backend_getxapi import GetXAPIReadBackend

from tests.conftest import FakeResponse


class FakeHTTP:
    def __init__(self, response):
        self.response = response
        self.calls = []

    def get(self, *args, **kwargs):
        self.calls.append((args, kwargs))
        return self.response


class TestGetXAPIReadBackend:
    def test_available_returns_false_without_api_key(self):
        # Arrange
        backend = GetXAPIReadBackend(api_key="", http=FakeHTTP(FakeResponse(200)))
        # Act
        available = backend.available()
        # Assert
        assert available is False

    def test_search_uses_authorization_bearer_header(self):
        # Arrange
        http = FakeHTTP(FakeResponse(200, json_data={"tweets": []}))
        backend = GetXAPIReadBackend(
            api_key="gx_test", base_url="https://x", http=http
        )
        # Act
        backend.search_tweets("agents", limit=3)
        # Assert
        assert http.calls[0][1]["headers"]["Authorization"] == "Bearer gx_test"

    def test_search_normalizes_tweets(self):
        # Arrange
        http = FakeHTTP(
            FakeResponse(
                200,
                json_data={
                    "data": [
                        {
                            "tweetId": "42",
                            "fullText": "Research thread",
                            "createdAt": "2026-01-01T00:00:00Z",
                            "user": {"username": "alice", "name": "Alice"},
                            "metrics": {"like_count": 7, "retweet_count": 2},
                        }
                    ]
                },
            )
        )
        backend = GetXAPIReadBackend(
            api_key="gx_test", base_url="https://x", http=http
        )
        # Act
        result = backend.search_tweets("research")
        tweet = result["tweets"][0]
        # Assert
        assert (tweet["id"], tweet["author_username"], tweet["likes"]) == (
            "42",
            "alice",
            7,
        )

    def test_user_tweets_builds_advanced_search_query(self):
        # Arrange
        http = FakeHTTP(FakeResponse(200, json_data={"tweets": []}))
        backend = GetXAPIReadBackend(
            api_key="gx_test", base_url="https://x", http=http
        )
        # Act
        backend.user_tweets("@alice", limit=5)
        # Assert
        assert (http.calls[0][0][0], http.calls[0][1]["params"]["q"]) == (
            "https://x/twitter/tweet/advanced_search",
            "from:alice -filter:replies",
        )

    def test_error_status_returns_failure(self):
        # Arrange
        http = FakeHTTP(
            FakeResponse(402, json_data={"error": "credits"}, text="Payment")
        )
        backend = GetXAPIReadBackend(
            api_key="gx_test", base_url="https://x", http=http
        )
        # Act
        result = backend.search_tweets("research")
        # Assert
        assert result["success"] is False
