# Revised exact-byte documentary checks

Candidate7e3ee583e652661363df6ef428665ff1f08dde5d/tree150590e8eb47f6061d53933ceeb982ae11f3606f. Git status empty.

- Three expected old replacement strings each occurred once; replacing only those strings in ec570da's brief produced the exact current bytes.
- BriefSHA c23ea315c94b478c568f105e94891a03af62393792a1478c33027a0371738bb8.
- ContractSHA54850f780c4442924e2d28ed319ae5f0fb109e291b367391ac0a4c86190294fc; bytes unchanged from ec570da.
- Eight incorporation rows, all raw hashes match. One exact contract marker with matching hash.
- Initial report/results hashes match67cee20b46b3fcc0f851fefb74effcd8f259bac818687b1e4d17eb285f09c00b / c99c09c42d6f725cdfab18244bac327be583f99b5338f5d29f810228778844f3.
- Runtime/config/control/schema/test/pin/build-path diff ec570da..7e3ee58 empty, exit0.
- Mapping declaration reread: selection_identity_field_paths is the existing empty-default tuple field.
- D013 partial provenance: original344bytes SHA3073bf56f920c44083e3b95db66e556747723211516ae755c603c5091e761f71; retained345bytes SHA7b9b244a2b9790d0b313ab210f6966c08ec55a94cba1d1341c549f54d68424e6; hex==original and retained==original+LF both true. No partial admitted as proof.

Read-only standard-library/Git/file checks only. No repository imports, tests, native/runtime validators, database, mypy/lint, provider operation, source/proof implementation or shared edit.
