<!-- ---
!-- Timestamp: 2026-01-20 14:24:50
!-- Author: ywatanabe
!-- File: /home/ywatanabe/proj/social/scitex/drafts/automated-research/2026-0120-reddit-latex-automated-research.md
!-- --- -->

# Automated Research Demo - Reddit r/LaTeX Draft

## Status: DRAFT

## Subreddit: r/LaTeX

## Title
I built a LaTeX manuscript system where AI autonomously writes and compiles papers—40 min demo from literature search to revision

---

## Body

Hi r/LaTeX,

I've been building a LaTeX manuscript system called **scitex-writer** that addresses pain points from my PhD/postdoc. Recently added MCP integration that lets AI agents compile LaTeX directly.

**Demo: 40 minutes, almost zero human intervention**

An AI agent autonomously conducted a sleep-cognition study (3×3 factorial, N=180):
- Defined research theme
- Searched local CrossRef database (167M papers with abstracts)
- Analyzed demo data
- Ran statistical analysis (ANOVA, post-hoc tests)
- Created 4 publication-quality figures
- Wrote 21-page manuscript with proper citations
- Simulated peer review and drafted revision responses

**Demo video + repo:** https://github.com/ywatanabe1989/automated-research-demo

**Core features of scitex-writer:**

1. **Figure/table ↔ text linking:** Figures live in `contents/figures/` with matching `.tex` caption files. Build system handles placement and numbering—no manual `\ref{}` syncing.

2. **Section-based organization:** Each IMRAD section (intro, methods, results, discussion) is a separate `.tex` file. Easier to navigate, version control, collaborate.

3. **Revision workflow:** TRIPLET format organizes reviewer comments → author response → manuscript changes in parallel `.tex` files.

4. **`./compile` wrapper:** One command compiles. Add `--diff <commit>` to generate latexdiff PDF showing exactly what changed.

5. **MCP integration:** LaTeX compilation exposed as a tool AI can call directly. Claude writes → compiles → sees errors → fixes → recompiles.

**Future goal:** Automated verification of scientific integrity at each pipeline stage—from raw data to final manuscript. Less burden on reviewers, more reproducible science.

**Links:**
- Writer source: https://github.com/ywatanabe1989/scitex-code/tree/main/src/scitex/writer
- Full framework: https://scitex.ai
- License: AGPL-3.0

**Feedback welcome, especially on:**
- The section/figure organization approach
- The revision management workflow
- What's missing for your workflow?

---

## Assets
- Demo video: https://scitex.ai/demos/watch/scitex-automated-research/
- Repo: https://github.com/ywatanabe1989/automated-research-demo

<!-- EOF -->