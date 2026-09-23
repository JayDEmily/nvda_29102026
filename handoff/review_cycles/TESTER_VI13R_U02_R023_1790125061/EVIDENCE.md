# Review evidence

**Status:** `COMPLETE`

## Binding

- role: fresh independent Reviewer 023 / TESTER
- authorised scope: IWO-U02 only; U03 not assessed
- source transport SHA-256: `a9d0a8b302db9bad5812f8ffff43c97dfafa25b8a80e6d92f89d64d6a57c2522`
- exact source transport filename: `NVDA_G03_TESTER_VI13R_U02_R023_1790125061_FULL_GIT_20260923.tar(1).gz`
- transported repository HEAD before review: `828b04e48632f11317bed544fb795702af167dad`
- accepted/promoted U01 main: `b806447eb440a016826728af075e714beee23d31`
- frozen U02 production candidate: `a77dc596b7cbc3f248097df94d8dd0bef4491bec`
- candidate tree: `1b8672a851f63c1bab8da02fb75de8357e4fad3c`
- candidate parent: `b806447eb440a016826728af075e714beee23d31`
- candidate production path: `src/nvda_desk/raw_signal_occurrence_truth/api.py` only
- complete production diff SHA-256: `6770e58da79510651a7b704ca4e43dbfc3d3ede21da9d0455e419fd210d77a98`

## Governing material inspected

The review read the complete root `README.md`, `GUARDRAILS.md`, root `AGENTS.md`, current
`EXEC_PLAN.md`, `tests/AGENTS.override.md`, `handoff/control/CURRENT_STATE.md` and active cycle
`REQUEST.md` before substantive review. It then inspected the accepted IRB BC-003/004/010,
BICP owner/public-boundary law including `BICP-COMP-002`, `IF-ARCH-004` and `IA17-ARCH-005`, the
IWO U01/U02 definitions, `docs/architecture/PUBLIC_SEAM_LAW.md`, Worker U02 evidence, the complete
candidate production diff/current `api.py`, and the complete bounded U02 proof relevant to the
candidate. U03 implementation/acceptance was not assessed.

## Exact candidate validation

Independent candidate validation ran detached at exact commit `a77dc596b7cbc3f248097df94d8dd0bef4491bec` with Python 3.13.5,
pytest 9.0.3, mypy 1.20.1 and Ruff 0.15.11. Project-pinned tooling was provisioned outside the
repository.

Observed results:

- focused U01+U02 pytest: **326 passed**;
- strict positive mypy specimen: pass;
- strict negative mypy specimen: expected non-zero with all 15 intended negative sites diagnosed;
- source mypy: pass across 15 source files;
- Ruff over `src tests tools`: pass;
- product proof control: pass, six families and 13/13 obligations;
- architecture validator: pass with zero dependency/public-seam violations;
- dependency and public-seam checkers: pass;
- architecture/bootstrap: **74 passed**;
- architecture promotion: **74 passed**;
- `git diff --check`: pass;
- `git fsck --full --strict`: pass.

Those green results are retained as evidence for the propositions they exercise; they do not
negate the concrete implementation-coupled escape below.

## Semantic review

The candidate's ordinary command path correctly checks policy interval overlap and the bounded
proof establishes the intended U02 schedule/identity behaviour on that path. However, the realised
public object graph exposes the exact mutable semantic state that those checks are meant to own:
`_CommandsV1.__slots__ = ("_state",)` and `_ReadsV1.__slots__ = ("_state",)` store the same mutable
`_U02State`, whose policy/capture dictionaries are directly writable. `create_owner()` returns both
facets carrying that state.

### R023-U02-F001 — public facets expose mutable semantic owner state

**Disposition:** material U02 implementation/proof defect; `OPEN`.

**Accepted propositions defeated:**

- BICP `BICP-COMP-002`: runtime direction is A00 -> M00 and private-state bypass is prohibited;
- BICP `IF-ARCH-004` / `IA17-ARCH-005`: cross-owner use is through the M00-owned typed command/read
  boundary, with private-state/table/repository bypass prohibited;
- IWO-U01: M owns the semantic write boundary and exposes a typed public command/read seam;
- IRB BC-003 / IWO-U02: at most one capture-scope policy version may be active at an instant;
- the active Reviewer-023 request: preserve referential U02 reads and accepted U01 identity/seam law.

**Concrete failure path:** the review constructed two overlapping policies solely through public
U01 factories. Public `register_capture_scope_policy()` correctly rejected the second policy.
Nevertheless `owner.commands._state` and `owner.reads._state` were ordinary reachable attributes
and were the same mutable `_U02State`. Writing the rejected policy directly into its policy maps
then allowed the public capture command to realise a capture at 12:01 UTC under that overlapping
policy. Public reads returned the forged policy. Clearing the policy map through the read facet then
made a previously admitted policy disappear from referential readback.

This is not a hypothetical arbitrary-reflection attack. It uses the concrete state capability that
the production candidate places directly on the objects returned by the public factory. The
architecture checker remains green because it reasons about imports/declarations, while this escape
occurs through the realised object graph after lawful public construction.

**Smallest owning-layer repair:** keep the repair inside the U02 M-owner implementation plus the
bounded U02 implementation-coupled proof. Remove ordinary caller-reachable mutable semantic-state
capability from the public command/read facets so that policy/capture facts cannot be inserted,
replaced, cleared or otherwise mutated outside M-owned command semantics. Add a focused regression
that defeats the concrete observed bypass while preserving the existing public API meaning. Exact
private decomposition remains implementation freedom; do not weaken BC-003 overlap law, widen
semantics, begin U03, or change accepted U01 identity/time/null meaning.

## Disposition

**`FAIL / RETURN_TO_WORKER`**.

The green standard suite is insufficient for U02 acceptance because `R023-U02-F001` demonstrates a
material realised private-state bypass capable of violating the single-active-policy invariant and
referential U02 truth. U02 must not be promoted. U03 remains prohibited pending the bounded U02
repair and a fresh independent U02 re-review.
