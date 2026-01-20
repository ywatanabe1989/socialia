<!-- ---
!-- Timestamp: 2026-01-11 14:39:58
!-- Author: ywatanabe
!-- File: /home/ywatanabe/proj/social/scitex/drafts/crossref-local/posted/2026-0111-reddit-crossref-local.md
!-- --- -->

# Reddit Draft: crossref-local
https://www.reddit.com/r/ResearchML/comments/1q9osrj/p_crossreflocal_167m_papers_with_abstracts_impact/


**Target Subreddits:** r/MachineLearning, r/LocalLLaMA, r/Python, r/datascience, r/bioinformatics

---

## Title Options

**r/MachineLearning / r/LocalLLaMA:**
[P] crossref-local: 167M papers with abstracts, impact factors, citation graphs — local, instant, no limits

**r/Python:**
crossref-local: Local database of 167M scholarly works with full abstracts and impact factors

**r/datascience / r/bioinformatics:**
A database for automated research agents — 167M papers with abstracts, impact factors, citation graphs

---

## Post Body

Major academic databases lack what AI scientists need most: abstracts, impact factors, and citation graphs. They also impose strict rate limits.

To address these challenges, I developed crossref-local — a fully open-source Python package built on CrossRef open data.

**167M scholarly works. Full abstracts. Impact factors. Citation graphs. Local. Instant. No limits.**

```bash
$ crossref-local search "CRISPR" -n 1 -a

# Found 87,473 matches in 18.2ms
#
# 1. RS-1 enhances CRISPR/Cas9- and TALEN-mediated knock-in efficiency (2016)
#    DOI: 10.1038/ncomms10548
#    Journal: Nature Communications
#    Abstract: Zinc-finger nuclease, transcription activator-like effector nuclease
#    and CRISPR/Cas9 are becoming major tools for genome editing. Importantly,
#    knock-in in several non-rodent species has been finally achieved...
```

**Note on impact factors:** Calculated from raw citation data, validated against JCR (Spearman r = 0.736). Some journals show lower estimates than official values — investigation ongoing.

**Tradeoff:** Database is 1.5TB and takes ~2 weeks to build from CrossRef data dump. Working on hosting options.

Feedback and contributions are welcome.

GitHub: https://github.com/ywatanabe1989/crossref-local

`pip install crossref-local`

---

## Notes
- Include readme_figure.png
- Honest about IF limitations and DB size
- LocalLLaMA loves "local, no API" angle

<!-- EOF -->