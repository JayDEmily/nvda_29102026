# M12 K19 Gate D validation summary

Proposition: `M12-K19-AUTHORITATIVE-REPLAY-V1`.

Implemented boundary: immutable embedded repository-owned typed replay material, exact ordered replay envelopes, fail-closed preserved-occurrence/governed-reexecution/comparison classification, and detached read-only review projections. Live reads, runtime repair, external side effects, capital/order/portfolio mutation, proof promotion, durable retention and production replay remain closed.

## Focused and control acceptance

- M12 focused proof: `22/22 passed`.
- Affected replay/review compatibility set: `64/64 passed` (the prior 63-case set plus the final authoritative-result hardening case).
- Vocabulary builder parity: `4/4 passed`.
- M12 vocabulary audit: `0 unresolved candidates`; `18` scanned files; `73` governed occurrences; touch stamp current.
- Proof-block manifests: `64/64 passed`.
- Proof-executor contract: `21/21 passed`.
- Tier B: `49/49 passed`.

## Complete Tier A comparison

- Hardened proof baseline `d889cb7`: `1,609 passed / 272 failed`.
- Gate D current: `1,628 passed / 253 failed`.
- Resolved failure nodes: `19`, exactly the admitted M12 production-facing cases.
- New failure nodes: `0`.

The non-vocabulary tree was rerun directly at baseline/current. The baseline vocabulary partition is unchanged from accepted M11 evidence (`100 passed / 3 failed`); the current partition was executed file-by-file and remains `100/3` with the same three pre-existing failures. The aggregate vocabulary command retains a known suite-order non-termination and is not represented as a clean single-run pass. No live, durable or production-readiness claim follows.
