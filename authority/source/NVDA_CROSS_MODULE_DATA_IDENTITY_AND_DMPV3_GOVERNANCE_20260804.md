# Cross-Module Data Identity and DMPV3 Governance

**Status:** Standalone architecture guidance  
**Date:** 4 August 2026  
**Scope:** Naming, identity and contract governance for data carried between independently owned modules, especially through DMPV3.

## 1. Decision

The project requires a canonical cross-module data vocabulary because DMPV3 transports information across semantic ownership boundaries. The earlier global vocabulary approach was directionally correct about shared data, but it applied governance too broadly.

Use this rule:

> Internal implementation names are module-local. Every concept crossing an ownership boundary must have one stable semantic definition, an owning authority and a versioned public contract.

Do **not** centrally govern every Python class, function, variable or intermediate value. Python namespaces already isolate local implementation names. Central governance is required only where another module, persisted record, replay process, audit surface or external interface must interpret the same datum consistently.

## 2. The three layers that must remain separate

### 2.1 Module-local implementation vocabulary

A module may define internal names such as `State`, `Signal`, `Decision`, `Config` or `Accumulator` without requiring repository-wide uniqueness.

```python
from nvda.temporal import model as temporal_model
from nvda.parallel_risk import model as risk_model

temporal_state = temporal_model.State(...)
risk_state = risk_model.State(...)
```

Python modules provide separate namespaces. Two modules may lawfully define the same local name because the module path disambiguates it. Repository-wide renaming of every class is therefore unnecessary overhead.

### 2.2 Canonical cross-module semantic identities

A datum requires a stable shared identity when its meaning must survive movement between owners. Examples include:

```text
signal.session_vwap
signal.best_bid_price
signal.gamma_exposure
coefficient.parallel_risk.gamma_pressure
decision.trade_permission
state.market_session
```

The stable identity answers:

> What concept is this?

It must remain independent of the current Python class name, file location and owning module number. Ownership can change while the concept remains the same.

### 2.3 Versioned payload contracts

The contract answers:

> In what structure, type and version is this concept carried at this boundary?

A contract defines fields, types, units, requiredness, null behaviour, allowed values, compatibility rules and schema version. A concept identity and a payload schema are related but are not interchangeable.

## 3. DMPV3 is the carrier, not the owner of all meaning

The current DMPV3 protocol states that one canonical outer envelope normalises inter-module carriage but does not merge module responsibility, runtime ownership or downstream meaning. It requires packet readers to interpret the packet through declared carriage surfaces rather than guessing from payload shape.

The canonical envelope currently includes:

- `id`;
- `source`;
- `type`;
- `time`;
- `dataschema`;
- `traceid`;
- `runid`;
- `scenarioid`;
- `packetrole`;
- `producer`;
- `lineage`;
- `validation`;
- `summary`;
- `data`;
- `dmpextensions`.

The Python implementation mirrors this envelope in `DmpV3Envelope`.

DMPV3 therefore owns:

- the outer carriage grammar;
- packet-occurrence identity rules;
- declared schema and packet-role carriage;
- producer metadata carriage;
- lineage carriage;
- validation-result carriage;
- compatibility and extension limits.

DMPV3 does **not** own:

- the semantic definition of session VWAP;
- the meaning of a risk coefficient;
- the authority to create a decision identity;
- the ownership of a position, execution, policy or state transition;
- the interpretation of a payload beyond its admitted contract.

The runtime module that owns a domain concept remains responsible for its semantic definition. DMPV3 transports that meaning under a declared schema.

## 4. Six identity layers

Do not collapse distinct meanings into one generic `id`.

| Identity layer | Meaning | Example |
|---|---|---|
| Packet occurrence | This particular DMPV3 emission | `packet:01J...` |
| Execution context | The trace, run or scenario in which it occurred | `trace:...`, `run:...` |
| Payload contract | The schema and version used for carriage | `nvda.market.PreparedContext.v1` |
| Data concept | The stable semantic meaning of the datum | `signal.session_vwap` |
| Domain instance | The particular instrument, observation, decision or position | `instrument.NVDA`, `decision:...` |
| Lineage object | The upstream packets, evidence, dependencies and replay references | `capture:...`, `source-artifact:...` |

### 4.1 Packet occurrence identity

`packet.id` identifies one emitted DMPV3 occurrence. It must not silently become the authoritative identity of an upstream observation, source artefact, decision, position, execution, policy, state transition or receipt.

A retry of the same preserved packet may retain its occurrence identity. A transformed packet, semantically new packet or newly emitted replay result requires a new packet-occurrence identity.

### 4.2 Execution-context identity

`traceid`, `runid` and `scenarioid` are separate identities:

- `traceid` correlates related packet occurrences;
- `runid` identifies the governed execution or replay run;
- `scenarioid` identifies the admitted scenario or operating context.

A packet builder propagates those identities. It does not invent them merely to satisfy field shape.

### 4.3 Payload-contract identity

`dataschema` identifies the versioned public payload contract. It tells a consumer how to decode and validate `data`.

The schema identity must not be treated as the identity of the packet occurrence or the data concept. Several packet occurrences may use the same schema, and one schema may carry several canonical data concepts.

### 4.4 Data-concept identity

A data-concept ID identifies a stable meaning such as `signal.session_vwap`. It is not an occurrence ID and should not encode its current owner.

Avoid:

```yaml
id: M03.DF01
```

Prefer:

```yaml
id: signal.session_vwap
owner: M03
historical_aliases:
  - DF01
```

If ownership later moves, the semantic identity survives.

### 4.5 Domain-instance identity

A concept such as `signal.session_vwap` may have many observations. The particular observation must retain its instrument, observation time and source identity independently of the concept ID.

### 4.6 Lineage identity

Lineage fields must carry their declared meanings rather than acting as an untyped bag of identifiers. Parent packet occurrences, dependencies, principal upstream domain outputs, source artefacts, replay references and decision traces are separate relationships.

## 5. Recommended governance surfaces

Replace a repository-wide vocabulary dictionary with two connected registries plus module-local code.

### 5.1 Canonical data-concept catalogue

The catalogue defines stable public meaning.

```yaml
concepts:
  - id: signal.session_vwap
    name: Session VWAP
    definition: >
      Volume-weighted average price for the governed market session.
    kind: derived_signal
    value_type: decimal
    unit: price
    owner: M03
    temporal_semantics: market_session
    null_semantics: unavailable_when_valid_volume_is_zero
    historical_aliases:
      - DF01
```

Minimum fields should include:

- stable concept ID;
- human definition;
- semantic owner;
- data kind;
- value type;
- unit or dimensional meaning;
- time semantics;
- null and invalid semantics;
- lifecycle status;
- historical aliases;
- source lineage where required.

### 5.2 Payload-schema registry

The schema registry defines boundary carriage.

```yaml
schemas:
  - id: nvda.market.PreparedContext.v1
    protocol: P01
    owner: M02
    version: 1
    fields:
      - concept: signal.session_vwap
        required: false
      - concept: signal.best_bid_price
        required: true
```

Minimum fields should include:

- stable schema ID and version;
- owning module;
- protocol used for carriage;
- field-to-concept mappings;
- requiredness;
- structural and semantic validation rules;
- compatibility and deprecation rules;
- named consumers.

### 5.3 Module-local implementation

Internal classes and functions remain owned and named by the module. They need not appear in either central registry unless they form part of a public seam.

## 6. Ownership model

The responsibilities should be divided as follows:

| Owner | Responsibility |
|---|---|
| Runtime module | Defines and produces the domain concept; owns its semantic correctness |
| `G02` vocabulary/data governance | Enforces uniqueness, definitions, aliases, lifecycle and consistency for public semantic identities |
| `P01` DMPV3 | Validates and carries the versioned envelope and declared payload contract |
| Consumer module | Depends on the public contract and concept meaning, not the producer's private implementation |
| Persistence/replay owner | Preserves occurrence, domain-instance, contract and lineage identities without collapsing them |

`G02` must not become the semantic owner of every datum. It governs the catalogue. The producing module owns the domain meaning.

## 7. When a datum needs a canonical concept ID

Assign a stable concept ID when one or more of these are true:

- it crosses a module boundary;
- it appears in more than one payload schema;
- it is persisted, replayed or independently audited;
- it is independently queried or monitored;
- its unit, timing, lineage or null semantics are material;
- it can change owner while retaining the same meaning;
- it is carried dynamically rather than as a fixed named field;
- multiple consumers must agree on its definition.

A module-local intermediate value does not need a central ID merely because it exists.

### Fixed typed payload

A fixed contract can identify meaning through its schema and field definition:

```python
@dataclass(frozen=True)
class PreparedMarketContext:
    session_vwap: Decimal | None
```

Here, `dataschema = nvda.market.PreparedContext.v1` plus the schema field definition can be sufficient.

### Dynamic heterogeneous payload

A dynamic signal collection requires explicit concept IDs:

```python
@dataclass(frozen=True)
class SignalObservation:
    concept_id: str
    value: Decimal | int | bool | str
```

This distinction prevents the catalogue from becoming an administrative inventory of every scalar in the repository.

## 8. Families, spreadsheet IDs and configuration

### 8.1 Families are tags

Signal families such as `options_surface`, `dealer_convexity` or `temporal_anchor` should be non-authoritative classifications. They must not automatically become:

- Python inheritance hierarchies;
- module boundaries;
- package boundaries;
- globally exclusive namespaces;
- ownership authorities.

A concept has one semantic owner but may have several descriptive families.

```yaml
id: signal.gamma_exposure_flip
owner: M07
families:
  - options_surface
  - dealer_convexity
```

### 8.2 Historical spreadsheet IDs are aliases

Identifiers such as `DF01` or `RP14` may remain as historical aliases and reconciliation keys. They should not be the permanent semantic identity because they carry little meaning and are fragile under catalogue change.

### 8.3 Configuration remains owner-local

Thresholds and coefficients should normally be defined and validated by the module that owns their meaning. A central coefficient index may be generated as a read-only audit view, but it should not become one mutable global registry that couples unrelated module configurations.

## 9. Naming rules

For public concepts and contracts:

1. Use the same name for the same concept.
2. Use different names for different concepts.
3. Avoid overloaded generic names such as `state`, `value`, `signal` or `record` without a bounded namespace.
4. Prefer stable semantic names over physical locations or current module numbers.
5. Keep occurrence identity separate from concept identity.
6. Keep schema identity separate from payload and domain-instance identity.
7. Record aliases and deprecations rather than silently reusing an old identifier with a new meaning.

## 10. Validation requirements

The architecture should mechanically validate at least:

- uniqueness of public concept IDs;
- uniqueness of schema IDs by version;
- existence of every concept referenced by a schema;
- one declared semantic owner per concept;
- valid lifecycle states and aliases;
- no alias collision with another active concept;
- declared units and value types where applicable;
- declared null semantics where absence is possible;
- declared consumers for public contracts;
- compatibility rules for schema evolution;
- no use of packet occurrence IDs as substitute domain identities;
- no unknown dynamic concept ID accepted as binding authority;
- no consumer inference from payload shape alone.

Mechanical validation can establish structural consistency. It cannot prove the domain definition itself is correct.

## 11. Repository law

> Internal implementation names are module-local and are disambiguated by Python namespaces. Public cross-module concepts must have stable semantic definitions and explicit owners. DMPV3 packet identity, execution-context identity, schema identity, data-concept identity, domain-instance identity and lineage identity must remain distinct. P01 carries these identities but does not own their domain meaning. G02 governs the consistency of public semantic identities, not every name in the codebase.

## 12. Evidence inspected in the current repository

The following surfaces were inspected from `NVDA_MAIN_D24F962_20260803_FULL_HISTORY.tar(1).gz`:

- `docs/09_DMPV3_PROTOCOL_CORE.md:19-29` — the outer envelope normalises carriage but does not merge responsibility or meaning;
- `docs/09_DMPV3_PROTOCOL_CORE.md:31-56` — canonical outer-envelope fields;
- `docs/09_DMPV3_PROTOCOL_CORE.md:78-91` — packet interpretation must use declared role, producer and schema rather than payload-shape inference;
- `docs/09_DMPV3_PROTOCOL_CORE.md:95-113` — bounded lineage fields and explicit upstream identities;
- `docs/09.1_DMPV3_PROTOCOL_WORKING.md:11-39` — packet-occurrence and execution-context identities;
- `docs/09.1_DMPV3_PROTOCOL_WORKING.md:41-59` — bounded lineage-field meanings;
- `docs/09.1_DMPV3_PROTOCOL_WORKING.md:63-79` — packet emission time must not replace source observation time;
- `docs/09.1_DMPV3_PROTOCOL_WORKING.md:81-119` — validation and extension limits;
- `src/nvda_desk/contracts/packets.py:418-440` — implemented `DmpV3Envelope` field surface.

This inspection supports the identity separation above. It does not certify the complete current DMPV3 implementation or all consumers.

## 13. Official external references

1. **Python Software Foundation — Python tutorial: scopes and namespaces.** Explains that names in different module namespaces are unrelated and can coexist without confusion.  
   https://docs.python.org/3/tutorial/classes.html#python-scopes-and-namespaces

2. **Python Software Foundation — Python tutorial: modules.** Describes module namespaces and qualified access through the module name.  
   https://docs.python.org/3/tutorial/modules.html

3. **Google Cloud — API Design Guide: Naming conventions.** Requires simple, intuitive and consistent public names; the same term for the same shared concept; different terms for different concepts; and avoidance of ambiguous overloading.  
   https://cloud.google.com/apis/design/naming_convention

4. **Microsoft Learn — Use tactical domain-driven design to design microservices.** Rejects a single unified model for a complex system and supports bounded contexts with their own internal models and explicit contracts at boundaries.  
   https://learn.microsoft.com/en-ca/azure/architecture/microservices/model/tactical-ddd

5. **Microsoft Learn — Domain events: design and implementation.** Distinguishes internal domain events from integration events published outside a bounded service or context.  
   https://learn.microsoft.com/en-us/dotnet/architecture/microservices/microservice-ddd-cqrs-patterns/domain-events-design-implementation

6. **Microsoft Learn — Integration event-based communication.** Describes explicit integration events for synchronising state across service or subsystem boundaries.  
   https://learn.microsoft.com/en-us/dotnet/architecture/microservices/multi-container-microservice-net-applications/integration-event-based-microservice-communications

7. **IBM — What is data governance?** Describes governance through ownership, standards, naming conventions, data flows and centralised definitions/metadata.  
   https://www.ibm.com/think/topics/data-governance

8. **IBM — What is a data catalog?** Distinguishes a broad data catalogue, which provides ownership and business context, from a data dictionary, which defines dataset structure, field types, allowed values, ranges and formats.  
   https://www.ibm.com/think/topics/data-catalog

## 14. Recommended next architectural artefacts

When this guidance is implemented, create only these bounded surfaces:

```text
config/data_concepts.yaml
config/payload_schemas.yaml
schemas/data_concept.schema.json
schemas/payload_schema.schema.json
docs/architecture/CROSS_MODULE_DATA_IDENTITY.md
tools/validate_data_contracts.py
```

Do not recreate a global dictionary of all code vocabulary.
