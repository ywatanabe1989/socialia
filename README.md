# Socialia

Unified social media management - posting, analytics, and insights.

Part of the [SciTeX](https://scitex.ai) ecosystem for scientific research automation.

## Installation

```bash
pip install socialia

# Or with optional dependencies
pip install socialia[reddit]      # Reddit support
pip install socialia[youtube]     # YouTube support
pip install socialia[analytics]   # Google Analytics Data API
pip install socialia[all]         # Everything
```

## CLI Usage

```bash
# Post to Twitter
socialia post twitter "Hello World!"

# Post to LinkedIn
socialia post linkedin "Professional update!"

# Post to Reddit
socialia post reddit "Post body" --subreddit python --title "Post Title"

# Post to YouTube (video upload)
socialia post youtube "Description" --video video.mp4 --title "My Video"

# Analytics tracking
socialia analytics track page_view --param page /docs

# Get realtime users
socialia analytics realtime

# Post from file
socialia post twitter --file tweet.txt

# Delete a post
socialia delete twitter 1234567890

# Post a thread (separate posts with ---)
socialia thread twitter --file thread.txt

# Dry run (preview without posting)
socialia post twitter "Test" --dry-run

# Show all commands
socialia help-recursive

# JSON output
socialia --json post twitter "Hello"
```

## Quick Start with Make

```bash
make install                    # Install package
make check                      # Verify credentials
make twitter MSG='Hello!'       # Post to Twitter
make linkedin MSG='Update'      # Post to LinkedIn
make dry-run P=twitter MSG='Test'  # Preview
make setup                      # View setup guide
```

## Python API

```python
from socialia import TwitterPoster, LinkedInPoster, RedditPoster, GoogleAnalytics, YouTubePoster

# Twitter
twitter = TwitterPoster()
result = twitter.post("Hello World!")
twitter.post_thread(["First", "Second", "Third"])

# LinkedIn
linkedin = LinkedInPoster()
linkedin.post("Professional update!")

# Reddit (requires: pip install socialia[reddit])
reddit = RedditPoster()
reddit.post("Post body", subreddit="test", title="Title")

# YouTube (requires: pip install socialia[youtube])
youtube = YouTubePoster()
youtube.post("Description", video_path="video.mp4", title="My Video")

# Google Analytics (requires: pip install socialia[analytics])
ga = GoogleAnalytics()
ga.track_event("social_post", {"platform": "twitter", "post_id": "123"})
ga.get_page_views(start_date="7daysAgo", end_date="today")
```

## MCP Server

Add to Claude Code settings:

```json
{
  "mcpServers": {
    "socialia": {
      "command": "python",
      "args": ["-m", "socialia.mcp_server"],
      "env": {
        "SCITEX_X_CONSUMER_KEY": "...",
        "SCITEX_X_CONSUMER_KEY_SECRET": "...",
        "SCITEX_X_ACCESSTOKEN": "...",
        "SCITEX_X_ACCESSTOKEN_SECRET": "..."
      }
    }
  }
}
```

## Environment Variables

```bash
# Twitter/X
export SCITEX_X_CONSUMER_KEY="your_consumer_key"
export SCITEX_X_CONSUMER_KEY_SECRET="your_consumer_secret"
export SCITEX_X_ACCESSTOKEN="your_access_token"
export SCITEX_X_ACCESSTOKEN_SECRET="your_access_token_secret"

# LinkedIn
export LINKEDIN_ACCESS_TOKEN="your_access_token"

# Reddit
export REDDIT_CLIENT_ID="your_client_id"
export REDDIT_CLIENT_SECRET="your_client_secret"
export REDDIT_USERNAME="your_username"
export REDDIT_PASSWORD="your_password"

# YouTube
export YOUTUBE_CLIENT_SECRETS_FILE="path/to/client_secrets.json"

# Google Analytics
export GA_MEASUREMENT_ID="G-XXXXXXXXXX"
export GA_API_SECRET="your_api_secret"
export GA_PROPERTY_ID="123456789"  # Optional, for Data API
```

**Detailed setup guide:** `make setup` or see [docs/SETUP.md](docs/SETUP.md)

## Project Structure

```
socialia/
├── src/socialia/         # Python package
│   ├── cli.py            # CLI with argparse
│   ├── twitter.py        # Twitter/X API
│   ├── linkedin.py       # LinkedIn API
│   ├── reddit.py         # Reddit API (PRAW)
│   ├── youtube.py        # YouTube API
│   ├── analytics.py      # Google Analytics
│   ├── mcp_server.py     # MCP server (delegates to CLI)
│   └── base.py           # Base class
├── docs/
│   ├── platforms/        # Platform API documentation
│   └── SETUP.md          # Step-by-step setup guide
├── Makefile              # Command dispatcher
├── pyproject.toml
└── .env                  # Credentials (gitignored)
```

## Supported Platforms

| Platform | Status | API | Install |
|----------|--------|-----|---------|
| Twitter/X | Ready | v2 OAuth 1.0a | `pip install socialia` |
| LinkedIn | Ready | v2 OAuth 2.0 | `pip install socialia` |
| Reddit | Ready | PRAW | `pip install socialia[reddit]` |
| YouTube | Ready | Data API v3 | `pip install socialia[youtube]` |
| Google Analytics | Ready | GA4 + Data API | `pip install socialia[analytics]` |

## SciTeX Integration

Socialia is part of the SciTeX ecosystem:

```bash
# Install via scitex
pip install scitex[social]

# Use in research workflows
import scitex as stx
from socialia import TwitterPoster

@stx.session
def share_results(twitter=stx.INJECTED):
    # Auto-configured from scitex settings
    twitter.post("New research results!")
```

## License

MIT
