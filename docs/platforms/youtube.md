# YouTube API Automation

## Status: Available (OAuth Required)

## Overview

YouTube Data API v3 provides comprehensive access for video uploads, playlist management, and channel operations.

## Capabilities

- Video upload
- Metadata management (title, description, tags)
- Thumbnail upload
- Privacy settings
- Scheduled publishing
- Playlist management

## Setup Steps

1. **Create Google Cloud Project**
   - Go to [Google Cloud Console](https://console.cloud.google.com)
   - Create new project

2. **Enable YouTube Data API v3**
   - Go to Library
   - Search "YouTube Data API v3"
   - Enable it

3. **Create OAuth Credentials**
   - Go to Credentials
   - Create Credentials → OAuth client ID
   - Application type: Desktop app
   - Download `client_secrets.json`

4. **Configure Consent Screen**
   - Set up OAuth consent screen
   - Add YouTube scopes

## Python Implementation

### Installation

```bash
pip install google-api-python-client google-auth-oauthlib
```

### Upload Video

```python
import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def get_authenticated_service():
    """Authenticate and return YouTube service."""
    flow = InstalledAppFlow.from_client_secrets_file(
        "client_secrets.json", SCOPES
    )
    credentials = flow.run_local_server(port=8080)

    return build("youtube", "v3", credentials=credentials)

def upload_video(youtube, video_path, title, description, tags, privacy="private"):
    """Upload video to YouTube."""

    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags,
            "categoryId": "22"  # People & Blogs
        },
        "status": {
            "privacyStatus": privacy,  # public, private, unlisted
            "selfDeclaredMadeForKids": False
        }
    }

    media = MediaFileUpload(
        video_path,
        chunksize=1024*1024,  # 1MB chunks
        resumable=True
    )

    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media
    )

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"Uploaded {int(status.progress() * 100)}%")

    print(f"Upload complete! Video ID: {response['id']}")
    return response

# Usage
youtube = get_authenticated_service()
upload_video(
    youtube,
    video_path="my_video.mp4",
    title="SciTeX Demo Video",
    description="Demonstrating SciTeX features",
    tags=["scitex", "research", "automation"],
    privacy="unlisted"
)
```

### Upload Thumbnail

```python
def set_thumbnail(youtube, video_id, thumbnail_path):
    """Set custom thumbnail for video."""
    youtube.thumbnails().set(
        videoId=video_id,
        media_body=MediaFileUpload(thumbnail_path)
    ).execute()
```

### Scheduled Publishing

```python
from datetime import datetime, timedelta

def upload_scheduled(youtube, video_path, title, description, publish_at):
    """Upload video with scheduled publish time."""

    body = {
        "snippet": {
            "title": title,
            "description": description
        },
        "status": {
            "privacyStatus": "private",
            "publishAt": publish_at.isoformat() + "Z"  # ISO 8601
        }
    }

    # ... rest of upload code

# Schedule for tomorrow at 9 AM
publish_time = datetime.utcnow() + timedelta(days=1)
publish_time = publish_time.replace(hour=9, minute=0, second=0)
```

## Using Refresh Tokens

```python
import json
from google.oauth2.credentials import Credentials

def save_credentials(credentials, filename="token.json"):
    """Save credentials for reuse."""
    with open(filename, "w") as f:
        json.dump({
            "token": credentials.token,
            "refresh_token": credentials.refresh_token,
            "token_uri": credentials.token_uri,
            "client_id": credentials.client_id,
            "client_secret": credentials.client_secret
        }, f)

def load_credentials(filename="token.json"):
    """Load saved credentials."""
    if os.path.exists(filename):
        with open(filename) as f:
            data = json.load(f)
            return Credentials(**data)
    return None

def get_youtube_service():
    """Get YouTube service with credential caching."""
    creds = load_credentials()

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "client_secrets.json", SCOPES
            )
            creds = flow.run_local_server(port=8080)

        save_credentials(creds)

    return build("youtube", "v3", credentials=creds)
```

## Rate Limits

- 10,000 quota units per day (default)
- Video upload: ~1600 units
- Request more quota if needed

## CLI Tool Alternative

```bash
# Install youtube-upload
pip install youtube-upload

# Upload via command line
youtube-upload \
    --title="My Video" \
    --description="Description here" \
    --tags="tag1,tag2" \
    --privacy="unlisted" \
    --client-secrets="client_secrets.json" \
    my_video.mp4
```

## Environment Variables

```bash
YOUTUBE_CLIENT_ID=
YOUTUBE_CLIENT_SECRET=
YOUTUBE_REFRESH_TOKEN=
```

## Sources

- [YouTube Data API Docs](https://developers.google.com/youtube/v3)
- [Upload Video Guide](https://developers.google.com/youtube/v3/guides/uploading_a_video)
- [YouTube Upload API Guide](https://getlate.dev/blog/youtube-upload-api)
- [youtube-upload CLI](https://github.com/tokland/youtube-upload)
