# Consolidated M01 F2 — provider-independent F2b worker-to-reviewer handoff

**STATUS:** Worker candidate for independent F2 review; **not** F2 acceptance, Stage-1 acceptance or F3 authorisation. Date: 09-10-2026. The exact Git HEAD/tree and verification are in the commit/manifest readback, not the historical filenames.

## Authority and scope

Current owner clarification 09-10-2026 14:13 authorises controlled, versioned R284/R289 proof through actual public M00 projection without preselecting a live provider. Earlier 13:55 source verification finding remains historically true, but **real-provider integration does not block controlled calculation proof**. User's 13:41 separation remains in force: D064 K07/P_SCORE calculation and D065 actual Boolean are M01 truth; strategy `event_filter_enabled: Boolean = FALSE` is deferred, not implemented. No category conversion or user-proposed 0.01–100 coefficients. No changes to accepted catalogue, GUARDRAILS, AGENTS, ExecPlan, M00, package version or strategy module.

## Code and proof sequence

- Source: `src/nvda_desk/derived_signal_calculation_truth/api.py` (typed ScoreFeature admits explicit R289, M00 R284 ISO timestamp under explicit versioned unit, per-event revision and event-scoped predecessor resolution, competing-event lineage) and `_stage1.py` (raw feature extractors, explicit weighted component scalarisation, canonical provider/variant/event-ID D064 linkage and correct Boolean D065). No direct M00 private table access; all sample data admitted and read through M00 public mechanism.
- First test-only red commit `da7f15b` captured six failing public projection proofs. Second test-only red `35d02d0` expanded adversarial matrix. Production `054aa1d` repaired the core implementation. Third proof `3c82bdb` captured **two red lineage failures** on competing R284 events; production `fad935d` preserves **every latest competing event revision** that affects nearest-event selection (superseded revisions excluded).
- Controlled identities: `event.id` is a **proof-only** native field declared in the versioned controlled projection mapping; canonical selection identity `event_id`, source provider and variant retain separate namespaces. No real native field is asserted. Separate R284 and R289 raw occurrences and importance/schedule revisions are admitted with cutoff and receipt/ingestion sequence. Equal precedence/identity ambiguities refuse results; no UUID or event-description equivalence.
- D064 score: declared numeric raw-R289 feature; K07 configured scalar extractor, explicit component coefficients, transforms, orientation, weights, clipping and intercept; no implicit category conversion. Missing raw identity, mandatory importance, feature or mapping returns no occurrence.
- D065: latest eligible R284 revision per stable event; nearest eligible scheduled event using accepted tie-earlier law, event-scoped D064 predecessor, version/temporal constraints, importance threshold; actual TRUE or FALSE. Outside the event window with known eligible calendar returns FALSE; missing/ambiguous event or importance does not become FALSE. D062 countdown need not exist after an event. Both selected D064's R289 and all latest competing R284 observations are recorded to reconstruct the decision.

## F2 edge and class reconciliation

- `../f2_observation_identity_20261009/F2_EDGE_RECONCILIATION.csv` lists exactly **18** F2 edges; independent set/identity/class comparison with accepted `F1_CLASSIFIED_EDGE_MAP.csv` is recorded in `F2_CENSUS_READBACK.json`. It validates against F1's **488** direct edges. The 18 F2 edges are **scoped to RC01, RC07, RC08, RC09, RC21**; neither 18 edges nor these tests exhaust all 488 edges or every member of those five classes.
- F2a RC07/RC08 D015/D016/D120: unchanged signed-flow witness and late-quote temporal regression are retained (`tests/product/derived_signal/test_m01_f2_observation_identity.py`, `test_m01_f2a_temporal_quote_sign.py`, `handoff/m01_completion/review/proof/test_f2_late_quote_sign_20261009.py`).
- F2a RC09 D017: exact same-observation trade price/size pairing proofs retained.
- F2b RC21 D064/R289 raw P_SCORE: 1 edge; F2b RC01 D065/R284 and D062/D064: 3 edges. Controlled event tests are in `tests/product/derived_signal/test_m01_f2b_event_public.py` (18 public-seam tests). Explicit D062 absence after event does not substitute a Boolean when an R284/R289 prerequisite is missing.
- **F3/F4 separation:** Other classes/rows in the F1 488-edge census remain governed by their own gates; previous Stage-1 partial proofs and unassessed D121/D122 grouped paths are not asserted complete here. No F3 grouping change occurred.

## Executed proof environment and results

- Offline project bundle `NVDA_U05_PROOF_ENV_BOOTSTRAP_PY313_PG17_9_20260926` supplied pinned Python **3.13.5**, pytest **9.0.3**, psycopg **3.3.4**, Ruff **0.15.11**, mypy **1.20.1**. PyYAML **6.0.3** reused from host site package without repository change.
- Portable PostgreSQL **17.9**, Unix domain socket, UTF-8, `fsync=on`, `synchronous_commit=on`, `full_page_writes=on`; isolated M00/M01 proof roles with separate schemas; proof M00 role granted database `CREATE` for existing R02 negative-path test.
- Combined applicable regression (all product tests other than separate M00 55-case durability file, architecture/bootstrap, M01 implementation) **693 passed**; M01 implementation **44 passed**; M00 implementation **34 passed**; all 55 M00 durability case IDs **passed in seven bounded invocations** (15+6+1+3+4+11+15), *not* one uninterrupted run. These are overlapping suites, not an additive unique-total figure.
- Ruff `check src tests tools`, mypy `src` (21 files), `tools/validate_architecture.py` all passed. Logs supplied by basename in this evidence folder; original failure-trace files with incidental pytest trailing whitespace are preserved **byte-for-byte** in `.log.gz` files rather than edited. See `SHA256SUMS`.
- An *initial* M00 durability attempt failed three cases due to configuring `NVDA_TEST_POSTGRES_DSN` for a different DB, while test `_admin_dsn` explicitly targets `dbname=postgres`. After using bundle-provided DSN all 15 in that group passed. A combined 16–25 run subsequently timed out during a multi-process test; the corresponding IDs were all rerun to completion in bounded sets. No source/tests were changed to bypass either test-environment issue.

## Proof boundary and review request

**Verified by controlled input:** typed M00→M01 provider-independent calculation, score configuration, event version matching and refusal, temporal/lineage invariants for the described cases, F2 edge ledger accounting, preserved F2a and database regression. **UNVERIFIED:** live provider-specific native event field, stable upstream identifier across actual feed updates, variant/version mapping, live integration; no live data was used. **NOT CLAIMED:** exhaustive 488-edge proof, full Stage 1, F2 independent acceptance or F3/Stage 2 authority.

**Next action:** one independent reviewer examines this exact full-Git candidate, compares F2a/F2b proofs with accepted brief and F1 census, and records F2 disposition. No intermediate reviewer round trip or F3 work is authorised by the worker.
