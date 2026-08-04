# 2026-04-28 Active Codebase Alignment Repair Tranche

Status: closed
Tranche ID: active_codebase_alignment_repair_tranche
Blueprint surface: testing, proof, and checkpoint surfaces / repo process truth
Target owner: retained-test authority and tranche-law route surfaces

## 1. Purpose

Repair the repo truth surfaces after the reviewed downstream capital deployment authority pilot tranche before any new Atlas blueprint-surface tranche is opened.

This tranche is deliberately small. It reconciles route truth, Tier A registry inventory truth, and shallow-proof inventory. It does not refactor runtime code or native tests.

## 2. Plan

Execute the following leaves in order:

| Order | Leaf | Purpose | Mutable scope |
|---:|---|---|---|
| 1 | `ACR-L01` | Open and route the active-codebase alignment repair tranche. | route files, pack file, brief, ledger |
| 2 | `ACR-L02` | Reconcile Tier A registry inventory truth. | `config/retained_test_registry.yaml` |
| 3 | `ACR-L03` | Inventory shallow / presence-only Tier A proof files without refactor. | `var/audit/ledgers/active_codebase_alignment_repair_presence_inventory.json` |
| 4 | `ACR-L04` | Mandatory closeout. | brief, ledger |

## 3. Scope boundary

This tranche may touch only:

- `AGENTS.md`
- `docs/06.1_PROCESS_AND_TRANCHE_LAW_WORKING.md`
- `intent_migration/active_codebase_alignment_repair/AGENTS.override.md`
- `config/retained_test_registry.yaml`
- `var/audit/briefs/2026-04-28_ACTIVE_CODEBASE_ALIGNMENT_REPAIR_TRANCHE.md`
- `var/audit/ledgers/active_codebase_alignment_repair_tranche_ledger.json`
- `var/audit/ledgers/active_codebase_alignment_repair_tranche_ledger.schema.json`
- `var/audit/ledgers/active_codebase_alignment_repair_presence_inventory.json`

This tranche must not touch:

- `src/**`
- `tests/**`
- a new Atlas blueprint-surface tranche
- the full Atlas evidence bundle as execution scope

## 4. Authority and evidence read

The following in-scope surfaces were read for this tranche:

- `AGENTS.md`
- `docs/06.1_PROCESS_AND_TRANCHE_LAW_WORKING.md`
- `docs/06_PROCESS_AND_TRANCHE_LAW_CORE.md`
- `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md`
- `config/retained_test_registry.yaml`
- `var/audit/briefs/2026-04-28_DOWNSTREAM_CAPITAL_DEPLOYMENT_AUTHORITY_PILOT_TRANCHE.md`
- `var/audit/ledgers/downstream_capital_deployment_authority_pilot_tranche_ledger.json`

## 5. Findings before repair

Static Tier A registry inventory found:

- `67` native Tier A pytest files under `tests/tier_a/**/test_*.py`
- `54` paths registered in `retained_seed_tier_a`
- `5` existing Tier A files registered outside `retained_seed_tier_a`
- `8` existing Tier A files with no explicit registry record before this repair tranche

Static proof-shape inventory found:

- `26` Tier A files with no `assert` statement or assert-like call
- `48` Tier A files using presence / structure probes such as `hasattr`, `getattr`, `isinstance`, `issubclass`, or `callable`
- `14` Tier A files with at least one `assert` statement or assert-like call

These counts are inventory evidence only. They do not prove behavioural adequacy or inadequacy by themselves.

## 6. Leaf execution record

| Leaf | Status | Evidence |
|---|---|---|
| `ACR-L01` | closed | Route files now admit `intent_migration/active_codebase_alignment_repair/AGENTS.override.md` as the active pack and retain the downstream pilot as closed evidence. |
| `ACR-L02` | closed | `config/retained_test_registry.yaml` now includes `tier_a_registry_reconciliation_inventory` with explicit status for all `67` Tier A pytest files. |
| `ACR-L03` | closed | `var/audit/ledgers/active_codebase_alignment_repair_presence_inventory.json` records static proof-shape inventory for all `67` Tier A pytest files. |
| `ACR-L04` | closed | This brief and the child ledger record the tranche as closed with carry-forward blockers. |

## 7. Verification

Completed in this pass:

- Python 3.13.5 available.
- Repo extracted from `repo_bridge_downstream_capital_pilot_leaves_reviewed_2026-04-28.zip`.
- `.git` root identified at `stage2_route_fix_1777119453`.
- `config/retained_test_registry.yaml` parsed as YAML after repair.
- `var/audit/ledgers/active_codebase_alignment_repair_presence_inventory.json` parsed as JSON after repair.
- `var/audit/ledgers/active_codebase_alignment_repair_tranche_ledger.json` parsed as JSON after repair.
- `var/audit/ledgers/active_codebase_alignment_repair_tranche_ledger.schema.json` parsed as JSON after repair.
- `git diff --check` passed.
- No `src/**` or `tests/**` files were changed by this tranche.

Not verified in this tranche:

- Full-suite pytest health.
- Runtime import health beyond prior baseline evidence.
- Behavioural adequacy of presence-only or zero-assert tests.

## 8. Carry-forward blockers

The next block must not open a large Atlas tranche until these are addressed or explicitly accepted in a bounded plan:

1. Full repo pytest health remains unverified in this repair tranche.
2. Presence-only / zero-assert Tier A tests remain an inventory item, not repaired behavioural proof.
3. The `8` files marked `pending_explicit_registry_record` need later retained-test admission, demotion, or retirement.
4. The `5` files marked `tier_a_file_registered_outside_retained_seed_tier_a` need later registry placement reconciliation.
5. Capital deployment authority broader sizing semantics remain outside this tranche.

## 9. Closeout

This tranche is closed.

It repairs truth surfaces and inventories proof weakness only. It does not claim the active codebase is fully aligned, and it does not authorise the next Atlas implementation tranche by itself.
