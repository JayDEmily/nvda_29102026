"""Conservative F4 progress reconciliation against accepted catalogue and F3 ledger.

The original F3 ledger remains immutable historical evidence. Its row-edge IDs are
mechanically rebased by (D row, kind, source ID) onto the authorised F1
D134/D135 R187 correction; no historical acceptance is silently invented.
The new D134/D135/D136 proofs apply only to their bounded public mechanism.
"""

from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
AUTHORITY = ROOT / "handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv"
F3 = ROOT / "handoff/m01_completion/proof/f3_20261009/F3_ALL_EDGES_RECONCILIATION.csv"
OUT = Path(__file__).resolve().parent
NORMATIVE_SHA256 = "d651436df1fcd1395f8f1147dfd80db1ed178da4834447a947c3c9c32fd82aa7"
STAGE1_KERNELS = {f"K{i:02d}" for i in range(1, 9)} | {"K16", "K17"}
F4_BOUNDED_PUBLIC_ROWS = {
    "D105": (
        "RC14", "tests/product/derived_signal/test_m01_f4_rc14_iv_baseline_public.py",
        "Exact NVDA ATM30D IV R183 within a year-long historical selection, "
        "prior .20/.40 and current .30 => rank 50; tie .40 => 100, "
        "full R-lineage, missing/wrong-point/future refusal and retry",
    ),
    "D106": (
        "RC14", "tests/product/derived_signal/test_m01_f4_rc14_iv_baseline_public.py",
        "Exact NVDA ATM30D IV R183 historical percentile prior .20/.40 "
        "current .30 => 50; .40 tie midrank => 75, historical-only "
        "full R-lineage, missing/wrong-point/future refusal and retry",
    ),
    "D118": (
        "RC14", "tests/product/derived_signal/test_m01_f4_rc14_option_chain_ratio_public.py",
        "Controlled M00 source-native aggregate R049 call 300 / R050 put 150 => 2 "
        "at exact expiry/strike region; unrelated region excluded, full R lineage, "
        "missing/zero/future/mismatched put refusal and retry",
    ),
    "D119": (
        "RC14", "tests/product/derived_signal/test_m01_f4_rc14_option_chain_ratio_public.py",
        "Controlled M00 source-native aggregate R047 call 400 / R048 put 200 => 2 "
        "at exact expiry/strike region; unrelated region excluded, full R lineage, "
        "missing/zero/future/mismatched put refusal and retry",
    ),
    "D180": (
        "RC16", "tests/product/derived_signal/test_m01_f4_rc16_position_public.py",
        "M00 native matched status R219=6/R220=4 => 0.6 completion, "
        "exact raw lineage/retry and zero-denominator refusal",
    ),
    "D181": (
        "RC16", "tests/product/derived_signal/test_m01_f4_rc16_position_public.py",
        "Two native position legs, quantity*multiplier*delta => 80; full "
        "leg lineage, known incomplete leg refusal, future invisible leg cutoff and retry",
    ),
    "D182": (
        "RC16", "tests/product/derived_signal/test_m01_f4_rc16_position_public.py",
        "Two native position legs, quantity*multiplier*gamma => 7; full "
        "leg lineage, known incomplete leg refusal, future invisible leg cutoff and retry",
    ),
    "D183": (
        "RC16", "tests/product/derived_signal/test_m01_f4_rc16_position_public.py",
        "Two native position legs, quantity*multiplier*vega => 190; full "
        "leg lineage, known incomplete leg refusal, future invisible leg cutoff and retry",
    ),
    "D184": (
        "RC16", "tests/product/derived_signal/test_m01_f4_rc16_position_public.py",
        "Two native position legs, quantity*multiplier*theta => -30; full "
        "leg lineage, known incomplete leg refusal, future invisible leg cutoff and retry",
    ),
    "D185": (
        "RC16", "tests/product/derived_signal/test_m01_f4_rc16_position_public.py",
        "Native realised 125/unrealised -45/total 80 retained as named "
        "components, exact three-field raw lineage and retry",
    ),
    "D099": (
        "RC14", "tests/product/derived_signal/test_m01_f4_rc14_skew_from_native_delta_public.py",
        "Exact-expiry native R111 IV and independently projected R112 25-delta "
        "and R015 strike joined by option contract: call .30/put .40 -> 10 "
        "vol points, field-level raw lineage and retry, absent delta/strike, "
        "future delta and contradictory 25-delta refusal",
    ),
    "D100": (
        "RC14", "tests/product/derived_signal/test_m01_f4_rc14_skew_from_native_delta_public.py",
        "Exact-expiry contract-matched native R111/R112/R015 ten-delta "
        "IV: call .20/put .50 -> 30 vol points, raw lineage and retry, "
        "selected missing-field refusal",
    ),
    "D101": (
        "RC14", "tests/product/derived_signal/test_m01_f4_rc14_skew_from_native_delta_public.py",
        "Native per-contract R111 and R112 at 25-delta and two 50-delta "
        "ATM points yield 100*(.40+.30-2*.33)=4 smile curvature, "
        "raw lineage and retry, selected missing R112 refusal",
    ),
    "D117": (
        "RC14", "tests/product/derived_signal/test_m01_f4_rc14_option_volume_z_public.py",
        "M00 exact NVDA call contract option volume R041 history 8/12 and current "
        "16 gives 6/sqrt(8) with versioned two-sample historical baseline, "
        "required R075, competing-contract exclusion, exact persisted R lineage, "
        "missing history/OI, zero-variance, future-cutoff refusal, retry",
    ),
    "D116": (
        "RC14", "tests/product/derived_signal/test_m01_f4_d116_authorised_public.py",
        "Programme Owner 2026-10-11 corrected R041/R047/R048: conditional exact "
        "call R047 or put R048, 300 volume / 1000 OI = 0.3, competing "
        "contract/opposite right/R075 excluded, zero-volume allowed, zero or "
        "negative OI refused, wrong contract/absence/future/version refusal, "
        "exact two-input lineage and deterministic public retry",
    ),
    "D092": (
        "RC14", "tests/product/derived_signal/test_m01_f4_rc14_option_iv_public.py",
        "M00 exact option contract R084/R093 bid .48 and ask .52 -> .50 "
        "IV midpoint, C2 distractor excluded, exact source lineage, "
        "missing/future refusal and deterministic retry",
    ),
    "D093": (
        "RC14", "tests/product/derived_signal/test_m01_f4_rc14_option_iv_public.py",
        "M00 exact option contract R084/R093 .48/.52 -> four volatility "
        "points of ask-minus-bid IV, C2 distractor excluded, exact "
        "lineage, missing/future refusal and retry",
    ),
    "D094": (
        "RC14", "tests/product/derived_signal/test_m01_f4_rc14_option_iv_history_public.py",
        "M00 exact contract R111 as-of five-minute IV .53-.50 -> three "
        "vol points; newer nearer-than-anchor IV .90 excluded, as-of "
        "same-contract historical lineage, no eligible historical value "
        "or different-contract reference refusal, retry",
    ),
    "D095": (
        "RC14", "tests/product/derived_signal/test_m01_f4_rc14_option_iv_history_public.py",
        "M00 exact contract R111/R183 prior comparable day .53-.48 -> "
        "five volatility points, 5m/near distractors excluded, required "
        "R183 present and in raw lineage, absence and wrong-contract "
        "history refusal, retry",
    ),
    "D040": (
        "RC06", "tests/product/derived_signal/test_m01_f4_rc06_trend_score_public.py",
        "M00 D020/D021/D027/D024 full four-predecessor momentum/acceleration "
        "weighted schema, exact numeric source inputs 1m/5m/30m, raw/D "
        "lineage, no 30m anchor or wrong-subject VWAP refusal, retry",
    ),
    "D061": (
        "RC06", "tests/product/derived_signal/test_m01_f4_rc06_market_regime_scores_public.py",
        "M00 D052/D053/D057/D058/D059/D060 full six-predecessor scored "
        "volatility regime with versioned P_SCORE feature extractors, "
        "300s history anchors, exact numerical arithmetic, source/predecessor "
        "lineage, missing/future/wrong-subject refusal and retry",
    ),
    "D070": (
        "RC06", "tests/product/derived_signal/test_m01_f4_rc06_market_regime_scores_public.py",
        "M00 D066/D067/D068/D069/D049/D050/D051 full seven-predecessor "
        "international risk schema, versioned daily and 300s anchors, "
        "exact numerical score, native source/D lineage, "
        "missing/future/wrong-subject refusal and retry",
    ),
    "D083": (
        "RC13", "tests/product/derived_signal/test_m01_f4_rc13_cross_section_public.py",
        "M00 immutable exact NVDA/AMD/INTC contemporaneous basket of three "
        "current/prior subject-scoped pairs; independently calculated N-1 "
        "sample SD of cross-member log returns; missing member and "
        "parameter/selection basket mismatch refusal, full R-lineage and retry",
    ),
    "D071": (
        "RC13", "tests/product/derived_signal/test_m01_f4_rc13_sector_returns_public.py",
        "M00 SPY instrument-specific current 120/prior close 100 => ln(1.2); "
        "AMD decoy excluded, wrong-subject/future-cutoff refusal, full lineage and retry",
    ),
    "D072": (
        "RC13", "tests/product/derived_signal/test_m01_f4_rc13_sector_returns_public.py",
        "M00 QQQ instrument-specific current/prior return ln(1.2); "
        "AMD decoy excluded, wrong-subject/future-cutoff refusal, full lineage and retry",
    ),
    "D073": (
        "RC13", "tests/product/derived_signal/test_m01_f4_rc13_sector_returns_public.py",
        "M00 SMH instrument-specific current/prior return ln(1.2); "
        "AMD decoy excluded, wrong-subject/future-cutoff refusal, full lineage and retry",
    ),
    "D074": (
        "RC13", "tests/product/derived_signal/test_m01_f4_rc13_sector_returns_public.py",
        "M00 SOXX instrument-specific current/prior return ln(1.2); "
        "AMD decoy excluded, wrong-subject/future-cutoff refusal, full lineage and retry",
    ),
    "D075": (
        "RC13", "tests/product/derived_signal/test_m01_f4_rc13_sector_returns_public.py",
        "M00 NVDA instrument-specific current/prior return ln(1.2); "
        "AMD decoy excluded, wrong-subject/future-cutoff refusal, full lineage and retry",
    ),
    "D032": (
        "RC04", "tests/product/derived_signal/test_m01_f4_rc04_realised_risk_public.py",
        "M00 exact 5-minute three-price return grid; two 2.5-minute intervals, "
        "annualised sum log-return squares per declared trading-year fraction; "
        "missing required sample refusal, full raw lineage, deterministic retry",
    ),
    "D033": (
        "RC04", "tests/product/derived_signal/test_m01_f4_rc04_realised_risk_public.py",
        "M00 exact 30-minute three-price return grid; two 15-minute intervals, "
        "annualised realised volatility, missing sample refusal and full lineage",
    ),
    "D034": (
        "RC04", "tests/product/derived_signal/test_m01_f4_rc04_realised_risk_public.py",
        "M00 exact 2-hour intraday three-price grid; two declared trading-time "
        "one-hour intervals, annualised realised volatility and cutoff refusal",
    ),
    "D035": (
        "RC04", "tests/product/derived_signal/test_m01_f4_rc04_realised_risk_public.py",
        "six successive valid weekday close instants spanning five complete "
        "trading-day intervals, declared policy and time-fraction, exact RV "
        "result, missing/future/subject refusal and full M00 lineage",
    ),
    "D036": (
        "RC04", "tests/product/derived_signal/test_m01_f4_rc04_realised_risk_public.py",
        "eleven successive valid weekday close instants spanning ten complete "
        "trading-day intervals; exact annualised RV, missing sample refusal",
    ),
    "D037": (
        "RC04", "tests/product/derived_signal/test_m01_f4_rc04_realised_risk_public.py",
        "twenty-one successive valid weekday close instants spanning twenty "
        "trading-day intervals; exact full-window volatility and absence refusal",
    ),
    "D038": (
        "RC04", "tests/product/derived_signal/test_m01_f4_rc04_realised_risk_public.py",
        "M00 same-occurrence native R151/R149/R150 with required instant grid; "
        "explicit RV minus pi-over-two bipower result, full R-lineage, "
        "wrong-subject/missing-window refusal and deterministic retry",
    ),
    "D039": (
        "RC04", "tests/product/derived_signal/test_m01_f4_rc04_realised_risk_public.py",
        "M00 two true-range five-minute bars, previous-close formula and exact "
        "16.5/18.5 averages; original red witness proves incomplete latest bar "
        "cannot silently substitute older complete bar; second red witness "
        "proves missing five-minute interval refuses; exact high/low/close "
        "lineage, wrong-subject and missing-window refusal, retry",
    ),
    "D028": (
        "RC04",
        "tests/product/derived_signal/test_m01_f4_rc04_elapsed_fraction_public.py",
        "M00 co-occurring R041/R044 source-native session fractions; refuse the "
        "two historical volumes at 0.25/0.75 when current fraction is 0.5; "
        "skip nearer interleaved unmatched 999 volume, calculate matched "
        "8/12 baseline and current 16 => ratio 1.6, exact lineage/retry; "
        "reject invalid fractions and incomplete history",
    ),
    "D029": (
        "RC04", "tests/product/derived_signal/test_m01_f4_rc04_time_of_day_bucket_public.py",
        "M00 source-native R144 bar-volume bucket selected by immutable P_BASELINE "
        "matching_rule; 8/12 prior versus 16 current gives exact sample-SD z, "
        "competing 200 off-bucket excluded, no matching history/missing rule refused, "
        "raw lineage and retry",
    ),
    "D030": (
        "RC04", "tests/product/derived_signal/test_m01_f4_rc04_time_of_day_bucket_public.py",
        "M00 source-native R062 trade-rate bucket selected by immutable P_BASELINE "
        "matching_rule; 8/12 prior versus 16 current gives exact sample-SD z, "
        "competing 200 off-bucket excluded, no matching history/missing rule refused, "
        "raw lineage and retry",
    ),
    "D031": (
        "RC04", "tests/product/derived_signal/test_m01_f4_rc04_time_of_day_bucket_public.py",
        "M00 source-native R063 volume-rate bucket selected by immutable P_BASELINE "
        "matching_rule; 8/12 prior versus 16 current gives exact sample-SD z, "
        "competing 200 off-bucket excluded, no matching history/missing rule refused, "
        "raw lineage and retry",
    ),
    "D009": (
        "RC20",
        "tests/product/derived_signal/test_m01_f4_macro_vintage_public.py",
        "M00 complete per-occurrence revision/vintage fields R280/R281/R282; "
        "latest as-of macro revision selected, full raw lineage, deterministic retry; "
        "partial newer native revision refuses rather than substituting earlier vintage",
    ),
    "D062": (
        "RC01",
        "tests/product/derived_signal/test_m01_f4_next_event_public.py",
        "M00 earliest eligible future event countdown 120 seconds/2 minutes; "
        "D001 public UTC predecessor and exact R002/R003/R284 raw lineage; "
        "past-only, missing and future-received event refusal",
    ),
    "D001": (
        "RC01",
        "tests/product/derived_signal/test_m01_f4_temporal_public.py",
        "M00 true-instant source offset converted to exact UTC; date/receipt-only "
        "refusal, raw lineage and deterministic retry",
    ),
    "D002": (
        "RC01",
        "tests/product/derived_signal/test_m01_f4_temporal_public.py",
        "M00 true-instant source-event age 10 seconds with D001 provenance; "
        "collector receipt-only age 15 seconds without invented D001; "
        "date-only, missing-input and future/invalid source refusal",
    ),
    "D003": (
        "RC01",
        "tests/product/derived_signal/test_m01_f4_temporal_public.py",
        "M00 timezone conversion of public D001 event without instant change; "
        "raw and derived provenance, future timezone and missing refusal",
    ),
    "D004": (
        "RC01",
        "tests/product/derived_signal/test_m01_f4_temporal_public.py",
        "configured 06:00 overnight boundary yields 2026-10-09 for 00:59:50 "
        "Australia/Melbourne; actual public D003 predecessor and M00 lineage",
    ),
    "D005": (
        "RC01",
        "tests/product/derived_signal/test_m01_f4_temporal_public.py",
        "versioned non-overlapping phase schedule yields overnight; actual public "
        "D003 predecessor, M00 lineage and missing schedule input refusal",
    ),
    "D010": (
        "RC01",
        "tests/product/derived_signal/test_m01_f4_temporal_public.py",
        "public D003 exchange-local timestamp and versioned market calendar/RTH "
        "policy; open overnight Saturday true, dated closure false, "
        "raw and derived lineage, missing-source refusal",
    ),
    "D085": (
        "RC01",
        "tests/product/derived_signal/test_m01_f4_temporal_public.py",
        "exact option-contract public D004 overnight trading-date predecessor; "
        "expiry 2026-10-16 minus local 2026-10-09 yields seven whole days; "
        "missing and expired-date refusal; raw/derived lineage",
    ),
    "D086": (
        "RC01",
        "tests/product/derived_signal/test_m01_f4_temporal_public.py",
        "exact option-contract public D001 UTC event predecessor; native expiry "
        "at configured 16:00 Melbourne converted UTC and ACT/365F; "
        "missing and expired-date refusal; raw/derived lineage",
    ),
    "D087": (
        "RC14",
        "tests/product/derived_signal/test_m01_f4_option_scalar_public.py",
        "exact option-contract M00 bid/ask midpoint 100; same-contract selection "
        "against decoy, raw lineage, absent/future refusal, retry",
    ),
    "D088": (
        "RC14",
        "tests/product/derived_signal/test_m01_f4_option_scalar_public.py",
        "exact contract option percentage spread 2 using recursively calculated "
        "D087 midpoint 100, R034/R035 and D occurrence lineage, missing/future refusal",
    ),
    "D089": (
        "RC14",
        "tests/product/derived_signal/test_m01_f4_option_scalar_public.py",
        "exact contract strike 150 / spot 120 = 1.25, native M00 raw lineage, "
        "other-contract/future/missing/zero-spot refusal and deterministic retry",
    ),
    "D090": (
        "RC14",
        "tests/product/derived_signal/test_m01_f4_option_scalar_public.py",
        "exact contract log(150/120) = ln(1.25), native M00 raw lineage, "
        "other-contract/future/missing/zero-spot refusal and deterministic retry",
    ),
    "D011": (
        "RC02",
        "tests/product/derived_signal/test_m01_f4_nbbo_algebra_public.py",
        "admitted M00 bid/ask source identities; midpoint 101, exact raw lineage, "
        "missing/future/different-subject refusal and idempotent retry",
    ),
    "D012": (
        "RC02",
        "tests/product/derived_signal/test_m01_f4_nbbo_algebra_public.py",
        "admitted M00 bid/ask source identities; absolute spread 2, exact raw lineage, "
        "missing-source refusal and idempotent retry",
    ),
    "D013": (
        "RC02",
        "tests/product/derived_signal/test_m01_f4_nbbo_algebra_public.py",
        "public recursive D011/D012 predecessor graph; percentage 200/101, "
        "exact D and inherited raw lineage; missing/future/wrong-subject refusal",
    ),
    "D014": (
        "RC02",
        "tests/product/derived_signal/test_m01_f4_nbbo_algebra_public.py",
        "admitted M00 bid/ask size source identities; imbalance 0.6, "
        "exact raw lineage; missing/future/wrong-subject refusal",
    ),
    "D018": (
        "RC02",
        "tests/product/derived_signal/test_m01_f4_vwap_gap_public.py",
        "public M00 trade price/size co-reference for D017 4.8 against provider VWAP 5; "
        "persisted D018 difference 0.2 and exact 10000*0.2/4.8 bps, "
        "source and D017 lineage, missing/future/partial trade refusal",
    ),
    "D025": (
        "RC02",
        "tests/product/derived_signal/test_m01_f4_rc02_scalar_algebra_public.py",
        "session price range position 0.5; R039/R040/R037 separate M00 sources; "
        "zero-range, missing, future and subject refusal",
    ),
    "D042": (
        "RC02",
        "tests/product/derived_signal/test_m01_f4_rc02_scalar_algebra_public.py",
        "Treasury 2s10s percentage-point slope 1.25 from canonical decimal yields "
        "R247/R249; missing/future/subject refusal",
    ),
    "D043": (
        "RC02",
        "tests/product/derived_signal/test_m01_f4_rc02_scalar_algebra_public.py",
        "Treasury 3m10y slope 1 from canonical decimal yields R246/R249; "
        "missing/future/subject refusal",
    ),
    "D047": (
        "RC02",
        "tests/product/derived_signal/test_m01_f4_rc02_scalar_algebra_public.py",
        "SOFR minus EFFR 10 basis points from canonical decimal R257/R256; "
        "missing/future/subject refusal",
    ),
    "D057": (
        "RC02",
        "tests/product/derived_signal/test_m01_f4_rc02_scalar_algebra_public.py",
        "VIX1D minus VIX9D -2 index points and ratio 0.9; R238/R239 lineage; "
        "missing/future/subject refusal",
    ),
    "D058": (
        "RC02",
        "tests/product/derived_signal/test_m01_f4_rc02_scalar_algebra_public.py",
        "VIX9D minus VIX 1 index point and ratio 20/19; R239/R236 lineage; "
        "missing/future/subject refusal",
    ),
    "D059": (
        "RC02",
        "tests/product/derived_signal/test_m01_f4_rc02_scalar_algebra_public.py",
        "VIX minus VIX3M -2 index points and ratio 19/21; R236/R240 lineage; "
        "missing/future/subject refusal",
    ),
    "D060": (
        "RC02",
        "tests/product/derived_signal/test_m01_f4_rc02_scalar_algebra_public.py",
        "VVIX/VIX ratio 110/19, zero-VIX and missing/future/subject refusal; "
        "R237/R236 lineage",
    ),
    "D131": (
        "RC12",
        "tests/product/derived_signal/test_m01_f4_option_depth_public.py",
        "M00 exact option contract selection with D087 midpoint predecessor, "
        "insert-shifted depth sum 25, historical sum 18; all raw/derived lineage; "
        "different-contract book exclusion and missing operation/midpoint refusal",
    ),
    "D134": (
        "RC12",
        "tests/product/derived_signal/test_m01_f4_positional_book_class.py",
        "M00 position-shifting operation reconstruction; top-two bid 17; "
        "missing operation refusal and exact lineage",
    ),
    "D135": (
        "RC12",
        "tests/product/derived_signal/test_m01_f4_positional_book_class.py",
        "M00 independent ask book top-two 13; explicit operations and exact lineage",
    ),
    "D136": (
        "RC12",
        "tests/product/derived_signal/test_m01_f4_positional_book_class.py",
        "M00 D134/D135 reconstructed ratio 4/30 with inherited lineage",
    ),
    "D137": (
        "RC12",
        "tests/product/derived_signal/test_m01_f4_microprice_public.py",
        "admitted M00 contemporaneous best bid/ask and independent bid/ask sizes; "
        "microprice 101.6, exact raw lineage, future and missing-size refusal",
    ),
    "D138": (
        "RC12",
        "tests/product/derived_signal/test_m01_f4_book_slope_public.py",
        "M00 source-complete price/size/side rows; D011 midpoint OLS 12.5/12; "
        "incomplete and unsupported-side refusal, predecessor/raw lineage",
    ),
    "D141": (
        "RC12",
        "tests/product/derived_signal/test_m01_f4_replenishment_public.py",
        "M00 native row depletion 4/restoration 3 at same source-side-price; "
        "score 3/4; seven raw inputs, lineage, missing-price and future-recovery refusal",
    ),
    "D142": (
        "RC12",
        "tests/product/derived_signal/test_m01_f4_resilience_public.py",
        "M00 public positional depth-shock 30 to 22 and joint spread/depth recovery "
        "after 1 second; all eight raw input identities, incomplete-event and "
        "unrecovered-historical refusal",
    ),
    "D145": (
        "RC12",
        "tests/product/derived_signal/test_m01_f4_book_ofi_public.py",
        "admitted M00 four-field ordered book; exact raw lineage; "
        "incomplete-field and cutoff refusal",
    ),
    "D139": (
        "RC12",
        "tests/product/derived_signal/test_m01_f4_book_rates_public.py",
        "controlled M00 book event rates by side/level; native event completeness; "
        "exact lineage",
    ),
    "D140": (
        "RC12",
        "tests/product/derived_signal/test_m01_f4_book_rates_public.py",
        "controlled M00 book quantity rates by side/level; "
        "native event completeness; exact lineage",
    ),
    "D143": (
        "RC12",
        "tests/product/derived_signal/test_m01_f4_direct_book_public.py",
        "controlled M00 direct venue concentration; missing venue refusal; "
        "independent venue insertion shifting, update and delete",
    ),
    "D144": (
        "RC12",
        "tests/product/derived_signal/test_m01_f4_direct_book_public.py",
        "controlled M00 SMART/direct matched-book divergence; incomplete event refusal; "
        "independent SMART and direct insertion shifting and delete",
    ),
    "D151": (
        "RC13",
        "tests/product/derived_signal/test_m01_f4_basket_breadth_public.py",
        "admitted M00 three-member basket; component-specific denominator; "
        "full lineage; missing-member refusal",
    ),
}


F4_BOUNDED_PUBLIC_ROWS["D082"] = (
    "RC05", "tests/product/derived_signal/test_m01_f4_rc05_correlations_public.py",
    "Admitted M00 four common-grid NVDA/SPY closes and P_REGRESSION three-return window; "
    "Pearson on aligned log returns yields +1 diagonal/-1 off-diagonal, full raw "
    "lineage, missing/future point, zero-return-variance and basket refusal, retry",
)


F4_BOUNDED_PUBLIC_ROWS["D179"] = (
    "RC16", "tests/product/derived_signal/test_m01_f4_rc16_fill_cost_public.py",
    "Admitted M00 arrival R221=99.8 vs fill R229=100.2; D087 quote midpoint=100 "
    "does not replace arrival benchmark; buy +0.4 and sell -0.4, exact bps, "
    "raw and predecessor lineage; missing/future/wrong-contract refusal and retry",
)
F4_BOUNDED_PUBLIC_ROWS["D193"] = (
    "RC16", "tests/product/derived_signal/test_m01_f4_rc16_fill_cost_public.py",
    "M00 matched execution quantity=3, multiplier=100, fees=2; consumes D179 "
    "signed arrival price slippage, buy cost 122 / sell cost -118, refuses "
    "missing benchmark/execution and mismatched/future quote; complete lineage and retry",
)


# RC21 D063 macro surprise proof first at d4ff247, bounded native completeness
# correction at 9a701de. Missing release fields must not delete releases
# from the selected baseline or substitute an older current print.
F4_BOUNDED_PUBLIC_ROWS["D063"] = (
    "RC21", "tests/product/derived_signal/test_m01_f4_rc21_macro_surprise_public.py",
    "M00 exact release-family native actual/consensus z-score, selected two "
    "prior surprises, complete release membership, other-family exclusion, "
    "non-zero historical SD, future-cutoff refusal, raw lineage and retry",
)


# D146/D147 bounded native macro factor scores: all named raw features plus the
# exact D063 release-family predecessor are propagated by the admitted M00 seam.
# The proof covers one versioned, coherent release-family selection; it does
# not establish arbitrarily heterogeneous macro-source joins.
F4_BOUNDED_PUBLIC_ROWS["D146"] = (
    "RC21", "tests/product/derived_signal/test_m01_f4_rc21_macro_growth_factor_public.py",
    "M00 six source-native growth fields plus complete historical D063 release "
    "surprise, exact weighted score 21+20/sqrt(200), seven-source lineage, "
    "other-family exclusion, incomplete-field and future receipt refusal, retry; "
    "bounded to one explicit release-family selection",
)
F4_BOUNDED_PUBLIC_ROWS["D147"] = (
    "RC21", "tests/product/derived_signal/test_m01_f4_rc21_macro_inflation_factor_public.py",
    "M00 five source-native inflation fields plus complete historical D063 "
    "release surprise, exact weighted score 15+20/sqrt(200), six-source lineage, "
    "other-family exclusion, incomplete-field and future receipt refusal, retry; "
    "bounded to one explicit release-family selection",
)


# RC15 D168 candidate Greek vector through exact M00 contract-leg subjects.
F4_BOUNDED_PUBLIC_ROWS["D168"] = (
    "RC15", "tests/product/derived_signal/test_m01_f4_rc15_candidate_greeks_public.py",
    "M00 exact two-member candidate basket C100/P100 with independent signed "
    "quantities and native 100x multipliers; delta 220/gamma -4/vega -5/"
    "theta 2 retained as named vector, full ten field/leg raw lineage, "
    "unselected contract exclusion, missing/future selected leg and "
    "omitted context/invalid basket refusal, retry",
)


# RC03 Stage-1-closed public proofs were committed independently, before this
# reconciliation update, at proof-first commit 3480116.  This remains bounded
# edge-level evidence rather than acceptance of all Stage 1.
RC03_WITNESS = "tests/product/derived_signal/test_m01_f4_rc03_history_public.py"
for _did in ("D019", "D020", "D021"):
    F4_BOUNDED_PUBLIC_ROWS[_did] = (
        "RC03", RC03_WITNESS,
        "M00 true-instant minute-anchor history; past-versus-near sample selection, "
        "competing instrument exclusion, exact log return, missing/late anchor refusal, "
        "future observation cutoff, persisted lineage and deterministic retry",
    )
for _did in ("D022", "D023", "D026"):
    F4_BOUNDED_PUBLIC_ROWS[_did] = (
        "RC03", RC03_WITNESS,
        "M00 exact-subject current/reference source values, log return or price/VWAP "
        "difference; missing/mismatched subject refusal, raw lineage and retry",
    )
F4_BOUNDED_PUBLIC_ROWS["D024"] = (
    "RC03", RC03_WITNESS,
    "M00 independently anchored 1m/5m/30m public predecessor graph, exact "
    "momentum vector and differences, three persisted D occurrences and ultimate "
    "R143 raw lineage; absent 30m anchor refused, retry",
)
for _did in ("D027",):
    F4_BOUNDED_PUBLIC_ROWS[_did] = (
        "RC03", RC03_WITNESS,
        "M00 aligned VWAP five-minute anchor, exact 4 price/minute and 4%/minute, "
        "closer non-anchor and competing instrument exclusion, absent anchor refusal",
    )
for _did in ("D044", "D045", "D046"):
    F4_BOUNDED_PUBLIC_ROWS[_did] = (
        "RC03", RC03_WITNESS,
        "M00 300-second time anchor for nominal/real/yield change, exact 1000 bp; "
        "nearest-without-anchor refusal, competing instrument exclusion, raw lineage",
    )
for _did in ("D048", "D049", "D050", "D051"):
    F4_BOUNDED_PUBLIC_ROWS[_did] = (
        "RC03", RC03_WITNESS,
        "M00 anchor-based 20% value change, raw lineage, competing instrument "
        "exclusion and missing proper anchor refusal",
    )
for _did in ("D052", "D053", "D054", "D055", "D056"):
    F4_BOUNDED_PUBLIC_ROWS[_did] = (
        "RC03", RC03_WITNESS,
        "M00 exact 20-point and 20% paired change over configured anchor, "
        "raw lineage and refusal with only an ineligible closer sample",
    )
for _did in ("D066", "D067", "D068", "D069"):
    F4_BOUNDED_PUBLIC_ROWS[_did] = (
        "RC03", RC03_WITNESS,
        "M00 one-day instant anchor and exact ln(1.2) return, competing instrument "
        "exclusion and absence refusal; no invented market-calendar adjustment",
    )


# RC01 public temporal/data-quality and trigger evidence, committed at 1a8a0c6.
F4_BOUNDED_PUBLIC_ROWS["D006"] = (
    "RC01", "tests/product/derived_signal/test_m01_f4_rc01_quality_public.py",
    "native M00 three-field P_SCORE source/type/cadence and actual D002 receipt age; "
    "exact versioned weighted result 2.75, persisted predecessor/raw lineage and "
    "missing/wrong-subject/refusal with deterministic retry",
)
F4_BOUNDED_PUBLIC_ROWS["D008"] = (
    "RC01", "tests/product/derived_signal/test_m01_f4_rc01_quality_public.py",
    "native M00 heterogeneous true-instant versus receipt-only sources, structured "
    "max-skew 5 sec, coverage 2/3, one missing instant and versioned sigmoid "
    "score; actual D001/D002 predecessor graph, all-receipt refusal and lineage",
)
F4_BOUNDED_PUBLIC_ROWS["D209"] = (
    "RC01", "tests/product/derived_signal/test_m01_f4_rc01_trigger_public.py",
    "versioned RecalculationSchedule and native receipt-only R001 M00 event; "
    "public trigger fact and receipt timestamp without external action, "
    "persisted raw lineage, missing/future/wrong-subject refusal and retry",
)



# RC13 D076/D077 proof-first e6b98e9, bounded sector-identity repair 0067dbc.
# This is the two-proxy standard D077 case; optional single-proxy policy is
# not independently proved by this witness and remains an explicit caveat.
F4_BOUNDED_PUBLIC_ROWS["D076"] = (
    "RC13", "tests/product/derived_signal/test_m01_f4_rc13_relative_sector_public.py",
    "M00 distinct SPY and QQQ R037/R042 observations; exact QQQ-minus-SPY "
    "log return spread, separate D072/D071 occurrence subjects and raw/D lineage, "
    "absent/future predecessor refusal, ambiguous SPY/SPX proxy refusal and retry",
)
F4_BOUNDED_PUBLIC_ROWS["D077"] = (
    "RC13", "tests/product/derived_signal/test_m01_f4_rc13_relative_sector_public.py",
    "M00 distinct SMH/SOXX/QQQ R037/R042 observations, two-proxy mean(SMH,SOXX) "
    "minus QQQ log return, three independent predecessor occurrences, full raw/D "
    "lineage and missing/future member refusal; named single-proxy mode not proved",
)

# RC14 D103 proof-first 9143a5e and bounded full-grid repair a48ded0.
# The presence of one matching point does not establish a complete comparable
# IV surface: unmatched, unclassified, duplicate and reversed snapshots refuse.
F4_BOUNDED_PUBLIC_ROWS["D103"] = (
    "RC14", "tests/product/derived_signal/test_m01_f4_rc14_surface_shift_public.py",
    "M00 native R111 matched two-strike current/prior IV grid produces exact "
    "five-vol-point mean parallel shift, four-source raw lineage and retry; "
    "missing/future/wrong-subject unmatched grid, duplicate grid, unclassified "
    "snapshot and reversed temporal ordering all refuse",
)

# F4 bounded end-to-end row demonstration: D110 native spot over D109
# exact ATM pair from both option contracts. R014 decoy is not lineage.
F4_BOUNDED_PUBLIC_ROWS["D110"] = (
    "RC14", "tests/product/derived_signal/test_m01_f4_d110_spot_expected_move_public.py",
    "M00 R118 spot 100 and exact-expiry/strike C100/P100 native mid prices "
    "5 + 4 via public D087/D091/D109 predecessor graph => D110=9 percent; "
    "persisted exact raw R118/R034/R035/R112 and D109 lineage, missing/wrong/"
    "future R118 or missing ATM put quote refusal, deterministic retry",
)

# Programme Owner 2026-10-11 controlled provider-independent official-period
# proof: both D123 catalogue edges are conditionally applicable and both have
# independently discriminated public M00 call/put tests.
F4_BOUNDED_PUBLIC_ROWS["D123"] = (
    "RC02", "tests/product/derived_signal/test_m01_f4_d123_controlled_public.py",
    "Controlled and versioned M00 official-reporting-period identities: exact call "
    "R047 / put R048 +25, absent opposite-side allowed, competing contract "
    "excluded, late prior-period correction +15 with cutoff-specific historical "
    "+25, ambiguous/missing period/revision/version refused; exact selected "
    "two raw versioned observations persisted in lineage; live provider unverified",
)


# Authorised reconstruction from 734cf58, proof-first f0e6bcd: the D041
# graph uses a separate immutable D040 P_SCORE parameter version, not the
# requesting D041 score schema; all three edges are publicly materialised.
F4_BOUNDED_PUBLIC_ROWS["D041"] = (
    "RC06", "tests/product/derived_signal/test_m01_f4_reconstruction_d041_public.py",
    "Controlled M00 D026 VWAP deviation, independently versioned D040 trend "
    "and D033 30-minute realised volatility provide exact D041 composite; "
    "full native R and immediate D lineage, nested score version-change "
    "recalculation, missing profile/version and missing history refusal, retry",
)


# Authorised reconstruction of the three independent D084 sector/dispersion
# predecessor baskets. The RED public seam precedes the bounded D084-specific
# scoped-policy production correction, with exact raw and predecessor lineage.
F4_BOUNDED_PUBLIC_ROWS["D084"] = (
    "RC06", "tests/product/derived_signal/test_m01_f4_reconstruction_d084_public.py",
    "Controlled M00 raw series for SPY/QQQ technology relative strength, "
    "SMH/SOXX/QQQ semiconductor relative strength, and NVDA/AMD/INTC "
    "contemporaneous sample dispersion are separately scoped by immutable "
    "selection-policy and parameter references; exact three-D output, "
    "14 raw observation lineages, missing/late/incompatible version/"
    "extra alias/absent child policy refusal and deterministic retry",
)


# Controlled native option public proof for four direct raw liquidity facts,
# genuine D088 spread and event-reconstructed D131 midpoint-window depth.
F4_BOUNDED_PUBLIC_ROWS["D132"] = (
    "RC06", "tests/product/derived_signal/test_m01_f4_reconstruction_d132_public.py",
    "Exact selected option-contract M00 R033/R036/R041/R062, matching "
    "D088 bid/ask spread and D131 reconstructed event-depth; score=459 "
    "with 11 raw source signal IDs, two persisted D predecessors and full "
    "source occurrence lineage; other-contract book row excluded, future "
    "book event ignored with lawful historic score=452, missing quote/book "
    "operation/direct trade-rate, wrong contract/mapping/strike rejected, retry",
)


# Reconstruction from 734cf58. Public proof exercises all six declared
# macro sources and three actual Stage-1 predecessor calculations.
F4_BOUNDED_PUBLIC_ROWS["D148"] = (
    "RC21", "tests/product/derived_signal/test_m01_f4_reconstruction_d148_public.py",
    "M00 exact six macro input values with historical prior 10y nominal/real "
    "rate anchors; D042 1.25 percentage-point slope plus D044 20 and D045 "
    "25 basis-point changes; final D148=52.3695, full eight raw/three D lineage, "
    "absent/future/wrong-subject macro and missing prior period refuse; retry",
)


# Reconstruction from 734cf58. Separate P_SCORE schemas for D149 and D061;
# R257/R256 and D047/D061 publicly evaluated from controlled M00 sources.
F4_BOUNDED_PUBLIC_ROWS["D149"] = (
    "RC21", "tests/product/derived_signal/test_m01_f4_reconstruction_d149_public.py",
    "Native M00 current R257/R256 funding rates yield D047=50 basis points; "
    "independent versioned D061 six-predecessor risk score from R236-R240; "
    "exact D149 sum and full nine raw/two immediate D lineage; missing/future/"
    "wrong-subject and missing nested score/history refusal, retry",
)


# Authorised reconstruction RC05. One immutable seven-sample OLS fit is
# established through the admitted controlled M00 public route; the three
# coefficient results share the same four aligned factor populations and
# exact truncated raw/D lineage. D078's current residual is NOT thereby proved.
for _regression_id in ("D079", "D080", "D081"):
    F4_BOUNDED_PUBLIC_ROWS[_regression_id] = (
        "RC05",
        "tests/product/derived_signal/test_m01_f4_reconstruction_regression_history_public.py",
        "Controlled M00 NVDA/SPY/QQQ/SMH/SOXX native close observations; "
        "versioned independent D075/D071/D076/D077 factor history with "
        "seven aligned timestamps and explicit P_REGRESSION window; "
        "D079=2 D080=3 D081=4, shared 28 D predecessor occurrences and "
        "40 actual R source occurrences excluding older out-of-window "
        "history, missing factor/selection and extra alias refusal, "
        "persisted exact fit lineage and deterministic retry",
    )


# Authorised reconstruction RC05: D078 out-of-sample residual draws exactly
# seven prior fitted factor rows and one current factor row; all three declared
# coefficient predecessors must share exact fitted input/version identity.
F4_BOUNDED_PUBLIC_ROWS["D078"] = (
    "RC05", "tests/product/derived_signal/test_m01_f4_reconstruction_regression_history_public.py",
    "M00 public eight-aligned-sample NVDA/SPY/QQQ/SMH/SOXX model with "
    "seven-sample prior fit D079=2 D080=3 D081=4; current outlier gives "
    "D078=0.02, three matching prior model coefficient identities, persisted "
    "source and predecessor lineage, mismatched injected beta refusal, "
    "missing aligned prior observation refusal and deterministic retry",
)


# RC06 continuation: D150's six exact Stage-1 predecessor edges are backed by
# controlled M00-to-M01 public materialisation with individually versioned
# P_SCORE profiles, independent scalar oracle, persisted raw/D lineage,
# required-child absence/refusal, temporal and mapping-version adversarial cases.
# The D104 mixed-skew RED and its semantic authority blocker remain untouched.
F4_BOUNDED_PUBLIC_ROWS["D150"] = (
    "RC21",
    "tests/product/derived_signal/test_m01_f4_d150_composite_public.py",
    "Controlled M00 exact D070/D146/D147/D148/D149/D048 graph with independently "
    "versioned K07 child feature schemas, D063 release history and matched "
    "time anchors, exact composite 195.8972630820587276330172811, "
    "51 selected raw lineage entries, six persisted direct D lineage IDs, "
    "deterministic retry, missing member from each of six parents refusal, "
    "missing release consensus, incompatible mapping version, wrong subject "
    "and knowledge-cutoff refusal; no external-provider integration claim",
)


# Programme Owner 2026-10-12, D104-20261012-01: each skew family is
# separately history-selected and D104 is the 10-delta change minus 25-delta
# change. Public M00 snapshots, persisted prior skew occurrences and direct
# raw/derived provenance are tested before crediting these two exact edges.
F4_BOUNDED_PUBLIC_ROWS["D104"] = (
    "RC14",
    "tests/product/derived_signal/test_m01_f4_d104_owner_rule.py",
    "Controlled two-refresh M00 exact-expiry native option surfaces; prior and current "
    "D099/D100 materialised independently; D104=0 for matching +10/+10 skew "
    "changes with exactly four persisted D predecessor identities and 24 raw "
    "observation identities; adversarial missing family/prior, mismatched "
    "expiry, incomplete native point, reverse-family regression and retry",
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    assert _sha256(AUTHORITY) == NORMATIVE_SHA256, "Accepted catalogue hash drift"
    with AUTHORITY.open(newline="", encoding="utf-8") as handle:
        catalogue = list(csv.DictReader(handle))
    assert len(catalogue) == 209
    authoritative = {item["derived_id"]: item for item in catalogue}
    assert len(authoritative) == 209
    stage1 = {
        did
        for did, item in authoritative.items()
        if item["kernel_id"].split("_", 1)[0] in STAGE1_KERNELS
    }
    assert len(stage1) == 174

    def closed(did: str, seen: frozenset[str] = frozenset()) -> bool:
        assert did not in seen, "Catalogue D graph must remain acyclic"
        if did not in stage1:
            return False
        return all(
            closed(dep, seen | {did})
            for dep in authoritative[did]["derived_dependencies"].split(";")
            if dep
        )

    closed_rows = {did for did in stage1 if closed(did)}
    deferred = stage1 - closed_rows
    assert (len(closed_rows), len(deferred)) == (144, 30)
    assert set(F4_BOUNDED_PUBLIC_ROWS).issubset(closed_rows)

    with F3.open(newline="", encoding="utf-8") as handle:
        old_edges = list(csv.DictReader(handle))
    assert len(old_edges) == 489, "Historical F3 ledger must remain the original 488+1"
    old_by_identity = {(e["derived_row"], e["source_type"], e["source_id"]): e for e in old_edges}
    assert len(old_by_identity) == 489
    classified = ROOT / "handoff/m01_completion/foundation/F1_CLASSIFIED_EDGE_MAP.csv"
    with classified.open(newline="", encoding="utf-8") as handle:
        historical_f1_edges = list(csv.DictReader(handle))
    assert len(historical_f1_edges) == 491, "historical F1 + D134/D135 correction is preserved"
    # D116-only 2026-10-11 programme-owner correction; original F1 and F3
    # ledgers remain immutable historical evidence. Mechanically rebase the
    # effective F4 relationship census to the currently accepted catalogue.
    canonical_edges = []
    for original in historical_f1_edges:
        if original["derived_id"] != "D116":
            canonical_edges.append(original)
            continue
        if original["source_id"] == "R075":
            for ordinal, rid in ((2, "R047"), (3, "R048")):
                amended = dict(original)
                amended.update({
                    "edge_id": f"D116:R:{ordinal:02d}",
                    "source_id": rid,
                    "dependency_ordinal": str(ordinal),
                    "raw_dependencies": "R041;R047;R048",
                    "authority_rule": f"§5 K02; programme owner 2026-10-11; D116/{rid}",
                    "relationship_label": ("Conditional exact-contract call/put "
                                           "open-interest source"),
                })
                canonical_edges.append(amended)
        else:
            amended = dict(original)
            amended["raw_dependencies"] = "R041;R047;R048"
            canonical_edges.append(amended)
    assert len(canonical_edges) == 492, "491 active dependencies plus D007 sentinel"
    assert {(x['source_id']) for x in canonical_edges if x['derived_id']=='D116'} == {
        'R041', 'R047', 'R048'
    }
    edges = []
    added = []
    for edge in canonical_edges:
        key = (edge["derived_id"], edge["source_type"], edge["source_id"])
        inherited = old_by_identity.get(key)
        if inherited is None:
            assert key in {
                ("D134", "R", "R187"), ("D135", "R", "R187"),
                ("D116", "R", "R047"), ("D116", "R", "R048"),
            }, key
            added.append(key)
            item = {
                "f1_edge_id": edge["edge_id"],
                "derived_row": edge["derived_id"],
                "source_type": edge["source_type"],
                "source_id": edge["source_id"],
                "relationship_class": edge["relationship_class"],
                "stage2_boundary": edge["stage2_boundary"],
                "f3c_disposition": "F4_OUTSTANDING_RELATIONSHIP_PROOF",
                "evidence_and_scope": (
                    "Programme Owner authorised amended edge; no inherited F3 proof"
                ),
            }
        else:
            item = dict(inherited)
            item["f1_edge_id"] = edge["edge_id"]
            assert item["relationship_class"] == edge["relationship_class"]
            assert item["stage2_boundary"] == edge["stage2_boundary"]
        edges.append(item)
    assert len(added) == 4 and len(edges) == 492
    ids = [item["f1_edge_id"] for item in edges]
    assert len(set(ids)) == 492
    assert sum(item["source_type"] in {"R", "D"} for item in edges) == 491
    for item in edges:
        did = item["derived_row"]
        if did in F4_BOUNDED_PUBLIC_ROWS:
            expected_class, witness, proof = F4_BOUNDED_PUBLIC_ROWS[did]
            assert item["stage2_boundary"] == "STAGE1_CLOSED"
            assert item["relationship_class"] == expected_class
            assert item["f3c_disposition"] == "F4_OUTSTANDING_RELATIONSHIP_PROOF"
            item["f4_disposition"] = "F4_BOUNDED_PUBLIC_ROW_PROOF"
            item["f4_evidence"] = witness + ": " + proof
        elif did == "D007" and item["source_type"] == "NONE":
            assert item["f3c_disposition"] == "ZERO_EDGE_SENTINEL_NO_DEPENDENCY"
            item["f4_disposition"] = "F4_ZERO_EDGE_PUBLIC_PROOF"
            item["f4_evidence"] = (
                "tests/product/derived_signal/test_m01_f4_required_field_public.py: "
                "required-field policy and M00 projection with allowed absence, future refusal"
            )
        else:
            item["f4_disposition"] = item["f3c_disposition"]
            item["f4_evidence"] = item["evidence_and_scope"]

    statuses = Counter(item["f4_disposition"] for item in edges)
    assert statuses == {
        "F2_ACCEPTED_SCOPED_EVIDENCE": 18,
        "F3A_BOUNDED_PUBLIC_PROOF": 4,
        "F3B_BOUNDED_PUBLIC_PROOF": 7,
        "F4_BOUNDED_PUBLIC_ROW_PROOF": 355,
        "STAGE2_BOUNDARY_DEFERRED": 107,
        "F4_ZERO_EDGE_PUBLIC_PROOF": 1,
    }, statuses
    csv_target = OUT / "F4_RELATIONSHIP_PROOF_LEDGER.csv"
    columns = [*edges[0].keys()]
    with csv_target.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, columns)
        writer.writeheader()
        writer.writerows(edges)
    # Full-population evidence readback: a bounded edge status is not Stage-1
    # acceptance, and a Stage-2 boundary is an unsatisfied kernel/public proof.
    by_row: dict[str, list[dict[str, str]]] = {did: [] for did in stage1}
    by_class: dict[str, list[dict[str, str]]] = {}
    for item in edges:
        if item["derived_row"] in by_row:
            by_row[item["derived_row"]].append(item)
        by_class.setdefault(item["relationship_class"], []).append(item)
    row_records: list[dict[str, object]] = []
    for did in sorted(stage1):
        row_edges = by_row[did]
        pending_count = sum(
            item["f4_disposition"] == "F4_OUTSTANDING_RELATIONSHIP_PROOF" for item in row_edges
        )
        if did in deferred:
            status = "CROSS_STAGE_OWN_KERNEL_AND_PUBLIC_REFUSAL_UNPROVED"
        elif any(
            item["f4_disposition"] == "F4_AUTHORITY_BLOCKED_SOURCE_SEMANTICS"
            for item in row_edges
        ):
            status = "STAGE1_CLOSED_NORMATIVE_SOURCE_AUTHORITY_BLOCKED"
        elif pending_count:
            status = "STAGE1_CLOSED_PUBLIC_RELATIONSHIP_PROOF_UNRESOLVED"
        else:
            status = "BOUNDED_EDGE_EVIDENCE_ONLY_NO_ROW_ACCEPTANCE"
        row_records.append(
            {
                "derived_id": did,
                "stage_boundary": "CROSS_STAGE" if did in deferred else "STAGE1_CLOSED",
                "public_acceptance_status": status,
                "total_ledger_relationships": len(row_edges),
                "outstanding_stage1_closed_edges": pending_count,
                "observed_bounded_dispositions": ";".join(
                    sorted({item["f4_disposition"] for item in row_edges})
                ),
                "relationship_classes": ";".join(
                    sorted({item["relationship_class"] for item in row_edges})
                ),
            }
        )
    assert len(row_records) == 174
    assert sum(x["stage_boundary"] == "STAGE1_CLOSED" for x in row_records) == 144
    assert sum(x["stage_boundary"] == "CROSS_STAGE" for x in row_records) == 30
    assert sum(x["outstanding_stage1_closed_edges"] for x in row_records) == 0
    with (OUT / "F4_ROW_EVIDENCE_MATRIX.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, list(row_records[0]))
        writer.writeheader()
        writer.writerows(row_records)
    class_records = []
    for cl, group in sorted(by_class.items()):
        missing = [
            item for item in group if item["f4_disposition"] == "F4_OUTSTANDING_RELATIONSHIP_PROOF"
        ]
        class_records.append(
            {
                "relationship_class": cl,
                "declared_ledger_records": len(group),
                "stage1_closed_outstanding_edges": len(missing),
                "stage1_closed_authority_blocked_edges": sum(
                    item["f4_disposition"] == "F4_AUTHORITY_BLOCKED_SOURCE_SEMANTICS"
                    for item in group
                ),
                "stage1_closed_outstanding_rows": len({item["derived_row"] for item in missing}),
                "stage2_deferred_edges": sum(
                    item["f4_disposition"] == "STAGE2_BOUNDARY_DEFERRED" for item in group
                ),
                "status": (
                    "SOURCE_AUTHORITY_BLOCKED"
                    if any(
                        item["f4_disposition"] == "F4_AUTHORITY_BLOCKED_SOURCE_SEMANTICS"
                        for item in group
                    )
                    else "UNPROVED" if missing else "NO_OPEN_STAGE1_EDGES_NOT_CLASS_ACCEPTANCE"
                ),
            }
        )
    assert sum(x["stage1_closed_outstanding_edges"] for x in class_records) == 0
    assert sum(x["stage1_closed_authority_blocked_edges"] for x in class_records) == 0
    with (OUT / "F4_CLASS_PROOF_RECONCILIATION.csv").open(
        "w", newline="", encoding="utf-8"
    ) as handle:
        writer = csv.DictWriter(handle, list(class_records[0]))
        writer.writeheader()
        writer.writerows(class_records)
    metadata = {
        "authority_catalogue_sha256": _sha256(AUTHORITY),
        "prior_f3_ledger_sha256": _sha256(F3),
        "stage1_rows": len(stage1),
        "stage1_closed_rows": len(closed_rows),
        "cross_stage_rows": len(deferred),
        "f4_new_bounded_public_rows": sorted(F4_BOUNDED_PUBLIC_ROWS),
        "total_dependency_edges": 491,
        "stage1_closed_rows_with_outstanding_edges": sum(
            bool(item["outstanding_stage1_closed_edges"]) for item in row_records
        ),
        "cross_stage_kernel_and_refusal_rows_unproved": 30,
        "stage1_closed_authority_blocked_rows": [],
        "stage1_closed_authority_blocked_edges": 0,
        "d116_corrected_dependencies": ["D116/R041", "D116/R047", "D116/R048"],
        "d123_provider_independent_proof": "BOUNDED_PUBLIC_VERIFIED_LIVE_PROVIDER_UNVERIFIED",
        "new_authorised_raw_edges": ["D134/R187", "D135/R187"],
        "zero_edge_sentinels": 1,
        "f4_dispositions": dict(sorted(statuses.items())),
        "unresolved_rc12_public_rows": [],
        "historical_three_field_witness": "retained in commit 450b7e6; formerly produced zero",
        "repaired_event_witness": "explicit R187 operation; D134=10, D135=7, D136=3/17",
        "depth_snapshot_vs_event_reconstruction_authority": "AUTHORISATION_RESOLVED_EVENT_DRIVEN",
        "stage1_f4_candidate_ready": False,
        "stage1_independent_acceptance": False,
        "boundary": (
            "Bounded row proofs do not prove all 144 Stage-1-closed rows or 30 cross-stage rows; "
            "30 cross-stage own-kernel/refusal obligations remain unproved and prevent "
            "Stage-1 candidate acceptance; D116 controlled ratio is bounded proof only"
        ),
    }
    (OUT / "F4_PROGRESS_READBACK.json").write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(metadata, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
