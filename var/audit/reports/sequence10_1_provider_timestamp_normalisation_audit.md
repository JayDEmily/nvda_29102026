# Sequence 10.1 provider timestamp normalisation audit

| Provider/source type | Raw timestamp/date field | Raw timezone source | Canonical repo field | Whether source_time_utc is lawful | Whether source_date is required instead | Whether captured_at_utc/persisted_at_utc must remain distinct |
|---|---|---|---|---|---|---|
| IBKR historical bars | Not implemented in accepted source adapter surface | Not available in accepted source | `source_time_utc` only after adapter proves timestamp precision/timezone | Gap registered: no IBKR historical bar parser exists in accepted source to prove conversion | Required for date-only historical bars if provider emits daily/date-level payload | Yes |
| IBKR real-time bars | Not implemented in accepted source adapter surface | Not available in accepted source | `source_time_utc` only after adapter proves timestamp precision/timezone | Gap registered: no IBKR real-time bar adapter exists in accepted source to prove conversion | No, unless provider emits date-only payload | Yes |
| IBKR daily bars | Not implemented in accepted source adapter surface | Not available in accepted source | `source_date` for date-level payloads; `source_time_utc` only for timestamped payloads | Not lawful to invent intraday precision from a daily bar date | Yes, when source payload is date-level | Yes |
| FRED-style .org/date-level macro data | Not implemented in accepted source adapter surface | Source calendar/date only if imported later | `source_date` | Not lawful for date-only payloads unless an external provider contract supplies a timestamp | Yes | Yes |
| Asia/HK/Japan reference calendar or precursor venue context | Calendar/reference projection surfaces exist, but no provider timestamp normalisation path proves source observation conversion | Venue/reference calendar fields, not observation timestamp timezone proof | `source_date` or event-window fields unless a timestamped provider contract is admitted | Gap registered for future provider adapter/readiness sequence | Required for date-level calendar records | Yes |

## Audit decision

Accepted source contains placeholder/fixture-style ingress adapters and calendar/reference projection surfaces, but no live IBKR/FRED/date-level provider normalisation implementation. Sequence 10.1 therefore hardens the internal temporal contract and registers provider-specific conversion as an adapter proof gap. It does not double-convert timestamps and does not invent timestamp precision for date-level sources.
