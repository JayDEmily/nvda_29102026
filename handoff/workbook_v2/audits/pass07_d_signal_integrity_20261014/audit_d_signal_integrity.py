#!/usr/bin/env python3
"""Read-only, standard-library OOXML audit of all D001-D209: V1 vs V2 Pass06.

No workbook edits; no acceptance or mathematical correctness is asserted.
Exit nonzero when any conservation, identity, name or allocation check fails.
"""
from __future__ import annotations
import collections
import hashlib
import json
import re
from pathlib import Path
from xml.etree import ElementTree as ET
from zipfile import ZipFile

REPO = Path(__file__).resolve().parents[4]
V1 = REPO / "implementation/authority/source_signal_catalogue/NVDA_80_STEP_ACADEMIC_EVIDENCE_AUDIT_WITH_SIGNALS_ADDENDUM_81_94.xlsx"
V2 = REPO / "handoff/workbook_v2/NVDA_SIGNALS_RESEARCH_WORKBOOK_V2_PASS06.xlsx"
OUT = Path(__file__).with_name("NVDA_V1_V2_D001_D209_INTEGRITY_AUDIT_20261014.md")
JSON = Path(__file__).with_name("PASS07_READBACK.json")
X = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
EXPECTED = {f"D{i:03d}" for i in range(1, 210)}

def digest(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()

def workbook_names(zipfile):
    root = ET.fromstring(zipfile.read("xl/workbook.xml"))
    return [x.get("name") for x in root.find(X+"sheets")]

def cells(zipfile, name):
    names = workbook_names(zipfile)
    if name not in names:
        raise ValueError(f"Missing worksheet: {name}")
    idx = names.index(name) + 1
    root = ET.fromstring(zipfile.read(f"xl/worksheets/sheet{idx}.xml"))
    strs = []
    if "xl/sharedStrings.xml" in zipfile.namelist():
        strings = ET.fromstring(zipfile.read("xl/sharedStrings.xml"))
        strs = ["".join((t.text or "") for t in si.iter(X+"t")) for si in strings.findall(X+"si")]
    output = {}
    for cell in root.findall(f".//{X}sheetData/{X}row/{X}c"):
        value, inline, formula = cell.find(X+"v"), cell.find(X+"is"), cell.find(X+"f")
        if value is not None:
            result = strs[int(value.text)] if cell.get("t") == "s" else value.text
        elif inline is not None:
            result = "".join(t.text or "" for t in inline.iter(X+"t"))
        elif formula is not None:
            result = "=" + (formula.text or "")
        else:
            continue
        output[cell.get("r")] = result
    return output

def listed(cells_dict, start, col_id="A", name_col="B", mod=None, mod_col=None):
    found = []
    for row in range(start, 400):
        val = cells_dict.get(f"{col_id}{row}")
        if re.fullmatch(r"D\d{3}", val or ""):
            found.append((val,cells_dict.get(f"{name_col}{row}", ""),mod if mod_col is None else cells_dict.get(f"{mod_col}{row}"),row))
    return found

def main():
    with ZipFile(V1) as z1, ZipFile(V2) as z2:
        source = cells(z1,"Derived Signals")
        retained = cells(z2,"Derived Signals")
        foundation = listed(cells(z2,"M01-1 Derived Raw"),6,mod="M01-1")
        allocation = listed(cells(z2,"M02-M31 Signal Allocation"),5,mod_col="C")
        actual_modules = []
        for n in range(2,32):
            mod=f"M{n:02d}"
            actual_modules.extend(listed(cells(z2,mod),5,mod=mod))
    v1 = listed(source,5,name_col="C")
    v2 = listed(retained,5,name_col="C")
    s_c=collections.Counter(row[0] for row in v1)
    retained_c=collections.Counter(row[0] for row in v2)
    foundation_c=collections.Counter(row[0] for row in foundation)
    allocation_c=collections.Counter(row[0] for row in allocation)
    module_c=collections.Counter(row[0] for row in actual_modules)
    assigned_c=foundation_c+module_c
    source_names={row[0]:row[1] for row in v1}
    retained_lookup={r[0]:r for r in v2}
    assignment_lookup={r[0]:r for r in foundation + actual_modules}
    allocation_lookup={r[0]:r for r in allocation}
    problems=[]
    if set(s_c)!=EXPECTED or any(n!=1 for n in s_c.values()):problems.append("V1 D-ID range/uniqueness differs from D001-D209")
    if source!=retained:problems.append("V1 and retained V2 Derived Signals worksheet cell values/formulas differ")
    if set(retained_c)!=set(s_c) or any(n!=1 for n in retained_c.values()):problems.append("Retained V2 identifiers differ or duplicate")
    if len(foundation)!=114 or len(actual_modules)!=95 or len(allocation)!=95:
        problems.append("M01-1/module/allocation row counts differ from recorded 114/95/95")
    if set(assigned_c)!=set(s_c) or any(n!=1 for n in assigned_c.values()):
        problems.append("Module allocation incomplete, extra or duplicated")
    if set(allocation_c)!=set(module_c) or any(n!=1 for n in allocation_c.values()):
        problems.append("M02-M31 allocation index differs from individual module sheets")
    output_rows=[]
    for did in sorted(EXPECTED):
        v1_name=source_names.get(did,"")
        v2_row=retained_lookup.get(did)
        dest=assignment_lookup.get(did)
        index=allocation_lookup.get(did)
        verified=(
            s_c[did]==1 and retained_c[did]==1 and
            assigned_c[did]==1 and
            v2_row is not None and dest is not None and
            v1_name==v2_row[1]==dest[1] and
            ((dest[2]=="M01-1" and allocation_c[did]==0) or
             (dest[2]!="M01-1" and allocation_c[did]==1 and index is not None and
              dest[2]==index[2] and v1_name==index[1]))
        )
        status="PASS" if verified else "FAIL"
        if not verified:problems.append(f"{did} row integrity mismatch")
        module = dest[2] if dest else "MISSING"
        sheet_row=(f"`{module}!A{dest[3]}`" if dest else "MISSING")
        output_rows.append((did,v1_name, "YES" if s_c[did]==1 else "NO",
               "YES" if retained_c[did]==1 and v2_row[1]==v1_name else "NO",
               module,sheet_row,assigned_c[did],status))
    # Catch any extra D-ID even when all D001-D209 rows pass.
    extra=sorted((set(s_c)|set(retained_c)|set(assigned_c)|set(allocation_c))-EXPECTED)
    if extra:problems.append("Extra IDs: "+", ".join(extra))
    status="PASS" if not problems else "FAIL"
    sha1,sha2=digest(V1),digest(V2)
    lines=[
        "# NVDA — D001–D209 original-to-V2 preservation and allocation audit",
        "",
        f"**Result: {status}** — {len(output_rows)} original signal designations checked against their preserved V2 source and proposed module allocation.",
        "",
        "## Scope and authority",
        "",
        "- Audit compares the **original V1 Excel `Derived Signals` tab** with the **Pass 06 V2 Excel `Derived Signals` tab** and its M01-1/M02–M31 allocation worksheets.",
        "- The V1 workbook is the original research catalogue; the M01 implementation's normative CSV remains its own authority. This check does not establish mathematical/test correctness or approve new architecture.",
        "- Every row is checked for exact D-ID, source name, original-tab retention, exactly-one proposed-module allocation, and matching names/module index. All populated values and formula text of the original `Derived Signals` sheet are compared against its retained V2 copy.",
        "",
        "## Inspected artefacts",
        "",
        f"- V1: `{V1.relative_to(REPO)}` (SHA-256 `{sha1}`)",
        f"- V2: `{V2.relative_to(REPO)}` (SHA-256 `{sha2}`)",
        "- Proposed module allocations remain review designations; M01-1 and M02–M31 have not been admitted as production module identities.",
        "",
        "## Reconciliation",
        "",
        "| Measure | Observed |",
        "|---|---:|",
        f"| Unique V1 D-identifiers | {len(s_c)} |",
        f"| Unique retained V2 D-identifiers | {len(retained_c)} |",
        f"| M01-1 worksheet entries | {len(foundation)} |",
        f"| M02–M31 worksheet entries | {len(actual_modules)} |",
        f"| M02–M31 allocation-index entries | {len(allocation)} |",
        f"| Missing module assignments | {len(set(s_c)-set(assigned_c))} |",
        f"| Extra module assignments | {len(set(assigned_c)-set(s_c))} |",
        f"| Multiply allocated D-identifiers | {sum(n!=1 for n in assigned_c.values())} |",
        f"| V1-to-V2 original sheet cell-content match | {'YES' if source==retained else 'NO'} |",
        f"| Individually passing D rows | {sum(r[-1]=='PASS' for r in output_rows)} / {len(output_rows)} |",
        "",
        "## Complete row-by-row audit",
        "",
        "`V1` confirms presence in the first workbook. `V2 retained` confirms the same ID/name remains in its preserved source worksheet. `Module` and `Module location` identify the proposed allocation (not a new canonical D-ID).",
        "",
        "| D-ID | Original V1 signal name | V1 present | V2 retained | Proposed module | Module location | Allocation count | Result |",
        "|---|---|---|---|---|---|---:|---|",
    ]
    for did,name,v1y,v2y,mod,where,count,result in output_rows:
        lines.append(f"| {did} | {name.replace('|',r'\|')} | {v1y} | {v2y} | {mod} | {where} | {count} | {result} |")
    lines.extend(["","## Discrepancies", ""])
    if problems:
        lines.extend(f"- {x}" for x in problems)
    else:
        lines.append("None detected by the stated preservation and allocation checks.")
    lines.extend(["",
        "## Limitations",
        "",
        "- This proves identifier, name, retained-source-cell and proposed module placement consistency only.",
        "- It does **not** prove independently correct equations, runtime behaviour, module boundaries, or individual test coverage.",
        "- A proposed module may need future dependency migration or private code duplication; neither is implemented by this audit.",
        "",
        "## Reproduction",
        "",
        "From the repository root:",
        "",
        "```sh",
        "python handoff/workbook_v2/audits/pass07_d_signal_integrity_20261014/audit_d_signal_integrity.py",
        "```",
        "",
    ])
    OUT.write_text("\n".join(lines),encoding="utf-8")
    summary={"status":status,"V1_sha256":sha1,"V2_sha256":sha2,
             "v1_unique":len(s_c),"v2_unique":len(retained_c),
             "m01_1_rows":len(foundation),"m02_m31_rows":len(actual_modules),
             "m02_m31_index_rows":len(allocation),
             "row_pass":sum(r[-1]=="PASS" for r in output_rows),
             "row_fail":sum(r[-1]!="PASS" for r in output_rows),
             "original_derived_sheet_value_formula_match":source==retained,
             "missing":sorted(set(s_c)-set(assigned_c)),
             "extra":sorted(set(assigned_c)-set(s_c)),"problems":problems}
    JSON.write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(summary,indent=2))
    if problems:raise SystemExit(1)

if __name__=="__main__":
    main()
