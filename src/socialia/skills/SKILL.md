---
name: socialia
description: Unified social media management - posting, threads, analytics, scheduling across platforms (Twitter/X, LinkedIn, Reddit, Slack, YouTube). Use when posting updates, sharing research findings, or managing social media presence.
allowed-tools: mcp__scitex__social_*
---

# Social Media with socialia

## Quick Start

```python
from socialia import Twitter, LinkedIn, Reddit, Slack, YouTube

# Post to Twitter/X
client = Twitter()
client.post("New paper published! Check out our findings.")

# Post a thread
client.post_thread([
    "Thread: Key findings from our study...",
    "1. First finding...",
    "2. Second finding...",
])

# Delete a post
client.delete(post_id="1234567890")

# LinkedIn
linkedin = LinkedIn()
linkedin.post("Excited to share our latest research!")
```

## Python API

### Platform Clients

| Class | Methods | Notes |
|-------|---------|-------|
| `Twitter()` | `post()`, `delete()`, `post_thread()` | Twitter/X API v2 |
| `LinkedIn()` | `post()`, `delete()` | LinkedIn API |
| `Reddit()` | `post()`, `delete()` | Reddit API |
| `Slack()` | `post()`, `delete()` | Slack webhooks |
| `YouTube()` | `post()`, `delete()` | YouTube Data API |
| `GoogleAnalytics()` | `track()`, `pageviews()`, `sources()`, `realtime()` | GA4 |

### Utility Functions

| Function | Purpose |
|----------|---------|
| `move_to_scheduled(path)` | Move draft to scheduled directory |
| `move_to_posted(path)` | Move to posted directory after publishing |
| `ensure_project_dirs()` | Create project directory structure |
| `PLATFORM_STRATEGIES` | Dict mapping platform names to client classes |

## CLI Commands

```bash
# Posting
socialia post "Hello world!" --platform twitter
socialia thread <file> --platform twitter
socialia delete <post-id> --platform twitter

# Status & Discovery
socialia status                  # Show all platform connection status
socialia check                   # Verify connections to all platforms
socialia me                      # Get authenticated user info
socialia feed                    # Get recent posts from platforms
socialia setup                   # Show platform setup instructions

# Scheduling
socialia schedule list
socialia schedule cancel <id>
socialia schedule run
socialia schedule daemon
socialia schedule update-source

# Analytics (Google Analytics)
socialia analytics track <event_name>
socialia analytics realtime
socialia analytics pageviews [--start <date>] [--end <date>]
socialia analytics sources [--start <date>] [--end <date>]

# Growth
socialia grow                    # Discover and follow users

# Org mode
socialia org                     # Org mode draft management

# YouTube
socialia youtube                 # YouTube batch operations

# MCP server
socialia mcp start
socialia mcp list-tools
socialia mcp doctor

# Introspection
socialia list-python-apis [-v]
```

## Environment Variables

### Twitter/X
| Variable | Purpose |
|----------|---------|
| `SOCIALIA_X_CONSUMER_KEY` | Twitter API consumer key |
| `SOCIALIA_X_CONSUMER_KEY_SECRET` | Twitter API consumer secret |
| `SOCIALIA_X_ACCESSTOKEN` | Twitter access token |
| `SOCIALIA_X_ACCESSTOKEN_SECRET` | Twitter access token secret |

### LinkedIn
| Variable | Purpose |
|----------|---------|
| `SOCIALIA_LINKEDIN_ACCESS_TOKEN` | LinkedIn API access token |

### Reddit
| Variable | Purpose |
|----------|---------|
| `SOCIALIA_REDDIT_CLIENT_ID` | Reddit app client ID |
| `SOCIALIA_REDDIT_CLIENT_SECRET` | Reddit app client secret |
| `SOCIALIA_REDDIT_USERNAME` | Reddit username |
| `SOCIALIA_REDDIT_PASSWORD` | Reddit password |

### YouTube
| Variable | Purpose |
|----------|---------|
| `SOCIALIA_YOUTUBE_CLIENT_SECRETS_FILE` | Path to YouTube OAuth client secrets |

### Google Analytics
| Variable | Purpose |
|----------|---------|
| `SOCIALIA_GOOGLE_ANALYTICS_MEASUREMENT_ID` | GA4 measurement ID |
| `SOCIALIA_GOOGLE_ANALYTICS_API_SECRET` | GA4 API secret |
| `SOCIALIA_GOOGLE_ANALYTICS_PROPERTY_ID` | GA4 property ID |

## MCP Tools (for AI agents)

| Tool | Parameters | Purpose |
|------|-----------|---------|
| `social_post` | `platform`, `text`, `reply_to`, `image`, `dry_run` | Post to platform |
| `social_delete` | `platform`, `post_id` | Delete a post |
| `social_status` | `platform` | Check platform connection |
| `social_analytics_track` | `event_name`, `params` | Track custom GA4 event |
| `social_analytics_pageviews` | `start_date`, `end_date`, `path` | Get page view metrics |
| `social_analytics_sources` | `start_date`, `end_date` | Get traffic sources |
| `social_analytics_realtime` | — | Get realtime active users |
