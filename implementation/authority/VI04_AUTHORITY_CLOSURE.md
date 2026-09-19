# VI-04 — Programme authority closure for required implementation Unknowns

## Status

**ACCEPTED CURRENT PROGRAMME AUTHORITY — 2026-09-19 (Australia/Melbourne).**

This record captures the explicit human/programme authority given after VI-03 identified the smallest implementation-required Remaining Unknown set.

The user replied:

> Yeah, I authorize it.

That assent applies to the immediately preceding proposed authority block, reproduced here exactly as the authorised scope:

> Authorise VI-04 to use `nvda_desk.raw_signal_occurrence_truth` as the M-owner package with public seam `nvda_desk.raw_signal_occurrence_truth.api`; use `psycopg[binary]==3.3.4` as the PostgreSQL Python driver; and authorise the implementation worker to choose the smallest correctness-only PostgreSQL relation layout, SQL types and dependent direct repository/adapter form necessary to satisfy BC-011. PostgreSQL/schema/driver remain non-owning mechanisms and may not define Raw Signal semantics. Do not introduce partitioning, pooling, performance/SLA policy or separately designed performance indexes; correctness constraints may use the database mechanisms intrinsically required to enforce them. Keep final distribution/version metadata unresolved until VI-15. PostgreSQL 17.9 may be used as the recorded proof environment without making 17.9 a production-version requirement.

## Authority effects

This current authority closes only the following implementation-required Unknowns:

1. **Owner package / public seam**
   - package: `nvda_desk.raw_signal_occurrence_truth`;
   - public seam: `nvda_desk.raw_signal_occurrence_truth.api`.

2. **PostgreSQL Python driver**
   - `psycopg[binary]==3.3.4`.

3. **Physical PostgreSQL implementation delegation**
   - the implementation worker may choose only the **smallest correctness-only** PostgreSQL relation/table layout, SQL/database types, and dependent direct repository/adapter form required to satisfy BC-011 and the accepted proof obligations;
   - that delegation does not transfer Raw Signal semantic authority to PostgreSQL, SQL schema, driver, repository or adapter;
   - selected physical forms must remain downstream of the M owner semantic persistence port and must be justified against the accepted IWO/proof surface before implementation.

4. **Proof environment**
   - PostgreSQL `17.9` is authorised as the recorded local proof environment;
   - this does not create a production PostgreSQL version requirement.

## Explicit non-authority / preserved Unknowns

This authority does **not** authorise:

- PostgreSQL partitioning;
- connection pooling;
- performance/SLA policy;
- independently designed performance indexes;
- a production PostgreSQL version requirement;
- P01/DMPV3;
- K01;
- authoritative replay;
- live provider/network integration;
- live external side effects or account authority;
- downstream business consumers;
- retention/deletion/recovery/SLA semantics;
- any other BC-016 Remaining Unknown not expressly closed above.

Correctness constraints may use database-intrinsic enforcement mechanisms only where required to make the authorised semantic invariants true; such mechanisms are not performance-policy authority.

Final **distribution/version metadata** remains unresolved and is deferred to the VI-15 packaging dependency. This VI-04 authority fixes the owner package path/public seam but does not select final distribution naming/version metadata.

## Lineage

- predecessor accepted VI-03 commit: `0662a1b1788986de69de1d644fc84a7436471b74`;
- predecessor tree: `07a41ae69db8ff719922f085be132751b4666c4f`;
- IRB SHA-256: `938debe255d68668b0ae60f021d679fc8e3022be6eb050e7f3cd6112818fd342`;
- accepted BICP JSON SHA-256: `5b99cead41fd8d3d372b5ed2ef4558065328b814e0a94c3680162fc6594df5ed`;
- prior implementation-authorisation reference: `IA-AUTH-001`.

This authority supplements the accepted BICP only for the exact implementation-required Remaining Unknowns above. It does not alter the BICP's semantic meaning.

## VI-04 disposition

With this authority:

- physical PostgreSQL table/layout design: **AUTHORITY CLOSED BY BOUNDED DELEGATION**;
- SQL/database types: **AUTHORITY CLOSED BY BOUNDED DELEGATION**;
- PostgreSQL driver selection: **AUTHORISED — `psycopg[binary]==3.3.4`**;
- dependent concrete repository/store form: **AUTHORITY CLOSED BY BOUNDED DELEGATION**;
- final owner-package name/public seam: **AUTHORISED**;
- final distribution/version metadata: **DEFERRED / STILL UNKNOWN UNTIL VI-15**.

No physical design is selected by this record itself beyond the fixed driver and package/public-seam identities. The bounded physical PostgreSQL choices remain to be derived under the accepted IWO/proof process.
