#!/bin/bash
# -*- coding: utf-8 -*-
# Timestamp: 2026-01-21
# Socialia Examples - Run All
#
# Usage:
#   ./00_run_all.sh           # Run all examples (dry-run mode)
#   ./00_run_all.sh --real    # Run with real posting (requires credentials)

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Parse arguments
REAL_MODE=false
if [[ "$1" == "--real" ]]; then
    REAL_MODE=true
    echo "WARNING: Running in REAL mode - posts will be published!"
    read -p "Continue? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 0
    fi
fi

echo "======================================"
echo "Socialia Examples"
echo "======================================"
echo ""

# 01: Twitter posting
echo "--- 01: Twitter Posting ---"
if $REAL_MODE; then
    python 01_post_twitter.py
else
    python 01_post_twitter.py --dry-run
fi
echo ""

# 02: LinkedIn posting
echo "--- 02: LinkedIn Posting ---"
if $REAL_MODE; then
    python 02_post_linkedin.py
else
    python 02_post_linkedin.py --dry-run
fi
echo ""

# 03: Thread posting
echo "--- 03: Thread Posting ---"
if $REAL_MODE; then
    python 03_thread_twitter.py
else
    python 03_thread_twitter.py --dry-run
fi
echo ""

# 04: Analytics (always dry-run safe)
echo "--- 04: Analytics ---"
python 04_analytics.py
echo ""

echo "======================================"
echo "All examples completed!"
echo "======================================"
