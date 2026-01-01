# Social

Private repository for managing SNS outreach across projects.

## Structure

```
social/
├── _template.md        # Shared post template
├── figrecipe/          # FigRecipe outreach
├── [project]/          # Future projects
└── docs/               # Claude configuration
```

## Naming Convention

`YYYY-MMDD-platform-subreddit.md`

## Workflow

1. Create project directory (e.g., `figrecipe/`)
2. Add `assets/`, `drafts/`, and `posted/` subdirectories
3. Copy `_template.md` for new posts in `drafts/`
4. After posting, create directory in `posted/` with all related files
5. Track engagement with screenshots and metrics
6. Write `assessment.md` with lessons learned
7. Update project README with key insights

## Post Structure

Each posted item contains:
```
YYYY-MMDD-platform/
├── YYYY-MMDD-platform.md    # Post content & metrics
├── assessment.md            # Lessons learned
└── insights-*.png           # Engagement screenshots
```

## Projects

| Project   | Status | Platforms |
|-----------|--------|-----------|
| figrecipe | Active | Reddit, LinkedIn |
| scitex    | Active | LinkedIn, Twitter |
