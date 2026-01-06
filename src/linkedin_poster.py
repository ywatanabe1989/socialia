#!/usr/bin/env python3
"""
LinkedIn Poster - Post to LinkedIn using the official API.

Note: Requires developer approval for w_member_social permission.
Token expires every 60 days.

Environment Variables:
    LINKEDIN_ACCESS_TOKEN: OAuth access token
    LINKEDIN_AUTHOR_URN: Author URN (optional, fetched if not provided)
"""

from typing import Optional

from .base import BasePoster, PostResult

try:
    import requests
except ImportError:
    requests = None


class LinkedInPoster(BasePoster):
    """Post to LinkedIn using the official Marketing API."""

    platform_name = "linkedin"
    BASE_URL = "https://api.linkedin.com/v2"
    API_VERSION = "202501"

    def __init__(self, env_path: Optional[str] = None):
        super().__init__(env_path)
        self.access_token = None
        self.author_urn = None
        self.headers = {}

    def initialize(self) -> bool:
        """Initialize LinkedIn API client."""
        if requests is None:
            self.logger.error("requests not installed. Run: pip install requests")
            return False

        try:
            self.access_token = self._get_env("LINKEDIN_ACCESS_TOKEN")
            self.headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json",
                "X-Restli-Protocol-Version": "2.0.0",
                "LinkedIn-Version": self.API_VERSION,
            }

            # Get author URN
            self.author_urn = self._get_env("LINKEDIN_AUTHOR_URN", required=False)
            if not self.author_urn:
                self.author_urn = self._fetch_author_urn()

            self._initialized = True
            self.logger.info("LinkedIn API initialized")
            return True

        except Exception as e:
            self.logger.error(f"Failed to initialize LinkedIn API: {e}")
            return False

    def _fetch_author_urn(self) -> Optional[str]:
        """Fetch author URN from API."""
        try:
            response = requests.get(
                f"{self.BASE_URL}/userinfo",
                headers=self.headers,
            )
            response.raise_for_status()
            user_id = response.json()["sub"]
            return f"urn:li:person:{user_id}"
        except Exception as e:
            self.logger.error(f"Failed to fetch author URN: {e}")
            return None

    def verify_credentials(self) -> bool:
        """Verify API credentials are valid."""
        if not self._initialized:
            if not self.initialize():
                return False

        try:
            response = requests.get(
                f"{self.BASE_URL}/userinfo",
                headers=self.headers,
            )
            response.raise_for_status()
            user = response.json()
            self.logger.info(f"Authenticated as {user.get('name', 'Unknown')}")
            return True
        except Exception as e:
            self.logger.error(f"Credential verification failed: {e}")
            return False

    def post_text(self, text: str, **kwargs) -> PostResult:
        """
        Post a text update to LinkedIn.

        Args:
            text: Post content
            visibility: "PUBLIC" or "CONNECTIONS" (default: PUBLIC)

        Returns:
            PostResult with post URN
        """
        if not self._initialized:
            if not self.initialize():
                return self._failed("Failed to initialize LinkedIn API")

        if not self.author_urn:
            return self._failed("Author URN not available")

        visibility = kwargs.get("visibility", "PUBLIC")

        post_data = {
            "author": self.author_urn,
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {"text": text},
                    "shareMediaCategory": "NONE",
                }
            },
            "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": visibility},
        }

        try:
            response = requests.post(
                f"{self.BASE_URL}/ugcPosts",
                headers=self.headers,
                json=post_data,
            )

            if response.status_code == 201:
                post_urn = response.headers.get("X-RestLi-Id", "")
                self.logger.info(f"Posted to LinkedIn: {post_urn}")
                return self._success(
                    post_id=post_urn,
                    url=f"https://www.linkedin.com/feed/update/{post_urn}",
                    text=text,
                )
            else:
                error = response.json().get("message", response.text)
                return self._failed(f"API error: {error}")

        except Exception as e:
            self.logger.error(f"Failed to post to LinkedIn: {e}")
            return self._failed(str(e))

    def post_link(self, text: str, url: str, **kwargs) -> PostResult:
        """
        Post with a link/article.

        Args:
            text: Post commentary
            url: Link URL to share
            title: Optional title for the link
            description: Optional description

        Returns:
            PostResult with post URN
        """
        if not self._initialized:
            if not self.initialize():
                return self._failed("Failed to initialize LinkedIn API")

        if not self.author_urn:
            return self._failed("Author URN not available")

        visibility = kwargs.get("visibility", "PUBLIC")

        post_data = {
            "author": self.author_urn,
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {"text": text},
                    "shareMediaCategory": "ARTICLE",
                    "media": [
                        {
                            "status": "READY",
                            "originalUrl": url,
                            "title": {"text": kwargs.get("title", "")},
                            "description": {"text": kwargs.get("description", "")},
                        }
                    ],
                }
            },
            "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": visibility},
        }

        try:
            response = requests.post(
                f"{self.BASE_URL}/ugcPosts",
                headers=self.headers,
                json=post_data,
            )

            if response.status_code == 201:
                post_urn = response.headers.get("X-RestLi-Id", "")
                self.logger.info(f"Posted link to LinkedIn: {post_urn}")
                return self._success(
                    post_id=post_urn,
                    url=f"https://www.linkedin.com/feed/update/{post_urn}",
                    link_url=url,
                )
            else:
                error = response.json().get("message", response.text)
                return self._failed(f"API error: {error}")

        except Exception as e:
            self.logger.error(f"Failed to post link to LinkedIn: {e}")
            return self._failed(str(e))

    def post_with_image(self, text: str, image_path: str, **kwargs) -> PostResult:
        """
        Post with an image.

        Note: LinkedIn requires uploading image first, then creating post.
        This is a simplified version - for production, implement full upload flow.

        Args:
            text: Post commentary
            image_path: Path to image (must be publicly accessible URL for now)

        Returns:
            PostResult with post URN
        """
        # LinkedIn image upload requires:
        # 1. Register upload
        # 2. Upload binary
        # 3. Create post with asset URN
        # For simplicity, treating image_path as URL
        self.logger.warning(
            "LinkedIn image upload requires public URL. "
            "For local files, implement full upload flow."
        )

        if image_path.startswith("http"):
            return self._post_with_image_url(text, image_path, **kwargs)
        else:
            return self._failed(
                "Local image upload not implemented. Use public URL or "
                "implement RegisterUpload flow."
            )

    def _post_with_image_url(self, text: str, image_url: str, **kwargs) -> PostResult:
        """Post with image from URL."""
        if not self._initialized:
            if not self.initialize():
                return self._failed("Failed to initialize LinkedIn API")

        if not self.author_urn:
            return self._failed("Author URN not available")

        post_data = {
            "author": self.author_urn,
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {"text": text},
                    "shareMediaCategory": "IMAGE",
                    "media": [
                        {
                            "status": "READY",
                            "originalUrl": image_url,
                        }
                    ],
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": kwargs.get(
                    "visibility", "PUBLIC"
                )
            },
        }

        try:
            response = requests.post(
                f"{self.BASE_URL}/ugcPosts",
                headers=self.headers,
                json=post_data,
            )

            if response.status_code == 201:
                post_urn = response.headers.get("X-RestLi-Id", "")
                return self._success(
                    post_id=post_urn,
                    url=f"https://www.linkedin.com/feed/update/{post_urn}",
                    image_url=image_url,
                )
            else:
                error = response.json().get("message", response.text)
                return self._failed(f"API error: {error}")

        except Exception as e:
            self.logger.error(f"Failed to post image to LinkedIn: {e}")
            return self._failed(str(e))

    def post_to_organization(
        self, text: str, organization_urn: str, **kwargs
    ) -> PostResult:
        """
        Post on behalf of an organization/company page.

        Args:
            text: Post content
            organization_urn: Organization URN (urn:li:organization:XXXXX)
            **kwargs: Same as post_text

        Returns:
            PostResult with post URN
        """
        if not self._initialized:
            if not self.initialize():
                return self._failed("Failed to initialize LinkedIn API")

        visibility = kwargs.get("visibility", "PUBLIC")

        post_data = {
            "author": organization_urn,
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {"text": text},
                    "shareMediaCategory": "NONE",
                }
            },
            "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": visibility},
        }

        try:
            response = requests.post(
                f"{self.BASE_URL}/ugcPosts",
                headers=self.headers,
                json=post_data,
            )

            if response.status_code == 201:
                post_urn = response.headers.get("X-RestLi-Id", "")
                self.logger.info(f"Posted to organization: {post_urn}")
                return self._success(
                    post_id=post_urn,
                    url=f"https://www.linkedin.com/feed/update/{post_urn}",
                    organization=organization_urn,
                )
            else:
                error = response.json().get("message", response.text)
                return self._failed(f"API error: {error}")

        except Exception as e:
            self.logger.error(f"Failed to post to organization: {e}")
            return self._failed(str(e))
