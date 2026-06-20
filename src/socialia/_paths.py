#!/usr/bin/env python3
"""Runtime path resolution for socialia.

Every socialia disk write goes under ``<scitex-dir>/socialia/runtime/``
(project or user scope — see ``06_local-state-directories.md``).

Public API
----------
- ``get_runtime_dir()``            — ``~/.scitex/socialia/runtime/``
- ``get_schedule_file()``          — ``runtime/scheduled.json``
- ``get_youtube_token_file()``     — ``runtime/youtube_token.json``
- ``get_completion_dir()``         — ``runtime/completion/``
"""

from __future__ import annotations

import os
import shutil
import sys
import warnings
from pathlib import Path

__all__ = [
    "get_runtime_dir",
    "get_schedule_file",
    "get_youtube_token_file",
    "get_completion_dir",
]


def _scitex_base() -> Path:
    """Return the scitex base directory (``$SCITEX_DIR`` or ``~/.scitex``)."""
    return Path(os.environ.get("SCITEX_DIR", Path.home() / ".scitex"))


def get_runtime_dir() -> Path:
    """Return the socialia runtime directory, creating it if needed.

    Resolves to ``$SCITEX_DIR/socialia/runtime/`` (or
    ``~/.scitex/socialia/runtime/`` by default).

    The directory is created lazily on first call (see §3.5 of the
    local-state-directories skill).
    """
    d = _scitex_base() / "socialia" / "runtime"
    d.mkdir(parents=True, exist_ok=True)
    return d


# ---------------------------------------------------------------------------
# Per-resource helpers with back-compat
# ---------------------------------------------------------------------------


def get_schedule_file() -> Path:
    """Return path to ``scheduled.json`` under the runtime directory.

    Back-compat (one minor version): if the legacy ``~/.socialia/scheduled.json``
    exists and the new path does not, it is migrated automatically. A
    deprecation warning is emitted on stderr.
    """
    new = get_runtime_dir() / "scheduled.json"
    _migrate_legacy(
        new,
        _legacy_candidates=[Path.home() / ".socialia" / "scheduled.json"],
        description="~/.socialia/scheduled.json",
    )
    return new


def get_youtube_token_file() -> Path:
    """Return path to the YouTube OAuth token under the runtime directory.

    Back-compat: migrates from ``~/.youtube_token.json`` on first access.
    """
    new = get_runtime_dir() / "youtube_token.json"
    _migrate_legacy(
        new,
        _legacy_candidates=[Path.home() / ".youtube_token.json"],
        description="~/.youtube_token.json",
    )
    return new


def get_completion_dir() -> Path:
    """Return the completion scripts directory under runtime.

    Back-compat (one minor version): if legacy completion files exist at
    ``~/.bash_completion.d/`` or ``~/.zsh/completions/`` they are copied
    to the new location on first access. A deprecation warning is emitted.
    """
    d = get_runtime_dir() / "completion"
    d.mkdir(parents=True, exist_ok=True)

    _migrate_legacy(
        d / "socialia.bash",
        _legacy_candidates=[Path.home() / ".bash_completion.d" / "socialia.bash"],
        description="~/.bash_completion.d/socialia.bash",
    )
    _migrate_legacy(
        d / "_socialia",
        _legacy_candidates=[Path.home() / ".zsh" / "completions" / "_socialia"],
        description="~/.zsh/completions/_socialia",
    )
    return d


# ---------------------------------------------------------------------------
# Legacy migration helpers
# ---------------------------------------------------------------------------


def _migrate_legacy(
    new_path: Path,
    _legacy_candidates: list[Path],
    description: str = "legacy path",
) -> None:
    """Migrate a single legacy file to *new_path* on first access.

    If *new_path* already exists it is used as-is (no migration).
    Otherwise the first legacy candidate that exists is moved to the new
    location and a one-time ``DeprecationWarning`` is emitted.

    This shim will be removed after one minor version — see §8 of the
    local-state-directories skill.
    """
    if new_path.exists():
        return

    for old in _legacy_candidates:
        if old.exists():
            new_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(old), str(new_path))
            warnings.warn(
                f"Migrated {description} to {new_path}. "
                f"See ~/.scitex/socialia/runtime/README.md for details.",
                DeprecationWarning,
                stacklevel=2,
            )
            return
