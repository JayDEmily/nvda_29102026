# 2026-03-25 Gate 32 Archetype and Entry-Gate Bridge Contracts

Status: Closed on `main`  
Gate: 32  
Leaf: `LEAF-G32-001`

## Closed set

1. `archive-module-020` / `archetype_matcher`
2. `archive-module-048` / `archetype_tagger`
3. `archive-module-023` / `entry_gate`

## What closed this gate

- Reconciled the selector-side `archetype_matcher` and `entry_gate` contracts already emitted by `tranche_a.py`.
- Reconciled the bridge-side `archetype_tagger` contract already emitted by `posture_enrichers.py`.
- Proved the exact three-item set in frozen order and preserved the current no-new-playbook boundary.

## Honesty boundary

- `entry_gate` remains advisory and may veto under permission or event-window stress.
- `archetype_matcher` stays bounded to existing runtime candidates; it does not invent new playbooks.
