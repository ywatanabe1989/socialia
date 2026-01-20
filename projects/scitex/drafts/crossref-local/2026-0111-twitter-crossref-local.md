<!-- ---
!-- Timestamp: 2026-01-11 14:44:23
!-- Author: ywatanabe
!-- File: /home/ywatanabe/proj/social/scitex/drafts/crossref-local/2026-0111-twitter-crossref-local.md
!-- --- -->

# Twitter Draft: crossref-local

**Target:** AI/ML researchers, research tool builders, automated science community

---

## Thread Option

**Tweet 1:**




Released a database system for automated research agents, using CrossRef Open Database.

github.com/ywatanabe1989/crossref-local

pip install crossref-local

crossref-local solves this:
- 167M scholarly works
- Full abstracts
- Impact factors
- Citation graphs
- Local, instant, no limits

Feedback welcome!


**Tweet 2 (reply):**
```bash
$ crossref-local search "CRISPR" -n 1 -a

# Found 87,473 matches in 18.2ms
# 1. RS-1 enhances CRISPR/Cas9-...
#    Journal: Nature Communications
#    Abstract: Zinc-finger nuclease...
```

22ms across 167M papers. Full abstracts for LLM context.

**Tweet 3 (reply):**
Impact factors calculated from raw citation data.

Validated against JCR (Spearman r = 0.736).
Some journals show lower estimates — investigating.

Still useful for relative quality ranking.

---

## Single Tweet Option

A database for automated research agents.

Major databases lack abstracts, impact factors, citation graphs — and impose rate limits.

crossref-local: 167M papers. Local. Instant. No limits.

github.com/ywatanabe1989/crossref-local

---

## Notes
- Include readme_figure.png
- Matches LinkedIn professional tone
- Honest about IF caveat

<!-- EOF -->