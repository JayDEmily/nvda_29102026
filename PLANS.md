# ExecPlan — NVDA Evolved Vision Reconstruction

## Objective

Reconstruct a clean, lossless and chronologically resolved English specification of the intended NVDA desk system from the 98 immutable admitted source documents only: 61 original planning contracts in `source_planning/` and 37 recovered successor briefs in `source_successor_briefs/`.

This is Phase 1 design-intent reconstruction. It excludes implementation, tests, Atlas/cohort records, current architecture, donor code and external project documents as semantic evidence.

## Authority and operating rules

`AGENTS.md` governs this execution. Tranche A is primary original design authority. Tranche B propositions require individual classification. Later documents supersede only the exact proposition they substantively amend, replace or retire. Unresolved conflicts remain unresolved. Administrative completion claims are not design authority.

All semantic propositions require exact source path and line-range lineage. Mechanical scripts may validate file identity, counts, IDs and citations but may not create or adjudicate semantic meaning.

## Baseline

- Archive SHA-256: `ac6af01badc5cd2dcc7ce770f7b50fd39d9c1bef026842d5fc545b5a6e103679`
- Initial repository branch: `main`
- Initial HEAD: `e908d3b072e4b1812e7fd2a1ce56563a1e4c6900`
- Initial worktree: clean
- Execution branch: `work/evolved-vision-reconstruction-v1`
- Admitted corpus: 61 Tranche A + 37 Tranche B = 98 Markdown files
- Mechanical manifest: `SOURCE_MANIFEST.tsv`
- Initial validation receipt: `reconstruction/evidence/INITIAL_BASELINE.txt`

## Actual execution topology

The available environment exposes one GPT-5.6 Thinking context and Git/container tools, but no separate subagent process or independently reset model context. Semantic extraction and review will therefore be separated by Git transaction and review artefact, with each review performed from untouched source files plus the proposed diff and prior accepted propositions. This is not equivalent to a genuinely independent fresh-model review and must remain a final assurance limitation unless an external independent reviewer later signs the work.

One accepted semantic commit will be created for each scheduled tranche on the execution branch. Failed review work will be repaired before the tranche is marked accepted.

## Proposition model

Stable proposition IDs use `P-<domain>-NNN`. Every proposition records:

- canonical English instruction and proposition class;
- introduction source and exact line range;
- all amendments, clarifications, replacements, retirements or reinstatements;
- authority state;
- historical aliases;
- inputs, validity constraints, transformations, outputs and guarantees;
- time/state semantics;
- null, boundary and failure behaviour;
- dependencies, downstream consequences, exclusions and unresolved questions.

## Chronological tranche schedule

Every admitted source appears exactly once below. Tranche A is completed before any Tranche B proposition is admitted.

### Tranche A — original planning authority

| Tranche | Source IDs |
|---|---|
| A01 | A001–A004 |
| A02 | A005–A008 |
| A03 | A009–A012 |
| A04 | A013–A016 |
| A05 | A017–A020 |
| A06 | A021–A024 |
| A07 | A025–A028 |
| A08 | A029–A032 |
| A09 | A033–A036 |
| A10 | A037–A040 |
| A11 | A041–A044 |
| A12 | A045–A048 |
| A13 | A049–A052 |
| A14 | A053–A056 |
| A15 | A057–A061 |

### Tranche B — successor proposition adjudication

| Tranche | Chronology | Source IDs |
|---|---|---|
| B01 | 2026-04-19 | B024, B027, B032 |
| B02 | 2026-04-20 | B020, B021, B023, B025, B026 |
| B03 | 2026-04-20 | B028, B029, B030, B031, B022 |
| B04 | 2026-04-22 | B001, B016, B033 |
| B05 | 2026-04-28 | B005, B003, B004 |
| B06 | 2026-04-28 | B002, B009, B008 |
| B07 | 2026-04-28 to 2026-05-01 | B006, B007, B010 |
| B08 | 2026-05-14 | B034, B035, B036, B037 |
| B09 | 2026-05-14 | B011, B012, B013 |
| B10 | 2026-05-14 | B014, B015, B017, B018, B019 |

Within equal-date successor groups, internal dependencies, stated baselines and recovered Git blob chronology are used. Any residual ambiguity is recorded, not invented away.

## Per-tranche acceptance unit

For each tranche:

1. read every source file in full with stable line numbers;
2. extract every material positive and negative instruction;
3. update the chronological proposition register and source reconciliation;
4. for Tranche B, classify each successor proposition under the exact allowed successor classes and resolve only scoped authority effects;
5. update affected canonical capability documents only after proposition adjudication;
6. perform a separate review pass against untouched sources, prior accepted propositions and the proposed diff;
7. record `PASS`, `FAIL_REPAIRABLE` or `HARD_BLOCK` in the tranche review artefact;
8. repair and re-review any failure before acceptance;
9. commit exactly one accepted transaction for the tranche.

## Required outputs

- `reconstruction/00_METHOD_STATUS_AND_SOURCE_MANIFEST.md`
- `reconstruction/01_CHRONOLOGICAL_AUTHORITY_AND_SUPERSESSION_INDEX.md`
- `reconstruction/02_CANONICAL_VISION_INDEX.md`
- `reconstruction/vision/*.md`
- `reconstruction/03_SOURCE_RECONCILIATION.md`
- `reconstruction/04_UNRESOLVED_CONFLICTS_AND_EXTERNAL_REFERENCES.md`
- `reconstruction/05_FINAL_ASSURANCE_REPORT.md`
- `reconstruction/tranches/<tranche>_REVIEW.md`
- optional mechanical validation artefacts under `reconstruction/evidence/`

## Validation commands

```bash
python tools/validate_source_corpus.py
python tools/validate_reconstruction.py
python -m compileall tools

git diff --exit-code -- source_planning source_successor_briefs SOURCE_MANIFEST.tsv
git status --short
```

`tools/validate_reconstruction.py` will mechanically check source coverage, tranche coverage, proposition ID uniqueness, citation path/line syntax and required output presence. It will not certify semantic completeness.

## Final acceptance criteria

- all 98 source hashes remain unchanged;
- all 98 files are assigned exactly once to the schedule and fully reconciled;
- every substantive instruction has an explicit proposition or disposition;
- every active proposition has exact source lineage;
- every supersession is scoped and cites both sides;
- formulas, thresholds, branches, transitions, failure rules, consumers and non-goals survive consolidation;
- successor repair documents contribute intended behaviour without importing implementation-completion claims;
- unresolved conflicts and external dependencies remain visible;
- capability organisation is independent of current module boundaries;
- every tranche has a recorded review verdict and accepted commit;
- final validation commands pass;
- worktree is clean;
- the assurance report distinguishes proven corpus reconstruction from the unavailable genuinely independent fresh-context review.

## Progress

- [x] Archive identity and extraction safety verified.
- [x] Branch, HEAD and initial clean worktree verified.
- [x] 61/37 source counts and all 98 manifest hashes validated.
- [x] Initial plan and evidence receipt prepared.
- [x] A01–A15 accepted.
- [x] B01 accepted.
- [x] B02 accepted.
- [ ] B03–B10 accepted.
- [ ] Final consolidation and assurance accepted.

## Next authorised action

Begin B03 successor adjudication against the accepted Tranche A and B01–B02 proposition set.
