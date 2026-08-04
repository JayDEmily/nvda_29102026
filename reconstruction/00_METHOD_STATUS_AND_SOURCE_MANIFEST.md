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
| Plan/baseline | 98 inventoried | PASS (mechanical only) | `d9bf965` |
| A01 | 4 | PASS | `042b57d` |
| A02 | 4 | PASS | `a6ec84b` |
| A03 | 4 | PASS | `62be887` |
| A04 | 4 | PASS | `6741dfb` |
| A05 | 4 | PASS | `f79ec4f` |
| A06 | 4 | PASS | `d36fe5e` |
| A07 | 4 | PASS | `f0b016d` |
| A08 | 4 | PASS | `e9993b4` |
| A09 | 4 | PASS | `46fb998` |
| A10 | 4 | PASS | `72037f7` |
| A11 | 4 | PASS | `c3e79f7` |
| A12 | 4 | PASS | `243ddd0` |
| A13 | 4 | PASS | `a95cb07` |
| A14 | 4 | PASS | `6f70388` |
| A15 | 5 | PASS | `f585e26` |
| B01 | 3 | PASS | `0718d95` |
| B02 | 5 | PASS | `6f32b7d` |
| B03 | 5 | PASS | `ac95830` |
| B04 | 3 | PASS | `96a7f27` |
| B05 | 3 | PASS (no canonical proposition) | `eb96212` |
| B06 | 3 | PASS | `a8d7a14` |
| B07 | 3 | PASS | `80224f2` |
| B08 | 4 | PASS | `75d82f2` |
| B09 | 3 | PASS | `f9152fb` |
| B10 | 5 | PASS | `aa0318e` |
| Final consolidation | 83 propositions / 10 capability documents | in progress | pending |
