# Buffer - Multi-Platform Automation

## Status: Ready (Third-Party Service)

## Overview

Buffer is a social media management tool that handles posting to multiple platforms through a single interface. Good fallback when direct API access is complex.

## Supported Platforms

- X/Twitter
- Facebook
- Instagram
- LinkedIn
- Pinterest
- TikTok
- Google Business
- Mastodon
- YouTube Shorts
- Threads
- Bluesky

## Pricing

| Plan | Cost | Channels | Features |
|------|------|----------|----------|
| Free | $0 | 3 | 10 posts queue, AI Assistant |
| Essentials | $6/mo/channel | Unlimited | Analytics, engagement tools |
| Team | $12/mo/channel | Unlimited | Collaboration, approval flows |

## Why Use Buffer

1. **Simpler setup** - No API credentials per platform
2. **Cross-posting** - One post to multiple platforms
3. **Scheduling** - Queue posts for optimal times
4. **Analytics** - Track engagement across platforms
5. **Team features** - Approval workflows

## Buffer API

Buffer provides an API for programmatic access.

### Authentication

```python
# Buffer uses OAuth 2.0
# Get access token from Buffer developer portal

ACCESS_TOKEN = "your_buffer_access_token"
```

### Python Implementation

```python
import requests

BASE_URL = "https://api.bufferapp.com/1"
ACCESS_TOKEN = "your_access_token"

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}"
}

def get_profiles():
    """Get connected social profiles."""
    response = requests.get(
        f"{BASE_URL}/profiles.json",
        headers=headers
    )
    return response.json()

def create_update(profile_ids, text, media=None, scheduled_at=None):
    """Create a post (update) in Buffer."""
    data = {
        "profile_ids[]": profile_ids,
        "text": text,
        "shorten": True
    }

    if media:
        data["media[link]"] = media.get("link")
        data["media[description]"] = media.get("description")
        data["media[picture]"] = media.get("picture")

    if scheduled_at:
        data["scheduled_at"] = scheduled_at  # Unix timestamp

    response = requests.post(
        f"{BASE_URL}/updates/create.json",
        headers=headers,
        data=data
    )
    return response.json()

def get_pending_updates(profile_id):
    """Get pending updates for a profile."""
    response = requests.get(
        f"{BASE_URL}/profiles/{profile_id}/updates/pending.json",
        headers=headers
    )
    return response.json()

# Usage
profiles = get_profiles()
twitter_profile = next(p for p in profiles if p["service"] == "twitter")

create_update(
    profile_ids=[twitter_profile["id"]],
    text="Hello from Buffer API!",
    media={
        "picture": "https://example.com/image.png",
        "description": "My image"
    }
)
```

## Zapier Integration

Buffer integrates with Zapier for automation:

```
Trigger: New row in Google Sheets
Action: Create Buffer post

Trigger: New RSS feed item
Action: Add to Buffer queue

Trigger: New file in Dropbox
Action: Create Buffer post with image
```

## n8n Integration

```javascript
// n8n workflow node for Buffer
{
  "nodes": [
    {
      "name": "Buffer",
      "type": "n8n-nodes-base.buffer",
      "parameters": {
        "operation": "create",
        "profileIds": ["profile_id"],
        "text": "Automated post via n8n"
      }
    }
  ]
}
```

## When to Use Buffer vs Direct API

| Scenario | Recommendation |
|----------|----------------|
| Quick multi-platform setup | Buffer |
| Full API control needed | Direct API |
| Team collaboration | Buffer |
| High volume posting | Direct API |
| Analytics dashboard | Buffer |
| Cost-sensitive | Direct API (free tiers) |
| Complex automation | Direct API |

## Setup Steps

1. **Create Buffer Account**
   - Go to [buffer.com](https://buffer.com)
   - Sign up (free tier available)

2. **Connect Social Accounts**
   - Dashboard → Channels
   - Add each platform
   - Authorize access

3. **Get API Access** (optional)
   - Go to [buffer.com/developers](https://buffer.com/developers)
   - Create app
   - Get access token

## Environment Variables

```bash
BUFFER_ACCESS_TOKEN=
BUFFER_CLIENT_ID=
BUFFER_CLIENT_SECRET=
```

## Sources

- [Buffer](https://buffer.com)
- [Buffer API Docs](https://buffer.com/developers/api)
- [Buffer vs Hootsuite](https://zapier.com/blog/hootsuite-vs-buffer/)
- [Social Media Automation Tools 2025](https://www.hostinger.com/tutorials/best-social-media-automation-tools)
