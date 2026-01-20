"""Base class for social media posters."""

from abc import ABC, abstractmethod


class BasePoster(ABC):
    """Abstract base class for social media posters."""

    @abstractmethod
    def post(self, text: str, **kwargs) -> dict:
        """Post content to the platform."""
        pass

    @abstractmethod
    def delete(self, post_id: str) -> dict:
        """Delete a post by ID."""
        pass

    def validate_credentials(self) -> bool:
        """Check if credentials are configured."""
        return True
