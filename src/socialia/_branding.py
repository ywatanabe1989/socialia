#!/usr/bin/env python3
"""Thin wrappers around ``scitex_dev._branding`` for socialia consumers.

Primary path: delegate to ``scitex_dev._branding`` (the ecosystem
branding-translation registry — see ``BRANDING_TRANSLATION_REGISTRY_PLAN.md``).

Fallback path: when the installed scitex-dev predates the registry
(``ModuleNotFoundError`` on import), fall back to the original local
``SOCIALIA_BRAND`` / ``SOCIALIA_ENV_PREFIX`` environment-variable lookup.
This keeps socialia installable against any scitex-dev>=0.11.7 while the
registry rolls out across the ecosystem; the wrappers below are byte-
identical in behaviour either way for the default (unbranded) case.

Public API:

  - ``get_env(key, default=None)``
  - ``get_env_var_name(key)``
  - ``get_mcp_server_name()``
"""

from __future__ import annotations

import os
from typing import Optional

__all__ = ["get_env", "get_env_var_name", "get_mcp_server_name"]

try:
    from scitex_dev._branding import get as _brand_get
    from scitex_dev._branding import get_env as _central_get_env

    _HAS_REGISTRY = True
    ENV_PREFIX = _brand_get("socialia", "env_prefix")
    BRAND_NAME = _brand_get("socialia", "display")
except ModuleNotFoundError:
    _HAS_REGISTRY = False
    _brand_get = None  # type: ignore[assignment]
    _central_get_env = None  # type: ignore[assignment]
    # Local fallback mirrors the pre-registry behaviour.
    BRAND_NAME = os.environ.get("SOCIALIA_BRAND", "socialia")
    ENV_PREFIX = os.environ.get("SOCIALIA_ENV_PREFIX", "SOCIALIA")

_ORIGINAL_PREFIX = "SOCIALIA"


def get_env(key: str, default: Optional[str] = None) -> Optional[str]:
    """Get an environment variable using the socialia brand's env_prefix
    (and the counterpart scitex-social prefix as fallback), then the
    unprefixed name, then *default*.
    """
    if _HAS_REGISTRY:
        return _central_get_env(key, brand_key="socialia", default=default)

    # Local fallback: branded prefix, then SOCIALIA_, then unprefixed.
    if ENV_PREFIX != _ORIGINAL_PREFIX:
        value = os.environ.get(f"{ENV_PREFIX}_{key}")
        if value:
            return value
    value = os.environ.get(f"{_ORIGINAL_PREFIX}_{key}")
    if value:
        return value
    value = os.environ.get(key)
    if value:
        return value
    return default


def get_env_var_name(key: str) -> str:
    """Get the branded environment variable name for documentation.

    Returns ``<env_prefix>_<key>`` where ``env_prefix`` comes from the
    socialia entry in the registry (currently ``SOCIALIA``), or from
    ``$SOCIALIA_ENV_PREFIX`` when the registry isn't available.
    """
    if _HAS_REGISTRY:
        prefix = _brand_get("socialia", "env_prefix")
    else:
        prefix = ENV_PREFIX
    return f"{prefix}_{key}"


def get_mcp_server_name() -> str:
    """Get the MCP server name for socialia (= registry display name with
    dots flattened to dashes, matching the legacy behaviour).
    """
    if _HAS_REGISTRY:
        display = _brand_get("socialia", "display")
    else:
        display = BRAND_NAME
    return display.replace(".", "-")
