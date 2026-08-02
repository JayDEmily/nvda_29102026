# Foundation Readiness Reconciliation — Unit Validation

## Unit 5 — residual physical failure adjudication

### Outcome

Unit 5 passes its bounded gate after a proposition-preservation audit required
by the user before acceptance. The 46 physical Tier A failures retained by Unit
4 are green through five current-law families: typed options/common-context
carriage; explicitly non-binding parallel-risk compatibility; fail-closed serial
orchestration with caller-owned candidate identity; downstream carry/review
lineage; and direct M13/M12 transaction/replay ownership.

The physical Tier A count remains exactly 1,990 tests. Three node names changed
only under explicit authority mappings: the failing capital packet-role proof
and two formerly green partial-mapping fallback proofs. No test was skipped,
xfail-marked, retired, broadened or weakened. The audit found one dropped
input-fingerprint assertion in the provisional Unit 5 tree; that assertion was
restored before acceptance. Replay replacement assertions were strengthened to
test absent reproduced-output identity and fingerprint directly. Every changed
test node is mapped in `evidence/UNIT5_TEST_CHANGE_AUTHORITY_REGISTER.tsv`.

### Test-change audit

The register contains the 46 Unit 4 red nodes plus every additional Unit 5 test
node or shared test helper changed by the implementation. Each record states the
old node, governing authority, original behavioural proposition, replacement
assertion and red-to-green evidence. Only these dispositions occur:

- production repair with the assertion unchanged;
- authority-complete fixture or current-owner binding with the proposition
  unchanged or strengthened; and
- normative supersession of an expressly non-admitted role or direct field
  location, with the original domain proposition retained before the current-law
  fail-closed or owned-location assertion.

The authority-audit route passes 46/46: 45 original failing node IDs plus the
mapped capital-role replacement. No ambiguous authority was
adjudicated by convenience, and no retirement disposition exists in Unit 5.

### Proof

| Surface | Result |
|---|---:|
| Unit 4 red propositions after assertion audit | 46 / 46 passed — 45 original node IDs plus 1 authority-mapped replacement |
| Unit 5A typed options/common context | 8 / 8 focused; 274 / 274 affected passed |
| Unit 5E M13 transaction / M12 replay ownership | 6 / 6 focused; 176 / 176 owner suites passed |
| Unit 5B packet-role and diagnostic compatibility | 31 / 31 focused; 105 / 105 affected passed |
| Unit 5C serial orchestration/candidate identity | 4 / 4 focused; 319 / 319 affected passed |
| Unit 5D carry/review evidence | 2 / 2 focused; 246 / 246 affected passed |
| Signed `alpha_current` at audited commit `35ebb93` | 19 / 19 blocks; 811 / 811 tests passed |
| Physical Tier A | 1,990 passed; 0 failed; 1,990 total |
| Unit 4 failure-proposition delta | 45 same-node failures green; 1 authority-mapped failure green; 0 new or retained failures; test count unchanged |
| Physical Tier B / Tier C | 91 / 91; 5 / 5 passed |
| Proof authority / block manifest | PASS — 201 families, 203 paths, 73 blocks; 73 / 73 definitions |
| Vocabulary namespaces | PASS — 13 / 13; zero unresolved candidates; 80 exact Unit 5 dispositions |
| Unit 5 Python write-set static checks | PASS — Ruff, Black, byte compilation and `git diff --check` |

One Tier B direct-construction fixture supplies the required
`MARKET_REGIME_POLICY_VERSION`; its original posture/permission assertions are
unchanged. Eighty vocabulary rows are exact occurrence dispositions only. They
admit no canonical label or alias; eleven were renewed after restored or
strengthened assertions shifted line-scoped occurrence identities.

The static PASS is scoped to the 42 Python files changed by Unit 5. Full-tree
`ruff check .` remains non-green at 138 historical errors with output exactly
identical to the Unit 4 base `11699fe`; Unit 5 adds no Ruff finding and makes no
full-tree lint-clean claim.

### Evidence and gate

- `UNIT5_C_NORM.md`
- `evidence/UNIT5_TEST_CHANGE_AUTHORITY_REGISTER.tsv`
- `evidence/UNIT5_TEST_CHANGE_AUDIT.md`
- `evidence/UNIT5_46_NODE_AUTHORITY_AUDIT_JUNIT.xml`
- `evidence/UNIT5_PHYSICAL_TIER_A_JUNIT.xml`
- `evidence/UNIT5_PHYSICAL_TIER_B_JUNIT.xml`
- `evidence/UNIT5_PHYSICAL_TIER_C_JUNIT.xml`
- `evidence/UNIT5_PHYSICAL_TIER_A_DIFFERENTIAL.json`
- `evidence/UNIT5_ALPHA_CURRENT_PROMOTION_RECEIPT.json`
- `evidence/UNIT5_VOCABULARY_NAMESPACES.txt`
- `evidence/UNIT5_PROOF_AUTHORITY.json`
- `evidence/UNIT5_PROOF_BLOCK_CHECK_RECEIPT.json`
- `evidence/UNIT5_STATIC_VALIDATION.json`
- `FULL_READ_MANIFEST.tsv`

Unit 5 may close. Unit 6 now owns only the one-commit readiness closure in
`CONTINUATION.md` section 10. New planned feature development remains closed
until that checkpoint passes.

## Unit 4 — structural integrity families

### Outcome

Unit 4 passes its bounded gate as four independently proved semantic slices.
M12 no longer imports M10 for replay fingerprinting and retains equivalent
fingerprint semantics through an owner-local primitive. Nineteen named
process-wide policy exports now expose immutable containers without changing
their accepted content. The vocabulary scanner no longer observes its own five
machine projection-header forms while retaining identical human prose. The
compatibility API no longer owns untyped veto/risk state or fabricates required
exit/close identities, and walk-forward authority packets require explicit
dataset identity and fingerprint.

Legacy compatibility loaders and routes were not selected as canonical
substitutes. No test was skipped, xfailed, weakened or retired, and no residual
physical failure was accepted by this unit.

### Proof

| Surface | Result |
|---|---:|
| Unit 4A expected-red / repaired M12 dependency proof | 1 failed + 1 passed → 2 passed |
| Complete M12 contract / M12 proof block / M13 restart proof | 24 / 24; 24 / 24; 10 / 10 passed |
| Unit 4B expected-red / repaired governed-policy proof | 19 failed → 19 passed |
| Unit 4B affected cone | 662 passed; 23 retained failures; 685 total; zero added failures |
| Unit 4C expected-red / repaired scanner proof | 1 failed → 1 passed |
| Complete vocabulary-scanner proof | 19 / 19 passed |
| Unit 4D expected-red / repaired authority proof | 3 failed + 1 passed → 4 passed |
| Unit 4D direct affected proof / complete affected cone | 15 / 15; 174 / 174 passed |
| Curated `alpha_current` physical membership | 811 passed; 0 failed |
| Physical Tier A | 1,944 passed; 46 failed; 1,990 total |
| Unit 3 failing-node delta | exactly 3 removed; 0 added; 46 retained |
| Physical Tier B / Tier C | 91 / 91; 5 / 5 passed |
| Proof authority / block manifest | PASS — 201 families, 203 paths, 73 blocks; 73 / 73 definitions |
| Vocabulary namespaces | PASS — 13 / 13; zero unresolved candidates |
| Static checks | PASS — Ruff, Black, compilation and `git diff --check` |

The physical Tier A universe grows by 22 new green Unit 4 cases. Its only
failing-node reduction is the three admitted Unit 4D propositions concerning
untyped API-owned state, fabricated exit/close authority and absent replay
dataset identity. The exact 46-node residual set remains visible for Unit 5.

The 35 Unit 4C and two Unit 4D vocabulary occurrence changes were exact
line-identity renewals against unchanged dispositions. No canonical vocabulary
label or alias changed.

### Evidence and gate

- `UNIT4_C_NORM.md`
- `evidence/UNIT4_ALPHA_CURRENT_PROMOTION_RECEIPT.json`
- `evidence/UNIT4_PHYSICAL_TIER_A_JUNIT.xml`
- `evidence/UNIT4_PHYSICAL_TIER_A_DIFFERENTIAL.json`
- `evidence/UNIT4B_POLICY_EXPECTED_RED.txt`
- `evidence/UNIT4C_SCANNER_EXPECTED_RED.txt`
- `evidence/UNIT4D_API_IDENTITY_EXPECTED_RED.txt`
- `FULL_READ_MANIFEST.tsv`

Unit 4 may close. Repository-wide readiness remains open at 46 physical Tier A
failures. Unit 5 may now adjudicate those residual families one semantic cause
at a time.


## Unit 3 — typed ingress and canonical composition

### Outcome

Unit 3 passes its bounded gate. `SourceAdmissionRequest` now accepts only a
concrete Pydantic payload model. M01 owns exact family/contract/version lookup,
constructs the registered payload type from transport JSON, rejects mismatched
models, and revalidates a detached payload before admission. M00 delegates
transport translation to the injected M01 owner and preserves typed requests
while composing the existing upstream command. CLI and ASGI entry routes use
that delegation.

The legacy raw-bundle compatibility loader remains runnable but is not selected
by the canonical transport route. No provider, capture, trace, scenario, run,
packet or domain identity is fabricated. One Tier C direct caller was
re-authored only to pass the concrete payload model it already constructs; no
production compatibility shim was added.

### Proof

| Surface | Result |
|---|---:|
| Unit 3 expected-red proof before implementation | 3 failed; 25 deselected |
| Unit 3 targeted proof after implementation | 3 passed; 25 deselected |
| Complete M01/M00/entry affected cone | 62 passed; 0 failed |
| M01 admitted proof block | 20 passed; 0 failed |
| M00 upstream proof block | 8 passed; 0 failed |
| M00 final-composition proof block | 16 passed; 0 failed |
| Transport-adapter proof block | 15 passed; 0 failed |
| Curated `alpha_current` physical membership | 809 passed; 0 failed |
| Physical Tier A | 1,919 passed; 49 failed; 1,968 total |
| Physical Tier B | 91 passed; 0 failed |
| Physical Tier C | 5 passed; 0 failed |
| Proof authority | PASS — 201 families, 203 paths, 73 blocks |
| Proof-block manifest | PASS — 73 blocks |
| Vocabulary namespaces | PASS — 13/13; zero unresolved candidates |
| Static checks | PASS — Ruff, Black, compilation and `git diff --check` |

The complete physical Tier A run adds and passes the three Unit 3 propositions.
Its 49 failing node IDs are exactly the same set retained by Unit 2: zero added
and zero removed. Unit 3 therefore introduces no new Tier A failure family and
does not claim that the remaining structural or residual families are accepted.

A direct boundary probe also confirms that a forged concrete payload type is
rejected and transport translation returns detached registered payload state.
Thirty-eight pre-existing vocabulary occurrences shifted line identity because
of the bounded implementation; each was renewed against its unchanged semantic
disposition. No canonical label or alias changed.

### Evidence and gate

- `UNIT3_C_NORM.md`
- `evidence/UNIT3_PHYSICAL_TIER_A_JUNIT.xml`
- `FULL_READ_MANIFEST.tsv`

Unit 3 may close. Repository-wide readiness remains open at 49 physical Tier A
failures. Unit 4 may open only the structural-integrity findings as separate
narrow semantic units.

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

## Units 1–4 retrospective test-preservation audit — 2026-08-03

The repository-wide rule in `AGENTS.md` was applied to every test/support surface changed from accepted base `3876f171...` through Unit 4 `11699fed...`. The exact inventory is 20 files and 47 changed top-level surfaces. No physical test file was deleted or renamed and no skip, xfail or equivalent mechanism was added.

Four under-preserved replacements were corrected: two FWD-004 packet identity/summary branches, FWD-009 prepared packet trace/lineage, and FWD-005 API method/process-state absence. Every changed surface is mapped in `evidence/UNIT1_4_TEST_CHANGE_AUTHORITY_REGISTER.tsv`.

| Surface | Result |
|---|---:|
| Altered-file cone | 439 passed; 0 failed; 0 skipped |
| Physical Tier A | 1,990 passed; 0 failed; 0 skipped |
| Physical Tier B | 91 passed; 0 failed; 0 skipped |
| Physical Tier C | 5 passed; 0 failed; 0 skipped |
| Proof authority | PASS — 201 families, 203 paths, 73 blocks |
| Proof-block definitions | PASS — 73/73 |
| Vocabulary | PASS — 13/13 namespaces, 0 candidates |

Verdict: **PASS**. Units 1–4 contain no unrecorded test retirement; the four incomplete proposition replacements have been restored without reopening obsolete compatibility authority.
