---
description: Environment variables per platform. All names prefixed with SOCIALIA_ by default.
---

# Environment Variables

Defaults use the `SOCIALIA_` prefix. Override prefix with `SOCIALIA_ENV_PREFIX=<NAME>`; `SOCIALIA_*` is always a fallback.

## Twitter/X

| Variable | Purpose |
|----------|---------|
| `SOCIALIA_X_CONSUMER_KEY` | Consumer key |
| `SOCIALIA_X_CONSUMER_KEY_SECRET` | Consumer secret |
| `SOCIALIA_X_ACCESSTOKEN` | Access token |
| `SOCIALIA_X_ACCESSTOKEN_SECRET` | Access token secret |

## LinkedIn

| Variable | Purpose |
|----------|---------|
| `SOCIALIA_LINKEDIN_ACCESS_TOKEN` | OAuth 2.0 access token |

## Reddit

| Variable | Purpose |
|----------|---------|
| `SOCIALIA_REDDIT_CLIENT_ID` | App client ID |
| `SOCIALIA_REDDIT_CLIENT_SECRET` | App client secret |
| `SOCIALIA_REDDIT_USERNAME` | Reddit username |
| `SOCIALIA_REDDIT_PASSWORD` | Reddit password |

## Slack

| Variable | Purpose |
|----------|---------|
| `SOCIALIA_SLACK_BOT_TOKEN` | Bot token (`xoxb-…`) |
| `SOCIALIA_SLACK_DEFAULT_CHANNEL` | Default channel when `channel` kwarg omitted |

## YouTube

| Variable | Purpose |
|----------|---------|
| `SOCIALIA_YOUTUBE_CLIENT_SECRETS_FILE` | Path to OAuth client secrets JSON |

## Google Analytics

| Variable | Purpose |
|----------|---------|
| `SOCIALIA_GOOGLE_ANALYTICS_MEASUREMENT_ID` | GA4 measurement ID |
| `SOCIALIA_GOOGLE_ANALYTICS_API_SECRET` | GA4 Measurement API secret |
| `SOCIALIA_GOOGLE_ANALYTICS_PROPERTY_ID` | GA4 property ID (Data API, optional) |

Run `socialia status` to see which variables are currently set.
