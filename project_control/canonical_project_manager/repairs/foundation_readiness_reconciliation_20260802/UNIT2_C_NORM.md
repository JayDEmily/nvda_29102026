# Unit 2 C-NORM Alignment — Prepared Identity and Packet Boundary

## Governing proposition

Unit 2 introduces no new normative meaning. It implements the existing public
seam between M03 prepared-data authority and M04 DMPV3 carriage:

- `docs/04.2_PREPARED_DATA_CONTRACTS_WORKING.md` makes the typed,
  fingerprint-valid `PreparedDataEnvelope` the M03 authority object and makes
  raw compatibility snapshots non-authoritative;
- `docs/09_DMPV3_PROTOCOL_CORE.md` requires caller-owned occurrence identity,
  exact producer occurrence identity, typed role data and source/derived
  lineage;
- `docs/09.1_DMPV3_PROTOCOL_WORKING.md` requires prepared-context packets to
  carry `PreparedContextIdentity`, derive from the prepared identity, preserve
  source artifacts and prepared fingerprint, and fail closed when required
  identity or owner validation is absent;
- the M03 and M04 module records retain those same ownership and validation
  boundaries at their accepted Gate D states.

## Exact implementation delta admitted

`nvda_desk.preparation.context_packet.build_prepared_context_packet` may:

1. revalidate the snapshot's canonical `PreparedDataEnvelope` at the public
   boundary;
2. project only the frozen `PreparedContextIdentity` into packet data;
3. require explicit caller-owned execution context, packet time, module version
   and module instance identity;
4. derive prepared/source/fingerprint lineage only from the revalidated M03
   envelope;
5. invoke the complete K07 common and prepared-role owner-check set; and
6. express only envelope-admitted optional limitations as degraded validation,
   with an explicit non-binding consumer restriction.

It may not fabricate governed identity or lineage from a raw compatibility
snapshot, opaque payload, local clock, packet ID or fallback string.

## Proof route

The current-blocking M03 proof owns the cross-boundary propositions. Retained
upstream-cognition compatibility tests may be re-authored only to follow the
same current law. Gate D opens only after the focused M03/M04, packet, runtime,
upstream-cognition and M00 affected cones establish the delta.
