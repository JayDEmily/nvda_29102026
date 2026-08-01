# Unit 4 Proof Promotion Evidence

- Date: 2026-08-02
- Parent commit: `cfecab3`
- Proof authority: `PASS families=196 tests=198 blocks=68`.
- Current promotion membership: `15` proof blocks, `15` current-blocking families, `17` test paths.
- Focused validation: `58 passed` across entry transport, M00 composition, proof authority and promotion-gate controls.
- Static M00 quarantine now permits exactly:
  - `src/nvda_desk/entry/cli.py`
  - `src/nvda_desk/entry/asgi.py`
- No other source file may import `nvda_desk.m00_application_shell` under the admitted proof.
- Entry family lifecycle moved from `next_gate_expected_red` to `current_blocking` only after all 15 transport cases passed.
