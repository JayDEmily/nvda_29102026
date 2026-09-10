# Architectural Object Taxonomy

## Normative propositions

- **AK-TAX-001 — Category separation.** Runtime semantic owners (`M`), protocols/carriers (`P`), governance planes (`G`), application shells (`A`), technical kernels (`K`) and architecture surfaces (`S`) are distinct categories. Registration in one category cannot create authority in another.
- **AK-ID-001 — Unbounded post-reset permanent identifiers.** Identifiers use a category prefix and decimal suffix padded to at least two digits. Allocation continues beyond `99`. Within the current post-reset namespace, an identity is consumed when it is currently registered, retired under current lifecycle authority, or durably recorded as a post-reset implementation allocation; consumed identities are never reused for different meaning. Pre-reset historical product identifiers do not reserve current post-reset identifiers merely because the same strings occurred before the reset.
- **AK-NAME-001 — Namespace-scoped Python naming.** Architectural object identifiers remain globally unique registry identities, while ordinary Python package, module, class, function, method and variable names follow the Python namespace model and applicable Python naming conventions. A Python symbol need be unique only within the namespace or public interface in which Python resolves or exposes it; repository-global synonym policing or identifier prefixing is not an architectural requirement.

## Identifier grammar

```text
M00 … M99, M100, M101, …
P00 … P99, P100, …
G00 … G99, G100, …
A00 … A99, A100, …
K00 … K99, K100, …
S00 … S99, S100, …
```

`M1`, negative suffixes, mixed prefixes and non-decimal suffixes are invalid. Schemas impose no maximum numeric value. Candidate resolution is monotonic within each category over identities consumed by the current post-reset namespace; historical pre-reset numbering is evidence, not an allocation input.

## Python naming scope

Official-source basis: the Python language tutorial's namespace model and PEP 8 naming conventions govern Python name resolution and ordinary Python naming style. This kernel law only maps those official rules into the architecture boundary; it does not create a parallel vocabulary system.

Python-visible names follow Python's own namespace model and the applicable Python naming conventions. Module qualification and containing object namespaces disambiguate names across separate namespaces, so a class, function or other symbol is not required to be globally unique across the repository merely because the same unqualified spelling exists elsewhere. Public-interface names must still be unambiguous within the interface that exposes them.

The architecture-object identifier grammar above is separate: `M`, `P`, `G`, `A`, `K` and `S` identifiers are registry identities and remain globally unique within the architecture registry.

## Categories

### M — runtime semantic ownership module

Owns one coherent domain decision, transformation, policy or lifecycle. An admitted runtime module declares its semantic responsibility, exclusions, inputs, outputs, dependencies, state/time/side-effect ownership and one typed public seam.

`M` ownership is semantic ownership. It does not imply that the module must directly implement every storage write, transaction primitive, adapter or review projection associated with its meaning.

### P — protocol or governed information carrier

Owns information shape, identity, versioning, validation, compatibility and carriage rules. It does not decide domain outcomes, acquire the meaning it transports or orchestrate runtime work.

A protocol may be declarative or may expose a Python-visible implementation boundary when separately admitted. Neither form makes it a runtime semantic owner.

### G — continuous governance plane

Constrains or evaluates the repository through proof, promotion or similar governance. It is not a runtime business dependency and does not acquire the semantic ownership of the artefacts it evaluates.

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
