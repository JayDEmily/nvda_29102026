# VI-02 — Repository-native ingress evidence

Observed command:

`PYTHONPATH=src python tools/validate_implementation_authority.py --binding implementation/authority/implementation_authority_binding.yaml --brief <exact external IRB>`

Observed output:

```text
PASS: implementation authority brief_sha256=938debe255d68668b0ae60f021d679fc8e3022be6eb050e7f3cd6112818fd342
candidate_targets: create:raw_signal_occurrence_truth->M00, modify:A00
```

Durable-state checks:

- modules SHA-256 before: `d86f0d22f9486e5d9bf95aaee90cf157c6761b4d5071adfdfda42ce1b39e0b21`
- modules SHA-256 after:  `d86f0d22f9486e5d9bf95aaee90cf157c6761b4d5071adfdfda42ce1b39e0b21`
- implementation allocations SHA-256 before: `79f68bb3e318d2ff7ce664d778e0fc1c505e8fe0bd50bbe20804a0bda7ba4676`
- implementation allocations SHA-256 after:  `79f68bb3e318d2ff7ce664d778e0fc1c505e8fe0bd50bbe20804a0bda7ba4676`

The equality of each before/after pair establishes that VI-02 candidate resolution did not mutate either durable architecture surface.
