# LinkedIn API Automation

## Status: Requires Approval

## Overview

LinkedIn provides official API access through Microsoft's developer portal. Requires application approval for posting capabilities.

## Access Requirements

- LinkedIn Developer Account
- App registration with LinkedIn
- `w_member_social` permission for posting
- Company Page admin access (for company posts)

## Setup Steps

1. **Create Developer Account**
   - Go to [LinkedIn Developers Portal](https://www.linkedin.com/developers/)
   - Create your application

2. **Request Permissions**
   - `w_member_social` - Post on behalf of member
   - `r_liteprofile` - Read profile
   - Most permissions require explicit approval

3. **Generate Token**
   - Visit [Token Generator](https://www.linkedin.com/developers/tools/oauth/token-generator)
   - Select your app
   - Check required scopes
   - Token expires in 60 days

## API Endpoints

```
# Get authenticated user
GET https://api.linkedin.com/v2/me

# Post to feed
POST https://api.linkedin.com/v2/posts

Headers:
  Authorization: Bearer {access_token}
  X-Restli-Protocol-Version: 2.0.0
  LinkedIn-Version: 202501
```

## Python Example

```python
import requests

headers = {
    "Authorization": f"Bearer {access_token}",
    "X-Restli-Protocol-Version": "2.0.0",
    "LinkedIn-Version": "202501",
    "Content-Type": "application/json"
}

# Get user URN
user = requests.get("https://api.linkedin.com/v2/me", headers=headers).json()
author_urn = f"urn:li:person:{user['id']}"

# Create post
post_data = {
    "author": author_urn,
    "lifecycleState": "PUBLISHED",
    "specificContent": {
        "com.linkedin.ugc.ShareContent": {
            "shareCommentary": {"text": "Hello LinkedIn!"},
            "shareMediaCategory": "NONE"
        }
    },
    "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"}
}

response = requests.post(
    "https://api.linkedin.com/v2/ugcPosts",
    headers=headers,
    json=post_data
)
```

## Limitations

- Token expires every 60 days (refresh required)
- Profile/Connections APIs highly restricted
- Partner program required for advanced features
- Individual developers limited vs. companies

## Alternative: Use Buffer/Hootsuite

For simpler setup, use third-party tools that handle LinkedIn API:
- Buffer ($6/mo per channel)
- Hootsuite ($99/mo)
- Zapier automation

## Environment Variables

```bash
LINKEDIN_CLIENT_ID=
LINKEDIN_CLIENT_SECRET=
LINKEDIN_ACCESS_TOKEN=
```

## Sources

- [LinkedIn Developers Portal](https://www.linkedin.com/developers/)
- [Posts API Documentation](https://learn.microsoft.com/en-us/linkedin/marketing/community-management/shares/posts-api)
- [Getting API Access](https://learn.microsoft.com/en-us/linkedin/shared/authentication/getting-access)
- [Posting via API Guide](https://marcusnoble.co.uk/2025-02-02-posting-to-linkedin-via-the-api/)
