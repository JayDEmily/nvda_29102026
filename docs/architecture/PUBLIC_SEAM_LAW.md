# Public Seam Law

Python does not enforce private package boundaries. Leading underscores, `__all__` and naming conventions communicate intent but do not prevent imports.

The repository therefore treats each active owner’s registry-declared `public_seam` as its only lawful cross-owner import target.

The static checker rejects:

1. an import of another owner’s undeclared submodule;
2. a relative import that crosses an owner root;
3. an undeclared owner edge;
4. `importlib.import_module`, `__import__` or equivalent dynamic import calls inside registered runtime owners;
5. an exception not explicitly listed in dependency rules.

The checker does not infer semantic ownership from directory names. Owners must be registered before cross-owner validation can recognise them.

Typed public seams are a project requirement. Static type annotations describe the contract; Python itself does not guarantee runtime type enforcement.
