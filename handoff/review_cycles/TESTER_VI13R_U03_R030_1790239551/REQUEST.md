# Review-cycle request

**Status:** `ACTIVE`

## Cycle identity

- **Cycle:** `TESTER_VI13R_U03_R030_1790239551`
- **Current actor:** `TESTER`
- **Predecessor Worker cycle:** `WORKER_VI12R_U03_NATIVE_DOMAIN_CLOSURE_1790236051`
- **Accepted/promoted U02 main:** `a78ae7b5515c2e482a2656cebeebae3fa5a6d584`
- **Rejected predecessor U03 candidate:** `d25aedeed5de65d0a241bdce6eae22671ef2ddf8`
- **Reviewer-029 FAIL:** `9b2ff603517c7fa5e063a4ad08790bb9fddd28c3`
- **Class-level U03 candidate:** `45ca4b8dcca6fdb5001e1754fd81bdba37ce05bf`
- **Candidate tree:** `81ef8edc93c9b322b29cdec6b9ab76b731d8e9a5`
- **Worker branch:** `work/vi12r-u03-native-domain-closure`
- **U04:** prohibited

## Mandatory readback

Before substantive review, read in full root `GUARDRAILS.md`, root `AGENTS.md`, the complete
current `EXEC_PLAN.md`, `handoff/control/CURRENT_STATE.md`, this request, and
`implementation/authority/VI13R_U03_NATIVE_VALUE_DOMAIN_AUTHORITY.md`. Read accepted IRB BC-005,
BC-006, BC-009, BC-010 and BC-012, IWO-U03, the exact candidate implementation/proof, and enough
Reviewer-025..029 lineage to preserve the recurrence/class-level context.

## Authorised task

Independently review only the repaired **IWO-U03 — Raw observation admission, native fidelity and
temporal-kind truth** class-level candidate bound above. Do not begin or assess U04.

Review the **class-level closure proposition** supplied by
`VI13R_U03_NATIVE_VALUE_DOMAIN_AUTHORITY.md`, not a new arbitrary Python value type outside the
authorised carrier. Determine whether, on this exact candidate:

- public/static and runtime boundaries agree on the authorised finite recursive NativeValueV1 carrier;
- allowed values preserve provider-logical native content and alias-safe readback;
- separately reconstructed identical admitted content is idempotent;
- conflicting admitted content rejects without replacing the first occurrence;
- mapping implementation/order is nonsemantic while logical exact string keys and recursive values are semantic;
- float and Decimal exactness are representation-sensitive as authorised;
- unsupported representations fail closed before semantic state mutation;
- no runtime path can use arbitrary user-defined `__eq__` or another unbounded object-equivalence fallback;
- the reclassified Reviewer-026..029 outside-carrier witnesses remain active fail-closed proof;
- existing U01/U02 and still-valid U03 semantics remain intact; and
- U04 remains untouched.

Do not demand a datetime comparator or another open-ended per-Python-type catalogue: datetime and
other values outside NativeValueV1 are unsupported under current authority. Do not invent provider
validity, provider duplicate/retransmission equivalence, persistence/replay or downstream semantics.

Primary obligations remain IA17-PROD-003, IA17-PROD-004, IA17-PROD-005 and the observation/identity
portion of IA17-PROD-008.

## Required disposition

Return exactly one U03 disposition: `PASS`, `FAIL / RETURN_TO_WORKER`, or `BLOCKED`.

If PASS, state that U03 may be lawfully promoted; U04 becomes authorised only after that promotion.
If FAIL, identify the exact authorised class-level proposition defeated, owning layer and smallest
bounded repair. If authority itself is insufficient or contradictory, return BLOCKED rather than
inventing law.

Record response/evidence/commands/result in this cycle, preserve exact candidate identity, create
the next opposite-role cycle required by the disposition, update `CURRENT_STATE.md`, and return a
full-Git TAR.
