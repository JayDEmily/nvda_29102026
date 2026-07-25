# Canonical Project Manager Validation Log

## PM-000 — Programme-control activation

### Baseline evidence

| Check | Observed result |
|---|---|
| Governed archive SHA-256 | `5a75fb237232d9b6a8bc804a81c6bc62c9ad7a719fee57346d632b39a060857c` |
| Baseline branch | `work/NVIDIA_2026_normative_authority_top_down_alignment_20260717` |
| Baseline commit | `f7bd3f46862fe9b33340f3f13951518795724fe7` |
| Baseline commit timestamp | `2026-07-20T08:17:46Z` |
| Baseline subject | `Decide bounded Gate D readiness` |
| Baseline status | Clean before PM branch creation |
| Baseline tracked files | 1,047 |
| PM working branch | `work/NVIDIA_2026_canonical_project_manager_20260720` |

### Read and inventory checks

- Root and subtree instruction files were discovered and semantically read in full.
- Root control placeholders/tombstone, the prior active plan, routing index, numbered normative corpus, vocabulary authority, normative-completion decisions N-01 through N-09, proof registers, all thirty-three proof-envelope files, and Gate D readiness evidence were semantically read in full.
- All 166 Tier A and all 13 Tier B Python test files were semantically read in full, together with `tests/AGENTS.override.md`, test support files, fixtures, the retained registry, proof blocks, and exercised runtime/configuration owners.
- All 203 Python files under `src/nvda_desk` were semantically read in full.
- Physical-to-retained inventory comparison produced 166/120 Tier A with 46 unlisted physical files and 13/13 Tier B with no difference.
- Live vocabulary recount produced 46 human headings, 87 generated entries, 26 normalised matches, 20 human-only labels, and 61 generated-only labels.
- Historical Git object verification at `f26b09f` reproduced the four Atlas source hashes and the eighteen-surface/1,716-record manifest counts recorded in the retained vocabulary slice.
- No 287-row cohort-register artefact was found in the supplied archives, live tree, or inspected reachable named paths. This remains a blocker rather than a negative proof that it never existed.

### Pytest environment attempts

1. `env PYTHONPATH=src python -m pytest ...` did not execute tests because the available Python 3.12 runtime had no `pytest` module.
2. `uv run --frozen pytest ...` could not initialise its default cache because `/root/.cache/uv` was read-only.
3. With cache and environment paths redirected to `/tmp`, the available Python 3.12 interpreter was correctly rejected because `pyproject.toml` requires Python 3.13.5.
4. `uv run --python 3.13.5 --frozen pytest ...` installed/selected CPython 3.13.5 and began locked environment creation, then failed fetching `pyyaml==6.0.3` from the package mirror with HTTP 502 after retries.
5. A fallback attempt to install `pytest` into a temporary Python 3.12 target failed because the package index proxy was unreachable.

Result: no pytest command is reported passed or failed at product level. Behavioural validation is `blocked_environment`; PM-000 uses only control/static/Git checks. The locked environment must be retried before a behavioural unit can be accepted.

### PM-000 control validation

| Check | Result |
|---|---|
| Current full-read manifest | 539 data rows; 539 unique paths |
| Current repo hashes in manifest | 534 repo paths checked; zero mismatches |
| External attachment records | 5 exact supplied SHA-256 records |
| Manifest status accounting | 531 `read_full_current`; 5 `authored_and_reread_full`; 2 binary archive inventories; 1 ten-record Atlas semantic projection |
| Required control files | 6/6 present and non-empty |
| Changed-path boundary | Only `PLANS.md`, `ROADMAP_LEDGER_V2.md`, and `project_control/canonical_project_manager/**` |
| Forbidden normative/test/source/config/generated mutation | None |
| Fixed implementation order | 33 unique units; exact canonical sequence |
| Closed-unit proof-return order | 11 unique units; exact canonical sequence |
| Physical test recount | Tier A 166, Tier B 13 |
| Retained reconciliation recount | Tier A 120 with 46 physical-only; Tier B 13 with zero difference |
| Vocabulary recount | 46 human, 87 generated, 26 matches, 20 human-only, 61 generated-only |
| Atlas vocabulary slice | 10 records; source metadata says 1,716/1,716 with matching historical object hashes |
| `make scaffold-check` | Passed: `repo scaffold present` |
| `python scripts/run_proof_block.py --check-all` | Passed: 51 proof blocks validated without executing them |
| PM-000 composite control validator | Passed: manifest 539, implementation order 33, closed order 11, Tier A 166/120, Tier B 13/13, vocabulary 46/87, Atlas slice 10 |
| `git diff --check` | Passed with no output |

The control files were reread in full after creation. PM-000 is accepted as a control checkpoint once the bounded commit is created and the resulting clean checkpoint/archive hash is reported. This acceptance does not open PM-001, P1 semantic mutation, test mutation, or Gate D implementation.

## 2026-07-25 — Canonical Gate C completion protocol freeze

### Outcome

- Parent programme plan remains `project_control/canonical_project_manager/EXEC_PLAN.md`.
- New frozen subordinate protocol: `project_control/canonical_project_manager/GATE_C_COMPLETION_PROTOCOL.md`.
- Live position pointer updated: `ROADMAP_LEDGER_V2.md`.
- Prior one-file P2 plan explicitly marked superseded for execution and retained as historical evidence.
- `CURRENT_PROJECT_STATE.md` marked as a historical assembly snapshot.
- Historical Gate A–D progress ledger preserved with an append-only continuation entry.
- P2 remains incomplete; P3, P4 and Gate D remain closed.
- No normative document, test, production source, configuration, fixture or generated trading artefact was authorised for mutation by this control leaf.

### Control validation

| Check | Result |
|---|---|
| Canonical checklist IDs | PASS — 56 unique checklist IDs |
| Frozen checked state | PASS — only `GC-000` through `GC-009` checked |
| P3 unit order | PASS — `D-009, D-012, D-015, D-010, D-016, D-033, D-017, D-031, D-021, D-048, D-041` |
| Referenced repository paths | PASS — all required internal control/evidence paths present |
| P2 standing ledger | PASS — 179 rows and 179 unique test paths |
| Old P2 plan status | PASS — explicitly superseded for execution and no worker dispatch |
| Programme/roadmap linkage | PASS — parent ExecPlan and live roadmap both reference the frozen Gate C protocol |
| Gate state | PASS — P2 incomplete; P3, P4 and Gate D closed |
| `git diff --check` | PASS |
| `make scaffold-check` | PASS — `repo scaffold present` |
| `python scripts/run_proof_block.py --check-all` | PASS — 51 proof blocks structurally validated |
| Forbidden mutation scan | PASS — no `src/`, `tests/`, `config/`, `schemas/`, `fixtures/`, `data/` or numbered normative-document change |

Structural validation does not establish semantic acceptance of P2, P3, P4 or Gate D.

## 2026-07-25 13:04:09 AEST — Sole Gate C checklist and main checkpoint

### Outcome

- `project_control/canonical_project_manager/GATE_C_COMPLETION_PROTOCOL.md` now states explicitly that it is the sole operational checklist for the remaining Gate C work.
- `project_control/canonical_project_manager/EXEC_PLAN.md` remains the parent programme controller.
- `ROADMAP_LEDGER_V2.md` remains the current-position pointer.
- Checkpoints, ledgers, receipts, reports, manifests and archives are supporting evidence only and do not create parallel plans or checklists.
- The checkpoint branch is `main`.
- P2 remains incomplete; P3, P4 and Gate D remain closed.

### Validation

| Check | Result |
|---|---|
| Canonical checklist IDs | PASS — 56 unique IDs |
| Frozen checked state | PASS — only `GC-000` through `GC-009` checked |
| P3 unit order | PASS — eleven units in canonical dependency-safe order |
| P2 standing ledger | PASS — 179 rows and 179 unique test paths |
| Sole-checklist routing | PASS — protocol, parent ExecPlan and live roadmap agree |
| Main ancestry before promotion | PASS — prior `main` is an ancestor of the checkpoint commit chain |
| Forbidden mutation scan | PASS — no `src/`, `tests/`, `config/`, `schemas/`, `fixtures/`, `data/` or numbered normative-document change |
| `git diff --check` | PASS |
| `make scaffold-check` | PASS — `repo scaffold present` |
| `python scripts/run_proof_block.py --check-all` | PASS — 51 proof blocks structurally validated |

This is a control/checkpoint validation. It does not accept P2, open P3/P4, or authorise Gate D.
