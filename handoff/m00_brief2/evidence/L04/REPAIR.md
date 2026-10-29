# L04 bounded additive public discovery repair

Worker `/root/l04_worker`, 27 October 2026. Read the actual reached failure,
BASELINE_REVIEW.md and hash-specific CONTRACT_REVIEW.md before this correction.
Baseline candidate `0617c7bf184f89353b78fe90210bc188099561af` passed35 retained
cases and failed the first required public control discovery with missing
`list_raw_observation_history`. Known-ID control persistence/full typed reads
and absent R187 had already succeeded. This is a public enumeration gap, not
permission to reinterpret controls or rewrite admitted proof.

Exact approved contract SHA256 remains
`3ea7ec1be2fb7eb3422d0aed380a35fb68e17dfb77306582573338f874426708`.
Changed only `src/nvda_desk/raw_signal_occurrence_truth/api.py`, 139 additive
lines at this authoring handoff:

- frozen/slotted RawObservationHistoryPageV1 of existing immutable observations
  and next_cursor, exported in the existing public module;
- exact private callable protocol, read-facet slot/constructor callback/method
  delegation and owner construction wiring for the approved keyword signature;
- owner-local generic filtering of exact subject/provider/variant, inclusive
  supported UTC cutoff and validated exact tuple/string native identity paths,
  followed by stable receipt/scope/sequence/ID sorting and offset pagination;
- actual durable `transaction(write=False)` enumeration from UTC datetime.min
  through cutoff+one microsecond. Explicitly reject unsupported datetime.max
  cutoff before arithmetic; missing/wrongly typed paths exclude without coercion.

The method reads existing admitted facts. It parses no broker callback, error
code, control kind, generation lifecycle or collector schema; those predicates
are supplied as generic paths by the separately declared consumer. It does not
calculate standing book state, validity, completeness or continuity. Equal
receipt/scope/sequence observations remain distinct under the stable ID tie-break.
Variant None means exact absence. Empty cursors, non-ASCII/non-digit cursors,
invalid limits and malformed selectors are refused under the approved domain.

All previous v1 record fields/validation, source time/native codec, old public
method signatures and bodies, public create_owner signature, admission/write
logic, persistence protocol/schema/adapters and old tests remain unchanged.
No sealed proof/helper/contract/oracle/generation byte was edited.

Static PostgreSQL inspection: retained _postgres.py's
`list_observations_received_between` uses `received_ts_utc >= start AND
received_ts_utc < end` and reconstructs existing observation records. Its
transaction(write=False) sets `SET TRANSACTION READ ONLY`. The new generic
owner read uses that existing protocol exactly; no adapter or shared protocol
change is needed. PostgreSQL execution remains deferred. Previously recorded
legacy datetime native-codec limitation remains unchanged, not certified away.
SQLite ordinary transaction mode=ro/query_only and its constructor-validation
mode=rw distinction remain unchanged.

Scoped author static checks only: Ruff passed on changed api.py on its first
run (`repair-ruff-initial.log`); mypy passed on that file (`repair-mypy.log`).
No product test, runtime probe, PostgreSQL session or old aggregate was run by
this Worker. Runtime recovery on the same immutable admitted proof, original
raw SQLite compatibility aggregate and independent direct control-discovery
sequence remain the independent reviewer's responsibility on a clean candidate.
These source/static results do not claim L04 semantic acceptance.

## Static cursor-contract correction before candidate sealing

At the first authoring handoff, static review noted that the new method's
`int(cursor)` could apply CPython's integer-string digit limit to an otherwise
valid ASCII digit offset. The exact approved contract declares no cursor length
limit and requires beyond-population offsets to return empty. This was a
source-relative contract concern, not an executed product failure; no runtime
probe or new physical test case was run or added. Root explicitly directed the
bounded correction before candidate sealing.

Only the new method now validates ASCII digit structure, strips leading zeroes,
compares the remaining decimal string's length/lexical magnitude with the
selected population count, and clamps a larger offset to that count. It calls
int only on an offset no larger than the population, avoiding arbitrary huge
integer conversion including long leading-zero cursors. Empty/no-next beyond
the population follows the same approved result. The old projected-history
method, sealed proof/helper/contract/generation and all other code remain
unchanged. The final production diff is 144 additive lines, replacing the
initial 139-line source handoff above.

This material source correction invalidated the initial successful static
checks for the final bytes. Original PASS logs remain intact. Scoped Ruff and
api.py mypy both passed again on the corrected bytes, in
`repair-ruff-cursor.log` and `repair-mypy-cursor.log`. Independent review may
exercise this precise noticed edge within its already required bounded new-seam
sequence; the Worker performed no product probe or duplicate successful suite.
