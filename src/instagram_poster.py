#!/usr/bin/env python3
"""
Instagram Poster - Post to Instagram using Meta Graph API.

Requirements:
    - Instagram Business or Creator account
    - Facebook Page connected to Instagram
    - Meta App with instagram_content_publish permission

Environment Variables:
    INSTAGRAM_ACCESS_TOKEN: Long-lived access token
    INSTAGRAM_ACCOUNT_ID: Instagram Business Account ID
"""

from typing import Optional, List
import time

from .base import BasePoster, PostResult

try:
    import requests
except ImportError:
    requests = None


class InstagramPoster(BasePoster):
    """Post to Instagram using Meta Graph API."""

    platform_name = "instagram"
    BASE_URL = "https://graph.facebook.com/v18.0"

    def __init__(self, env_path: Optional[str] = None):
        super().__init__(env_path)
        self.access_token = None
        self.account_id = None

    def initialize(self) -> bool:
        """Initialize Instagram API client."""
        if requests is None:
            self.logger.error("requests not installed. Run: pip install requests")
            return False

        try:
            self.access_token = self._get_env("INSTAGRAM_ACCESS_TOKEN")
            self.account_id = self._get_env("INSTAGRAM_ACCOUNT_ID")

            self._initialized = True
            self.logger.info("Instagram API initialized")
            return True

        except Exception as e:
            self.logger.error(f"Failed to initialize Instagram API: {e}")
            return False

    def verify_credentials(self) -> bool:
        """Verify API credentials are valid."""
        if not self._initialized:
            if not self.initialize():
                return False

        try:
            response = requests.get(
                f"{self.BASE_URL}/{self.account_id}",
                params={
                    "fields": "username,name",
                    "access_token": self.access_token,
                },
            )
            response.raise_for_status()
            user = response.json()
            self.logger.info(f"Authenticated as @{user.get('username', 'Unknown')}")
            return True
        except Exception as e:
            self.logger.error(f"Credential verification failed: {e}")
            return False

    def post_text(self, text: str, **kwargs) -> PostResult:
        """
        Instagram doesn't support text-only posts.
        Use post_with_image instead.
        """
        return self._failed("Instagram requires an image or video for posts")

    def post_with_image(self, text: str, image_path: str, **kwargs) -> PostResult:
        """
        Post an image to Instagram.

        Note: image_path must be a publicly accessible URL.
        Instagram fetches the image from the URL.

        Args:
            text: Caption for the post
            image_path: Public URL to the image

        Returns:
            PostResult with post ID
        """
        if not self._initialized:
            if not self.initialize():
                return self._failed("Failed to initialize Instagram API")

        if not image_path.startswith("http"):
            return self._failed(
                "Instagram requires a public URL for images. "
                "Upload image to a public server first."
            )

        try:
            # Step 1: Create media container
            container_response = requests.post(
                f"{self.BASE_URL}/{self.account_id}/media",
                params={
                    "image_url": image_path,
                    "caption": text,
                    "access_token": self.access_token,
                },
            )
            container_response.raise_for_status()
            creation_id = container_response.json()["id"]

            # Step 2: Wait for container to be ready (optional polling)
            time.sleep(2)

            # Step 3: Publish the container
            publish_response = requests.post(
                f"{self.BASE_URL}/{self.account_id}/media_publish",
                params={
                    "creation_id": creation_id,
                    "access_token": self.access_token,
                },
            )
            publish_response.raise_for_status()
            media_id = publish_response.json()["id"]

            self.logger.info(f"Posted to Instagram: {media_id}")
            return self._success(
                post_id=media_id,
                url=f"https://www.instagram.com/p/{media_id}/",
                caption=text,
                image_url=image_path,
            )

        except Exception as e:
            self.logger.error(f"Failed to post to Instagram: {e}")
            return self._failed(str(e))

    def post_with_images(
        self, text: str, image_paths: List[str], **kwargs
    ) -> PostResult:
        """
        Post a carousel (multiple images) to Instagram.

        Args:
            text: Caption for the carousel
            image_paths: List of public image URLs (2-10 images)

        Returns:
            PostResult with post ID
        """
        if not self._initialized:
            if not self.initialize():
                return self._failed("Failed to initialize Instagram API")

        if len(image_paths) < 2:
            return self.post_with_image(text, image_paths[0], **kwargs)

        if len(image_paths) > 10:
            self.logger.warning("Instagram carousels support max 10 images")
            image_paths = image_paths[:10]

        # Validate all are URLs
        for path in image_paths:
            if not path.startswith("http"):
                return self._failed("All images must be public URLs")

        try:
            # Step 1: Create container for each image
            children_ids = []
            for url in image_paths:
                container = requests.post(
                    f"{self.BASE_URL}/{self.account_id}/media",
                    params={
                        "image_url": url,
                        "is_carousel_item": True,
                        "access_token": self.access_token,
                    },
                )
                container.raise_for_status()
                children_ids.append(container.json()["id"])

            # Step 2: Create carousel container
            carousel = requests.post(
                f"{self.BASE_URL}/{self.account_id}/media",
                params={
                    "media_type": "CAROUSEL",
                    "children": ",".join(children_ids),
                    "caption": text,
                    "access_token": self.access_token,
                },
            )
            carousel.raise_for_status()
            creation_id = carousel.json()["id"]

            time.sleep(2)

            # Step 3: Publish
            publish = requests.post(
                f"{self.BASE_URL}/{self.account_id}/media_publish",
                params={
                    "creation_id": creation_id,
                    "access_token": self.access_token,
                },
            )
            publish.raise_for_status()
            media_id = publish.json()["id"]

            self.logger.info(f"Posted carousel to Instagram: {media_id}")
            return self._success(
                post_id=media_id,
                caption=text,
                image_count=len(image_paths),
            )

        except Exception as e:
            self.logger.error(f"Failed to post carousel to Instagram: {e}")
            return self._failed(str(e))

    def post_reel(self, caption: str, video_url: str, **kwargs) -> PostResult:
        """
        Post a Reel to Instagram.

        Args:
            caption: Reel caption
            video_url: Public URL to the video
            cover_url: Optional cover image URL
            share_to_feed: Whether to share to feed (default: True)

        Returns:
            PostResult with reel ID
        """
        if not self._initialized:
            if not self.initialize():
                return self._failed("Failed to initialize Instagram API")

        if not video_url.startswith("http"):
            return self._failed("Video must be a public URL")

        try:
            params = {
                "media_type": "REELS",
                "video_url": video_url,
                "caption": caption,
                "share_to_feed": kwargs.get("share_to_feed", True),
                "access_token": self.access_token,
            }

            if kwargs.get("cover_url"):
                params["cover_url"] = kwargs["cover_url"]

            # Create container
            container = requests.post(
                f"{self.BASE_URL}/{self.account_id}/media",
                params=params,
            )
            container.raise_for_status()
            creation_id = container.json()["id"]

            # Wait for processing
            time.sleep(5)

            # Publish
            publish = requests.post(
                f"{self.BASE_URL}/{self.account_id}/media_publish",
                params={
                    "creation_id": creation_id,
                    "access_token": self.access_token,
                },
            )
            publish.raise_for_status()
            media_id = publish.json()["id"]

            self.logger.info(f"Posted Reel to Instagram: {media_id}")
            return self._success(
                post_id=media_id,
                caption=caption,
                video_url=video_url,
            )

        except Exception as e:
            self.logger.error(f"Failed to post Reel: {e}")
            return self._failed(str(e))

    def post_story(self, image_url: str, **kwargs) -> PostResult:
        """
        Post a Story to Instagram.

        Args:
            image_url: Public URL to the image

        Returns:
            PostResult with story ID
        """
        if not self._initialized:
            if not self.initialize():
                return self._failed("Failed to initialize Instagram API")

        try:
            # Create story container
            container = requests.post(
                f"{self.BASE_URL}/{self.account_id}/media",
                params={
                    "media_type": "STORIES",
                    "image_url": image_url,
                    "access_token": self.access_token,
                },
            )
            container.raise_for_status()
            creation_id = container.json()["id"]

            time.sleep(2)

            # Publish
            publish = requests.post(
                f"{self.BASE_URL}/{self.account_id}/media_publish",
                params={
                    "creation_id": creation_id,
                    "access_token": self.access_token,
                },
            )
            publish.raise_for_status()
            media_id = publish.json()["id"]

            self.logger.info(f"Posted Story to Instagram: {media_id}")
            return self._success(
                post_id=media_id,
                image_url=image_url,
            )

        except Exception as e:
            self.logger.error(f"Failed to post Story: {e}")
            return self._failed(str(e))
