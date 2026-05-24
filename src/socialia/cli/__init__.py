#!/usr/bin/env python3
"""Socialia CLI package.

Click-based CLI (post-audit migration). The argparse implementation has been
replaced; deprecated subcommand names continue to work via the argv-rewrite
shim in `_click_cli._rewrite_argv`.
"""

from ._click_cli import main, main_group

__all__ = ["main", "main_group"]
