# Evolved Vision Reconstruction

## Mission

Reconstruct, from the 98 immutable planning documents in the two source tranches, a clean, lossless and chronologically resolved specification of what the user intended the NVDA desk system to do and how that vision lawfully evolved.

This is **Phase 1 only: design-intent reconstruction**. Do not inspect the messy implementation, the Atlas, cohorts, current modular architecture, production code, tests, receipts outside this corpus, or project documents outside the two admitted source tranches. Do not design modules, write code, repair code, or judge the current architecture.

The final result must be a self-contained English specification from which a competent engineer could later validate an architecture, derive normative obligations and tests, and implement the intended system without needing to rediscover the user’s ideas from these historical briefs.

## Source boundary

- The sole evidence corpus is:
  - **Tranche A — original planning authority:** 61 Markdown gate contracts under `source_planning/`.
  - **Tranche B — recovered successor briefs:** 37 Markdown implementation, repair, migration and continuation briefs under `source_successor_briefs/`.
- Treat all 98 files as immutable evidence. Never edit, rename or reformat them.
- Verify at the start that exactly 61 Tranche A files and exactly 37 Tranche B files exist; record SHA-256 hashes for all 98.
- Do not import claims from memory, prior conversations, the internet, the donor codebase, Atlas records, Gate 3/4 tables, or implementation receipts outside these admitted documents.
- Historical references inside a source document may be recorded as unresolved external references, but they are not independently verified in this phase.

The original archive also contained eight administrative or assurance-only gate documents that were intentionally excluded from Tranche A: Gates 46, 56, 106, 112, 113, 131, 134 and 149. Do not recreate content from them or infer design requirements from their absence.

## Two-tranche authority law

Tranche A and Tranche B do not have equal automatic authority.

1. Tranche A is the primary record of the original design vision.
2. Tranche B is a candidate successor corpus. Every successor brief must be classified before any proposition from it changes the canonical vision.
3. Classify each successor proposition as exactly one of:
   - `new_design_authority`
   - `clarification`
   - `bounded_amendment`
   - `bounded_repair`
   - `explicit_replacement`
   - `explicit_retirement`
   - `implementation_specific_instruction`
   - `historical_implementation_claim`
   - `process_only`
   - `derived_from_superseded_premise`
   - `unresolved`
4. A successor brief may reveal intended behaviour when it identifies a defect, omission or incorrect implementation. Extract that intended behaviour, but do not inherit the claim that the repair was completed.
5. A successor brief does not become general architecture authority merely because it is later, more detailed, marked authoritative, or associated with green tests.
6. A later brief supersedes only the exact proposition it expressly and substantively changes. Every unaffected earlier proposition survives.
7. If a successor brief depends on an external normative document not included in this corpus, record the dependency. Do not silently import the external document's content.
8. The 37 successor documents must be reconciled both against earlier accepted propositions and against one another. Later successor documents may themselves be partially superseded.
9. Documents without a reliable date in their filename must be ordered using internal dates, stated baselines and recovered Git chronology. Any residual chronology ambiguity remains explicit.

## Operating topology

Use native Codex project instructions, subagents and isolated Git worktrees where available.

- **Programme Manager:** GPT-5.6 High. Owns chronology, authority adjudication, the global proposition graph, integration and final acceptance.
- **Semantic workers:** fresh GPT-5.6 Medium context for each bounded chronological tranche, normally three to five closely related documents.
- **Independent reviewers:** fresh GPT-5.6 High context. Review the tranche against the untouched source documents without receiving the worker’s reasoning narrative.
- Do not run multiple semantic writers concurrently. Read-only mechanical inventory may run in parallel.
- Use one branch/worktree and one accepted commit per tranche. A failed tranche is repaired in a fresh context, not defended indefinitely in the original worker context.
- If explicit model-effort controls are unavailable, preserve the role and context separation and record the actual settings used.

The Programme Manager must not outsource final authority resolution. Workers extract and propose; reviewers challenge; the Programme Manager integrates only evidence-supported results.

## Required first action

Before semantic extraction:

1. verify branch, HEAD and clean worktree;
2. verify the 61-file Tranche A count, 37-file Tranche B count and all 98 hashes;
   - run `python tools/validate_source_corpus.py` and preserve its exact output;
3. create `PLANS.md` as a living ExecPlan for this entire reconstruction;
4. create a chronological tranche schedule covering every one of the 98 source documents exactly once, with Tranche A reconstructed before successor propositions are admitted;
5. define validation commands and final acceptance criteria in that ExecPlan;
6. commit the plan and mechanical source manifest before opening the first semantic tranche.

The ExecPlan must remain self-contained and current throughout the work. Record discoveries, decisions, completed tranches, failed reviews, repairs and the next authorised action. Do not use the plan as semantic authority; source documents remain the evidence.

## Authority and supersession law

Chronology is necessary but not sufficient. **A later date does not automatically override an earlier instruction.** Apply these rules proposition by proposition:

1. **Introduction:** the earliest document that clearly states a behaviour, capability, calculation, boundary or design decision introduces it.
2. **Survival:** an introduced instruction remains active unless a later document explicitly amends, replaces, retires or contradicts that specific instruction.
3. **Scoped repair authority:** a repair, corrective or successor document has authority over the exact defect or behaviour it expressly repairs. It does not erase unrelated earlier ideas.
4. **Partial supersession:** where only part of an earlier instruction changes, preserve the unaffected part and identify the exact amended scope.
5. **Clarification:** a later document that explains an earlier instruction without changing its observable meaning is a clarification, not a replacement.
6. **Replacement:** mark an earlier proposition superseded only when the later source establishes incompatible replacement behaviour or explicitly retires it.
7. **Reinstatement:** if a later source restores an earlier rule after an intervening change, preserve the full chain and mark the currently active proposition.
8. **Repair evidence:** when a document says code was wrong, incomplete or repaired, extract the intended behaviour revealed by the repair. Treat statements that work was completed or tests were green only as historical implementation claims, not as proof of design correctness.
9. **Administrative language:** branch names, status labels, packaging, merge instructions, gate progression and test receipts are process history unless they explicitly alter intended system behaviour.
10. **Non-goals and prohibitions:** preserve them. Negative boundaries are part of the design and must not disappear during consolidation.
11. **Conflict:** when two sources conflict and neither explicitly or structurally resolves the other, do not guess. Preserve both, record the conflict and classify the canonical result as unresolved.
12. **Vocabulary evolution:** preserve renamed terms as historical aliases and separate a terminology change from a behavioural change.

Every supersession claim must cite both the superseded and superseding source with exact line ranges and explain why the change is substantive.

## Semantic extraction rule

Read each source document as a human design record, not as a bag of keywords. Extract every material instruction concerning:

- user purpose and operating objective;
- data and external inputs;
- derived information, formulae, thresholds and classifications;
- sequence, routing and cognitive workflow;
- state, time, sessions, horizons, persistence and replay;
- decisions, permissions, gates and overrides;
- playbooks, variants, expressions and selection logic;
- risk, posture, capital and terminal constraints;
- execution, lifecycle, position continuity and exits;
- review, attribution, explanation and evidence;
- interfaces, ownership boundaries and prohibited coupling;
- null, missing, stale, invalid and degraded behaviour;
- deterministic requirements and explicit non-goals;
- configurable policy, governed vocabulary and change authority.

Do not compress a formula, threshold, branch, exception, state transition, timing rule, consumer consequence or negative constraint into a generic capability label. Preserve the observable semantics.

Do not preserve arbitrary document, gate, file, function or legacy-module boundaries in the final specification. Consolidate by intended capability only after the chronological authority chain has been resolved.

## Canonical proposition model

Represent each material instruction with a stable proposition ID and at least:

- canonical English instruction;
- proposition class;
- first introducing source and exact lines;
- every amendment, clarification, replacement, retirement or reinstatement and exact lines;
- current authority state: `active`, `partially_superseded`, `superseded`, `retired`, `unresolved` or `process_only`;
- preserved historical aliases;
- inputs and validity constraints;
- transformation, calculation, decision or routing semantics;
- outputs and guarantees;
- time and state semantics;
- null, boundary and failure behaviour;
- dependencies and downstream consequences;
- explicit exclusions and non-goals;
- unresolved questions.

The canonical English proposition is authoritative only after independent review. Source excerpts and line citations are evidence; worker summaries are not evidence.

## Required outputs

Create all work under `reconstruction/` except `PLANS.md`.

At minimum produce:

1. `reconstruction/00_METHOD_STATUS_AND_SOURCE_MANIFEST.md`
   - method, source hashes, tranche status, worker/reviewer identities or thread references, actual reasoning settings and validation results.

2. `reconstruction/01_CHRONOLOGICAL_AUTHORITY_AND_SUPERSESSION_INDEX.md`
   - every substantive proposition in chronological order;
   - explicit introduction, amendment, clarification, replacement, retirement, reinstatement and unresolved-conflict chains.

3. `reconstruction/02_CANONICAL_VISION_INDEX.md`
   - navigational index to the final active design specification.

4. `reconstruction/vision/*.md`
   - the clean, current, human-readable design instructions grouped by coherent capability domains discovered from the corpus;
   - do not force them into the current M00-M15 architecture during this phase.

5. `reconstruction/03_SOURCE_RECONCILIATION.md`
   - all 98 source files, each reconciled completely to proposition IDs or explicit `duplicate`, `process_only`, `historical_implementation_claim`, `superseded`, or `unresolved` dispositions;
   - no silent omissions.

6. `reconstruction/04_UNRESOLVED_CONFLICTS_AND_EXTERNAL_REFERENCES.md`
   - every conflict, missing external authority, ambiguous formula, incomplete threshold, absent source or decision that the corpus cannot resolve.

7. `reconstruction/05_FINAL_ASSURANCE_REPORT.md`
   - independent review results, coverage counts, known limitations and a precise statement of what is and is not established.

A generated CSV or JSON index may be added for navigation and mechanical checks, but Markdown is the semantic authority. Generated indexes must not restate or silently alter the canonical instructions.

## Losslessness and completeness controls

The reconstruction is complete only when:

- all 98 source files are hash-verified and unchanged, with the 61/37 tranche split preserved;
- every source file has been semantically read in chronological context, including successor-to-original and successor-to-successor effects;
- every substantive source instruction has an explicit disposition;
- every active proposition retains exact source lineage;
- every supersession is scoped and evidenced, not inferred from date alone;
- every repair document has been checked for the intended behaviour it reveals;
- all formulas, thresholds, branches, timing rules, state transitions, failure rules, consumers and non-goals survive consolidation;
- duplicates are merged without losing distinct semantics or provenance;
- unresolved conflicts remain visible rather than being harmonised by invention;
- the canonical vision contains no claims derived from current code, Atlas, cohorts or later architecture;
- each tranche passes independent high-reasoning review;
- the final reviewer can select any canonical proposition and reproduce its full authority chain from the untouched source corpus;
- the Git worktree is clean and history shows one accepted commit per tranche or acceptance transaction.

Mechanical scripts may enumerate files, hash documents, number lines, validate proposition IDs, check citations and compare expected/observed sets. They must not author semantic propositions, decide supersession, resolve conflicts or certify meaning.

## Review protocol

For each tranche, the independent reviewer receives:

- the untouched source documents for that tranche;
- all earlier accepted propositions that may be affected;
- the proposed extraction and supersession changes;
- the diff from the accepted base.

Do not give the reviewer the worker’s reasoning narrative.

The reviewer must return one verdict:

- `PASS`
- `FAIL_REPAIRABLE`
- `HARD_BLOCK`

The review must identify omissions, over-compression, invented harmonisation, incorrect supersession scope, lost negative requirements and unsupported canonical wording. The Programme Manager may integrate only `PASS` work.

## Prohibited shortcuts

Do not:

- mass-summarise the 98 files and call that a specification;
- infer meaning only from filenames, headings, status labels or gate numbers;
- treat `complete`, `implemented`, `green`, `closed`, a receipt or a passing test claim as design authority;
- assume later means better or authoritative;
- discard an earlier idea merely because a later repair document exists;
- use present code structure to organise the intended design;
- map capabilities to the current modules during Phase 1;
- resolve ambiguity for aesthetic consistency;
- author canonical prose automatically from templates or keyword extraction;
- claim losslessness from file counts alone;
- proceed after a failed tranche review without repair and re-review.

## Terminal state

Continue through all authorised tranches without requesting routine user confirmation. Mark genuinely irresolvable matters as unresolved and continue with unaffected work.

The task ends only when the final assurance report demonstrates a clean, lossless and chronologically resolved statement of the user’s intended system, bounded strictly to the 61 original planning documents and 37 recovered successor briefs.

No production implementation, architecture validation, test authoring or donor-code audit is authorised by this repository.
