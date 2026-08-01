# M12 C-PROOF Separate Worktree Review

- Baseline reviewed: `3394f41acef8230f7cbb756bee2de66b8e84afe0`
- Worktree: detached `/tmp/nvda_m12_proof_review`
- Initial boundary: 3 reference cases passed; 12 production cases failed only at absent package.
- Independent gaps found before Gate D:
  1. an authoritative result was not yet required to have its exact original output occurrence and fingerprint in the material set;
  2. non-UTC material time and out-of-range owner identity were not challenged;
  3. duplicate executable versions and duplicate/blank incompleteness facts were not challenged;
  4. comparison-only result evidence could blur replay classes;
  5. projection revalidation of forged assessment copies was not challenged.
- Disposition: all five gaps admitted into the hardened proof before implementation.
- Later proof hardening ruled out detached-hash authority by requiring embedded typed content that is dynamically revalidated against its repository-owned Pydantic contract and recomputed fingerprint.
- Later proof hardening also requires authoritative assessments and review projections to remain cross-field consistent after copied-model or fully recomputed forgery attempts.
- Final proof baseline: `d889cb7`; 3 reference cases pass and 19 production cases are exact red.
