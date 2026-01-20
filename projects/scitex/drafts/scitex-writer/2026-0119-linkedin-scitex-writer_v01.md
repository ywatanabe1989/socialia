<!-- ---
!-- Timestamp: 2026-01-19 09:53:26
!-- Author: ywatanabe
!-- File: /home/ywatanabe/proj/social/scitex/drafts/scitex-writer/2026-0119-linkedin-scitex-writer.md
!-- --- -->

# LinkedIn Draft: scitex-writer

**Target:** Researchers, academic writers, LaTeX users, AI/ML developers, research tool builders

---

## Post

An AI agent that writes scientific manuscripts.

I built scitex-writer — a LaTeX compilation system with MCP server integration that lets AI agent write complete scientific papers autonomously.

In the demo, the AI agent:

- Generated a full IMRAD manuscript
- Linked figures, tables, and citations in contents
- Compiled to PDF in 27 seconds
- Tracked versions with Git diff
- Responded to simulated peer review

All in ~25 minutes for step by step demonstration. No human intervention.

----------

Key features:

- Modular sections (abstract, intro, methods, results, discussion)
- Auto-deduplication of bibliographies
- Figure/table processing (PNG, PDF, SVG, Mermaid, CSV)
- Automatic diff PDF generation (red=deleted, blue=added)
- Manuscript, Supplementary Material, and Revision templates included
- Cross-platform (Linux, macOS, WSL2, Docker, HPC)

----------

Fully open-source. Part of the SciTeX ecosystem.

This is the third standalone MCP server - graphing (figrecipe), literature search (crossref-local), and manuscript writing (scitex-writer) now available as MCP servers — we have a solid foundation for automated science.

Demo Video: https://scitex.ai/demos/watch/scitex-writer/
All three MCP server demo videos: https://scitex.ai/demos/
GitHub: https://github.com/ywatanabe1989/scitex-writer
PyPI: pip install scitex-writer

#OpenSource #LaTeX #ScientificWriting #AIAgents #MCP #AcademicWriting #ResearchTools #AutomatedScience

---

## Media
- **Primary:** scitex-demos-page.png (screenshot of https://scitex.ai/demos/)
- **Alternative:** scitex-writer-v2.2.0-demo-thumbnail.png from ~/proj/scitex-writer/examples/

## Notes
- Emphasize: AI wrote the manuscript, not just formatted it
- Show the workflow: write → compile → version → revise
- Cross-platform is important for HPC users

<!-- EOF -->