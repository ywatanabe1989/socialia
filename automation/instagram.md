# Instagram API Automation (Meta Graph)

## Status: Available (Requires Business Account)

## Overview

Instagram posting is available through Meta's Graph API. Requires a Business or Creator account connected to a Facebook Page.

## Requirements

1. **Instagram Business/Creator Account** (not Personal)
2. **Facebook Page** connected to Instagram
3. **Meta Developer Account**
4. **App with Instagram permissions**

## Setup Steps

1. **Convert to Business Account**
   - Instagram Settings → Account → Switch to Professional
   - Choose Business or Creator

2. **Connect Facebook Page**
   - Instagram Settings → Account → Linked Accounts → Facebook
   - Connect or create a Facebook Page

3. **Create Meta App**
   - Go to [developers.facebook.com](https://developers.facebook.com)
   - Create new app → Business type
   - Add "Instagram Graph API" product

4. **Get Access Token**
   - Use Graph API Explorer or OAuth flow
   - Request permissions: `instagram_basic`, `instagram_content_publish`

## API Capabilities

| Feature | Supported |
|---------|-----------|
| Photo posts | Yes |
| Video posts | Yes |
| Reels | Yes (since 2022) |
| Stories | Yes (since 2023) |
| Carousels | Yes |
| Scheduling | Yes |

## Python Implementation

```python
import requests

ACCESS_TOKEN = "your_access_token"
INSTAGRAM_ACCOUNT_ID = "your_ig_account_id"

def get_instagram_account_id(page_id, access_token):
    """Get Instagram Business Account ID from Facebook Page."""
    url = f"https://graph.facebook.com/v18.0/{page_id}"
    params = {
        "fields": "instagram_business_account",
        "access_token": access_token
    }
    response = requests.get(url, params=params)
    return response.json()["instagram_business_account"]["id"]

def post_image(image_url, caption):
    """Post an image to Instagram (must be publicly accessible URL)."""

    # Step 1: Create media container
    container_url = f"https://graph.facebook.com/v18.0/{INSTAGRAM_ACCOUNT_ID}/media"
    container_params = {
        "image_url": image_url,  # Must be public URL
        "caption": caption,
        "access_token": ACCESS_TOKEN
    }
    container = requests.post(container_url, params=container_params).json()
    creation_id = container["id"]

    # Step 2: Publish the container
    publish_url = f"https://graph.facebook.com/v18.0/{INSTAGRAM_ACCOUNT_ID}/media_publish"
    publish_params = {
        "creation_id": creation_id,
        "access_token": ACCESS_TOKEN
    }
    result = requests.post(publish_url, params=publish_params).json()
    return result

def post_carousel(image_urls, caption):
    """Post multiple images as carousel."""
    children_ids = []

    # Create container for each image
    for url in image_urls:
        container = requests.post(
            f"https://graph.facebook.com/v18.0/{INSTAGRAM_ACCOUNT_ID}/media",
            params={
                "image_url": url,
                "is_carousel_item": True,
                "access_token": ACCESS_TOKEN
            }
        ).json()
        children_ids.append(container["id"])

    # Create carousel container
    carousel = requests.post(
        f"https://graph.facebook.com/v18.0/{INSTAGRAM_ACCOUNT_ID}/media",
        params={
            "media_type": "CAROUSEL",
            "children": ",".join(children_ids),
            "caption": caption,
            "access_token": ACCESS_TOKEN
        }
    ).json()

    # Publish
    result = requests.post(
        f"https://graph.facebook.com/v18.0/{INSTAGRAM_ACCOUNT_ID}/media_publish",
        params={
            "creation_id": carousel["id"],
            "access_token": ACCESS_TOKEN
        }
    ).json()
    return result
```

## Rate Limits

- API calls: 200/hour (reduced from 5,000)
- DMs: 200/hour
- Content: Follow Instagram's posting guidelines

## Token Management

- Short-lived tokens: ~1 hour
- Long-lived tokens: 60 days
- **Refresh every 50-55 days**

```python
def refresh_token(current_token):
    url = "https://graph.facebook.com/v18.0/oauth/access_token"
    params = {
        "grant_type": "fb_exchange_token",
        "client_id": APP_ID,
        "client_secret": APP_SECRET,
        "fb_exchange_token": current_token
    }
    return requests.get(url, params=params).json()
```

## Important Notes

1. **Image URL must be public** - Instagram fetches from URL
2. **No direct file upload** - Host image first
3. **Business account required** - Personal accounts unsupported
4. **Don't use password-based tools** - Risk of ban

## Environment Variables

```bash
META_APP_ID=
META_APP_SECRET=
INSTAGRAM_ACCESS_TOKEN=
INSTAGRAM_ACCOUNT_ID=
FACEBOOK_PAGE_ID=
```

## Sources

- [Instagram Graph API Guide](https://elfsight.com/blog/instagram-graph-api-complete-developer-guide-for-2025/)
- [Meta Graph API Docs](https://developers.facebook.com/docs/instagram-api)
- [Instagram API Use Cases](https://www.getphyllo.com/post/instagram-graph-api-use-cases-in-2025-iv)
