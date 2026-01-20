<!-- ---
!-- Timestamp: 2026-01-11 14:39:35
!-- Author: ywatanabe
!-- File: /home/ywatanabe/proj/social/scitex/drafts/crossref-local/posted/2026-0111-linkedin-crossref-local.md
!-- --- -->

# LinkedIn Draft: crossref-local

**Target:** Researchers, data scientists, LLM/AI developers, research tool builders
https://www.linkedin.com/feed/update/urn:li:activity:7415955472794562560/

---

## Post

A database for automated research agents.

Major academic databases lack what AI scientists need most: abstracts, impact factors, and citation graphs. They also impose strict rate limits.

To address these challenges, I developed crossref-local — a fully open-source Python package built on CrossRef open data.

- 167M scholarly works
- Full abstracts
- Impact factors
- Citation graphs
- Local
- Instant
- No limits

----------
$ crossref-local search "CRISPR" -n 1 -a

# Found 87,473 matches in 18.2ms
# 
# 1. RS-1 enhances CRISPR/Cas9- and TALEN-mediated knock-in efficiency (2016)
#  DOI: 10.1038/ncomms10548
#  Journal: Nature Communications
#  Abstract: Zinc-finger nuclease, transcription activator-like effector nuclease
#  and CRISPR/Cas9 are becoming major tools for genome editing. Importantly,
#  knock-in in several non-rodent species has been finally achieved...
----------

Feedback and contributions are welcome.

GitHub: https://lnkd.in/gkHbQc4c

#OpenSource #ResearchTools #LLM #RAG #AcademicResearch #AIAgents #AutomatedScience #Python

## Notes
- Include readme_figure.png showing IF validation + citation network
- Five pillars: evidence, abstracts, impact factor, speed, local

<!-- EOF -->