# Evidence

## Authority / routing

- Governing parent: `2439688f254d0bb7fc856e5e770fa1e5ae293b4a`.
- Reviewer 029 rejected candidate: `d25aedeed5de65d0a241bdce6eae22671ef2ddf8`.
- Current public field at that candidate: `RawObservationOccurrenceV1.native_record: Mapping[str, object]`.
- Relevant semantic authority: IRB BC-005, BC-009, BC-010 and IWO-U03.

## Independent blocker reproduction

Executed against the governed current source through the public U03 owner seam:

```text
AlwaysEqual 1 2 => ACCEPTED
NeverEqual 1 1 => ValueError: observation occurrence identity is already admitted with different content
```

`AlwaysEqual` is one deepcopy-able value type whose `__eq__` returns true for any same-type instance; changed native state therefore collapses. `NeverEqual` is one deepcopy-able value type whose `__eq__` always returns false; reconstructed equivalent state therefore cannot be idempotent. Both are mechanically admitted under the current `Mapping[str, object]` public surface.

## External Worker response

Programme Owner supplied a response reporting blocker commit `85738686e5ee41d2e6f638c1ca890d15e555a0f0` / tree `c97991ba61f1cfdd43d89805994c6a9602bd30e3`, parent `2439688f254d0bb7fc856e5e770fa1e5ae293b4a`. The corresponding repository/archive was not supplied here, so those Git objects are recorded as externally reported rather than independently verified.
