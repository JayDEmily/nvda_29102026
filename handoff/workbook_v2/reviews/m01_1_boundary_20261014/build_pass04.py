"""Workbook V2 Pass 04: exhaustive proposed M01-1 semantic eligibility, and candidate-only tab.

Evidence and only source of D/R dependency authority: 209-row effective M01 CSV.
Original V1 workbook is cited by D-ID + source row, and left unchanged.
Programmatically reconciles full 209 rows, recursively checks every proposed YES ancestor,
and refuses account/position/order/execution raw upstream dependencies.

This is a proposal based on calculation semantics. It is NOT an independent per-D
code/test certification, a classification-authority adoption, or an M01 edit.
"""
from pathlib import Path
import csv,hashlib,json,collections
from artifact_tool import Blob,SpreadsheetFile

ROOT=Path(__file__).resolve().parents[4]
HERE=Path(__file__).resolve().parent
SRC=ROOT/'handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv'
V1=ROOT/'handoff/m01_completion/authority/NVDA_80_STEP_ACADEMIC_EVIDENCE_AUDIT_WITH_SIGNALS_ADDENDUM_81_94.xlsx'
INCOMING=ROOT/'handoff/workbook_v2/NVDA_SIGNALS_RESEARCH_WORKBOOK_V2_PASS02.xlsx'
PREV=ROOT/'handoff/workbook_v2/reviews/calculation_class_audit_20261014/NVDA_209_CALCULATION_CLASS_REVIEW_ONLY.csv'
OUT=ROOT/'handoff/workbook_v2/NVDA_SIGNALS_RESEARCH_WORKBOOK_V2_PASS04.xlsx'
CSV=HERE/'M01_1_FULL_209_ROW_ELIGIBILITY_REVIEW.csv'
SUM=HERE/'M01_1_AUDIT_SUMMARY.json'
assert hashlib.sha256(SRC.read_bytes()).hexdigest()=='26c5486d1a4c7ff68025c7ce2d7e6847a7798759b847a716c942fd05345f3803'
assert hashlib.sha256(V1.read_bytes()).hexdigest()=='519ea9449297d564ae4a02afc1bf4e60e4471631c81a0842620f9fb60bb4f9ae'
assert hashlib.sha256(INCOMING.read_bytes()).hexdigest()=='7b656fc5c53284f3c67c9c3d40641c56b33dde8534682595cde6d867ff16e036'

with SRC.open(newline='',encoding='utf-8-sig') as f: catalogue=list(csv.DictReader(f))
with PREV.open(newline='',encoding='utf-8-sig') as f: prev=list(csv.DictReader(f))
assert len(catalogue)==len(prev)==209
assert [x['derived_id'] for x in catalogue]==[f'D{i:03}' for i in range(1,210)]
assert [x['D_ID'] for x in prev]==[x['derived_id'] for x in catalogue]

# Every group below is a deliberate row-by-row semantic assessment after reading
# the original 15-column worksheet, all 18 columns of the effective catalogue,
# and the accepted K01..K17 mathematics. No automatic family/kernel acceptance.
YES=set()
def add(lo,hi=None):
    for i in range(lo,(hi or lo)+1):
        ident=f'D{i:03}'
        assert ident not in YES, ('duplicate reviewed inclusion',ident)
        YES.add(ident)
# Source-time/integrity, quote/trade, price path, volume and realized volatility
add(1,5);add(9,10);add(11,39)
# Macro, FX, VIX and descriptive surprise/market return statistics
add(42,60);add(63);add(66,69);add(71,83)
# Contract/time/quote market transforms and IV calculations, including D096
# mathematical delta interpolation but excluding D091 tunable bucket definition
add(85,90);add(92,101);add(103,108)
# Raw-derived contract volume, OI and option flow, excluding D109/D110 because
# both use unadmitted D091 and D121 for the same reason
add(116,120);add(122,124)
# Objective order-book measurements; D141/142 configurable detection thresholds
# have not been fixed as non-discretionary definitions
add(131);add(134,140);add(143,145)
# Market breadth has a proposed variable-weight mode: D151 excluded conservatively.
assert len(YES)==114,len(YES)

# Every NO gets an explicit semantic basis, never a kernel/family-only inference.
reason={}
def no(ids,reason_code,detail):
    for i in ids:
        key=f'D{i:03}'
        assert key not in reason and key not in YES, ('conflicting judgement',key)
        reason[key]=(reason_code,detail)

no([6,8],'WEIGHTED_QUALITY_SCORE','Configured staleness/synchronisation weights or a scored quality model; not a fixed pure market-data transform.')
no([7],'REQUIRED_FIELD_POLICY','Requires RequiredFieldPolicy keyed to active decision requirements; non-signal policy input.')
no([40,41,61,70,84,132],'CONFIGURED_COMPOSITE_SCORE','P_SCORE supplies feature extraction, weights/orientation/transforms; independent coefficient choices rather than only upstream market values.')
no([62],'EVENT_SELECTION_CONTEXT','Next *relevant* scheduled event requires an external applicability/selection definition, not solely a fixed market transformation.')
no([64],'EVENT_IMPORTANCE_MODEL','Importance and historical market sensitivity are externally modelled/weighted into a score.')
no([65],'EVENT_APPLICABILITY_GATE','Configured event-importance threshold and applicability rule constitute a decision-context gate.')
no([91],'UNFIXED_BUCKET_POLICY','P_RULE supplies externally versioned delta-bucket boundaries. The fixed objective bucket contract required by M01-1 is not established.')
no([102],'FITTED_PRICING_MODEL','Constrained option-surface fit uses OptionRevaluationConventionVersion and selected pricing/model assumptions.')
no([109,110,121],'NONQUALIFYING_PREDECESSOR','Uses D091 delta buckets whose non-discretionary boundary contract is not yet established; transitive M01-1 criterion fails.')
no([111,112,113,114,115],'MODEL_DISTRIBUTION','Depends on fitted risk-neutral/physical distributions, probability density modelling, threshold selection or model-comparison conventions.')
no([125,126,127,128,129,130],'DEALER_POSITION_ASSUMPTION','Inferred dealer side/sign, gamma exposure or dealer-hedging scenario requires an external positioning/revaluation assumption.')
no([133],'ORDER_INTENT_CONTEXT','Expected executable slippage depends on intended order size/side and liquidity/extrapolation convention, not solely a market-measurement output.')
no([141,142],'CONFIGURED_EVENT_THRESHOLD','Replenishment/recovery event requires adjustable time or recovery-fraction/spread thresholds; not yet a fixed non-strategy measurement definition.')
no([146,147,148,149,150],'LATENT_FACTOR_WEIGHTS','Versioned latent/composite-factor features, scalings and discretionary weights are configured under P_SCORE.')
no([151],'VARIABLE_BASKET_WEIGHTS','Canonical breadth carrier permits externally weighted basket variant; no single fixed, non-strategy weight convention is established for the entire D151 definition.')
no([152,153,154],'FITTED_REGIME_MODEL','Multinomial/softmax probabilities require coefficient matrix/intercepts and feature standardisation model inputs.')
no([155],'MIXED_MODEL_STATE_ASSEMBLY','Canonical vector includes upstream probability and composite model/score outputs outside the proposed M01-1 graph.')
no([156],'NONQUALIFYING_PREDECESSOR','Correlation/partial-correlation matrix consumes mixed model-based D155 state and a separately chosen ridge penalty.')
no([157,158,159],'WEIGHTED_DECISION_QUALITY','Includes model/score predecessor paths plus P_SCORE weights or tradeability/decision-quality criteria.')
no([160],'SCENARIO_MODEL','Joint scenarios use model distributions, shocks, grids and versioned scenario mappings.')
no([161,162,163,164,165,166,167],'CANDIDATE_RISK_UTILITY_POLICY','Candidate P&L/risk, expected costs, parameterised utility, eligibility and selection depend on candidate or policy assumptions.')
no([168,169,170],'CANDIDATE_STRUCTURE_CONTEXT','Structure-level exposure, maximum loss or breakeven uses a hypothetical candidate leg/quantity/premium configuration.')
no([171,172,173],'STRATEGY_STRUCTURE_SCORING','Chosen strike/expiry/structure scoring consumes configurable weights/targets and candidate sets.')
no([174,175,176],'RISK_LIMIT_POSITION_SIZING','Candidate stress outcomes, permissible risk policy and sizing require non-market candidate/portfolio/policy inputs.')
no([177,178],'TRADE_EXECUTION_DECISION','Prospective executable edge and order limit selection depend on order intent and strategy reserve.')
no([179,180],'ORDER_EXECUTION_STATE','Fill slippage/fill fraction consume actual order/execution/account state, not raw market signals alone.')
no([181,182,183,184,185],'LIVE_PORTFOLIO_STATE','Depends on position quantities or provider realised/unrealised P&L, not market signal values alone.')
no([186,187,188,189,190,191,192],'LIVE_CONTROL_POLICY','Entry/current portfolio comparison, invalidation, hold utility, hedge, liquidation or action rule depends on policy/position/decision contexts.')
no([193,194,195,196,197,198,199],'TRADE_ATTRIBUTION','Execution costs, position path, Greek-attributed P&L and residuals require trade/position history and attribution conventions.')
no([200,201,202,203,204,205,206,207,208],'MODEL_EVALUATION','Retrospective judgement/calibration, counterfactual, performance evaluation or signal admission policy needs evaluated forecasts/outcomes or evaluation sets.')
no([209],'RECALCULATION_CONTROL','Scheduled/runtime control-loop trigger is not a strategy-independent mathematical market signal.')

ALL={f'D{i:03}' for i in range(1,210)}
assert YES.isdisjoint(reason), YES&set(reason)
assert YES|set(reason)==ALL, sorted(ALL-YES-set(reason))
byid={r['derived_id']:r for r in catalogue}
raw_market_exclusion=range(205,236) # provider account, positions, orders/executions
for ident in sorted(YES):
    r=byid[ident]
    for d in filter(None,r['derived_dependencies'].split(';')):
        assert d in YES, (ident,'unadmitted D predecessor',d)
    for raw in filter(None,r['raw_dependencies'].split(';')):
        assert int(raw[1:]) not in raw_market_exclusion, (ident,'non-market account/order/position R predecessor',raw)

rkeys=['D_ID','M01_1_Proposed_Eligibility','Eligibility_Status','Exclusion_Code','Individual_Assessment','Source_Row_V1','Original_Family_V1','Proposed_Family_Review_Only','Proposed_Calculation_Class_Review_Only','Signal_Name','Raw_Dependencies_Effective','Derived_Dependencies_Effective','Parameter_Profiles_Effective','Typed_Contexts_Effective','Kernel_Effective','Concept_Effective','Concept_V1','Source_Unit','Source_Window','Source_Cadence','Source_Universe','Normative_Brief_Reference','V1_Locator','Effective_CSV_Locator','Requires_NonStrategy_Convention_Freeze','Implementation_And_Independent_Tests','Approval_Status']

rows=[]
for index,(r,p) in enumerate(zip(catalogue,prev),start=1):
    ident=r['derived_id']; assert ident==p['D_ID']
    # Direct interpretation uses actual row concept, effective R/D graph, Kxx definition.
    yes=ident in YES
    if yes:
        code=''
        detail=('Exact accepted '+r['kernel_id']+' measurement of '+r['derived_signal']+' from admitted R/D market/clock inputs; '
                'no candidate, portfolio, decision policy, dealer-position or scored predictive-model input in its effective dependency closure.')
    else:
        code,detail=reason[ident]
    # Explicitly identify the review qualification for parameters whose precise
    # fixed non-strategy sampling conventions must still be evidenced/proved.
    needs='YES' if yes and r['parameter_profiles'] in ('P_WINDOW','P_BASELINE','P_REGRESSION','P_CROSS_SECTION','P_SURFACE','P_RULE','P_TIME') else 'NO'
    text=detail+(' A non-strategy measurement convention must be fixed to the D-definition before formal module admission.' if needs=='YES' else '')
    rows.append(dict(zip(rkeys, [
        ident,'YES' if yes else 'NO','PROPOSED_SEMANTIC_ELIGIBILITY_ONLY' if yes else 'NOT_ADMITTED_PROVISIONALLY',
        code,text,r['workbook_row'].split('!')[-1],p['Original_Family'],p['Proposed_Family_Review_Only'],p['Proposed_Calculation_Class'],
        r['derived_signal'],r['raw_dependencies'],r['derived_dependencies'],r['parameter_profiles'],r['typed_contexts'],r['kernel_id'],
        r['calculation_concept'],p['Original_Calculation_Concept'],r['units'],r['parameter_window'],r['update_cadence'],r['applicable_universe'],
        r['brief_rule_ref'],'Derived Signals!A'+str(index+4)+':O'+str(index+4),f'NVDA_DERIVED_SIGNAL_CATALOGUE.csv:{index+1}',
        needs,'NOT_INDIVIDUALLY_VERIFIED_IN_THIS_PASS','WORKBOOK_V2_REVIEW_NOT_M01_AUTHORITY'])) )
assert len(rows)==209 and sum(r['M01_1_Proposed_Eligibility']=='YES' for r in rows)==114
with CSV.open('w',encoding='utf-8-sig',newline='') as f:
    writer=csv.DictWriter(f,fieldnames=rkeys);writer.writeheader();writer.writerows(rows)

# Preserve the 8 existing tabs unchanged and ADD only the candidate-only tab.
w=SpreadsheetFile.import_xlsx(Blob.load(str(INCOMING)))
name='M01-1 Derived Raw'
s=w.worksheets.add(name)
s.get_range('A1:S1').merge()
s.get_range('A1').values=[['M01-1 — STRATEGY-INDEPENDENT DERIVED RAW SIGNALS | REVIEW CANDIDATES ONLY']]
s.get_range('A1:S1').format={'fill':'#13314D','font':{'bold':True,'color':'#FFFFFF','size':14},'row_height':30}
s.get_range('A2:S2').merge()
s.get_range('A2').values=[[f'{len(YES)} of 209 D-signals — proposed semantic eligibility; not accepted architecture or individually proved tests. Full 209 YES/NO evidence in committed CSV.']]
s.get_range('A2:S2').format={'fill':'#E8F1F7','font':{'color':'#123B56','size':10},'row_height':26,'wrap_text':True}
s.get_range('A3:S3').merge()
s.get_range('A3').values=[['Original family preserved; proposed family and calculation class are UNAPPROVED review labels. R/D dependencies and calculation concepts use effective normative M01 catalogue.']]
s.get_range('A3:S3').format={'font':{'color':'#334155','italic':True,'size':10},'row_height':24,'wrap_text':True}
cols=['D-ID','Name','Original family (V1)','Proposed family (review)','Proposed class (review)','R dependencies','D dependencies','Kernel','Parameter profile','Typed context','Effective calculation concept','V1 calculation concept','Units','Window','Cadence','Universe','Source V1 row','Why M01-1 candidate','Outstanding convention/proof']
s.get_range('A5:S5').values=[cols]
s.get_range('A5:S5').format={'fill':'#17637A','font':{'bold':True,'color':'#FFFFFF','size':10},'row_height':34,'wrap_text':True}
subset=[r for r in rows if r['M01_1_Proposed_Eligibility']=='YES']
values=[]
for r in subset:
    values.append([r['D_ID'],r['Signal_Name'],r['Original_Family_V1'],r['Proposed_Family_Review_Only'],r['Proposed_Calculation_Class_Review_Only'],r['Raw_Dependencies_Effective'],r['Derived_Dependencies_Effective'],r['Kernel_Effective'],r['Parameter_Profiles_Effective'],r['Typed_Contexts_Effective'],r['Concept_Effective'],r['Concept_V1'],r['Source_Unit'],r['Source_Window'],r['Source_Cadence'],r['Source_Universe'],r['V1_Locator'],r['Individual_Assessment'],
            ('Non-strategy measurement convention must be frozen. ' if r['Requires_NonStrategy_Convention_Freeze']=='YES' else '')+'Separate per-signal code/test proof NOT established.'])
s.get_range(f'A6:S{5+len(values)}').values=values
s.get_range(f'A6:S{5+len(values)}').format.row_height=58
s.get_range(f'A6:S{5+len(values)}').format.vertical_alignment='top'
# Bounded widths; legibility via wrapping/filter rather than unbounded autofit.
for col,width in {'A':11,'B':32,'C':23,'D':26,'E':29,'F':25,'G':22,'H':24,'I':20,'J':26,'K':58,'L':58,'M':18,'N':23,'O':23,'P':26,'Q':22,'R':62,'S':46}.items():
    s.get_range(f'{col}:{col}').format.column_width=width
s.get_range(f'A5:S{5+len(values)}').format.wrap_text=True
s.freeze_panes.freeze_rows(5)
# Filterable candidate-only range; the table belongs exclusively to the new sheet.
s.tables.add(f'A5:S{5+len(values)}',True,'M011Candidates')
SpreadsheetFile.export_xlsx(w).save(str(OUT))

summary={'source_catalogue_sha256':hashlib.sha256(SRC.read_bytes()).hexdigest(),
'original_v1_sha256':hashlib.sha256(V1.read_bytes()).hexdigest(),
'incoming_v2_pass02_sha256':hashlib.sha256(INCOMING.read_bytes()).hexdigest(),
'pass04_sha256':hashlib.sha256(OUT.read_bytes()).hexdigest(),
'assessed_ids':209,'proposed_yes':len(YES),'proposed_no':209-len(YES),
'proposed_yes_ids':sorted(YES),'no_reason_codes':dict(collections.Counter(r['Exclusion_Code'] for r in rows if r['M01_1_Proposed_Eligibility']=='NO')),
'yes_to_no_derived_edges':0,'yes_direct_to_nonmarket_account_order_position_R':0,
'candidate_sheet_name':name,'formal_module_admission':'NOT_AUTHORISED',
'per_signal_code_test_independent_proof':'NOT_ESTABLISHED',
'classification_status':'PROPOSAL_NOT_ACCEPTED','row_audit_csv_sha256':hashlib.sha256(CSV.read_bytes()).hexdigest()}
SUM.write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in summary.items() if k!='proposed_yes_ids'},indent=2))
