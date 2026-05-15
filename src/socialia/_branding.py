#!/usr/bin/env python3
"""Thin wrappers around ``scitex_dev._branding`` for socialia consumers.

The original module duplicated the registry's job locally (reading
``SOCIALIA_BRAND`` / ``SOCIALIA_ENV_PREFIX`` from the environment and
computing aliases). The single source of truth now lives in
``scitex_dev._branding`` (see ``BRANDING_TRANSLATION_REGISTRY_PLAN.md``);
this module exists only to preserve socialia's public import surface for
existing callers (twitter.py, linkedin.py, ...).

Public API (byte-identical to the previous module):

  - ``get_env(key, default=None)``
  - ``get_env_var_name(key)``
  - ``get_mcp_server_name()``
"""

from __future__ import annotations

from typing import Optional

from scitex_dev._branding import get as _brand_get
from scitex_dev._branding import get_env as _central_get_env

__all__ = ["get_env", "get_env_var_name", "get_mcp_server_name"]

# Kept (read-only) for back-compat with callers that imported the private
# attribute (e.g. tests/test_base.py). New code should use get_env() /
# get_env_var_name() instead — they read the registry directly.
ENV_PREFIX = _brand_get("socialia", "env_prefix")
BRAND_NAME = _brand_get("socialia", "display")


def get_env(key: str, default: Optional[str] = None) -> Optional[str]:
    """Get an environment variable using the socialia brand's env_prefix
    (and the counterpart scitex-social prefix as fallback), then the
    unprefixed name, then *default*.

    Lookup order is now controlled by the central registry rather than
    a local ``SOCIALIA_ENV_PREFIX`` env var, so white-label rebrands
    happen by editing ``scitex_dev/_branding/registry.yaml`` instead of
    munging ``os.environ`` before import.
    """
    return _central_get_env(key, brand_key="socialia", default=default)


def get_env_var_name(key: str) -> str:
    """Get the branded environment variable name for documentation.

    Returns ``<env_prefix>_<key>`` where ``env_prefix`` comes from the
    socialia entry in the registry (currently ``SOCIALIA``).
    """
    prefix = _brand_get("socialia", "env_prefix")
    return f"{prefix}_{key}"


def get_mcp_server_name() -> str:
    """Get the MCP server name for socialia (= registry display name with
    dots flattened to dashes, matching the legacy behaviour).
    """
    display = _brand_get("socialia", "display")
    return display.replace(".", "-")
