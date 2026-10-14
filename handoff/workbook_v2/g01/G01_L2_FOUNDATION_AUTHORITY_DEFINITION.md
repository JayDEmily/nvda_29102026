# G01-L2 — V2 foundation scope and definition candidate

**Disposition: PROPOSED/OPEN FOR OWNER DECISION, not accepted foundation authority.**

## Governing boundary

M00 retains admitted raw occurrence truth and typed read-only projections; it does not own any derived D calculation. `M01` is the consumed, registered runtime object identifier, which is proposed to own precisely the `M01-1` fixed, reproducible, descriptive market/source-time calculations rather than all 209 original mathematical rows. `M01-1` is a human-facing V2 capability label, not an independently registrable `M` identity. No current production allocation, registry, catalogue, workbook or public API has been changed. Original M01 semantics/evidence survive historical migration, while original Stage-1/Stage-2 execution ordering is not imported as a V2 ownership constraint.

## Identity and complete direct/transitive dependency accounting

The linked CSV `G01_L2_D001_D209_AUTHORITY_CROSSWALK.csv` uses the **effective 13 October normative CSV** rather than the older workbook as per-signal authority. It reconciles 209/209 unique canonical D IDs, with 114 workbook-proposed M01-1 and 95 downstream working owners. All direct and transitively reachable D predecessors, ultimate R inputs, typed contexts and versioned parameter profiles were recomputed from the effective catalogue and compared with the independently earlier audit. No accounting discrepancies were found. This is **graph-accounting evidence**, not authority that all 114 qualify semantically or are implementable.

## Definition and authority needed

For every M01-1 D ID, the versioned measurement contract must fix the eligible subject/contract, raw field and provider mapping, sampling/anchor/window, units, time/knowledge cutoff, calendar, versioned parameter profile and selection restrictions, exact output shape, insufficient-history refusal, and lineage. Downstream consumers may choose between pre-defined meaningful measurements but may not mutate a foundation measurement's mathematical meaning by altering a parameter object. V2 modules M02–M31 remain proposed peer owners of 95 outputs; private strategy-dependent chain duplication is not a new canonical D identity.

**65 of 114 candidates** are explicitly flagged by prior semantic reviewers for measurement-convention freeze. These flags are not established defects or individually granted authority to choose a convention. The full semantics, local code path and provider-native contracts have not been independently proved row-by-row by this gate, and the 114 candidates are **not admitted** by this document. No blanket owner approval is presumed.

## Separately reviewable findings and decisions

- **D025 (identified discrepancy):** Accepted raw workbook `R039=High`, `R040=Low`, `R037=Last`; `_stage1.py:1354–1361` labels R039 as low and R040 as high. At High=120, Low=80, Last=90, authority formula `(90−80)/(120−80)=0.25`; actual source branch mathematically computes `(90−120)/(80−120)=0.75`. This is *static proof of mathematical field-meaning disagreement*, not an executed public-path result. Requires independently executed public-path witness and separately authorised proof-first repair.
- **D099/D100 (identified source-contract discrepancy):** `R015` in original source workbook is **option right C/P**, not strike. The current `_stage1.py:1430–1481` treats `R015` as a numeric strike and converts it to `Decimal` against IV metadata strike. Test fixtures supplying numeric R015 cannot establish the accepted semantics. A true C/P public-path test must distinguish refusal/exceptions from a lawful skew result. Fix requires a lawful accepted source contract and later separate code repair authority.
- **D009 (vintage classification evidence gap):** Accepted §5 K01 definition distinguishes `initial`, `latest_known_at_cutoff`, `revised`; code `_stage1.py:1188–1224` only emits `initial` or `latest_known_at_cutoff`. Need timestamp/version-aware witness across at least three qualified vintages; original row-level provider identity required.
- **D096/D097/D098/D107/D108 (missing predecessor):** Current original Stage-1 public dispatcher cannot materialise D096 (original Stage-2 kernel), although D096 is a proposed foundation measurement. Distinguish absence of D096 kernel from downstream 4 dependent rows; separate scope required to implement.
- **D117/R075:** R075 explicitly means average option volume (original source workbook) and is retained in accepted D117. No dependency deletion authorised.
- **D123 official open interest:** Controlled identity/version semantics are authorised in the subsequent 11 October amendment to the 11 October D123 clarification; live provider mapping and official-period/revision semantics remain unproved.
- **D138 Level-II depth:** Must distinguish native event-stream reconstruction from complete snapshots before declaring a provider defect; checked book-event semantics remain a source-contract question.
- **D139/D140** have direct `CalculationParameterSet:P_RULE` typed context; their configured insert/delete window/bucket conventions must remain measurement-only and immutable, not a strategy-selectable threshold.

## Gate eligibility outcome

**L2 population reconciliation:** VERIFIED (209 D IDs, 114/95 proposals and transitive graph accounting). **L2 authoritative eligibility freeze:** NOT ACCEPTED — requires per-row semantic and provider/input-convention decisions, owner approval and independent assessment. The next leaf's D025/D099/D100/D009 tests may be conducted against the **already accepted original mathematical/raw authority** independent of whether all 114 are ultimately allocated. Do not change any V2 allocation or claim L2 semantic acceptance based on these tests.
