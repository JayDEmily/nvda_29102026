# M01 F4 D123 — mandatory official-refresh identity source-contract blocker

Date: 2026-10-11. Status: `BLOCKED` under GUARDRAILS failure/stop law. **Not** an F4 or Stage-1 reviewer candidate.

## Verified repository boundary

* Continuation from complete full-Git D123 blocker checkpoint `e84060a06dd56b02af1cf0117a29b66169eb671e`, descendant of RC14 `6f611c68a3de32bc90e63a9ce8289f80027b5e83`.
* Programme Owner now explicitly authorises the D123-only right-conditional interpretation of the unchanged R047/R048 catalogue set and the official-refresh rule. Normative meaning preserved at `authority/D123_CALCULATION_DEFINITION_AUTHORISED_CLARIFICATION_20261011.md`.
* The accepted reference workbook `Raw Signals` identifies R047 as IBKR *Option Call Open Interest*, tick 27, and R048 as *Option Put Open Interest*, tick 28, both delivered via `EWrapper.tickSize`. It provides no official OI report-period field or vintage precedence in those R047/R048 source rows. This workbook is reference evidence, not an overriding catalogue source.
* The admitted M00 `RawObservationOccurrenceV1` and `ProjectedRawValueV1` carry `source_timestamp_raw`, `source_temporal_kind`, `received_ts_utc`, `ingestion_sequence/scope`, `revision_vintage_native`, and optional `selection_identity`. An explicit versioned mapping can project native identity fields. The current D123 controlled M00 witness maps **only** exact contract dimensions and value, and uses generic `official-v1` vintage text. No official reporting-period key, provider guarantee tying the source timestamp to a report period, or provider revision precedence has been established.
* IBKR's published tick-type definitions (https://interactivebrokers.github.io/tws-api/tick_types.html) identify values for tick 27 and tick 28. They do not, in those tick definitions, document a separately emitted official reporting-period identity or revision-ordering field. This is a narrow observation about the consulted definitions, not proof that no other admissible official source exists.
* `src/nvda_desk/derived_signal_calculation_truth/_stage1.py` D123 currently takes two most recent event/receipt-ranked points by `subject_instrument` for each raw ID and sums changes; it cannot distinguish official reporting periods or same-period revisions. `api.py` currently insists on a cross-side exact join and loads both dependencies, so it also conflicts with the authorised call/put conditional interpretation.

## First unmet mandatory invariant

Select **two distinct eligible official reporting periods** for the selected exact call or put contract, then select each period's authoritative revision using established source/version precedence. The admitted fields by themselves do not say which reporting period a native IBKR open-interest tick belongs to or how different revisions of the same report period are ordered. Two successive received ticks could represent distinct official periods or same-period revisions. Without source authority, both interpretations are compatible with the same observed tick/receipt history but yield different deltas. Deduplicating on tick receipt time or treating opaque `revision_vintage_native` strings as sorted version numbers would invent semantics, expressly prohibited by the current instruction.

**Exact required authority/contract:** identify the authoritative official-OI source for R047/R048, the precise immutable native field(s) or M00 mapping that establishes *reporting-period identity* separately from *revision identity*, the rule for selecting the latest eligible revision of each period, and the authoritative ordering of periods and vintages under a cutoff. If IBKR tick 27/28 supply only the numeric OI value, clarify the admitted source of the period/revision identity rather than deriving it from arrival timestamps.

## Evidence and disposition

Original +25 public-seam witness: `tests/product/derived_signal/test_m01_f4_d123_exact_contract_authority.py` (unchanged). Its controlled records have distinct source instants and receipt instants and an opaque `official-v1` vintage; those do not establish two *official report periods*. Its expected +25 result is preserved. Original failing results and direct-kernel control are at `proof/f4_20261010_d123_blocked/`. This continuation did **not** change production source, the CSV, those tests, or the D123 arithmetic, nor did it claim that existing 1,069-pass RC14 regression establishes D123.

No dependent D123 repair may responsibly be marked green before this source-contract gap is resolved. The prior reconciliation reports 56 outstanding Stage-1-closed edges and 30 cross-stage own-kernel/refusal proof obligations; no evidence in this checkpoint reduces them. The independent R075/D116 discrepancy is not resolved or modified; preserve it as a separate investigation after D123 has a valid source contract. F4 and Stage 1 remain unaccepted; Stage 2 remains unauthorised.

This is an authority/source-contract stop expressly required by the 2026-10-11 Programme Owner instruction §3, not an intermediate review request after completed D123 work.

## 2026-10-11 executable evidence readback

* `python -m pytest -q tests/product/derived_signal/test_m01_f4_d123_exact_contract_authority.py` — **1 failed** (same preserved +25 public `materialise` witness returns `None`). New log `D123_ORIGINAL_PUBLIC_WITNESS_REPRODUCTION.log`.
* `python -m pytest -q tests/product/derived_signal/test_m01_stage1_semantics.py -k open_interest_change` — **1 passed**, **40 deselected**; this legacy *direct-kernel* control does not distinguish official report periods from arriving ticks, so its pass does not answer this blocker.
* `python -m pytest -q tests/product/derived_signal/test_m01_f4_d123_official_reporting_identity_red.py` — **1 failed as designed**: current direct kernel emits `+25` despite no reporting-period identity in either raw value. The proof was committed *before* any production change, commit `241069bd836dacfd51d3bc1be4e0ac7b6ac6b01a`.
* Broader PostgreSQL/architecture/type/lint checks **not run on this checkpoint** because no authorised production repair occurred and the mandatory source contract is unresolved. The active Python environment has pytest 9.0.2 and lacks the `ruff` and `mypy` modules; the archived pinned offline environment bundles remain available, but no type/lint PASS is inferred.

**Important separate obligations:** conditional R047/R048 repair is authorised but not implemented here. The new normative clarification must not be mistaken for a code correction. The RED proof is retained intentionally; code changes dependent on defining reporting-period identity were stopped at the first missing invariant, not patched around.
