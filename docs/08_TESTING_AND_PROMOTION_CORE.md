# 08_TESTING_AND_PROMOTION_CORE

All repo paths in the numbered control stack are repo-root-relative.


## Scope of this document

This document owns:

- environment and install provenance for governed proof
- proof-tier law
- temporary-state proof lifecycle law
- vocabulary constraints inside proof artefacts
- checkpoint and docstring proof requirements where current live doctrine requires them
- documentation and control-surface proof law
- proof receipt law
- promotion and demotion law

## Environment and install provenance law

Governed proof must run in the repo-local declared environment.

That environment must be created from the repo packaging authority and the canonical install flow declared by current live doctrine.

If current live doctrine declares canonical setup commands such as `make install` or equivalent setup commands, those commands are the required environment path unless a higher-priority live surface explicitly routes a different path.

Ad hoc package installation, undeclared environment drift, or missing environment provenance makes governed proof insufficient.

## Proof-tier law

Governed proof is classified into three tiers:

- Tier A: blocking governed proof
- Tier B: bounded shadow proof
- Tier C: historical, observational, or non-blocking proof

A proof artefact is Tier A only when current live doctrine or the active bounded pack explicitly classifies that artefact as Tier A.

A proof artefact does not change tier by habit or convenience.

## Tier A law

Tier A owns the blocking proof required for the current claim.

If a Tier A artefact that owns a touched surface is red, missing, or unreconciled, the work is not ready for promotion.

A green local proof slice is insufficient while another Tier A artefact that owns a touched surface remains unreconciled.

## Tier B law

Tier B is lawful for bounded shadow checking that is relevant to the current tranche but that is not blocking by current live doctrine.

Tier B debt does not block promotion unless live doctrine or the active bounded pack explicitly promotes it to blocking status.

Tier B must not be presented as Tier A.

## Tier C law

Tier C contains historical, observational, predecessor, or cleanup proof that is not blocking for the current claim unless live doctrine or the active bounded pack explicitly promotes it.

Tier C must not remain treated as blocking after live doctrine and router truth move on.

## Existing Tier A fallout declaration law

If a gate changes a surface in a way that changes the live Tier A boundary for an existing block, the active bounded pack must declare the exact pre-existing Tier A proof files or families that are permitted to receive bounded fallout repair.

If no pre-existing Tier A fallout repair is authorised, the active bounded pack must say `none; stop and re-plan` before those files are touched.

## Packet-carriage proof law

If a tranche changes live packet-carriage law, packet-envelope law, or packet readers, Tier A proof must cover the changed packet families.

That proof must include:

- envelope conformance proof
- producer-side emission proof
- consumer-side acceptance proof
- preserved-seam distinction proof where packet carriage crosses bounded ownership surfaces
- invalid or degraded packet proof where the changed packet family lawfully emits those states

A packet-carriage tranche is incomplete if it proves only packet production or only packet consumption.

## Packet numeric-integrity proof law

If a tranche changes packet carriage for numeric fields, Tier A proof must include representative numeric-integrity cases for the changed packet family.

Those cases must cover the forms that matter for the changed contracts, including where applicable:

- signed values
- zero values
- decimal precision
- percentage scale
- magnitude-sensitive values where `0.01` and `0.0001` are not equivalent

A packet-carriage tranche is incomplete if numeric meaning drifts while envelope proof remains green.

## Packet state-semantics proof law

If a tranche changes packet carriage for a field whose state meaning depends on omission, `null`, or an explicit state value, Tier A proof must cover those distinctions for the changed packet family.

A packet-carriage tranche is incomplete if the migrated contract makes those states ambiguous.

## Install record law

Where governed proof is required, the execution record must make the environment path inspectable.

At minimum, the record must show the canonical setup command or commands that were used for the proof run.

If the environment path cannot be shown, the proof claim is incomplete.

## Temporary-state proof law

Any proof artefact that encodes a temporary or point-in-time state must declare its lifecycle as one of:

- later-state tolerant
- mandatory retire at closeout
- mandatory replace at closeout

A temporary-state proof artefact must not remain in place as if it were permanent law after the state it described has lawfully changed.

## Vocabulary-in-proof law

A non-admitted durable term must not enter a proof artefact that itself becomes lasting repo law.

That restriction applies to artefacts including:

- governed test names
- durable fixture names
- manifest labels
- proof-block names
- contract-facing assertions

Proof artefacts must not become a back door for vocabulary drift.

## Checkpoint proof requirement

If current live doctrine requires a checkpoint declaration for a changed proof artefact, that declaration is part of governed proof.

It must be explicit.

If a required checkpoint declaration is missing, the proof-backed claim is incomplete.

## Docstring proof requirement

If current live doctrine requires a docstring applicability declaration for a changed owned surface, that declaration is part of governed proof.

It must be explicit.

If a required docstring declaration is missing, the proof-backed claim is incomplete.

## Documentation and control-surface proof law

Documentation, router, manifest, retained-test-registry, and control-surface changes are not exempt from governed proof.

If current live doctrine requires those changes to be proven through a governed proof artefact, that proof must run and be recorded before the changed repo truth is claimed.

Documentation work is not self-validating merely because it does not change runtime code.

## Proof receipt law

If proof-backed branch truth changed, update every required proof receipt surface that records that changed truth.

Required proof receipt surfaces include:

- touched proof-manifest or proof-block ownership surfaces when their truth changed
- `config/retained_test_registry.yaml` when tier status changed
- touched control-surface receipts affected by the changed truth

A proof-backed claim is incomplete if a required proof receipt is missing or if it records the wrong state.

## Promotion and demotion law

A proof artefact moves from Tier B or Tier C to Tier A only by explicit live doctrine or lawful active-pack authority.

A proof artefact moves from Tier A only by explicit live doctrine or lawful active-pack authority together with truthful manifest and receipt reconciliation.

Silent promotion and silent demotion are prohibited.

## Proof-closeout rule

Proof-backed work is not ready for promotion if any required proof condition remains unmet.

That includes any case where:

- required blocking proof is red, missing, or unreconciled
- the environment provenance is missing or unlawful
- a temporary-state proof artefact has no declared lifecycle
- a required checkpoint declaration is missing
- a required docstring declaration is missing
- a required proof receipt is missing or incorrect

A persuasive narrative does not make insufficient proof sufficient.

## Native Architecture Blueprint boundary

Within native code-structure architecture scope, this document must be read with `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md`.

`docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md` owns target package placement, component form, seams, ownership, persistence, test-family mapping, reservations, module allocation, and traceability for native code-structure architecture.

It does not override the authority hierarchy defined by `docs/01_NORMATIVE_CORE.md`.

All durable terms used by live control documents must be governed by `docs/vocabulary/vocabulary_registry.md` or lawfully admitted by the vocabulary process before they become canonical language.
