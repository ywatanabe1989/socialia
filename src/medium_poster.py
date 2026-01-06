#!/usr/bin/env python3
"""
Medium Poster - Post articles to Medium.

Note: Medium's official API is deprecated but still functional.
Only supports creating posts, not updating or deleting.

Environment Variables:
    MEDIUM_INTEGRATION_TOKEN: Integration token from Medium settings
    MEDIUM_AUTHOR_ID: Author ID (optional, can be fetched)
"""

from typing import Optional, List

from .base import BasePoster, PostResult

try:
    import requests
except ImportError:
    requests = None


class MediumPoster(BasePoster):
    """Post articles to Medium using the (deprecated) official API."""

    platform_name = "medium"
    BASE_URL = "https://api.medium.com/v1"

    def __init__(self, env_path: Optional[str] = None):
        super().__init__(env_path)
        self.token = None
        self.author_id = None
        self.headers = {}

    def initialize(self) -> bool:
        """Initialize Medium API client."""
        if requests is None:
            self.logger.error("requests not installed. Run: pip install requests")
            return False

        try:
            self.token = self._get_env("MEDIUM_INTEGRATION_TOKEN")
            self.headers = {
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            }

            # Try to get author ID from env or fetch it
            self.author_id = self._get_env("MEDIUM_AUTHOR_ID", required=False)
            if not self.author_id:
                self.author_id = self._fetch_author_id()

            self._initialized = True
            self.logger.info("Medium API initialized")
            return True

        except Exception as e:
            self.logger.error(f"Failed to initialize Medium API: {e}")
            return False

    def _fetch_author_id(self) -> Optional[str]:
        """Fetch author ID from API."""
        try:
            response = requests.get(
                f"{self.BASE_URL}/me",
                headers=self.headers,
            )
            response.raise_for_status()
            return response.json()["data"]["id"]
        except Exception as e:
            self.logger.error(f"Failed to fetch author ID: {e}")
            return None

    def verify_credentials(self) -> bool:
        """Verify API credentials are valid."""
        if not self._initialized:
            if not self.initialize():
                return False

        try:
            response = requests.get(
                f"{self.BASE_URL}/me",
                headers=self.headers,
            )
            response.raise_for_status()
            user = response.json()["data"]
            self.logger.info(f"Authenticated as {user['name']} (@{user['username']})")
            return True
        except Exception as e:
            self.logger.error(f"Credential verification failed: {e}")
            return False

    def post_text(self, text: str, **kwargs) -> PostResult:
        """
        Post an article to Medium.

        Args:
            text: Article content (markdown or HTML)
            title: Article title (required)
            content_format: "markdown" or "html" (default: markdown)
            publish_status: "draft", "public", or "unlisted" (default: draft)
            tags: List of tags (max 5)
            canonical_url: Original URL if cross-posting

        Returns:
            PostResult with article URL
        """
        if not self._initialized:
            if not self.initialize():
                return self._failed("Failed to initialize Medium API")

        title = kwargs.get("title")
        if not title:
            return self._failed("title parameter is required")

        content_format = kwargs.get("content_format", "markdown")
        publish_status = kwargs.get("publish_status", "draft")
        tags = kwargs.get("tags", [])[:5]  # Max 5 tags

        post_data = {
            "title": title,
            "contentFormat": content_format,
            "content": text,
            "publishStatus": publish_status,
            "tags": tags,
        }

        if kwargs.get("canonical_url"):
            post_data["canonicalUrl"] = kwargs["canonical_url"]

        try:
            response = requests.post(
                f"{self.BASE_URL}/users/{self.author_id}/posts",
                headers=self.headers,
                json=post_data,
            )

            if response.status_code == 201:
                data = response.json()["data"]
                self.logger.info(f"Posted to Medium: {data['url']}")
                return self._success(
                    post_id=data["id"],
                    url=data["url"],
                    title=title,
                    publish_status=data["publishStatus"],
                )
            else:
                error = (
                    response.json()
                    .get("errors", [{}])[0]
                    .get("message", "Unknown error")
                )
                return self._failed(f"API error: {error}")

        except Exception as e:
            self.logger.error(f"Failed to post to Medium: {e}")
            return self._failed(str(e))

    def post_to_publication(
        self, text: str, publication_id: str, **kwargs
    ) -> PostResult:
        """
        Post an article to a Medium publication.

        Args:
            text: Article content
            publication_id: Publication ID to post to
            **kwargs: Same as post_text

        Returns:
            PostResult with article URL
        """
        if not self._initialized:
            if not self.initialize():
                return self._failed("Failed to initialize Medium API")

        title = kwargs.get("title")
        if not title:
            return self._failed("title parameter is required")

        post_data = {
            "title": title,
            "contentFormat": kwargs.get("content_format", "markdown"),
            "content": text,
            "publishStatus": kwargs.get("publish_status", "draft"),
            "tags": kwargs.get("tags", [])[:5],
        }

        try:
            response = requests.post(
                f"{self.BASE_URL}/publications/{publication_id}/posts",
                headers=self.headers,
                json=post_data,
            )

            if response.status_code == 201:
                data = response.json()["data"]
                self.logger.info(f"Posted to publication: {data['url']}")
                return self._success(
                    post_id=data["id"],
                    url=data["url"],
                    title=title,
                    publication_id=publication_id,
                )
            else:
                error = response.json().get("errors", [{}])[0].get("message", "Unknown")
                return self._failed(f"API error: {error}")

        except Exception as e:
            self.logger.error(f"Failed to post to publication: {e}")
            return self._failed(str(e))

    def get_publications(self) -> List[dict]:
        """
        Get list of publications the user can write to.

        Returns:
            List of publication dicts with id, name, etc.
        """
        if not self._initialized:
            if not self.initialize():
                return []

        try:
            response = requests.get(
                f"{self.BASE_URL}/users/{self.author_id}/publications",
                headers=self.headers,
            )
            response.raise_for_status()
            return response.json()["data"]
        except Exception as e:
            self.logger.error(f"Failed to get publications: {e}")
            return []

    def create_draft(self, title: str, content: str, **kwargs) -> PostResult:
        """
        Convenience method to create a draft article.

        Args:
            title: Article title
            content: Article content (markdown)
            **kwargs: Additional options

        Returns:
            PostResult with draft URL
        """
        return self.post_text(
            content,
            title=title,
            publish_status="draft",
            **kwargs,
        )
