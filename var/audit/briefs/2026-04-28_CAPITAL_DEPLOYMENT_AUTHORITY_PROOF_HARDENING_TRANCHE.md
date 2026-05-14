# CAPITAL DEPLOYMENT AUTHORITY PROOF-HARDENING TRANCHE

Status: closed and runtime-reconciled.

## Plan

This tranche hardens the capital deployment authority proof layer after the downstream capital deployment authority pilot and active-codebase alignment repair tranche.

Execution order:

1. normative/control docs;
2. Tier A proof;
3. code conformance;
4. receipt/closeout truth.

## Scope

No new Atlas `blueprint_surface` tranche is opened. No virtual environment is created. No full Atlas batch is processed.

## Leaf queue

| Leaf | Type | Purpose | Status |
|---|---|---|---|
| CAP-PROOF-L01 | control reconciliation | Confirm authority and write the bounded plan. | closed |
| CAP-PROOF-L02 | test-first proof | Harden Tier A proof for explicit capital-state and bounded-policy sizing. | closed |
| CAP-PROOF-L03 | code conformance | Refactor capital code only to satisfy hardened proof. | closed |
| CAP-PROOF-L04 | mandatory closeout | Reconcile brief, ledger, registry, verification, and blockers. | closed |

## Execution notes

CAP-PROOF-L02 reauthored `tests/tier_a/capital_deployment/test_capital_contract_models.py` to require explicit capital-state and bounded-policy inputs.

CAP-PROOF-L03 updated capital contracts and authority helpers so authorised notional is computed from supplied `available_capital_usd` and the lesser of `requested_deployable_pct` and `max_deployable_pct`, instead of a hard-coded notional base.

CAP-PROOF-L04 reconciled the retained test registry and ledger truth.

## Runtime reconciliation

The follow-on runtime reconciliation pass closed the previous Unknown execution-health blockers.

Verification evidence from the runtime reconciliation pass:

- Targeted capital proof: `tests/tier_a/capital_deployment` passed 8/8.
- Full repo proof: `tests` passed 133/133.
- Test execution surface: Python 3.13.5 in-kernel runtime with repo `src` added to `sys.path`.
- No virtual environment was created.
- No package installation was performed.

Runtime caveat:

- Shell default `python3` resolved to `/opt/pyvenv/bin/python3` and hung during normal site startup in this environment.
- `/usr/bin/python3` started cleanly but did not have repo dependencies such as `pytest` and `pydantic`.
- The successful verification surface was therefore recorded explicitly rather than hidden.

## Verification

- Targeted capital proof: pass, 8 passed.
- Full-suite pytest: pass, 133 passed.
- Ledger JSON parse: pass.
- Ledger schema JSON parse: pass.
- Brief SHA matched ledger parent brief SHA: pass after reconciliation.
- No virtual environment created.
- No new Atlas tranche opened.

## Carry-forward blockers

- None for capital deployment authority proof-hardening runtime verification.
- Broader Tier A presence-proof replacement remains a separate future bounded tranche.

## Closeout

Closed with code/test/receipt surfaces updated and runtime verification reconciled.
