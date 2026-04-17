---
description: Unified social media management for Twitter/X, LinkedIn, Reddit, Slack, YouTube, and Google Analytics — Python API, CLI, and MCP tools.
allowed-tools: mcp__socialia__social_*
---

# socialia

Unified multi-platform social media posting, scheduling, analytics, and AI-agent integration. Part of the [SciTeX](https://scitex.ai) ecosystem.

## Installation

```bash
pip install socialia
# Optional extras: [reddit], [youtube], [analytics], [mcp], [all]
pip install -e /home/ywatanabe/proj/socialia     # local dev
```

## What it gives you

- **Platform clients** — `Twitter`, `LinkedIn`, `Reddit`, `Slack`, `YouTube`, `GoogleAnalytics`.
- **CLI** — `socialia post|feed|check|me|schedule|analytics|org|grow|mcp|completion|status`.
- **MCP server** (`socialia mcp start`) — 7 tools for AI agents (`social_post`, `social_delete`, `social_status`, `social_analytics_{track,pageviews,sources,realtime}`).
- **Scheduling daemon** — persistent job queue for deferred posts.
- **Org-mode draft workflow** — manage TODO/SCHEDULED drafts in Emacs org files.
- **Twitter growth** — `Twitter.grow()`, follow/unfollow, follower lookup.
- **Org-file lifecycle helpers** — `move_to_scheduled`, `move_to_posted`, `ensure_project_dirs`.

## Sub-skills

- [quick-start.md](quick-start.md) — Minimal working examples per platform.
- [platforms.md](platforms.md) — Supported platforms and capabilities.
- [environment.md](environment.md) — Credentials / env vars per platform.
- [python-api.md](python-api.md) — Class-by-class method reference.
- [cli-reference.md](cli-reference.md) — Full CLI surface.
- [mcp-tools.md](mcp-tools.md) — MCP tools exposed to AI agents.

## Quick example

```python
from socialia import Twitter, LinkedIn, Slack

Twitter().post("Hello world!")
LinkedIn().post("Professional update")
Slack().post("Ping from CI", channel="#alerts")
```

```bash
socialia check                               # verify all platform credentials
socialia post twitter "Hello!" --image a.png
socialia mcp start                           # run MCP server for AI agents
```
