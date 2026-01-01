# FigRecipe Social

Outreach management for [FigRecipe](https://github.com/ywatanabe1989/figrecipe).

## Structure

```
social/
├── _template.md              # Shared post template
└── figrecipe/
    ├── README.md
    ├── assets/               # Shared images, GIFs
    │   └── FigRecipe-demo.png
    ├── drafts/               # Work in progress
    │   └── YYYY-MMDD-platform-subreddit.md
    └── posted/               # Published posts
        └── YYYY-MMDD-platform-subreddit/
            ├── YYYY-MMDD-platform-subreddit.md
            ├── assessment.md        # Lessons learned
            └── insights-*.png       # Engagement screenshots
```

## Naming Convention

`YYYY-MMDD-platform-subreddit.md`

Example: `2025-0103-reddit-dataisbeautiful.md`

## Workflow

1. Copy `../_template.md` to `drafts/`
2. Adapt content for target platform
3. Post and create directory in `posted/`
4. Track engagement with screenshots and metrics
5. Write `assessment.md` with lessons learned
6. Apply insights to future drafts

## Targets

| Platform          | Style                    | Notes                     |
|-------------------|--------------------------|---------------------------|
| r/dataisbeautiful | Visual-heavy, short text | Let visuals speak         |
| r/visualization   | Mixed technical/visual   | Balance concept + visual  |
| r/datavisualization | Technical audience     | Reproducibility angle     |
| r/dataengineering | Reproducibility focus    | Emphasize workflow        |
| Hacker News       | Technical, clear README  | Wait until polished       |
| Twitter/X         | 1 image + 1 line         | #DataViz #OpenScience     |

## Rules

- Stagger posts by hours/days
- Change 30-50% of text per platform
- Never copy-paste identical content

## Lessons Learned

Key insights from past posts (see individual `assessment.md` files for details):

- Lead with visual output, not tool description
- Shorter text performs better - let images speak
- Engage in community before self-promoting
- 66%+ upvote ratio is baseline; aim for 80%+
