---
description: Supported platforms and capability matrix.
---

# Supported Platforms

| Platform | Class | Transport / API | Extra install |
|----------|-------|-----------------|---------------|
| Twitter/X | `Twitter` | v2 REST + OAuth 1.0a | (core) |
| LinkedIn | `LinkedIn` | v2 REST + OAuth 2.0 | (core) |
| Reddit | `Reddit` | PRAW | `socialia[reddit]` |
| Slack | `Slack` | Web API (bot token) | (core) |
| YouTube | `YouTube` | Data API v3 + OAuth | `socialia[youtube]` |
| Google Analytics | `GoogleAnalytics` | GA4 Measurement + Data API | `socialia[analytics]` |

## Feature matrix

| | post | delete | feed | me | thread | mentions | replies | update | media/video |
|--|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| Twitter | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |   | image |
| LinkedIn | ✓ | ✓ | ✓ | ✓ |   |   |   |   |   |
| Reddit | ✓ | ✓ | ✓ | ✓ |   | ✓ |   | ✓ |   |
| Slack | ✓ | ✓ | ✓ | ✓ | ✓ |   |   | ✓ |   |
| YouTube | ✓ | ✓ | ✓ | ✓ |   |   |   | ✓ | video |

## Twitter growth (extra)

```python
from socialia import Twitter
t = Twitter()
t.follow_by_username("someone")
t.get_followers(limit=100)
t.grow(keywords=["ml"], max_follows=10)   # discover + follow
```

## Org-file lifecycle helpers

```python
from socialia import move_to_scheduled, move_to_posted, ensure_project_dirs
ensure_project_dirs("/path/to/project")
move_to_scheduled("draft.org")   # → scheduled/
move_to_posted("draft.org")      # → posted/
```

## PLATFORM_STRATEGIES

`from socialia import PLATFORM_STRATEGIES` — dict used by the MCP server to pick a client per platform. Empty if `fastmcp` is not installed.
