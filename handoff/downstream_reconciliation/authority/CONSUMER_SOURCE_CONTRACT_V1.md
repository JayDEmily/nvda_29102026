# L01 consumer source contract candidate — native-shaped M00 → M02

**Status: PROPOSED / PARTIALLY GROUNDED; NOT AN ACCEPTED IMPLEMENTATION BRIEF.**

The owner has commissioned R2, which requires exact accepted owner/normative profiles before dependent code. This document records source-grounded facts and isolates remaining policy decisions. Do not treat this draft, the earlier M00 proof or its numerical oracles as an admissible M02 code-authorisation on their own. No product proof has been executed in this tranche.

## Source authority and ownership

- Existing synthetic source and observations: `handoff/planning/m00_brief2_20261027/BRIEF_2_M00_RECONCILED_V3_20261027_1622_AEDT.md` §§1–3 and completed M00 L06 output `handoff/m00_brief2/FINAL_REPORT.md`. M00 is the immutable raw owner, not the native book/quote policy owner.
- Original `handoff/m00_brief2/authority/CONTROL_HISTORY_CONTRACT_V1.md` defines the publicly available observation-history transport. The file's original `PROPOSAL` header is historical; consult completed L06 and independent review rather than inferring current approval from the header.
- `docs/architecture/OWNERSHIP_AND_COMPONENT_LAW.md`, `DEPENDENCY_LAWS.md`, and `IMPLEMENTATION_AUTHORITY_INGRESS.md` govern owner, public seam and exact accepted brief identity. M02 owns reconstructing and interpreting, never writes new M00 facts.
- `handoff/m01_completion/authority/D138_D145_L2_OWNER_APPROVED_DEPENDENCY_AMENDMENT_20261016.md` governs only the amended R dependencies, **not** invented provider event time or completeness.
- L00 inspection and independent review: `handoff/downstream_reconciliation/L00/BASELINE_AND_IMPACT.md` and `L00/INDEPENDENT_REVIEW.md` at source baseline `97f944d51ab9e403250fe76910e2754b50425c73`.

## Existing, directly inspected M00 public input interface

`create_owner(...).reads.list_projected_raw_history` is currently:

```python
def list_projected_raw_history(
    raw_signal_catalogue_id: RawSignalCatalogueId,
    *,
    mappings: Sequence[RawSignalProjectionMappingV1],
    subject_instrument: str | None,
    received_at_or_before_utc: datetime | None,
    event_at_or_before_utc: datetime | None = None,
    limit: int,
    cursor: str | None,
) -> ProjectedRawHistoryPageV1: ...
```

`create_owner(...).reads.list_raw_observation_history` is currently:

```python
def list_raw_observation_history(
    *,
    subject_instrument: str,
    source_provider: str,
    source_variant: str | None,
    received_at_or_before_utc: datetime,
    native_identity_selectors: tuple[tuple[tuple[str, ...], str], ...] = (),
    limit: int,
    cursor: str | None,
) -> RawObservationHistoryPageV1: ...
```

These signatures are copied from `src/nvda_desk/raw_signal_occurrence_truth/api.py` at the L00 baseline, lines 1142–1182. An additive M02 reader protocol can legally expose both methods without extending M00 or accessing raw persistence internals. Do **not** widen the existing `RawProjectionReaderV1` numeric selector to invent event timestamps.

## Grounded native/controlled profile facts

| Fact/profile | Source and identities | Preserved meaning and selection restrictions |
| --- | --- | --- |
| Native SMART stock A4 | provider `foundation-controlled-ibkr-m00-v1`, variant `ibkr-smart-depth/native-v1`, request `STK-SMART-R1`, generation `STK-SMART-G1`, scope `STK1/SMART/G1` | Side `1=BID`, `0=ASK`; operations `0/1/2` insert/update/delete; positions zero-based; receipt-only, provider time absent; 4 callbacks, 5 R roles each; share units. |
| Native SMART CALL C1 | provider `foundation-controlled-ibkr-m00-coherent-v2`, variant `ibkr-smart-depth/native-v2`, scope `OPT-C100/SMART/COHERENT-V2`, generation `OPT-C100-SMART-COHERENT-V2` | CALL identity `NVDA-OPT-C100-CONTROL-1`; distinct from A5 legacy midpoint-100 source; option contract sizes, receipt-only; 3 callbacks and 15 R projections. |
| Native direct shares C2 | same coherent-v2 provider, variant `ibkr-direct-depth/native-v2`; request exchange `SYNTH-DIRECT-EXCHANGE-1`, scope `STK1/DIRECT-EXCH1/GEN1` | One subscribed side book spans MPIDs `ALPHA`,`BETA`; native `marketMaker` is MPID, distinct from requested exchange; 4 callbacks, 6 R roles; no per-MPID position restart. |
| Native direct CALL C3 | coherent-v2 provider, variant `ibkr-direct-depth/native-v2`; CALL, scope `OPT-C100/DIRECT-EXCH1/GEN1` | Same native addressing, option contract sizes. This synthetic specimen does **not** imply option direct-data entitlement or direct PUT coverage. |
| Asynchronous options A2/A3 | provider `foundation-controlled-ibkr-m00-v1`, variant `ibkr-async-l1/native-v1`, distinct CALL `OPT-C100/L1/G1` and PUT `OPT-P100/L1/G1` | Four distinct callback identities each; one native field per callback; no fabricated common event or clock. A2: price bid 1.20, ask 1.40, size bid 10, ask 8; A3: bid 2.20, ask 2.40, sizes 6/4. |
| Atomic shares A1 | provider `foundation-controlled-ibkr-m00-v1`, variant `ibkr-bidask-atomic/native-v1`, id `SYN-L1-STK-ATOMIC-01` | Four R roles from one genuine native tick-by-tick shares quote; its stock co-reference remains valid. |
| Legacy synthetic profiles | old M02 D087/D131/D134–D140/D143 claims and original generation bytes | Retain original side conventions and event-based fields only for their exact **legacy controlled** provenance; do not silently reinterpret the same identity/version as native. |

Subject/right, provider, variant, contract, request, generation, requested exchange, source native callback kind, position, MPID and mapping IDs/versions must be exact AND filters in every native-compatible profile. `None` variant must not become a wildcard; source M00 selects only exact declared variants. All numeric outputs preserve `Decimal` and integer type, and source times remain null where missing. M00 projections remain byte-identical.

## Proposed M02 input and control semantics — needs formal L01 authority

1. M02 owns explicit `receipt_only` vs `true_instant` time-basis types in the new (versioned) lineage and durable record codec; event time is nullable only for the explicitly receipt-based profile. Keep legacy `BookRawLineageV1` and its persisted records readable, with no global relaxation of `_selection.py`.
2. For a receipt-based source, select projected R histories with `event_at_or_before_utc=None`, **inclusive receipt cutoff**, exact subject and role mappings. Consume separately enumerated controls from `list_raw_observation_history` by the exact source and native `_collector` selector paths. Fully exhaust pages under a fixed committed population and deduplicate overlapping generation discovery by immutable observation ID.
3. A control with declared `invalidates=true` invalidates standing state for its exact request/generation. A restart from G1 to G2 is discovered from both the outgoing G1 and incoming G2 boundary queries. Preserve control receipt/scope/sequence/ID. Require complete post-boundary book warm-up from a lawfully established start; presence of new rows does not by itself establish completeness.
4. Sort for enumeration by receipt UTC, ingestion scope, ingestion sequence and ID as in M00 history contract. ID ties give deterministic display order, **not causal order**. If two relevant facts are causally unorderable and the calculation requires an ordered state, refuse; do not infer order from identifier spelling. Separately document what establishes completeness and ordering (see policy decisions below).
5. For native SMART positional events, apply operation to the selected subscribed book side after complete starting state; only then derive bid, ask, slope or rate. For native direct depth, apply updates to one subscribed side book across MPIDs and group completed rows afterward; never treat MPID as the requested exchange.
6. For asynchronous option R033–R036, M02 must hold four distinct constituent identities in derived assembly metadata, filter the correct request/contract/right/generation and enforce an **approved** as-of/cutoff/age/skew policy. Synthetic 250 ms skew and 1000 ms age examples in Brief2 are **not production-approved defaults**.
7. M02 durable occurrence readback must preserve native source/projection identities, optional event time, collector receipt cutoff, control identities, quote members and exact profile/definition/mapping versions. A missing required role or discontinuity means refusal, not a zero result or silent history entry.

## Authority decisions not established by the inspected sources

These cannot be created by this draft or replaced by worker judgement:

- **A01 — receipt/event clock and causality:** an authorised M02 versioned input/time-selection policy for receipt-only book mutation and control ordering, including ties, generation restart and the definition of sufficient warm-up. M00 only supplies immutable transport.
- **A02 — option assembly:** an authorised synthetic M02 membership/as-of, skew, age and stale/missing/refusal policy for both CALL and PUT (without extrapolating to live market policy). `250/1000 ms` is available only as a controlled fixture proposal.
- **A03 — direct concentration scope:** an authorised definition of which C2 reconstructed side rows/levels enter grouping and whether both sides contribute to D143 HHI; the example 6/2 and HHI 5/8 is conditional on grouping *all four* C2 rows and must not overwrite the old per-venue-top-one model.
- **A04 — carrier and proof admission:** an accepted additive typed M02 carrier/codec shape, exact implementation-ready brief SHA/binding, and approved immutable claim/generation/case allocation for each changed source profile. Older accepted claims are not new-native admission.
- **A05 — D145:** remains **PAUSED**. A differently based receipt-clock K17 model would need independent explicit new authority; it is not silently included in this G1 choice.

**Disposition:** G1/L01 is a source-grounded candidate, not `AUTHORITY_READY`. Any L02–L12 code depending on A01–A04 is `BLOCKED` pending the exact approval/ingress required by root R2. No provider-source field or financial mathematics is invented to bypass these decisions.
