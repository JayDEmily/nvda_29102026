# NVIDIA 2026 — MVP Gate C Completion Protocol

## Status

**Status:** `MVP_FAST_TRACK_ACTIVE_M04_GATE_C_COMPLETE`
**Amendment date:** `2026-07-31`
**Owner:** User and Project Manager thread
**Parent plan:** `project_control/canonical_project_manager/EXEC_PLAN.md`
**Live pointer:** `ROADMAP_LEDGER_V2.md`
**Scope:** alpha normative closure and truthful proof admission before module-local Gate D

This file is the sole current Gate C operating protocol. The former eight-leaf
`MLC-A → MLC-R → MLC-O → MLC-D → MLC-P → MLC-T → MLC-V → MLC-I`
sequence is retained in Git history and completed module records as historical
evidence. It is no longer the mandatory execution route.

Gate C does not contain production implementation. A module that passes this
protocol opens its bounded Gate D implementation immediately; it does not wait
for programme-wide Gate C completion.

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
5. run the complete legacy suite as shadow evidence when available;
6. classify new shadow failures without automatically obeying unadmitted tests;
7. update the existing module record and validation log;
8. create one checkpoint for the completed module slice.

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
- the existing validation log;
- Git checkpoint evidence.

Not required by default:

- a new project tracker;
- one receipt per test or Atlas record;
- one commit per review activity;
- one worker archive plus one tester archive per ordinary module;
- independent control testing for a non-risk control wording update;
- programme-wide vocabulary or legacy-test reconciliation on each term.

## 9. Current conversion

| Module | Converted Gate C state | Next action |
|---|---|---|
| M13 state kernel | accepted implementation checkpoint retained | no repeat Gate C |
| M04 packet protocol / K07 | `C-NORM PASS`; `C-PROOF PASS` from the existing 239-case reference/matrix/mutant evidence and 11 exact production-red cases | Gate D implementation open |
| M01 source admission | `C-NORM PASS`; prior 179-file routing retained as navigation only | write minimum `C-PROOF`, then Gate D |
| M07 coefficient/modifier authority | `C-NORM BLOCKED` on K12 identity/version, precedence, bounds and application receipt | amend K12, then minimum proof |
| M08 playbook catalogue | `C-NORM BLOCKED` on K13 catalogue and eligibility decision semantics | amend K13, then minimum proof |

The former requirement for a separate M04 MLC-V worker is superseded. M04 has
already exceeded the ordinary deterministic-contract proof threshold: its
reference/matrix/outcome checks pass, all ten declared false-positive mutants
are detected, and production remains red at the eleven claimed gaps.

## 10. Delivery order

The immediate delivery sequence is:

1. implement the already-open M04 K07 Gate D slice;
2. complete M01 minimum proof and implementation;
3. complete M07 and M08 normative/proof slices;
4. continue through the dependency graph:
   `M01 → M02 → M03`, then `M05/M06`, `M09`, `M10`, `M11`, `M12`, and
   final `M00` composition;
5. operate M14 proof promotion and M15 vocabulary governance continuously.

Dependency readiness may change this order. Numeric module or `D-xxx` order is
never authority.

## 11. Final alpha consolidation

Final consolidation is a milestone check, not a retroactive re-adjudication
programme. It must:

- reconcile accepted/rejected/deferred Atlas behaviour;
- retain every `D-xxx` lineage outcome;
- run admitted targeted/affected proof and the full shadow suite;
- verify module dependency direction, vocabulary projection, transaction
  boundaries and replay limitations;
- record remaining unknowns and explicit alpha exclusions.

It must not require new per-test receipts unless a real contradiction is found.
Production, paper, live and operational-readiness decisions remain separate.

## 12. Change control

This protocol may change only by direct user strategy instruction or measured
evidence that the route is unsafe or again disproportionate. The same change
must update the ExecPlan, live roadmap and current process overlay. Accepted
evidence remains in module records and Git history.
