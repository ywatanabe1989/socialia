---
description: Unified posting + analytics client for 6 platforms — `Twitter` (X), `LinkedIn`, `Reddit`, `Slack`, `YouTube`, `GoogleAnalytics`. Python API — per-platform classes (each with post / delete / check / feed methods where applicable), scheduled-post file helpers (`move_to_scheduled`, `move_to_posted`, `ensure_project_dirs`), and `PLATFORM_STRATEGIES` for per-platform content rules (length limits, hashtag style, thread handling). 9 MCP tools — `social_post`, `social_delete`, `social_status`, `social_check`, `social_feed`, plus GA4 analytics `social_analytics_track` / `_pageviews` / `_sources` / `_realtime`. Drop-in replacement for `tweepy`, `linkedin-api`, `praw` (Reddit), `slack_sdk`, `google-api-python-client` for YouTube / GA4 — unified under one interface so you write one post and fan out. Use whenever the user asks to "post to Twitter / X / LinkedIn / Reddit / Slack / YouTube", "schedule a post", "check post status", "delete a tweet / LinkedIn post", "get GA4 realtime users", "pull GA4 pageviews or traffic sources", "track a GA4 event", "move scheduled posts to posted", "announce my paper on social", or mentions Twitter API, LinkedIn API, Reddit praw, Slack webhook, YouTube Data API, Google Analytics 4.
allowed-tools: mcp__scitex__social_*
primary_interface: mcp
interfaces:
  python: 1
  cli: 1
  mcp: 3
  skills: 2
  hook: 0
  http: 0
name: socialia
tags: [socialia, scitex-package]
---

# socialia

> **Interfaces:** Python ⭐ · CLI ⭐ · MCP ⭐⭐⭐ (primary) · Skills ⭐⭐ · Hook — · HTTP —

## Installation & import (two equivalent paths)

The same module is reachable via two install paths. Both forms work at
runtime; which one a user has depends on their install choice.

```python
# Standalone — pip install socialia
import socialia as soc
soc.LinkedIn(...)

# Umbrella — pip install scitex
import scitex.social as soc
soc.LinkedIn(...)
```

`pip install socialia` alone does NOT expose the `scitex` namespace;
`import scitex.social` raises `ModuleNotFoundError`. To use the
`scitex.social` form, also `pip install scitex`.

See [../../general/02_interface-python-api.md] for the ecosystem-wide
rule and empirical verification table.

## Sub-skills

### Core
- [01_quick-start.md](01_quick-start.md) — Basic usage
- [02_platforms.md](02_platforms.md) — Supported platforms
- [03_python-api.md](03_python-api.md) — Python API reference (classes, methods, utilities)

### Workflows
- [10_cli-reference.md](10_cli-reference.md) — CLI commands
- [11_mcp-tools.md](11_mcp-tools.md) — MCP tools for AI agents

### Standards
- [20_environment.md](20_environment.md) — Environment variables for all platforms

## CLI

```bash
socialia post "New paper published!" --platform twitter
socialia status
```

## MCP Tools

| Tool | Description |
|------|-------------|
| `social_post` | Post content to a chosen platform |
| `social_delete` | Delete a previously submitted post |
| `social_status` | Check per-platform auth & reachability |
| `social_check` | Validate credentials for a platform |
| `social_feed` | Fetch recent posts / timeline |
| `social_analytics_track` | Track a custom GA4 event |
| `social_analytics_pageviews` | Query GA4 pageview metrics |
| `social_analytics_sources` | Query GA4 traffic sources |
| `social_analytics_realtime` | Query GA4 realtime active users |


## Environment

- [21_env-vars.md](21_env-vars.md) — SCITEX_* env vars read by socialia at runtime
