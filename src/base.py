#!/usr/bin/env python3
"""
Base class for social media posters.

All platform-specific posters inherit from BasePoster.
"""

import os
import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional, List, Dict, Any
from dataclasses import dataclass
from enum import Enum
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)


class PostStatus(Enum):
    """Status of a post operation."""

    SUCCESS = "success"
    FAILED = "failed"
    DRAFT = "draft"
    PENDING = "pending"


@dataclass
class PostResult:
    """Result of a posting operation."""

    status: PostStatus
    platform: str
    post_id: Optional[str] = None
    url: Optional[str] = None
    message: Optional[str] = None
    data: Optional[Dict[str, Any]] = None

    def __bool__(self):
        return self.status == PostStatus.SUCCESS


class BasePoster(ABC):
    """
    Abstract base class for social media posters.

    All platform-specific implementations should inherit from this class
    and implement the required abstract methods.
    """

    platform_name: str = "base"

    def __init__(self, env_path: Optional[str] = None):
        """
        Initialize the poster.

        Args:
            env_path: Path to .env file. Defaults to project root .env
        """
        self.logger = logging.getLogger(f"{self.__class__.__name__}")
        self._load_env(env_path)
        self._initialized = False

    def _load_env(self, env_path: Optional[str] = None):
        """Load environment variables from .env file."""
        if env_path:
            load_dotenv(env_path)
        else:
            # Try project root .env
            project_root = Path(__file__).parent.parent
            env_file = project_root / ".env"
            if env_file.exists():
                load_dotenv(env_file)

    def _get_env(self, key: str, required: bool = True) -> Optional[str]:
        """Get environment variable with optional requirement check."""
        value = os.getenv(key)
        if required and not value:
            raise ValueError(f"Missing required environment variable: {key}")
        return value

    @abstractmethod
    def initialize(self) -> bool:
        """
        Initialize the API client.

        Returns:
            True if initialization successful, False otherwise.
        """
        pass

    @abstractmethod
    def verify_credentials(self) -> bool:
        """
        Verify API credentials are valid.

        Returns:
            True if credentials are valid, False otherwise.
        """
        pass

    @abstractmethod
    def post_text(self, text: str, **kwargs) -> PostResult:
        """
        Post text content.

        Args:
            text: The text content to post.
            **kwargs: Platform-specific options.

        Returns:
            PostResult with status and details.
        """
        pass

    def post_with_image(self, text: str, image_path: str, **kwargs) -> PostResult:
        """
        Post text with a single image.

        Args:
            text: The text content.
            image_path: Path to the image file.
            **kwargs: Platform-specific options.

        Returns:
            PostResult with status and details.
        """
        return self.post_with_images(text, [image_path], **kwargs)

    def post_with_images(
        self, text: str, image_paths: List[str], **kwargs
    ) -> PostResult:
        """
        Post text with multiple images.

        Args:
            text: The text content.
            image_paths: List of image file paths.
            **kwargs: Platform-specific options.

        Returns:
            PostResult with status and details.
        """
        # Default implementation - override in subclasses that support images
        self.logger.warning(f"{self.platform_name} does not support image posts")
        return PostResult(
            status=PostStatus.FAILED,
            platform=self.platform_name,
            message="Image posts not supported",
        )

    def post_link(self, text: str, url: str, **kwargs) -> PostResult:
        """
        Post a link with text.

        Args:
            text: The text content.
            url: The URL to share.
            **kwargs: Platform-specific options.

        Returns:
            PostResult with status and details.
        """
        # Default: append URL to text
        return self.post_text(f"{text}\n{url}", **kwargs)

    def _validate_image_paths(self, image_paths: List[str]) -> List[Path]:
        """Validate image paths exist and return Path objects."""
        valid_paths = []
        for path_str in image_paths:
            path = Path(path_str)
            if path.exists():
                valid_paths.append(path)
            else:
                self.logger.warning(f"Image not found: {path_str}")
        return valid_paths

    def _success(
        self,
        post_id: Optional[str] = None,
        url: Optional[str] = None,
        message: str = "Posted successfully",
        **data,
    ) -> PostResult:
        """Create a success result."""
        return PostResult(
            status=PostStatus.SUCCESS,
            platform=self.platform_name,
            post_id=post_id,
            url=url,
            message=message,
            data=data if data else None,
        )

    def _failed(self, message: str, **data) -> PostResult:
        """Create a failed result."""
        return PostResult(
            status=PostStatus.FAILED,
            platform=self.platform_name,
            message=message,
            data=data if data else None,
        )

    def _draft(
        self, post_id: Optional[str] = None, message: str = "Saved as draft", **data
    ) -> PostResult:
        """Create a draft result."""
        return PostResult(
            status=PostStatus.DRAFT,
            platform=self.platform_name,
            post_id=post_id,
            message=message,
            data=data if data else None,
        )
