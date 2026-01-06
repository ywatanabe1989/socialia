# Social Media Automation Guide

## Overview

This directory contains documentation and resources for automating social media posting across all platforms used by SciTeX projects.

## Platform Status Summary

| Platform | API Available | Cost | Difficulty | Implementation |
|----------|--------------|------|------------|----------------|
| X/Twitter | Yes (Official) | Free tier: 500 posts/mo | Easy | `twitter.md` |
| LinkedIn | Yes (Official) | Free (w/ approval) | Medium | `linkedin.md` |
| Reddit | Yes (PRAW) | Free | Easy | `reddit.md` |
| Medium | Deprecated | Free | Medium | `medium.md` |
| Note.com | Unofficial only | Free | Hard | `note.md` |
| Instagram | Yes (Meta Graph) | Free | Medium | `instagram.md` |
| TikTok | Yes (Content API) | Free (w/ audit) | Medium | `tiktok.md` |
| YouTube | Yes (Data API v3) | Free | Medium | `youtube.md` |

## Quick Start Priority

### Tier 1 - Ready to Implement
1. **X/Twitter** - Tweepy + Free API tier (500 posts/mo)
2. **Reddit** - PRAW library (60 req/min)
3. **Medium** - Unofficial but working

### Tier 2 - Requires Setup
4. **LinkedIn** - Needs developer approval
5. **Instagram** - Requires Business account + Facebook Page
6. **YouTube** - OAuth setup required

### Tier 3 - Complex/Limited
7. **TikTok** - Requires audit for public posting
8. **Note.com** - Unofficial API only, Japanese docs

## Directory Structure

```
automation/
├── README.md              # This file
├── twitter.md             # X/Twitter API guide
├── linkedin.md            # LinkedIn API guide
├── reddit.md              # Reddit/PRAW guide
├── medium.md              # Medium API guide
├── note.md                # Note.com (Japan) guide
├── instagram.md           # Instagram/Meta Graph guide
├── tiktok.md              # TikTok Content API guide
├── youtube.md             # YouTube Data API guide
└── buffer.md              # Buffer (multi-platform tool)
```

## Environment Variables

All credentials should be stored in the root `.env` file:

```bash
# X/Twitter
TWITTER_API_KEY=
TWITTER_API_SECRET=
TWITTER_ACCESS_TOKEN=
TWITTER_ACCESS_SECRET=
TWITTER_BEARER_TOKEN=

# Reddit
REDDIT_CLIENT_ID=
REDDIT_CLIENT_SECRET=
REDDIT_USER_AGENT=
REDDIT_USERNAME=
REDDIT_PASSWORD=

# LinkedIn
LINKEDIN_CLIENT_ID=
LINKEDIN_CLIENT_SECRET=
LINKEDIN_ACCESS_TOKEN=

# Medium
MEDIUM_INTEGRATION_TOKEN=

# Instagram/Meta
META_APP_ID=
META_APP_SECRET=
INSTAGRAM_ACCESS_TOKEN=

# TikTok
TIKTOK_CLIENT_KEY=
TIKTOK_CLIENT_SECRET=

# YouTube
YOUTUBE_CLIENT_ID=
YOUTUBE_CLIENT_SECRET=
```

## Implementation Location

Python implementations are in `../src/`:
- `twitter_poster.py` - Twitter/X posting
- (More to be added)

## Recommended Approach

1. Start with **Twitter** (already implemented in `src/`)
2. Add **Reddit** next (PRAW is well-documented)
3. Set up **LinkedIn** for professional reach
4. Use **Buffer** as backup for cross-posting
