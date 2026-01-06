#!/usr/bin/env python3
"""
Reddit Poster - Post to Reddit using PRAW.

Environment Variables:
    REDDIT_CLIENT_ID: App client ID
    REDDIT_CLIENT_SECRET: App client secret
    REDDIT_USER_AGENT: User agent string
    REDDIT_USERNAME: Reddit username
    REDDIT_PASSWORD: Reddit password
"""

from typing import Optional, List

from .base import BasePoster, PostResult

try:
    import praw
except ImportError:
    praw = None


class RedditPoster(BasePoster):
    """Post to Reddit using PRAW (Python Reddit API Wrapper)."""

    platform_name = "reddit"

    def __init__(self, env_path: Optional[str] = None):
        super().__init__(env_path)
        self.reddit = None

    def initialize(self) -> bool:
        """Initialize Reddit API client."""
        if praw is None:
            self.logger.error("praw not installed. Run: pip install praw")
            return False

        try:
            self.reddit = praw.Reddit(
                client_id=self._get_env("REDDIT_CLIENT_ID"),
                client_secret=self._get_env("REDDIT_CLIENT_SECRET"),
                user_agent=self._get_env("REDDIT_USER_AGENT", required=False)
                or "SciTeX:v1.0",
                username=self._get_env("REDDIT_USERNAME"),
                password=self._get_env("REDDIT_PASSWORD"),
            )

            self._initialized = True
            self.logger.info("Reddit API client initialized")
            return True

        except Exception as e:
            self.logger.error(f"Failed to initialize Reddit API: {e}")
            return False

    def verify_credentials(self) -> bool:
        """Verify API credentials are valid."""
        if not self._initialized:
            if not self.initialize():
                return False

        try:
            user = self.reddit.user.me()
            self.logger.info(f"Authenticated as u/{user.name}")
            return True
        except Exception as e:
            self.logger.error(f"Credential verification failed: {e}")
            return False

    def post_text(self, text: str, **kwargs) -> PostResult:
        """
        Post a text submission to a subreddit.

        Args:
            text: Post body content
            subreddit: Subreddit name (without r/)
            title: Post title (required)
            flair_id: Optional flair ID
            flair_text: Optional flair text

        Returns:
            PostResult with submission ID and URL
        """
        if not self._initialized:
            if not self.initialize():
                return self._failed("Failed to initialize Reddit API")

        subreddit_name = kwargs.get("subreddit")
        title = kwargs.get("title")

        if not subreddit_name:
            return self._failed("subreddit parameter is required")
        if not title:
            return self._failed("title parameter is required")

        try:
            subreddit = self.reddit.subreddit(subreddit_name)

            submission = subreddit.submit(
                title=title,
                selftext=text,
                flair_id=kwargs.get("flair_id"),
                flair_text=kwargs.get("flair_text"),
            )

            self.logger.info(f"Posted to r/{subreddit_name}: {submission.id}")
            return self._success(
                post_id=submission.id,
                url=submission.url,
                title=title,
                subreddit=subreddit_name,
            )

        except Exception as e:
            self.logger.error(f"Failed to post to Reddit: {e}")
            return self._failed(str(e))

    def post_link(self, text: str, url: str, **kwargs) -> PostResult:
        """
        Post a link submission to a subreddit.

        Args:
            text: Not used (Reddit link posts don't have body text)
            url: URL to share
            subreddit: Subreddit name
            title: Post title (required)

        Returns:
            PostResult with submission ID
        """
        if not self._initialized:
            if not self.initialize():
                return self._failed("Failed to initialize Reddit API")

        subreddit_name = kwargs.get("subreddit")
        title = kwargs.get("title")

        if not subreddit_name:
            return self._failed("subreddit parameter is required")
        if not title:
            return self._failed("title parameter is required")

        try:
            subreddit = self.reddit.subreddit(subreddit_name)

            submission = subreddit.submit(
                title=title,
                url=url,
                flair_id=kwargs.get("flair_id"),
                flair_text=kwargs.get("flair_text"),
            )

            self.logger.info(f"Posted link to r/{subreddit_name}: {submission.id}")
            return self._success(
                post_id=submission.id,
                url=submission.url,
                title=title,
                subreddit=subreddit_name,
                link_url=url,
            )

        except Exception as e:
            self.logger.error(f"Failed to post link to Reddit: {e}")
            return self._failed(str(e))

    def post_with_image(self, text: str, image_path: str, **kwargs) -> PostResult:
        """
        Post an image submission to a subreddit.

        Args:
            text: Not used for image posts
            image_path: Path to image file
            subreddit: Subreddit name
            title: Post title (required)

        Returns:
            PostResult with submission ID
        """
        if not self._initialized:
            if not self.initialize():
                return self._failed("Failed to initialize Reddit API")

        subreddit_name = kwargs.get("subreddit")
        title = kwargs.get("title")

        if not subreddit_name:
            return self._failed("subreddit parameter is required")
        if not title:
            return self._failed("title parameter is required")

        valid_paths = self._validate_image_paths([image_path])
        if not valid_paths:
            return self._failed(f"Image not found: {image_path}")

        try:
            subreddit = self.reddit.subreddit(subreddit_name)

            submission = subreddit.submit_image(
                title=title,
                image_path=str(valid_paths[0]),
                flair_id=kwargs.get("flair_id"),
                flair_text=kwargs.get("flair_text"),
            )

            self.logger.info(f"Posted image to r/{subreddit_name}: {submission.id}")
            return self._success(
                post_id=submission.id,
                url=submission.url,
                title=title,
                subreddit=subreddit_name,
            )

        except Exception as e:
            self.logger.error(f"Failed to post image to Reddit: {e}")
            return self._failed(str(e))

    def post_gallery(self, title: str, image_paths: List[str], **kwargs) -> PostResult:
        """
        Post a gallery (multiple images) to a subreddit.

        Args:
            title: Post title
            image_paths: List of image paths
            subreddit: Subreddit name

        Returns:
            PostResult with submission ID
        """
        if not self._initialized:
            if not self.initialize():
                return self._failed("Failed to initialize Reddit API")

        subreddit_name = kwargs.get("subreddit")

        if not subreddit_name:
            return self._failed("subreddit parameter is required")

        valid_paths = self._validate_image_paths(image_paths)
        if not valid_paths:
            return self._failed("No valid images found")

        try:
            subreddit = self.reddit.subreddit(subreddit_name)

            images = [{"image_path": str(p)} for p in valid_paths]
            submission = subreddit.submit_gallery(title=title, images=images)

            self.logger.info(
                f"Posted gallery ({len(valid_paths)} images) to r/{subreddit_name}"
            )
            return self._success(
                post_id=submission.id,
                url=submission.url,
                title=title,
                subreddit=subreddit_name,
                image_count=len(valid_paths),
            )

        except Exception as e:
            self.logger.error(f"Failed to post gallery to Reddit: {e}")
            return self._failed(str(e))

    def reply_to_post(self, post_id: str, text: str) -> PostResult:
        """
        Reply to an existing post.

        Args:
            post_id: Submission ID to reply to
            text: Comment text

        Returns:
            PostResult with comment ID
        """
        if not self._initialized:
            if not self.initialize():
                return self._failed("Failed to initialize Reddit API")

        try:
            submission = self.reddit.submission(id=post_id)
            comment = submission.reply(text)

            self.logger.info(f"Replied to post {post_id}: {comment.id}")
            return self._success(
                post_id=comment.id,
                url=f"https://reddit.com{comment.permalink}",
                parent_id=post_id,
            )

        except Exception as e:
            self.logger.error(f"Failed to reply to post: {e}")
            return self._failed(str(e))
