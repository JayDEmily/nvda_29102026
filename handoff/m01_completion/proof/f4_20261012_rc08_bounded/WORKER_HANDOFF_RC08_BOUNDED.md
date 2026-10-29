# M01 F4 RC08 — independent fail-closed repair with outstanding clarification

**Status:** IN PROGRESS / AUTHORITY BLOCKED. **Not a consolidated Stage-1 candidate.**

**Base:** RC07 Git `fcad845bd4638428af46761cb2c7aebc5daceb0f`.
**Work branch:** `work/m01-f4-rc08-independent-refusal-20261012`.

## New changes

1. `fae7079` adds four authority-derived failing direct Stage-1-kernel tests, with initial 4 RED reproductions. They prove D178 can emit without D133 or D177, D189 can emit without D175, and D192 can emit without D175. Tests contain positive branch controls, so absent-input cases are not vacuous.
2. `1b64bd4` adds six lines of **absence-only** fail-closed guarding at these three row dispatch points; no arithmetic, catalogue, runtime schema or public-boundary change.
3. `CONSOLIDATED_OWNER_CLARIFICATION_PROPOSAL.md` isolates the four remaining required normative/typed-contract choices. It is **not normative authority** and must not be mistaken for programme approval of its illustrative flat `P_RULE` naming proposal.

## Checks against the modified RC08 tree

- Focused new missing-dependency tests: **4 passed**.
- Focused established cross-stage rule/remaining own-kernel tests together with new tests: **19 passed**.
- Derived-signal product suite, **excluding the inherited deliberately RED D186**: **671 passed**.
- Architecture/bootstrap: **74 passed**; this invocation put the ambient PyYAML 6.0.3 site-packages path on `PYTHONPATH` to satisfy an environmental dependency absent from the pinned offline wheel bundle. Do not conflate with the clean M00 durability environment.
- Scoped Ruff lint and formatting: **passed**.
- Scoped Mypy `_stage1.py`, with `--follow-imports=silent --ignore-missing-imports`: **passed**.
- RC08 M00 PostgreSQL public-seam/durability rerun: **not executed**. No PostgreSQL/persistence code was changed. RC07 evidence is historical and not a current RC08 rerun.
- Repository-wide Ruff format: **not run**. Previously known inherited formatting failures remain open; no claim made.
- Current RC08 complete product suite including D186: **not green** by definition; the previously committed D186 RED remains unmodified.

**Next lawful work:** obtain approval of the concrete decisions C1–C4; then commit discriminating tests before substantive production repairs, separately for each semantic unit; complete 30-row public-refusal proof, PostgreSQL and all required validations, and freeze one full-Git review candidate. Stage 1 remains unaccepted; Stage 2 unauthorised.
