#!/usr/bin/env python3
"""
TikTok Poster - Post to TikTok using the Content Posting API.

Note: Unaudited apps can only post with SELF_ONLY privacy.
Submit for audit to enable PUBLIC_TO_EVERYONE.

Environment Variables:
    TIKTOK_CLIENT_KEY: App client key
    TIKTOK_CLIENT_SECRET: App client secret
    TIKTOK_ACCESS_TOKEN: User access token
"""

from typing import Optional
import os
import time

from .base import BasePoster, PostResult

try:
    import requests
except ImportError:
    requests = None


class TikTokPoster(BasePoster):
    """Post to TikTok using the Content Posting API."""

    platform_name = "tiktok"
    BASE_URL = "https://open.tiktokapis.com/v2"

    def __init__(self, env_path: Optional[str] = None):
        super().__init__(env_path)
        self.client_key = None
        self.client_secret = None
        self.access_token = None

    def initialize(self) -> bool:
        """Initialize TikTok API client."""
        if requests is None:
            self.logger.error("requests not installed. Run: pip install requests")
            return False

        try:
            self.client_key = self._get_env("TIKTOK_CLIENT_KEY")
            self.client_secret = self._get_env("TIKTOK_CLIENT_SECRET")
            self.access_token = self._get_env("TIKTOK_ACCESS_TOKEN")

            self._initialized = True
            self.logger.info("TikTok API initialized")
            return True

        except Exception as e:
            self.logger.error(f"Failed to initialize TikTok API: {e}")
            return False

    def verify_credentials(self) -> bool:
        """Verify API credentials are valid."""
        if not self._initialized:
            if not self.initialize():
                return False

        try:
            response = requests.get(
                f"{self.BASE_URL}/user/info/",
                headers={"Authorization": f"Bearer {self.access_token}"},
                params={"fields": "display_name,avatar_url"},
            )
            response.raise_for_status()
            user = response.json().get("data", {}).get("user", {})
            self.logger.info(f"Authenticated as {user.get('display_name', 'Unknown')}")
            return True
        except Exception as e:
            self.logger.error(f"Credential verification failed: {e}")
            return False

    def post_text(self, text: str, **kwargs) -> PostResult:
        """
        TikTok doesn't support text-only posts.
        Use post_video instead.
        """
        return self._failed("TikTok requires video content for posts")

    def post_video(self, video_path: str, caption: str = "", **kwargs) -> PostResult:
        """
        Post a video to TikTok.

        Args:
            video_path: Path to video file
            caption: Video caption/title
            privacy: SELF_ONLY, MUTUAL_FOLLOW_FRIENDS, or PUBLIC_TO_EVERYONE
            disable_duet: Disable duet feature
            disable_comment: Disable comments
            disable_stitch: Disable stitch feature

        Returns:
            PostResult with publish ID
        """
        if not self._initialized:
            if not self.initialize():
                return self._failed("Failed to initialize TikTok API")

        if not os.path.exists(video_path):
            return self._failed(f"Video file not found: {video_path}")

        privacy = kwargs.get("privacy", "SELF_ONLY")
        video_size = os.path.getsize(video_path)

        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }

        try:
            # Step 1: Initialize upload
            init_data = {
                "post_info": {
                    "title": caption,
                    "privacy_level": privacy,
                    "disable_duet": kwargs.get("disable_duet", False),
                    "disable_comment": kwargs.get("disable_comment", False),
                    "disable_stitch": kwargs.get("disable_stitch", False),
                },
                "source_info": {
                    "source": "FILE_UPLOAD",
                    "video_size": video_size,
                },
            }

            init_response = requests.post(
                f"{self.BASE_URL}/post/publish/video/init/",
                headers=headers,
                json=init_data,
            )
            init_response.raise_for_status()
            init_result = init_response.json()

            if "error" in init_result:
                return self._failed(f"Init error: {init_result['error']}")

            upload_url = init_result["data"]["upload_url"]
            publish_id = init_result["data"]["publish_id"]

            # Step 2: Upload video
            with open(video_path, "rb") as video_file:
                upload_response = requests.put(
                    upload_url,
                    headers={"Content-Type": "video/mp4"},
                    data=video_file,
                )
                upload_response.raise_for_status()

            # Step 3: Check publish status
            time.sleep(2)
            status = self._check_publish_status(publish_id)

            if status.get("status") == "PUBLISH_COMPLETE":
                self.logger.info(f"Posted video to TikTok: {publish_id}")
                return self._success(
                    post_id=publish_id,
                    caption=caption,
                    privacy=privacy,
                )
            else:
                return self._success(
                    post_id=publish_id,
                    message=f"Upload submitted, status: {status.get('status')}",
                    caption=caption,
                )

        except Exception as e:
            self.logger.error(f"Failed to post video to TikTok: {e}")
            return self._failed(str(e))

    def _check_publish_status(self, publish_id: str) -> dict:
        """Check the status of a video publish operation."""
        try:
            response = requests.post(
                f"{self.BASE_URL}/post/publish/status/fetch/",
                headers={
                    "Authorization": f"Bearer {self.access_token}",
                    "Content-Type": "application/json",
                },
                json={"publish_id": publish_id},
            )
            response.raise_for_status()
            return response.json().get("data", {})
        except Exception as e:
            self.logger.error(f"Failed to check publish status: {e}")
            return {"status": "UNKNOWN", "error": str(e)}

    def post_photo(self, image_urls: list, caption: str = "", **kwargs) -> PostResult:
        """
        Post photos to TikTok (carousel style).

        Args:
            image_urls: List of public image URLs
            caption: Photo post caption
            privacy: Privacy level

        Returns:
            PostResult with publish ID
        """
        if not self._initialized:
            if not self.initialize():
                return self._failed("Failed to initialize TikTok API")

        privacy = kwargs.get("privacy", "SELF_ONLY")

        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }

        try:
            data = {
                "post_info": {
                    "title": caption,
                    "privacy_level": privacy,
                },
                "source_info": {
                    "source": "PULL_FROM_URL",
                    "photo_images": image_urls,
                },
                "post_mode": "DIRECT_POST",
                "media_type": "PHOTO",
            }

            response = requests.post(
                f"{self.BASE_URL}/post/publish/content/init/",
                headers=headers,
                json=data,
            )
            response.raise_for_status()
            result = response.json()

            if "data" in result:
                publish_id = result["data"].get("publish_id", "")
                self.logger.info(f"Posted photos to TikTok: {publish_id}")
                return self._success(
                    post_id=publish_id,
                    caption=caption,
                    image_count=len(image_urls),
                )
            else:
                return self._failed(f"API error: {result}")

        except Exception as e:
            self.logger.error(f"Failed to post photos to TikTok: {e}")
            return self._failed(str(e))

    def post_video_from_url(
        self, video_url: str, caption: str = "", **kwargs
    ) -> PostResult:
        """
        Post a video from URL (pull from URL method).

        Args:
            video_url: Public URL to video
            caption: Video caption
            privacy: Privacy level

        Returns:
            PostResult with publish ID
        """
        if not self._initialized:
            if not self.initialize():
                return self._failed("Failed to initialize TikTok API")

        privacy = kwargs.get("privacy", "SELF_ONLY")

        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }

        try:
            data = {
                "post_info": {
                    "title": caption,
                    "privacy_level": privacy,
                    "disable_duet": kwargs.get("disable_duet", False),
                    "disable_comment": kwargs.get("disable_comment", False),
                    "disable_stitch": kwargs.get("disable_stitch", False),
                },
                "source_info": {
                    "source": "PULL_FROM_URL",
                    "video_url": video_url,
                },
                "post_mode": "DIRECT_POST",
                "media_type": "VIDEO",
            }

            response = requests.post(
                f"{self.BASE_URL}/post/publish/content/init/",
                headers=headers,
                json=data,
            )
            response.raise_for_status()
            result = response.json()

            if "data" in result:
                publish_id = result["data"].get("publish_id", "")
                self.logger.info(f"Posted video from URL to TikTok: {publish_id}")
                return self._success(
                    post_id=publish_id,
                    caption=caption,
                    video_url=video_url,
                )
            else:
                return self._failed(f"API error: {result}")

        except Exception as e:
            self.logger.error(f"Failed to post video from URL: {e}")
            return self._failed(str(e))
