# M01 Relevant-Test Routing Worker Record V1

## Status

`PROPOSED_M01_RELEVANT_TEST_ROUTING_V1_AWAITING_LANE_1AT`

This is a routing proposal only. It does not accept, reject, rank, strengthen, weaken, observe or interpret any test.

## Source checkpoint

| Field | Value |
|---|---|
| Unit | `M01-PROOF-MLC-R-V1` |
| Source branch | `review/parallel-control-r2-accepted` |
| Source commit | `ee67c752d14073a959fda478f31f4466b6952cae` |
| Source parent | `e672b27ca01efbd1f47de27d41fa54733bc73c63` |
| Worker branch | `work/lane-1a-m01-mlc-r-v1` |
| Owner | M01 `source_admission` |
| Boundary | K01 `SourceArtifactEnvelope`; K02 `CaptureReceipt`; K03 `RawSignalBatch` |

The supplied full-history source archive matched the PM launch SHA-256, branch, commit and parent; its worktree was clean and its repository was non-shallow with complete reachable history.

## Bounded question and route law

The accepted M01 proposition is the general source-admission law recorded in `M01_AUTHORITY_PM_REVIEW_V1.md`. The exact current requirement joins retained from its accepted C/D/N mapping are:

- direct M01: `C-001/D-001`, `C-002/D-002`, `C-007/D-007`;
- M01/M03 boundary: `C-003/D-003`, `C-004/D-049/N-01`;
- M01 lineage contribution only: `C-015/D-015`;
- M01 source-time contribution only: `C-025/D-025`.

`C-021/D-021` and `C-048/D-048` remain outside bounded M01 under the accepted mapping and create no M01 route here.

A physical file is classified `M01_CURRENT_CLAIM_ROUTE` only when:

1. it exists in the complete PM-011 physical census;
2. a current row for the bounded C-set names the file in `EXISTING_TEST_DISPOSITION.tsv` or `GATE_C_TEST_AUTHORITY_REGISTER.tsv`;
3. the corresponding retained D-envelope names the same physical file under `Positive Tier A proof` or `Existing Tier A dependants`;
4. the accepted M01 C/D/N mapping and PM review join that requirement to the bounded M01 owner/proposition.

This is a governed join beyond path, directory, import or filename. It routes the file's current claim; it does not decide the claim's admission, tier, adequacy or factual truth.

A census file is classified `LEGACY_SHADOW_UNADMITTED` for this bounded M01 leaf when it has no current join through that complete C/D/N set. The label is relative to bounded M01 only. It does not deny that the same file may have a current claim for another module or proposition.

## Result

| Measure | Count |
|---|---:|
| PM-011 physical candidate universe | 179 |
| `M01_CURRENT_CLAIM_ROUTE` | 20 |
| `LEGACY_SHADOW_UNADMITTED` for bounded M01 | 159 |
| Omitted census paths | 0 |
| Duplicate inventory paths | 0 |
| Routed paths absent from PM-011 | 0 |
| Positive paths lacking a current governed join | 0 |

The complete one-row-per-physical-file result is retained in `raw_validation/mlc_r_v1/PHYSICAL_TEST_ROUTING_INVENTORY.tsv`. The 20 positive chains from census through current test row, C/D/N mapping, accepted M01 owner and current proposition locators are retained in `raw_validation/mlc_r_v1/M01_CURRENT_CLAIM_ROUTE_CHAINS.tsv`.

## Positive physical routes

The current M01 claim routes are:

- external-source contract/interface/transform files through `C-001/D-001` and, for the transform boundary, `C-003/D-003`;
- raw-bundle and raw-capture temporal files through `C-002/D-002`;
- the current ingress identity/DMP file through `C-001`, `C-002`, `C-003` and the M01 lineage contribution of `C-015`;
- the typed-options completion file and its current existing dependants through `C-004/D-049/N-01`;
- the four raw-signal-family files through `C-007/D-007`;
- the two existing prepared-lineage files through the M01 contribution of `C-015/D-015`;
- the two existing source-temporal/calendar-query files and the current policy-version file through the M01 source-time contribution of `C-025/D-025`.

The selected D-envelopes' `Positive Tier A proof` plus `Existing Tier A dependants` sections mechanically normalize to the same 20 unique physical files. No test body, assertion, fixture or runtime behaviour was inspected to reach this result.

## Shadow routing evidence

All 159 shadow rows are individually enumerated in the physical inventory. Their objective route result is the complement of the 20-path current M01 join set inside the complete 179-path PM-011 census.

This exclusion does not rely on a directory, filename or import inference. It relies on absence from every current test-evidence/test-target field for the accepted bounded C-set, reconciled against every selected D-envelope's positive and existing-dependant sections. The explicit D-049 Tier B shadow path remains `LEGACY_SHADOW_UNADMITTED`, consistent with its envelope's `Tier B shadow evidence` section.

The retained-test registry, proof-block registry and PM-011 allocation fields were read as routing controls, but no registry tier or proof-block label was used to override the current C/D/N join result.

## Boundaries preserved

- No production source, physical test, fixture, configuration, proof registry, vocabulary or normative programme document changed.
- No test behaviour was run or observed.
- No assertion was interpreted.
- No Tier A or Tier B admission decision was made.
- No proof design, expected-red work, implementation repair or downstream module work was performed.
- Architecture rows were used only to confirm accepted M01 ownership and traceability, never as independent behavioural authority.

## Evidence

Lane-owned evidence under `raw_validation/mlc_r_v1/` includes:

- the assignment-local `FULL_READ_MANIFEST.tsv`;
- `PHYSICAL_TEST_ROUTING_INVENTORY.tsv`;
- `M01_CURRENT_CLAIM_ROUTE_CHAINS.tsv`;
- `WORKER_CLAIM.md`;
- source, routing, changed-path, Git and fresh-extraction validations with exact exit statuses;
- evidence hashes and verification.

## Next lawful gate

This proposal awaits independent Lane 1AT review. It does not open M01 test or source mutation.
