# Foundation Readiness Reconciliation — Unit Validation

## Unit 2 — prepared identity and packet boundary

### Outcome

Unit 2 passes its bounded gate. The M03/M04 public seam now accepts only a
revalidated `PreparedDataEnvelope`, projects typed `PreparedContextIdentity`,
derives packet lineage and fingerprints from that envelope, and requires the
caller-owned execution, producer and occurrence facts already required by
DMPV3/K07 law. Raw compatibility snapshots cannot be promoted into governed
packets. The admitted serial-runtime packet path likewise fails closed when
caller-owned packet authority is absent; its non-packet compatibility fallback
remains available.

No normative meaning was added. `UNIT2_C_NORM.md` records the pre-existing M03,
M04 and K07 authority used for the implementation.

### Proof

| Surface | Result |
|---|---:|
| Unit 2 affected Tier A cone | 618 passed; 0 failed |
| M04 current proof | 271 passed; 0 failed |
| Physical Tier A | 1,916 passed; 49 failed; 1,965 total |
| Physical Tier B | 91 passed; 0 failed |
| Proof authority | PASS — 201 families, 203 paths, 73 blocks |
| Proof-block manifest | PASS — 73 blocks |
| Vocabulary namespaces | PASS — 13/13; zero unresolved candidates |

The complete physical Tier A run closes 198 baseline failures and adds five
positive/fail-closed propositions. Its remaining 49 failures are retained in
exact JUnit evidence for Units 3–5; they do not fall inside the now-green Unit 2
dependency cone. The residual families include unadmitted parallel-risk input,
legacy runtime callers without explicit authority, absent next-gate types,
remaining scenario/role/version facts and distinct API assertions.

Formatting shifted exact occurrence identities after initial vocabulary
adjudication. Thirty-two unique final-tree occurrences were therefore
re-adjudicated in the occurrence-scoped disposition register. Together with the
earlier Unit 2 adjudications, all 13 namespace scans are clean. No canonical
vocabulary label or alias changed.

### Evidence and gate

- `UNIT2_C_NORM.md`
- `evidence/UNIT2_PHYSICAL_TIER_A_JUNIT.xml`
- `FULL_READ_MANIFEST.tsv`

Unit 2 may close. Repository-wide readiness remains open at 49 physical Tier A
failures; Unit 3 may open on typed M01 ingress and canonical composition.

## Unit 1 — exact proof universe and baseline truth

## Outcome

Unit 1 passes. The canonical v4 authority admits every current physical test
file exactly once: 203 physical paths, 203 admissions, zero missing and zero
stale. The earlier 32-file result is a legacy-section join defect, not a current
admission gap.

The supplied locked wheelhouses created the declared CPython 3.13.5
environment. Complete physical proof was then reproduced without changing
production behaviour:

| Surface | Result |
|---|---:|
| Physical Tier A | 1,713 passed; 247 failed; 1,960 total |
| Physical Tier B | 91 passed; 0 failed |
| Physical Tier C | 5 passed; 0 failed |
| Curated `alpha_current` | 802 passed; 0 failed |
| Proof authority | PASS — 201 families, 203 paths, 73 blocks |
| Proof-block manifest | PASS — 73 blocks |
| M14 contract proof | PASS — 18 tests |

The Tier A result exactly reproduces the comparative arithmetic. Its 247 nodes
are concentrated in eight partitions and are preserved in JUnit evidence. A
single caller-owned `scenario_id` failure accounts for 204 nodes; unadmitted
K07 packet roles account for 17. The remaining 26 nodes divide among explicit
module-version/trace identity, missing next-gate contract surfaces and 13
distinct assertions. This supports cause-sized execution beginning at the
prepared identity/packet boundary.

## Changes

- Activated this subordinate plan across the parent plan, roadmap and process
  overlay.
- Added the active pack to the M14 singular-control validator and its Tier B
  contract proof.
- Corrected current governance statements that treated the historical
  legacy-section join as canonical admission truth.
- Retained the comparative audit and its 32-path artefact unchanged as
  historical evidence.

No file under `src/` changed. No production or product-test proposition was
weakened, skipped, xfailed, retired or reclassified. The only test change proves
the M14 active-control state introduced by this unit.

## Evidence

- `evidence/UNIT1_PROOF_UNIVERSE.json`
- `evidence/PHYSICAL_TIER_A_JUNIT.xml`
- `FULL_READ_MANIFEST.tsv`

Successful Tier B, Tier C and curated results are retained as concise counts;
only the red Tier A route retains raw JUnit for exact node identity.

## Gate

Unit 1 control truth is closed. Unit 2 may open on the prepared-context/M04
owner-identity boundary. Repository-wide readiness remains open because
physical Tier A is red.
