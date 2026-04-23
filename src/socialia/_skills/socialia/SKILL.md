---
description: Unified social media management — posting across Twitter/X, LinkedIn, and other platforms.
allowed-tools: mcp__scitex__social_*
---

# socialia

## Installation & import (two equivalent paths)

The same module is reachable via two install paths. Both forms work at
runtime; which one a user has depends on their install choice.

```python
# Standalone — pip install socialia
import socialia as soc
soc.post(...)

# Umbrella — pip install scitex
import scitex.social as soc
soc.post(...)
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
| `social_post` | Post to social media |
| `social_status` | Check platform status |
| `social_delete` | Delete a post |
| `social_analytics_track` | Track custom GA4 event |
| `social_analytics_pageviews` | Get page view metrics |
| `social_analytics_sources` | Get traffic sources |
| `social_analytics_realtime` | Get realtime active users |
