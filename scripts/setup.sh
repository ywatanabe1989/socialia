#!/usr/bin/env bash
# -*- coding: utf-8 -*-
# Socialia - Platform Setup Guide
# Usage: ./scripts/setup.sh [platform]
# Platforms: twitter, linkedin, reddit, youtube, analytics, all

set -euo pipefail

usage() {
    cat <<'EOF'
Usage: ./scripts/setup.sh [platform]

Platforms:
  twitter     Twitter/X API setup
  linkedin    LinkedIn API setup
  reddit      Reddit API setup
  youtube     YouTube API setup
  analytics   Google Analytics setup
  all         Show all platform guides

Examples:
  ./scripts/setup.sh twitter
  ./scripts/setup.sh all
EOF
}

setup_twitter() {
    cat <<'EOF'
TWITTER/X SETUP
===============

1. Go to https://developer.x.com
2. Create app with Read+Write permissions
3. Generate API keys and access tokens

Environment Variables:
  export SCITEX_X_CONSUMER_KEY="..."
  export SCITEX_X_CONSUMER_KEY_SECRET="..."
  export SCITEX_X_ACCESSTOKEN="..."
  export SCITEX_X_ACCESSTOKEN_SECRET="..."

Test:
  socialia post twitter "Test" --dry-run

Full guide: docs/SETUP.md
EOF
}

setup_linkedin() {
    cat <<'EOF'
LINKEDIN SETUP
==============

1. Go to https://www.linkedin.com/developers/
2. Create app, request 'Share on LinkedIn' product
3. Generate token at Token Generator

Environment Variables:
  export LINKEDIN_ACCESS_TOKEN="..."

Note: Tokens expire after 60 days.

Test:
  socialia post linkedin "Test" --dry-run

Full guide: docs/SETUP.md
EOF
}

setup_reddit() {
    cat <<'EOF'
REDDIT SETUP
============

1. Go to https://www.reddit.com/prefs/apps
2. Create 'script' type app

Environment Variables:
  export REDDIT_CLIENT_ID="..."
  export REDDIT_CLIENT_SECRET="..."
  export REDDIT_USERNAME="..."
  export REDDIT_PASSWORD="..."

Test:
  socialia post reddit "Test" --subreddit test --dry-run

Full guide: docs/SETUP.md
EOF
}

setup_youtube() {
    cat <<'EOF'
YOUTUBE SETUP
=============

1. Go to https://console.cloud.google.com/
2. Enable YouTube Data API v3
3. Create OAuth 2.0 credentials
4. Download client_secrets.json

Environment Variables:
  export YOUTUBE_CLIENT_SECRETS_FILE="/path/to/client_secrets.json"

Test:
  socialia post youtube "Test" --video test.mp4 --dry-run

Full guide: docs/SETUP.md
EOF
}

setup_analytics() {
    cat <<'EOF'
GOOGLE ANALYTICS SETUP
======================

1. Go to https://analytics.google.com/
2. Admin > Data Streams > Measurement Protocol API secrets

Environment Variables:
  export GA_MEASUREMENT_ID="G-XXXXXXXXXX"
  export GA_API_SECRET="..."
  export GA_PROPERTY_ID="..." (optional, for Data API)

Test:
  socialia analytics track test_event

Full guide: docs/SETUP.md
EOF
}

main() {
    if [[ $# -eq 0 ]]; then
        usage
        exit 0
    fi

    case "$1" in
    -h | --help)
        usage
        exit 0
        ;;
    twitter)
        setup_twitter
        ;;
    linkedin)
        setup_linkedin
        ;;
    reddit)
        setup_reddit
        ;;
    youtube)
        setup_youtube
        ;;
    analytics)
        setup_analytics
        ;;
    all)
        setup_twitter
        echo ""
        setup_linkedin
        echo ""
        setup_reddit
        echo ""
        setup_youtube
        echo ""
        setup_analytics
        ;;
    *)
        echo "Unknown platform: $1" >&2
        usage
        exit 1
        ;;
    esac
}

main "$@"
