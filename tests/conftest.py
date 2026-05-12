"""Pytest fixtures for socialia tests.

Also wires module-import-time coverage configuration (parallel + subprocess
support). ``os.environ.setdefault`` would be a no-op here because pytest-cov
has already set ``COVERAGE_FILE`` to a tmp dir by the time conftest is loaded.
"""

from __future__ import annotations

import os
import sys
import sysconfig
from pathlib import Path

import pytest
from unittest.mock import MagicMock, patch

_PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Pin coverage's data file at the repo root and point process_startup
# at our pyproject so child interpreters configure themselves correctly.
os.environ["COVERAGE_PROCESS_START"] = str(_PROJECT_ROOT / "pyproject.toml")
os.environ["COVERAGE_FILE"] = str(_PROJECT_ROOT / ".coverage")


def _ensure_subprocess_coverage_shim() -> None:
    """Drop an idempotent ``.pth`` file in site-packages that auto-starts
    coverage in every child Python interpreter via
    ``coverage.process_startup()``.
    """
    purelib = Path(sysconfig.get_paths()["purelib"])
    pth = purelib / "_socialia_subprocess_coverage.pth"
    shim = (
        "import os, coverage\n"
        "if os.environ.get('COVERAGE_PROCESS_START'):\n"
        "    coverage.process_startup()\n"
    )
    try:
        if not pth.exists() or pth.read_text() != shim:
            pth.write_text(shim)
    except OSError:
        # site-packages may be read-only (e.g. system Python); silently
        # skip — local dev venvs are writable and that's where this matters.
        pass


_ensure_subprocess_coverage_shim()


@pytest.fixture
def mock_oauth_session():
    """Mock OAuth1Session for Twitter tests."""
    with patch("socialia.twitter.OAuth1Session") as mock:
        session = MagicMock()
        mock.return_value = session
        yield session


@pytest.fixture
def mock_requests():
    """Mock requests for LinkedIn tests."""
    with patch("socialia.linkedin.requests") as mock:
        yield mock


@pytest.fixture
def twitter_credentials():
    """Provide test Twitter credentials."""
    return {
        "consumer_key": "test_consumer_key",
        "consumer_secret": "test_consumer_secret",
        "access_token": "test_access_token",
        "access_token_secret": "test_access_token_secret",
    }


@pytest.fixture
def linkedin_credentials():
    """Provide test LinkedIn credentials."""
    return {
        "access_token": "test_linkedin_token",
    }
