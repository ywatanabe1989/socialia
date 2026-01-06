#!/usr/bin/env python3
"""
Twitter/X Poster - Post to X (Twitter) using Tweepy.

Environment Variables:
    TWITTER_API_KEY: API Key (Consumer Key)
    TWITTER_API_SECRET: API Secret (Consumer Secret)
    TWITTER_ACCESS_TOKEN: Access Token
    TWITTER_ACCESS_SECRET: Access Token Secret
    TWITTER_BEARER_TOKEN: Bearer Token (optional, for v2 API)
"""

from typing import Optional, List
from pathlib import Path

from .base import BasePoster, PostResult, PostStatus

try:
    import tweepy
except ImportError:
    tweepy = None


class TwitterPoster(BasePoster):
    """Post to X (Twitter) using the official API via Tweepy."""

    platform_name = "twitter"

    def __init__(self, env_path: Optional[str] = None):
        super().__init__(env_path)
        self.api_v1 = None
        self.client = None

    def initialize(self) -> bool:
        """Initialize Twitter API clients."""
        if tweepy is None:
            self.logger.error("tweepy not installed. Run: pip install tweepy")
            return False

        try:
            api_key = self._get_env("TWITTER_API_KEY")
            api_secret = self._get_env("TWITTER_API_SECRET")
            access_token = self._get_env("TWITTER_ACCESS_TOKEN")
            access_secret = self._get_env("TWITTER_ACCESS_SECRET")
            bearer_token = self._get_env("TWITTER_BEARER_TOKEN", required=False)

            # OAuth1 handler for v1.1 API (media uploads)
            auth = tweepy.OAuth1UserHandler(
                api_key, api_secret, access_token, access_secret
            )
            self.api_v1 = tweepy.API(auth)

            # Client for v2 API (posting tweets)
            self.client = tweepy.Client(
                bearer_token=bearer_token,
                consumer_key=api_key,
                consumer_secret=api_secret,
                access_token=access_token,
                access_token_secret=access_secret,
            )

            self._initialized = True
            self.logger.info("Twitter API clients initialized")
            return True

        except Exception as e:
            self.logger.error(f"Failed to initialize Twitter API: {e}")
            return False

    def verify_credentials(self) -> bool:
        """Verify API credentials are valid."""
        if not self._initialized:
            if not self.initialize():
                return False

        try:
            user = self.api_v1.verify_credentials()
            self.logger.info(f"Authenticated as @{user.screen_name}")
            return True
        except Exception as e:
            self.logger.error(f"Credential verification failed: {e}")
            return False

    def post_text(self, text: str, **kwargs) -> PostResult:
        """
        Post a text tweet.

        Args:
            text: Tweet content (max 280 characters)
            reply_to: Optional tweet ID to reply to

        Returns:
            PostResult with tweet ID and URL
        """
        if not self._initialized:
            if not self.initialize():
                return self._failed("Failed to initialize Twitter API")

        if len(text) > 280:
            self.logger.warning(
                f"Tweet exceeds 280 chars ({len(text)}), will be truncated"
            )

        try:
            reply_to = kwargs.get("reply_to")
            response = self.client.create_tweet(
                text=text,
                in_reply_to_tweet_id=reply_to,
            )
            tweet_id = response.data["id"]
            url = f"https://x.com/i/status/{tweet_id}"

            self.logger.info(f"Posted tweet: {tweet_id}")
            return self._success(post_id=tweet_id, url=url, text=text)

        except Exception as e:
            self.logger.error(f"Failed to post tweet: {e}")
            return self._failed(str(e))

    def _upload_media(self, media_path: str) -> Optional[str]:
        """Upload media file to Twitter."""
        path = Path(media_path)
        if not path.exists():
            self.logger.error(f"Media file not found: {media_path}")
            return None

        try:
            media = self.api_v1.media_upload(filename=str(path))
            self.logger.info(f"Uploaded media: {media.media_id}")
            return str(media.media_id)
        except Exception as e:
            self.logger.error(f"Failed to upload media: {e}")
            return None

    def post_with_images(
        self, text: str, image_paths: List[str], **kwargs
    ) -> PostResult:
        """
        Post a tweet with images (up to 4).

        Args:
            text: Tweet content
            image_paths: List of image file paths (max 4)

        Returns:
            PostResult with tweet ID
        """
        if not self._initialized:
            if not self.initialize():
                return self._failed("Failed to initialize Twitter API")

        if len(image_paths) > 4:
            self.logger.warning("Twitter allows max 4 images, using first 4")
            image_paths = image_paths[:4]

        media_ids = []
        for path in image_paths:
            media_id = self._upload_media(path)
            if media_id:
                media_ids.append(media_id)

        if not media_ids:
            self.logger.error("No media uploaded successfully")
            return self._failed("Failed to upload any media")

        try:
            response = self.client.create_tweet(text=text, media_ids=media_ids)
            tweet_id = response.data["id"]
            url = f"https://x.com/i/status/{tweet_id}"

            self.logger.info(f"Posted tweet with {len(media_ids)} images: {tweet_id}")
            return self._success(
                post_id=tweet_id, url=url, text=text, media_ids=media_ids
            )

        except Exception as e:
            self.logger.error(f"Failed to post tweet with images: {e}")
            return self._failed(str(e))

    def post_thread(self, tweets: List[str]) -> List[PostResult]:
        """
        Post a thread (series of connected tweets).

        Args:
            tweets: List of tweet texts

        Returns:
            List of PostResult for each tweet
        """
        if not self._initialized:
            if not self.initialize():
                return [self._failed("Failed to initialize Twitter API")]

        results = []
        reply_to_id = None

        for i, text in enumerate(tweets):
            result = self.post_text(text, reply_to=reply_to_id)
            results.append(result)

            if result.status == PostStatus.SUCCESS:
                reply_to_id = result.post_id
                self.logger.info(f"Posted thread tweet {i + 1}/{len(tweets)}")
            else:
                self.logger.error(f"Failed to post thread tweet {i + 1}")
                break

        return results


def main():
    """CLI entry point for testing."""
    import argparse

    parser = argparse.ArgumentParser(description="Post to Twitter/X")
    parser.add_argument("--verify", action="store_true", help="Verify credentials")
    parser.add_argument("--text", type=str, help="Tweet text to post")
    parser.add_argument("--image", type=str, help="Image path to attach")
    args = parser.parse_args()

    poster = TwitterPoster()

    if args.verify:
        if poster.verify_credentials():
            print("Credentials verified successfully!")
        else:
            print("Credential verification failed!")
            return 1

    if args.text:
        if args.image:
            result = poster.post_with_image(args.text, args.image)
        else:
            result = poster.post_text(args.text)

        if result:
            print(f"Posted successfully! URL: {result.url}")
        else:
            print(f"Failed: {result.message}")
            return 1

    return 0


if __name__ == "__main__":
    exit(main())
