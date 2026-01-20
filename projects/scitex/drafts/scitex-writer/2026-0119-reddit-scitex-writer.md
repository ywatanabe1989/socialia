<!-- ---
!-- Timestamp: 2026-01-19 09:45:00
!-- Author: ywatanabe
!-- File: /home/ywatanabe/proj/social/scitex/drafts/scitex-writer/2026-0119-reddit-scitex-writer.md
!-- --- -->

# Reddit Draft: scitex-writer

**Target Subreddits:** r/MachineLearning, r/LocalLLaMA, r/LaTeX, r/AcademicPhilosophy, r/GradSchool, r/bioinformatics

---

## Title Options

**r/MachineLearning:**
[P] scitex-writer: MCP server that lets AI agents write complete scientific manuscripts — demo inside

**r/LocalLLaMA:**
scitex-writer: Let Claude Code write your scientific papers autonomously — open-source MCP server

**r/LaTeX:**
scitex-writer: LaTeX compilation system with AI agent integration — modular IMRAD, auto-diff, revision tracking

**r/GradSchool / r/AcademicPhilosophy:**
I built a tool that lets AI write scientific manuscripts. Here's a demo of it writing a 2,700-word paper in 25 minutes.

---

## Post Body

An AI agent that writes scientific manuscripts.

I built scitex-writer — a LaTeX compilation system with MCP server integration that lets AI agent write complete scientific papers autonomously.

**Demo Video:** https://scitex.ai/demos/watch/scitex-writer/

**GitHub:** https://github.com/ywatanabe1989/scitex-writer

`pip install scitex-writer`

In the demo, the AI agent:

- Generated a full IMRAD manuscript (Introduction, Methods, Results, Discussion)
- Linked figures, tables, and citations in contents
- Compiled to PDF in 27 seconds
- Tracked versions with Git diff
- Responded to simulated peer review

All in ~25 minutes for step by step demonstration. No human intervention.

---

**Key features:**

- Modular sections (abstract, intro, methods, results, discussion)
- Auto-deduplication of bibliographies
- Figure/table processing (PNG, PDF, SVG, Mermaid, CSV)
- Automatic diff PDF generation (red=deleted, blue=added)
- Manuscript, Supplementary Material, and Revision templates included
- Cross-platform (Linux, macOS, WSL2, Docker, HPC)

---

Fully open-source. Part of the SciTeX ecosystem.

This is the third standalone MCP server - graphing (figrecipe), literature search (crossref-local), and manuscript writing (scitex-writer) now available as MCP servers — we are building a foundation for automated science.

**All three MCP server demo videos:** https://scitex.ai/demos/

Feedback and contributions welcome!

---

## Media
- **Primary:** scitex-demos-page.png (screenshot of https://scitex.ai/demos/)
- **Alternative:** scitex-writer-v2.2.0-demo-thumbnail.png from ~/proj/scitex-writer/examples/

## Notes
- r/MachineLearning requires [P] prefix for projects
- r/LaTeX audience cares about compilation details
- r/LocalLLaMA likes local-first tools (mention it runs locally)
- Be honest about limitations
- Include demo thumbnail or link to video

<!-- EOF -->
