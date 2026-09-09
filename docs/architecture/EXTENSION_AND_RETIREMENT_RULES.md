# Extension and Retirement Rules

## Normative propositions

- **AK-LIFE-001 — Lifecycle identity integrity.** Retired identities cannot be reused. Predecessor/successor identities must be lawful, self-lineage is prohibited, and current reciprocal relationships must be structurally consistent while historical lineage remains representable without reactivation.
- **AK-EXT-001 — Open-ended category extension.** Adding a new object in an existing category must not require a central identifier enumeration, hard-coded count ceiling or architectural redesign. Admission uses declarative registration plus category-appropriate authority, implementation and proof.

## Runtime-module admission

For brief-derived implementation, this sequence begins only after a valid implementation-authority ingress under `IMPLEMENTATION_AUTHORITY_INGRESS.md`. A new runtime semantic owner is admitted only after current authority establishes the boundary. The architecture sequence is:

1. allocate the next unused `M` identifier;
2. define one bounded semantic responsibility and explicit exclusions;
3. declare inputs, outputs, state/time/side-effect ownership and durable-state writer/reader obligations where applicable;
4. choose lawful component forms and owner-local implementation structure;
5. declare permitted owner dependencies;
6. declare one typed Python-visible public seam where Python-visible cross-owner use exists;
7. bind the exact normative propositions that govern the implementation;
8. admit exact architecture and behavioural proof derived from those propositions;
9. compose the module through the application shell when runtime participation is required;
10. pass the applicable architecture/promotion proof.

The accepted semantic/normative authority supplies the domain meaning. The architecture does not invent missing meaning in order to complete admission.

## Other categories

The same identity/lifecycle discipline applies to `P`, `G`, `A`, `K` and `S` with category-appropriate requirements.

A protocol, governance plane or surface does not require a runtime package merely because it is registered. A Python-visible protocol/kernel implementation must expose enough package/seam metadata for the dependency/public-seam controls that actually apply to it.

## Replacement, split and merger

A replacement, split or merger preserves and explicitly dispositions:

- predecessor/successor identities;
- semantic migration;
- compatibility impact;
- consumer migration;
- state/persistence ownership effects;
- proof effects.

No successor silently inherits implementation status, semantic authority or consumer acceptance.

## Deprecation and retirement

A deprecated object is unavailable for new composition/admission and carries an explicit retirement path. A retired object is absent from active composition and its identifier remains permanently reserved.

Git history preserves prior implementation. Material that does not belong in the target active tree is `DO_NOT_CARRY_FORWARD`; it is not destroyed merely because it is absent from the target tree. `DO_NOT_CARRY_FORWARD` is a target-tree/Git-history disposition, not an architectural lifecycle transition: it does not by itself make an object `retired` or place its identifier in `retired_ids`. Lifecycle retirement requires explicit current authority for that retirement.
