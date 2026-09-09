# Architectural Object Taxonomy

## Normative propositions

- **AK-TAX-001 — Category separation.** Runtime semantic owners (`M`), protocols/carriers (`P`), governance planes (`G`), application shells (`A`), technical kernels (`K`) and architecture surfaces (`S`) are distinct categories. Registration in one category cannot create authority in another.
- **AK-ID-001 — Unbounded permanent identifiers.** Identifiers use a category prefix and decimal suffix padded to at least two digits. Allocation continues beyond `99`; retired identities are never reused for different meaning.

## Identifier grammar

```text
M00 … M99, M100, M101, …
P00 … P99, P100, …
G00 … G99, G100, …
A00 … A99, A100, …
K00 … K99, K100, …
S00 … S99, S100, …
```

`M1`, negative suffixes, mixed prefixes and non-decimal suffixes are invalid. Schemas impose no maximum numeric value. Allocation is monotonic within each category.

## Categories

### M — runtime semantic ownership module

Owns one coherent domain decision, transformation, policy or lifecycle. An admitted runtime module declares its semantic responsibility, exclusions, inputs, outputs, dependencies, state/time/side-effect ownership and one typed public seam.

`M` ownership is semantic ownership. It does not imply that the module must directly implement every storage write, transaction primitive, adapter or review projection associated with its meaning.

### P — protocol or governed information carrier

Owns information shape, identity, versioning, validation, compatibility and carriage rules. It does not decide domain outcomes, acquire the meaning it transports or orchestrate runtime work.

A protocol may be declarative or may expose a Python-visible implementation boundary when separately admitted. Neither form makes it a runtime semantic owner.

### G — continuous governance plane

Constrains or evaluates the repository through proof, promotion, vocabulary or similar governance. It is not a runtime business dependency and does not acquire the semantic ownership of the artefacts it evaluates.

### A — application shell and composition

Owns startup, shutdown, dependency construction, adapter translation and top-level run lifecycle. It composes admitted runtime objects but does not own their semantic decisions or hide dependencies through a service locator.

### K — shared technical kernel or mechanism

Provides domain-neutral mechanisms such as transaction coordination or storage abstractions. A kernel does not acquire the domain meaning, policy or record ownership of its consumers merely because it performs technical work on their behalf.

### S — architecture surface

Describes end-to-end coverage or assurance across architectural objects. It is a view and review boundary, not automatically a package, runtime owner, module allocation or implementation-completion claim.

## Statuses

- `placeholder` — identity exists with no admitted implementation;
- `bootstrap` — minimal shell exists but is not an active domain participant;
- `framework` — governance/configuration machinery exists but is not a runtime domain service;
- `active` — the category-appropriate implementation has been admitted for its lawful use;
- `deprecated` — present only for bounded transition and unavailable for new admission/composition;
- `retired` — inactive historical identity; never reusable.

Runtime composability is category-appropriate. `active` is necessary where runtime composition applies, but a protocol, governance plane or surface does not become a runtime module merely by becoming active in its own category.
