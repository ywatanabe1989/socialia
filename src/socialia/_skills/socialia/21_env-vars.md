---
name: socialia-env-vars
description: Environment variables read by socialia at import / runtime. Follow SCITEX_<MODULE>_* convention — see general/10_arch-environment-variables.md.
tags: [socialia, scitex-package]
---

# socialia — Environment Variables

| Variable | Purpose | Default | Type |
|---|---|---|---|
| `SCITEX_X_CONSUMER_KEY` | Twitter/X API v1.1 consumer key (OAuth 1.0a). Required for posting to X. | `—` | string (required) |

## Notes

- socialia also reads platform-specific credentials (Mastodon access token,
  Bluesky app-password, LinkedIn OAuth tokens) via each platform's SDK-owned
  env vars — see `20_environment.md` for the full per-platform table.
- The SciTeX-namespaced var above is the only `SCITEX_*` env var socialia
  reads directly.

## Audit

```bash
grep -rhoE 'SCITEX_[A-Z0-9_]+' $HOME/proj/socialia/src/ | sort -u
```
