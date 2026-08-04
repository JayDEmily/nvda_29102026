# NVDA Evolved Vision Reconstruction Corpus

This repository contains the admitted evidence corpus for Phase 1: lossless reconstruction of the user's intended NVDA desk system before architecture validation or implementation.

| Source tranche | Documents | Role | Repository path |
|---|---:|---|---|
| A — Original design-bearing gate contracts | 61 | Primary original planning authority | `source_planning/` |
| B — Recovered successor briefs | 37 | Candidate additions, clarifications, bounded repairs, amendments or process-only records | `source_successor_briefs/` |
| **Total admitted corpus** | **98** | Chronological proposition-level reconstruction | — |

Later does not automatically win. `AGENTS.md` defines the authority, supersession, review and losslessness rules.

`SOURCE_CORPUS_INVENTORY.md` is the human-readable source table. `SOURCE_MANIFEST.tsv` is the mechanical manifest.

## Mechanical validation

```bash
python tools/validate_source_corpus.py
```

This validates file counts, manifest identity, paths and SHA-256 values. It does not adjudicate semantic authority or supersession.
