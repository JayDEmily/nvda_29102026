# VI-11R Tester Iteration 004 Disposition

## Status

`FAIL / RETURN_TO_WORKER — ROUTED TO VI-10R2 PROOF REPAIR`

Fresh independent VI-11R review of the VI-10R successor returned eleven material proof-adequacy findings. The reviewed candidate remains preserved in Git history. Production implementation remains prohibited.

## Exact review binding

- tester archive SHA-256: `17be4cd55336d9daee27109fcbc59ae162583af1d2f56b2ab0b5fb37f06262aa`
- tester response SHA-256: `86444f62118c52ca1c65ed3557b5c6d064e514a9d9193f2d1a25d2d4973b7814`
- reviewed wrapper HEAD: `120966888cff16a6b083ddf670fde302eb7b9bcc`
- reviewed wrapper tree: `7ec1c39d2243e8025eddf05bbf919957a6b8c5f8`
- reviewed physical proof candidate: `375e61b73c219a40c9fc2e9684cf3f3e26d25d54`
- reviewed physical proof tree: `a45d5678aedea4e116f5e5a390b2bb6a128c33e4`
- failed predecessor remains preserved: `f83efd9b489dbe7072da8c96320504a468c55a1a`

The tester independently verified transport, Git identity, 155-test collection, 13/13 structural obligation coverage, 74/74 architecture/bootstrap proof, mypy, Ruff, dependency and seam validation. The failure is therefore proof adequacy, not transport or basic proof-control integrity.

## Findings and owning repair

| Finding | Severity | Required proof repair |
|---|---|---|
| `T004-F001` | Critical | discriminate PostgreSQL as the semantic durable source, not merely a participant |
| `T004-F002` | Critical | prove each occurrence/assessment success is independently committed before later commands |
| `T004-F003` | Important | exact fresh-process readback of complete original facts plus lineage/schedule context |
| `T004-F004` | Critical | use genuinely distinct opaque typed identity values rather than lexical string prefixes |
| `T004-F005` | Important | cover complete five-contract `.v1` compatibility dimensions |
| `T004-F006` | Important | reject conflicting same-policy-ID/version re-registration and preserve original |
| `T004-F007` | Important | prove presence-side exact preservation of every optional provider metadata field |
| `T004-F008` | Important | discriminate decreasing same-scope ingestion sequence while permitting independent scopes |
| `T004-F009` | Critical | prove exact effective-policy/observation inputs to eligibility authority and relation lineage |
| `T004-F010` | Critical | discriminate M00 semantic ownership from repository/adapter-owned semantic decisions |
| `T004-F011` | Important | prove complete A00 semantic command/read argument wiring, not order alone |

## Authority disposition

The findings remain downstream proof defects. They do not alter the accepted IRB, BICP, IWO, routed METHOD-006 normatives, architecture allocation, six-family decomposition, thirteen product obligations, or product tier treatment.

Under the accepted ExecPlan owning-layer rule, all eleven findings return to successor pre-implementation proof repair. No `src/nvda_desk/**` production behaviour is authorised until a fresh independent VI-11R rechallenge accepts the successor proof candidate.
