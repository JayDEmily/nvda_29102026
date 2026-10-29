# L04 independent semantic acceptance — PASS

Reviewer and sole strict executor `/root/l04_independent_review`, 27 October
2026. Accepted clean production/proof candidate
`88eefd9f721ff74e364e7700b4d75e14ecc84c86`; unchanged Brief2 immutable
generation3 SHA256
`d3b58bfeb1684138b73db35a9a21c4d5bf424aa3b7f9fc856ffe7966ef5dd504`;
approved control-history contract SHA256
`3ea7ec1be2fb7eb3422d0aed380a35fb68e17dfb77306582573338f874426708`.
Observed clean before each strict command and after all runtime sequences,
before writing this review. The L01 oracle manifest remains
`0628fb8a7196b44d0322ea438db7a180eb0f97b50f36cece0b2d0739dd0f4e04`.

## Preserved failure, approval and correction

Source adequacy review, relevant L02/L03 lineage and the isolated lifecycle
wording clarification are preserved in PREFLIGHT.md. Baseline on clean
`0617c7bf184f89353b78fe90210bc188099561af` passed35 retained cases and
failed the first required generic public control discovery with AttributeError
for absent `list_raw_observation_history`. All five controls had already
passed public admission, full typed known-ID readback and absent R187 checks.
Original full failure remains `/workspace/scratch/ad31885d756b/l04-baseline-red.log`;
BASELINE_REVIEW.md distinguishes the observed failure from its scoped diagnosis.

Only after that reached result did CONTRACT_REVIEW.md independently approve
the exact additive read model above against the original brief, current
commission/binding, IRB compatibility law, ingress and ownership law. The
approval does not rely on a proposal header self-authorising implementation.

Reviewed the complete final production diff:144 additive lines in api.py only.
It adds the frozen/slotted RawObservationHistoryPageV1, private callable/facet
wiring, public generic observation-history delegation and owner-local exact
filter/order/page implementation. All old method bodies, public create_owner
signature, v1 observation fields/validation, admission/codec logic, persistence
protocol/schema/adapters and old tests are unchanged. The new method performs
no broker/error/control parsing or book/completeness/validity calculation.
Exact string paths and subject/provider/variant/UTC cutoff select immutable
facts before stable receipt/scope/sequence/ID pagination. None variant selects
absence. Unsupported maximum cutoff is explicitly rejected before inclusive
cutoff+one-microsecond enumeration, preserving existing half-open storage law.

Worker/root static review noticed that naive int(cursor) could reject a valid
very long decimal cursor under CPython's digit limit. This was a source-relative
new-method contract issue, not a runtime failure or a recurrence of the closed
typed-fresh proof class. Before sealing the production candidate, the Worker
normalised leading zeroes, compared decimal magnitude with the selected count
and bounded int conversion to that count. The exact approved contract/proof
bytes stayed unchanged. Original and materially required final Ruff/mypy PASS
logs plus this static correction rationale remain in REPAIR.md and its logs.

## Strict runtime evidence

From the clean candidate, sole recovery command:

```
PYTHONPATH=src /workspace/scratch/ad31885d756b/m00-env/bin/python tools/run_product_proof_gate.py --aggregate m00_brief2
```

Full external output `/workspace/scratch/ad31885d756b/l04-green.log` records
**36 passed in87.01s**, exit0, exact candidate/generation above. The same
immutable admitted proof was used before and after the production correction;
no expected oracle, valid old test or evidence rule was weakened or resealed.

The control case proves N08/N09/N15: four depth facts plus five separate
control observations are publicly discoverable through page-size1/full cursor
exhaustion, with all full typed observations and all five literal independent
control outputs matching exactly. Error317/error316 native request/error fields
remain separate from collector reconnect/gap/restart metadata, with no fake
R187 operation or provider timestamp. Their order relative to depth, exact
prefix cutoffs, G1 invalidations/outgoing restart and G2 incoming restart link
are retained. Six identity counterfacts are excluded from the selected stream
but fully retained and compared through fresh typed public reads. Selected,
prefix and generation-link results repeat in fresh processes supplied only
database path/selectors; database bytes stay unchanged. Known-ID success is
checked separately and cannot pre-satisfy discovery input. New limit/cursor/
unsupported-cutoff refusals pass. The retained20 native/15 history cases also
pass, retaining all36 positive observations/155 base projections and their
literal oracle/history obligations separately from the five controls.

New public read-facet callback wiring materially touches original owner
construction/compatibility guarantees. The warranted original raw SQLite
aggregate was therefore run once on this repaired candidate:

```
PYTHONPATH=src /workspace/scratch/ad31885d756b/m00-env/bin/python tools/run_product_proof_gate.py --aggregate raw_signal_occurrence_truth_sqlite
```

Full external output `/workspace/scratch/ad31885d756b/l04-original-regression.log`
records **30 passed in31.93s**, exit0, unchanged original generation
`51e87129c2a31c71599b7a01beb8ba39717ed5118a4d5c849bcb2015b6c80c6f`.
No unrelated D-signal, broad suite or duplicate successful aggregate was run.
Both strict snapshot checks completed before review-document writes.

## Independent public sequence

Source `/workspace/scratch/ad31885d756b/l04-direct-sequence.py` imports actual
public M00 and its technical SQLite constructor, with no Worker fixture,
transport, expected loader or test helper. It constructs literal synthetic
reviewer-only subject/provider/request7/scope facts. It first admits one depth
callback and discovers only that fact. It then admits a separately identified
native error(reqId7,errorCode317) and discovers depth+error. Only afterwards
does it admit the collector-labelled G1→G2 restart and discover all three.
This decomposes command ordering instead of preloading a convenient composite.

Direct size1 public enumeration checks before-error, exact-error and
before-restart cutoffs, and discovers G2's incoming boundary via the declared
generation_after path with no known control IDs in query input. Error R187
projection is absent. Complete typed records compare with the independently
constructed literal admitted records. After releasing writer, a separately
launched process receives only database path, performs the same direct reads,
and returns identical full results; database bytes remain unchanged. Exactly
one noticed-edge query uses a valid5000-digit cursor and returns empty/no-next,
substantiating the static cursor correction without a speculative probe suite.

Full external `/workspace/scratch/ad31885d756b/l04-direct-sequence.log` records
DIRECT_SEQUENCE_PASS,3 observations, error317, incoming G1→G2 boundary,
no known control IDs in queries, long-cursor empty result and unchanged bytes.

## Disposition and limits

PASS for L04 on actual public SQLite paths. The public discovery gap is closed
by the approved additive read and the original native/payload/caller guarantees
remain supported by the relevant evidence. Relevant typed-fresh adequacy risk
is closed at class level; isolated wording/static-cursor issues and the original
reached baseline failure remain explicit, not hidden as an unconditional green.

SQLite ordinary transactions remain mode=ro/query_only; constructor validation
with create=False remains mode=rw, so no filesystem permission boundary is
claimed. PostgreSQL compatibility is static: the same existing read-only
received-between protocol is used without adapter change. No PostgreSQL runtime
or parity is certified; its previously recorded separate datetime-codec gap
remains unchanged. No live IBKR acquisition, feed entitlement, direct-option
availability, universal collector lifecycle policy, global causality, standing
book, completeness or re-warm-up is certified by these synthetic controls.

L05 deterministic actual-output publication/reproduction and L06 final brief
disposition remain separate. Root may preserve the external full logs/direct
source, commit acceptance, then verify/save/expose the cumulative L04 checkpoint
before beginning L05. D145 and unrelated work remain paused.
