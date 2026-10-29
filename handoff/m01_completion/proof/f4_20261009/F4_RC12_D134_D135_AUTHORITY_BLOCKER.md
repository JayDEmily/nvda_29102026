# F4 — first unresolved RC12 invariant: D134/D135 book representation

Date: 09-10-2026. Disposition: **BLOCKED — authority required; not F4 accepted**.

## Normative inputs and observed code

1. Accepted immutable `handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv` lists **D134** and **D135** as K02/P_BASIC with exactly `R188;R190;R185` raw dependencies, respectively SMART side, size, and level/position; **R187 operation is absent** from both rows. D136 has only the derived `D134;D135` dependencies.
2. Accepted `handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md`, §5 K02, requires D131/D134/D135 to be exact displayed-size depth sums after deterministic book reconstruction. **For event-driven** L2 books it requires operation and row-position semantics in receipt/ingestion order, including insert/update/delete.
3. `src/nvda_desk/derived_signal_calculation_truth/_stage1.py`, `_book_events`, requires (`R185`,`R187`,`R188`,`R190`) to form each SMART native book event. The D134/D135 `K02` branch calls `_book_events` and `_book_final_state`, then sums depth. `R187` cannot be supplied through those rows' declared dependency bindings without crossing the accepted catalogue boundary.
4. The M00 admitted projection and native metadata contain provider/variant, observation IDs, revision and timestamp data. They do not, without a separately accepted semantic contract, assert that an arbitrary set of `R185/R188/R190` observations is a complete, coherent level-2 **snapshot**, rather than part of an event-driven mutation stream. A source variant or `native_units` label in controlled test data cannot itself legislate snapshot completeness.

## Discriminating public result

- `tests/product/derived_signal/test_m01_f4_depth_snapshot_authority.py` admits two controlled versioned observations through the real M00 owner, each with exactly the normatively declared R185/R188/R190 fields (bid level 1 size 10, ask level 1 size 7), with identical eligible event instants, provider and variant.
- The public D134 result is **persisted `0`**, not expected bid displayed size `10`; no operation R187 can be reconstructed. The witness is committed **as failing**, and is not counted as an accepted source-format or implementation proof. See `F4_RC12_D134_D135_PUBLIC_DEPTH_RED.log` and preceding proof-first commit `450b7e6`.
- Whether the controlled records can be admitted as **complete snapshots** is precisely the missing normative distinction. Therefore the red witness establishes the present public representational failure and evidence insufficiency, but does **not** independently prove a fully specified valid snapshot contract. Calling the returned zero a definitively wrong real-provider depth would overstate that evidence.

## Required authority decision — one bounded resolution

**Recommended programme-owner clarification:** Define a versioned, typed **complete SMART book snapshot** input contract for D134/D135, using only their existing R185/R188/R190 dependencies. Specify the exact completeness/batch identity, subject/provider/variant and revision association, top-N level and side coverage, selected as-of state and temporal precedence, and fail-closed treatment of missing levels/partial snapshots. The M00→M01 public projection must carry sufficient evidence to prove the selected snapshot coherent; a guessed variant string or an assumed zero baseline is insufficient. Permit *only then* a proof-first implementation of the accepted depth sums.

If the programme instead requires **incremental event replay** for D134/D135, it must separately reconcile the accepted three-field catalogue with mandatory R187 operation access through an authorised normative/domain change. The current F4 worker cannot alter that catalogue unilaterally. No choice between those contracts is authorised by the inspected materials.

Until this decision, **do not calculate a surrogate zero, inject R187 undeclared, or label D134/D135/D136 public reachability proved.** Stop dependent F4/Stage-1 completion under `GUARDRAILS.md` stop law and `EXEC_PLAN.md` F4 scope lock.

## Remaining F4 evidence

The independent F1 inventory remains 488 declared dependency edges and one D007 zero-edge sentinel. The updated `f4_progress_readback.py` conservatively accounts for 18 previously accepted F2, 11 bounded F3, 35 bounded F4 public edges, **317 Stage-1-closed edges still without bounded public proof** (including six D134/D135 edges), and 107 Stage-2-boundary-deferred edges; the D007 zero-edge sentinel has its own public witness. These are accounting statuses, not proof of all 144 closed rows or 30 cross-stage rows. No independent Stage-1 acceptance is claimed.

## Test scope

The recorded combined regression excludes the deliberately failing D134/D135 authority witness **and** the separately exercised M00 durability suite. Its 734 passes, Ruff and source mypy are not evidence that D134/D135 is correct or that F4 is complete. PostgreSQL M01 boundary tests were included using the established role-specific DSNs. The independent 55-case M00 durability suite was passed during the prior F3 checkpoint and was not rerun in this blocked-F4 pass.
