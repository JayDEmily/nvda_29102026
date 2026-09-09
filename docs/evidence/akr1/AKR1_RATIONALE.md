# AKR-1 canonical end-state inventory — reconstruction evidence

## Scope

This record re-executes AKR-1 after loss of the prior sandbox Git objects. It does not recreate the lost commit SHA. Classification starts from exact source HEAD `892a6c042f19d19d84a3d1fb2c639033789f9bc1` plus the explicitly accepted reconstructed governance commit.

## Authorities and challenge evidence read

- `GUARDRAILS.md`, `AGENTS.md`, current accepted `EXEC_PLAN.md`;
- current architecture taxonomy, kernel, dependency, public-seam, proof/promotion and extension/retirement laws;
- current reset brief in full;
- September 2026 conformance ADR in full;
- mature pre-reset Native Architecture Blueprint core/working material at `d24f9626a23b526384668b3cb26ee811b235eb5c`;
- mature DMPV3 and domain architecture material needed to distinguish carrier/protocol, semantic owner, persistence/mechanism and cross-cutting governance responsibilities.

Historical material is challenge evidence only. It does not reactivate M00–M15 allocation or business behaviour.

## Governing architectural conclusions

1. `M`, `P`, `G`, `A`, `K` and `S` are distinct categories. A surface is not automatically a module/package.
2. A protocol/carrier does not acquire the semantic meaning it transports; DMPV3 therefore remains category `P`, not a runtime semantic owner merely because historical code used `M04`.
3. A technical state/transaction mechanism does not acquire its consumers' semantic record ownership.
4. Semantic ownership, authorised writing/persistence, coordination, reading and review are separate responsibilities.
5. Historical M00–M15 allocation is evidence, not automatic current allocation.
6. The current Raw Signal Gate-0/Gate-1/Codex control system is programme/development orchestration, not permanent behaviour-neutral kernel law.
7. The permanent kernel must be able to admit the first lawful active module; the reset-only empty-module validator cannot remain unchanged.
8. Exact architecture proof must exercise the actual representation/path it claims.

## Reproduced executable defects affecting classification

### Public-seam ImportFrom bypass

With registered active M01/M02 owners and a declared edge:

```text
import nvda_desk.m02.internal
-> PRIVATE_SEAM

from nvda_desk import m02
-> no violations
```

The second form bypasses current owner/seam recognition because the analyser resolves only the `ImportFrom.module` path and does not resolve the imported member as an owner path. Therefore `src/nvda_desk/architecture/dependencies.py` and `tests/architecture/test_public_seam_law.py` are `REWRITE`.

### Reset-only first-active-module blocker

`src/nvda_desk/architecture/validation.py` raises `runtime module registry must be empty during the reset` whenever an active module exists. This is correct reset-history behaviour but cannot be the permanent first-active-module admission rule. It is `REWRITE`.

### Proof discovery scope

`src/nvda_desk/architecture/proof.py` uses top-level `glob("test_*.py")` under the two test jurisdictions. The written proof law refers to every physical test in those jurisdictions. The permanent system must make implementation and law agree. Textual proposition-ID discovery proves binding/addressability only, not semantic entailment. `proof.py` and its proof-control tests are `REWRITE`.

## Classification totals

```text
KEEP                    54
REWRITE                 39
HISTORICAL_ONLY          3
DO_NOT_CARRY_FORWARD   122
BLOCKED                   0
TOTAL                   218
```

The 218 total includes these two AKR-1 evidence files. They are themselves `DO_NOT_CARRY_FORWARD`: Git history preserves the decision evidence without making it permanent kernel authority.

## AKR-2 boundary

AKR-2 must apply only the 63 programme/domain-specific `DO_NOT_CARRY_FORWARD` classifications. The 57 pre-existing reset/audit evidence files and these two AKR-1 evidence files are not part of AKR-2 programme-surface removal; they remain available for AKR-3 reconciliation before later target-tree simplification.
