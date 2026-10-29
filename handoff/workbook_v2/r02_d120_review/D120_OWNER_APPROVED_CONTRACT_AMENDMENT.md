# D120 owner-approved native-field contract amendment

Authority: current owner instruction 15 October 2026, approximately 05:10 Australia/Melbourne, expressly authorises the previously explained repair. Parent HEAD 204f5ec1cb02526a4d2895d3923652114f895f38. This is a narrow calculation-definition/source-contract amendment, not new financial mathematics.

Definition revision: D120-NATIVE-MULTIPLIER-20261015-01.
Direct raw dependencies: R120;R121;R126;R127;R015;R016. Predecessor remains D015.
R015 is native option right C/P. R016 is the numeric contract multiplier. No constant/default multiplier is authorised. Preserve signed_contracts = sum(sign*size) and signed_premium_notional = sum(sign*size*trade_price*multiplier).

Selection applies accepted brief §8.1, §9 and §11: pair trade price/size by the same M00 trade occurrence; select the latest eligible R015 and R016 for that exact subject, underlying, expiry, strike, option right and contract, known no later than the trade receipt and with effective basis no later than that trade's applicable time. Contract metadata can be receipt_only; never fabricate an event instant. Each metadata field preserves its own occurrence namespace and mapping/unit version. Equal latest event/receipt priority with distinct occurrences is ambiguous and refuses. Metadata must satisfy explicit policy freshness/skew; missing, future, incompatible or non-positive/non-finite numeric multiplier refuses. Native C/P must agree with selected contract identity. Persist only metadata observations actually consumed; selected trade sign and all other existing dependencies remain required.

The accepted original brief remains byte-identical. This owner-approved amendment overrides its inherited CSV dependency binding only for D120. The authority index identifies the exact amended effective catalogue digest. All unrelated catalogue rows and accepted exceptions remain unchanged. Distribution version 1.0.0, M00 source files, V2 ownership allocations and original G01 disposition remain unchanged.

Independent review is now requested, replacing the previous bounded waiver. No GitHub interaction or invented main branch is authorised by this instruction.
