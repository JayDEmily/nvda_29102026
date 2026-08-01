# M09 C-PROOF Separate-Worktree Adversarial Review

## Review boundary

- initial proof commit: `730c66cb000e093e9b010cf2380eb34eed232168`;
- hardened proof commit: `8542846bbb3be926fc4b70ec386fbaf5390266a4`;
- execution: detached Git worktree, no production package present;
- purpose: challenge the admitted reference law with cases not authored in the original proof.

## Initial result

`FAIL_REPAIRABLE:PROOF_INCOMPLETE`

Four of four additional cases exposed missing proof law:

1. zero available capital incorrectly retained a positive percentage and `continue`;
2. negative reserved capital did not fail closed;
3. percentage inputs above 100 could authorise more than total available capital; and
4. a caution multiplier above 1 could increase rather than reduce authority.

The defects were in the proof boundary, not production code, because Gate D had not opened.

## Disposition

All four cases were admitted. Section 7.13.3 was clarified before proof mutation to require closed percentage and multiplier domains, non-negative capital facts, and zero-capital `no_trade` semantics. The reference law and production-facing assertions were then hardened.

## Hardened result

`PASS:SEPARATE_WORKTREE_REVIEW:GATE_D_MAY_OPEN`

The same detached four-case script passed at `8542846bbb3be926fc4b70ec386fbaf5390266a4` with zero failures. The admitted proof now contains 16 green reference/mutant cases and seven exact-red production assertions. No production source existed or changed during either review.
