# NVDA V2 — Findings and Results of Gate 1

**Purpose:** This is the single entry point for the cumulative Gate 1 investigation. The full investigation is in the six linked, tracked documents below; this page is navigation and status only, not a replacement for their primary evidence or a second governing plan.

**Controlling plan (frozen):** [`EXEC_PLAN.md`](EXEC_PLAN.md), Revision 4, originally committed on audited local `main` at `3e71054c9a2bb162ffefdbe262f8a14a096a24fb`. Its Git blob is `9bf00d95de5800c42502becac60ea3488f5cf789`; the plan has not been changed by the Gate 1 investigation or this consolidation.

**Assessment/acceptance boundary:** All G1.1–G1.6 investigations have been recorded and marked `READY_FOR_DECISION` in their respective findings documents. This does **not** mean Gate 1 has been formally accepted. The programme-owner Gate 1 exit decision is outstanding, and Gate 2 is **not open**. The frozen plan's opening `NOT_STARTED` execution status is a historical snapshot from before assessment; the current status lives in these separate findings records under the programme owner's explicit freeze instruction. Do not use that static line to overwrite subsequent investigation evidence or infer gate acceptance.

## Leaf-by-leaf findings

| Exact ExecPlan leaf | Canonical findings document | What the investigation addresses |
|---|---|---|
| **G1.1 — Verify the baseline and lifecycle identities** | [Findings and Results of Gate 1.1](handoff/workbook_v2/gates_01_02/FINDINGS_AND_RESULTS_OF_GATE_1_1.md) | Current Git/archive baseline; registered, reserved and retired module identity; original-reference archive-byte uncertainty |
| **G1.2 — Establish governing authority and effective amendments** | [Original G1.2 finding](handoff/workbook_v2/gates_01_02/FINDINGS_AND_RESULTS_OF_GATE_1_2.md) **+ [effective-authority R1 correction](handoff/workbook_v2/gates_01_02/GATE_1_REVIEW_SUPPLEMENT_20261015.md)** | Effective calculation authority and amendments; exact scope of prior G01/R01/R02 reviews. Read the correction as authoritative for the incorporated F4 approval. |
| **G1.3 — Establish original/V2 design provenance and its status** | [Findings and Results of Gate 1.3](handoff/workbook_v2/gates_01_02/FINDINGS_AND_RESULTS_OF_GATE_1_3.md) | Original and Pass08 workbooks; accepted mathematics versus historical workbook proposals |
| **G1.4 — Establish the real responsibility mismatch** | [Findings and Results of Gate 1.4](handoff/workbook_v2/gates_01_02/FINDINGS_AND_RESULTS_OF_GATE_1_4.md) | Why original M01 cannot simply be renamed M02; independence and state/interface boundaries |
| **G1.5 — Design the lawful identity and retirement crosswalk, without allocating anything** | [Findings and Results of Gate 1.5](handoff/workbook_v2/gates_01_02/FINDINGS_AND_RESULTS_OF_GATE_1_5.md) | Two-era module labels, 30 historical groups, lawful allocation conditions and M01 migration/retirement dependencies |
| **G1.6 — Resolve transition authority and disposition every outstanding active obligation** | [Findings and Results of Gate 1.6](handoff/workbook_v2/gates_01_02/FINDINGS_AND_RESULTS_OF_GATE_1_6.md) | Obligation-by-obligation transition ledger, accepted/reusable work, unclosed obligations and required future decisions |

## How this repository is organised

- `EXEC_PLAN.md` — the **unchanged governing plan** (Gate 1 and Gate 2 requirements, criteria and exit protocol).
- `FINDINGS_AND_RESULTS_OF_GATE_1.md` — **this navigation index**, in the repository root.
- `handoff/workbook_v2/gates_01_02/FINDINGS_AND_RESULTS_OF_GATE_1_1.md` through `..._1_6.md` — **the complete cumulative findings**. Every document is a committed repository file, not an external download or an untracked attachment.
- `handoff/workbook_v2/decisions/`, `handoff/m01_completion/authority/`, `config/architecture/` and the repository Git history — the applicable **primary sources** cited by those findings; a description in this index does not replace source inspection.

## Practical follow-on

**R1 supplementary correction — 15 October 2026:** [Gate 1 review supplement](handoff/workbook_v2/gates_01_02/GATE_1_REVIEW_SUPPLEMENT_20261015.md) records the effective F4 authority correction to G1.2. **Read G1.2 together with that supplement:** its assertion that the D178 economics remain unapproved and its D178 “open authority” language are superseded by the incorporated 13 October owner approval. The original six leaf documents remain unchanged as historical submissions. **R2 / G1.6 latest-obligation reconciliation remains outstanding; Gate 1 is not accepted and Gate 2 is not open.**

**Original review disposition — 15 October 2026:** [Gate 1 review addendum](handoff/workbook_v2/gates_01_02/GATE_1_REVIEW_ADDENDUM_20261015.md) recommends **RETURN** for bounded G1.2 authority correction and G1.6 latest-F4 obligation reconciliation. The original leaf submissions remain unchanged as evidence; their READY_FOR_DECISION labels do not override this review. Gate 1 is not accepted and Gate 2 remains NOT_OPEN.

After resolving the remaining R2 findings, perform the Gate 1 cumulative exit assessment against the six historical findings, R1/R2 supplement and frozen ExecPlan's mandatory exit claims. Preserve unresolved evidence gaps and owner decisions explicitly; neither this consolidation nor a Git commit authorises Gate 2, creates M02/M03+, completes M01 or retires any module.

**Consolidation change boundary:** This index and moving the local `main` pointer to a descendant containing the six existing findings are documentation/navigation changes only. All inherited history and investigation records remain available. The frozen ExecPlan, guardrails, agents, domain source, workbooks, architecture registries, runtime, tests and application code are unchanged.
