# Public Seam Law

## Normative proposition

- **AK-SEAM-001 — Public seam only.** Every cross-owner Python-visible dependency must enter through the target owner's declared public seam and a lawful declared dependency edge. Naming conventions alone are not enforcement.

## Seam contract

A public seam is an owned boundary, not merely a convenient import path. Accepted implementation authority must make the relevant boundary facts explicit, including:

- upstream/owning authority;
- intended consumers or consumer class;
- interface/carrier shape;
- required invariants;
- state or side effects visible across the seam;
- lawful variants and prohibited forms;
- traceability to the authority that supplied the meaning.

The seam transports or exposes owned meaning. It does not become the owner of that meaning.

## Python import enforcement

Python does not enforce private package boundaries. Leading underscores, `__all__` and naming conventions communicate intent but do not prevent imports.

Repository-owned static analysis must therefore reject, for registered Python-visible owners:

1. imports of another owner's undeclared submodule or member path;
2. relative imports that cross an owner root;
3. undeclared owner edges;
4. supported direct or aliased dynamic-import forms that would bypass owner/seam validation;
5. public-seam exceptions that are absent, malformed or broader than their explicit declaration.

All ordinary Python import forms that resolve to a registered owner must be judged against the same owner/dependency/seam law. The law is not weakened when the current checker has an implementation gap; the gap must be repaired before the affected proposition is claimed as proved.

The checker is not required to claim prevention of arbitrary metaprogramming, `eval`/`exec`, runtime monkey-patching or every possible dynamic-execution technique unless such coverage is separately admitted and proved.

## Typed boundary

Python-visible public seams are typed project contracts. A pinned static type checker is required for the Python-visible type proposition; Python annotations and Ruff alone do not establish static compatibility, and static typing does not establish semantic correctness or runtime validation.
