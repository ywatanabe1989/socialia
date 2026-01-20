"""Twitter/X API v2 poster."""

import os
from typing import Optional
from requests_oauthlib import OAuth1Session

from .base import BasePoster


class TwitterPoster(BasePoster):
    """Twitter/X API v2 poster using OAuth 1.0a."""

    POST_ENDPOINT = "https://api.x.com/2/tweets"
    DELETE_ENDPOINT = "https://api.x.com/2/tweets/{tweet_id}"

    def __init__(
        self,
        consumer_key: Optional[str] = None,
        consumer_secret: Optional[str] = None,
        access_token: Optional[str] = None,
        access_token_secret: Optional[str] = None,
    ):
        self.consumer_key = consumer_key or os.environ.get("SCITEX_X_CONSUMER_KEY")
        self.consumer_secret = consumer_secret or os.environ.get(
            "SCITEX_X_CONSUMER_KEY_SECRET"
        )
        self.access_token = access_token or os.environ.get("SCITEX_X_ACCESSTOKEN")
        self.access_token_secret = access_token_secret or os.environ.get(
            "SCITEX_X_ACCESSTOKEN_SECRET"
        )

    def _get_session(self) -> OAuth1Session:
        """Create OAuth1 session."""
        return OAuth1Session(
            self.consumer_key,
            client_secret=self.consumer_secret,
            resource_owner_key=self.access_token,
            resource_owner_secret=self.access_token_secret,
        )

    def validate_credentials(self) -> bool:
        """Check if all credentials are set."""
        return all(
            [
                self.consumer_key,
                self.consumer_secret,
                self.access_token,
                self.access_token_secret,
            ]
        )

    def post(
        self,
        text: str,
        reply_to: Optional[str] = None,
        quote_tweet_id: Optional[str] = None,
    ) -> dict:
        """
        Post a tweet.

        Args:
            text: Tweet content (max 280 chars standard, 25000 premium)
            reply_to: Tweet ID to reply to
            quote_tweet_id: Tweet ID to quote

        Returns:
            dict with 'success', 'id', 'url' or 'error'
        """
        if not self.validate_credentials():
            return {"success": False, "error": "Missing credentials"}

        oauth = self._get_session()
        payload = {"text": text}

        if reply_to:
            payload["reply"] = {"in_reply_to_tweet_id": reply_to}
        if quote_tweet_id:
            payload["quote_tweet_id"] = quote_tweet_id

        response = oauth.post(self.POST_ENDPOINT, json=payload)

        if response.status_code == 201:
            data = response.json()
            tweet_id = data["data"]["id"]
            return {
                "success": True,
                "id": tweet_id,
                "url": f"https://x.com/i/web/status/{tweet_id}",
            }
        else:
            return {
                "success": False,
                "error": f"{response.status_code}: {response.text}",
            }

    def delete(self, post_id: str) -> dict:
        """
        Delete a tweet.

        Args:
            post_id: Tweet ID to delete

        Returns:
            dict with 'success' and 'deleted' or 'error'
        """
        if not self.validate_credentials():
            return {"success": False, "error": "Missing credentials"}

        oauth = self._get_session()
        url = self.DELETE_ENDPOINT.format(tweet_id=post_id)
        response = oauth.delete(url)

        if response.status_code == 200:
            return {"success": True, "deleted": True}
        else:
            return {
                "success": False,
                "error": f"{response.status_code}: {response.text}",
            }

    def post_thread(self, tweets: list[str]) -> dict:
        """
        Post a thread of tweets.

        Args:
            tweets: List of tweet texts

        Returns:
            dict with 'success', 'ids', 'urls' or 'error'
        """
        ids = []
        urls = []
        reply_to = None

        for i, text in enumerate(tweets):
            result = self.post(text, reply_to=reply_to)
            if result["success"]:
                ids.append(result["id"])
                urls.append(result["url"])
                reply_to = result["id"]
            else:
                return {
                    "success": False,
                    "error": f"Failed at tweet {i + 1}: {result['error']}",
                    "partial_ids": ids,
                }

        return {"success": True, "ids": ids, "urls": urls}
