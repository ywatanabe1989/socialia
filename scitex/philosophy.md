# SciTeX Philosophy

Core principles guiding SciTeX development and usage.

---

## 1. Proximity Principle

**Script and output should be close together.**

```
path/to/script.py      → path/to/script_out/
path/to/analysis.py    → path/to/analysis_out/
experiments/run_01.py  → experiments/run_01_out/
```

**Why:**
- Traceability: Immediately see which script produced which results
- Readability: No hunting across distant directories
- Reproducibility: Script + output stay bundled together
- Version control: Changes to script and output are co-located in commits

**Anti-pattern:**
```
scripts/analysis.py
results/2026-01-04/output.csv   # Where did this come from?
```

---

## 2. Output Naming Conventions

**Consistent `_out/` suffix for all script outputs.**

```
scripts/mnist/download.py       → scripts/mnist/download_out/
scripts/mnist/clf_svm.py        → scripts/mnist/clf_svm_out/
scripts/mnist/plot_digits.py    → scripts/mnist/plot_digits_out/
```

**Output directory structure:**
```
script_out/
├── data/                    # Symlinked artifacts (-> ./data/)
│   └── mnist/
│       └── figures/
│           └── result.jpg
├── RUNNING/                 # Active execution logs
├── FINISHED_SUCCESS/        # Successful run logs
│   └── 2025Y-02M-15D-01h10m16s_hOkM/
│       └── logs/
│           ├── stdout.log
│           └── stderr.log
├── FINISHED_FAILED/         # Failed run logs
└── [direct outputs]         # CSVs, NPYs, PKLs
```

**Timestamp format:** `YYYY`Y-`MM`M-`DD`D-`HH`h`MM`m`SS`s_`RAND`

---

## 3. Centralized Configuration

**Parameters belong in `./config/`, not in scripts.**

```yaml
# ./config/PATH.yaml
PATH:
  MNIST:
    FLATTENED:
      TRAIN: "./data/mnist/train_flattened.npy"
      TEST: "./data/mnist/test_flattened.npy"

# ./config/MNIST.yaml
MNIST:
  RANDOM_STATE: 42
  BATCH_SIZE: 64
```

**Precedence:** direct argument → config file → environment → default

**Why:**
- Single source of truth for parameters
- Easy to reproduce experiments
- No magic numbers buried in code

---

## 4. Symlinks for Data Flow

**Script outputs symlink to centralized `./data/` directory.**

```
./data/mnist/figures/confusion_matrix.jpg
    → ../../../scripts/mnist/plot_conf_mat_out/data/mnist/figures/confusion_matrix.jpg
```

**Why:**
- `./data/` provides unified access to all artifacts
- Source traceability maintained through proximity
- Avoids duplication while enabling organization

---

## 5. One Class/Function Per File

**Atomic units for maintainability.**

```
# Classes
_MarkdownChunker.py  → class MarkdownChunker(...)
_BaseCar.py          → class BaseCar(ABC, ...)

# Functions
_get_file_type.py    → def get_file_type(...)
_clean_text.py       → def clean_text(...)
```

**Private files start with underscore.**

**Each file includes:**
- The single class/function
- `main()` for usage demonstration
- Main guard (`if __name__ == "__main__"`)

---

## 6. Source-Test Mirroring

**One-to-one mapping between source and tests.**

```
src:   ./src/package/domain/filename.py
tests: ./tests/package/domain/test_filename.py

src:   ./src/package/domain/_private.py
tests: ./tests/package/domain/test__private.py  # double underscore
```

---

## 7. Explicit Over Implicit

**Naming should reveal intent.**

```python
# Good
mcp_server.py
ChromaVectorDBManager
def get_database_overview()

# Bad
server.py
VectorStore
def get_overview()
```

**Method format:** `verb_object()`
- `search()`, `get_topics()`, `load_config()`

---

## 8. Quality Gates

**Every change must pass:**
- [ ] All tests passing
- [ ] Coverage meets threshold
- [ ] No linting errors (ruff)
- [ ] Type checking passes (mypy)
- [ ] Documentation updated for API changes

---

## 9. Architectural Agreement First

**Before coding:**
1. Examine reference implementations
2. Present tree-like project structure
3. Get user feedback and iterate
4. Expand with method signatures
5. Document with Mermaid diagrams
6. Then implement

---

## 10. Development Sandbox

**`.dev/` for experiments, not production.**

```
.dev/           # gitignored sandbox
├── test_idea.py
└── scratch/
```

Successful experiments must be incorporated into `src/` or `scripts/`.

---

## Summary

| Principle | Key Rule |
|-----------|----------|
| Proximity | `script.py` → `script_out/` |
| Naming | `_out/` suffix, timestamps, status dirs |
| Config | `./config/*.yaml`, no magic numbers |
| Symlinks | `./data/` ← script outputs |
| Atomicity | One class/function per file |
| Mirroring | Source structure = test structure |
| Explicit | Names reveal purpose |
| Quality | Tests + lint + types + docs |
| Agreement | Architecture before implementation |
| Sandbox | `.dev/` for experiments only |
