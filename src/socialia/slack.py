"""Slack API client for channel messaging."""

from typing import Optional

import requests

from ._branding import get_env
from .base import BasePoster


class Slack(BasePoster):
    """Slack Web API client for posting to channels."""

    platform_name = "slack"

    API_BASE = "https://slack.com/api"
    POST_MESSAGE_ENDPOINT = f"{API_BASE}/chat.postMessage"
    DELETE_MESSAGE_ENDPOINT = f"{API_BASE}/chat.delete"
    UPDATE_MESSAGE_ENDPOINT = f"{API_BASE}/chat.update"
    CONVERSATIONS_HISTORY_ENDPOINT = f"{API_BASE}/conversations.history"
    AUTH_TEST_ENDPOINT = f"{API_BASE}/auth.test"
    USERS_INFO_ENDPOINT = f"{API_BASE}/users.info"

    def __init__(
        self,
        bot_token: Optional[str] = None,
        default_channel: Optional[str] = None,
    ):
        """
        Initialize Slack client.

        Args:
            bot_token: Slack Bot Token (xoxb-...)
            default_channel: Default channel ID to post to
        """
        self.bot_token = bot_token or get_env("SLACK_BOT_TOKEN")
        self.default_channel = default_channel or get_env("SLACK_DEFAULT_CHANNEL")

    def _headers(self) -> dict:
        """Get authorization headers."""
        return {
            "Authorization": f"Bearer {self.bot_token}",
            "Content-Type": "application/json",
        }

    def validate_credentials(self) -> bool:
        """Check if bot token is set."""
        return bool(self.bot_token)

    def post(
        self,
        text: str,
        channel: Optional[str] = None,
        thread_ts: Optional[str] = None,
        unfurl_links: bool = True,
        unfurl_media: bool = True,
    ) -> dict:
        """
        Post a message to a Slack channel.

        Args:
            text: Message content (supports Slack markdown)
            channel: Channel ID (uses default if not specified)
            thread_ts: Thread timestamp to reply to
            unfurl_links: Enable link previews
            unfurl_media: Enable media previews

        Returns:
            dict with 'success', 'id', 'ts', 'channel' or 'error'
        """
        if not self.validate_credentials():
            return {"success": False, "error": "Missing bot token"}

        target_channel = channel or self.default_channel
        if not target_channel:
            return {"success": False, "error": "No channel specified"}

        payload = {
            "channel": target_channel,
            "text": text,
            "unfurl_links": unfurl_links,
            "unfurl_media": unfurl_media,
        }

        if thread_ts:
            payload["thread_ts"] = thread_ts

        response = requests.post(
            self.POST_MESSAGE_ENDPOINT,
            headers=self._headers(),
            json=payload,
        )

        data = response.json()
        if data.get("ok"):
            return {
                "success": True,
                "id": data["ts"],
                "ts": data["ts"],
                "channel": data["channel"],
                "url": self._build_message_url(data["channel"], data["ts"]),
            }
        return {
            "success": False,
            "error": data.get("error", "Unknown error"),
        }

    def delete(self, post_id: str, channel: Optional[str] = None) -> dict:
        """
        Delete a message from a Slack channel.

        Args:
            post_id: Message timestamp (ts)
            channel: Channel ID (uses default if not specified)

        Returns:
            dict with 'success', 'deleted' or 'error'
        """
        if not self.validate_credentials():
            return {"success": False, "error": "Missing bot token"}

        target_channel = channel or self.default_channel
        if not target_channel:
            return {"success": False, "error": "No channel specified"}

        payload = {
            "channel": target_channel,
            "ts": post_id,
        }

        response = requests.post(
            self.DELETE_MESSAGE_ENDPOINT,
            headers=self._headers(),
            json=payload,
        )

        data = response.json()
        if data.get("ok"):
            return {"success": True, "deleted": True}
        return {
            "success": False,
            "error": data.get("error", "Unknown error"),
        }

    def update(
        self,
        post_id: str,
        text: str,
        channel: Optional[str] = None,
    ) -> dict:
        """
        Update an existing message.

        Args:
            post_id: Message timestamp (ts)
            text: New message content
            channel: Channel ID (uses default if not specified)

        Returns:
            dict with 'success', 'ts' or 'error'
        """
        if not self.validate_credentials():
            return {"success": False, "error": "Missing bot token"}

        target_channel = channel or self.default_channel
        if not target_channel:
            return {"success": False, "error": "No channel specified"}

        payload = {
            "channel": target_channel,
            "ts": post_id,
            "text": text,
        }

        response = requests.post(
            self.UPDATE_MESSAGE_ENDPOINT,
            headers=self._headers(),
            json=payload,
        )

        data = response.json()
        if data.get("ok"):
            return {
                "success": True,
                "ts": data["ts"],
                "channel": data["channel"],
            }
        return {
            "success": False,
            "error": data.get("error", "Unknown error"),
        }

    def feed(self, limit: int = 10, channel: Optional[str] = None) -> dict:
        """
        Get recent messages from a channel.

        Args:
            limit: Maximum number of messages to return
            channel: Channel ID (uses default if not specified)

        Returns:
            dict with 'success', 'messages' list or 'error'
        """
        if not self.validate_credentials():
            return {"success": False, "error": "Missing bot token"}

        target_channel = channel or self.default_channel
        if not target_channel:
            return {"success": False, "error": "No channel specified"}

        response = requests.get(
            self.CONVERSATIONS_HISTORY_ENDPOINT,
            headers=self._headers(),
            params={
                "channel": target_channel,
                "limit": limit,
            },
        )

        data = response.json()
        if data.get("ok"):
            messages = []
            for msg in data.get("messages", []):
                messages.append(
                    {
                        "ts": msg["ts"],
                        "text": msg.get("text", ""),
                        "user": msg.get("user"),
                        "type": msg.get("type"),
                        "url": self._build_message_url(target_channel, msg["ts"]),
                    }
                )
            return {"success": True, "messages": messages, "count": len(messages)}
        return {
            "success": False,
            "error": data.get("error", "Unknown error"),
        }

    def me(self) -> dict:
        """
        Get authenticated bot info.

        Returns:
            dict with 'success', 'id', 'name', 'team' or 'error'
        """
        if not self.validate_credentials():
            return {"success": False, "error": "Missing bot token"}

        response = requests.get(
            self.AUTH_TEST_ENDPOINT,
            headers=self._headers(),
        )

        data = response.json()
        if data.get("ok"):
            return {
                "success": True,
                "id": data["user_id"],
                "name": data["user"],
                "team": data["team"],
                "team_id": data["team_id"],
                "url": data.get("url"),
            }
        return {
            "success": False,
            "error": data.get("error", "Unknown error"),
        }

    def post_thread(self, messages: list, channel: Optional[str] = None) -> dict:
        """
        Post a thread of messages.

        Args:
            messages: List of message texts
            channel: Channel ID (uses default if not specified)

        Returns:
            dict with 'success', 'ts_list', 'thread_ts' or 'error'
        """
        ts_list = []
        thread_ts = None

        for i, text in enumerate(messages):
            result = self.post(text, channel=channel, thread_ts=thread_ts)
            if result["success"]:
                ts_list.append(result["ts"])
                if i == 0:
                    thread_ts = result["ts"]
            else:
                return {
                    "success": False,
                    "error": f"Failed at message {i + 1}: {result['error']}",
                    "partial_ts_list": ts_list,
                }

        return {
            "success": True,
            "ts_list": ts_list,
            "thread_ts": thread_ts,
            "channel": channel or self.default_channel,
        }

    def _build_message_url(self, channel: str, ts: str) -> str:
        """Build a URL to a specific message."""
        # Slack message URLs use ts without the dot
        ts_no_dot = ts.replace(".", "")
        return f"https://slack.com/archives/{channel}/p{ts_no_dot}"
