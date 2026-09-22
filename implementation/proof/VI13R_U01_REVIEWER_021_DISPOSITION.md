# VI-13R U01 Reviewer 021 disposition

## Disposition

`FAIL / RETURN_TO_WORKER`

U02 remains prohibited. The two Worker-observed failures are proof-harness defects, but the realised
U01 candidate also contains two material implementation/proof defects that defeat the accepted U01
public-contract proposition. They require Worker repair and fresh independent U01 re-review before
lawful promotion or U02.

## Binding

Fresh Reviewer 021 reviewed only IWO-U01 from the supplied full-Git archive.

- submitted archive SHA-256:
  `f81eda4d2b24c19dc9368906b9e4a7cb3c465c82840203e046bba047cd5c5f8f`;
- submitted repository HEAD:
  `57f3e96e3df6fcf8fbbcc627b6de9eef245d2c6c` / tree
  `6e0398dffee38efe725f83c78412dba251d15367`;
- pre-U01 accepted forward `main`:
  `95c0aeabf3b76316bd32870ffe6c311be8ad1237`;
- U01 production candidate:
  `d14190cdfe845fdd60629ca9b1eed8d1d2704d44` / tree
  `00f036fcd22a6e3ec6f79c5ddfeb9d210d1418b9`;
- candidate parent:
  `95c0aeabf3b76316bd32870ffe6c311be8ad1237`;
- candidate production change:
  `src/nvda_desk/raw_signal_occurrence_truth/api.py` only;
- complete production diff SHA-256:
  `e1e4752df4fbca13a2e01ace57b0ace554f22fea9084c71736037f7bcf5f87e0`;
- `git fsck --full --no-dangling`: return code 0, no output.

The accepted IRB and BICP hashes were independently checked against the repository bytes:

- IRB:
  `938debe255d68668b0ae60f021d679fc8e3022be6eb050e7f3cd6112818fd342`;
- BICP Markdown:
  `6b2906b92e11bf09fd7f8b188e8ed6555a0a5ae61636909f676f84827601d21f`;
- BICP JSON:
  `5b99cead41fd8d3d372b5ed2ef4558065328b814e0a94c3680162fc6594df5ed`.

## Material inspected

The review read in full the governing `GUARDRAILS.md`, root `AGENTS.md`, current `EXEC_PLAN.md`,
`tests/AGENTS.override.md`, the accepted IRB, BICP Markdown, IWO, Worker U01 evidence, complete U01
production diff/current `api.py`, complete U01 proof file, support module, and positive/negative
mypy specimens. The BICP JSON was inspected for the U01 proof obligations and lineage. No U02
implementation or acceptance was assessed.

The U01 contract proof binds `IA17-PROD-001`, `IA17-PROD-011` and `IA17-PROD-012`, with supporting
`IA17-ARCH-003` and `IA17-ARCH-005`. In particular, `IA17-PROD-011` requires exact v1 contracts at
the A00/M00 typed public boundary with no private-state bypass, while `IA17-PROD-012` prohibits
silent weakening of v1 null/identity/time/provenance semantics.

## Environment and mandatory command results

Exact review runtime/tool versions:

- Python 3.13.5;
- pytest 9.0.3;
- mypy 1.20.1 (compiled);
- Ruff 0.15.11.

The exact project-pinned Python validation tools were provisioned outside the repository and used
only as execution tooling; the supplied full-Git repository remained the sole repository state.

Commands executed on a detached worktree at the exact candidate:

- U01 pytest: `293 passed, 2 failed`;
- strict positive mypy specimen: return code 0;
- strict negative mypy specimen: return code 1 with all 15 intended `STATIC_NEGATIVE` sites
  diagnosed at lines 15, 18, 21, 23, 28, 34, 43, 48, 53, 59, 64, 67, 70, 73 and 76;
- `python -m mypy src --show-error-codes`: success, 15 source files;
- `python -m ruff check src tests tools`: pass;
- `python tools/validate_product_proof.py`: pass, 6 families and 13/13 obligations;
- `python tools/validate_architecture.py`: pass, zero dependency/public-seam violations;
- `python tools/check_dependencies.py`: pass;
- `python tools/check_public_seams.py`: pass;
- `python tools/run_promotion_gate.py --set architecture_kernel`: 74 passed;
- `git diff --check`: return code 0.

Exact command output is preserved in
`implementation/proof/VI13R_U01_REVIEWER_021_COMMAND_LOG.txt`.

## Semantic review of the realised U01 candidate

The candidate correctly establishes the five named v1 payload classes, finite temporal/relation/
assessment discriminants, runtime-distinct identity classes, receipt-only/source-timestamp
rejection, separate command/read facets, and explicit `NotImplementedError` boundaries for later
U02-U05 behaviour. No schedule generation, provider mapping, persistence, packet carriage, replay
or downstream capability is implemented early.

The accepted optional-absence convention is not a new finding here. The pre-implementation proof
history explicitly treats typed `None` in the structural optional field position as lawful absence,
while provider-native null remains a value inside `native_record`; this is materially different
from accepting an untyped null in a required semantic position. The realised candidate preserves
that contextual distinction.

Two other concrete U01 defects remain.

## Worker discrepancy W-U01-F001 — proof-harness contradiction

**Disposition:** proof-layer defect; the production receipt-only law is correct.

The generic allowed-discriminant test replaces only `source_temporal_kind` on the default
observation specimen. That default is a `true_instant` specimen carrying
`source_timestamp_raw="2026-09-20T12:00:04.900000Z"`. The generated `receipt_only` case therefore
retains a provider timestamp and the candidate rejects it at `api.py:267`. The explicit temporal
negative test independently requires exactly that rejection. IRB BC-005 and BC-009 require
`source_timestamp_raw` absent for `receipt_only`.

**Smallest owning-layer repair:** in the generic proof constructor, make the `receipt_only`
discriminant specimen coherent by also setting `source_timestamp_raw` to absence. Do not weaken the
candidate's receipt-only rejection.

## Worker discrepancy W-U01-F002 — mypy path parser

**Disposition:** proof-layer defect; the static negative proposition itself succeeds.

Direct pinned mypy reports a type error at all 15 marked negative sites. The pytest wrapper builds
an absolute `TYPECHECK_NEGATIVE` prefix, runs mypy with repository `cwd`, and mypy emits relative
paths, so the parser records no matching diagnostic lines.

**Smallest owning-layer repair:** normalise both diagnostic paths and the expected specimen path to
the same repository-relative or resolved form before comparing line numbers. Preserve the exact
requirement that all 15 marked sites are diagnosed.

## R021-U01-F003 — mutable `native_record` defeats the U01 fact contract

**Accepted proposition defeated:** IRB BC-005 requires the admitted provider-logical field names and
values in `native_record` to be preserved unchanged; U01 is the public v1 contract layer used by all
later units. The Reviewer brief explicitly requires challenge of mutable state in the realised U01
contract.

**Concrete failure path:** `RawObservationOccurrenceV1` is declared frozen, but its
`native_record` field is a mutable `dict[str, object]` stored by reference. A focused check
constructed an observation from a source dictionary, mutated that source dictionary afterwards,
and observed the already-constructed U01 payload change from `123.45` to `999.99` and gain a new
`Injected` field. Mutating `obs.native_record` directly then changed the value again to `888.88`.
The Worker's claim that the public payload object is immutable/frozen is therefore not true for the
material native payload state.

**Owning layer:** U01 production contract representation, with a missing U01 proof discriminator.

**Smallest required repair:** make `native_record` an alias-safe immutable/read-only snapshot at the
U01 boundary while preserving provider-logical names, values and provider-native null semantics
unchanged. Add a focused U01 proof that mutation of the caller's original container and mutation
through the returned payload cannot alter the constructed occurrence. Do not move admission,
persistence or provider mapping behaviour forward from U03/U05.

## R021-U01-F004 — no lawful public construction path for required identity-bearing payloads

**Accepted proposition defeated:** IWO section 3 assigns construction/source translation to A00;
IWO section 4 requires the M public seam to expose typed representations and command/read facets
sufficient for A00; U01 explicitly requires a public seam shape sufficient for later units.
`IA17-PROD-011` and `IA17-ARCH-005` bind that use to the declared A00 -> M00 public seam rather than
private-member access.

**Concrete failure path:** the public contract constructors require `_ConceptId`, `_ContractId`,
`_ScopePolicyId`, `_EligibilityPolicyRef`, `_CaptureOccurrenceId`, `_ScopePolicyRef`,
`_ObservationOccurrenceId`, `_DeliveryArtifactRef`, `_ProviderId`, `_IngestionSequenceScope` and
`_AssessmentOccurrenceId`, but none of those identity constructors is exported by the public seam;
`RawSignalCatalogueId` is the only public identity export. Supplying ordinary opaque string values
fails immediately (`TypeError: concept_id must use the _ConceptId identity layer`). The proof
support constructs these values by inspecting private field annotations, and the positive mypy
specimen accepts already-constructed payloads as function arguments, so it never proves that A00
can construct the U01 vocabulary lawfully through the declared public seam.

**Owning layer:** U01 public API design and U01 static/public-seam proof.

**Smallest required repair:** provide a typed public construction path inside
`nvda_desk.raw_signal_occurrence_truth.api` for every required identity-bearing U01 payload without
requiring A00 to import/access underscore/private members or use annotation introspection. The
implementation may expose suitable public identity value types or public factories; exact private
helper naming remains implementation freedom. Extend the positive static proof to construct and
use the U01 payloads through only the declared public API. Do not widen semantic ownership or
activate U02 behaviour.

## Final gate effect

The two Worker-observed failures are not product-semantic reasons to weaken the implementation;
they require bounded proof repair. Separately, `R021-U01-F003` and `R021-U01-F004` are concrete
realised U01 implementation/proof defects. Therefore U01 cannot be lawfully promoted from
`d14190cdfe845fdd60629ca9b1eed8d1d2704d44`.

Final Reviewer 021 disposition: **`FAIL / RETURN_TO_WORKER`**.

U02 **remains prohibited** pending the smallest U01 production/proof repairs above and a fresh
independent U01 re-review after the repaired candidate is frozen.
