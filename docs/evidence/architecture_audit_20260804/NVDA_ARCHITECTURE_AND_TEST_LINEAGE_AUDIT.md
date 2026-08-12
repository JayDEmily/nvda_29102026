# NVDA Architecture and Test-Lineage Audit

**Audit date:** 2026-08-04  
**Repository:** `Nvda11`  
**Branch:** `main`  
**Commit:** `d24f9626a23b526384668b3cb26ee811b235eb5c`  
**Repository state:** clean before and after audit  
**Overall verdict:** **FAIL_REPAIRABLE**

## 1. Direct outcome

The **architecture model is sound**: it correctly separates eighteen end-to-end architecture surfaces from sixteen semantic ownership modules, uses a modular-monolith target, distinguishes runtime, transaction, governance and test dependency planes, and treats physical package placement as subordinate to ownership and typed public seams.

The current repository is **not fully conformant to that model**. One confirmed post-law implementation defect and one corresponding proof defect remain:

1. canonical M05 introduced private M07 and M08 submodule imports after the public-seam prohibition;
2. the architecture readiness probe does not test that prohibition, so it returns PASS while the defect exists.

The test-admission and promotion-control machinery itself is unusually rigorous and mechanically coherent. The lineage is substantially recorded for Google, Microsoft and IBM, but AWS is absent from the admitted external-source register. This audit supplies the missing indexed AWS crosswalk without pretending that AWS originated the project-specific surfaces, modules or trading-domain allocations.

## 2. Scope and evidence actually inspected

Read in full:

- `00_TASK/PROJECT_EXECUTION_METHOD.md`
- `AGENTS.md`
- `PLANS.md`
- `ROADMAP_LEDGER.md`
- `tests/AGENTS.override.md`
- `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md`
- `docs/11.1_NATIVE_ARCHITECTURE_BLUEPRINT_WORKING.md`
- `docs/08_TESTING_AND_PROMOTION_CORE.md`
- `docs/08.1_TESTING_AND_PROMOTION_WORKING.md`
- `project_control/normative_authority_top_down_alignment/EXTERNAL_SOURCE_DECISIONS.md`
- public `__init__.py` APIs for every physical canonical `mXX` package
- proof-authority, proof-block, promotion-gate and foundation-readiness control scripts relevant to the audit findings
- source and Git history for every reported private-import defect

Structural inventory covered all Python imports under `src/nvda_desk`, all 203 physical tier test paths, all 201 test families and all 73 proof blocks. Selected implementation files were read where required to adjudicate ownership-boundary findings. This was not a semantic review of every runtime algorithm or every test assertion.

Commands executed and retained in `evidence/`:

- `make scaffold-check` — returned 0
- `python3.13 scripts/proof_authority.py --check --json` — returned PASS
- `python3.13 scripts/run_proof_block.py --check-all` — returned PASS for 73 block definitions
- `python3.13 scripts/run_promotion_gate.py --set alpha_current --check-only` — resolved 19 families / 21 paths; tests not executed
- `python3.13 scripts/foundation_readiness_probe.py --output ...` — returned PASS with 260 modules, zero exact module cycles and zero declared dependency violations

No repository file was changed.

## 3. Audited architecture framework

### 3.1 Three distinct maps

| Map | Count | Meaning | What it is not |
|---|---:|---|---|
| Architecture surfaces | 18 | End-to-end responsibility and assurance planes, including cross-cutting persistence, proof and vocabulary | Not one package per surface |
| Ownership modules | 16 (`M00`–`M15`) | Semantic code-capability owners inside the modular monolith | Not a literal runtime call sequence and not identical to surfaces |
| Physical packages/components | Current implementation-specific | Concrete package, adapter, compatibility and governance locations | Not ownership proof by naming or location |

The many-to-many distinction is explicit at `docs/11.1_NATIVE_ARCHITECTURE_BLUEPRINT_WORKING.md:150-173`. The complete audited crosswalk is in `ARCHITECTURE_SURFACE_INDEX.csv` and `OWNERSHIP_MODULE_INDEX.csv`.

### 3.2 Architecture judgement

**Pass:**

- The modular monolith is a defensible target for the alpha system; the blueprint explicitly rejects automatic microservice decomposition (`docs/11.1_NATIVE_ARCHITECTURE_BLUEPRINT_WORKING.md:87`, `150-173`).
- The owner graph is explicit and acyclic at exact Python-module granularity. The current readiness probe returned zero cycles, syntax errors, unresolved internal imports and unbounded dependency violations.
- M04's lack of a physical package is lawful, not missing architecture: the blueprint permits M04 to remain a logical owner until a real change requires a clearer boundary (`docs/11.1_NATIVE_ARCHITECTURE_BLUEPRINT_WORKING.md:459-476`).
- M14 and M15 are continuous governance planes, not runtime services (`docs/11.1_NATIVE_ARCHITECTURE_BLUEPRINT_WORKING.md:443-457`).

**Repair required:**

- `docs/11.1_NATIVE_ARCHITECTURE_BLUEPRINT_WORKING.md:443-446` requires cross-module use to enter through the owner's public API or an accepted evidence/transaction port.
- `src/nvda_desk/m05_serial_cognition/composition.py:30-40` imports four M07/M08 contract types from private submodules.
- Those imports were introduced in commit `7ff10db` after the rule was introduced in commit `3876f17`; see `evidence/git_lineage_private_import_violation.txt`.
- The relevant types are not exported by `src/nvda_desk/m07_coefficient_modifier_authority/__init__.py:1-16` or `src/nvda_desk/m08_playbook_catalogue/__init__.py:1-10`.

This is an architecture-boundary defect, not evidence that the M05 behaviour is functionally wrong.

### 3.3 Coarse package tangles versus exact import cycles

A coarse package aggregation produces two mutual-dependency tangles:

- `contracts`, `packets`, `preparation`
- `cognition`, `domain`

The exact Python module graph remains acyclic. The correct interpretation is therefore **compatibility/responsibility tangle**, not a runtime circular-import failure. The package evidence is retained in `evidence/static_package_dependency_graph.json` and `evidence/static_package_import_evidence.tsv`.

## 4. Test and promotion framework audit

### 4.1 Current control model

The test system has two independent axes:

1. **Tier** — proof class (`A`, `B`, `C`);
2. **Lifecycle** — whether that family is current blocking, current nonblocking, historical, expected-red or superseded compatibility.

Current inventory:

| Tier/lifecycle | Families | Paths |
|---|---:|---:|
| Tier A / current blocking | 19 | 21 |
| Tier A / all other lifecycles | 165 | 165 |
| Tier B / all lifecycles | 16 | 16 |
| Tier C / current nonblocking | 1 | 1 |
| **Total** | **201** | **203** |

Therefore, saying “186 Tier A tests” does **not** mean 186 current blockers. The authoritative current claim is the 19-family, 21-path `alpha_current` set.

### 4.2 What the machinery correctly enforces

`proof_authority.py` enforces:

- every physical test path has exactly one admission;
- admitted paths exist and physical unadmitted/stale paths fail;
- family tier matches physical tier;
- every current-blocking family has proposition identifiers;
- proof-block executable path membership equals registry-derived family membership;
- promotion sets contain only current-blocking families;
- `alpha_current` equals the complete current-blocking family set.

The PR workflow installs the locked environment, runs non-executing controls, then executes `make promotion-gate` (`.github/workflows/pr-preflight.yml:50-63`). This rules out the earlier concern that CI only checked membership.

### 4.3 Proof gap

The current architecture probe checks exact module cycles and owner-direction, but its conformance function accepts any import within an allowed owner edge or prefix (`scripts/foundation_readiness_probe.py:245-282`). It does not determine whether the target is the owner package's public export.

Consequently:

- the probe returned PASS;
- the confirmed M05 private imports remained undetected;
- no `alpha_current` family is traced to the section 11.12.2 public-export proposition (`evidence/alpha_current_family_proposition_index.tsv`).

The test framework is therefore strong at **admission and execution authority**, but incomplete at one material **architecture proposition**.

## 5. Lineage judgement

### 5.1 What is directly recorded in the repository

The admitted external-source register already records:

- Google modular design and clear interfaces;
- Microsoft dependency inversion, composition roots, anti-corruption layers, event/replay guidance and testing strategy;
- IBM module partitioning, business rules, lineage, requirements-based testing and terminology governance;
- additional NIST, CloudEvents and W3C sources where more appropriate than the four vendors.

### 5.2 AWS gap

The admitted 432-line source-decision register contains no AWS/Amazon Web Services reference. That is a lineage-index gap, not proof that AWS had no influence.

Official AWS guidance closely corroborates:

- bounded-context/subdomain decomposition;
- hexagonal ports and adapters;
- anti-corruption layers;
- incremental strangler-style migration;
- layered CI testing and quality gates.

These are recorded as **AWS_CORROBORATING** or **AWS_ANALOGUE**, not as direct project authority. The exact M00–M15 allocation, eighteen surfaces, dependency planes, DMPV3, serial/parallel trading topology and tier/lifecycle control model remain project-specific.

See `ARCHITECTURE_LINEAGE_INDEX.csv` and `TEST_LINEAGE_INDEX.csv`.

## 6. Recommended repair path

One bounded sequence closes the material gaps without redesigning the architecture:

1. **Repair M05 public seams:** export the genuinely shared M07/M08 carrier types through intentional owner APIs, or narrow the cross-owner contracts; remove M05 private-submodule imports.
2. **Promote the public-seam law into proof:** add one registry-admitted current-blocking architecture family that rejects newly introduced private cross-owner imports and recognises only explicit evidence/transaction-port exceptions.
3. **Reconcile the blueprint status row:** update the 5.17 status note so declared environment and aggregate promotion are no longer described as incomplete; retain only the architecture-level gap until step 2 passes.
4. **Admit the lineage indexes:** add AWS as corroborating lineage with project adaptation and rejected-interpretation notes; keep project-specific features labelled as such.

No module or surface reallocation is required.

## 7. Validation status and unknowns

| Item | Status |
|---|---|
| Repository identity and clean state | Proven by retained Git output |
| Required normative/test-control reading | Completed for the files listed in section 2 |
| Physical test admission consistency | Command returned PASS |
| Proof-block definition consistency | Command returned PASS |
| `alpha_current` membership resolution | Command returned PASS; tests not executed |
| Exact module graph/readiness probe | Command returned PASS |
| Full Tier A/B/C functional greenness on current checkout | **Unknown — not executed in this audit** |
| Runtime semantic correctness of every surface | **Unknown — outside this structural audit** |
| Live trading, production durability, profitability or operational commissioning | **Not claimed** |

## 8. Artefact index

- `ARCHITECTURE_SURFACE_INDEX.csv` — surfaces, primary modules, physical loci and lineage IDs
- `OWNERSHIP_MODULE_INDEX.csv` — M00–M15 ownership and physical state
- `ARCHITECTURE_LINEAGE_INDEX.csv` — feature-level source lineage
- `TEST_FRAMEWORK_INDEX.csv` — exact tier/lifecycle population
- `TEST_LINEAGE_INDEX.csv` — test-framework source lineage
- `DEFECT_AND_FINDING_REGISTER.csv` — evidence-backed findings and dispositions
- `evidence/` — command outputs, graph inventories, Git lineage and hashes
