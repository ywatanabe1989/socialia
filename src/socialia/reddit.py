"""Reddit API client using PRAW."""

from typing import Optional

from ._branding import get_env
from .base import BasePoster

try:
    import praw

    HAS_PRAW = True
except ImportError:
    HAS_PRAW = False


class Reddit(BasePoster):
    """Reddit API client using PRAW (Python Reddit API Wrapper)."""

    def __init__(
        self,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        user_agent: Optional[str] = None,
    ):
        self.client_id = client_id or get_env("REDDIT_CLIENT_ID")
        self.client_secret = client_secret or get_env("REDDIT_CLIENT_SECRET")
        self.username = username or get_env("REDDIT_USERNAME")
        self.password = password or get_env("REDDIT_PASSWORD")
        self.user_agent = user_agent or (
            get_env("REDDIT_USER_AGENT") or "Socialia v0.1"
        )
        self._reddit: Optional["praw.Reddit"] = None

    def _get_client(self) -> Optional["praw.Reddit"]:
        """Get authenticated Reddit client."""
        if not HAS_PRAW:
            return None

        if self._reddit:
            return self._reddit

        if not self.validate_credentials():
            return None

        self._reddit = praw.Reddit(
            client_id=self.client_id,
            client_secret=self.client_secret,
            username=self.username,
            password=self.password,
            user_agent=self.user_agent,
        )
        return self._reddit

    def validate_credentials(self) -> bool:
        """Check if all credentials are set."""
        if not HAS_PRAW:
            return False
        return all(
            [
                self.client_id,
                self.client_secret,
                self.username,
                self.password,
            ]
        )

    def post(
        self,
        text: str,
        subreddit: str = "test",
        title: Optional[str] = None,
        url: Optional[str] = None,
        flair_id: Optional[str] = None,
    ) -> dict:
        """
        Post to a subreddit.

        Args:
            text: Post body (for self posts) or ignored for link posts
            subreddit: Target subreddit name (without r/)
            title: Post title (required for Reddit)
            url: URL for link posts (makes it a link post instead of self post)
            flair_id: Optional flair ID

        Returns:
            dict with 'success', 'id', 'url' or 'error'
        """
        if not HAS_PRAW:
            return {
                "success": False,
                "error": "PRAW not installed. Run: pip install praw",
            }

        if not self.validate_credentials():
            return {"success": False, "error": "Missing credentials"}

        if not title:
            # Use first line or truncated text as title
            title = text.split("\n")[0][:300]

        reddit = self._get_client()
        if not reddit:
            return {"success": False, "error": "Could not create Reddit client"}

        try:
            sub = reddit.subreddit(subreddit)

            if url:
                # Link post
                submission = sub.submit(
                    title=title,
                    url=url,
                    flair_id=flair_id,
                )
            else:
                # Self/text post
                submission = sub.submit(
                    title=title,
                    selftext=text,
                    flair_id=flair_id,
                )

            return {
                "success": True,
                "id": submission.id,
                "url": f"https://reddit.com{submission.permalink}",
            }

        except praw.exceptions.APIException as e:
            return {"success": False, "error": f"Reddit API error: {e}"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def delete(self, post_id: str) -> dict:
        """
        Delete a Reddit post.

        Args:
            post_id: Reddit submission ID

        Returns:
            dict with 'success' or 'error'
        """
        if not HAS_PRAW:
            return {"success": False, "error": "PRAW not installed"}

        if not self.validate_credentials():
            return {"success": False, "error": "Missing credentials"}

        reddit = self._get_client()
        if not reddit:
            return {"success": False, "error": "Could not create Reddit client"}

        try:
            submission = reddit.submission(id=post_id)
            submission.delete()
            return {"success": True, "deleted": True}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def comment(
        self,
        post_id: str,
        text: str,
    ) -> dict:
        """
        Add a comment to a post.

        Args:
            post_id: Reddit submission ID
            text: Comment text

        Returns:
            dict with 'success', 'id' or 'error'
        """
        if not HAS_PRAW:
            return {"success": False, "error": "PRAW not installed"}

        if not self.validate_credentials():
            return {"success": False, "error": "Missing credentials"}

        reddit = self._get_client()
        if not reddit:
            return {"success": False, "error": "Could not create Reddit client"}

        try:
            submission = reddit.submission(id=post_id)
            comment = submission.reply(text)
            return {
                "success": True,
                "id": comment.id,
                "url": f"https://reddit.com{comment.permalink}",
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
