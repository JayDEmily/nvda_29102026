# Gate 48 — Carry-Horizon Handoff

Status: complete on `main`

## Purpose

Formalise the typed handoff from intraday close-state outputs into overnight, weekend, and event-carry evaluation so weekend logic stops being implied and becomes explicit.

## Why this gate exists

The repo already has a separate carry branch in principle, but the handoff from intraday cognition into carry evaluation is not yet a first-class typed contract.

## Leaves in Gate 48

1. `LEAF-G48-001` — define the typed close-state to carry-state handoff contract.
2. `LEAF-G48-002` — define the horizon taxonomy for `overnight`, `weekend`, and `event_carry`, including Friday close and pre-event hold cases.
3. `LEAF-G48-003` — extend the overnight schemas and carry services to consume the new handoff packet.
4. `LEAF-G48-004` — define the allowed carry actions and overrides: `flatten`, `hold_small`, `hold_baseline`, `add_carry`, `block_carry`, and the conditions under which each is legal.
5. `LEAF-G48-005` — add replay and contract tests that prove weekend/event carry remain a separate branch rather than a disguised intraday playbook.

## Entry rule

Gate 47 must be complete enough that the playbook/horizon split is explicit.

## Exit rule

Carry evaluation has an explicit typed upstream packet, horizon taxonomy is frozen, and replay tests prove the branch separation.

## Non-goals

- no mixing of weekend logic into ordinary intraday playbook eligibility;
- no fake booked-position theatre;
- no silent policy changes about mandatory flattening.

## Exit evidence

- Typed close-state handoff, carry taxonomy, carry actions, carry services, and replay tests are in place.
