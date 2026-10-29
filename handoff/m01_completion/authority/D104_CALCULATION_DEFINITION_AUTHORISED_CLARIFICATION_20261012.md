# D104 calculation-definition clarification — Programme Owner, 2026-10-12

**Version:** `D104-20261012-01` (normative calculation-definition revision label; no distribution-version change).
**Authority:** Explicit programme-owner instruction, 12-10-2026, “M01 F4 — D104 Skew-Rotation Correction and Final Stage-1 Semantic Preflight”.
**Status:** AUTHORISED mathematical and selection definition; implementation and F4 acceptance require independent evidence.

For one underlying, one applicable expiry and the exact same authorised `P_WINDOW` comparison horizon, D104 requires both D099 (25-delta put/call skew) and D100 (10-delta put/call skew):

```
D104 = (D100_current - D099_current) - (D100_prior - D099_prior)
     = (D100_current - D100_prior) - (D099_current - D099_prior)
```

Select the latest eligible `current` and corresponding `prior` at or before the exact comparison anchor **within each family separately**. Both families must have compatible current and prior surface states, exact underlying and expiry identity, knowledge-cutoff and version-selection context. Insufficient, missing, ambiguous, cross-family, stale, wrong-expiry/subject or incompatible history refuses. Both families' actual current/prior predecessor identities and ultimate source observations must be in the derived lineage, without unrelated historical records. Preserve K03_CHANGE_RETURN, `P_WINDOW`, `D099;D100`, result units `vol points`, and D099/D100 arithmetic. No extra factor 100 and no invented spot adjustment. D104 changes are not accepted Stage 1 merely because this clarification exists.

The source-semantic preflight authorised in the same instruction is read-only with respect to accepted normative authority and production; it is not permission to change other D rows.
