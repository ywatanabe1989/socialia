<!-- ---
!-- Timestamp: 2026-01-01 14:31:22
!-- Author: ywatanabe
!-- File: /home/ywatanabe/proj/social/CLAUDE.md
!-- --- -->

# Social Outreach Project

## Purpose
Manage SNS outreach for open-source projects (SciTeX ecosystem, FigRecipe, etc.) with systematic tracking and continuous improvement.

## Workflow

### When user shares a post URL/screenshot:
1. Identify the project and platform
2. Create or update the post log in `[project]/posted/YYYY-MMDD-platform/`
3. Extract and log engagement metrics from screenshots
4. Save screenshots as `insights-YYYYMMDD-HHMM.png`
5. Create/update `assessment.md` with lessons learned

### Post Structure
```
[project]/posted/YYYY-MMDD-platform/
├── YYYY-MMDD-platform.md    # Post content, URL, metrics
├── assessment.md            # Analysis and lessons
└── insights-*.png           # Engagement screenshots
```

## Gradual Improvement Strategy

### Track Over Time
- Log engagement metrics at multiple time points (1h, 24h, 1w)
- Compare performance across platforms and post types
- Identify patterns in successful vs underperforming posts

### Iterate on Content
- Apply lessons from assessments to future drafts
- A/B test different formats (text-heavy vs visual, long vs short)
- Adapt tone/style per platform norms

### Optimize Posting
- Track best posting times by platform
- Monitor hashtag effectiveness
- Build engagement before self-promotion

## Quality Guidelines
- Always include URL in post logs
- Save screenshots for historical tracking
- Write honest assessments (what failed matters most)
- Keep action items specific and actionable

## Projects
| Project   | Focus                       | Key Platforms                    |
|-----------|-----------------------------|----------------------------------|
| figrecipe | Data visualization library  | Reddit, LinkedIn                 |
| scitex    | Research workflow ecosystem | LinkedIn, Twitter, Note, Medium  |

## Analytics

| Project   | Platform         | Account          | Dashboard URL                                                                                        |
|-----------|------------------|------------------|------------------------------------------------------------------------------------------------------|
| scitex    | Google Analytics | social@scitex.ai | https://analytics.google.com/analytics/web/#/p518230835/reports/intelligenthome |

## Accounts

| Platform  | Username/Handle | Email (Now)       | Email (Should be) | URL                                        | Env Var          |
|-----------|-----------------|-------------------|-------------------|--------------------------------------------|------------------|
| LinkedIn  | scitex.ai       | social@scitex.ai  | social@scitex.ai  | https://linkedin.com/company/scitex-ai     | `LINKEDIN_PASS`  |
| X/Twitter | @SciTeX_AI      | social@scitex.ai  | social@scitex.ai  | https://x.com/SciTeX_AI                    | `TWITTER_PASS`   |
| Reddit    |                 |                   | social@scitex.ai  | https://reddit.com/u/                      | `REDDIT_PASS`    |
| Instagram |                 | support@scitex.ai | social@scitex.ai  | https://instagram.com/                     | `INSTAGRAM_PASS` |
| TikTok    |                 |                   | social@scitex.ai  | https://tiktok.com/@                       | `TIKTOK_PASS`    |
| YouTube   |                 |                   | social@scitex.ai  | https://youtube.com/@                      | `YOUTUBE_PASS`   |
| Note      |                 |                   | social@scitex.ai  | https://note.com/                          | `NOTE_PASS`      |
| Medium    |                 |                   | social@scitex.ai  | https://medium.com/@                       | `MEDIUM_PASS`    |
| Buffer    |                 |                   | social@scitex.ai  | https://buffer.com                         | `BUFFER_PASS`    |
| Twitch    | scitex_ai       |                   | social@scitex.ai  | https://twitch.tv/scitex_ai                | `TWITCH_PASS`    |
| Slack     | scitexworkspace | admin@scitex.ai   | social@scitex.ai  | https://scitexworkspace.slack.com          | `SLACK_PASS`     |

## Environment Files

```
social/
├── .env                    # Shared account credentials
├── scitex/.env             # SciTeX-specific (GA, APIs)
└── figrecipe/.env          # FigRecipe-specific (GA, APIs)
```

**Root `.env`** — shared across all projects:
- `SCITEX_EMAIL_PASSWORD` — social@scitex.ai
- `LINKEDIN_PASS`, `TWITTER_PASS`, etc.

**Project `.env`** — project-specific tracking:
- `GOOGLE_ANALYTICS_ID`
- Project-specific API keys

**Loading:**
```bash
# For scitex work
source .env && source scitex/.env

# For figrecipe work
source .env && source figrecipe/.env
```

**Security**: All `.env` files excluded via `.gitignore`


TEL AU: +61-4-6152-2907
TEL JA: +81-80-4022-3567

Linkedin -> Personal
https://www.linkedin.com/in/yusuke-watanabe-870953170/

<!-- EOF -->