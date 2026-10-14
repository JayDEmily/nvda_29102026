# NVDA V2 — Evidence index, authority and read boundary

Status: read-only investigation evidence index, **not** an acceptance certificate.

## Governing and normative sources actually read

1. `repository/GUARDRAILS.md` (10,247 characters) — highest frozen repository governance; authority, trace, stop, claims, Git preservation.
2. `repository/AGENTS.md` (5,617 characters), `repository/tests/AGENTS.override.md` — operating and test-local scope.
3. `repository/EXEC_PLAN.md` (30,411 characters) — original M01 3-stage plan with Stage1 F1–F4 amendments.
4. `repository/handoff/m01_completion/AUTHORITY_INDEX.md` — accepted starting boundary and effective amendments.
5. `repository/handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md` — 71,716 characters; §§1–18 and appendix, K01–K17 meanings.
6. Same authority directory: `NVDA_DERIVED_SIGNAL_CATALOGUE.csv` — SHA-256 `26c5486d1a4c7ff68025c7ce2d7e6847a7798759b847a716c942fd05345f3803`; `D104_CALCULATION_DEFINITION_AUTHORISED_CLARIFICATION_20261012.md`, `D116_CALCULATION_DEFINITION_AUTHORISED_CORRECTION_20261011.md`, `D123_CALCULATION_DEFINITION_AUTHORISED_CLARIFICATION_20261011.md`, `F4_OWNER_APPROVED_CLARIFICATION_20261013.md`.
7. Original workbook `NVDA_80_STEP_ACADEMIC_EVIDENCE_AUDIT_WITH_SIGNALS_ADDENDUM_81_94.xlsx`, original `Raw Signals`, `Derived Signals` source rows.
8. V2 workbook `handoff/workbook_v2/NVDA_SIGNALS_RESEARCH_WORKBOOK_V2_PASS08.xlsx` (41 sheets), old seven original tabs, 00 method, M01-1 candidates, module register/allocation and individual M02–M31 sheets; XML read-only parsing (not workbook formula evaluation).
9. V2 `ADR_WBV2_001_MODULE_RESPONSIBILITY_CLASSIFICATION.md`, `ADR_WBV2_002_DOWNSTREAM_MODULES_LOCAL_DUPLICATION.md`, `pass08_independence_clarification/PASS08_CLARIFICATION.md`.
10. V2 `reviews/m01_1_boundary_20261014/M01_1_FULL_209_ROW_ELIGIBILITY_REVIEW.csv`; `pass06_modules/PASS06_30_MODULE_REGISTER.csv`, `PASS06_95_D_MODULE_ALLOCATIONS.csv`, `PASS06_107_CROSS_MODULE_D_REFERENCES.csv`.
11. `docs/architecture/{OWNERSHIP_AND_COMPONENT_LAW,ARCHITECTURE_KERNEL,ARCHITECTURAL_OBJECT_TAXONOMY,EXTENSION_AND_RETIREMENT_RULES,PUBLIC_SEAM_LAW,DEPENDENCY_LAWS,TEST_AND_PROMOTION_KERNEL,IMPLEMENTATION_AUTHORITY_INGRESS}.md`. Relevant architecture text was loaded for read-only evaluation; identity, ownership, dependency, ingress and retirement clauses were inspected explicitly.
12. `config/architecture/modules.yaml` and `config/architecture/implementation_allocations.yaml` — current M00 active / M01 bootstrap and consumed identities.
13. Original source `src/nvda_desk/derived_signal_calculation_truth/{api.py,_stage1.py,_catalogue.py,_postgres.py,_financial_policy.py}` — inspected static AST function map, Stage1 dispatcher, public selection/lineage/materialisation, specific signal branches. **Not a complete per-function semantic reading of 209 calculations.**
14. Relevant actual test *source* (not run): `test_m01_f4_rc02_scalar_algebra_public.py`, `test_m01_f4_rc14_skew_from_native_delta_public.py`, `test_m01_f4_macro_vintage_public.py`, `test_m01_f4_book_slope_public.py`, `test_m01_f4_rc14_option_volume_z_public.py`, D123 public/controlled tests. Other test names in 209 CSV are textual mention navigation only.
15. Historical `handoff/m01_completion/proof/f4_20261012_source_preflight/SOURCE_SEMANTIC_PREFLIGHT_DISCREPANCY_REGISTER.md`, `.../f4_20261013_implementation/{PROGRESS.md,PAUSE_HANDOFF.md,INDEPENDENT_REVIEW_RETURN.md}`; historic results explicitly not re-executed or promoted.
16. Prior audit bundle `M01_TO_M01_1_SEMANTIC_REUSE_AUDIT.md`, `M01_M011_209_SIGNAL_SEMANTIC_AUDIT.csv` — inspected as claims/locations requiring independent verification; no governing status.

## Independently computed static reconciliations

- SHA-256 entire supplied primary and supporting archive files matched commissioning hashes.
- Git status clean at extraction; `git rev-parse HEAD` and `HEAD^{tree}` matched archive branch; `git fsck --full --no-reflogs` returned exit 0 with unreachable/dangling objects noted.
- Both current source-controlled catalogue copies had equal SHA-256 and 209 unique D IDs.
- The workbook V2 had 41 actual worksheets. Original workbook had seven.
- Effective D dependencies had no missing predecessor IDs and no cycle in the static DFS. Exactly 174 Stage1 / 35 Stage2 families; 144 Stage1-closed / 30 cross-stage; proposed M01-1 114 and downstream 95 exactly once; 107 direct peer-group references and 67 ordered group pairs in historical lineage.
- Full canonical predecessor closure, ultimate declared R field set and direct/recursive typed contexts for 209 IDs written to `02_D001_D209_TRACEABILITY.csv`; 95 downstream root closures and 30 peer summaries computed independently from effective normative D graph, not reused as claimed runtime edges.
- No row-level tests, databases, application code, lint, mypy or performance suites executed in this turn. No production or governance bytes changed.

## Precise inspected line witnesses

- `brief.md:95` — D009 three vintage statuses; `_stage1.py:1188–1225` only initial/latest.
- `brief.md:123` — D025 formula; `Raw Signals` R039=High/R040=Low; `_stage1.py:1354–1361` inverted; `test_m01_f4_rc02_scalar_algebra_public.py:29–30` inverted fixture.
- `Raw Signals` R015 = C/P option right, `_stage1.py:1430–1501` expects strike; `test_m01_f4_rc14_skew_from_native_delta_public.py:33–39` synthetic numeric R015.
- `brief.md:298`, `_stage1.py:1406–1428,1505–1510` and `api.py:2316–2330` — D096 K09 missing, four K02 dependent routes.
- `_stage1.py:2270–2401` — D117 uses R041, R075 role unknown.
- `D123 ... AUTHORISED_CLARIFICATION`, `_stage1.py:142–243`, `api.py:2485–2502` — controlled OI selection; native mapping unresolved.
- `_stage1.py:2603–2660` — D138 book-state OLS; L2 update event/snapshot contract unresolved.
- `api.py:2937–3046` — calculation, lineage, occurrence identity, append-only persistence.
- `config/architecture/modules.yaml` — M01 bootstrap/non-composable, D001–D209; M00 active.
- `ARCHITECTURAL_OBJECT_TAXONOMY.md` — decimal M identity syntax; `EXTENSION_AND_RETIREMENT_RULES.md` — owner transitions cannot silently inherit status.
- `PAUSE_HANDOFF.md` / `INDEPENDENT_REVIEW_RETURN.md` — no final original Stage1 acceptance.

## Retained epistemic limitations

A static CSV row/dispatcher mention is only a source location, not correctness. A test file mention is not coverage. Historical test logs can support only the exact old revision, environment and proposition. A controlled provider-independent test is not evidence of native official-period or full L2 book availability. A proposed workbook allocation is not an architecture admission. A SHA-256 or clean Git status is not semantic acceptance. This index must not be used to promote row-level `UNASSESSED` to `VERIFIED`.

## Resumption boundary

Next worker should open exact attached primary archive and this evidence index, reread current guardrails/agents/plan, verify the baseline, and continue **individual 209-row semantic/source/call-path/historical-evidence assessment**, particularly outside the named findings, before claiming investigation completion. Reconcile any new baseline by exact Git identity and catalogue digest. Keep tests off until a separately authorised future implementation/proof phase.
