# VI-12R U04 Reviewer-031 repair evidence

**Status:** Worker candidate frozen; independent Reviewer 032 required.

Reviewer 031 rejected U04 candidate `e7eb44119bdf7fb22abacae8291788619792c96a` because assessment
presence depended on optional materialised relation state and observation receipt time was used as a
system-knowledge/visibility proxy. The bounded successor is
`dc3b448191a2b2d3528ffb576b1ebc2c56839991` / tree
`3c7a42eb215d708a0f8d8db37727133ecc234275`.

The repair removes `relations_by_capture` as the assessment evidence source. Assessments now derive
from the currently admitted owner observation state for the exact capture, applying `[start,end)`
receipt locality and the capture's admitted effective-policy eligibility authority. Optional relation
materialisation is therefore not a prerequisite. Required eligibility authority missing in the
presence of in-slot evidence fails closed. `received_ts_utc` is not compared with
`evidence_as_of_ts_utc`; it remains only the receipt-time/capture-slot fact. No new commit clock,
provider-event validity, finality/SLA or U05 durability semantics are introduced.

Three bounded regressions prove eligible evidence without relation materialisation, fail-closed
missing eligibility authority for in-slot evidence, and stable same-ID assessment retry after later
evidence. Exact pinned Worker validation records U04 32/32, U01-U04 416/416, mypy/Ruff and all
current product/architecture/dependency/public-seam controls green, and architecture/bootstrap plus
promotion 74/74. These results establish Worker evidence only, not U04 acceptance.
