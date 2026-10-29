# VI-13R Reviewer 031 — IWO-U04 Receipt Evidence / Assessment Disposition

**Date:** 2026-09-24
**Role:** fresh independent `TESTER` / Reviewer 031
**Reviewed candidate:** `e7eb44119bdf7fb22abacae8291788619792c96a`
**Candidate tree:** `ea104900fcaf8e2db4177df3909956f464d6a918`
**Disposition:** `FAIL / RETURN_TO_WORKER`

## 1. Scope and lineage

Reviewer 031 reviewed only IWO-U04. U03 promotion ancestry was confirmed before the U04 candidate;
U05 was not assessed or implemented.

This is U04's first VI-13R rejection/repair cycle. There is no prior U04 Reviewer-failure / Worker-
repair lineage, so the finding is classified `ISOLATED` under ExecPlan section 6.11.

## 2. Finding R031-U04-F001

**Title:** assessment evidence visibility depends on optional relation materialisation and a receipt-
time proxy.

**Severity:** Critical.

**Owning layer:** U04 M-owner assessment derivation plus bounded implementation-coupled U04 proof.

BC-007 permits `CaptureReceiptEvidenceRelation.v1` materialisation to be omitted. BC-008 requires an
assessment to represent eligible committed raw-observation evidence visible to its own transaction at
system-knowledge `evidence_as_of_ts_utc`. The admitted U04 product-proof metadata also states
`relation materialisation is not required`.

The candidate does not satisfy that separation. `append_assessment` scans only
`state.relations_by_capture`; it neither inspects admitted observations nor invokes the eligibility
authority unless the optional relation command was previously called. Its visibility predicate is
`relation.received_ts_utc <= evidence_as_of_ts_utc`, so observation receipt time is also used as a
surrogate for evidence commit/knowledge visibility.

An independent public-seam canary admitted an in-slot observation under an injected eligibility
authority returning exact `True`, intentionally omitted relation materialisation, then appended an
assessment. The eligibility authority was called zero times and the assessment returned
`zero_received`. With the same in-slot observation and no eligibility authority injected, the
assessment again returned `zero_received`, masking unresolved eligibility as zero.

This is a material false negative: the semantic assessment can depend on whether an optional relation
object happened to be materialised, rather than on the eligible committed observation evidence.

## 3. Required bounded repair proposition

The next U04 candidate must establish all of the following without entering U05:

1. assessment outcome is derived from capture-local eligible admitted/committed observation evidence
   visible to the assessment's own transaction, not from optional relation-materialisation state;
2. omitting receipt-evidence relation materialisation cannot turn otherwise eligible visible evidence
   into `zero_received`;
3. where an admitted in-slot observation requires eligibility adjudication, absent required
   eligibility authority fails closed rather than manufacturing zero;
4. `received_ts_utc` remains receipt time and is not used as a substitute for system-knowledge or
   commit-visibility time;
5. existing lawful ineligible/out-of-slot/no-evidence zero behaviour remains intact;
6. relation role/nonclaims, append-only immediate-predecessor assessment chaining, same-ID retry,
   capture-locality and U01-U03 accepted behaviour remain intact; and
7. add bounded implementation-coupled regressions for this mechanism. Do not begin PostgreSQL,
   restart reconciliation, provider mapping semantics or other U05 work.

If satisfying item 4 requires a new authority value that is not already fixed, the Worker must stop
`BLOCKED` on that exact gap rather than substituting receipt time or another clock.

## 4. Independent evidence

On exact candidate `e7eb441...`:

- U04 bounded proof: 29/29 passed;
- U01-U04 excluding exactly three mypy-invoking test bodies unavailable in this sandbox: 410 passed /
  3 deselected;
- product-proof, structural architecture, dependency and public-seam validators: PASS;
- candidate diff check: PASS;
- strict Git integrity: exit 0 with five unreachable dangling blobs diagnosed.

The Tester sandbox lacks the `mypy` and `ruff` modules. Worker-preserved pinned static/lint evidence is
retained as Worker evidence and is not relabelled as independently executed.

The green bounded proof does not override the independently demonstrated semantic escape.

## 5. Disposition

`FAIL / RETURN_TO_WORKER`.

U04 is not promotable. U05 remains prohibited pending a bounded repair and fresh independent U04
review.
