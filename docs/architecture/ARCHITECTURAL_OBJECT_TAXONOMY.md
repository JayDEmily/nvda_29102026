# Architectural Object Taxonomy

## Identifier grammar

Each identifier is a category prefix followed by a decimal integer padded to at least two digits:

```text
M00 … M99, M100, M101, …
P00 … P99, P100, …
G00 … G99, G100, …
A00 … A99, A100, …
K00 … K99, K100, …
S00 … S99, S100, …
```

`M1`, negative suffixes, mixed prefixes and non-decimal suffixes are invalid. The schemas impose no maximum numeric value. Allocation is monotonic within each category. A retired identifier remains reserved permanently.

## Categories

### M — runtime semantic ownership module

Owns one coherent domain decision, transformation, policy or lifecycle. An active module requires semantic responsibility, explicit inputs/outputs, exclusions, declared dependencies, a typed public seam and independently admitted obligations.

### P — protocol or governed information carrier

Owns information shape, identity, versioning, validation, compatibility and carriage rules. It does not decide domain outcomes or orchestrate runtime work.

### G — continuous governance plane

Constrains or evaluates the repository through proof, promotion, vocabulary or similar governance. It is not a runtime business dependency.

### A — application shell and composition

Owns startup, shutdown, dependency construction, adapter translation and top-level run lifecycle. It composes admitted runtime objects but does not own their semantic decisions.

### K — shared technical kernel or mechanism

Provides domain-neutral mechanisms such as transaction coordination or storage abstractions. A kernel does not acquire the domain meaning or record ownership of its consumers.

### S — architecture surface

Describes end-to-end coverage or assurance across objects. It is a view, not automatically a package, runtime owner or implementation claim.

## Statuses

- `placeholder` — identity reserved with no admitted implementation;
- `bootstrap` — minimal shell exists but is not an active business participant;
- `framework` — governance/configuration machinery exists but is not a runtime domain service;
- `active` — implementation and public seam are admitted for composition;
- `deprecated` — still present only for bounded transition; not selectable for new composition;
- `retired` — inactive historical identity; never reusable.

Only `active` is runtime-composable.
