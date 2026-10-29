# D132 adversarial test-design correction (2026-10-11)

While extending the controlled public D132 proof, a first version of
`test_reconstructed_d132_future_book_event_refuses` asserted that a book-update
record received after the knowledge cutoff must invalidate the whole calculation.
That assertion failed: M01 produced a lawful historical D132 occurrence.

Inspection of the actual selected M00 raw lineage showed the future
`bid-push` event excluded, with prior inserts still available. The correct
accepted temporal proposition is **no use of ineligible future information**,
not absence whenever an optional future event exists. The subsequent test
asserts the exact historic score `452`, rather than the `459` obtained with the
eligible bid-push, and checks the future UUID is absent from lineage.

No production change or weakening of an established valid regression occurred;
this correction concerns a newly authored, invalid adversarial test premise.
The initial failure was observed in the worker execution transcript; no saved
initial failing log is claimed. The final full test run is preserved separately.
