# M04 K07 MLC-T validation receipt

Source checkpoint: `cc69d479e3a8d2da4b974a79cea665f8f3739ca7`.

Runtime used for executable proof: repository-pinned `pytest==9.0.3`; repository-pinned `ruff==0.15.11`.

| Command scope | Exit | Result |
|---|---:|---|
| candidate collection | 0 | 252 collected |
| candidate excluding production subject | 0 | 239 passed, 13 deselected |
| complete candidate | 1 | 241 passed, 11 expected-red failures |
| retained partial K07 function | 1 | one expected-red failure; missing combined context/lineage still does not reject |
| candidate proof-block check | 0 | PASS |
| all proof-block checks | 0 | PASS, 53 blocks |
| proof-executor contract shadow | 0 | 21 passed |
| changed Python lint | 0 | PASS |

The 11 complete-family failures are ten role-profile assertions receiving only `schema_validation` and one missing-`scenarioid` case that does not raise. They are behavioural K07 gaps, not import, constructor, fixture or collection failures.

The candidate is not admitted by this receipt. Independent `M04-PROOF-MLC-V-V1` remains mandatory.
