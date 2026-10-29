# Review evidence

**Status:** `COMPLETE`

## Binding

- role: fresh independent Reviewer 025 / TESTER
- authorised scope: IWO-U03 only; U04 not assessed
- source transport SHA-256: `44e374883a61de4fff96a359d645241ee2c73ae9a02a4e3db287bab5527a8be2`
- exact source transport filename: `NVDA_G03_TESTER_VI13R_U03_R025_1790139709_FULL_GIT_20260923.tar(1).gz`
- transported repository HEAD before review: `c96cc8bb752317006ccaeebb6c97f6a82f9b9db6`
- accepted/promoted U02 forward `main`: `a78ae7b5515c2e482a2656cebeebae3fa5a6d584`
- frozen U03 production candidate: `7cf8936f854fbed952a468ce06c2f2a0320d9291`
- candidate tree: `b63aac7fb538ea6a38ce3dea5aab719fc7be0ee0`
- candidate parent: `a78ae7b5515c2e482a2656cebeebae3fa5a6d584`
- candidate production path: `src/nvda_desk/raw_signal_occurrence_truth/api.py` only
- complete production diff SHA-256: `91f20c62a03884aae9a666c105a91a4477ad66257e1ad00ffc50cba9046fb8ff`
- candidate-to-transport material diff over `src tests config tools pyproject.toml`: none

## Governing material inspected

Read in full before substantive review: root `README.md`, `GUARDRAILS.md`, root `AGENTS.md`, complete
current `EXEC_PLAN.md`, `tests/AGENTS.override.md`, `handoff/control/CURRENT_STATE.md`, active
Reviewer-025 `REQUEST.md`, accepted IRB, BICP Markdown, complete IWO and Worker U03 evidence. The
review then inspected the complete U03 production diff/current `api.py`, complete U03 product proof,
relevant U01 support/public-contract code and the accepted Reviewer-024 boundary disposition.
Relevant semantic clauses were BC-005, BC-006, BC-009 and BC-010. U04 implementation acceptance was
not assessed.

## Exact candidate validation

Validation ran in a detached worktree at exact candidate commit
`7cf8936f854fbed952a468ce06c2f2a0320d9291` with project-pinned tooling provisioned outside the
repository:

- Python 3.13.5
- pytest 9.0.3
- mypy 1.20.1 (compiled)
- Ruff 0.15.11

Observed results:

- focused U01+U02+U03 pytest: **366 passed**
- strict positive public-seam mypy specimen: **pass**
- strict negative public-seam mypy specimen: **expected rc 1**, all 15 intended negative sites diagnosed
- source mypy: **pass across 15 source files**
- Ruff over `src tests tools`: **pass**
- product-proof control: **pass, six families and 13/13 obligations**
- architecture validation: **pass, zero dependency/public-seam violations**
- dependency validation: **pass**
- public-seam validation: **pass**
- architecture/bootstrap: **74 passed**
- `architecture_kernel` promotion: **74 passed**
- `git diff --check`: **pass**
- `git fsck --full --strict`: **pass**
- exact candidate detached worktree after validation: **clean**

One earlier promotion invocation used the positional form instead of repository-declared `--set` and
returned CLI rc 2; the correct repository-native invocation then passed 74/74. One temporary
adversarial script invocation omitted the repository root from `PYTHONPATH`; it was corrected to
`PYTHONPATH=src:.` without repository mutation. Neither environment/command error is attributed to
the candidate.

## Bounded U03 challenge

The candidate correctly preserves several requested U03 behaviours under direct challenge:
ordinary `_state` is not exposed on the public facets; distinct observation IDs sharing one delivery
remain distinct; separately reconstructed genuinely identical payloads retry idempotently; local
sequence decrease is rejected while another scope may restart at a lower sequence; no-scope
observation readback succeeds; and no raw `event_ts_utc` is introduced.

### R025-U03-F001 — retry equality collapses exact native numeric content

**Status:** `OPEN` / material implementation defect.

**Accepted propositions defeated:**

- IRB BC-005: preserve provider-native values unchanged, including admitted exact numeric fidelity;
- IRB BC-009: conflicting payload under the same occurrence identity is rejected without synthetic
  replacement;
- IRB BC-010: same occurrence identity is idempotent only for identical content and conflicting
  content under that identity must fail closed;
- IWO-U03 and active Reviewer-025 request: exact native numeric runtime type/representation plus
  same-occurrence retry/conflict separation.

**Concrete failure path:** the implementation checks `existing != value` where dataclass/Mapping
comparison uses ordinary Python value equality. Python therefore considers native `1 == 1.0` and
`Decimal("1.0") == Decimal("1.00")`. Independent canaries using the public owner command proved:

1. first admit same-ID `native_record={"Native": 1}`;
2. retry same ID with `native_record={"Native": 1.0}`;
3. payloads compare equal; retry is accepted and the stored `int` value is returned rather than
   rejecting the changed runtime type;
4. separately, first admit `Decimal("1.0")`, retry `Decimal("1.00")`; retry is accepted although
   their exact `Decimal.as_tuple()` representations differ, and the first scale is silently retained.

This is not a hypothetical provider-equivalence rule. U03 already treats exact numeric runtime type
and Decimal representation as fidelity-bearing evidence, while BC-010 requires conflict rejection
under same occurrence identity. The current equality check collapses those accepted distinctions.

**Owning layer:** U03 M-owner implementation plus bounded implementation-coupled U03 proof.

**Smallest repair:** replace the retry-content equivalence check with a comparison that regards
native runtime type as part of exact content and preserves already-admitted representation
distinctions such as Decimal tuple/scale. Add a focused U03 regression for the concrete int/float
and/or Decimal-scale escape while preserving idempotency for separately reconstructed truly
identical content. Do not define provider duplicate/retransmission equivalence, broaden native value
validation, implement U04, or weaken any accepted U01/U02/U03 proof.

## Disposition

**`FAIL / RETURN_TO_WORKER`**.

U03 must not be promoted. U04 remains prohibited pending the bounded U03 repair and a fresh
independent U03 re-review.
