# NVIDIA 2026 — Live Roadmap

## Current position

| Field | Current truth |
|---|---|
| Programme | M00–M15 modular-monolith alpha delivery |
| Branch | `work/m09-k11-k14-capital-authority-v1` |
| Current branch source checkpoint | `330becaa99e862f40ae4066d35e21ae9788ddcae` |
| Gate C protocol | module delivery route: `C-NORM → C-PROOF → Gate D`, with concise evidence retention |
| Latest accepted implementation slice | M09 K11 final-risk join and K14 bounded fresh-capital authority |
| Current active slice | paused for clean full-history checkpoint after M09 Gate D acceptance |
| Production implementation | M09 Gate D accepted; M10 has not started |
| Live/paper/production claim | closed |

## Why the route changed

The former M04 sequence used seven commits and 34 changed files after the Atlas
path repair, adding 3,442 lines while changing no M04 production behaviour.
The protocol now follows the normative requirement to use the smallest proof
combination that establishes the accepted claim.

Historical MLC records remain evidence. They are not mandatory future leaves.

## Evidence-retention correction

Required validation still executes. From this branch onward, ordinary module
acceptance retains one concise reproducible summary rather than committed full
successful stdout/stderr, duplicate baseline/current transcripts or JUnit XML.
The summary records commands, environment, exit status, counts, failing-node
identity and delta, material warnings and Git state. Raw output is retained only
for novel regressions, non-determinism, material environment failures or
risk-triggered independent review.

The latest accepted comparable checkpoint supplies the baseline node set unless
its admitted tests, environment, command route or comparability changed. This
removes duplicated evidence generation without weakening proof or shadow
validation.

## Gate C conversion

| Module | Normative closure | Minimum proof | State |
|---|---|---|---|
| M13 state kernel | passed | independently passed | accepted implementation retained |
| M04 packet protocol / K07 | passed — `docs/09.1...` section 9.10 | passed — 271 admitted cases plus retained partial case | `GATE_D_ACCEPTED` |
| M01 source admission | passed | passed — 18 focused public-seam cases | `GATE_D_ACCEPTED` |
| M07 coefficient/modifier authority | passed — `docs/07.1...` section 7.7 | passed — 20 focused cases; five mutants killed | `GATE_D_ACCEPTED` |
| M08 playbook catalogue | passed — `docs/07.1...` section 7.8 | passed — 23 focused cases; five mutants killed | `GATE_D_ACCEPTED` |
| M02 financial calendar | passed — `docs/07.1...` section 7.9 | passed — 33 focused cases; six mutants killed | `GATE_D_ACCEPTED` |
| M03 prepared data / field resolution | passed — `docs/07.1...` section 7.10 | passed — 29 focused cases; six mutants killed; adversarial reconciliation accepted | `GATE_D_REPAIR_ACCEPTED` |
| M05 serial cognition | passed — `docs/07.1...` section 7.11 | passed — 37 focused cases; seven mutants killed; state/result identity repair accepted | `GATE_D_REPAIR_ACCEPTED` |
| M06 parallel risk | passed — `docs/07.1...` section 7.12 | passed — 33 focused cases; seven mutants killed; threshold/version repair accepted | `GATE_D_REPAIR_ACCEPTED` |

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

M02 K04 Gate D acceptance records 33/33 focused cases, proof-manifest integrity
at 57/57 and the proof executor at 21/21. Tier A moved from 1,390 passed / 274
failed to 1,414 passed / 263 failed: the seven formerly expected-red K04 nodes
and four bounded compatibility nodes resolved, 13 direct integrity regressions
were added and zero new failing nodes appeared. Tier B remains 49/49. The M02
namespace is clean across 23 scoped files. Ruff and Black were unavailable
because the locked modules are not installed; no substitute was used.

M03 K05/K06 Gate D acceptance records 25/25 focused cases, proof-manifest
integrity at 58/58 and the proof executor at 21/21. Tier A moved from 1,426
passed / 270 failed to 1,444 passed / 258 failed: 12 M03 public-seam and
normative-integrity nodes resolved, six direct integrity cases were added and
zero new failing nodes appeared. Tier B remains 49/49. The M03 namespace is
clean across 16 scoped files and 72 governed occurrences. The unsplit Tier A
route did not terminate after reaching 97%; the complete admitted set was run
in non-vocabulary and vocabulary partitions for the exact node comparison.
Ruff and Black were unavailable because the locked modules are not installed;
no substitute was used.

M05 K08/K09 Gate D acceptance records 32/32 focused cases, proof-manifest
integrity at 59/59 and the proof executor at 21/21. Tier A moved from 1,457
passed / 265 failed to 1,476 passed / 258 failed: the seven formerly
expected-red K08/K09 nodes resolved, 12 direct integrity cases were added and
zero new failing nodes appeared. Tier B passed 49/49 in two explicit
partitions; the combined route did not terminate after partial progress and is
recorded as a suite-order warning. The M05 namespace is clean across 35 scoped
files and 81 governed occurrences. Ruff and Black were unavailable because the
locked modules are not installed; no substitute was used.

M06 K10 Gate D acceptance records 30/30 focused cases, proof-manifest integrity
at 60/60 and the proof executor at 21/21. Tier A moved from 1,489 passed / 265
failed to 1,508 passed / 256 failed: the seven formerly expected-red K10 nodes
and two module-global compatibility-state nodes resolved, ten direct integrity
cases were added and zero new failing nodes appeared. Tier B passed 49/49 in
two explicit partitions. The all-vocabulary route did not terminate after
partial progress, so all 17 vocabulary files were run separately in baseline
and current trees. The M06 namespace is clean across 58 scoped files and 145
governed occurrences. Ruff and Black were unavailable because the locked
modules are not installed; no substitute was used.

The PM-011 census, Cycle 01 worker/tester outputs and historical MLC records
remain navigation and challenge evidence. No file-by-file re-adjudication is
required before implementation.

## M03/M05/M06 adversarial repair acceptance

The repair admitted 12 exact red cases at proof baseline `6d03237` and now passes 99/99 focused cases. The original positive/metamorphic checks pass 8/8, proof manifests pass 60/60, the proof-executor contract passes 21/21 and Tier B passes 49/49. Complete comparable Tier A moved from 1,508 passed / 268 failed to 1,520 / 256: all 12 admitted nodes resolved and zero new failing nodes appeared. All 17 vocabulary files were run individually; 100 cases pass and the same three baseline failures remain. Evidence is under `project_control/canonical_project_manager/repairs/chat_audit_repair_20260731/`.

## M09 K11/K14 Gate D acceptance

M09 acceptance records 32/32 focused cases, three bounded C-036 compatibility
cases, proof-manifest integrity at 61/61 and the proof executor at 21/21. Tier B
passes 49/49. A mandatory detached proof review closed capital/policy numeric
domains before Gate D; a later boundary probe found and closed upward percentage
rounding and decimal replay-identity defects before acceptance.

Complete Tier A moved from 1,537 passed / 271 failed at hardened proof baseline
`66f6bc4` to 1,555 / 253: 18 exact M09/C-036 nodes resolved and zero new failing
nodes appeared. The vocabulary partition remains 100 passed / three unchanged
failures; the M09 namespace audit is clean across 27 files and 297 governed
occurrences. Evidence is under
`project_control/canonical_project_manager/modules/M09/validation/m09_k11_k14_v1/`.

The current M06 evaluator still reports explicit unknowns when three owner facts
are unavailable, so this acceptance does not claim complete M00 end-to-end
eligibility.

## Immediate next action

Publish the clean full-history checkpoint for accepted M09 K11/K14 Gate D. The
next semantic unit is M10 execution-gateway authority; it has not started.
