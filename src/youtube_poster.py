#!/usr/bin/env python3
"""
YouTube Poster - Upload videos to YouTube using Data API v3.

Environment Variables:
    YOUTUBE_CLIENT_ID: OAuth client ID
    YOUTUBE_CLIENT_SECRET: OAuth client secret
    YOUTUBE_REFRESH_TOKEN: OAuth refresh token
"""

from typing import Optional, List
import os

from .base import BasePoster, PostResult

try:
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload

    GOOGLE_AVAILABLE = True
except ImportError:
    GOOGLE_AVAILABLE = False


class YouTubePoster(BasePoster):
    """Upload videos to YouTube using the Data API v3."""

    platform_name = "youtube"
    SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

    def __init__(self, env_path: Optional[str] = None):
        super().__init__(env_path)
        self.youtube = None
        self.credentials = None

    def initialize(self) -> bool:
        """Initialize YouTube API client."""
        if not GOOGLE_AVAILABLE:
            self.logger.error(
                "Google API libraries not installed. Run: "
                "pip install google-api-python-client google-auth-oauthlib"
            )
            return False

        try:
            client_id = self._get_env("YOUTUBE_CLIENT_ID")
            client_secret = self._get_env("YOUTUBE_CLIENT_SECRET")
            refresh_token = self._get_env("YOUTUBE_REFRESH_TOKEN")

            self.credentials = Credentials(
                token=None,
                refresh_token=refresh_token,
                token_uri="https://oauth2.googleapis.com/token",
                client_id=client_id,
                client_secret=client_secret,
            )

            # Refresh the token
            self.credentials.refresh(Request())

            self.youtube = build("youtube", "v3", credentials=self.credentials)

            self._initialized = True
            self.logger.info("YouTube API initialized")
            return True

        except Exception as e:
            self.logger.error(f"Failed to initialize YouTube API: {e}")
            return False

    def verify_credentials(self) -> bool:
        """Verify API credentials are valid."""
        if not self._initialized:
            if not self.initialize():
                return False

        try:
            response = self.youtube.channels().list(part="snippet", mine=True).execute()
            if response.get("items"):
                channel = response["items"][0]["snippet"]
                self.logger.info(f"Authenticated as {channel['title']}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Credential verification failed: {e}")
            return False

    def post_text(self, text: str, **kwargs) -> PostResult:
        """
        YouTube doesn't support text-only posts.
        Use upload_video instead.
        """
        return self._failed("YouTube requires video content. Use upload_video()")

    def upload_video(
        self, video_path: str, title: str, description: str = "", **kwargs
    ) -> PostResult:
        """
        Upload a video to YouTube.

        Args:
            video_path: Path to video file
            title: Video title
            description: Video description
            tags: List of tags
            category_id: YouTube category ID (default: 22 = People & Blogs)
            privacy: public, private, or unlisted (default: private)
            publish_at: ISO 8601 datetime for scheduled publish (requires private)

        Returns:
            PostResult with video ID and URL
        """
        if not self._initialized:
            if not self.initialize():
                return self._failed("Failed to initialize YouTube API")

        if not os.path.exists(video_path):
            return self._failed(f"Video file not found: {video_path}")

        privacy = kwargs.get("privacy", "private")
        tags = kwargs.get("tags", [])
        category_id = kwargs.get("category_id", "22")

        body = {
            "snippet": {
                "title": title,
                "description": description,
                "tags": tags,
                "categoryId": category_id,
            },
            "status": {
                "privacyStatus": privacy,
                "selfDeclaredMadeForKids": False,
            },
        }

        # Scheduled publishing
        if kwargs.get("publish_at"):
            body["status"]["privacyStatus"] = "private"
            body["status"]["publishAt"] = kwargs["publish_at"]

        try:
            media = MediaFileUpload(
                video_path,
                chunksize=1024 * 1024,  # 1MB chunks
                resumable=True,
            )

            request = self.youtube.videos().insert(
                part="snippet,status",
                body=body,
                media_body=media,
            )

            response = None
            while response is None:
                status, response = request.next_chunk()
                if status:
                    self.logger.info(
                        f"Upload progress: {int(status.progress() * 100)}%"
                    )

            video_id = response["id"]
            video_url = f"https://www.youtube.com/watch?v={video_id}"

            self.logger.info(f"Uploaded video to YouTube: {video_id}")
            return self._success(
                post_id=video_id,
                url=video_url,
                title=title,
                privacy=privacy,
            )

        except Exception as e:
            self.logger.error(f"Failed to upload video to YouTube: {e}")
            return self._failed(str(e))

    def set_thumbnail(self, video_id: str, thumbnail_path: str) -> PostResult:
        """
        Set custom thumbnail for a video.

        Args:
            video_id: YouTube video ID
            thumbnail_path: Path to thumbnail image

        Returns:
            PostResult indicating success/failure
        """
        if not self._initialized:
            if not self.initialize():
                return self._failed("Failed to initialize YouTube API")

        if not os.path.exists(thumbnail_path):
            return self._failed(f"Thumbnail not found: {thumbnail_path}")

        try:
            self.youtube.thumbnails().set(
                videoId=video_id,
                media_body=MediaFileUpload(thumbnail_path),
            ).execute()

            self.logger.info(f"Set thumbnail for video {video_id}")
            return self._success(
                post_id=video_id,
                message="Thumbnail set successfully",
            )

        except Exception as e:
            self.logger.error(f"Failed to set thumbnail: {e}")
            return self._failed(str(e))

    def update_video(
        self,
        video_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        tags: Optional[List[str]] = None,
        **kwargs,
    ) -> PostResult:
        """
        Update video metadata.

        Args:
            video_id: YouTube video ID
            title: New title (optional)
            description: New description (optional)
            tags: New tags (optional)

        Returns:
            PostResult indicating success/failure
        """
        if not self._initialized:
            if not self.initialize():
                return self._failed("Failed to initialize YouTube API")

        try:
            # Get current video data
            video = (
                self.youtube.videos()
                .list(
                    part="snippet",
                    id=video_id,
                )
                .execute()
            )

            if not video.get("items"):
                return self._failed(f"Video not found: {video_id}")

            snippet = video["items"][0]["snippet"]

            # Update fields
            if title:
                snippet["title"] = title
            if description:
                snippet["description"] = description
            if tags:
                snippet["tags"] = tags

            self.youtube.videos().update(
                part="snippet",
                body={
                    "id": video_id,
                    "snippet": snippet,
                },
            ).execute()

            self.logger.info(f"Updated video {video_id}")
            return self._success(
                post_id=video_id,
                message="Video updated successfully",
            )

        except Exception as e:
            self.logger.error(f"Failed to update video: {e}")
            return self._failed(str(e))

    def create_playlist(
        self, title: str, description: str = "", privacy: str = "private"
    ) -> PostResult:
        """
        Create a new playlist.

        Args:
            title: Playlist title
            description: Playlist description
            privacy: public, private, or unlisted

        Returns:
            PostResult with playlist ID
        """
        if not self._initialized:
            if not self.initialize():
                return self._failed("Failed to initialize YouTube API")

        try:
            response = (
                self.youtube.playlists()
                .insert(
                    part="snippet,status",
                    body={
                        "snippet": {
                            "title": title,
                            "description": description,
                        },
                        "status": {
                            "privacyStatus": privacy,
                        },
                    },
                )
                .execute()
            )

            playlist_id = response["id"]
            self.logger.info(f"Created playlist: {playlist_id}")
            return self._success(
                post_id=playlist_id,
                url=f"https://www.youtube.com/playlist?list={playlist_id}",
                title=title,
            )

        except Exception as e:
            self.logger.error(f"Failed to create playlist: {e}")
            return self._failed(str(e))

    def add_to_playlist(self, playlist_id: str, video_id: str) -> PostResult:
        """
        Add a video to a playlist.

        Args:
            playlist_id: YouTube playlist ID
            video_id: YouTube video ID

        Returns:
            PostResult indicating success/failure
        """
        if not self._initialized:
            if not self.initialize():
                return self._failed("Failed to initialize YouTube API")

        try:
            self.youtube.playlistItems().insert(
                part="snippet",
                body={
                    "snippet": {
                        "playlistId": playlist_id,
                        "resourceId": {
                            "kind": "youtube#video",
                            "videoId": video_id,
                        },
                    },
                },
            ).execute()

            self.logger.info(f"Added video {video_id} to playlist {playlist_id}")
            return self._success(
                message="Video added to playlist",
                playlist_id=playlist_id,
                video_id=video_id,
            )

        except Exception as e:
            self.logger.error(f"Failed to add to playlist: {e}")
            return self._failed(str(e))
