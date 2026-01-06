# X/Twitter API Automation

## Status: Ready to Use

## Overview

X (Twitter) provides official API access for posting through the developer portal.

## API Tiers

| Tier | Cost | Posts/Month | Read Access | Best For |
|------|------|-------------|-------------|----------|
| Free | $0 | 500 | Very limited | Basic bots, testing |
| Basic | $200/mo | 50,000 | 10,000 tweets | Production apps |
| Pro | $5,000/mo | 1,000,000 | Full | Enterprise |

## Setup Steps

1. **Create Developer Account**
   - Go to [developer.x.com](https://developer.x.com)
   - Sign in with your X account
   - Apply for developer access

2. **Create App**
   - Create a new project in dashboard
   - Add an app to the project
   - Generate API keys

3. **Get Credentials**
   - API Key (Consumer Key)
   - API Secret (Consumer Secret)
   - Access Token
   - Access Token Secret
   - Bearer Token (for v2 API)

## Python Implementation

```python
# Install: pip install tweepy python-dotenv
import tweepy

client = tweepy.Client(
    consumer_key="API_KEY",
    consumer_secret="API_SECRET",
    access_token="ACCESS_TOKEN",
    access_token_secret="ACCESS_SECRET"
)

# Post text
client.create_tweet(text="Hello World!")

# Post with image (requires v1.1 API for upload)
auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)
media = api.media_upload("image.png")
client.create_tweet(text="With image!", media_ids=[media.media_id])
```

## Rate Limits (Free Tier)

- 500 posts per month (~16/day)
- 1 request per 24 hours on most read endpoints
- Media upload: separate limits

## Environment Variables

```bash
TWITTER_API_KEY=
TWITTER_API_SECRET=
TWITTER_ACCESS_TOKEN=
TWITTER_ACCESS_SECRET=
TWITTER_BEARER_TOKEN=
```

## Implementation

See `../src/twitter_poster.py` for full implementation.

## Sources

- [X Developer Portal](https://developer.x.com)
- [Tweepy Documentation](https://www.tweepy.org/)
- [X API Pricing 2025](https://twitterapi.io/blog/twitter-api-pricing-2025)
- [Getting X API Key Guide](https://elfsight.com/blog/how-to-get-x-twitter-api-key-in-2025/)
