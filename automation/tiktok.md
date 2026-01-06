# TikTok API Automation

## Status: Available (Requires Audit for Public Posts)

## Overview

TikTok provides official Content Posting API for developers. Unaudited apps post as private-only until approved.

## Key Limitation

> All content posted by unaudited clients will be restricted to private viewing mode.

Your app must pass TikTok's audit to post publicly visible content.

## Requirements

1. **TikTok Developer Account**
2. **TikTok Business Account** (for most features)
3. **App audit** (for public posting)

## Setup Steps

1. **Register as Developer**
   - Go to [developers.tiktok.com](https://developers.tiktok.com)
   - Create developer account

2. **Create App**
   - Create new app in dashboard
   - Add Content Posting API product
   - Configure OAuth redirect URI

3. **Submit for Audit**
   - Test integration thoroughly
   - Submit app for compliance review
   - Wait for approval

## Content Posting API

### Capabilities
- Direct video posting
- Photo posting (recently added)
- Draft uploads
- Caption, hashtags, privacy settings

### Supported Platforms
- Desktop apps
- Cloud/web applications

## Python Implementation

```python
import requests

CLIENT_KEY = "your_client_key"
CLIENT_SECRET = "your_client_secret"
ACCESS_TOKEN = "user_access_token"

def upload_video(video_path, caption):
    """Upload video to TikTok."""

    # Step 1: Initialize upload
    init_url = "https://open.tiktokapis.com/v2/post/publish/video/init/"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    init_data = {
        "post_info": {
            "title": caption,
            "privacy_level": "PUBLIC_TO_EVERYONE",  # or SELF_ONLY for testing
            "disable_duet": False,
            "disable_comment": False,
            "disable_stitch": False
        },
        "source_info": {
            "source": "FILE_UPLOAD",
            "video_size": os.path.getsize(video_path)
        }
    }

    init_response = requests.post(init_url, headers=headers, json=init_data).json()
    upload_url = init_response["data"]["upload_url"]
    publish_id = init_response["data"]["publish_id"]

    # Step 2: Upload video file
    with open(video_path, "rb") as video_file:
        upload_response = requests.put(
            upload_url,
            headers={"Content-Type": "video/mp4"},
            data=video_file
        )

    # Step 3: Check publish status
    status_url = "https://open.tiktokapis.com/v2/post/publish/status/fetch/"
    status_data = {"publish_id": publish_id}
    status = requests.post(status_url, headers=headers, json=status_data).json()

    return status

def upload_photo(image_paths, caption):
    """Upload photos to TikTok (carousel style)."""

    url = "https://open.tiktokapis.com/v2/post/publish/content/init/"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "post_info": {
            "title": caption,
            "privacy_level": "PUBLIC_TO_EVERYONE"
        },
        "source_info": {
            "source": "PULL_FROM_URL",
            "photo_images": image_paths  # Must be public URLs
        },
        "post_mode": "DIRECT_POST",
        "media_type": "PHOTO"
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()
```

## OAuth 2.0 Flow

```python
# Step 1: Redirect user to authorization
auth_url = (
    f"https://www.tiktok.com/v2/auth/authorize/"
    f"?client_key={CLIENT_KEY}"
    f"&scope=user.info.basic,video.publish"
    f"&response_type=code"
    f"&redirect_uri={REDIRECT_URI}"
)

# Step 2: Exchange code for token
def get_access_token(auth_code):
    url = "https://open.tiktokapis.com/v2/oauth/token/"
    data = {
        "client_key": CLIENT_KEY,
        "client_secret": CLIENT_SECRET,
        "code": auth_code,
        "grant_type": "authorization_code",
        "redirect_uri": REDIRECT_URI
    }
    response = requests.post(url, data=data)
    return response.json()
```

## Privacy Levels

- `PUBLIC_TO_EVERYONE` - Public (requires audit)
- `MUTUAL_FOLLOW_FRIENDS` - Friends only
- `SELF_ONLY` - Private (works without audit)

## Best Practices

1. **Test with SELF_ONLY** until audit approved
2. **Follow community guidelines** strictly
3. **Respect rate limits**
4. **Keep API usage compliant**

## Environment Variables

```bash
TIKTOK_CLIENT_KEY=
TIKTOK_CLIENT_SECRET=
TIKTOK_ACCESS_TOKEN=
TIKTOK_REDIRECT_URI=
```

## Sources

- [TikTok Developers](https://developers.tiktok.com/)
- [Content Posting API](https://developers.tiktok.com/products/content-posting-api/)
- [API Get Started Guide](https://developers.tiktok.com/doc/content-posting-api-get-started)
- [TikTok API Guide 2025](https://getlate.dev/blog/tiktok-api)
