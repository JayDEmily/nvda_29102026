# ExecPlan — Chronological–Semantic Chapter Reconstruction

## Objective

Transform the approved 98-document lossless design-intent reconstruction into a readable, sequential chapter set without changing the admitted source corpus, proposition meanings, authority states, chronology, supersession chains, qualifications, dependencies, exclusions or unresolved matters.

The chapter set is a navigational and narrative projection of the approved reconstruction. It is not a new source of design authority and must not replace the proposition register, exact source lineage or canonical capability specification.

## Authorisation and baseline

- User authorisation: on 2026-08-04 the user stated that the repaired reconstruction had been approved by the independent audit thread and authorised this chaptering task.
- Audit artefact: no new approval report was supplied in this thread; the approval status is therefore recorded as user-reported authority, not independently re-performed here.
- Base branch: `work/evolved-vision-reconstruction-v1`
- Base commit: `cebe05a2c1e9159a3239a0f5b7e09ad422c8f091`
- Execution branch: `work/chronological-semantic-chapters-v1`
- Admitted corpus: 61 original planning briefs plus 37 successor briefs, immutable.
- Approved semantic substrate: 83 canonical propositions, their complete field register, the chronological authority/supersession index, canonical vision documents, source reconciliation and unresolved register.

`AGENTS.md` continues to govern source authority and losslessness. This plan adds only the authorised chaptering method and outputs.

## Core method

### 1. Work at proposition level

Treat each approved canonical proposition as the minimum semantic unit. Do not assign whole briefing documents to a single topic merely because they share a filename, gate or date.

For each proposition retain:

- stable proposition ID;
- canonical instruction;
- exact source path and line lineage;
- authority state;
- chronology and supersession links;
- inputs, transformations, outputs and guarantees;
- time/state semantics;
- dependencies and downstream consequences;
- qualifications, exclusions, failure behaviour and unresolved questions.

### 2. Produce candidate semantic clusters

Create candidate idea families by comparing proposition meaning, owned decision or transformation, data dependencies, temporal position and downstream consumers.

OpenAI embeddings may be used only as a non-authoritative discovery aid where an authorised API credential is available. They may suggest proximity or hidden groupings, but they may not assign a proposition, resolve authority, merge distinct semantics or certify a chapter. No OpenAI API credential is available in this execution environment, so the controlling execution path is direct human-semantic adjudication by the active model context, supported only by mechanical inventory and coverage checks.

### 3. Semantically adjudicate every assignment

For every proposition, decide and record:

- exactly one primary chapter;
- zero or more secondary cross-references;
- its role in the chapter's development: `introduction`, `refinement`, `constraint`, `challenge`, `replacement`, `reinstatement`, `current_form`, `unresolved`, or `supporting_context`;
- why it belongs there and why superficially related propositions remain separate where necessary.

Similarity is not authority. Formulae, thresholds, branches, specimen values, failure modes, negative constraints and conditional reservations must remain distinct even when they concern the same broad topic.

### 4. Preserve chronology inside each idea family

Within each chapter, present the lawful development sequence:

1. original intention;
2. subsequent refinement;
3. introduced constraints or challenges;
4. amendment, replacement, retirement or reinstatement;
5. current authoritative form;
6. unresolved questions or external dependencies.

A chapter must expose conflicting or conditional branches rather than harmonising them for narrative smoothness.

### 5. Order chapters by conceptual dependency

Chapter order follows the system's semantic dependency and operating flow rather than source-file order alone. The provisional dependency spine is:

1. operating objective and advisory boundaries;
2. information identity and raw inputs;
3. temporal and session interpretation;
4. derived features and contextual signals;
5. cognition and serial decision workflow;
6. playbooks, posture and modifier logic;
7. DMPV3 and governed information carriage;
8. parallel risk, final risk and capital;
9. execution, lifecycle, state and persistence;
10. review, trace, replay and governance.

These are candidate chapter families. Final titles and boundaries must be justified by the approved propositions, and may be split or merged only where semantic reading supports it.

### 6. Write chapters as developmental narratives

Each chapter must use this internal form:

> Original intention → development → constraints and conflicts → authority resolution → current authoritative position → unresolved matters

The prose must remain technically exact. It may improve navigation and continuity, but it must not semantically compress a proposition into a generic capability statement.

### 7. Retain cross-links without duplicating authority

Each proposition has one primary chapter. Secondary chapters link back to the primary treatment rather than restating or subtly altering it. Every substantive chapter section cites proposition IDs; proposition IDs retain the exact source lineage.

### 8. Validate coverage and fidelity

Validation must establish mechanically that:

- all 83 proposition IDs are assigned exactly once as primary;
- no unknown proposition ID appears;
- all chapter files named in the index exist;
- all primary and cross-reference mappings resolve;
- every unresolved proposition or reservation is visible in a chapter;
- source files and the approved reconstruction substrate remain unchanged unless a chaptering defect requires an explicitly authorised correction;
- the chapter set never claims that mechanical validation certifies semantic fidelity.

Semantic validation is a proposition-by-proposition human review of the mapping and chapter prose against the approved canonical proposition text and, where needed, the cited immutable source lines.

## Required outputs

Create all new work under `chapter_reconstruction/`, except this living `Exec_plan.md` and the validator under `tools/`.

1. `chapter_reconstruction/00_METHOD_AND_BASELINE.md`
   - scope, authority, actual execution method, embedding availability, baseline and limitations.
2. `chapter_reconstruction/01_CHAPTER_INDEX.md`
   - final chapter order, purpose, dependency relationship and navigation.
3. `chapter_reconstruction/02_PROPOSITION_TO_CHAPTER_MAP.md`
   - authoritative semantic mapping for all 83 propositions, with primary chapter, cross-references, developmental role and rationale.
4. `chapter_reconstruction/02_PROPOSITION_TO_CHAPTER_MAP.tsv`
   - mechanically checkable projection of the Markdown mapping; not semantic authority.
5. `chapter_reconstruction/chapters/*.md`
   - complete chronological–semantic narrative chapters.
6. `chapter_reconstruction/03_CROSS_REFERENCE_AND_COVERAGE.md`
   - chapter-to-chapter cross-links, proposition coverage and unresolved-item visibility.
7. `chapter_reconstruction/04_CHAPTER_ASSURANCE_REPORT.md`
   - exact scope established, validation results, limitations and remaining Unknowns.
8. `chapter_reconstruction/evidence/*.txt`
   - baseline and final command outputs.
9. `tools/validate_chapter_reconstruction.py`
   - mechanical coverage and reference validator only.

## Semantic acceptance units and commit plan

1. **C0 — Plan and baseline:** commit this ExecPlan and exact baseline validation receipt.
2. **C1 — Cluster adjudication:** complete all 83 primary assignments, cross-references, roles and rationales; commit the map and chapter index.
3. **C2–C11 — Chapters 1–10:** write and semantically review one chapter at a time; commit each accepted chapter separately.
4. **C12 — Cross-reference and assurance closeout:** add coverage report, validator, exact validation output, final assurance report and updated ExecPlan; commit and package.

No chapter may be declared accepted merely because its IDs appear in the mapping or the validator passes.

## Validation commands

```bash
python tools/validate_source_corpus.py
python tools/validate_reconstruction.py
python tools/validate_chapter_reconstruction.py
python -m py_compile tools/validate_chapter_reconstruction.py

git diff --exit-code cebe05a2c1e9159a3239a0f5b7e09ad422c8f091 -- \
  source_planning source_successor_briefs SOURCE_MANIFEST.tsv \
  reconstruction/propositions reconstruction/vision \
  reconstruction/01_CHRONOLOGICAL_AUTHORITY_AND_SUPERSESSION_INDEX.md \
  reconstruction/03_SOURCE_RECONCILIATION.md \
  reconstruction/04_UNRESOLVED_CONFLICTS_AND_EXTERNAL_REFERENCES.md \
  reconstruction/06_CANONICAL_PROPOSITION_FIELD_REGISTER.md

git status --short
```


## Final acceptance criteria

- the 98 admitted source files remain byte-identical;
- the approved 83-proposition substrate remains unchanged;
- every proposition has exactly one primary chapter assignment;
- chapter order follows semantic dependency while each chapter preserves internal chronology;
- all authority changes, conditions, specimen values, formulas, thresholds, failures, exclusions and unresolved matters survive chaptering;
- cross-references do not create duplicate or competing canonical wording;
- chapter prose is traceable through proposition IDs to exact source lines;
- mechanical validation passes and is explicitly bounded to structure;
- Git history shows the plan, mapping, each chapter and closeout as separate acceptance transactions;
- final worktree is clean and the full-history archive is reproducible.

## Progress

- [x] Verified base branch, base HEAD and clean worktree.
- [x] Verified 61/37 source counts and all 98 source identities.
- [x] Re-ran reconstruction mechanical validation at the approved base.
- [x] Created execution branch.
- [x] C0 plan and baseline committed.
- [x] C1 all 83 propositions clustered and mapped.
- [x] C2 chapter 1 accepted.
- [ ] C3 chapter 2 accepted.
- [ ] C4 chapter 3 accepted.
- [ ] C5 chapter 4 accepted.
- [ ] C6 chapter 5 accepted.
- [ ] C7 chapter 6 accepted.
- [ ] C8 chapter 7 accepted.
- [ ] C9 chapter 8 accepted.
- [ ] C10 chapter 9 accepted.
- [ ] C11 chapter 10 accepted.
- [ ] C12 cross-reference, validation, assurance and packaging complete.

## Discoveries and decisions

- 2026-08-04: the environment has no `OPENAI_API_KEY`, `OPENAI_BASE_URL` or Azure OpenAI credential. Embedding-based candidate generation cannot be executed and will not be simulated or claimed. Human-semantic cluster adjudication remains the controlling method.
- 2026-08-04: the existing ten canonical vision domains are candidate evidence for chapter boundaries, not an automatic chapter assignment. The chapter map must still adjudicate every proposition individually.

## Next authorised action

Draft and semantically review Chapter 2 against its eleven primary propositions, preserving the frozen raw-path specimen and unresolved regime-completeness ownership.
