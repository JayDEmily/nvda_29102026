# NVIDIA 2026 — Live Roadmap

## Current position

| Field | Current truth |
|---|---|
| Programme | M00–M15 modular-monolith alpha delivery |
| Branch | `control/atlas-current-path-rebase-gate-c-continuation-v1` |
| Resumed source checkpoint | `c9122e9d732f01de5f08af4b366df255270b7d0f` |
| Gate C protocol | two-step MVP route: `C-NORM → C-PROOF` |
| Latest accepted implementation slice | M08 K13 playbook catalogue authority |
| Current active slice | M02 K04 C-PROOF |
| Production implementation | closed for M02 until C-PROOF passes |
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
| M08 playbook catalogue | passed — `docs/07.1...` section 7.8 | passed — 23 focused cases; five mutants killed | `GATE_D_ACCEPTED` |
| M02 financial calendar | passed — `docs/07.1...` section 7.9 | active | `C_PROOF` |

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

M08 K13 Gate D acceptance records 23/23 focused cases, proof-manifest
integrity at 56/56 and the proof executor at 21/21. Tier A moved from 1,365
passed / 274 failed to 1,377 passed / 267 failed: the seven formerly
expected-red K13 nodes resolved, five direct integrity regressions were added
and zero new failing nodes appeared. Tier B remains 49/49. The M08 namespace
is clean across 25 scoped files. Ruff was unavailable because no locked module
is installed; no substitute was used.

The PM-011 census, Cycle 01 worker/tester outputs and historical MLC records
remain navigation and challenge evidence. No file-by-file re-adjudication is
required before implementation.

## Immediate next action

Open M02 K04 `C-PROOF` for the exact `CalendarFactCandidate`,
`FinancialCalendarSnapshot` and `CalendarProjection` public seam. Production
mutation remains closed until the minimum truthful proof is accepted.
