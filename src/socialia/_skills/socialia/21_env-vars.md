---
description: |
  [TOPIC] Env Vars
  [DETAILS] Environment variables read by socialia at import / runtime. Follow SCITEX_<MODULE>_* convention — see general/10_arch-environment-variables.md.
tags: [socialia-env-vars]
---

# socialia — Environment Variables

All variables use the `SCITEX_` prefix via the branding registry
(see `20_environment.md` for the `SOCIALIA_`-prefixed equivalents).

| Variable | Purpose | Default | Type |
|---|---|---|---|
| `SCITEX_X_CONSUMER_KEY` | Twitter/X API v1.1 consumer key (OAuth 1.0a) | `—` | string (required) |
| `SCITEX_X_CONSUMER_KEY_SECRET` | Twitter/X API consumer secret | `—` | string (required) |
| `SCITEX_X_ACCESSTOKEN` | Twitter/X access token | `—` | string (required) |
| `SCITEX_X_ACCESSTOKEN_SECRET` | Twitter/X access token secret | `—` | string (required) |
| `SCITEX_LINKEDIN_ACCESS_TOKEN` | LinkedIn OAuth access token | `—` | string (required) |
| `SCITEX_LINKEDIN_CLIENT_ID` | LinkedIn OAuth client ID | `—` | string (optional) |
| `SCITEX_LINKEDIN_CLIENT_SECRET` | LinkedIn OAuth client secret | `—` | string (optional) |
| `SCITEX_REDDIT_CLIENT_ID` | Reddit app client ID | `—` | string (required) |
| `SCITEX_REDDIT_CLIENT_SECRET` | Reddit app client secret | `—` | string (required) |
| `SCITEX_REDDIT_USERNAME` | Reddit account username | `—` | string (required) |
| `SCITEX_REDDIT_PASSWORD` | Reddit account password | `—` | string (required) |
| `SCITEX_REDDIT_USER_AGENT` | Reddit API user agent string | `Socialia v0.1` | string (optional) |
| `SCITEX_SLACK_BOT_TOKEN` | Slack bot OAuth token | `—` | string (required) |
| `SCITEX_SLACK_DEFAULT_CHANNEL` | Default Slack channel | `—` | string (optional) |
| `SCITEX_YOUTUBE_CLIENT_SECRETS_FILE` | Path to YouTube OAuth client secrets JSON | `—` | string (required) |
| `SCITEX_YOUTUBE_TOKEN_FILE` | Path to YouTube OAuth token JSON | `runtime/youtube_token.json` | string (optional) |
| `SCITEX_GOOGLE_ANALYTICS_MEASUREMENT_ID` | GA4 measurement ID (format: G-XXXXXXXXXX) | `—` | string (required) |
| `SCITEX_GOOGLE_ANALYTICS_API_SECRET` | GA4 Measurement Protocol API secret | `—` | string (required) |
| `SCITEX_GOOGLE_ANALYTICS_PROPERTY_ID` | GA4 property ID for Data API | `—` | string (optional) |
| `SCITEX_GOOGLE_APPLICATION_CREDENTIALS` | Path to GCP service account JSON for GA4 Data API | `—` | string (optional) |

## Lookup order

Each variable is resolved in this priority order (see `_branding.py`):

1. `SCITEX_<KEY>` (SciTeX-namespaced)
2. `SOCIALIA_<KEY>` (legacy brand prefix)
3. `<KEY>` (unprefixed fallback)

## Notes

- Only variables actually read by the codebase are listed above.
  `grep -rhoE 'SCITEX_[A-Z0-9_]+'` is not an accurate audit — the
  branding registry resolves at runtime, not via literal string search.

## Audit

```bash
python3 -c "
from socialia._branding import get_env
keys = ['X_CONSUMER_KEY', 'LINKEDIN_ACCESS_TOKEN', 'REDDIT_CLIENT_ID',
        'SLACK_BOT_TOKEN', 'YOUTUBE_CLIENT_SECRETS_FILE',
        'GOOGLE_ANALYTICS_MEASUREMENT_ID', 'GOOGLE_APPLICATION_CREDENTIALS']
for k in keys:
    print(f'{k:45s} → {get_env(k) or \"(not set)\"}')
```
