# VI-09 Product-Proof Admission/Control Design

## Status

**PM DESIGN — AUTHORISED VI-09 ONLY**

This design implements no Raw Signal product behaviour and authors no physical Raw Signal product test. It defines the minimum separate product-proof control surface required before VI-10 can author adversarial physical proof.

## Exact source state

- PM source commit: `8c4d7374f479c249bb1de5d202a5a8d5fbd2a94b`
- PM source tree: `eab8e12d60ea46e70afb8db51581433d63eeb6a5`
- accepted recovered VI-08 implementation commit: `c3cda85fe32e43a88292a80c38de3a4e696e2240`
- accepted recovered VI-08 implementation tree: `c13b1cb10eec5ef6076c386a1fd2a3b41005aa6b`

## Required authority readback completed for this design

The design was derived after reading the current repository governance, current architecture proof law/current admitted architecture/bootstrap proof corpus, the exact routed METHOD-006 authority, and preserved Tier A/B/C proof-method evidence.

Exact METHOD-006 baseline:

- commit `7c76b1dc87a9773e92841cae47e34b3b50190614`
- tree `3cf7d5e78a490611076a6317f3b709b692cdf553`

Exact routed authority bytes:

- N04 `5bbe3c0cd3e813b167241574e22a9791289f481657be590e0c860e5d37549ca3`
- Vocabulary Governance `2706f3ae0cb65e548c6acabff710e8d1e53876c76523febe4ccdccf68a0a861f`
- N06 `de0d1e529d12251e048ac35e8eeedf87d179099d5ba35055d9e10f34c371b9c9`
- N18 `4cbf5bc045a2203639fa10246ee52e9597258a25e992379057ced431b39cf989`
- N15 `62bbaed0306e1cf3e85de3e482284f967a971e5ff806d75e7674dd7c35d8403e`
- N19 `d46567a2594657e26c54d3c0bb45e44c4adadca58b8ca349d516f980dc7504fb`

Current repository proof-method authorities additionally include `docs/architecture/TEST_AND_PROMOTION_KERNEL.md` and `tests/AGENTS.override.md`. Historical Tier A/B/C material from preserved pre-reset architecture commit `d24f9626a23b526384668b3cb26ee811b235eb5c` was read as method evidence only; its identities, tiers, admissions and green states are not current authority.

## Exact task/proof authority

- BICP Candidate 005 JSON SHA-256: `5b99cead41fd8d3d372b5ed2ef4558065328b814e0a94c3680162fc6594df5ed`
- IRB SHA-256: `938debe255d68668b0ae60f021d679fc8e3022be6eb050e7f3cd6112818fd342`
- implementation target after VI-08: current active owner `M00`, package `nvda_desk.raw_signal_occurrence_truth`, public seam `nvda_desk.raw_signal_occurrence_truth.api`
- separate architecture aggregate remains `architecture_kernel`

Current product proof obligations, exactly thirteen:

1. `IA17-PROD-001`
2. `IA17-PROD-002`
3. `IA17-PROD-003`
4. `IA17-PROD-004`
5. `IA17-PROD-005`
6. `IA17-PROD-006`
7. `IA17-PROD-007`
8. `IA17-PROD-008`
9. `IA22R01-PROD-009`
10. `IA17-PROD-010`
11. `IA17-PROD-011`
12. `IA17-PROD-012`
13. `IA17-PROD-013`

`IA17-PROD-009` is predecessor lineage only and is forbidden from the current product aggregate.

All thirteen current product obligations have `tier_treatment: NOT_CLASSIFIED`. VI-09 must not relabel them Tier A/B/C. The historical tier framework is method evidence; it is not product-proof admission authority.

## Control proposition

VI-09 must make this statement mechanically true:

> The repository contains one separate, exact-authority-bound product-proof control surface for the current Raw Signal Occurrence Truth claim. It knows the exact thirteen product obligations and the exact implementation identity, admits no physical product family by file placement, cannot absorb architecture obligations or historical predecessor proof IDs, cannot introduce Tier A/B/C product classification, and cannot report a successful product aggregate while the physical family registry is empty or obligation coverage is incomplete.

This is control readiness only. It is not product proof.

## Required surface

Create a clearly separate product-proof namespace:

- `config/product_proof/authority.yaml`
- `config/product_proof/families.yaml`
- `config/product_proof/aggregates.yaml`
- `schemas/product_proof_authority.schema.json`
- `schemas/product_proof_family.schema.json`
- `schemas/product_proof_aggregate.schema.json`
- `tools/validate_product_proof.py`
- `tools/run_product_proof_gate.py`
- `implementation/proof/VI09_PRODUCT_PROOF_CONTROL_EVIDENCE.md`

No `tests/product/**` file is created in VI-09.

## Authority binding requirements

`authority.yaml` must bind:

- exact BICP path/hash;
- exact IRB path/hash;
- current implementation target `M00` plus package/public seam;
- exact six routed authority IDs `AUTH-N04`, `AUTH-VG`, `AUTH-N06`, `AUTH-N18`, `AUTH-N15`, `AUTH-N19`;
- exact thirteen current product proof IDs;
- forbidden predecessor `IA17-PROD-009`;
- explicit product tier treatment `NOT_CLASSIFIED`;
- architecture proof axis identifier `architecture_kernel`, as a separate non-substitutable axis.

The validator must derive/verify these facts against the BICP bytes rather than trusting duplicated local labels.

## Family contract for VI-10

The VI-09 schema/validator must require every later admitted physical family to provide at least:

- unique family ID and exact physical path;
- current implementation target/boundary;
- exact proof level;
- one or more current product proof obligation IDs;
- exact proposition/authority bindings that are permitted by the BICP routed authority;
- authoritative fixtures/inputs/state;
- dependency substitutions;
- all four N15 case classes, each containing concrete cases or an explicit bounded `not_applicable_reason`:
  - lawful positive;
  - prohibited/false-positive;
  - missing mandatory authority;
  - lawful optional absence;
- expected failure signal(s);
- exact command;
- declared environment and material versions;
- limitations/adjacent non-claims;
- `tier_treatment: NOT_CLASSIFIED`.

Physical file location must never admit a family. The validator must require exact registry parity once physical product tests exist.

## Aggregate contract

Create one product aggregate: `raw_signal_occurrence_truth_product`.

At VI-09 its family set is truthfully empty and its state must be explicitly incomplete, not green. The validator may accept this as a valid pre-implementation control configuration, but the runner must return failure/non-success because no physical product families have been admitted and the thirteen obligations are not physically covered.

A later ready aggregate may become runnable only when:

- every referenced family is admitted and physically present;
- the union of family obligation IDs covers exactly the required current product-obligation set for the claim;
- no forbidden/architecture obligation is present;
- registry/aggregate membership is internally consistent;
- all family metadata satisfies the N15 contract.

## Required adversarial control checks

Before VI-09 completion, demonstrate that the validator/runner reject at least:

1. wrong BICP hash;
2. missing current product obligation;
3. substitution of predecessor `IA17-PROD-009` for `IA22R01-PROD-009`;
4. architecture obligation contamination;
5. Tier A/B/C product classification drift;
6. unadmitted physical product test path;
7. family missing an N15 case/metadata requirement;
8. proposition/authority binding outside the BICP-routed authority;
9. duplicate family path/ID;
10. aggregate marked ready with incomplete obligation coverage;
11. empty physical-family set being reported as successful proof.

Rejecting corruption earlier at schema validation is acceptable and stronger than reaching a later semantic validator, provided the failure is attributable and the governed valid state remains accepted.

## Non-goals / prohibitions

VI-09 must not:

- author a physical Raw Signal product test;
- implement Raw Signal product behaviour;
- mutate `config/proof/**` or otherwise insert product propositions into `architecture_kernel`;
- relabel product obligations Tier A/B/C;
- change BICP/IRB/METHOD-006/architecture normative authority;
- activate P01, K01, replay, external effects/accounts or downstream consumers;
- claim product proof PASS.

## Acceptance evidence

VI-09 is complete only if:

- valid control configuration validates from exact committed bytes;
- all required adversarial control probes reject as intended;
- empty/incomplete aggregate cannot produce success;
- existing `architecture_kernel` promotion remains green and unchanged in membership;
- mypy/Ruff and relevant repository checks are green;
- final diff contains no physical product test or product implementation;
- committed evidence records exact commands/results and commit/tree.
