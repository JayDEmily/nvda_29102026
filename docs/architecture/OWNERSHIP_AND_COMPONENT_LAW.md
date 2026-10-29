# Ownership and Component Law

## Purpose

This document owns the generic separation between semantic ownership, component form, coordination and durable-state roles. It carries forward the behaviour-neutral architecture principles required to prevent a future module, carrier, repository, adapter or governance surface from absorbing another role merely because implementation is convenient.

## Normative propositions

- **AK-OWN-001 — One bounded semantic owner.** A material decision, transformation, policy, lifecycle or governed output has one bounded semantic owner. A package, class, carrier, writer, reader, coordinator, reviewer, test or physical file location does not acquire that ownership by proximity.
- **AK-FORM-001 — Component-form separation.** A component must use the form appropriate to its responsibility. A component may combine forms only when accepted implementation authority explicitly establishes that the combination preserves ownership and seam law.
- **AK-STATE-001 — Writer/reader and semantic-ownership separation.** Durable truth has an authorised semantic owner and an authorised write boundary. Technical storage or transaction mechanisms, read projections and review surfaces do not acquire the domain meaning they store, read or describe.

## Component forms

| Component form | Owns | Must not silently own |
|---|---|---|
| adapter | translation at an external or compatibility boundary | domain decisions |
| contract/public API | boundary shape and invariants | runtime orchestration or persistence policy |
| schema/model | validated data structure | service coordination or semantic decisions |
| service | bounded operation owned by its semantic authority | unrelated persistence authority or cross-owner policy |
| repository/store | durable read/write mechanism under an authorised state boundary | the domain decision that creates the record |
| orchestrator/composition | ordered coordination and construction | hidden domain rules belonging to participants |
| configuration authority | governed parameters and allowed values | ad-hoc runtime mutation or hidden policy ownership |
| test/proof surface | evidence about an admitted proposition | production decision logic or semantic authority |

## State and persistence

For every material durable-state domain, accepted implementation authority must identify, as applicable:

1. the semantic owner of the state;
2. the authorised writer boundary;
3. lawful readers/read models;
4. the persistence or transaction mechanism used;
5. prohibited writers or substitutions;
6. replay/lineage obligations required by the owned meaning.

A shared `K` mechanism may coordinate transactions or expose storage abstractions. Participation in that mechanism does not transfer semantic ownership from an `M` owner to `K`.

A read projection may differ from the write model. It must preserve the owned meaning and identify the source state; it does not become a competing authority.

## Coordination

Application shells and orchestrators may sequence lawful owners and translate at their boundaries. Coordination does not create ownership of the participants' decisions.

Governance and review may inspect or evaluate outputs. Inspection, validation, promotion or explanation does not make those planes semantic owners.
