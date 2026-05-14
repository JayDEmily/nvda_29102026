# Financial Calendar Bundle v1 (2026)

This bundle is a **proposal-quality reference calendar pack** for the NVDA desk-cognition repo.

It is designed to solve the exact problem discussed in the planning thread:

- reduce avoidable surprise
- preserve scheduled context that a serious operator already knows
- keep the raw calendar broader than the runtime references
- project only narrow deterministic tags into the live stack
- emit DMPV3 reference packets while routing retained legacy support artefacts into an explicit archive subtree as evidence

## Why this exists

The repo already has event/session surfaces, but the current live path is too thin for the next adaptation layer.

A Tier 1-style operator does not need a bloated "calendar of everything".
They need a **curated scheduled-facts scaffold** covering:

1. **U.S. market structure**
   - cash-market closures
   - half-days
   - listed-options expiry anchors
   - month-end / quarter-end markers

2. **U.S. macro and policy**
   - FOMC
   - CPI
   - Employment Situation / payrolls
   - PPI
   - Personal Income and Outlays / PCE
   - GDP release ladder

3. **NVDA and direct read-through corporate catalysts**
   - NVDA earnings
   - a small set of hyperscaler / mega-cap dates that can change NVDA demand interpretation

4. **Asia precursor venue context**
   - JPX cash holidays
   - JPX derivatives holiday-trading distinctions
   - HKEX holidays and half-days
   - Stock Connect availability
   - mainland A-share holiday spans

## Files

- `financial_calendar_master_2026.json`  
  Master manifest and layer index.

- `layers/01_layer_01_us_market_structure_2026.json`  
  U.S. cash/expiry/month-end structure.

- `layers/02_layer_02_us_macro_policy_2026.json`  
  U.S. macro and policy dates.

- `layers/03_layer_03_nvda_sector_catalysts_2026.json`  
  NVDA and direct read-through corporate catalysts.

- `layers/04_layer_04_asia_precursor_venue_context_2026.json`  
  Japan / Hong Kong / mainland-China precursor venue state.

- `source_manifest.json`  
  Official source inventory used to populate this bundle.




## Design choices

### 1. JSON, not SQL
You said you don't want a SQL setup for this, and that makes sense at this stage.

JSON is the right intermediate format here because:
- it is simple to review
- it is easy to diff in Git
- it matches the repo's planning/data style
- it can later be imported into a DB if needed
- it works naturally with DMPV3 reference packets and retained legacy support artefacts

### 2. Raw truth first, derived tags later
The bundle stores **raw scheduled facts**.
The runtime should consume **derived tags**, not the entire raw calendar.

Examples:
- raw fact: `2026-06-19` is Juneteenth and NYSE is closed
- derived tag: `us_cash_closed`

- raw fact: `2026-09-22` is a Japan holiday but JPX derivatives holiday trading is open
- derived tag: `jpx_derivatives_open`

- raw fact: NVIDIA reports on `2026-05-20`
- derived tag: `nvda_earnings`

This keeps the calendar durable while keeping runtime state narrow.

### 3. Curated, not exhaustive
This bundle intentionally does **not** include:
- every foreign earnings date
- every low-impact data release
- unscheduled headline risk
- opinionated alpha conclusions

It is a **scheduled-facts layer**, not a news engine.

### 4. Confirmed events only in the corporate layer
For corporate catalysts, this pack stores only dates that are confirmed on official IR or company pages.
It does **not** invent future earnings dates.

That means the corporate layer will always be incomplete far into the future — and that is correct.

## How this should sit in the repo

Suggested on-repo location:

`data/reference/financial_calendar/`

Likely consumers:
- `src/nvda_desk/services/events.py`
- `src/nvda_desk/services/temporal_context.py`
- future modifier-policy surfaces
- review/evaluation segmentation

Likely import projection:
- venue closures / half-days -> `SessionCalendarCreate`
- macro, expiry, earnings, precursor-state dates -> `MarketEventCreate`
- runtime tags -> temporal / event / carry context surfaces

## Active DMPV3 fit and retained legacy support

This bundle should **not** be shoved into one giant runtime JSON object.

The active repo pattern is:
- one DMPV3 reference packet carrying bundle metadata and authoritative artefact references in the payload
- explicit retained legacy support files listed separately from the active packet shell

That lets the repo keep:
- lineage
- review traceability
- schema discipline
- authoritative artefact references
- explicit separation between active DMPV3 truth and retained legacy support evidence

without inflating runtime packets or confusing the active shell with the retained legacy example.

## Notes and limits

- This bundle is for **2026 scheduled facts**.
- Corporate entries are only as complete as current official announcements allow.
- Mainland China cash-market spans use the official SZSE 2026 calendar and HKEX Stock Connect calendar as corroboration for Shanghai/Shenzhen closure state.
- The presence of a calendar event does **not** mean the event must become a primary signal.
  It means the repo can now test whether it matters for:
  - routing
  - permissioning
  - posture
  - evaluation slicing
  - review packets

## Recommended next repo step

Do **not** wire every event straight into runtime behaviour.

First:
1. import the reference bundle
2. project narrow daily tags
3. expose those tags in event/temporal context
4. only then test whether specific posture or review rules should reference them
