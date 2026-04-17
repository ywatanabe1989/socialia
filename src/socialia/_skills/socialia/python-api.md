---
description: Python API reference — class methods and utility functions exposed by socialia.
---

# Python API

Import surface (see `socialia/__init__.py`):

```python
from socialia import (
    Twitter, LinkedIn, Reddit, Slack, YouTube, GoogleAnalytics,
    move_to_scheduled, move_to_posted, ensure_project_dirs,
    PLATFORM_STRATEGIES, __version__,
)
```

## Twitter

```python
Twitter().post(text, reply_to=None, quote_tweet_id=None, media_ids=None)
Twitter().post_thread(tweets: list[str])
Twitter().delete(post_id)
Twitter().upload_media(file_path)
Twitter().me() / .feed(limit=10) / .mentions(limit=10) / .replies(limit=10)
Twitter().validate_credentials()
# Growth (TwitterGrowthMixin):
Twitter().follow(user_id) / .unfollow(user_id) / .follow_by_username(name)
Twitter().get_user(username) / .get_followers(limit=100) / .get_following(limit=100)
Twitter().search_tweets(...) / .discover_users(...) / .grow(...)
```

## LinkedIn

```python
LinkedIn().post(text, visibility="PUBLIC")
LinkedIn().delete(post_id)
LinkedIn().me() / .feed(limit=10) / .get_token_info() / .validate_credentials()
```

## Reddit (requires `socialia[reddit]`)

```python
Reddit().post(text, subreddit="test", title=None, url=None, flair_id=None)
Reddit().comment(...)
Reddit().delete(post_id) / .update(post_id, text)
Reddit().me() / .feed(limit=10) / .mentions(limit=10) / .validate_credentials()
```

## Slack

```python
Slack().post(text, channel=None, thread_ts=None, unfurl_links=True, unfurl_media=True)
Slack().post_thread(messages, channel=None)
Slack().update(..., channel=None) / .delete(post_id, channel=None)
Slack().me() / .feed(limit=10, channel=None) / .validate_credentials()
```

## YouTube (requires `socialia[youtube]`)

```python
YouTube().post(text, video_path=None, title=None, description=None,
               tags=None, privacy="public", thumbnail=None)
YouTube().update(video_id, ...) / .delete(video_id)
YouTube().me() / .feed(limit=10) / .get_channel_info() / .list_videos(max_results=10)
YouTube().validate_credentials()
```

## GoogleAnalytics (requires `socialia[analytics]`)

```python
GoogleAnalytics().track_event(event_name, params)
GoogleAnalytics().track_social_post(...)
GoogleAnalytics().track_social_delete(platform, post_id)
GoogleAnalytics().get_realtime_users()
GoogleAnalytics().get_page_views(start_date=..., end_date=..., path=None)
GoogleAnalytics().get_traffic_sources(start_date=..., end_date=...)
GoogleAnalytics().validate_credentials()
```

## Org-file helpers

```python
from socialia import move_to_scheduled, move_to_posted, ensure_project_dirs
ensure_project_dirs("/path/to/project")   # create drafts/scheduled/posted dirs
move_to_scheduled("draft.org")             # drafts/ → scheduled/
move_to_posted("draft.org")                # scheduled/ → posted/
```

## `socialia.org.OrgDraftManager`

```python
from socialia.org import OrgDraftManager
m = OrgDraftManager("drafts.org")
m.status_report() / m.get_pending() / m.get_due()
m.schedule_all()
m.post_draft(draft, dry_run=True)
```

## PLATFORM_STRATEGIES

Dict used by the MCP server to dispatch platform-specific posting. Empty `{}` if `fastmcp` is not installed.
