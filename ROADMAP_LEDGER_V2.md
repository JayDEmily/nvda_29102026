# NVIDIA 2026 — Live Roadmap

## Current position

| Field | Current truth |
|---|---|
| Programme | M00–M15 modular-monolith alpha delivery |
| Branch | `control/atlas-current-path-rebase-gate-c-continuation-v1` |
| Source checkpoint | `2aab666a3c9441728c6701acbd4baa7f71056d97` |
| Gate C protocol | two-step MVP route: `C-NORM → C-PROOF` |
| Current completed module | M13 state kernel accepted |
| Current implementation-open slice | M04 K07 packet protocol |
| Production implementation | open only for bounded M04 K07 Gate D |
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
| M04 packet protocol / K07 | passed — `docs/09.1...` section 9.10 | passed — 239 proof-instrument cases, ten mutant kills, eleven exact production-red cases | `GATE_D_OPEN` |
| M01 source admission | passed | pending focused public-seam family | `C_PROOF_NEXT_AFTER_M04` |
| M07 coefficient/modifier authority | missing K12 identity/version, precedence, bounds and receipt meaning | closed pending norm | `C_NORM_REQUIRED` |
| M08 playbook catalogue | missing K13 catalogue/eligibility decision meaning | closed pending norm | `C_NORM_REQUIRED` |

The PM-011 179-test census, Cycle 01 worker/tester outputs and M04 MLC-A through
MLC-T records remain navigation and challenge evidence. No file-by-file
re-adjudication is required before implementation.

## Immediate next action

Implement the smallest M04 K07 Gate D change:

1. require caller-owned `traceid`, `runid` and `scenarioid`;
2. enforce the admitted role-specific lineage matrix;
3. record the named common and role-specific validation results;
4. reject invalid binding packets and preserve diagnostic/rejection separation;
5. run the admitted K07 proof, affected packet/runtime tests and full suite as
   shadow evidence;
6. checkpoint the completed M04 slice.

After M04, complete M01 minimum proof/implementation, then M07 and M08
normative/proof work. Later modules follow dependency readiness, not paperwork
age or numeric `D-xxx` order.
