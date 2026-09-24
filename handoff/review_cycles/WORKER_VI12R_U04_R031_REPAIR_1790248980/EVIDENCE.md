# Worker cycle evidence

**Status:** `COMPLETE`

## Source and authority binding

- received archive: `NVDA_G03_TESTER_VI13R_U04_R031_FAIL_WORKER_REPAIR_HANDOFF_FULL_GIT_20260924.tar(1).gz`;
- received archive SHA-256: `024069d902fdd8cbb9722a47b759bac756f1ad71735c95494a01ddcf64aa7e90`;
- routed Reviewer-031 handoff HEAD: `a3564f4908283f9bacf72f3720d020503f124e55`;
- Reviewer-031 disposition commit: `6c33e51ab436b8f19dd1799ddf60cc0b3d87ebaa`;
- rejected U04 candidate: `e7eb44119bdf7fb22abacae8291788619792c96a` / tree
  `ea104900fcaf8e2db4177df3909956f464d6a918`;
- open finding repaired by this cycle: `R031-U04-F001`;
- recurrence classification entering repair: `ISOLATED`;
- accepted/promoted U03 forward main remains `63bbeee9cec14f38ed6da6260095ccf0d8e8e6ec`;
- U05 and later remained prohibited throughout this Worker cycle.

The Worker read root `README.md`, `GUARDRAILS.md`, root `AGENTS.md`, applicable
`tests/AGENTS.override.md`, complete current `EXEC_PLAN.md`, `CURRENT_STATE.md`, the active repair
request, Reviewer-031 response/evidence/result, accepted IRB BC-007/BC-008/BC-009/BC-010, IWO-U04,
the admitted U04 proof family, physical U04 proof and exact rejected implementation/diff before
mutation. No authority conflict requiring `BLOCKED` was found.

## Repaired candidate

- branch: `work/vi12r-u04-r031-repair`;
- candidate commit: `dc3b448191a2b2d3528ffb576b1ebc2c56839991`;
- candidate tree: `3c7a42eb215d708a0f8d8db37727133ecc234275`;
- candidate parent/routed handoff: `a3564f4908283f9bacf72f3720d020503f124e55`;
- changed paths:
  - `src/nvda_desk/raw_signal_occurrence_truth/api.py`;
  - `tests/product/raw_signal/test_u04_receipt_assessment.py`;
- candidate binary diff SHA-256: `2a1d6bc3d8aa923d0d9576173e4111ea575b4da491445cd75ae45db839ecdf93`.

### Mechanism closure

The rejected candidate maintained `relations_by_capture` and derived assessment presence only from
that optional materialised relation state. The repair removes that assessment dependency entirely.
`append_assessment` now examines the owner transaction's currently admitted observations, restricts
receipt evidence to the realised capture's exact `[slot_start_utc, slot_end_utc)` window, obtains the
capture's exact stored effective policy and invokes the admitted eligibility resolver for each
in-slot observation. Positive eligibility establishes `one_or_more_received`; an established lack of
eligible in-slot observations establishes `zero_received`. If in-slot evidence exists but the
required eligibility authority is unavailable, the command raises rather than manufacturing zero.

Observation `received_ts_utc` is no longer compared with `evidence_as_of_ts_utc`; it is used only for
the accepted receipt/capture-slot fact. The supplied UTC `evidence_as_of_ts_utc` remains the
assessment's BC-008 system-knowledge label. The U04 in-memory owner exposes no independent commit
clock, and this repair does not invent one; durable transaction/commit semantics remain deferred to
U05.

Existing assessment identity is checked before fresh evidence derivation. A same-ID retry with the
same capture/as-of/supersedes identity returns the already-appended record even if later evidence is
now admitted, preserving idempotence; changed identity-bearing inputs conflict. A new later
assessment still derives against the then-visible owner state and must supersede the immediate
predecessor.

The proof additions establish the repair mechanism rather than making relation materialisation
mandatory:

1. eligible admitted in-slot evidence yields `one_or_more_received` even when no relation object has
   been materialised;
2. in-slot evidence with no eligibility resolver fails closed; and
3. exact same-assessment retry remains its original zero after later evidence appears, requiring a
   new superseding assessment for changed knowledge.

Relation role/nonclaims, capture locality, ineligible/out-of-slot zero behaviour, append-only
history, immediate-predecessor supersession and U01-U03 behaviour remain covered by the preserved
proof.

## Exact pinned validation

Toolchain used: Python 3.13.5; pytest 9.0.3; mypy 1.20.1 (compiled); Ruff 0.15.11. The pinned tools
were restored offline from preserved project wheel evidence. No network package retrieval was
relied upon.

On candidate `dc3b448191a2b2d3528ffb576b1ebc2c56839991` / tree
`3c7a42eb215d708a0f8d8db37727133ecc234275`:

- U04 proof: **32 passed**;
- U01+U02+U03+U04: **416 passed**;
- source mypy: success, 15 source files;
- strict `--disallow-any-expr` mypy on modified `api.py`: success;
- Ruff `src tests tools`: pass;
- product-proof control: PASS, six families / 13 of 13 obligations;
- architecture validation: PASS, zero dependency/public-seam violations;
- dependency/public-seam checks: PASS;
- architecture/bootstrap: **74 passed**;
- clean-state architecture promotion: **74 passed**;
- `git diff HEAD^ HEAD --check`: pass;
- `git fsck --full --strict`: exit 0, with non-fatal dangling blobs
  `d9e05bce55672517b98b3b92de90379e30ec1be2`,
  `7293b42e4c2104678c5e61262e4b870f5056635e`,
  `895775b2d27b6006f3f245b6742d5d021fed089b`,
  `8b2975c927849b624b0d55b9118974975c91bada`, and
  `5f2b966adcbd83a68e901e79de258e620f15c8cc`;
- candidate worktree before handoff metadata: clean.

One validator invocation initially omitted the repository's required `PYTHONPATH=src:.` and stopped
at `ModuleNotFoundError: nvda_desk`; no semantic validator result was claimed from that invocation.
The command was rerun with the same invocation environment used by the repository's prior review
records and passed all four structural/control validators.

These are Worker-executed evidence only. U04 remains unaccepted pending fresh Reviewer 032.
