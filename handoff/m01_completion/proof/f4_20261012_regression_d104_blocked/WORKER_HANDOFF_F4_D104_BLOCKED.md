# NVDA M01 F4 — 2026-10-12 blocked continuation checkpoint

**Status: F4 BLOCKED / STAGE 1 NOT ACCEPTED / NOT an independent F4 acceptance candidate.**

## Authority and upstream position

- This continuation extends `e35821ae54923db78266baca998c69552a2a430f`, the authorised reconstruction of the `734cf58e8b826a065349b10efdac4019908e83fd` recovery base. It does **not** purport to recover the absent original RC23 commit `296fbae`.
- Binding authorities: repository `GUARDRAILS.md`, `AGENTS.md`, test override, root `EXEC_PLAN.md`, accepted M01 input brief and accepted CSV catalogue, plus the explicit D123/D116 programme-owner exceptions recorded earlier in Git.
- No normative source, GUARDRAILS, AGENTS, ExecPlan, provider mapping or Stage 2 implementation was modified in this continuation.

## Verified newly established proof (F4 RC05)

- D079/D080/D081 consume four separately scoped, versioned factor histories D075, D071, D076 and D077 through the admitted controlled M00 public interface. For seven aligned samples, expected slopes `2`, `3`, `4` are obtained. An eighth, excluded older outlier changes neither fit nor raw/predecessor lineage. These three rows have the same exact predecessor ID sets, raw lineage and fitted input version references. Missing aligned history, wrong child scope, extra aliases and insufficient history refuse.
- D078 uses the seven **prior** aligned observations to calculate the coefficients, then evaluates the eighth (current) return. Current injected outlier `0.02` produces an exact controlled residual of `0.02`, while all three predecessor coefficient occurrences share the same prior model source/provenance. A mismatched coefficient refuses at the kernel. Existing valid out-of-sample direct-kernel residual expectations are preserved.
- Separate proof-first RED commits precede the minimum production changes in `_stage1.py` and `api.py`. The substantive fix is scoped to M01 recursion, fit-window identity, aligned input usage and exact raw-to-derived provenance.
- F4 reconciliation recomputed against the unchanged authoritative 491 dependency edges plus one zero-edge sentinel: 174 Stage-1 rows = 144 closed + 30 cross-stage. Newly proven: 12 D079–D081 edges and seven D078 edges. **Eight closed-stage edges remain unproved: D104=2 and D150=6.** The 30 cross-stage own-kernel/public refusal proofs remain outstanding, without reduction.

## Genuine stop condition — D104

- **Source:** accepted brief `handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md` §5 K03, D104 rule; catalogue `handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv`, D104.
- The accepted catalogue requires **both** D099 (25-delta skew) and D100 (10-delta skew), classifies D104 as a single `vol points` result and specifies a comparison horizon. Its narrative specifies a current skew measure minus the **corresponding** prior skew measure, but does not specify how both skew families combine to form one scalar, nor any authorised family selector or invariant proving whether one side is conditional.
- **Observed defect:** current `_stage1.py` D104 implementation pools D099/D100 histories, then applies `_history_anchor` to the concatenation. The committed controlled RED witness demonstrates D099 prior/current = 10/20 and D100 prior/current = 30/40, both actual same-family changes +10; the kernel returns **−10** by pairing current D099 with prior D100 based on record identity ordering. This is a verified semantic defect. The missing normative choice of D104 scalar/family semantics is **not** resolved by choosing the other sort order.
- **Programme-owner question:** How shall D104's one `vol points` value be derived from the two separately corresponding 25-delta and 10-delta changes? State the exact required scalar rule or authorised conditional family-selection contract, including whether both D099 and D100 are mandatory. Do not invent arithmetic or a selection key. Once decided, commit normative clarification (with its explicit authority), bounded public proof before production repair, then continue F4.
- D104 mixed-family RED is deliberately retained as one failing test; it is not suppressed or labelled a full-suite PASS. D150 and the cross-stage 30 obligations were not completed. They may be continued after the authority condition under the existing ExecPlan.

## Validation for this exact checkpoint

- After the D078 production repair **before the new D104 RED**, PostgreSQL-backed `pytest -q tests/architecture tests/bootstrap tests/product tests/implementation/derived_signal --ignore=tests/product/raw_signal/test_u05_postgresql_durability.py` with the two separate M00/M01 DSNs and controlled PyYAML path: **1,155 passed** (`D078_BROADER_1155_PASS.log`).
- On the **current** tree containing the intentionally RED D104 test: same suite **1 failed, 1,155 passed**. The one failure is D104's mixed-family chronology (`CURRENT_BROADER_1155_PASS_1_RED.log`). No overall PASS is claimed.
- Isolated M00 PostgreSQL durability on current tree: interrupted after 27 progress marks due to execution limit; **no completed durability result** this turn. The earlier reconstructed checkpoint retains its independently recorded 55-pass M00 durability result (not substituted as this tree's rerun).
- Scoped Ruff lint and formatting on all touched implementation/test Python files **PASS** (`RUFF_LINT_PASS.log`, `RUFF_FORMAT_SCOPED_PASS.log`). Scoped Mypy **PASS** on `api.py` and `_stage1.py` (`MYPY_SCOPED_PASS.log`). These are not claims of whole-repository formatting or unexecuted broader Mypy.
- F4 reconciliation script **PASS** with original `491/492` population invariants; row status ledger still marks F4 candidate=false and Stage 1 independent acceptance=false.
- Reproducible environment: Python 3.13.5 pinned supplied offline U05 tools; PostgreSQL 17.9 with distinct M00/M01 roles via local socket port 55432. Exact test commands are recorded above; source path `PYTHONPATH=src:/mnt/data/F4_RUNNER/yaml_import` contains controlled available PyYAML, not the ambient Pydantic package. External runtime artifacts are supplied independently from this Git repository and are not shipped inside this tarball.

## Carry-forward / review status

- Keep D123 provider-independent proof and the **unverified** live provider mapping separate. Keep the authorised D116 dependency correction and R075/D117 meanings intact.
- Keep F1/F2/F3/F4 accepted prior evidence and full reconstruction Git lineage. Historical readbacks are historical evidence and should not override the current F4 ledger.
- No independent F4 Stage-1 acceptance candidate exists yet. Do not hand this package to the reviewer for Stage-1 acceptance. It is a **programme-owner authority-blocked checkpoint** with one precise D104 question, eight closed-stage edges and 30 cross-stage obligations still outstanding.

See parent archive manifest for exact HEAD, tree, SHA-256, readback and clean-state verification.
