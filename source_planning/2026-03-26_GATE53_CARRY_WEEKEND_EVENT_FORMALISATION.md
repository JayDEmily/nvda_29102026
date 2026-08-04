# Gate 53 — Carry / Weekend / Event-Horizon Formalisation

Status: complete on `main`

## Purpose

Formalise the typed handoff between intraday cognition and carry-horizon decisioning so weekend, ordinary overnight, and event carry are explicit horizon branches rather than hidden extensions of intraday logic.

## Leaves closed in Gate 53

1. `LEAF-G53-001` — define the close-state to carry-state handoff packet with held-position / inventory context.
2. `LEAF-G53-002` — encode weekend, overnight, and event-carry taxonomy plus carry actions in typed runtime surfaces.
3. `LEAF-G53-003` — harden downgrade / override rules so carry recommendations remain deterministic and explanation-safe.

## Outputs landed by Gate 53

- `src/nvda_desk/schemas/overnight.py`
- `src/nvda_desk/services/carry_handoff.py`
- `src/nvda_desk/services/carry_market.py`
- `tests/test_gate48_carry_handoff.py`
- `tests/test_gate53_carry_handoff.py`

## Entry rule

Gate 52 must already be complete on `main`, with family/setup lineage available as a native runtime surface.

## Exit rule

Carry-horizon routing must explicitly capture held-position context, family/setup/playbook lineage, and deterministic allowed-action ceilings for overnight, weekend, and event carry.

## Non-goals

- no DMP binding-surface promotion;
- no vocabulary-governance rewrite;
- no attempt to collapse carry logic back into intraday eligibility.
