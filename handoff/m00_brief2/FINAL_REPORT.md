# M00 Brief 2 final handoff — verified synthetic SQLite scope

28 October 2026. Independent final reviewer `/root/l06_final`. Reviewed accepted leaf tree `d14cb0102bfdf405bc157c7e4fa3e0d1714fb41a`; runtime candidate `63e68751107035d2747a1591700a45a83181ca11`, immutable generation5 `e03468aec24f9dec4d152c9ed44135d6f6cf26704f735b0cfeb0c706b8b1ded7`.

The authorised synthetic public admission → SQLite → public projection/history/control discovery → portable output chain is complete for the exact brief. This is no claim of live acquisition, downstream calculation, PostgreSQL execution or feed entitlement. D145 remains PAUSED.

## Brief gates

| Brief gate | Disposition | Primary evidence relative to handoff/m00_brief2 |
| --- | --- | --- |
| 0 baseline/authority | VERIFIED | authority/BASELINE_AND_SCOPE.md; evidence/L00/INDEPENDENT_REVIEW.md |
| 1 independent oracle | VERIFIED | fixture_manifest_v1.json; evidence/L01/INDEPENDENT_REVIEW.md |
| 2 public SQLite proof | VERIFIED | evidence/L05/strict-green.log; evidence/L02–L04 independent reviews |
| 3 bounded corrections | VERIFIED | evidence/L02/REPAIR.md; evidence/L04/CONTRACT_REVIEW.md and REPAIR.md; evidence/L05/CONTROL_DOMAIN_REPAIR.md |
| 4 deterministic publication | VERIFIED | outputs/L05_verified/acceptance_manifest_v1.json and reproduction_v1.json |
| 5 independent handoff | VERIFIED | evidence/L06/FINAL_REVIEW.md and artifact-verification.json; enclosing final checkpoint integrity receipt |

## Exact positive coverage

Every scenario is asserted by `tests/product/m00_brief2/test_ibkr_native_projection.py::test_native_scenarios` and `test_ibkr_history.py::test_history_scenarios`, with its explicit parameter below. `test_export.py::test_export_pipeline` verifies all published rows and clean-checkout reproduction. Actual data: `outputs/L05_verified/actual_m00_output_v1.jsonl`. Exact full-row JSON multiset independently equals the three family oracles plus the control oracle; this check compares values, types, lexical Decimal scale and metadata, not just counts.

| Scenario parameter | Observations | Projections | Required distinction retained |
| --- | ---: | ---: | --- |
| A1 | 1 | 4 | one atomic STK callback |
| A2 | 4 | 4 | four independent CALL callbacks |
| A3 | 4 | 4 | four independent PUT callbacks |
| A4 | 4 | 20 | SMART stock five roles |
| A5 | 3 | 15 | isolated legacy CALL prices |
| A6 | 2 | 10 | SMART PUT one level per side |
| B | 7 | 35 | 26 Oct namespace and seven literal IDs |
| C1 | 3 | 15 | coherent CALL V2 context |
| C2 | 4 | 24 | direct stock MPID/source exchange |
| C3 | 4 | 24 | conditional direct CALL MPID/source exchange |
| Total | 36 | 155 | Five controls additional, never extra R187 values |

## Negative coverage

All following cases have actual isolated SQLite replay results in `outputs/L05_verified/negative_outcomes_v1.json`, indexed by case_id, and passed the export proof. The listed native/history test is the explicit parameter of `test_native_negative` or `test_history_negative`; control rows use `test_ibkr_controls.py::test_control_discoverability`. Actual supplementary absence results are in `actual_absence_outcomes_v1.json`.

| ID | Requirement demonstrated | Assertion family |
| --- | --- | --- |
| N01 | Native side1/0 preserved | native |
| N02 | Receipt-only admission and receipt history | native/history |
| N03 | Fabricated receipt-only source time rejected; fresh absence | native |
| N04 | Event cutoff excludes receipt-only, receipt selection retains facts | history |
| N05 | Distinct tied IDs retained; UNKNOWN_TIED_RECEIPT_SCOPE_SEQUENCE published | history |
| N06 | Five independent omissions preserve other typed facts, missing roles absent | native |
| N07 | Insert/update/delete, positions and zero-size preserved | native |
| N08 | Separate error317 publicly discoverable; no R187 error operation | controls |
| N09 | Error316/reconnect/gap/restart lifecycle discoverable | controls |
| N10 | Subject/right/source/request/generation/exchange isolation | history |
| N11 | Foreign option callback contract retained; four IDs | native |
| N12 | Equal batch receipt does not collapse distinct callback IDs | native |
| N13 | Post-cutoff history excluded, full observation retained | history |
| N14 | Missing book field remains absent, completeness NOT_ASSERTED | native |
| N15 | Identity/cutoff enumeration independently of known control IDs | controls |
| N16 | Identical retry, changed-payload rejection, original retained | history |
| N17 | Direct MPID remains distinct from requested exchange | native |
| N18 | Missing R001 absent; valid typed collector receipt equals envelope UTC | native |

## Production changes, failures and accepted evidence

The complete M00 production diff from D143 is only the additive UTC datetime codec tag in `_native_codec.py` and additive generic observation-history page/read/facet wiring in `api.py`. Original payload fields, prior methods, persistence protocol/tables/adapters and downstream definitions are unchanged. `CONTROL_HISTORY_CONTRACT_V1.md` exact SHA `3ea7ec1be2fb7eb3422d0aed380a35fb68e17dfb77306582573338f874426708` was independently approved after the missing-public-read witness, before implementation. The new owner read interprets no error/control policy: caller-supplied string identity paths select immutable observations. Lifecycle interpretation and before/after union are declared consumer metadata.

L02 baseline19/20 exposed an admitted UTC datetime failing SQLite encoding. Minimal codec correction passed20/20 and relevant original SQLite30/30; the initial historical child-import environment failure23/30 is retained separately, resolved by offline editable project installation. L04 baseline35/36 exposed missing public control discovery despite successful known-ID persistence. Approved additive read passed36/36 plus original SQLite30/30. L05 generation4 passed36/37 but failed supplemental-control DTO validation against the narrower positive units schema; first-failure/ preserves output and NOT_ATTEMPTED reproduction. The generation5 domain-correct container retains lawful nulls and all typed control facts; no frozen schema was weakened. Recovery passed37/37 and clean reproduction.

The authoritative latest command is `PYTHONPATH=src M00_EXPORT_EVIDENCE=<external-path> python tools/run_product_proof_gate.py --aggregate m00_brief2`: 37 passed in62.13s, exit0, exact candidate/generation above, retained `evidence/L05/strict-green.log`. Existing original SQLite evidence is 30 passed in31.93s at `88eefd9f721ff74e364e7700b4d75e14ecc84c86`, in `evidence/L04/original-sqlite-regression.log`. Git comparisons independently establish that all production source/old raw SQLite proofs/frozen guardrails are byte-unchanged since that L04 candidate, and tools/tests/config/implementation/schemas unchanged since the L05 runtime candidate. Subsequent accepted-leaf changes were documentary/output publication only. No successful product suite was rerun solely for L06 or workspace recovery.

Relevant recurrence class closure was reviewed, including L01 permissive/portable schema, L02–L04 exact typed fresh-read adequacy, and L05 publication domain/first-failure handling. Original findings/repairs and failed generations remain recoverable. Full persisted comparisons and separate direct reviewer sequences support omission/state-transition claims; no reliance exclusively on a Worker composite fixture is claimed.

## Deliverables and hashes

`outputs/L05_verified/portable_output_v1.tar.gz` contains actual data, independent input/oracle fixtures, schemas/mappings, acceptance/reproduction manifests and REPLAY.md. The cumulative checkpoint also contains the complete Git history and source replay tool. Dataset hashes independently rechecked in L06:

- `actual_m00_output_v1.jsonl`: `70583a82602ebf30fa4d9c3f0731746fd4c99479902e33738bc45a6cdf37a281`
- `actual_control_output_v1.jsonl`: `5b808cd12cbe566aa26e41c11935cb3efce5f6258299925cb14ed97739267501`
- `negative_outcomes_v1.json`: `576cd3674da7ce0c576fc41d2b28139c4be85c17bbc3968c24ed2920b9e6e505`
- `actual_absence_outcomes_v1.json`: `bd0faf848a3f40eaa583b82838a639b8ad16e68d6b74bdabf07a15deb665f14c`

Portable package SHA256: `4ed3f4c6cae23ecb245b50ba301dafe03d24fc20d3833c865d79d4e71faadb86`. All29 signed fixture hashes match the accepted manifest `0628fb8a7196b44d0322ea438db7a180eb0f97b50f36cece0b2d0739dd0f4e04`. Four deterministic dataset hashes match the retained clean second-checkout reproduction. Producer-time manifest review-pending status is historical provenance; the later separate hash-specific acceptance manifest carries actual independent PASS.

## Inspection and practical limits

This final reviewer read current governing files/plan and original brief §§0–7; complete history/control/export proof source, exporter and negative replay paths; full L00/L01/L02/L04-contract/L05 reviews and relevant repair lineage; complete delivered main rows during independent JSON comparison, negative outcome structure and specific ambiguity/omission/rejection/carrier records. M00 source inspection was the full actual production diff plus relevant public/projection/persistence paths, not a fresh exhaustive review of every historical owner/module. Earlier full-source inspections remain attributed to their leaf reviewers. Primary logs, immutable generation and output hash links were inspected directly. Final verification is artifact/Git evidence assessment, not newly executed M00 runtime certification.

EXPECTED_SYNTHETIC_OUTPUT_AUTHORISED, ACTUAL_M00_OUTPUT_VERIFIED and SQLITE_READBACK_VERIFIED apply to the commissioned synthetic scope. POSTGRES_RUNTIME_DEFERRED and LIVE_IBKR_UNVERIFIED remain explicit. The retained PostgreSQL inline native codec's datetime gap remains a known static limitation. Ordinary SQLite read transactions are mode=ro/query_only; create=False constructor validation still uses mode=rw, so no filesystem permission boundary is certified. New observation-history cutoff excludes the unsupported maximum datetime by explicit refusal; cursors guarantee fixed-population traversal, not concurrent snapshot isolation. ID tie-break is display order, not causal proof. C3 is a conditional direct-CALL specimen, not direct PUT/feed entitlement certification. No standing-book completeness/re-warm-up/skew policy/microstructure/D calculation or deployed collector is certified. These exclusions are not unresolved mandatory SQLite brief items. D145 and unrelated signal work remain paused.
