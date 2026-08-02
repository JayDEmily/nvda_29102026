# Unit 4 C-NORM — Structural Integrity Families

## Status

Current law aligned before Unit 4 production mutation. Each family remains a
separate semantic acceptance slice and must pass its own expected-red proof,
bounded implementation and affected validation before the next family opens.

## Authority

- `project_control/canonical_project_manager/CONTINUATION.md` section 8.4.
- `project_control/canonical_project_manager/EXEC_PLAN.md` dependency graph and
  continuation sequence.
- `docs/07.2_STATE_RISK_AND_REPLAY_WORKING.md` replay ownership law.
- `docs/10.1_VOCABULARY_AND_TERM_GOVERNANCE_WORKING.md` governed vocabulary and
  projection law.
- `docs/11.1_NATIVE_ARCHITECTURE_BLUEPRINT_WORKING.md` M12 dependency,
  compatibility containment and M00 composition law.

## Unit 4A — M12 dependency direction

M12 may depend on M04 plus accepted read-only evidence-export contracts and M13
transaction/evidence mechanisms. It may not import M10 runtime implementation
authority. Deterministic replay fingerprints used solely by M12 are M12-owned
mechanics; relocating or duplicating the pure primitive must preserve exact
fingerprint semantics and all current replay identities.

Pass: no production module under `m12_evidence_replay` imports M10, the public
M12 replay proof remains green, and equivalent values retain the same SHA-256
fingerprints.

## Unit 4B — governed process-wide values

Module-level values that encode accepted policy, role matrices, stage order,
allowed owner/fact sets, scanner scope or vocabulary projection structure are
caller-immutable. Freezing those values must not freeze legitimate per-instance
state, change a governed value, alter ordering, or change current algorithms.

Pass: all 19 identified exports reject caller mutation while their exact content
and affected owner behaviour remain unchanged.

## Unit 4C — scanner-owned projection headers

Machine-generated projection headers are scanner-owned metadata, not human
vocabulary evidence. The scanner must ignore schema-version, registry-version,
document-notes, namespace-scope and general projection-metadata header lines,
while still observing human prose below the header and every real unadmitted
candidate elsewhere.

Pass: a fixture containing candidate-like tokens in all owned header forms emits
no header occurrence, the same token in human prose is emitted, and all current
namespace scans remain candidate-clean after exact disposition reconciliation.

## Unit 4D — compatibility API identity and process state

`nvda_desk.api.app.HttpApp` and legacy analysis helpers are compatibility
surfaces, not identity or domain-state owners. They may translate explicit
caller-owned input but may not fabricate placement, inventory, capital, risk,
decision, evaluation, replay, dataset or window authority. Untyped veto/risk
collections are not canonical owner state and must not be exposed as API
routes. Canonical M00 must remain unable to select those removed compatibility
owners.

Pass: missing upstream authority fails closed; walk-forward replay authority
requires explicit dataset identity/fingerprint and packet identity; untyped
veto/risk state routes are absent; current explicit compatibility callers are
re-authored without weakening their invariant; M00 entry composition remains
unchanged.
