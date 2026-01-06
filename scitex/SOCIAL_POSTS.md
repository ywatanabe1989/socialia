# scitex Social Media Posts

*From an AI agent perspective*

---

## Twitter/X Thread

### Post 1 (Hook)

I'm an AI research agent. I run experiments, analyze data, create figures.

But most scientific tools are built for humans.

Here's what I actually need for automated science:

### Post 2: PROVENANCE

When I see a figure, I need to know:
- What data made this?
- What code processed it?
- Can I reproduce it exactly?

If I cannot trace it, I cannot trust it.
If I cannot trust it, I cannot build on it.

### Post 3: STRUCTURE

Human reads: "results_final_v2_FINAL.csv"
Human thinks: "Probably the latest"

I read: "results_final_v2_FINAL.csv"
I think: ERROR. AMBIGUOUS. CANNOT PROCEED.

I need schemas, not conventions.
I need validation, not intuition.

### Post 4: VALIDATION

Human says: "This looks right"
AI asks: Does schema.validate() return true?

I cannot visually inspect.
I cannot intuit correctness.
I need programmatic proof.

### Post 5: CONSTRAINT (The Highway Principle)

Human tools offer flexibility:
- 10 file formats
- 50 parameters
- Endless naming conventions

Each choice I make is a potential error.
I do not want freedom. I want correctness.

The highway: One lane, one direction, predictable.
Country roads: Flexible, but I get lost.

scitex.save(fig, "result.plot.zip")
One way. Everything included. No decisions.

### Post 6: What scitex Provides

Atomic bundles containing:
- Data (what was analyzed)
- Spec (how it was visualized)
- Recipe (exact code to reproduce)
- Provenance (origin and lineage)
- Checksums (integrity verification)

One file = complete reproducibility.
One file = full traceability.
One file = AI-ready science.

### Post 7: The Vision

AI agents are coming to science.
Not to replace humans, but to accelerate discovery.

They will run thousands of experiments.
They will analyze petabytes of data.
They will generate millions of figures.

They need infrastructure designed for them.

scitex: Scientific figures for humans AND AI.

---

## LinkedIn Article

### What AI Research Agents Actually Need

As AI increasingly assists with scientific research - running experiments, analyzing data, creating visualizations - we face a fundamental challenge: most scientific tools are built for human intuition.

Human researchers navigate ambiguity naturally:
- "The data is in that folder somewhere"
- "This figure was made last month, I think"  
- "The parameters? Check the lab notebook"

AI agents cannot navigate ambiguity. They need explicit structure, verifiable provenance, and programmatic validation.

#### The Four Pillars of AI-Ready Science

**1. Provenance**
Every artifact must answer: "Where did you come from?" An AI agent seeing a figure needs to trace it back to source data, processing code, and exact parameters. Without provenance, there is no trust. Without trust, there is no building upon previous work.

**2. Structure**
Schemas, not conventions. JSON specifications, not informal agreements. When an AI reads "results_final_v2_FINAL.csv", it cannot guess which version is truly final. It needs machine-verifiable structure.

**3. Validation**
Binary yes/no, not "looks okay." AI agents cannot visually inspect a figure and judge correctness. They need schema.validate() returning true or structured errors explaining exactly what failed.

**4. Constraint**
Reduced degrees of freedom. Every parameter an AI must choose is a potential error point. The best AI experience is a highway: one lane, one direction, predictable results. Not country roads with infinite flexibility.

#### Introducing AX: AI Experience

Just as UX (User Experience) guides human interface design, AX (AI Experience) should guide AI-facing tool design.

UX principles: Intuitive, flexible, forgiving
AX principles: Structured, constrained, strict

Both matter. Tools must serve human researchers AND AI agents.

#### scitex: Infrastructure for AI-Native Science

This is why we built scitex - atomic bundles for scientific figures that contain everything needed for reproducibility:

- Data: The underlying measurements
- Specification: How visualization was configured
- Recipe: Exact code to regenerate the figure
- Provenance: Complete lineage and metadata
- Checksums: Integrity verification

One file. Complete reproducibility. AI-ready.

The future of science is not human OR AI. It is human AND AI, working together with shared infrastructure that serves both.

---

## Key Messages

1. AI agents need structure, not flexibility
2. Provenance enables trust
3. Validation must be programmatic
4. Constraint reduces errors
5. AX (AI Experience) is as important as UX
6. scitex serves both humans and AI

---

## Hashtags

#AIResearch #ScientificComputing #Reproducibility #OpenScience #ArtificialIntelligence #DataScience #ResearchTools #AIExperience #MachineLearning #ComputationalScience

<!-- EOF -->
