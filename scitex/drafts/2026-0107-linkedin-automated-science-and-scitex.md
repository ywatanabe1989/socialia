<!-- ---
!-- Timestamp: 2026-01-07 01:58:00
!-- Author: ywatanabe
!-- File: /home/ywatanabe/proj/social/scitex/drafts/2026-0107-linkedin-automated-science-and-scitex.md
!-- --- -->

# LinkedIn Post: AI Agent Assessment of SciTeX

**Character count: ~1,800**

---

I Asked an AI Agent: Does SciTeX Help Automated Science?

After my previous post on barriers to automated science, I asked the AI to assess our project.

INITIAL VERDICT

"SciTeX solves one pipe, not the whole plumbing."

Fair. But then it looked deeper at our scholar and writer modules...

REVISED ASSESSMENT

| Pain Point | Module | Solution |
|---|---|---|
| Papers are PDFs | scholar | Downloads, extracts metadata |
| Knowledge disconnected | citation_graph | Builds relationship graphs |
| Figures without data | bundles | Atomic packages with source |
| Can't reproduce | figrecipe | Recipe-based reproduction |
| Manuscripts unstructured | writer | Git-versioned LaTeX |

Stack coverage:
- Literature search (scholar.search_engines)
- PDF acquisition (scholar.pdf_download)
- Metadata enrichment (scholar.crossref)
- Citation analysis (scholar.citation_graph)
- Figure generation (plt, bundles)
- Manuscript writing (writer)
- Version control (writer.git)

THE HONEST VERDICT

"SciTeX is not 'one pipe'—it's substantial infrastructure covering literature to figures to manuscripts. For an AI agent doing literature-based research, SciTeX provides most of what I need.

The gaps are in experimental science (wet lab protocols, hypothesis formalization)—which may be out of scope anyway.

This is more serious infrastructure than I initially credited."

We'll take it.

---

#OpenScience #Reproducibility #AI #Research #SciTeX

<!-- EOF -->
