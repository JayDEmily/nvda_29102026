# M04 Authority Tester Review V1

## Assignment and verdict

| Field | Value |
|---|---|
| Tester | `Lane 2AT` |
| Worker | `Lane 2AW` |
| Unit | `M04-PROOF-MLC-A-V1` |
| Module / contract | `M04 packet_protocol` / `K07 DmpV3Packet` |
| Worker candidate revision | `R2` |
| Worker candidate commit | `b24260fa27248fae61f2537dc59905f62099fcee` |
| Tester branch | `test/lane-2a-m04-mlc-a-v1` |
| Verdict | `PASS` |

`PASS`

The repaired worker candidate is suitable for Project Manager integration review. The worker's central disposition follows current numbered meaning, preserves the M04 packet-carriage/validation boundary, and exposes the material role-specific authority gap without borrowing normative authority from tests, code or Atlas evidence.

## Known true

1. The PM launch archive has SHA-256 `983d0ffdb977a75a4cd3063bd9d645d24ae7817ff47620e543f9e1f8bfb5a381` and reconstructs cleanly on `review/parallel-control-r2-accepted` at `ee67c752d14073a959fda478f31f4466b6952cae` with complete Git history.
2. The R2 worker archive has SHA-256 `1276a1d7dc64f166e89dc71baa0efb5de54cf7644b76a4e301a34c497049e5fd` and reconstructs cleanly at worker commit `b24260fa27248fae61f2537dc59905f62099fcee` with append-only ancestry through the two R1 commits and two R2 repair/evidence commits.
3. The worker changed only `project_control/canonical_project_manager/modules/M04/M04_AUTHORITY_WORKER_RECORD_V1.md` and `project_control/canonical_project_manager/modules/M04/raw_validation/mlc_a_v1/**`. No source, physical test, configuration, numbered authority, architecture artefact, global control or other lane path changed.
4. Current numbered authority establishes the common DMPV3 shell, deliberate inter-module carriage, owner-supplied identities and lineage, packet-occurrence versus source/domain identity separation, emission-time semantics, role-exact validation, replay occurrence/equivalence distinctions and no transfer of domain ownership to M04.
5. Current numbered authority does not enumerate the mandatory/conditional/optional/not-applicable identity, lineage and validation matrix for every governed packet role. `docs/09.1_DMPV3_PROTOCOL_WORKING.md:61` defers the lineage subset, lines `83-91` require exact role checks, and line `161` prohibits inference from defaults.
6. D-010 retains a real conflict between a reference-packet test permitting absent/defaulted runtime context and the proposed C-010 assertion rejecting missing caller-owned context. That test conflict is evidence of the unresolved exception boundary; it is not authority to select either rule.
7. Independent challenge found no numbered proposition granting a reference-packet exception for omitted caller-owned `traceid`, `runid` or `scenarioid`. The worker's missing-authority return question is therefore materially supported.
8. M04 remains carriage and validation only. It does not absorb M01 source admission, typed payload ownership, downstream domain decisions, state ownership, persistence truth or identity/time fabrication.

## R2 defect closure

| Defect | Result | Evidence |
|---|---|---|
| `T2A-01` incorrect line locator | `PASS` | The worker record now cites `docs/11.1_NATIVE_ARCHITECTURE_BLUEPRINT_WORKING.md:50`; independent revalidation confirms line 50 is the exact surface 5.6 current-truth row. |
| `T2A-02` invalid JSON selector | `PASS` | `.modules[] | select(.module_id=="M04") | .owns` executes under `jq -e` and returns `"DMPV3 envelope validation and packet carriage only"`. |
| `T2A-03` incomplete exact-locator validation | `PASS` | Independent execution found 63 literal locator occurrences and 63 matching validation rows, with no missing/substituted coverage and zero failures. Required workbook ranges were separately inspected using `artifact_tool`. |

## Independent falsification result

The tester challenged whether numbered authority itself permits a financial-calendar/reference packet to omit caller-owned runtime context. Searches and full reading of the numbered packet, ownership, architecture and guardrail surfaces found no such role-specific exception. The exact role matrix remains intentionally deferred, while historical tests disagree. This challenge did not falsify the worker's disposition and confirmed that resolving the conflict requires new numbered meaning rather than selecting whichever existing test is convenient.

## Ruled out

- `FAIL_REPAIRABLE` is ruled out: all three bounded R1 defects are corrected and independently reproducible within the authorised worker write set.
- `HARD_BLOCK` is ruled out: the baseline, ancestry, history, architecture allocation and scope are valid, and no new scope or authority is required to assess the worker's truthful blocked disposition.
- Canonical acceptance is not claimed. The Project Manager remains the only integration and acceptance authority.

`SUITABLE_FOR_PM_M04_MLC_A_INTEGRATION_REVIEW`
