# VI-15-L1 — Pre-authority distribution metadata inspection

## Status

**WORKER PRE-AUTHORITY INSPECTION COMPLETE — BLOCKED FOR PROGRAMME OWNER DECISION.**

No final distribution name or version has been selected or applied by the Worker.

## Governing proposition

The accepted `EXEC_PLAN.md` requires VI-15-L1 to establish the current distribution/build state and
then stop for explicit Programme Owner authority over the final distribution name and version.
The current `pyproject.toml` values are repository state only and are not final authority.

Accepted BICP/IWO authority likewise preserves final distribution naming/version metadata as a
Remaining Unknown until VI-15.

## Verified current distribution/build state

Current `pyproject.toml` declares:

- distribution name: `nvda-architecture-kernel`;
- distribution version: `0.1.0`;
- build backend: `hatchling.build`;
- build requirement: `hatchling==1.29.0`;
- wheel package root: `src/nvda_desk`;
- Python requirement: exactly `3.13.5`;
- runtime dependencies: `PyYAML==6.0.3` and `psycopg[binary]==3.3.4`.

The realised import/package topology is:

- `nvda_desk.architecture`;
- `nvda_desk.composition`;
- accepted M-owner package `nvda_desk.raw_signal_occurrence_truth`;
- accepted M public seam `nvda_desk.raw_signal_occurrence_truth.api`.

The accepted VI-04 authority fixes the owner package/public seam above but explicitly does not select
final distribution name/version metadata.

## Distribution identity is independent of owner/import topology

Hatchling is configured to package `src/nvda_desk`. No accepted architecture or package law found in
the inspected authority requires the distribution name to equal the Python import package or the
Raw Signal owner package name.

Therefore a Programme Owner decision to change the distribution name does not, by itself, require a
module rename or architecture-owner/public-seam change.

## Exact mutation consequences of the Programme Owner decision

### If current name and version are retained

Explicitly authorising `nvda-architecture-kernel==0.1.0` as final requires no package/source/test byte
change merely to align the current values. The authority and candidate evidence still need to record
that the previously unresolved values are now final.

### If distribution name changes but version remains `0.1.0`

At minimum:

- `pyproject.toml` project `name` must change;
- `tests/bootstrap/test_legacy_exclusion.py` currently asserts the literal
  `nvda-architecture-kernel` and must be updated to the newly authorised identity or otherwise made
  truthfully derive the same authorised proposition.

No runtime module/package rename is established as necessary by current evidence.

### If distribution version changes

At minimum:

- `pyproject.toml` project `version` must change;
- `src/nvda_desk/__init__.py` currently exposes `__version__ = "0.1.0"` and must be kept truthful to
  the authorised distribution version;
- `tests/bootstrap/test_minimal_imports.py` currently asserts `nvda_desk.__version__ == "0.1.0"` and
  must be updated accordingly.

Changing the version therefore has a strictly packaging/version-related source/test consequence, but
no evidence establishes a need to alter Raw Signal semantics, owner identity, module topology,
dependencies or public seams.

Historical evidence documents that mention the old distribution/version remain historical evidence
and are not to be rewritten merely because a final VI-15 identity is authorised.

## Normative constraints established

- final distribution name/version are non-free and require explicit Programme Owner authority;
- owner package `nvda_desk.raw_signal_occurrence_truth` and its public seam are already fixed and are
  not reopened by VI-15-L1;
- current values cannot become final by convention, precedent or implementation convenience;
- metadata application must not broaden product semantics, dependencies or module admission;
- VI-15-L2 package/build/install proof cannot begin until VI-15-L1 receives authority, freezes one
  exact candidate, passes independent Tester review and is promoted.

No inspected accepted authority supplies a mandatory alternative distribution name or version.

## Smallest required Programme Owner decision

Please explicitly authorise exactly:

1. final distribution name; and
2. final distribution version.

One valid form, if intended, is an explicit instruction to retain the current values as final:

`nvda-architecture-kernel`, version `0.1.0`.

No metadata will be applied until that authority is supplied.
