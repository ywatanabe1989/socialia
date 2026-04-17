---
description: Full CLI reference for the `socialia` command.
---

# CLI Reference

Run `socialia --help` or `socialia --help-recursive` for the live tree.
Platforms accepted everywhere: `twitter`, `linkedin`, `reddit`, `slack`, `youtube`.

## Posting & content

```bash
socialia post <platform> "text" [--file FILE] [--dry-run] [--schedule SPEC]
socialia post twitter  "..." [--reply-to ID] [--quote ID] [--image PATH]
socialia post reddit   "..." [--subreddit NAME] [--title TITLE]
socialia post slack    "..." [--channel CH] [--thread-ts TS]
socialia post youtube  "desc" --video FILE [--title T] [--tags a,b]
                              [--thumbnail PATH] [--privacy public|private|unlisted]

socialia thread <platform> --file FILE [--dry-run]
socialia delete <platform> <post-id>
```

`--schedule` accepts `HH:MM`, `YYYY-MM-DD HH:MM`, `+1h`, `+30m`.

## Discovery / status

```bash
socialia status                      # env var + config snapshot
socialia check [platform] [--json]   # verify live credentials
socialia me <platform> [--json]      # authenticated user info
socialia feed [platform] [-l N] [--mentions] [--replies] [--detail] [--json]
socialia setup [platform|all]        # printable setup instructions
```

## Scheduling

```bash
socialia schedule list [--full]
socialia schedule cancel <job-id>
socialia schedule run
socialia schedule daemon [--interval SECONDS]
socialia schedule update-source <old> <new>
```

## Analytics (Google Analytics)

```bash
socialia analytics track <event> [-p KEY VALUE ...]
socialia analytics realtime
socialia analytics pageviews [--start 7daysAgo] [--end today] [--path P]
socialia analytics sources   [--start 7daysAgo] [--end today]
```

## Shell completion

```bash
socialia completion bash | zsh | install [--shell bash|zsh] | status
```

## Org-mode drafts

```bash
socialia org init <file> [--platform twitter]
socialia org status <file>
socialia org list <file>
socialia org schedule <file>
socialia org post <file> [--dry-run]
```

## Other

```bash
socialia youtube …                   # YouTube batch operations
socialia grow                        # Twitter discover + follow
socialia list-python-apis [-v] [-d N] [--json]

socialia mcp start                   # run MCP server (requires socialia[mcp])
socialia mcp list-tools [-v]
socialia mcp doctor
socialia mcp installation            # Claude Desktop config snippet
```
