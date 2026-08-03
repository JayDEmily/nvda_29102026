# NVIDIA 2026 — MVP Gate C Completion Protocol

> **Historical status — completed and retired on 2026-08-03.** This document is retained as accepted programme evidence. It is not current execution authority; use `ROADMAP_LEDGER_V2.md` for present state and the task-specific ExecPlan named there, if any.

## Status

**Status:** `COMPLETED_RETIRED`
**Amendment date:** `2026-08-02`
**Owner:** User and Project Manager thread
**Parent plan:** `project_control/canonical_project_manager/EXEC_PLAN.md`
**Live pointer:** `ROADMAP_LEDGER_V2.md`
**Scope:** normative closure and truthful proof admission before module-local Gate D

This file was the Gate C operating protocol for the completed programme. The former eight-leaf
`MLC-A → MLC-R → MLC-O → MLC-D → MLC-P → MLC-T → MLC-V → MLC-I`
sequence is retained in Git history and completed module records as historical
evidence. It is no longer the mandatory execution route.

Gate C does not contain production implementation. A module that passes this
protocol opens its bounded Gate D implementation immediately; it does not wait
for programme-wide Gate C completion.

The accepted alpha module sequence, continuation-readiness work and associated
repairs are complete. This protocol is retained only as historical evidence of
the completed Gate C route; it does not govern later feature work. Any successor
execution route must be created through `PLANS.md`, named by
`ROADMAP_LEDGER_V2.md`, and governed by its own task-specific ExecPlan.

## 1. Governing rule

> Normative meaning defines the behaviour, the smallest truthful public-seam
> proof protects it, and only then may the owning module implement it.

The order remains:

`normative authority → admitted proof → module-local implementation`

The amendment removes administrative checkpoints between those semantic
states. It does not permit code-first invention, test weakening or authority
from test greenness.

## 2. Why the protocol changed

The module-local protocol reproduced the global-gate problem it was intended
to solve.

From the accepted Atlas-path repair checkpoint `27fa427` to the M04 MLC-T
checkpoint `2aab666`:

- seven commits and 34 files changed;
- 3,442 lines were added and 262 deleted;
- M04 production behaviour did not change;
- the test-authoring leaf alone added 946 lines across eleven files;
- the current M04 implementation gap is concentrated in explicit
  execution-context, lineage and role-validation rules in two packet surfaces.

This is disproportionate for a `thin_seam` alpha. The numbered doctrine
requires the smallest proof combination that establishes the accepted claim
and warns against excessive modularity. The eight leaves were a project-control
choice, not a top-level normative requirement.

A second measured correction was directed on 2026-07-31 after the accepted M07,
M08 and M02 slices retained 44,256, 44,897 and 42,555 lines of validation
material respectively. In each case the decisive result already fit in a short
summary containing the command outcome, counts and failing-node delta. The
largest duplicated artefacts were baseline/current full-suite transcripts or
JUnit XML. Those files did not add a new semantic or behavioural claim.

The current route therefore separates validation execution from evidence
retention: required checks still run, while duplicate successful raw output is
not committed by default.

## 3. Non-negotiable constraints

1. Normative documents remain above tests and code.
2. Each behaviour has one accepted Ownership Module and one public seam.
3. Missing mandatory meaning is amended in the existing routed normative
   document before authoritative tests or code.
4. Atlas remains candidate behavioural evidence until the owning module admits,
   rejects or defers the relevant cohort behaviour.
5. Tests must exercise the public seam and fail or pass for the claimed reason.
6. No test, fixture or vocabulary rule may be weakened to fit current code.
7. Unrelated legacy tests remain runnable shadow evidence, not automatic
   authority.
8. Production implementation belongs to Gate D and opens only after the active
   module passes both Gate C steps.
9. Current alpha boundaries remain explicit: no live execution, production
   durability, operational readiness or profitability claim is created here.

## 4. The two Gate C steps

### `C-NORM` — normative closure

One bounded module change must establish:

- the behaviour and prohibited authority;
- owner, public seam, inputs and outputs;
- mandatory identity, lineage, time and state semantics where material;
- the relevant Atlas cohort/record routes and `D-xxx` lineage;
- whether each relevant candidate behaviour is admitted, rejected or deferred;
- any durable vocabulary admission through the existing namespace mechanism.

The worker may inspect existing tests and code to find gaps, but it does not
have to produce a file-by-file observation or disposition census.

Pass result:

`C_NORM_PASS:<module>:<behaviour>`

Fail result:

`C_NORM_BLOCKED:<exact missing or contradictory proposition>`

### `C-PROOF` — minimum truthful proof

Write or identify the smallest test family that establishes the accepted
behaviour. As applicable, it must cover:

- one conforming public-seam case;
- the material missing/forbidden input or action;
- one plausible false-positive implementation;
- state isolation, ordering, replay or substitution only when the behaviour
  actually owns those concerns.

Expected red is a passing Gate C result when it truthfully demonstrates absent
implementation. Existing green proof may be admitted when it matches the
normative proposition and public seam exactly.

The validation record must state:

- the proposition locator;
- the public seam;
- what the proof establishes and does not establish;
- targeted command and result;
- expected-red or existing-green reason;
- the false-positive challenge used, if material.

Pass result:

`C_PROOF_PASS_GATE_D_OPEN:<module>:<behaviour>`

Fail result:

`C_PROOF_BLOCKED:<exact proof defect or normative return>`

No separate routing, observation, disposition, proof-specification,
test-authoring or validation checkpoint is required.

## 5. Risk-triggered independent validation

Independent validation remains mandatory before Gate D only when the change
owns one or more of:

- atomic state transition, rollback, idempotency or transaction participation;
- fresh-capital sizing or deployment authority;
- broker submission, execution acknowledgement or fill reconciliation;
- live position, inventory, exit or close mutation;
- durable storage migration, recovery or promotion authority;
- another boundary that the Project Manager records as equivalently
  irreversible or high-consequence.

For ordinary deterministic contracts, classifiers, packet validation,
preparation transforms, catalogue lookup and read-only review surfaces,
reproducible proof plus a recorded Project Manager check is sufficient. A
separate worker/tester pair, branch, archive and commit are optional tools, not
mandatory gates.

## 6. Gate D implementation

After `C_PROOF_PASS_GATE_D_OPEN`:

1. implement the smallest semantically complete owner-local change;
2. run the targeted admitted proof;
3. run affected admitted proof;
4. run architecture/dependency and vocabulary checks where affected;
5. run the current admitted aggregate route and relevant legacy shadow suite
   once when available;
6. compare current failing-node identity with the latest accepted comparable
   checkpoint; do not rerun an unchanged baseline solely to create another raw
   transcript;
7. classify new shadow failures without automatically obeying unadmitted tests;
8. update the existing module record, validation log and live roadmap with one
   concise reproducible validation summary; and
9. create one checkpoint for the completed module slice.

The concise summary must retain the proposition and public seam, exact command
or stable command locator, declared environment/interpreter, exit status,
collected/pass/fail/skip counts, failing-node set and delta, material warnings or
unavailable checks, and pre/post Git state.

Full successful stdout/stderr, duplicate baseline/current transcripts, JUnit XML,
whole-tree hash listings and repeated copies of unchanged command output are not
tracked by default. Keep raw output outside the tracked tree and discard it after
the summary is checked, unless it contains a novel regression, non-deterministic
result, material environment failure, or evidence expressly required for a
high-consequence independent review. A baseline must be rerun when its admitted
set, environment, command route or comparability is stale, changed or Unknown.

There is no checkpoint between every internal coding action. A checkpoint is
required at a completed semantic slice, before a conflicting module or shared
surface opens.

## 7. Atlas and historical-test treatment

- The accepted 287-cohort/1,716-record workbook governs traceability and target
  allocation, not automatic behavioural admission.
- Only cohorts relevant to the active module behaviour require current
  adjudication.
- Cohorts may be admitted, split, merged, rejected or deferred with lineage
  retained.
- No dossier is required for every Atlas record.
- The 179-file PM-011 census remains navigation evidence. It is not a
  prerequisite to module implementation.
- Historical `MLC-*`, `D-xxx`, worker/tester and proof-envelope records remain
  challenge evidence. They do not create new mandatory leaves.

## 8. Evidence economy

Required current records:

- this protocol;
- the parent ExecPlan;
- the live roadmap;
- the accepted architecture report and Atlas trace;
- one existing module record updated per active behaviour;
- one current-target full-read manifest per semantic unit;
- one concise validation summary with reproducible commands and material deltas;
- the existing validation log;
- Git checkpoint evidence.

Not required by default:

- a new project tracker;
- one receipt per test or Atlas record;
- one commit per review activity;
- one worker archive plus one tester archive per ordinary module;
- independent control testing for a non-risk control wording update;
- programme-wide vocabulary or legacy-test reconciliation on each term;
- committed full successful test transcripts or JUnit XML;
- duplicate baseline and current suite output when node-level comparison is
  reproducible from the accepted checkpoint;
- exhaustive hash lists for unchanged files already protected by Git.

Evidence must remain sufficient to reproduce and falsify the claim. Economy is
not permission to omit a failing node, unavailable check, changed environment or
material diagnostic.

## 9. Current conversion

| Surface | Current state | Treatment |
|---|---|---|
| Accepted M01–M13 behaviours | historical Gate D evidence retained | do not repeat Gate C without a current failing or contradictory proposition |
| M00 final composition and later post-alpha slices | accepted within recorded alpha bounds | preserve and use their current public seams |
| Continuation foundation readiness | strategy defined; execution not started | use this protocol for each behaviour-changing reconciliation unit |
| Future planned concepts | closed until the readiness checkpoint | reopen one concept at a time after the checkpoint |
| M14 and M15 | continuing governance planes | maintain exact proof admission and vocabulary projection continuously |

Accepted historical proof and implementation evidence remains valid. The
comparative audit corrects current repository readiness; it does not downgrade
every module or require deletion and rewriting of retained evidence.

## 10. Continuation delivery order

The immediate sequence is governed in full by `CONTINUATION.md`:

1. prove exact canonical-model admission and cluster the current failing nodes
   by authority/common cause;
2. close the prepared-context/M04 identity boundary;
3. close typed M01 ingress with current M00/transport callers;
4. close confirmed dependency, state-policy, vocabulary-scanner and canonical
   API identity/state findings as narrow units;
5. adjudicate only residual failure families; and
6. publish one current readiness checkpoint.

Each behaviour-changing unit uses `C-NORM → C-PROOF → Gate D`. Dependency
readiness may reorder disjoint narrow units only when the live plan records the
reason and shared integration remains serial. Numeric module, test or `D-xxx`
order is never authority.

## 11. Continuation-readiness and later integration

The readiness checkpoint is a milestone check, not a retroactive module
programme. It must establish on one commit:

- a green retained physical Tier A/Tier B universe with zero unadmitted or
  stale physical proof paths;
- a green current curated promotion route;
- lawful module dependency direction in addition to cycle/unresolved-import
  health;
- current import-order, state, replay, boundary and vocabulary assurance;
- closure or proved canonical quarantine of the named structural findings; and
- agreement among the ExecPlan, roadmap, module records, proof control,
  validation summary and Git state.

It must reuse comparable accepted evidence, work by failure family and avoid
new per-test receipts unless a real contradiction requires one. After this
single checkpoint, every feature follows the same protocol as one bounded
concept; no new repository-wide retrospective is required by default.

Production, paper, live, profitability and operational-readiness decisions
remain separate.

## 12. Change control

This protocol may change only by direct user strategy instruction or measured
evidence that the route is unsafe or again disproportionate. The same change
must update the ExecPlan, live roadmap and current process overlay. Accepted
evidence remains in module records and Git history.
