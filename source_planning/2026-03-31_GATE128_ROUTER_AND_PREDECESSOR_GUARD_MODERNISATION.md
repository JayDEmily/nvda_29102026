Status: complete on `main`; Gate 129 is now the active gate
# Gate 128 — Router and Predecessor-Guard Modernisation

## What closed

Gate 128 is complete on `main`. Router-only and predecessor-evidence guard tests now assert against the modern active-pack model instead of fossilised literal `PLANS.md` eras. Retained evidence for earlier packs still has to exist, but the tests no longer pretend the repo-root router must keep every historical status line forever.

## What changed

- updated financial-calendar, successor-pack, corrective-pack, testing-pack, and signal-coefficient closeout tests so they accept the current post-flight pack as the active router surface;
- moved older gate-completion checks toward the canonical gate map where the repo now freezes long-run status truth;
- preserved predecessor evidence requirements instead of weakening them into a free pass;
- advanced the post-flight repo consistency pack honestly to Gate 129.

## Receipt

- branch: `work/gate-128-router-and-predecessor-guard-modernisation-20260331`
- start commit: `2228c27`
- closing proof command: `PYTHONPATH=src pytest -q tests/test_gate128_post_flight_repo_consistency_planning.py tests/test_gate107_repo_process_governance.py tests/test_gate108_router_only_control_surface.py tests/test_gate109_template_pack_governance.py tests/test_gate110_agents_reading_order.py tests/test_gate112_governance_closeout.py tests/test_gate113_execution_authority_microtranche.py tests/test_gate114_research_mode_clarity_microtranche.py tests/test_gate115_historical_evaluation_readiness_planning.py tests/test_financial_calendar_planning_v3.py tests/test_gate125_review_visible_lineage.py tests/test_gate126_temporal_threshold_authority.py tests/test_gate46_50_planning_pack.py tests/test_gate51_cognitive_workflow_planning.py tests/test_gate59_doctrine_rebase.py tests/test_gate80_corrective_pass_reset.py tests/test_gate95_phase0_closeout.py tests/test_successor_pack_anti_drift.py`
- observed result: `43 passed`

## Why this is honest

This gate does not claim that older packs disappeared. It preserves them as evidence, but stops the guard tests from asserting that today's router must still spell out each older state in the same literal form. The router now tells the truth about the active pack; the gate map keeps the wider historical status lattice.
