# VI-13R Reviewer 032 — IWO-U04 Receipt Evidence / Assessment Disposition

**Date:** 2026-09-24
**Role:** fresh independent `TESTER` / Reviewer 032
**Reviewed candidate:** `dc3b448191a2b2d3528ffb576b1ebc2c56839991`
**Candidate tree:** `3c7a42eb215d708a0f8d8db37727133ecc234275`
**Disposition:** `PASS`

## 1. Scope and lineage

Reviewer 032 reviewed only repaired IWO-U04. The rejected predecessor is
`e7eb44119bdf7fb22abacae8291788619792c96a`; Reviewer 031 finding `R031-U04-F001` was classified
`ISOLATED` and routed for one mechanism-level repair. U05 was not assessed or implemented.

The previously authorised Tester fixture-independence rule was carried into this lineage at
`6d90d86200a2139ed2a2d47511630d0c58edad6d` before disposition. That governance-only carry-forward
changed no candidate production/test bytes.

## 2. R031-U04-F001 closure

The repaired candidate closes the Reviewer-031 mechanism:

1. assessment presence derives from capture-local admitted observations plus accepted eligibility
   authority, not from optional receipt-relation materialisation;
2. omitting the optional relation command does not convert otherwise eligible in-slot evidence to
   `zero_received`;
3. admitted in-slot evidence with unavailable eligibility authority fails closed;
4. receipt time is not used as the system-knowledge/commit-visibility surrogate;
5. lawful no-evidence, ineligible and out-of-slot zero states remain intact;
6. same-ID retry remains idempotent; and
7. later eligible evidence uses a new immediate-predecessor-superseding assessment rather than
   mutating the earlier assessment.

A direct authority-derived public-seam sequence, independent of Worker convenience fixtures, proved
items 1-3 and an expanded matrix exercised the preserved zero, retry and supersession behaviours.

Reviewer 032 separately observed that an assessment whose asserted `evidence_as_of_ts_utc` precedes
the observation receipt timestamp still sees the currently admitted observation. This does not
establish a U04 defect: BC-008 identifies the field as system-knowledge time but current U04 law does
not provide a historical query/commit clock, and Reviewer 031 explicitly prohibited receipt time from
being used as that substitute. Reviewer 032 therefore did not invent a new temporal rule.

## 3. Independent evidence

On exact repaired candidate `dc3b448...`:

- U04 proof: 32/32 passed;
- direct fixture-independent public-seam challenge: PASS;
- expanded direct state/sequence matrix: PASS;
- U01-U04 excluding exactly three mypy-invoking test bodies unavailable in this sandbox:
  413 passed / 3 deselected;
- architecture/bootstrap excluding exactly two mypy-invoking tests: 72 passed / 2 deselected;
- product-proof, structural architecture, dependency and public-seam validators: PASS;
- diff check: PASS;
- strict Git integrity: exit 0 with five existing unreachable dangling blobs reported diagnostically.

The Tester sandbox lacks mypy and Ruff. Worker-preserved exact-pinned 416/416, mypy/Ruff and 74/74
evidence remains separately attributable and was not relabelled as independently rerun.

## 4. Recurrence classification

`R031-U04-F001` remains an `ISOLATED` first-U04 finding and is now closed. Reviewer 032 established no
new materially related or independent U04 failure, so no `RECURRENT_CLASS` escalation is opened.

## 5. Disposition

`PASS`.

Exact repaired U04 candidate `dc3b448191a2b2d3528ffb576b1ebc2c56839991` may be lawfully promoted
with preserved ancestry. U05 becomes authorised only after that promotion succeeds and the next
Worker is freshly routed.
