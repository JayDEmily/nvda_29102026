"""Pass 01: add only 00_Guardrails & Method to a V2 copy of the hash-bound V1 workbook.

The seven original worksheets are imported as-is and are not targeted for writes.
Run from the repository root: python handoff/workbook_v2/pass01_build.py
"""
from pathlib import Path
import hashlib
from artifact_tool import Blob, SpreadsheetFile

ROOT=Path(__file__).resolve().parents[2]
NAME='NVDA_80_STEP_ACADEMIC_EVIDENCE_AUDIT_WITH_SIGNALS_ADDENDUM_81_94.xlsx'
SOURCE=ROOT/'handoff/m01_completion/authority'/NAME
OUTPUT=ROOT/'handoff/workbook_v2/NVDA_SIGNALS_RESEARCH_WORKBOOK_V2_PASS01.xlsx'
SHA='519ea9449297d564ae4a02afc1bf4e60e4471631c81a0842620f9fb60bb4f9ae'
assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==SHA, 'V1 workbook digest mismatch: refuse output'

# Each mandatory rule cites the workbook cells inspected. The accepted M01 brief,
# normative CSV and root governance retain their separate authority jurisdictions.
sections=[
 ('A. JURISDICTION, SCOPE AND SOURCE FIDELITY',[
 ('G-001','01 / 02','This pass creates only this guardrails worksheet. The future 01_Raw Signals and 02_Derived Signal Index are NOT created, populated, renamed or reordered in Pass 01.','Current programme-owner direction; V1 Raw Signals; V1 Derived Signals','V2 has precisely the original seven worksheet names plus this one; other original sheets retain their values and structure.'),
 ('G-002','01 / 02','Treat Version 1 as immutable reference evidence. Preserve each exact Rxxx and Dxxx identity, every original cell, notes, blanks and the academic audit. Never replace Version 1.','V1 SHA-256 519ea9449297d564ae4a02afc1bf4e60e4471631c81a0842620f9fb60bb4f9ae; Raw Signals!A5:Y327; Derived Signals!A5:O213','Before future worksheet transformations, compare every source cell against V1 and record intentional differences.'),
 ('G-003','01 / 02','This worksheet governs the proposed V2 research reorganisation only. It does not amend GUARDRAILS.md, AGENTS.md, EXEC_PLAN.md, M00, M01, the accepted brief, normative catalogue or production code.','GUARDRAILS.md; EXEC_PLAN.md §§1-4; handoff/m01_completion/AUTHORITY_INDEX.md','Any changed semantic dependency, calculation meaning or software owner requires separate applicable programme authority.'),
 ('G-004','01 / 02','Record provenance per transferred row as original workbook identity, original worksheet, source Excel row number and original R/D identifier. Do not infer an ID from the position after sorting.','Raw Signals!A5:A327; Derived Signals!A5:A213','Carry a source locator for each future index row; compare against source-row readback manifest.'),
 ('G-005','01 / 02','Preserve source text exactly: provider identifiers, descriptive labels, punctuation, units, time semantics, source URLs, blanks, N/A, TBD and uncertainty labels. Never fill an empty cell by inference.','Raw Signals!A4:Y327; Derived Signals!A4:O213','Field-for-field comparison required; any editorial normalisation lives in separately marked proposed fields.'),
 ('G-006','01 / 02','Keep the original workbook\'s citation/research links and framework-step references distinct from API source documentation. Research support is not implementation proof or observed profitability.','Raw Signals!U4:X327; Derived Signals!L4:M213; Method & Legend!A1:B16','Do not infer successful implementation or validated alpha from a paper citation, a source label or a framework step.'),
 ]),
 ('B. FUTURE 01_RAW SIGNALS — ROW AND SOURCE CONTRACT',[
 ('R-001','01','The source row set is exactly R001–R323, one of each, in V1 rows 5–327. Preserve all 25 original columns A:Y, including partially populated columns.','Raw Signals!A4:Y327','323 unique IDs; zero omissions, duplicates or unsolicited renumberings; 7,517 populated source cells including title/note/header.'),
 ('R-002','01','Retain the original raw column roles: identity/family/description/scope (A:D); provider/product/native extraction (E:K); unit/cadence/access (L:O); time semantics (P:S); revision/steps/downstream/status/URL/notes (T:Y).','Raw Signals!A4:Y4','Map all 25 headers explicitly before any future rearrangement; do not collapse native identifier, native field or tick/series ID.'),
 ('R-003','01','Preserve E:Provider and F:Provider product/API separately, and preserve G:Native endpoint/callback, H:Native identifier, I:Native field, J:Tick/series ID and K:Source variant as separately named source evidence.','Raw Signals!E4:K327','No guessed replacement provider, endpoint, subscription or field binding; do not treat provider name as sufficient extraction law.'),
 ('R-004','01','Do not assume that every R-signal is a market quote or delivered by API. The original catalogue includes system time/provenance, IBKR account/risk, positions, orders/executions and seven TBD-provider economic-calendar inputs.','Raw Signals!B5:F327; R001–R006; R205–R235; R283–R289','Preserve native family and provider values; distinguish source type using the actual row, not a blanket market-data label.'),
 ('R-005','01','Preserve all 19 raw-family names and assignments exactly. Family is original catalogue organisation; it is not permission to modify M00 or create a software module.','Raw Signals!B5:B327','Each R-ID retains precisely its original family; group by family only after recording complete individual provenance.'),
 ('R-006','01','Preserve provider/data-access status verbatim: 275 Verified; 34 Verified API schema; 7 Verified symbol; live access TBD; 7 TBD provider. These are V1 labels, not proof that live subscriptions or integrations work.','Raw Signals!W5:W327','All 323 statuses retained; do not promote a TBD/verification label into a provider-runtime claim.'),
 ('R-007','01','Preserve original URLs as evidence without inventing missing ones. 312 raw rows contain X:Source URL; 11 lack one (R001–R003, R006, R283–R289).','Raw Signals!X5:X327','Source link absence is recorded as absence; provider verification requires separate evidence.'),
 ('R-008','01','Preserve source timestamp field P, timestamp meaning Q, native timezone R and UTC handling rule S independently. Receipt time, true event instant and date-only period are not interchangeable.','Raw Signals!P4:S327; Raw Signals!A2; R001–R004','No fabricated intraday timestamp from a date-only source; no inferred timezone when unavailable; native timestamp preserved.'),
 ('R-009','01','Preserve the source variant, units, cadence, session availability and access/subscription distinctions without rescaling, changing sampling or asserting currently available data.','Raw Signals!K4:O327','Changing units/temporal meaning/provider product is a separately disclosed proposal, not a formatting edit.'),
 ('R-010','01','Preserve revisions/vintages T and source-status W as separate properties; a published value, revision or market-data type must not be silently conflated with another.','Raw Signals!T4:W327; R005; FRED macro/vintage families','Do not discard historical correction/vintage information or replace delayed/frozen with live labels.'),
 ('R-011','01','Preserve U:Required steps, V:Downstream derived IDs and Y:Notes as source metadata. A blank V is not evidence that no D-signal depends on the R-signal; V is populated for 111 of 323 rows.','Raw Signals!U4:Y327','Do not invent missing links or treat the V1 V column as normative dependency closure.'),
 ('R-012','01','Do not deduplicate R rows by description or provider-field coincidence. Different instruments, source variants, contract identities, periods and timestamps are separately meaningful.','Raw Signals!C4:K327; H4:S327','The R-ID, not a non-unique description or field string, is the source row key.'),
 ]),
 ('C. FUTURE 02_DERIVED SIGNAL INDEX — IDENTITY AND FAMILY CONTRACT',[
 ('D-001','02','The source row set is exactly D001–D209, one of each, in V1 rows 5–213. Preserve all 15 original columns A:O as reference fields in a future traceable index.','Derived Signals!A4:O213','209 unique IDs; zero omissions, duplicates or unsolicited renumberings; 2,637 populated source cells including title/note/header.'),
 ('D-002','02','Retain the original derived columns: ID A; family B; name C; symbolic label D; raw dependencies E; derived dependencies F; calculation concept G; parameter/window H; units I; cadence J; universe K; steps L; purpose M; definition status N; notes O.','Derived Signals!A4:O4','Map all 15 source headers; every future derived row is traceable back to its individual V1 row.'),
 ('D-003','02','Preserve all 34 native family labels and each D-ID assignment exactly in the initial index. Treat family as descriptive grouping, not execution order, mathematics, classification, module identity or ownership admission.','Derived Signals!B5:B213; accepted M01 brief §2','Do not split or renumber families as software modules in Pass 01; future module mapping requires separate evidence and approval.'),
 ('D-004','02','Preserve the original row sequence and source Excel locator even if future index presentation is sorted or grouped. Do not infer dependency order from the visual family order.','Derived Signals!A5:B213; E5:F213','Retain original D-ID, family and source row as independent fields before any grouping.'),
 ('D-005','02','Keep raw and derived dependencies distinct. In V1, 105 D rows declare only R inputs, 35 declare R and D, 66 declare only D; D007, D204 and D205 declare neither.','Derived Signals!E5:F213','Do not fill blanks by assumption; preserve the original dependency text as historical source evidence.'),
 ('D-006','02','The workbook E/F lists are reference evidence, not current normative M01 dependencies. Where current accepted brief/catalogue law differs (for example authorised D134/D135, D116, D175/D189 changes), retain both identities and report divergence; do not silently merge.','Derived Signals!E4:F213; accepted brief §7; handoff/m01_completion/AUTHORITY_INDEX.md','No worksheet reorganisation can supersede the accepted brief/current normative CSV or rewrite historical V1 dependency declarations.'),
 ('D-007','02','Column G is explicitly "Calculation concept (no equation)". Column N "Specified" (206) / "Specified; provider pending" (3) does NOT prove that the source workbook contains a complete equation, executable code or independent tests.','Derived Signals!A2; G4:G213; N4:N213','Never invent equations, coefficient values, provider bindings, tests or implementation status from the concept/definition status.'),
 ('D-008','02','Preserve H:Parameter/window, I:Units, J:Update cadence and K:Applicable universe, including blanks, as four independent specifications. A missing parameter/window is not permission to select a default.','Derived Signals!H4:K213','Report absent or ambiguous requirements as gaps; do not silently shorten windows, change estimators or broaden universe.'),
 ('D-009','02','Preserve required framework steps L, purpose/output M, definition status N and notes O separately. An academic mechanism reference is not a trading strategy choice, equation, test or correctness proof.','Derived Signals!L4:O213; Method & Legend!A1:B16','Research support, equation authority, production implementation and validation remain separately identified.'),
 ('D-010','02','Do not classify a D-signal as a straightforward derived market calculation merely from its Family, concept or presence of R inputs. Classification is a separate per-D decision requiring exact equation, full dependency closure, external-context check and test evidence.','Derived Signals!B4:K213; accepted brief §§5–8','No inherited 122/87 count, strategy split, ownership reassignment or calculation redefinition is authorised by this Pass 01.'),
 ('D-011','02','Preserve notes on D123 (intraday volume not OI change), D125 (dealer sign not directly observed), and D129 (model-dependent) without silently resolving them.','Derived Signals!O127; O129; O133 (locators must be checked against source)','Preserve precise row-located notes; report unresolved assumptions explicitly.'),
 ('D-012','02','The future index must preserve the actual typed source reference for each D-ID. M00 source values and prior D results are different categories; no downstream formula is made true merely by a catalogue R/D ID.','Derived Signals!E4:F213; accepted brief §§7,9','Index records source dependencies, but cannot substitute for typed projection/mapping, mathematical definition, or runtime validation.'),
 ]),
 ('D. VERIFICATION, CHANGE CONTROL AND CURRENT DEFERRED BOUNDARY',[
 ('V-001','01 / 02','A future pass must read every row and every populated/empty source column in both source sheets before deciding to move, rename, normalise or classify a record. Sample-row review is insufficient.','V1 Raw Signals!A4:Y327; Derived Signals!A4:O213','Machine-readable row manifest and source-to-target per-cell readback required; original source retained.'),
 ('V-002','01 / 02','Refuse success if a row disappears, duplicates, changes identity, loses a note/URL, or merges blank with N/A/TBD. Log intentional V2-only additions in separately identified columns with V1 unchanged.','Raw Signals!A5:Y327; Derived Signals!A5:O213','Future strict check: 323 R and 209 D; all original source values recoverable by ID and source row.'),
 ('V-003','02','Independently validate any future R/D relationship or family reorganisation against the actual per-row references. An acyclic workbook reference graph alone does not demonstrate executable or accepted dependency truth.','Derived Signals!E5:F213; accepted brief Appendix B; authority index','No invented cross-reference from a missing dependency; no automatic promotion from research index into M01 catalogue.'),
 ('V-004','01 / 02','This Pass 01 does not create 01_Raw Signals or 02_Derived Signal Index, redistribute families, change source providers, write equations, introduce tests, or change M01 implementation.','Programme-owner Pass 01 instruction','Only new worksheet: 00_Guardrails & Method, within a distinct V2 workbook under handoff/workbook_v2.'),
 ('V-005','01 / 02','Do not claim final V2 governance, full independent calculation proofs, source correctness, API connectivity or academic validation merely from this structural pass. The guardrails here apply only to the two future worksheets.','Root GUARDRAILS.md; Method & Legend!A1:B16; current branch evidence','Pass 01 is a versioned workbook-design checkpoint; later workbook sections and software modules remain deferred.'),
 ])
]

w=SpreadsheetFile.import_xlsx(Blob.load(str(SOURCE)))
before=[w.worksheets.get_item_at(i).name for i in range(7)]
assert before==['Evidence Audit','Source Register','Method & Legend','Summary','Raw Signals','Derived Signals','Addendum Evidence Audit']
s=w.worksheets.add('00_Guardrails & Method')
s.get_range('A1:E1').merge()
s.get_range('A1').values=[['00_Guardrails & Method | Workbook V2 — Pass 01']]
s.get_range('A1:E1').format={'fill':'#122339','font':{'bold':True,'size':17,'color':'#FFFFFF'},'row_height':37,'vertical_alignment':'center'}
s.get_range('A2:E2').merge()
s.get_range('A2').values=[['Governs only future 01_Raw Signals and 02_Derived Signal Index. No other V2 transformation in this pass.']]
s.get_range('A2:E2').format={'fill':'#E8EDF3','font':{'size':11,'color':'#23384F'},'row_height':30,'wrap_text':True}
meta=[
 ['Jurisdiction','Research-workbook V2 design guardrails only; accepted M01 and source workbook remain unchanged'],
 ['Original source',NAME+' | SHA-256 '+SHA],
 ['Source census','Raw Signals R001–R323: 323/323; Derived Signals D001–D209: 209/209; 19 raw and 34 derived families'],
 ['Pass-01 boundary','Only this 00 worksheet created. Future 01 and 02 worksheets deferred. Audit evidence: PASS01_SOURCE_CENSUS.json and PASS01_SOURCE_ROW_DIGESTS.csv'],
]
for i,(label,value) in enumerate(meta, start=4):
 s.get_range(f'A{i}').values=[[label]]
 s.get_range(f'B{i}:E{i}').merge()
 s.get_range(f'B{i}').values=[[value]]
 s.get_range(f'A{i}').format={'fill':'#F0F4F8','font':{'bold':True,'color':'#213547'},'row_height':29,'wrap_text':True,'vertical_alignment':'center'}
 s.get_range(f'B{i}:E{i}').format={'fill':'#F6F8FB','font':{'color':'#26394E','size':10},'wrap_text':True,'vertical_alignment':'center','row_height':29}
s.get_range('A9:E9').values=[['Rule ID','Scope','Mandatory rule (future worksheet design)','Source authority / V1 locator','Required readback / failure condition']]
s.get_range('A9:E9').format={'fill':'#29435F','font':{'bold':True,'color':'#FFFFFF','size':10},'row_height':30,'wrap_text':True,'vertical_alignment':'center'}
r=10
for heading,items in sections:
 s.get_range(f'A{r}:E{r}').merge()
 s.get_range(f'A{r}').values=[[heading]]
 s.get_range(f'A{r}:E{r}').format={'fill':'#DBE6F0','font':{'bold':True,'color':'#16344F','size':11},'row_height':24}
 r+=1
 for record in items:
  s.get_range(f'A{r}:E{r}').values=[list(record)]
  s.get_range(f'A{r}:E{r}').format={'fill':'#FFFFFF' if r%2==0 else '#F6F9FC','wrap_text':True,'vertical_alignment':'top','row_height':68,'font':{'size':10,'color':'#243247'}}
  s.get_range(f'A{r}').format={'font':{'bold':True,'color':'#1E4674'}}
  r+=1
s.get_range('A1:A'+str(r)).format.column_width=14
s.get_range('B1:B'+str(r)).format.column_width=12
s.get_range('C1:C'+str(r)).format.column_width=74
s.get_range('D1:D'+str(r)).format.column_width=62
s.get_range('E1:E'+str(r)).format.column_width=64
s.freeze_panes.freeze_rows(9)
assert [w.worksheets.get_item_at(i).name for i in range(8)][-1]=='00_Guardrails & Method'
print('Created',sum(map(lambda x:len(x[1]),sections)),'rules; last row',r-1)
print('New worksheet spot check:',w.inspect({'kind':'table','range':"'00_Guardrails & Method'!A9:E12",'include':'values','table_max_rows':4,'table_max_cols':5}).ndjson[:1500])
OUTPUT.parent.mkdir(parents=True,exist_ok=True)
SpreadsheetFile.export_xlsx(w).save(str(OUTPUT))
print('EXPORT',OUTPUT,'BYTES',OUTPUT.stat().st_size,'SHA256',hashlib.sha256(OUTPUT.read_bytes()).hexdigest())
