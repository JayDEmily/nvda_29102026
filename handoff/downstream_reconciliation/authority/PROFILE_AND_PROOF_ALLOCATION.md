# L01 provisional profile / proof allocation — NOT AUTHORISED, NOT RUN

The original owning claims and immutable generations remain unchanged. This is an allocation proposal for L14 proof after owner/normative source-profile and claim admission, **not a new proof admission**. Under current R2 no product, runtime or static tests run before L14.

The current restored source has one parametrised `success`/`refusal` test entry per old owner at `tests/product/market_measurement_dNNN/test_signal.py`, including D135 whose existing pair exercises both top-two and top-one. Physical count is by collected cases, not by assertions or profiles. Each new native profile needs its own approved exact success/refusal pair unless existing cases can lawfully cover the required proof without concealment. Six is an absolute per-D ceiling, not an automatic allocation.

| Owning D | Legacy claim (retain exact old provenance) | Native candidate / independently stated success | Native refusal to author | Plan leaf | Gate status |
| --- | --- | --- | --- | --- | --- |
| D087 | `neutral_market_measurement_truth_d087` | A2 CALL asynchronous bid1.20 + ask1.40 → midpoint1.30; A3 PUT scope separately mandatory for source support | Missing/stale/mismatched callback or right | L03 | Pending A02/A04 |
| D131 | `neutral_market_measurement_truth_d131` | C1 compatible public D087 midpoint1.30, ±0.50 band 0.80–1.80, bid5 + ask3 = 8 contracts | Unwarmed post-reset / missing source role | L04 | Pending L03/A01/A04 |
| D134 | `neutral_market_measurement_truth_d134` | A4 side1 bid positions0/1 size5+3=8 shares | Missing operation with other fields retained | L05 | Pending A01/A04 |
| D135 | `neutral_market_measurement_truth_d135` | A4 side0 ask top-two2+4=6; top-one=2; both profile identities retained | Separate reset after warm-up | L06 | Pending A01/A04; case count review |
| D136 | `neutral_market_measurement_truth_d136` | actual compatible D134=8,D135=6: `(8-6)/(8+6)=1/7` | Same-context D135 top-one2 versus top-two request | L07 | Pending L05/L06/A04 |
| D138 | `neutral_market_measurement_truth_d138` | exact separate authorised 3-level fixture: bid slope7/2, ask slope5/2 with public D011 | Reset without proven complete warm-up | L08 | Pending A01/A04/fixture |
| D139 | `neutral_market_measurement_truth_d139` | 4-second R001 collector-receipt window, inserts3/5: count1/2 events/s, size2 shares/s | Operation missing | L09 | Pending A01/A04 |
| D140 | `neutral_market_measurement_truth_d140` | 2-second R001 receipt bucket, deletion size0 removes prior6: count1/2 events/s, size3 shares/s | Delete nonexistent standing position | L10 | Pending A01/A04 |
| D143 | `neutral_market_measurement_truth_d143` | C2 ALPHA6/BETA2, HHI5/8 **only if** complete four-row grouping is approved | MPID missing with size present and cross-MPID mutation witness | L11 | Pending A03/A04 |
| D137 | `neutral_market_measurement_truth_d137` | legacy atomic shares stock microprice201/2 retained; new asynchronous option exact oracle not yet approved | Missing/mismatched constituent, denominator-zero where relevant | L12 | Pending A02/A04 |

**Helper L02:** cross-owner public receipt/control contract case allocation must be accepted independently; it cannot silently consume an existing D profile's two-case allocation.

**Case accounting:** Old preserved D claims each currently have one `pytest.mark.parametrize` success/refusal pair. A newly approved success/refusal pair per D would give four physical cases for that D if retained independently, below the six hard ceiling; however this is a **planning arithmetic bound**, not proof-loader admission or a claim that every multiple-profile assertion fits within four cases. D135 and D087 rights/profiles need explicit counting before authoring and no hidden loops. No new tests, claim generations or synthetic fixture values are committed in this L01 draft.

**Decision blocker:** A01–A04 in `CONSUMER_SOURCE_CONTRACT_V1.md` need exact current owner/normative approval before implementation. L14 retains independent external source-oracle review and strict execution. No `TESTED_ACCEPTED` status is available now.
