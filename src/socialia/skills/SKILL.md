---
name: socialia
description: Unified social media management - posting, analytics, and insights across platforms (Twitter/X, Bluesky, etc.). Use when posting updates, sharing research findings, or managing social media presence.
allowed-tools: mcp__scitex__social_*
---

# Social Media with socialia

## Quick Start

```python
from socialia import post, status

# Post to all configured platforms
post("New paper published! Check out our findings on neural oscillations.")

# Check connection status
status()
```

## CLI Commands

```bash
socialia post "Hello world!"
socialia status
socialia delete <post-id>

# Skills
socialia skills list
```

## MCP Tools

| Tool | Purpose |
|------|---------|
| `social_post` | Post to social media platforms |
| `social_status` | Check platform connection status |
| `social_delete` | Delete a post |
