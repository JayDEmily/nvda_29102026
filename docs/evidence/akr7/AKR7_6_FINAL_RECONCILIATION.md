# AKR-7.6 final reconciliation evidence

## Status and scope

This record reconciles AKR-7.1 through AKR-7.5 with the current steady-state architecture authority before the external durable-closeout checkpoint and terminal verdict are issued.

It does not implement the external rehearsal brief and does not design the future brief-to-code continuation.

The terminal outcome is deliberately not asserted inside this pre-checkpoint repository record. Section 18 of `EXEC_PLAN.md` permits a terminal outcome only after the final committed state and its durable full-Git checkpoint have both been verified. The exact final commit, checkpoint archive identity, retained-file inventory and terminal outcome therefore belong to the external closeout receipt created after this record is committed and re-proved.

AKR-7 start commit:

```text
610a66365ce7ce981f6f6702c2062875fd1f4c3b
```

AKR-7.6 branch:

```text
work/akr-7.6-final-reconciliation
```

## Governing material and human trace

Before this reconciliation, the current `GUARDRAILS.md`, root `AGENTS.md`, `tests/AGENTS.override.md` and complete accepted `EXEC_PLAN.md` were reread. The AKR-7.1 through AKR-7.5 evidence records were reread together with the current normative architecture corpus under `docs/architecture/`.

The retained active control surface was then read across:

```text
.github/workflows/architecture-kernel.yml
.python-version
Makefile
README.md
pyproject.toml
uv.lock
config/architecture/*.yaml
config/proof/*.yaml
schemas/*.json
templates/*/*
src/nvda_desk/**/*.py
tools/*.py
tests/architecture/*.py
tests/bootstrap/*.py
```

Green commands are not used as substitutes for that semantic trace.

## Current structural state

The current architecture registries establish:

```text
P01 | protocol          | placeholder | no current runtime implementation
G01 | governance plane  | framework   | proof/promotion governance
A00 | application shell | bootstrap   | nvda_desk.composition
K01 | technical kernel  | placeholder | no current runtime implementation

modules: []
surfaces: []
implementation_allocations: []
retired_ids: []
declared_owner_edges: []
public_seam_exceptions: []
```

The active Python package contains only `nvda_desk.architecture` and `nvda_desk.composition`, with 13 Python source files in total. No product runtime owner is registered or packaged.

## Final-state assertion reconciliation

### 1. Active tree is behaviour-neutral — ESTABLISHED

The production registries have no runtime modules, architecture surfaces or durable implementation allocations. The active source package is limited to architecture enforcement plus the bootstrap composition shell. The AKR-7.5 semantic audit found no active product/Raw Signal runtime package, product entry point, domain production dependency or programme orchestration surface.

### 2. No product module is active — ESTABLISHED

`config/architecture/modules.yaml` contains `modules: []`. Aggregate structural validation reports zero active runtime modules. Physical package discovery contains no admitted product package.

### 3. No architecture surface is active unless separately admitted — ESTABLISHED

`config/architecture/surfaces.yaml` contains `surfaces: []`. No active surface is therefore admitted in the current state.

### 4. No upstream semantic-reconstruction process is contained in the kernel — ESTABLISHED

The upstream semantic-to-implementation-ready-brief methodology remains outside this repository. Active executable/configuration surfaces contain no M10/G1-G7/PMB worker/reviewer/orchestration implementation. The only M10 occurrence in the blocking test jurisdiction is a negative ingress fixture proving that upstream-only metadata is rejected by the generic ingress schema. `IMPLEMENTATION_AUTHORITY_INGRESS.md` explicitly requires upstream-methodology opacity.

### 5. No Raw Signal semantic programme is contained in the kernel — ESTABLISHED

Former programme prefixes `.agents/`, `.codex/`, `authority/`, `docs/governance/`, `docs/orchestration/`, `tests/gate0/` and `tests/governance/` have zero tracked files. Raw Signal authority/programme material carried out of the target tree remains recoverable through ordinary Git history rather than active in the kernel.

### 6. Exact external implementation-ready brief can enter through one generic ingress boundary — ESTABLISHED WITH AUTHORITY BOUNDARY

The generic ingress comprises:

```text
docs/architecture/IMPLEMENTATION_AUTHORITY_INGRESS.md
schemas/implementation_authority_binding.schema.json
templates/implementation_authority/binding.yaml.template
src/nvda_desk/architecture/implementation_authority.py
tools/validate_implementation_authority.py
tests/architecture/test_implementation_authority_ingress.py
```

It hashes brief bytes exactly as supplied, requires explicit external implementation acceptance, accepts only a bounded create/modify architectural projection, resolves create identifiers as non-durable candidates from current post-reset state and rejects upstream-only metadata. It neither copies nor reconstructs brief meaning.

AKR-6 rehearsal evidence records the accepted external brief identity as SHA-256 `938debe255d68668b0ae60f021d679fc8e3022be6eb050e7f3cd6112818fd342` and records successful execution through this repository-native ingress. The brief bytes themselves are intentionally not copied into the active tree, so this AKR-7 closeout does not re-assert their semantic content independently of the accepted AKR-6 human trace.

### 7. Architectural allocation remains open-ended — ESTABLISHED

`ARCHITECTURAL_OBJECT_TAXONOMY.md`, the identifier grammar and `identifiers.py` impose no numeric upper bound. Current executable candidate resolution over the empty post-reset allocation ledger produced, in request order:

```text
M00, M01, M02, A01, P02, K02, G02, S00
```

The admitted tests exercise the `M99 -> M100` transition and larger identifiers. Candidate resolution does not durably mutate the allocation ledger.

### 8. Future code is constrained by ownership, dependencies, public seams, lifecycle and proof — ESTABLISHED

The current law is owned by `OWNERSHIP_AND_COMPONENT_LAW.md`, `DEPENDENCY_LAWS.md`, `PUBLIC_SEAM_LAW.md`, `EXTENSION_AND_RETIREMENT_RULES.md` and `TEST_AND_PROMOTION_KERNEL.md`. The committed schemas, registry loader, dependency/public-seam analyser, activation readiness checks and proof/promotion registries provide the corresponding mechanical admission path. The blocking tests exercise lawful and unlawful representative cases rather than treating empty current registries as proof of future behaviour.

### 9. Typed public seams are mechanically checked — ESTABLISHED

`pyproject.toml` pins `mypy==1.20.1` as development-only proof tooling. The admitted static-type proof verifies the current source tree and separately demonstrates rejection of an incompatible call through a Python-visible public seam. AKR-7.2 and subsequent proof runs report no type errors in the 13 current source files.

### 10. Packaging is minimal and reproducible — ESTABLISHED SUBJECT TO FINAL-COMMIT REBUILD

The wheel target packages only `src/nvda_desk`. The observed wheel contains exactly 13 current Python source files plus distribution metadata/licence. The sdist is constrained by the explicit Hatch include list and its sole generated/non-repository file is `PKG-INFO`.

Two independent offline builds from the pre-closeout committed state were byte-identical for both wheel and sdist. The final committed state must be rebuilt after this evidence record is committed; only that post-commit result may close this assertion for the terminal verdict.

### 11. Historical product/domain work remains recoverable from Git history — ESTABLISHED WITH TWO DISTINCT HISTORY SCOPES

The final `DO_NOT_CARRY_FORWARD` set is 125 paths: the 122 canonical AKR-1 paths, the later-dispositioned vocabulary registry/schema, and the stale AKR-6 projection-attempt evidence. None is tracked in the target active tree. Every one has at least one content-bearing commit reachable from the current branch history.

The mature pre-reset product source lineage is intentionally separate from the reconstructed current repository. `docs/provenance/CLEAN_REPOSITORY_PROVENANCE.md` identifies preserved full-history commit `d24f9626a23b526384668b3cb26ee811b235eb5c` as challenge/provenance evidence rather than current product authority. The separately preserved architecture-reset full-history archive was inspected during this reconciliation: that commit exists, is an ancestor of the archive's reset HEAD, and contains 265 source paths including historical adapters, API, contracts and domain/runtime code. This external historical Git lineage is not imported into the current active repository or used as current authority.

### 12. Unresolved matters are explicit — ESTABLISHED

One AKR-7-specific unresolved limitation remains:

```text
implementation_allocations.implemented_on
```

The current schema/loader validates textual `YYYY-MM-DD` shape only and therefore accepts impossible calendar dates such as `2026-02-31`. Current governing/normative authority does not require calendar-validity, so AKR-7.2 correctly deferred rather than invented that stronger invariant.

The following are separately deferred by accepted scope and are not kernel-completion defects: design of the future implementation-writing methodology; implementation of a real coding brief; Raw Signal semantic admission; historical M16 re-admission; DMPV3 activation; state/transaction activation; product-module allocation/build order; PMB ordering; Python 3.14 migration; UUIDv7; deployment/production readiness.

## AKR-7 changes relative to start commit

Relative to AKR-7 start commit `610a66365ce7ce981f6f6702c2062875fd1f4c3b`, no runtime architecture implementation, ingress mechanism, schema, registry, dependency/toolchain declaration, lockfile, Makefile entry point or package source was functionally rewritten by AKR-7.

AKR-7 changed only:

- `EXEC_PLAN.md` progress recording;
- AKR-7 evidence records;
- target-tree carry-forward disposition of the 59 audit/reset/AKR-1 evidence paths already classified `DO_NOT_CARRY_FORWARD` by AKR-1.

The functional AKR-7.5 repair is ordinary Git history and preserves those 59 files in the parent commit.

## Dependency/toolchain disposition

AKR-7 introduced no dependency or toolchain change. The final declared toolchain remains Python `3.13.5`, `PyYAML==6.0.3` runtime, `pytest==9.0.3`, `ruff==0.15.11`, `mypy==1.20.1` development/proof, Hatchling `1.29.0` build backend and the admitted offline wheelhouse. The user explicitly excluded lint as an AKR-7 concern unless a changed surface or higher authority required it; AKR-7 did not change a lint-governed functional surface requiring a new lint acceptance criterion.

## Pre-final proof observations

From a clean AKR-7.5 committed state on this branch, the following were observed before committing this reconciliation record:

```text
sha256sum -c vendor/wheels/SHA256SUMS
  all 15 wheels: OK

uv lock --check --offline
  Resolved 13 packages

make validate PYTHON=/mnt/data/nvda_akr7_env/bin/python
  architecture objects: 4
  active runtime modules: 0
  implementation allocations: 0
  admitted test families: 11
  promotion sets: 1
  dependency/public-seam violations: 0
  PASS: structural architecture validation

python tools/check_dependencies.py
  PASS: dependency direction and cycle validation

python tools/check_public_seams.py
  PASS: public-seam validation

make typecheck PYTHON=/mnt/data/nvda_akr7_env/bin/python
  Success: no issues found in 13 source files

python -m pytest -q tests/architecture tests/bootstrap
  74 passed

python tools/run_promotion_gate.py --set architecture_kernel
  resolved test paths: 11
  74 passed

git diff --check
  no output

git fsck --full
  no output

git status --porcelain=v1
  no output
```

Two independent offline pre-final builds were byte-identical. Their wheel SHA-256 was `5bc7e5ad6fa7da1fdcc1cb171cbcb85e6ebb761ca25d21d2a14b77139f65d074`; the pre-final sdist SHA-256 was `c9654a707aa48921c3ac6f2cad9596f9e8ea53185422e424e10a3fc02a9498af`. The wheel contained 18 files total, including exactly 13 source files with zero source-byte mismatches. The sdist contained 89 files, with zero repository-backed byte mismatches and `PKG-INFO` as its sole generated path.

These pre-final results are not the terminal proof. The exact committed closeout state must be re-run, rebuilt and externally checkpointed before Section 18 is resolved.

## Operator-probe correction

One ad hoc candidate-resolution probe initially attempted to import a non-existent helper named `resolve_candidate_ids` and failed with `ImportError`. The source was reread immediately; the actual production helper is `resolve_candidate_identifiers`. The corrected probe produced the open-ended candidate sequence recorded above. This was an operator invocation error, not a repository failure or bypassed invariant.

## Terminal boundary

No Section 18 terminal outcome is claimed by this record itself. The terminal decision requires all of the following against the exact final committed repository state:

1. re-run the required structural/type/proof/promotion/integrity evidence;
2. rebuild and inspect two independent distributions and establish byte reproducibility;
3. generate exact retained and `DO_NOT_CARRY_FORWARD` inventories;
4. create a complete Git bundle/checkpoint;
5. verify the bundle, fresh-clone exact branch/HEAD/tree, clean clone and full Git integrity;
6. issue exactly one terminal outcome in the external closeout receipt and user report.
