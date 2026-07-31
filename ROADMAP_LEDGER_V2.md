# NVIDIA 2026 — Live Roadmap

## Current position

| Field | Current truth |
|---|---|
| Programme | M00–M15 modular-monolith alpha delivery |
| Branch | `control/atlas-current-path-rebase-gate-c-continuation-v1` |
| Resumed source checkpoint | `c9122e9d732f01de5f08af4b366df255270b7d0f` |
| Gate C protocol | two-step MVP route: `C-NORM → C-PROOF` |
| Latest accepted implementation slice | M07 K12 coefficient/modifier authority |
| Current active slice | M08 K13 C-PROOF |
| Production implementation | closed for M08 until C-PROOF passes |
| Live/paper/production claim | closed |

## Why the route changed

The former M04 sequence used seven commits and 34 changed files after the Atlas
path repair, adding 3,442 lines while changing no M04 production behaviour.
The protocol now follows the normative requirement to use the smallest proof
combination that establishes the accepted claim.

Historical MLC records remain evidence. They are not mandatory future leaves.

## Gate C conversion

| Module | Normative closure | Minimum proof | State |
|---|---|---|---|
| M13 state kernel | passed | independently passed | accepted implementation retained |
| M04 packet protocol / K07 | passed — `docs/09.1...` section 9.10 | passed — 271 admitted cases plus retained partial case | `GATE_D_ACCEPTED` |
| M01 source admission | passed | passed — 18 focused public-seam cases | `GATE_D_ACCEPTED` |
| M07 coefficient/modifier authority | passed — `docs/07.1...` section 7.7 | passed — 20 focused cases; five mutants killed | `GATE_D_ACCEPTED` |
| M08 playbook catalogue | passed — `docs/07.1...` section 7.8 | open — minimum truthful K13 public-seam proof | `C_PROOF_ACTIVE` |

M04 Gate D acceptance records zero new Tier A shadow failure nodes relative to
`c9122e9`, one resolved node, all 49 Tier B tests passing, and a clean M04
vocabulary boundary. Pinned Ruff was unavailable because the configured mirror
returned HTTP 404 for locked `orjson==3.11.7`; that unavailable check is
recorded rather than substituted.

M01 Gate D acceptance records 18 focused proof cases passing, proof-manifest
integrity at 54/54, the proof-executor contract at 21/21, and four repaired M01
compatibility cases passing directly. Tier A moved from 1,312 passed / 271
failed to 1,334 passed / 267 failed, with zero new failing nodes and four
resolved M01 nodes. Tier B remains 49/49; Tier C contains no tests. The global
vocabulary shadow remains blocked by the same 50 pre-existing shared candidates,
and pinned Ruff was unavailable because the locked `pytokens==0.4.1` wheel
returned HTTP 404 from the configured mirror.


M07 Gate D acceptance records 20/20 focused proof cases, 30/30 directly affected
legacy compatibility cases, proof-manifest integrity at 55/55 and the proof
executor at 21/21. Tier A moved from 1,345 passed / 274 failed to 1,354 passed /
267 failed: the seven formerly expected-red K12 nodes resolved, two new
model-copy authority-bypass regressions pass and zero new failing nodes exist.
Tier B remains 49/49. The M07 namespace is clean across 16 scoped files. Pinned
Ruff was unavailable because the locked `openpyxl==3.1.5` wheel returned HTTP
404 from the configured mirror; no unpinned substitute was used.

M08 K13 C-NORM acceptance defines immutable catalogue/definition identity and
version law, mandatory posture/context facts, exact rejection and lawful
stand-down states, authority-owned ordering/tie-break, eligibility-lead meaning,
decision fingerprinting and bounded lifecycle carriage. The M08 vocabulary
namespace contains the exact `PlaybookDefinition`, `PlaybookCatalogue` and
`EligibilityDecision` contracts and is clean across 20 scoped files. Existing
vocabulary parity is intentionally expected red because it still hard-codes the
pre-M08 namespace set; no test was changed during normative closure.

The PM-011 census, Cycle 01 worker/tester outputs and historical MLC records
remain navigation and challenge evidence. No file-by-file re-adjudication is
required before implementation.

## Immediate next action

Open M08 K13 `C-PROOF`:

1. encode the accepted K13 outcomes in a reference subject without production code;
2. prove invalid authority, posture-block and valid-empty stand-down are distinct;
3. prove catalogue priority and the explicit identity/version tie-break defeat caller order;
4. prove deterministic lineage, eligibility-lead meaning and lifecycle/foreign-authority closure;
5. leave the canonical M08 package assertions expected red until Gate D implementation.

Later modules follow dependency readiness, not paperwork age or numeric `D-xxx`
order.
