"""Optional GetXAPI-backed Twitter read backend."""

from __future__ import annotations

from typing import Any, Optional
from urllib.parse import quote, urljoin

import requests

from ._branding import get_env
from ._twitter_read_backend import _find_list, _normalize_tweet

DEFAULT_BASE_URL = "https://api.getxapi.com"
TIMEOUT_SECONDS = 30


class GetXAPIReadBackend:
    """Small adapter for read-only X endpoints exposed through GetXAPI."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        http: Optional[Any] = None,
    ) -> None:
        self.api_key = (
            api_key
            or get_env("GETXAPI_API_KEY")
            or get_env("GETXAPI_KEY")
            or ""
        )
        self.base_url = (
            base_url
            or get_env("GETXAPI_BASE_URL")
            or DEFAULT_BASE_URL
        ).rstrip("/")
        self._http = http or requests

    def available(self) -> bool:
        return bool(self.api_key)

    def _headers(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self.api_key}"}

    def _get(self, path: str, params: Optional[dict[str, Any]] = None) -> dict:
        if not self.available():
            return {
                "success": False,
                "error": "GETXAPI_API_KEY is not configured.",
            }
        url = urljoin(f"{self.base_url}/", path.lstrip("/"))
        response = self._http.get(
            url,
            params=params or {},
            headers=self._headers(),
            timeout=TIMEOUT_SECONDS,
        )
        try:
            payload = response.json()
        except ValueError:
            payload = {"text": response.text}
        if response.status_code < 200 or response.status_code >= 300:
            return {
                "success": False,
                "error": f"{response.status_code}: {response.text}",
                "status_code": response.status_code,
                "response": payload,
            }
        return payload if isinstance(payload, dict) else {"data": payload}

    def _tweets_result(
        self, payload: dict, key: str, limit: Optional[int] = None
    ) -> dict:
        if payload.get("success") is False:
            return payload
        items = _find_list(payload, ("tweets", key, "data", "results", "items"))
        tweets = [_normalize_tweet(item) for item in items if isinstance(item, dict)]
        if limit is not None:
            tweets = tweets[: max(1, min(limit, 100))]
        return {"success": True, key: tweets, "count": len(tweets)}

    def search_tweets(
        self, query: str, limit: int = 10, include_users: bool = True
    ) -> dict:
        _ = include_users
        payload = self._get(
            "/twitter/tweet/advanced_search",
            params={"q": query, "limit": max(1, min(limit, 100))},
        )
        return self._tweets_result(payload, "tweets")

    def user_tweets(self, username: str, limit: int = 10) -> dict:
        handle = quote(username.lstrip("@"))
        payload = self._get(
            "/twitter/tweet/advanced_search",
            params={
                "q": f"from:{handle} -filter:replies",
                "limit": max(1, min(limit, 100)),
            },
        )
        return self._tweets_result(payload, "tweets", limit=limit)

    def mentions(self, username: str, limit: int = 10) -> dict:
        handle = username.lstrip("@")
        payload = self._get(
            "/twitter/tweet/advanced_search",
            params={
                "q": f"@{handle} -from:{handle}",
                "limit": max(1, min(limit, 100)),
            },
        )
        return self._tweets_result(payload, "mentions", limit=limit)

    def replies(self, username: str, limit: int = 10) -> dict:
        result = self.search_tweets(
            f"to:{username.lstrip('@')} -from:{username.lstrip('@')}",
            limit=limit,
            include_users=True,
        )
        if not result.get("success"):
            return result
        replies = result.get("tweets", [])
        return {"success": True, "replies": replies, "count": len(replies)}
