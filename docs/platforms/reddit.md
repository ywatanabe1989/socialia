# Reddit API Automation (PRAW)

## Status: Ready to Use

## Overview

Reddit provides excellent API access through PRAW (Python Reddit API Wrapper). Free and well-documented.

## Setup Steps

1. **Create Reddit App**
   - Go to [reddit.com/prefs/apps](https://reddit.com/prefs/apps)
   - Click "Create App" at bottom
   - Select "script" type
   - Set redirect URI to `http://localhost:8080`

2. **Get Credentials**
   - Client ID (under app name)
   - Client Secret
   - Your Reddit username/password

## Installation

```bash
pip install praw
```

## Python Implementation

```python
import praw

reddit = praw.Reddit(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
    user_agent="SciTeX:v1.0 (by /u/your_username)",
    username="your_reddit_username",
    password="your_reddit_password"
)

# Verify authentication
print(f"Logged in as: {reddit.user.me()}")

# Post to subreddit
subreddit = reddit.subreddit("test")  # Use "test" for testing

# Text post
submission = subreddit.submit(
    title="My Post Title",
    selftext="Post content here"
)
print(f"Posted: {submission.url}")

# Link post
submission = subreddit.submit(
    title="Check out this link",
    url="https://scitex.ai"
)

# Image post
submission = subreddit.submit_image(
    title="Server Status",
    image_path="path/to/image.png"
)
```

## Rate Limits

- 60 requests per minute
- 100 items per request
- PRAW handles rate limiting automatically

## Best Practices

1. **Use descriptive user_agent**
   ```python
   user_agent = "platform:appname:version (by /u/username)"
   ```

2. **Test in r/test first**
   ```python
   subreddit = reddit.subreddit("test")
   ```

3. **Don't spam** - Reddit communities dislike self-promotion
   - Follow subreddit rules
   - Engage authentically
   - 10:1 ratio (10 comments per 1 self-post)

4. **Handle exceptions**
   ```python
   from prawcore.exceptions import ResponseException

   try:
       submission = subreddit.submit(title="Test", selftext="Content")
   except ResponseException as e:
       print(f"Error: {e}")
   ```

## Useful Features

```python
# Get subreddit info
sub = reddit.subreddit("datascience")
print(sub.subscribers, sub.description)

# Reply to comments
for comment in submission.comments:
    comment.reply("Thanks for the feedback!")

# Check if post succeeded
if submission.id:
    print(f"Success! ID: {submission.id}")
```

## Environment Variables

```bash
REDDIT_CLIENT_ID=
REDDIT_CLIENT_SECRET=
REDDIT_USER_AGENT=SciTeX:v1.0 (by /u/username)
REDDIT_USERNAME=
REDDIT_PASSWORD=
```

## Sources

- [PRAW Documentation](https://praw.readthedocs.io/)
- [PRAW GitHub](https://github.com/praw-dev/praw)
- [Reddit API Guide](https://www.jcchouinard.com/reddit-api/)
- [Posting with PRAW](https://www.jcchouinard.com/post-on-reddit-api-with-python-praw/)
