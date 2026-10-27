# L03 reconstruction after workspace reset

Worker `/root/l03_rebuild`, 27 October 2026. This source reconstruction starts
from recovered accepted L02 commit `5219004223e33291f1b831382e8427742e00427f`.
Prior uncommitted L03 source and reviewer preflight bytes were not present in
the restored checkpoint. The continuity summary describes their intended scope
and a typed fresh-read adequacy finding; it is not substituted for a recovered
review receipt or runtime evidence. No prior L03 product pass is claimed.

Read full current GUARDRAILS, AGENTS, tests override, root plan and original
Brief2. Inspected full L02 native test/transport and primary L02 preflight/final
review; exact N04/N05/N10/N13/N16 perturbation specifications; current public
projection/history implementation, SQLite transaction read mode and L01 input/
expected record structures. Other M00 source inspection here is scoped, not a
new claim of full-owner review.

Changed only the test transport and new history proof, plus this evidence:

- `history_rows` calls actual public `list_projected_raw_history`, one row per
  page, exhausts cursors with a repeated-cursor guard, serialises every public
  projection field and applies exact type/value identity filtering. Request,
  generation, requested exchange and scenario selection are consumer checks on
  returned identity; they are not falsely presented as built-in M00 keywords.
  Exact mapping provider/variant and public subject/receipt/event selectors
  retain their existing roles. No expected loader is called by actual history.
- Ten scenario cases compare each role/group's entire typed history against
  the independent L01 oracle, including B's two separate subjects. They drop
  the writer owner, launch fresh processes from database/query selectors only,
  compare again, and check unchanged database bytes.
- N04 tests both B streams, positive receipt selection and empty event-cutoff
  selection, again from fresh owners. N05 retains two equal receipt/scope/
  sequence facts and compares complete projections to the L01 original plus
  sole occurrence-ID change; full fresh observations compare to exact typed
  admitted originals. Stable ID order is display order, with provider causal
  order explicitly unknown; later export must carry that ambiguity metadata.
- N10 mixes A4/A5/A6/C2/C3 and adds six independent counterfacts for the exact
  declared selector dimensions. `OTHER-SOURCE`, `OTHER-VARIANT` and
  `OTHER-EXCHANGE` are test choices for dimensions already required in the
  immutable N10 specification; no approved fixture bytes change. Every selected
  stream compares to exact L01 output, and all counterfacts' complete tagged
  observations are checked through fresh ordinary known-ID public reads.
- N13 compares pre-cutoff histories and the complete post-cutoff known-ID
  observation, including independent fresh full observation readback. N16
  verifies exact identical retry, rejected changed native payload and full
  original typed fresh observation/history preservation.

The common adequacy risk reported in the continuity summary is directly
addressed at class level: absence/exclusion assertions are paired with exact
typed fresh retained-fact comparisons, never only truthiness, ID existence or
numeric equality. The primary L02 review's same numeric-equality weakness is
available to the independent L03 reviewer for recurrence assessment; this
Worker does not manufacture the lost L03 review's exact wording/disposition.

Scoped static checks only: Ruff helper/new test passed (`ruff-initial.log`);
after materially adding explicit writer-owner release before each child
read, Ruff passed (`ruff.log`). Helper mypy passed (`mypy.log`). No product
tests, strict aggregate, production edits, admission/generation changes or
L03 semantic acceptance were performed by this Worker. Independent preflight
and admitted strict execution remain required.
