# Method, Status and Source Manifest

## Scope

Phase 1 design-intent reconstruction from exactly 98 immutable Markdown sources: 61 original gate contracts and 37 recovered successor briefs. No implementation, tests, Atlas, current architecture or external project material is semantic evidence.

## Baseline status

| Item | Result |
|---|---|
| Archive SHA-256 | `ac6af01badc5cd2dcc7ce770f7b50fd39d9c1bef026842d5fc545b5a6e103679` |
| Initial branch | `main` |
| Initial HEAD | `e908d3b072e4b1812e7fd2a1ce56563a1e4c6900` |
| Initial worktree | Clean |
| Tranche A count | 61 |
| Tranche B count | 37 |
| Corpus validator | PASS |
| Mechanical manifest | `SOURCE_MANIFEST.tsv` |

Exact initial commands and validator output are preserved in `reconstruction/evidence/INITIAL_BASELINE.txt`.

## Method

Semantic work is performed chronologically in the tranche schedule defined by `PLANS.md`. Each source is read in full. Material instructions are represented as stable propositions with exact line lineage. Tranche B propositions are classified individually before changing the canonical vision. Later chronology alone never establishes supersession.

Mechanical checks validate source identity, coverage, proposition identifiers and citation form only. They do not create or certify semantic meaning.

## Worker and reviewer setting

- Programme manager / semantic worker: GPT-5.6 Thinking in the current execution context.
- Review pass: separate source-and-diff pass after each tranche, recorded under `reconstruction/tranches/`.
- Limitation: no distinct fresh-model subagent context is available. Review separation is procedural, not genuinely independent. This remains explicit in final assurance.

## Source hashes

`SOURCE_MANIFEST.tsv` is the authoritative mechanical list of all 98 admitted paths and SHA-256 values. It was validated against the filesystem before semantic extraction and is not modified by this work.

## Tranche status

| Tranche | Sources | Verdict | Commit |
|---|---:|---|---|
| Plan/baseline | 98 inventoried | PASS (mechanical only) | pending |
