# Unit 3 C-NORM Alignment — Typed Ingress and Canonical Composition

## Governing proposition

Unit 3 introduces no new source-admission or composition meaning. It implements
the accepted M01/M00 boundary already stated by:

- `docs/03.1_DOMAIN_MODEL_WORKING.md`, which requires an input-family-specific
  typed payload contract and forbids shape inference or fabricated source facts;
- `docs/04.1_TECHNICAL_ARCHITECTURE_WORKING.md`, which assigns provider-field
  mapping and construction of the typed native carrier to the external adapter
  or source reader;
- `docs/05.1_GUARDRAILS_WORKING.md`, which forbids generic dictionaries at
  strongly typed payload seams and requires missing authority to fail closed;
- the accepted M01 authority record and implementation, which make the
  registered `SourceFamilyContract.payload_model` the exact family payload
  contract; and
- `docs/11.1_NATIVE_ARCHITECTURE_BLUEPRINT_WORKING.md` propositions
  `M00-COMP-003`, `M00-COMP-008`, `M00-COMP-009` and `M00-UPSTREAM-001` through
  `M00-UPSTREAM-005`.

## Exact implementation delta admitted

1. `SourceAdmissionRequest.typed_payload` becomes a concrete Pydantic model,
   not a mapping that M01 later coerces.
2. M01 may expose a bounded transport-translation method that resolves the
   exact registered family/contract/version first and constructs that family's
   concrete payload model from JSON-shaped material.
3. `SourceAdmissionService.admit` accepts only an instance of the resolved
   contract's payload model and revalidates a detached copy before admission.
4. M00 may delegate upstream transport translation to that injected M01 seam,
   then construct the existing typed `UpstreamPreparationCommand`; it may not
   inspect or infer provider payload meaning itself.
5. CLI and ASGI preparation routes may call that M00 delegation path. Direct
   programmatic M00 callers continue to supply the exact typed command.

The legacy raw-bundle loader and mutable compatibility API remain noncanonical
and unselected by the M00 package. This unit does not repair them or grant them
M01 authority.

## Identity and scope ceiling

Translation preserves every supplied source, contract, schema, provider,
channel, temporal, capture and limitation fact. It creates no source, capture,
packet, trace, run, scenario, policy or time identity. Unknown contracts,
missing typed payload material and payload-contract mismatch fail before owner
execution.

## Proof route

Current M01 public-seam proof owns rejection of a mapping at the admission
request seam and acceptance of the exact registered concrete payload. Current
M00 upstream and entry-adapter proof owns delegated JSON translation and exact
typed command construction. The affected M01, M00 and entry cones must be green
before Unit 3 closes.
