# Atlas Architecture Control-Integration Validation Receipt

Date: 2026-07-25
Unit: `CTRL-ARCH-001`
Branch: `control/accept-module-architecture`
Baseline: `main` at `0c207f9b71868f82d2abdca6c9091556b5a214c5`
Original status: **PASS — control integration accepted on branch on 2026-07-25**

Current status: **see 2026-07-30 current-path revalidation below**

## Source controls

| Source | SHA-256 | Result |
|---|---|---|
| `Atlas_Architecture_Planning_Package_20260720.tar.gz` | `1cc0ce57d67a2dc4100ebb62e32730628df0f2d5edd3299c1fd23c0c566b3e79` | PASS — supplied package checksum evidence retained |
| Original uploaded `Atlas_Architecture_Traceability.xlsx` | `1120c7ef006c1e6f8cf29718524f78bdf9118c72ac0a19e3d24f1b909053e37b` | PASS — original source preserved by hash |
| Original Project Manager brief | `43be514d3633651df5d404ee68e9741a879d4a4a6cf0da6dcbe2f40589f68bc8` | PASS — source hash retained; repository copy adds a supersession banner and normalises Markdown trailing whitespace only |
| Baseline repository archive | `860a8dee5f557d6eac4f0b8638ea87d6f56ea7ae72f6b16e9e2a8fa5870acde7` | PASS — baseline branch/commit verified before mutation |

Original and integrated artefact hashes are recorded in `SOURCE_SHA256SUMS.txt`.

## Accepted control decisions

- the four-map vocabulary is behavioural spine, 18 architecture surfaces, 16 Ownership Modules and implementation obligations;
- `M00`–`M15` are accepted target ownership modules;
- `M07` is `coefficient_modifier_authority`, not general `policy_authority`;
- runtime/contract, state/transaction, governance/promotion and build/test relationships are separate dependency planes;
- accepted dependency arrows run provider/prerequisite → consumer/dependent; historical D-unit rows retain their original convention as historical planning evidence only;
- physical `Mxx` package migration is progressive;
- all 33 `D-xxx` records remain traceability obligations rather than a fixed execution order;
- mandatory positive implementation obligations are explicit for `M07`, `M09`, `M10` and `M11`;
- Gate C is module-local, with final global reconciliation retained;
- `M13 state_kernel` is the first planned code module after this control integration is accepted on `main` and its local proof gate passes;
- seven durable control terms are admitted in the human vocabulary registry and projected through the unchanged deterministic builder.

## Structural validation

| Check | Expected | Actual | Result |
|---|---:|---:|---|
| Atlas cohorts | 287 | 287 | PASS |
| Atlas records | 1,716 | 1,716 | PASS |
| Architecture surfaces | 18 | 18 | PASS |
| Ownership modules | 16 | 16 | PASS |
| Historical `D-xxx` records | 33 | 33 | PASS |
| `D-xxx` records with accepted module routes | 33 | 33 | PASS |
| Mandatory positive module obligations | 4 | 4 | PASS |
| Accepted module-sequence entries | 14 | 14 | PASS |
| Runtime/contract graph acyclic | true | true — 13/13 domain nodes visited | PASS |
| Governance edges separated from runtime | true | true | PASS |
| State/transaction participation separated | true | true | PASS |
| `M08 → M07` runtime dependency absent | true | true | PASS |
| `M07` accepted name | `coefficient_modifier_authority` | `coefficient_modifier_authority` | PASS |
| Workbook formula-error scan | zero | zero | PASS |
| Workbook ZIP integrity | valid | valid | PASS |
| Continuous `M14/M15` governance represented | true | true | PASS |
| Final global reconciliation represented | true | true | PASS |

## Vocabulary projection validation

- human registry version: `2026-07-25-module-architecture-v1`;
- accepted registry records: 124 total, including seven new control records;
- canonical JSON SHA-256 before builder run: `cc96fc074a407f8dfeb74cbb018595eecd37e5735e67964dc00a9a927ea23b71`;
- canonical JSON SHA-256 after builder run: `cc96fc074a407f8dfeb74cbb018595eecd37e5735e67964dc00a9a927ea23b71`;
- `build_canonical_payload()` exactly equals the committed JSON;
- no builder source, candidate report or vocabulary stamp changed.

## Repository-boundary validation

The changed-path validator reported 32 PASS checks and zero failures. Mutations are confined to the expressly opened control, routed working-authority, vocabulary projection and architecture-evidence surfaces.

No changed path exists under:

- `src/`;
- `tests/`;
- `config/`.

No package migration or module implementation occurred. `git diff --check` passed.

Behavioural tests were not used to claim runtime correctness because this unit changes no production behaviour. The deterministic vocabulary projection and architecture/control validators are the applicable proof surfaces.

## External Git checkpoint evidence

| Check | Result |
|---|---|
| Integration commit | PASS — `9ec838a45bd4cf98313e83f73f47d376b1e42806` on `control/accept-module-architecture` |
| Integration archive | PASS — `NVDA_MODULE_ARCHITECTURE_CONTROL_INTEGRATION_9ec838a_20260725.tar.gz` |
| Archive SHA-256 | `faa6d2e196923bcd1641b1616c2fb8bfb3cf0900e4972642b79e2943333d5d5b` |
| Archive size | `25193160` bytes |
| Archive integrity | PASS — `gzip -t` |
| Fresh extraction branch | PASS — `control/accept-module-architecture` |
| Fresh extraction commit | PASS — `9ec838a45bd4cf98313e83f73f47d376b1e42806` |
| Fresh extraction worktree | PASS — clean |

## Vocabulary Tier A differential

The branch and baseline were both run with:

```text
PYTHONPATH=src python -m pytest -q tests/tier_a/vocabulary
```

| Worktree | Result |
|---|---|
| Control branch | 18 failed, 83 passed |
| Detached baseline `0c207f9b7186` | 18 failed, 83 passed |
| Failed node comparison | identical 18 node IDs |

This is a **no-new-failure differential**, not a green-suite claim. The eighteen vocabulary failures pre-exist this control branch and remain open.

## Claim boundary

This receipt does not claim:

- that any target module is implemented;
- that every Atlas cohort or record was semantically re-adjudicated during this branch;
- that all 179 physical tests have current authority dispositions;
- production durability, availability, capacity, deployment, paper-trading or live-trading readiness;
- that passing legacy tests establish product meaning;
- that the branch has been merged or pushed.

The 287 cohort rows and 1,716 record rows are retained as traceability evidence. Their behavioural propositions remain subject to normative and proof admission when the owning module opens.

## Current-path revalidation — 2026-07-30

Unit: `ATLAS-CURRENT-PATH-REBASE-AND-GATE-C-CONTINUATION-V1`

Source: `integration/parallel-cycle-01` at `73f1e7ab3ce212c9951f03c407e94741e6c68913`

Repair branch: `control/atlas-current-path-rebase-gate-c-continuation-v1`

Disposition: **PASS — current/governing paths repaired and Gate C control continuation reconciled**

### Recovery decision

| Search surface | Result |
|---|---|
| All 248 repository commits and named objects | neither stale filename present |
| Unreachable Git objects | neither stale filename present |
| Supplied full-history and planning archives | neither stale filename present |
| Connected GitHub repository, all eight branches | both paths returned not found on every branch |

The two filenames were therefore stale Atlas labels, not recoverable governing documents. The operating-behaviour label was rebased to the current operating-model core. The obsolete composite process/test/review label was removed because every affected row already routes to the current review/replay authority and the rows requiring testing authority already route to the testing core.

### Projection repair

| Check | Before | After | Result |
|---|---:|---:|---|
| Old operating-document occurrences, workbook | 105 | 0 | PASS |
| Old composite-document occurrences, workbook | 70 | 0 | PASS |
| Old operating-document occurrences, JSON | 105 | 0 | PASS |
| Old composite-document occurrences, JSON | 70 | 0 | PASS |
| Affected cohort rows | 159 | 159 repaired | PASS |
| Affected surface rows | 3 | 3 repaired | PASS |
| Cohorts | 287 | 287 | PASS |
| Records | 1,716 | 1,716 | PASS |
| Surfaces | 18 | 18 | PASS |

No cohort membership, record lineage, ownership module, disposition or architecture treatment changed.

### Embedded current/governing-path validator

Run from the repository root with the primary Python runtime. The validator is retained here rather than in another project-control file.

```python
from __future__ import annotations

import json
from pathlib import Path

from openpyxl import load_workbook


ROOT = Path.cwd()
ARCH = ROOT / "project_control/canonical_project_manager/architecture"
XLSX = ARCH / "Atlas_Architecture_Traceability.xlsx"
JSON_PATH = ARCH / "Atlas_Architecture_Machine_Readable.json"
STALE = {
    "docs/02_BRIEFING_AND_BEHAVIOURAL_ARCHITECTURE_CORE.md",
    "docs/06_PROCESS_TEST_REVIEW_AND_LEARNING_CORE.md",
}


def docs(value: object) -> tuple[str, ...]:
    if value is None:
        return ()
    return tuple(part.strip() for part in str(value).split(";") if part.strip())


projection = json.loads(JSON_PATH.read_text(encoding="utf-8"))
workbook = load_workbook(XLSX, read_only=True, data_only=False)
surface_sheet = workbook["Surface Map"]
cohort_sheet = workbook["Cohort Trace"]
surface_headers = {cell.value: cell.column for cell in next(surface_sheet.iter_rows())}
cohort_headers = {cell.value: cell.column for cell in next(cohort_sheet.iter_rows())}

workbook_surfaces = {
    str(row[surface_headers["Surface Id"] - 1].value): docs(
        row[surface_headers["Governing Docs"] - 1].value
    )
    for row in surface_sheet.iter_rows(min_row=2)
    if row[surface_headers["Surface Id"] - 1].value is not None
}
workbook_cohorts = {
    str(row[cohort_headers["Cohort Id"] - 1].value): docs(
        row[cohort_headers["Current Governing Docs"] - 1].value
    )
    for row in cohort_sheet.iter_rows(min_row=2)
    if row[cohort_headers["Cohort Id"] - 1].value is not None
}
json_surfaces = {
    str(item["surface_id"]): docs(item["governing_docs"])
    for item in projection["surfaces"]
}
json_cohorts = {
    str(item["cohort_id"]): docs(item["current_governing_docs"])
    for item in projection["cohorts"]
}

assert workbook_surfaces == json_surfaces
assert workbook_cohorts == json_cohorts
assert len(workbook_surfaces) == 18
assert len(workbook_cohorts) == 287
assert len(projection["records"]) == 1716

all_doc_refs = [
    item
    for mapping in (
        workbook_surfaces,
        workbook_cohorts,
        json_surfaces,
        json_cohorts,
    )
    for values in mapping.values()
    for item in values
]
assert not {item for item in all_doc_refs if not (ROOT / item).is_file()}
assert not (STALE & set(all_doc_refs))

stale_workbook_cells = []
for sheet in workbook.worksheets:
    for row in sheet.iter_rows():
        for cell in row:
            if isinstance(cell.value, str) and any(
                stale in cell.value for stale in STALE
            ):
                stale_workbook_cells.append(f"{sheet.title}!{cell.coordinate}")
assert not stale_workbook_cells
json_text = JSON_PATH.read_text(encoding="utf-8")
assert not any(stale in json_text for stale in STALE)

print("PASS current/governing path resolution")
print(f"PASS workbook/JSON surface parity: {len(workbook_surfaces)}")
print(f"PASS workbook/JSON cohort parity: {len(workbook_cohorts)}")
print(f"PASS record count preserved: {len(projection['records'])}")
print(f"PASS unique existing governing documents: {len(set(all_doc_refs))}")
print(f"PASS governing-document references checked: {len(all_doc_refs)}")
print("PASS stale path occurrences: 0")
```

Recorded output:

```text
PASS current/governing path resolution
PASS workbook/JSON surface parity: 18
PASS workbook/JSON cohort parity: 287
PASS record count preserved: 1716
PASS unique existing governing documents: 20
PASS governing-document references checked: 3340
PASS stale path occurrences: 0
```

Workbook ZIP integrity passed. All 19 worksheets were rendered after mutation; the original table styling, headers, widths and visible content structure remain intact. `git diff --check` passed.

The integrated-hash check also exposed two pre-existing stale entries in `SOURCE_SHA256SUMS.txt` for the unchanged vocabulary registry and generated vocabulary JSON. Those two checksum lines were corrected to the current repository bytes; neither vocabulary artefact was mutated.

### Current claim boundary

This repair changes locators only. It does not admit an Atlas behavioural proposition, change numbered normative meaning, open a physical test, authorise production implementation, or claim Gate C completion. The next lawful leaf is the bounded M04 K07 numbered normative proposition identified in the reconciled ExecPlan and Gate C protocol.
