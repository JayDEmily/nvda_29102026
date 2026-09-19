# Reviewer 004 — VI-11 Fresh Proof-Adequacy Review

## Assignment

Execute **VI-11 only** as a genuinely fresh independent reviewer.

The reviewer must not inherit the VI-10 proof author's reasoning/history and must not inspect or author production implementation. Review the exact accepted authority against the committed physical proof and decide whether materially wrong implementations could still pass.

## Exact review target

VI-10 Worker state:

- commit: `f83efd9b489dbe7072da8c96320504a468c55a1a`
- tree: `beba36d889696915bbcecccd861dab9ab0c1a4cd`
- PM design/handoff baseline: `a2a3578aee21f2b3ab5412e2244284ba59c895f6`
- baseline tree: `061534297b1879477200e8215b1ce04b6e31de21`

Review the proof-authoring delta `a2a3578a...f83efd9b` and the exact committed files at the VI-10 Worker state.

## Mandatory read order

1. `GUARDRAILS.md` in full.
2. Root `AGENTS.md`.
3. Accepted root `EXEC_PLAN.md`, especially VI-09 through VI-12R.
4. Exact accepted BICP/IRB/IWO:
   - `handoff/authority/BICP_CANDIDATE_005.json`
   - `handoff/authority/IRB_ACCEPTED_IMPLEMENTATION_BRIEF.md`
   - `handoff/authority/VI05_IMPLEMENTATION_WORK_ORDER_CANDIDATE_001.md`
5. Exact current/routed product-proof normatives identified by the BICP, especially N15/N19 and the N04/N06/N18/vocabulary propositions cited by the six families.
6. `tests/AGENTS.override.md`.
7. `implementation/proof/VI10_ADVERSARIAL_PRODUCT_PROOF_DESIGN.md`.
8. `config/product_proof/authority.yaml`, `families.yaml`, `aggregates.yaml`, schemas and validator/runner.
9. All six physical `tests/product/raw_signal/test_u0*.py` files plus `_support.py`.
10. `implementation/proof/VI10_ADVERSARIAL_PRODUCT_PROOF_EVIDENCE.md` as evidence only, never as a substitute for inspecting the tests/authority.

## Review questions

Return findings against these propositions:

1. **Authority fidelity:** Does every asserted product meaning trace to exact accepted authority, with no test-authored product semantics or defaulted Remaining Unknown?
2. **Coverage completeness:** Do the six families physically exercise every current product obligation they claim and the BC-014/BC-015 adversarial surface, rather than merely list it in YAML?
3. **False-positive resistance:** For each material proposition, could a plausible wrong implementation pass because only the positive case is exercised?
4. **Negative/absence/unknown matrix:** Are prohibited/false-positive, missing-mandatory-authority, lawful optional-absence, identity/retry, lineage/status and temporal substitutions exercised where applicable?
5. **Real-boundary fidelity:** Does U05 genuinely require real PostgreSQL 17.9 + Psycopg 3.3.4 and fresh durable readback/restart, with no in-memory/mock/same-process substitute?
6. **Proof/architecture separation:** Is product proof kept distinct from `architecture_kernel`; are product families still `NOT_CLASSIFIED` rather than Tier A/B/C?
7. **Test-facing construction glue:** Could `_build_test_owner` or `_build_test_application` hide domain semantics and let a wrong owner/composition pass? Are the tests strong enough to detect that class of cheat?
8. **A00/M00 boundary:** Could A00 decide Raw Signal outcomes, bypass the typed seam/private state, reverse the dependency or activate P01/K01/downstream meaning while the current U06 tests still pass?
9. **Identity/time/null law:** Could identity layers collapse, date-only become midnight UTC, receipt time fill provider time/timezone, optional absence become a default, provider null be lost, or D001/event time appear while tests still pass?
10. **Assessment law:** Could history be overwritten, supersession be cyclic/non-immediate, unknown collapse to zero, or one-or-more become exact count/finality while tests still pass?
11. **Schedule law:** Could a second capture be admitted for the same `(policy, slot)`, activation/deactivation boundaries drift, or wake/receipt/provider time become schedule truth while tests still pass?
12. **Compatibility law:** Does the physical proof genuinely discriminate breaking v1 requiredness/discriminant/time/null/identity/provenance changes, or only claim compatibility in metadata?
13. **Claim precision:** Are proof levels, environment, limitations and adjacent nonclaims exact? Does any family overclaim beyond what its physical test observes?

## Required method

- Review authority and physical tests, not production code.
- Construct plausible mutants/wrong implementations mentally or in isolated proof-only fixtures where useful and ask whether they would pass.
- Do not weaken or rewrite tests to obtain a favourable verdict.
- Do not count registry prose as physical coverage where the corresponding test does not exercise it.
- Do not count pre-implementation red as proof adequacy by itself.
- Treat historical Tier A/B/C material as method evidence only; do not reactivate historical identities, admissions or green states.
- Distinguish proof gaps from intentionally deferred production behaviour.

## Verdict contract

Return exactly one overall verdict:

- `PASS` — no load-bearing proof-adequacy finding remains;
- `FAIL` — one or more concrete proof gaps could allow a materially wrong implementation to pass;
- `BLOCKED` — required review authority/evidence/capability is unavailable.

For each finding provide:

- stable finding ID;
- severity: `CRITICAL | IMPORTANT | MINOR`;
- exact authority/proposition affected;
- exact physical test/config path and relevant test name(s);
- a concrete wrong implementation or false-positive path that could pass;
- why existing proof fails to discriminate it;
- smallest proof-side correction needed.

Do not begin VI-12R implementation.
