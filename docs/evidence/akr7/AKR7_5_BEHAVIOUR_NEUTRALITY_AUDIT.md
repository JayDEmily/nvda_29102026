# AKR-7.5 — exclusion and behaviour-neutrality audit

Status: NON-NORMATIVE EXECUTION EVIDENCE.

## Scope and authority

This leaf audits the committed active tree and the actual AKR-7.4 distribution artefacts against the accepted AKR-7.5 exclusion/behaviour-neutrality propositions. It does not implement the external rehearsal brief, admit a product module, or design the future brief-to-code continuation.

The governing `GUARDRAILS.md`, root `AGENTS.md`, accepted `EXEC_PLAN.md`, current registries, packaging authority, active architecture law, retained historical-status documents, source/tool surfaces and implementation-authority ingress path were read before acceptance. `tests/AGENTS.override.md` remained applicable to the re-proof population.

## First observed defect and bounded repair

The canonical AKR-1 inventory classified 122 paths as `DO_NOT_CARRY_FORWARD`. AKR-2 intentionally carried only the 63 programme/domain-specific paths out of the active tree while retaining 57 reset/audit evidence paths plus the two AKR-1 evidence files for later reconciliation. At AKR-7.5 entry those remaining 59 canonical `DO_NOT_CARRY_FORWARD` paths were still tracked.

The affected semantic records identify the retained material as historical audit/reset evidence rather than current kernel authority. Under the guardrail carry-forward law and the accepted target-inventory authority, those 59 paths were carried out of the target active tree by ordinary Git commit `65f55f0d7bdcd3bbaa232bf325adc33c069ca7b2`. No history was rewritten or pruned. All 59 paths were proved readable from the immediate parent tree before and after the transition. The staged change contained exactly 59 deletions and no other path mutation; `git diff --cached --check` was clean.

After that commit, none of the 122 canonical AKR-1 `DO_NOT_CARRY_FORWARD` paths remained tracked. The target tree had 120 tracked files before this AKR-7.5 evidence/progress record was added.

## Active-tree semantic inspection

The repaired committed target tree was inspected by path, configuration and content rather than by filename absence alone.

### Active architecture state

Current registries state:

```text
modules:                   []
surfaces:                  []
implementation_allocations: []
P01: placeholder
G01: framework
A00: bootstrap
K01: placeholder
retired IDs: none
owner dependency edges: none
public-seam exceptions: none
```

The four retained objects are structural foundation identities. None is an admitted product runtime module. `A00` is the minimal composition shell, `G01` is proof/promotion framework state, and `P01`/`K01` remain non-active placeholders.

### Executable/source surface

The active Python package contains exactly 13 source files, all beneath `nvda_desk.architecture`, `nvda_desk.composition`, or the package root. There is no additional product/domain package under `src/nvda_desk`.

The source and tool paths were human-read. Their executable responsibilities are registry/schema loading, identifier/candidate allocation, dependency/public-seam analysis, proof/promotion control, implementation-authority byte/target validation, aggregate structural validation and minimal composition. No source file implements Raw Signal, trading, market-data, portfolio, execution or another NVIDIA business capability. No source/tool path implements an upstream semantic-reconstruction or semantic-to-brief process.

The active test population contains exactly 11 Python files and is confined to `tests/architecture` and `tests/bootstrap`. The retained `M16` text occurs in a negative implementation-authority fixture that proves a caller cannot select a historical numeric create identity; it is not an admitted module or product behaviour test.

Former programme/control prefixes are absent from the repaired tracked tree: `.agents/`, `.codex/`, `authority/`, `docs/governance/`, `docs/orchestration/`, `tests/gate0/`, `tests/governance/`, and former programme/governance tool prefixes all resolve to zero tracked paths.

### Dependencies and command surfaces

`pyproject.toml` declares exactly one production dependency, `PyYAML==6.0.3`. `pytest`, `ruff` and `mypy` are development-only dependencies. No historical production/domain dependency is declared.

The five installed console scripts are architecture controls only:

```text
nvda-validate-architecture
nvda-check-dependencies
nvda-check-public-seams
nvda-promotion-gate
nvda-validate-implementation-authority
```

There is no product/trading/operational console entry point.

### Semantic-to-brief exclusion and ingress boundary

`IMPLEMENTATION_AUTHORITY_INGRESS.md`, `templates/implementation_authority/binding.yaml.template`, `schemas/implementation_authority_binding.schema.json`, and `src/nvda_desk/architecture/implementation_authority.py` were read together.

The executable ingress accepts exact brief bytes by SHA-256 plus an externally supplied accepted-for-implementation reference and a bounded create/modify structural projection. Create requests supply category plus responsibility name; candidate numeric identity is mechanically resolved from current structural/allocation state. The schema has no M10, G1-G7, PMB, semantic-candidate, source-corpus, worker/reviewer or upstream methodology fields. The code validates bytes and architecture state; it does not parse or reconstruct upstream source meaning.

The retained AKR-6 records are explicitly marked `NON-NORMATIVE REHEARSAL EVIDENCE`; they document the bounded exact-brief rehearsal and stop before business code, durable allocation or composition. Their domain terms therefore remain evidence of the rehearsal rather than active programme authority or runtime implementation.

### Historical material still intentionally present

`ARCHITECTURE_KERNEL.md` explicitly states that `ARCHITECTURE_KERNEL_RESET_BRIEF.md` and the September conformance ADR are historical evidence explaining how the steady-state kernel was reached, not owners of current steady-state law. The reset brief carries a prominent historical/non-governing banner. `docs/history/AKR5_BLOCKER_STATIC_TYPE_CHECKER_20260909.md` and `docs/history/LEGACY_IDENTIFIER_CROSSWALK.md` likewise identify themselves as historical evidence. Domain/former-identifier terms in these files do not activate registry state, package code or proof admission.

## Actual AKR-7.4 built artefact audit

The exact AKR-7.4 artefacts audited were:

```text
nvda_architecture_kernel-0.1.0-py3-none-any.whl
SHA-256 5bc7e5ad6fa7da1fdcc1cb171cbcb85e6ebb761ca25d21d2a14b77139f65d074

nvda_architecture_kernel-0.1.0.tar.gz
SHA-256 2d9596841554a592f575c02bdff523aee6e897fa8e07ca4218bcd7690ebaea30
```

The wheel contains 18 files: exactly 13 current `nvda_desk` Python source files plus distribution metadata/licence. Its Python inventory exactly matches the current source inventory and every source byte matches. Text search found no Raw Signal/former-allocation/upstream-semantic-to-brief/product-domain term in the wheel source. Its installed metadata declares only `pyyaml==6.0.3` at runtime and the same five architecture-only console scripts listed above.

The sdist contains 89 files. It contains no `authority/`, `.agents/`, `.codex/`, programme-governance test/tool path or active programme/orchestration path. Relative to the repaired tree, every repository-backed sdist byte still matches except `EXEC_PLAN.md`; that expected delta exists because the artefact was built from the clean AKR-7.3 committed state during AKR-7.4, before the AKR-7.4 closeout/progress text was appended to `EXEC_PLAN.md`. The only non-repository generated sdist file is `PKG-INFO`. The AKR-7.5 carry-forward repair removed only `docs/evidence/**` paths, which are not selected by the sdist packaging declaration.

Domain/former-programme terms found in the sdist are confined to their inspected roles: current exclusion/planning text in `EXEC_PLAN.md`, the explicitly historical reset/conformance/crosswalk documents, and the negative `M16` ingress test fixture. No product/domain implementation, operational entry point or upstream semantic-reconstruction machinery is present in the distributable.

## Re-proof after repair

Proof was run from clean repair commit `65f55f0d7bdcd3bbaa232bf325adc33c069ca7b2` using the reconstructed CPython 3.13.5 environment:

```text
PYTHONPATH=src /mnt/data/nvda_akr7_env/bin/python tools/validate_architecture.py
/mnt/data/nvda_akr7_env/bin/python -m mypy src
PYTHONPATH=src /mnt/data/nvda_akr7_env/bin/python -m pytest tests/architecture tests/bootstrap -q
PYTHONPATH=src /mnt/data/nvda_akr7_env/bin/python tools/run_promotion_gate.py --set architecture_kernel
```

Observed results:

```text
architecture objects: 4
active runtime modules: 0
implementation allocations: 0
admitted test families: 11
promotion sets: 1
dependency/public-seam violations: 0
mypy: Success: no issues found in 13 source files
architecture/bootstrap proof: 74 passed
promotion resolved test paths: 11
promotion proof: 74 passed
worktree before/after promotion: clean
```

Lint was not run: this leaf changed only historical/evidence carry-forward state, and current user authority excludes lint from AKR-7 unless a changed surface or higher authority specifically requires it.

## Acceptance boundary

The repaired active tree and the actual AKR-7.4 distributable contain no active historical product module/allocation, Raw Signal implementation or semantic programme, Raw Signal worker/reviewer/orchestration machinery, removed-programme behavioural proof, product console entry point, domain production dependency, or duplicated upstream semantic-to-brief methodology. Current module, surface and durable implementation-allocation state remains empty.

This establishes AKR-7.5's exclusion/behaviour-neutrality proposition only. It does not implement a product capability, admit the external rehearsal brief, or establish the terminal AKR-7 outcome; final assertions, reproducibility from the final committed state, repository integrity and the durable closeout checkpoint remain AKR-7.6 work.
