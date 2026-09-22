# Tester Iteration 014 — bounded VI-11 review directive

## Status

**CURRENT TESTER DIRECTIVE — Programme Owner authorised, 2026-09-22.**

This directive operationalises the current root `EXEC_PLAN.md` sections 6.3, 6.4, 6.4A,
6.4B, 6.4C and the VI-11 current-tranche transition rule for the already-submitted
VI-10R11 candidate.

It does not change IRB/BICP/IWO/METHOD-006/BUILD-001 meaning, production source, accepted
product obligations or the physical VI-10R11 candidate. It changes the **scope and routing of
Tester Iteration 014** so that VI-11 decides bounded pre-implementation contract adequacy rather
than attempting implementation-independent closure of every hypothetical future proof-harness
escape.

`implementation/handoff/REVIEWER_020_VI11R11_PROOF_ADEQUACY.md` remains preserved as historical
assignment evidence. Where its challenge breadth or execution requirements conflict with this
directive or the current root `EXEC_PLAN.md`, this directive and the current root plan govern.
Do not rewrite or relabel Reviewer 020.

## Exact review target

Audit the exact already-submitted VI-10R11 candidate:

- submitted handoff branch: `work/vi10r11-proof-repair`;
- submitted handoff commit: `8c87fef8ed38a6ebbbd1ec65eb34618df3834bbf`;
- physical proof commit: `cca84de4ce2e9df52647352237c8a64e52a10db5`;
- physical proof tree: `6b7881fc045345eef357248f4fa8f75f38599923`;
- Tester Iteration 013 continuity commit: `39b5ca75e74ecd5cdee50c66c3a26fe3f34aec65`;
- preserved predecessor physical proof: `548a61107fda52e643142542ddb60dee584bd46e`;
- physical candidate changed path: one `tests/product/raw_signal/**` path;
- production-source changes in the physical candidate: none.

The current `main` branch contains later governance/handoff control only. Its existence does **not**
constitute VI-11 acceptance, a Tester PASS, or production implementation.

Bind the review separately to the supplied transport/archive identity after verifying it. Do not
infer repository identity from the archive filename.

## Mandatory read order

Before substantive review:

1. root `GUARDRAILS.md` in full;
2. root `AGENTS.md` in full;
3. root `EXEC_PLAN.md` in full, especially sections 6.3-6.4C and VI-11;
4. this directive;
5. `handoff/tester_continuity/iteration_013/RESPONSE.md` and `EVIDENCE.md`;
6. `implementation/proof/VI11R10_TESTER_ITERATION_013_DISPOSITION.md`;
7. `implementation/proof/VI10R11_ADVERSARIAL_PRODUCT_PROOF_REPAIR_DESIGN.md`;
8. `implementation/proof/VI10R11_ADVERSARIAL_PRODUCT_PROOF_REPAIR_EVIDENCE.md`;
9. `tests/AGENTS.override.md`;
10. the exact VI-10R11 physical diff and complete affected proof file;
11. `implementation/handoff/REVIEWER_020_VI11R11_PROOF_ADEQUACY.md` as preserved historical
    challenge context, subject to this directive and the current plan.

## VI-11 question

Tester Iteration 014 answers this question:

> Does the bounded pre-implementation proof faithfully represent the accepted semantic contract,
> discriminate material semantic violations sufficiently to authorise the first bounded
> implementation unit, and state its evidence limits truthfully?

It does **not** ask whether the proof harness defeats every conceivable Python object graph,
process topology, transaction construction, SQL representation or other hypothetical future
implementation technique before production code exists.

## Finding classification — mandatory

Classify every material finding into exactly one current proof class before deciding whether it
blocks VI-12R.

### 1. `PRE_IMPLEMENTATION_CONTRACT_PROOF`

A finding is blocking at VI-11 only when it establishes at least one of the following:

- accepted semantic meaning is absent or materially misrepresented in the bounded contract;
- a materially semantically wrong first implementation could satisfy the bounded contract;
- the proof makes a claim that its present evidence does not establish and that claim is required
  for the bounded pre-implementation contract;
- an explicit current governing invariant requires this proposition to be closed before the first
  implementation unit.

A finding in this class may justify `FAIL / RETURN_TO_WORKER`.

### 2. `IMPLEMENTATION_COUPLED_ADVERSARIAL_PROOF`

Use this class when the issue depends on, or is most meaningfully tested against, the actual future
candidate implementation: its object graph, dependency topology, concrete adapter exposure,
transaction strategy, process structure or another realised false-positive path.

Record the finding precisely and route it to VI-13R. **Do not return VI-11 FAIL solely because this
class contains an unresolved hypothetical implementation technique.**

### 3. `MILESTONE_REAL_BOUNDARY_PROOF`

Use this class for heavyweight environment-dependent evidence whose truth depends on the realised
system or execution environment, including PostgreSQL durability/restart/commit-acknowledgement,
process/namespace/isolation boundaries and clean package/install behaviour where those propositions
are not required to decide the bounded VI-11 contract.

Record unavailable axes as `UNPROVED` or `BLOCKED` exactly as observed and route them to VI-14/VI-15.
**Never convert unavailable real-boundary evidence into PASS, but do not make its mere unavailability
a VI-11 failure when the current bounded contract does not depend on it.**

## Treatment of T013-F001 and T013-F002

Re-examine `T013-F001` and `T013-F002` against the exact VI-10R11 candidate. Confirm what the
successor proof actually establishes and identify any concrete false-positive path you can
demonstrate.

The broad challenge prompts in Reviewer 020 — including arbitrary normalised multi-table/update/
delete representations and any parent-reachable object that might recover a concrete adapter — are
no longer automatic pre-implementation blocking requirements. If a newly imagined escape is not a
bounded-contract defect, classify it under `IMPLEMENTATION_COUPLED_ADVERSARIAL_PROOF` and preserve
it for VI-13R rather than creating an automatic VI-10R12 loop.

A demonstrated escape that **does** allow material violation of an accepted semantic proposition
while satisfying the current bounded contract remains a valid VI-11 blocker.

## Environment and execution control

Perform the bounded environment preflight required by root `EXEC_PLAN.md` section 6.4B. Establish
only the capabilities needed for the current review and report exact unavailable axes.

For Tester Iteration 014:

- verify repository/transport identity and the exact target Git objects;
- inspect the physical proof diff and complete affected proof file;
- run focused tests/canaries that materially bear on the bounded VI-11 question and on the claimed
  repair of `T013-F001` / `T013-F002` where the environment supports them;
- run repository-mandated lightweight structural/type/lint checks only where they bear on the
  proposition being reviewed and are available under the repository-configured runtime;
- do **not** rebuild infrastructure repeatedly merely to reproduce an environment-heavy axis;
- do **not** require execution of the entire 453-test product corpus solely because it exists;
- do **not** require every PostgreSQL/namespace/process/isolation adversarial case to close before
  VI-12R unless you establish that the bounded pre-implementation contract itself depends on that
  specific proposition.

Existing tests are not deleted, weakened, skipped, renamed or relabelled by this directive. This
is an execution/routing control, not a test-removal authority.

## Verdict law

Return exactly one VI-11 verdict:

- `PASS` — no unresolved `PRE_IMPLEMENTATION_CONTRACT_PROOF` blocker remains. Separately recorded
  implementation-coupled findings and milestone `UNPROVED` axes may coexist with this bounded VI-11
  PASS and retain their required later closure.
- `FAIL / RETURN_TO_WORKER` — at least one concrete unresolved `PRE_IMPLEMENTATION_CONTRACT_PROOF`
  blocker remains. State the exact accepted proposition defeated and the concrete false-positive or
  evidence defect. Do not open VI-10R12 merely for a hypothetical implementation-specific escape.
- `BLOCKED` — evidence necessary to decide the bounded VI-11 question itself cannot be obtained in
  the current environment. State why the missing evidence is necessary to this leaf rather than a
  later implementation-coupled or milestone proof class.

Tester independence is unchanged. This directive narrows the proposition being decided; it does not
instruct the tester to return PASS.

## Required response

The Tester Iteration 014 response must record:

1. supplied archive/transport identity and verified Git identities;
2. environment preflight and exact unavailable axes;
3. exact material inspected and focused commands actually run;
4. separate disposition of `T013-F001` and `T013-F002`;
5. every new material finding with one of the three proof classes above;
6. for every blocking finding, the exact accepted semantic proposition or governing invariant it
   defeats;
7. every `UNPROVED` milestone axis preserved without overclaim;
8. final `PASS`, `FAIL / RETURN_TO_WORKER`, or `BLOCKED` for the **bounded VI-11 contract**;
9. explicit routing of non-blocking findings to VI-13R, VI-14 or VI-15 as applicable.

If VI-11 returns `PASS`, the next lawful programme step is VI-12R. That transition does not erase
or accept any separately recorded implementation-coupled or milestone finding.
