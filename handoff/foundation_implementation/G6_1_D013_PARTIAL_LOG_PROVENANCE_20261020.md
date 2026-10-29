# D013 excluded partial stdout — exact preservation correction

Verified20October2026,00:42Melbourne: the original incomplete D012 stdout at /workspace/scratch/d549b6d808a9/d013-final-candidate-X08ONL/strict_d012.log is344bytes, SHA2563073bf56f920c44083e3b95db66e556747723211516ae755c603c5091e761f71. The retained text copy d013_candidate_evidence_20261020/strict_d012.log is345bytes, SHA2567b9b244a2b9790d0b313ab210f6966c08ec55a94cba1d1341c549f54d68424e6. Direct byte comparison establishes retained_text == original_bytes + one trailing LF. The text-file patch preservation added that LF; no original progress character changed.

Correction: G6_1_D013_CANDIDATE_20261020.md's wording "exact incomplete output" must not be interpreted as byte-identical preservation of this one partial stdout. It is a newline-terminated text rendering of344 original bytes. Preserve the original report and its reviewed historical digest; this addendum corrects the narrower preservation claim rather than silently changing reviewed evidence. Other independently byte-compared review files are unaffected.

The original run remains incomplete, cause UNKNOWN, excluded as product evidence. Neither344 nor345bytes contains an aggregate outcome. The complete author80 retry and independent80 rerun remain separate complete evidence; this correction does not change runtime/proof/generation bytes or D013's bounded acceptance. No fullG6.1/native claim follows.

Exact original344bytes are recoverable by concatenating/hex-decoding the following single hexadecimal value; decoded size/SHA256 are given above. Do not append a newline to the decoded bytes.

```text
3d3d3d3d3d3d3d3d3d3d3d3d3d3d3d3d3d3d3d3d3d3d3d3d3d3d3d3d3d20746573742073657373696f6e20737461727473203d3d3d3d3d3d3d3d3d3d3d3d3d3d3d3d3d3d3d3d3d3d3d3d3d3d3d3d3d3d0a706c6174666f726d206c696e7578202d2d20507974686f6e20332e31322e31342c207079746573742d392e302e332c20706c756767792d312e372e300a726f6f746469723a202f776f726b73706163652f736372617463682f6435343962366438303861392f6735322d7265636f766572792f7265706f7369746f72790a636f6e66696766696c653a20707970726f6a6563742e746f6d6c0a636f6c6c6563746564203830206974656d730a0a74657374732f70726f647563742f6d61726b65745f6d6561737572656d656e745f643031322f746573745f7370726561642e7079202e2e2e2e2e2e2e2e2e2e2e2e2e2e2e2e2e2e2e205b203233255d0a2e2e2e2e2e2e2e2e2e2e
```

TS: 20-10-26 00:42
