---
description: |
  [TOPIC] Installation
  [DETAILS] pip install socialia. Per-platform extras pull only the SDKs you need (twitter, linkedin, reddit, slack, youtube, ga4).
tags: [socialia-installation]
---

# Installation

## Standard

```bash
pip install socialia
```

Core install pulls a thin shared layer; each platform pulls its own SDK on
demand via extras.

## Per-platform extras

| Platform   | Install                                | SDK pulled                  |
|------------|----------------------------------------|-----------------------------|
| Twitter/X  | `pip install socialia[twitter]`        | `tweepy`                    |
| LinkedIn   | `pip install socialia[linkedin]`       | `requests` + OAuth helpers  |
| Reddit     | `pip install socialia[reddit]`         | `praw`                      |
| Slack      | `pip install socialia[slack]`          | `slack-sdk`                 |
| YouTube    | `pip install socialia[youtube]`        | `google-api-python-client`  |
| GA4        | `pip install socialia[analytics]`      | `google-analytics-data`     |
| Everything | `pip install socialia[all]`            | all of the above            |

## Credentials

Each platform reads keys from env vars (e.g. `TWITTER_API_KEY`,
`LINKEDIN_ACCESS_TOKEN`). See [21_env-vars.md](21_env-vars.md) for the full
matrix.

## Verify

```bash
socialia --version
socialia status                              # per-platform auth + reachability
python -c "import socialia; print(socialia.__version__)"
```

## Editable install (development)

```bash
git clone https://github.com/ywatanabe1989/socialia
cd socialia
pip install -e .[all]
```
