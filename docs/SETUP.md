# Setup Guide

Complete step-by-step instructions for setting up API access.

## Twitter/X Setup

### Step 1: Create Developer Account

1. Go to https://developer.x.com
2. Sign in with your X account (@SciTeX_AI)
3. Click "Sign up for Free Account" or "Developer Portal"

### Step 2: Create a Project and App

1. In Developer Portal, click **Projects & Apps** → **+ New Project**
2. Name: `SciTeX Social Poster`
3. Use case: Select "Making a bot" or "Building tools"
4. Create an **App** within the project
5. App name: `scitex-poster`

### Step 3: Set App Permissions

**CRITICAL: Must be done before generating tokens**

1. Go to your App → **Settings** → **User authentication settings**
2. Click **Set up**
3. App permissions: Select **Read and write**
4. Type of App: Select **Web App, Automated App or Bot**
5. Callback URL: `https://localhost:3000/callback` (placeholder)
6. Website URL: `https://scitex.ai`
7. Save

### Step 4: Generate API Keys

1. Go to App → **Keys and tokens**
2. Under **Consumer Keys**, click **Regenerate**
3. Copy and save:
   - API Key (Consumer Key)
   - API Key Secret (Consumer Secret)

4. Under **Authentication Tokens** → **Access Token and Secret**
5. Click **Generate** (or Regenerate if exists)
6. Copy and save:
   - Access Token
   - Access Token Secret

### Step 5: Configure Environment

Add to `.env`:

```bash
export SCITEX_X_CONSUMER_KEY="kkjFPvxTZq7ZcxA2DOZbQntu9"
export SCITEX_X_CONSUMER_KEY_SECRET="your_consumer_secret_here"
export SCITEX_X_ACCESSTOKEN="your_access_token_here"
export SCITEX_X_ACCESSTOKEN_SECRET="your_access_token_secret_here"
```

### Step 6: Test

```bash
source .env
socialia post twitter "Test post" --dry-run
socialia post twitter "Hello from CLI!"  # Real post
```

### Troubleshooting

| Error | Solution |
|-------|----------|
| 403 Forbidden oauth1-permissions | App permissions not set to "Read and write". Go to Step 3, then regenerate tokens. |
| 401 Unauthorized | Tokens expired or invalid. Regenerate in Step 4. |
| Rate limit exceeded | Free tier: 500 posts/month. Wait or upgrade. |

---

## LinkedIn Setup

### Step 1: Create Developer Account

1. Go to https://www.linkedin.com/developers/
2. Sign in with LinkedIn account (social@scitex.ai)
3. Click **Create app**

### Step 2: Create Application

1. App name: `SciTeX Social Poster`
2. LinkedIn Page: Select your company page (scitex-ai)
3. Privacy policy URL: `https://scitex.ai/privacy`
4. App logo: Upload logo
5. Accept terms and click **Create app**

### Step 3: Request Permissions

1. Go to your App → **Products** tab
2. Request access to **Share on LinkedIn**
3. This adds `w_member_social` permission
4. Wait for approval (usually instant for Share)

### Step 4: Generate Access Token

**Option A: Token Generator (Easy, 60-day expiry)**

1. Go to https://www.linkedin.com/developers/tools/oauth/token-generator
2. Select your app
3. Check scopes: `w_member_social`, `r_liteprofile`
4. Click **Request access token**
5. Authorize the app
6. Copy the access token

**Option B: OAuth 2.0 Flow (For automation)**

1. Get Client ID and Secret from App → **Auth** tab
2. Implement OAuth 2.0 flow (see `docs/platforms/linkedin.md`)

### Step 5: Configure Environment

Add to `.env`:

```bash
export LINKEDIN_ACCESS_TOKEN="your_access_token_here"
export LINKEDIN_CLIENT_ID="your_client_id"
export LINKEDIN_CLIENT_SECRET="your_client_secret"
```

### Step 6: Test

```bash
source .env
socialia post linkedin "Test post" --dry-run
socialia post linkedin "Professional update from CLI!"
```

### Troubleshooting

| Error | Solution |
|-------|----------|
| 401 Unauthorized | Token expired (60-day limit). Regenerate in Step 4. |
| 403 Forbidden | Missing `w_member_social` permission. Request in Step 3. |
| Invalid scope | App not approved for Share on LinkedIn product. |

### Token Refresh Reminder

LinkedIn tokens expire after **60 days**. Set a calendar reminder to refresh.

```bash
# Check token validity
socialia --json post linkedin "test" --dry-run
```

---

## Reddit Setup (Coming Soon)

### Prerequisites
- Reddit account
- Subreddit karma requirements met

### Step 1: Create Application

1. Go to https://www.reddit.com/prefs/apps
2. Click **create another app...**
3. Name: `SciTeX Poster`
4. Type: Select **script**
5. Redirect URI: `http://localhost:8080`
6. Create app

### Step 2: Get Credentials

- Client ID: Under app name (short string)
- Client Secret: Listed as "secret"

### Environment Variables

```bash
export REDDIT_CLIENT_ID="your_client_id"
export REDDIT_CLIENT_SECRET="your_client_secret"
export REDDIT_USERNAME="your_username"
export REDDIT_PASSWORD="your_password"
```

---

## Google Analytics Setup

### Prerequisites
- Google account with access to Google Analytics
- GA4 property created for your website

### Step 1: Get Measurement ID

1. Go to https://analytics.google.com
2. Select your GA4 property
3. Click **Admin** (gear icon)
4. Under **Data collection and modification** → **Data streams**
5. Select your web stream
6. Copy the **Measurement ID** (format: `G-XXXXXXXXXX`)

### Step 2: Create API Secret (For Measurement Protocol)

1. In the same Data stream settings
2. Scroll to **Measurement Protocol API secrets**
3. Click **Create**
4. Name: `socialia`
5. Copy the generated secret

### Step 3: Get Property ID (For Data API - Optional)

1. In Admin → **Property settings**
2. Copy the **Property ID** (numeric, e.g., `123456789`)

### Step 4: Service Account (For Data API - Optional)

If you need to read analytics data (pageviews, sources):

1. Go to https://console.cloud.google.com
2. Create or select a project
3. Enable **Google Analytics Data API**
4. Go to **IAM & Admin** → **Service Accounts**
5. Create service account: `socialia-analytics`
6. Create key → JSON → Download
7. In Google Analytics Admin → **Property access management**
8. Add the service account email with **Viewer** role

### Step 5: Configure Environment

Add to `.env`:

```bash
# Required for tracking events
export GA_MEASUREMENT_ID="G-XXXXXXXXXX"
export GA_API_SECRET="your_api_secret_here"

# Optional for reading analytics data
export GA_PROPERTY_ID="123456789"
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account.json"
```

### Step 6: Test

```bash
source .env

# Track a custom event
socialia analytics track test_event --param key value

# Get realtime users (requires Data API setup)
socialia analytics realtime

# Get page views
socialia analytics pageviews --start 7daysAgo --end today

# Get traffic sources
socialia analytics sources
```

### Troubleshooting

| Error | Solution |
|-------|----------|
| Missing GA_MEASUREMENT_ID | Copy from GA4 Admin → Data Streams |
| Missing GA_API_SECRET | Create in Data stream → Measurement Protocol API secrets |
| Data API permission denied | Add service account to GA property with Viewer role |
| google-analytics-data not installed | Run: `pip install socialia[analytics]` |

---

## YouTube Setup

### Prerequisites
- Google account
- YouTube channel

### Step 1: Create Google Cloud Project

1. Go to https://console.cloud.google.com
2. Create new project: `SciTeX Social Poster`
3. Select the project

### Step 2: Enable YouTube API

1. Go to **APIs & Services** → **Library**
2. Search for **YouTube Data API v3**
3. Click **Enable**

### Step 3: Create OAuth Credentials

1. Go to **APIs & Services** → **Credentials**
2. Click **+ CREATE CREDENTIALS** → **OAuth client ID**
3. If prompted, configure OAuth consent screen:
   - User type: External
   - App name: `SciTeX Social Poster`
   - User support email: your email
   - Developer contact: your email
   - Add scopes: `youtube.upload`, `youtube`, `youtube.force-ssl`
   - Add test users: your email
4. Create OAuth client ID:
   - Application type: **Desktop app**
   - Name: `socialia`
5. Download the JSON file

### Step 4: Configure Environment

```bash
# Move the downloaded JSON to a secure location
mv ~/Downloads/client_secret_*.json ~/.youtube_client_secrets.json

# Add to .env
export YOUTUBE_CLIENT_SECRETS_FILE="$HOME/.youtube_client_secrets.json"
export YOUTUBE_TOKEN_FILE="$HOME/.youtube_token.json"
```

### Step 5: First-Time Authentication

The first time you use the YouTube poster, it will:
1. Open a browser for OAuth consent
2. Ask you to authorize the app
3. Save the token to `YOUTUBE_TOKEN_FILE`

```bash
source .env
socialia post youtube "Test video description" --video test.mp4 --title "Test" --dry-run
```

### Step 6: Test

```bash
# Upload a video
socialia post youtube "Video description" --video video.mp4 --title "My Video" --privacy unlisted

# With thumbnail and tags
socialia post youtube "Description" --video video.mp4 --title "Title" --thumbnail thumb.jpg --tags "tag1,tag2,tag3"
```

### Troubleshooting

| Error | Solution |
|-------|----------|
| YouTube libraries not installed | Run: `pip install socialia[youtube]` |
| OAuth consent required | Run once interactively to complete OAuth flow |
| Quota exceeded | YouTube API has daily quotas. Check console.cloud.google.com |
| Video processing failed | Check video format (MP4 recommended, max 128GB) |

### Notes

- **Community posts** require 500+ subscribers and are not available via API
- **Video uploads** consume quota (1600 units per upload, 10000 daily limit)
- OAuth tokens are stored locally and refresh automatically

---

## Quick Reference

| Platform | Token Location | Expiry | Refresh |
|----------|---------------|--------|---------|
| Twitter | developer.x.com → App → Keys | Never* | Manual regenerate |
| LinkedIn | developers.linkedin.com → Token Generator | 60 days | Manual regenerate |
| Reddit | reddit.com/prefs/apps | Never* | N/A |
| Google Analytics | analytics.google.com → Admin → Data Streams | Never* | N/A |
| YouTube | console.cloud.google.com → OAuth | Auto-refresh | OAuth token |

*Unless revoked manually
