---
description: MCP tools exposed by `socialia mcp start` for AI agents.
---

# MCP Tools

Requires `pip install socialia[mcp]` (pulls in `fastmcp`). Start with `socialia mcp start`.

| Tool | Parameters | Purpose |
|------|------------|---------|
| `social_post` | `platform`, `text`, `reply_to?`, `image?`, `dry_run?` | Post to twitter/linkedin/reddit/slack/youtube. Twitter accepts `image` path. |
| `social_delete` | `platform`, `post_id` | Delete a post by ID. |
| `social_status` | `platform` | Check credentials / connection for one platform. |
| `social_analytics_track` | `event_name`, `params?` | Send a custom GA4 event. |
| `social_analytics_pageviews` | `start_date?`, `end_date?`, `path?` | Query pageview metrics via GA4 Data API. |
| `social_analytics_sources` | `start_date?`, `end_date?` | Query traffic source breakdown. |
| `social_analytics_realtime` | — | Current active users. |

`platform` ∈ `{"twitter", "linkedin", "reddit", "slack", "youtube"}`.

The server name registered with MCP is `socialia`, so Claude Code tool names appear as `mcp__socialia__social_post`, etc.

## Claude Desktop / Code config

```json
{
  "mcpServers": {
    "socialia": {
      "command": "socialia",
      "args": ["mcp", "start"],
      "env": {
        "SOCIALIA_X_CONSUMER_KEY": "…",
        "SOCIALIA_X_CONSUMER_KEY_SECRET": "…",
        "SOCIALIA_X_ACCESSTOKEN": "…",
        "SOCIALIA_X_ACCESSTOKEN_SECRET": "…"
      }
    }
  }
}
```

`socialia mcp installation` prints this snippet with your branding substituted in.
