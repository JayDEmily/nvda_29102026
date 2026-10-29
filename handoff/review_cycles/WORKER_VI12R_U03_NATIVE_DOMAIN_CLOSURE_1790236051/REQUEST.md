# Review-cycle request

**Status:** `ACTIVE`

## Cycle identity

- **Cycle:** `WORKER_VI12R_U03_NATIVE_DOMAIN_CLOSURE_1790236051`
- **Current actor:** `WORKER`
- **Authority-resolution parent:** `65716819fd24cc7d5941cace83e5883d8e0e76f9`
- **Rejected U03 candidate still under repair:** `d25aedeed5de65d0a241bdce6eae22671ef2ddf8`
- **Rejected candidate tree:** `21eb6bd2ba53b29ea6d80f90c01af40668f56955`
- **Reviewer-029 disposition:** `FAIL / RETURN_TO_WORKER` at `9b2ff603517c7fa5e063a4ad08790bb9fddd28c3`
- **Accepted/promoted U02 main:** `a78ae7b5515c2e482a2656cebeebae3fa5a6d584`
- **U04:** prohibited

## Mandatory readback

Before mutation, read in full:

1. root `GUARDRAILS.md`;
2. root `AGENTS.md`;
3. root `EXEC_PLAN.md`;
4. `handoff/control/CURRENT_STATE.md`;
5. `implementation/authority/VI13R_U03_NATIVE_VALUE_DOMAIN_AUTHORITY.md`;
6. accepted IRB BC-005, BC-006, BC-009, BC-010 and BC-012;
7. IWO-U03 and the current U03 implementation/proof relevant to the candidate;
8. Reviewer 025 through Reviewer 029 dispositions sufficiently to preserve the relevant lineage.

## Authorised task

Implement the class-level U03 closure established by `VI13R_U03_NATIVE_VALUE_DOMAIN_AUTHORITY.md`.

The Worker is **not** being asked to invent a domain or determine whether authority is sufficient. That decision is now supplied. Implement the smallest complete repair that makes the authorised NativeValueV1 carrier and exact-content relation true at both the public/static seam and runtime boundary.

Required result:

- finite NativeValueV1 carrier exactly as authorised;
- runtime admission rejects unsupported carrier representations before semantic state mutation;
- native snapshot/readback remains alias-safe and preserves admitted logical value content;
- retry exactness is total over the authorised carrier and has no generic arbitrary-object equality fallback;
- separately reconstructed identical allowed values remain idempotent;
- conflicting allowed values reject and preserve the first record;
- mapping implementation/order is not semantic content, but logical string-key/value content is;
- float and Decimal exactness remain representation-sensitive as authorised;
- all still-valid prior U03 semantic proof remains green;
- prior implementation-coupled witnesses that are now outside the authorised carrier are explicitly reclassified into compact fail-closed unsupported-representation proof rather than silently removed.

Do not implement a `datetime` special case. Do not create another open-ended per-Python-type comparator catalogue. Do not broaden into provider mapping policy, U04, persistence or replay.

## Mutation boundary

Production mutation is limited to the U03 Raw Signal owner/public carrier implementation required for this authority closure. Proof mutation is limited to U03/type-seam/support paths necessary to express the new finite carrier and reclassify superseded implementation-coupled witness assumptions. Do not mutate `GUARDRAILS.md`, accepted IRB/BICP meaning, U04 production, U05 or later units.

If a still-valid accepted proof appears to conflict with the new authority, stop and identify the exact conflict rather than weakening it silently.

## Validation and handoff

Before routing to Reviewer 030, freeze one candidate and record:

- exact commit/tree and changed paths;
- the public/static NativeValueV1 declaration;
- runtime admission/validation behaviour;
- allowed-carrier exactness tests including reconstructed NaN/Decimal representation and recursive container cases;
- compact unsupported-carrier fail-closed tests including at least one arbitrary custom `__eq__` object and the Reviewer-029 `datetime` witness class;
- proof that rejected conflict/unsupported retry does not replace the first stored occurrence;
- complete U01+U02+U03 proposition-bearing proof;
- current required mypy/Ruff/product/architecture/dependency/public-seam controls; and
- clean Git/integrity state.

Only after that evidence exists may the Worker create a fresh `TESTER_...` Reviewer 030 cycle. Reviewer 030 must review the class-level closure proposition in the authority document. U04 remains prohibited until U03 receives independent PASS and lawful promotion.
