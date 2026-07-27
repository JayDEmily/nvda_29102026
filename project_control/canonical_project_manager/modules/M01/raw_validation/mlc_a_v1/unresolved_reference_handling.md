# M01 unresolved and changed reference handling

## Result

The M01 workbook subset contains 174 referenced rebase rows:

- 150 `unchanged_since_atlas_snapshot`;
- 9 `directory_reference_present`;
- 15 `unresolved_reference`.

The exact non-current rows and affected cohort IDs are retained in `unresolved_reference_list.tsv`.

## Changed reference

The accepted architecture report identifies `docs/07.1_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_WORKING.md` as byte-changed since the Atlas snapshot. Its current repository version was read in full. Current lines 138-145 provide the retained external-ingress ownership supplement: no durable writer is admitted there; offline/recorded material is permitted; carrier validation has no domain/trading/persistence authority.

No conclusion relies on the obsolete snapshot hash or wording.

## Directory-level references

All nine directory-level references point to test directories. They were retained mechanically but not narrowed because:

1. this leaf determines normative authority before test routing;
2. MLC-R is not open;
3. tests are lower-precedence evidence and may not create authority.

Classification: `OUTSIDE_BOUNDED_M01_QUESTION` for this leaf.

## Unresolved references

The fifteen unresolved rows are stale test or implementation paths from the Atlas snapshot. They were not guessed, substituted or used as current authority.

Classification: `STALE_OR_UNRESOLVED_REFERENCE`.

Their absence does not block this authority-sufficiency proposal because every accepted claim is supported by a current numbered normative locator. Any later use of an affected Atlas cohort for proof routing or implementation must replace or narrow the stale reference under that later gate.

## Semantic admission

No changed, directory-level or unresolved Atlas reference was mechanically admitted. The exact workbook extraction is traceability evidence only.
