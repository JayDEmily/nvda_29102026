# tests/AGENTS.override.md

## Purpose

This file governs any task that reads, edits, retires, restores, or creates files under `tests/`.

Greenness is not the target. Truthful protection of real invariants is the target.

This file is subordinate to the current user instruction, repo-root `AGENTS.md`, the active approved `EXEC_PLAN.md`, `PLANS.md`, and the repo normative documents governing the selected subject area, including `docs/08_TESTING_AND_PROMOTION_CORE.md` for test, proof, promotion, demotion, receipt, checkpoint, and docstring-proof law. It provides subtree-specific constraints for work under `tests/`.

## Required read sequence for test work

Before touching a file under `tests/`, read in this order:

1. repo-root `AGENTS.md`, `PLANS.md` and `ROADMAP_LEDGER.md`;
2. the active ExecPlan, when one is active;
3. every complete normative document named by that ExecPlan, in full and in its stated order, or the exact complete set recorded under direct user authority when no ExecPlan is active;
4. `config/retained_test_registry.yaml`;
5. `config/proof_blocks.yaml`;
6. this file;
7. only then the specific native test family, legacy test source, runtime code, fixtures and retained artefacts in scope.

This override does not independently choose the normative document set. If test work exposes a missing testing, vocabulary, architecture or domain authority family, amend the governing plan or manifest and complete that read before continuing.

## Authority hierarchy for tests

For test work, the governing hierarchy is:

1. official source material when the task depends on external language, API, package, platform, or tool behaviour
2. repo-root `AGENTS.md` and the numbered normative/control stack
3. vocabulary governance for durable terms
4. `docs/08_TESTING_AND_PROMOTION_CORE.md` for tier, proof, promotion, demotion, receipt, checkpoint, and docstring obligations
5. `config/retained_test_registry.yaml` and `config/proof_blocks.yaml`
6. admitted tests and governed proof artefacts
7. runtime code as the observed implementation surface
8. docstrings as owned explanatory surfaces

Runtime code is never permitted to override normative doctrine, vocabulary governance, admitted proof, or retained-test registry authority.

## Admission and registry rule

No native pytest file is admitted by folder placement alone.

A file under `tests/tier_a`, `tests/tier_b`, or `tests/tier_c` is governed only through explicit registry, proof-block, or active-pack authority.

New tests, promoted tests, demoted tests, archived tests, and migrated tests must update the required receipt surfaces before promotion or completion is claimed.

## Invariant-first rule

Before changing a failing, migrating, or retained test, identify:

1. the invariant the test is intended to protect
2. whether that invariant is still live in the clean rebuild
3. whether the truthful action is re-author, defer, archive, demote, promote, or block

## Source-truth rule

Legacy tests under `legacy_import/tests/` are source evidence only.

A legacy test file is not native authority.

## Code-and-docstring reread rule

Before re-authoring, admitting, promoting, demoting, or materially relying on a native test family:

1. reread the runtime code under test
2. reread the docstrings on the owned runtime surface
3. compare the docstrings to the runtime code
4. compare the test assertions to the governing invariant and runtime code
5. record any material divergence in the relevant receipt surface

If a docstring and runtime code diverge, runtime code is the observed implementation surface only.

That observation does not make runtime code authoritative over normative doctrine, vocabulary governance, admitted tests, or retained-test registry authority.

A proof claim is incomplete until the divergence is declared and the governed follow-up is recorded.
