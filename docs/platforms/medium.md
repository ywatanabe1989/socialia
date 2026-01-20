# Medium API Automation

## Status: Deprecated but Functional

## Overview

Medium's official API is deprecated and unsupported, but still works for basic posting. The API allows creating posts but NOT updating or deleting them.

## Limitations

- **Create only** - Cannot update/delete posts via API
- **No list access** - Cannot retrieve user's posts
- **Unsupported** - May break without notice
- No official maintenance since ~2020

## Setup Steps

1. **Get Integration Token**
   - Log in to Medium
   - Go to Settings (click avatar → Settings)
   - Scroll to "Integration tokens"
   - Generate new token

2. **Get Your Author ID**
   ```bash
   curl -H "Authorization: Bearer YOUR_TOKEN" \
        https://api.medium.com/v1/me
   ```

## Python Implementation

```python
import requests

MEDIUM_TOKEN = "your_integration_token"
headers = {
    "Authorization": f"Bearer {MEDIUM_TOKEN}",
    "Content-Type": "application/json"
}

# Get user info and author ID
user = requests.get(
    "https://api.medium.com/v1/me",
    headers=headers
).json()

author_id = user["data"]["id"]
print(f"Author ID: {author_id}")

# Create a post
post_data = {
    "title": "My Article Title",
    "contentFormat": "markdown",  # or "html"
    "content": """
# Hello Medium!

This is my automated post.

- Bullet point 1
- Bullet point 2

**Bold text** and *italic text*.
    """,
    "publishStatus": "draft",  # "draft" or "public"
    "tags": ["python", "automation", "api"]
}

response = requests.post(
    f"https://api.medium.com/v1/users/{author_id}/posts",
    headers=headers,
    json=post_data
)

if response.status_code == 201:
    post = response.json()["data"]
    print(f"Created: {post['url']}")
else:
    print(f"Error: {response.text}")
```

## Content Formats

### Markdown
```python
post_data = {
    "contentFormat": "markdown",
    "content": "# Title\n\nParagraph with **bold**."
}
```

### HTML
```python
post_data = {
    "contentFormat": "html",
    "content": "<h1>Title</h1><p>Paragraph with <strong>bold</strong>.</p>"
}
```

## Publish Status

- `draft` - Save as draft (recommended for review)
- `public` - Publish immediately
- `unlisted` - Published but not in feeds

## Posting to Publications

```python
# Get user's publications
pubs = requests.get(
    f"https://api.medium.com/v1/users/{author_id}/publications",
    headers=headers
).json()

publication_id = pubs["data"][0]["id"]

# Post to publication (as draft for editor review)
response = requests.post(
    f"https://api.medium.com/v1/publications/{publication_id}/posts",
    headers=headers,
    json=post_data
)
```

## Environment Variables

```bash
MEDIUM_INTEGRATION_TOKEN=
MEDIUM_AUTHOR_ID=  # Optional, can be fetched
```

## Alternatives

1. **Unofficial Medium API** (mediumapi.com)
   - Paid service for reading Medium data
   - `pip install medium-api`

2. **Cross-posting tools**
   - Dev.to + Medium sync
   - Hashnode integration

## Sources

- [Medium API Docs (Archived)](https://github.com/Medium/medium-api-docs)
- [Medium API Guide](https://medium.com/codex/medium-has-an-api-605b51037b52)
- [Publishing with Python](https://hackernoon.com/automate-your-writing-publishing-to-medium-with-python-and-the-medium-api)
