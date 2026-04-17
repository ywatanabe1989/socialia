---
description: Minimal working examples per platform (Twitter, LinkedIn, Reddit, Slack, YouTube).
---

# Quick Start

```python
from socialia import Twitter, LinkedIn, Reddit, Slack, YouTube, GoogleAnalytics

# Twitter/X
twitter = Twitter()
twitter.post("Hello world!")
twitter.post_thread(["First", "Second", "Third"])

# LinkedIn
linkedin = LinkedIn()
linkedin.post("Professional update")

# Reddit  (requires: pip install socialia[reddit])
reddit = Reddit()
reddit.post("Body text", subreddit="test", title="Post title")

# Slack
slack = Slack()
slack.post("Deploy finished", channel="#alerts")

# YouTube  (requires: pip install socialia[youtube])
youtube = YouTube()
youtube.post("Description", video_path="clip.mp4", title="My video")

# Google Analytics  (requires: pip install socialia[analytics])
ga = GoogleAnalytics()
ga.track_event("page_view", {"page": "/docs"})
```

CLI equivalent:

```bash
socialia post twitter "Hello world!"
socialia post linkedin "Professional update"
socialia post reddit "Body text" --subreddit test --title "Post title"
socialia post slack "Deploy finished" --channel "#alerts"
socialia post youtube "Description" --video clip.mp4 --title "My video"
```
