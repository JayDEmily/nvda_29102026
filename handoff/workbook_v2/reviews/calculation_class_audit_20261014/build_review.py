#!/usr/bin/env python3
"""Read-only 209-row class proposal from exact V1 workbook + effective M01 catalogue.
Do not mutate accepted catalogue, workbook V2, M01 or governance. Requires artifact_tool.
"""
import csv, hashlib, json, collections, re
from pathlib import Path
from artifact_tool import Blob, SpreadsheetFile, Workbook
ROOT=Path(__file__).resolve().parents[4]
DST=Path(__file__).resolve().parent
SOURCE=ROOT/'handoff/m01_completion/authority/NVDA_80_STEP_ACADEMIC_EVIDENCE_AUDIT_WITH_SIGNALS_ADDENDUM_81_94.xlsx'
CAT=ROOT/'handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv'
PREVIEW=ROOT/'handoff/workbook_v2/reviews/derived_family_audit_20261014/NVDA_FUTURE_02_TWO_FIELDS_209_ROW_PREVIEW_20261014.csv'
FAM=ROOT/'handoff/workbook_v2/reviews/derived_family_audit_20261014/NVDA_DERIVED_FAMILY_FULL_209_ROW_AUDIT_20261014.csv'

classes=[
 ('C01','TEMPORAL_AND_DATA_INTEGRITY','Derive timestamp, calendar/session, completeness, vintage or provenance-quality facts','Not directional market behaviour, candidate policy or weighted composite score'),
 ('C02','MARKET_DETERMINISTIC_TRANSFORM','Arithmetic, return, ratio, delta bucket, trade-flow or book-operation reduction of market signal values','No fitted distribution, predictive inference, candidate economics or decision policy'),
 ('C03','DESCRIPTIVE_STATISTICAL_ESTIMATE','Historical volatility, rank, z-score, historical regression, dependence, dispersion or empirical event-rate statistic','Not forward-looking scenario or fitted risk-neutral/physical probability distribution'),
 ('C04','MODEL_BASED_MARKET_INFERENCE','Fitted IV surface, inferred probability, dealer exposure, latent scenario or conditional probabilistic regime','Not a simple observed signal transformation or historical descriptive estimator'),
 ('C05','CONFIGURED_COMPOSITE_SCORE','Multifeature weighted/parameterised scalar score reflecting state or suitability with nontrivial aggregation weights','Not an externally decided permissible limit/action or a raw arithmetic proxy'),
 ('C06','STRUCTURED_STATE_ASSEMBLY','Construct a validated typed multi-signal state vector without treating it as a scalar arithmetic result','Not a fitted probability model or configured trade decision'),
 ('C07','CANDIDATE_ECONOMIC_MEASUREMENT','Prospective execution cost, candidate structure exposure, payoff, expected P&L or stress value','Not permissible risk limits, sizing selection, execution command or actual live holdings'),
 ('C08','LIVE_PORTFOLIO_ECONOMIC_MEASUREMENT','Current portfolio risk Greeks, current P&L, position continuation/modification or liquidation value','Not pre-trade candidate valuation, prescribed hedge/action, or realised fill measurement'),
 ('C09','POLICY_AND_DECISION_RULE','Output is a rule-governed gating, risk budget, size, order-price, exposure selection, hedge or other policy classification','Not merely measuring market facts, economic amounts, or a score used by a separate decision'),
 ('C10','EXECUTION_OUTCOME_MEASUREMENT','Measure completed order fill, completion or realised execution cost','Not forecast cost or a trading order decision'),
 ('C11','PNL_PATH_ATTRIBUTION','Attribute realised/marked P&L over an observed path to the defined risk component or residual','Not live aggregate P&L fields, prospective P&L or forecast scoring'),
 ('C12','RETROSPECTIVE_MODEL_DECISION_EVALUATION','Evaluate locked forecasts, signal value, decision quality, counterfactuals, or model drift on evidence/outcomes','Not current market assessment, prospective strategy utility or order selection'),
 ('C13','OPERATIONAL_RECALCULATION_SCHEDULING','Schedule the next observation/derived recalculation event','Not a trade execution action or current market feature'),
]
# Per-D explicit classification proposals, never inherited from original/proposed family or K-id.
assign={
'C01':'001-005,007,009-010,018',
'C02':'011-017,019-027,042-060,062,066-069,071-077,085-095,097-101,103-104,107-110,116,118-124,131,134-137,143-145,151',
'C03':'028-039,063,078-083,105-106,117,138-142,156',
'C04':'096,102,111-115,125-130,152-154,160',
'C05':'006,008,040-041,061,064,070,084,132,146-150,157-159,163,171-173,187',
'C06':'155',
'C07':'133,161-162,164,168-170,174,177',
'C08':'181-185,188,190-191',
'C09':'065,165-167,175-176,178,186,189,192,208',
'C10':'179-180,193',
'C11':'194-199',
'C12':'200-207',
'C13':'209',
}
assign_map={}
for code, ranges in assign.items():
 for token in ranges.split(','):
  nums=token.split('-'); lo=int(nums[0]); hi=int(nums[-1])
  for n in range(lo,hi+1):
   did=f'D{n:03d}'
   if did in assign_map:raise AssertionError(('duplicate',did,code,assign_map[did]))
   assign_map[did]=code
assert set(assign_map)=={f'D{i:03d}' for i in range(1,210)}, ('missing',sorted({f'D{i:03d}' for i in range(1,210)}-set(assign_map)))
# Targeted judgement notes identify ambiguous/mixed cases; no assertion of authority acceptance.
notes={
 'D006':'Staleness score is weighted/configured, not a bare elapsed-time transformation.',
 'D007':'RequiredFieldPolicy determines the denominator and eligible requirements; not solely R signal values.',
 'D008':'Cross-source temporal alignment quality is scored from multiple time inputs, not raw timestamp conversion.',
 'D015':'Direction classification is rule-governed but output describes contemporaneous market trade direction, not trading strategy.',
 'D026':'Scaling may use price or realised volatility; exact selected definition/parameter law must remain bound.',
 'D040':'Trend score combines persistence, consistency and VWAP slope under configured aggregation.',
 'D061':'Market volatility regime score has market inputs but uses configured score aggregation.',
 'D063':'Macro surprise normalised by empirical historical surprise dispersion, not a fitted forecast.',
 'D064':'Historical sensitivity and event importance mapping are configured event scoring.',
 'D065':'Active window is a rule/policy flag using event importance, not a market return.',
 'D070':'International overnight risk score aggregates returns and FX confirmation; not arithmetic index return.',
 'D078':'Residual conditional factor attribution is a historical regression output; exact conditioning law matters.',
 'D079':'Conditional market beta is regression-based descriptive statistic, not a trading-decision output.',
 'D080':'Conditional technology beta is regression-based descriptive statistic, not trading policy.',
 'D081':'Conditional semiconductor beta is regression-based descriptive statistic, not trading policy.',
 'D082':'Rolling correlations are empirical dependence estimates; condition/universe are versioned.',
 'D084':'Sector rotation score combines several market measurements under configured aggregation.',
 'D091':'Delta bucket is a market-descriptive discrete transform using fixed bucket selection law, not a trade decision.',
 'D096':'ATM-by-expiry surface selection/interpolation is model/convention-sensitive, not simple arithmetic.',
 'D102':'Fitted arbitrage-aware surface error requires a surface fit, not just subtracting two R values.',
 'D104':'Skew rotation is a fixed difference of D099 and D100 at current/prior horizons; 12 Oct authority overrides loose source concept.',
 'D111':'No-arbitrage risk-neutral distribution is inferred from option prices and surface conventions.',
 'D112':'Tail probability integrates an inferred D111 probability density, so retains model inference class.',
 'D113':'Tail probability integrates an inferred D111 probability density, so retains model inference class.',
 'D114':'Physical distribution is predictive conditional modelling with explicit P_MODEL.',
 'D115':'Risk-neutral versus physical gap inherits fitted distribution assumptions even though its final step compares values.',
 'D120':'Signed order-flow aggregate is measured option market activity; quote/trade correlation is essential.',
 'D121':'Flow-by-delta-bucket is a market activity aggregation, not an order allocation policy.',
 'D122':'Flow-by-expiry is a market activity aggregation, not a trade expiry-selection policy.',
 'D125':'Exposure sign requires dealer-side assumption/model even though raw Greeks and OI are market sourced.',
 'D126':'Exposure sign requires inferred dealer position, not observable portfolio holdings.',
 'D127':'Exposure sign requires inferred dealer position, not observable portfolio holdings.',
 'D128':'Concentration inherits modelled dealer gamma exposure D125.',
 'D129':'Gamma flip relies on modelled net dealer gamma scenario, not observed market level.',
 'D130':'Dealer hedging-pressure scenarios are conditional revaluations under assumed dealer-side model.',
 'D132':'Liquidity score mixes spread/depth/flow measures using configured weighting.',
 'D133':'Slippage is a prospective cost estimate under order size/urgency intent, not market liquidity itself.',
 'D138':'Order-book slope is a fitted descriptive relation between price distance and cumulative depth.',
 'D139':'Insert rate is observed-event counting over time; its P_RULE context controls event selection, not an order decision.',
 'D140':'Cancellation rate is observed-event counting over time; its P_RULE context controls event selection.',
 'D141':'Replenishment is a rule-based proxy estimated from order-book/trade events, not an execution command.',
 'D142':'Resilience measures recovery from market-depth disruptions; selection windows matter.',
 'D146':'Latent growth-shock factor is a configured multi-source composite, not a direct yield transformation.',
 'D147':'Latent inflation-shock factor is a configured multi-source composite.',
 'D148':'Latent rate/policy factor is a configured multi-source composite.',
 'D149':'Latent funding/liquidity factor is a configured multi-source composite.',
 'D150':'Composite risk factor is a configured aggregation of other factors.',
 'D152':'Probabilities of dominant drivers are inferred, not observed or just standardised.',
 'D153':'Underlying regime probabilities are inferred from features, not descriptive transforms.',
 'D154':'Options/dealer regime probabilities are inferred from model/state.',
 'D155':'A typed market-state vector is assembly; components may themselves be models/policy-weighted.',
 'D156':'A dependence matrix is an estimated statistical relationship among assembled candidate signals.',
 'D157':'Conflict score discounts correlated information with configured weights.',
 'D158':'Composite data-quality score combines unrelated quality measures with configured weighting.',
 'D159':'Tradeability score is a configured state-quality assessment, before any definitive allow/deny policy.',
 'D160':'A conditional joint scenario set is inferred, forecast-like, with spot/IV/sector/rates/liquidity paths.',
 'D161':'Expected candidate P&L is a prospective amount over candidate exposures and scenarios.',
 'D162':'Tail/CVaR candidate exposure is a prospective economic risk amount, not an allowable limit.',
 'D163':'Uncertainty penalty is configured scoring used to adjust a later utility/decision.',
 'D164':'Total expected costs are prospective candidate/order-intent economics under versioned fee schedules.',
 'D165':'Expected utility applies selected risk/utility policy to measured P&L, costs and risk.',
 'D166':'Tradeable distribution is an allow/deny policy threshold applied to quality and utility.',
 'D167':'Selected exposure is a categorical strategy selection, not market evidence.',
 'D168':'Greek aggregation describes the exposure of a candidate structure, not market-wide dealer exposure.',
 'D169':'Maximum loss depends on candidate payoff/topology and possible scenario convention.',
 'D170':'Breakeven points depend on candidate strikes/leg topology and premiums.',
 'D171':'Expiry suitability is configured scoring of a candidate option-expiry choice.',
 'D172':'Strike suitability is configured scoring of a candidate contract choice.',
 'D173':'Neighbour comparison is configured scoring of alternative candidate choices.',
 'D174':'Stress-loss matrix is a candidate-specific revaluation result, not a permissible capital limit.',
 'D175':'Maximum permissible position risk is a risk-limit policy, distinct from measured candidate CVaR/stress.',
 'D176':'Recommended size is a sizing policy using risk budget, utility and liquidity.',
 'D177':'Current executable entry edge is a prospective economic valuation after costs.',
 'D178':'Limit target selects an execution action price using urgency and minimum edge policy.',
 'D179':'Slippage is realised fill against arrival benchmark, not forecast cost.',
 'D180':'Completion ratio measures executed fraction of an order, not an instruction.',
 'D181':'Live delta is current holdings times live Greeks, not prospective candidate exposure.',
 'D182':'Live gamma is current holdings exposure.',
 'D183':'Live vega is current holdings exposure.',
 'D184':'Live theta is current holdings exposure.',
 'D185':'Live P&L combines current IBKR position/account fields.',
 'D186':'Current-vs-entry similarity applies a stored thesis/entry-state comparison rule.',
 'D187':'Invalidation score is configured thesis-failure aggregation, distinct from a final exit decision.',
 'D188':'Continuation value is prospective valuation of an existing position, not a decision to hold.',
 'D189':'Required hedge is a normative decision about permissible exposure bands, not measured Greeks.',
 'D190':'Modification value compares economic alternatives for a live position; no order is selected.',
 'D191':'Immediate exit value is economic liquidation value after expected costs; not an instruction.',
 'D192':'Hold/hedge/modify/exit is explicit policy/action state.',
 'D193':'Realised costs measure actual fills and commissions.',
 'D194':'Delta P&L attribution is a path decomposition under attribution convention.',
 'D195':'Gamma P&L attribution is a path decomposition under attribution convention.',
 'D196':'Vega P&L attribution is a path decomposition under attribution convention.',
 'D197':'Theta P&L attribution is a path decomposition under attribution convention.',
 'D198':'Skew P&L attribution is a path decomposition under attribution/revaluation convention.',
 'D199':'Unexplained P&L is the residual of the attribution decomposition.',
 'D200':'Decision-quality score evaluates past information-set justification, not a live trading score.',
 'D201':'Counterfactuals evaluate locked past choices on a subsequent observed path; not live scenario forecasts.',
 'D202':'Incremental information value is out-of-sample evaluation, not the original signal itself.',
 'D203':'Calibration error is realised-outcome assessment of probability forecasts.',
 'D204':'Brier score evaluates past binary probability forecast/outcome pairs.',
 'D205':'Log score evaluates past distribution forecasts and realised outcomes.',
 'D206':'OOS decision performance uses historically locked model and realised costs.',
 'D207':'Model drift score evaluates degradation in calibration, usefulness and costs.',
 'D208':'Signal disposition is a governed review classification that constrains future signal use.',
 'D209':'Next update trigger schedules observation/recomputation, not a brokerage trade action.',
}
flagged={'D007','D015','D026','D078','D079','D080','D081','D082','D091','D096','D102','D104','D115','D125','D126','D127','D128','D129','D130','D133','D138','D139','D140','D141','D142','D155','D156','D157','D158','D159','D163','D165','D169','D174','D175','D177','D178','D186','D188','D189','D190','D191','D200','D201','D207','D208'}

# Explicit input agreement: original workbook V1 and source catalogue, not family-to-class mapping.
assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()=='519ea9449297d564ae4a02afc1bf4e60e4471631c81a0842620f9fb60bb4f9ae'
w=SpreadsheetFile.import_xlsx(Blob.load(str(SOURCE)))
s=w.worksheets.get_item('Derived Signals'); original=s.get_range('A5:O213').values
assert len(original)==209 and all(len(row)==15 for row in original)
cat=list(csv.DictReader(CAT.open(encoding='utf-8-sig',newline='')))
old=list(csv.DictReader(PREVIEW.open(encoding='utf-8-sig',newline='')))
family=list(csv.DictReader(FAM.open(encoding='utf-8-sig',newline='')))
assert len(cat)==len(old)==len(family)==209
assert [row[0] for row in original]==[r['derived_id'] for r in cat]==[r['D_ID'] for r in old]==[r['D_ID'] for r in family]
assert all(orow[1]==r['family']==p['Family']==f['Original_Family'] for orow,r,p,f in zip(original,cat,old,family))
assert all(orow[2]==r['derived_signal'] for orow,r in zip(original,cat))
concept_delta=[r['derived_id'] for orow,r in zip(original,cat) if orow[6]!=r['calculation_concept']]
assert concept_delta==['D116'], ('unexpected V1/current catalogue concept differences',concept_delta)
assert all(p['Calculation_class']=='' and p['Calculation_class_Status']=='UNASSESSED' for p in old)
classinfo={x[0]:x for x in classes}

cols=['D_ID','Original_Excel_Row','Original_Family','Proposed_Family_Review_Only','Proposed_Calculation_Class_Code','Proposed_Calculation_Class','Proposal_Status','Adjudication_Needed','Individual_Classification_Reason','Original_Calculation_Concept','Effective_Calculation_Concept','V1_vs_Normative_Concept','Original_Parameter_Window','Original_Units','Original_Update_Cadence','Original_Applicable_Universe','Original_Purpose','Original_Notes','V1_R_Dependencies','V1_D_Dependencies','Effective_R_Dependencies','Effective_D_Dependencies','R_Dependency_Delta','D_Dependency_Delta','Effective_Kernel','Effective_Parameter_Profiles','Effective_Authority_Class','Effective_Typed_Contexts','Effective_Brief_Rule_Ref','Effective_Binding_Note','V1_Source_Locator','V1_Row_SHA256','Effective_Catalogue_Locator','Normative_Status','Future_02_Calculation_Class','Future_02_Class_Status']
rows=[]
diff_r=[];diff_d=[]
for i,(v,n,o,f) in enumerate(zip(original,cat,old,family),start=5):
 did=v[0];cc=assign_map[did];item=classinfo[cc]
 vraw=re.findall(r'R\d{3}',v[4] or '')
 vderived=re.findall(r'D\d{3}',v[5] or '')
 eraw=n['raw_dependencies'].split(';') if n['raw_dependencies'] else []
 ederived=n['derived_dependencies'].split(';') if n['derived_dependencies'] else []
 rdelta='DIFF' if set(vraw)!=set(eraw) else 'SAME'
 ddelta='DIFF' if set(vderived)!=set(ederived) else 'SAME'
 if rdelta=='DIFF':diff_r.append(did)
 if ddelta=='DIFF':diff_d.append(did)
 vsha=hashlib.sha256(json.dumps(v,ensure_ascii=False,default=str,separators=(',',':')).encode('utf-8')).hexdigest()
 why=notes.get(did)
 if not why:
  why=f"{did}: output '{n['derived_signal']}' is assigned by its documented operation: {n['calculation_concept']} Classification criterion: {item[2]}"
 row=[did,i,v[1],f['Proposed_Family'],cc,item[1],'PROPOSAL_NOT_APPROVED','YES' if did in flagged else 'NO',why,v[6],n['calculation_concept'],'CHANGED_D116_AUTHORISED_20261011' if did=='D116' else 'IDENTICAL',v[7],v[8],v[9],v[10],v[12],v[14],v[4],v[5],n['raw_dependencies'],n['derived_dependencies'],rdelta,ddelta,n['kernel_id'],n['parameter_profiles'],n['authority_class'],n['typed_contexts'],n['brief_rule_ref'],n['binding_note'],f'Derived Signals!A{i}:O{i}',vsha,f'NVDA_DERIVED_SIGNAL_CATALOGUE.csv:{i-3}','UNCHANGED',None,'UNASSESSED']
 rows.append(row)
assert len(rows)==209
with (DST/'NVDA_209_CALCULATION_CLASS_REVIEW_ONLY.csv').open('w',newline='',encoding='utf-8-sig') as fp:
 wr=csv.writer(fp);wr.writerow(cols);wr.writerows(rows)
with (DST/'NVDA_PROPOSED_13_CALCULATION_CLASSES.csv').open('w',newline='',encoding='utf-8-sig') as fp:
 wr=csv.writer(fp);wr.writerow(['Class_Code','Proposed_Calculation_Class','Definition','Exclusion']);wr.writerows(classes)

counts=collections.Counter(assign_map.values())
summary={'source_workbook_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'effective_m01_catalogue_sha256':hashlib.sha256(CAT.read_bytes()).hexdigest(),'source_d_rows_read':len(original),'source_vs_effective_concept_differences':concept_delta,'source_vs_effective_raw_dependency_differences':diff_r,'source_vs_effective_derived_dependency_differences':diff_d,'class_proposals':len(rows),'candidate_classes':len(classes),'adjudication_flags':sorted(flagged),'class_counts':dict(sorted(counts.items())),'original_workbook_modified':False,'existing_v2_workbook_modified':False,'taxonomy_approved':False,'future_02_calculation_class_assigned':0}
(DST/'AUDIT_READBACK.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

# Reader-oriented supplemental review workbook. Do NOT open/re-export the original 7-tab or V2 workbook.
book=Workbook.create()
ws=book.worksheets.add('Overview')
ws.get_range('A1:D5').values=[['CALCULATION CLASS — REVIEW ONLY',None,None,None],['209 D-signals assessed individually; no accepted class assignment',None,None,None],['Source of truth','V1 workbook / effective M01 CSV',None,None],['Classification status','PROPOSAL_NOT_APPROVED',None,None],['Future 02 class fields','UNASSESSED throughout',None,None]]
ws.get_range('A7:D7').values=[['Code','Proposed class','Count','Scope']]
ws.get_range('A8:D20').values=[[code,name,counts[code],desc] for code,name,desc,_ in classes]
ws.get_range('A22').values=[['Review flags']];ws.get_range('B22').values=[[len(flagged)]]
ws.get_range('A24').values=[['No 40-family adoption; no normative catalogue, module or equation changes.']]
ws.get_range('A1:D1').format={'fill':'#172A41','font':{'color':'#FFFFFF','bold':True},'row_height':32}
ws.get_range('A7:D7').format={'fill':'#24425B','font':{'color':'#FFFFFF','bold':True},'row_height':24}
for col,width in [('A',25),('B',41),('C',12),('D',78)]:ws.get_range(f'{col}1:{col}24').format.column_width=width
ws.freeze_panes.freeze_rows(7)
ws2=book.worksheets.add('Class Definitions')
ws2.get_range('A1:D14').values=[['Code','Proposed class','Positive definition','Exclusion boundary']]+[list(x) for x in classes]
ws2.get_range('A1:D1').format={'fill':'#172A41','font':{'color':'#FFFFFF','bold':True},'row_height':30}
for col,width in [('A',14),('B',40),('C',85),('D',75)]:ws2.get_range(f'{col}1:{col}14').format.column_width=width
ws2.freeze_panes.freeze_rows(1)
ws3=book.worksheets.add('209 Row Audit')
# A bounded review table, with source details already in the adjacent raw CSV.
short_headers=['D-ID','V1 row','Original family','Proposed family (review)','Proposed class','Status','Flag','Individual reason','V1 concept','Effective R','Effective D','Kernel','Contexts','V1 source']
short_idx=[cols.index(k) for k in ['D_ID','Original_Excel_Row','Original_Family','Proposed_Family_Review_Only','Proposed_Calculation_Class','Proposal_Status','Adjudication_Needed','Individual_Classification_Reason','Original_Calculation_Concept','Effective_R_Dependencies','Effective_D_Dependencies','Effective_Kernel','Effective_Typed_Contexts','V1_Source_Locator']]
ws3.get_range_by_indexes(0,0,210,len(short_headers)).values=[short_headers]+[[r[j] for j in short_idx] for r in rows]
ws3.get_range('A1:N1').format={'fill':'#172A41','font':{'color':'#FFFFFF','bold':True},'row_height':32}
for col,width in [('A',11),('B',11),('C',25),('D',35),('E',43),('F',24),('G',11),('H',75),('I',84),('J',25),('K',25),('L',32),('M',40),('N',30)]:ws3.get_range(f'{col}1:{col}210').format.column_width=width
ws3.freeze_panes.freeze_rows(1)
# Include explicit future 02 status in a second sheet; unassessed blanks never confused with approval.
ws4=book.worksheets.add('02 Field Preview Only')
ws4.get_range('A1:H210').values=[['D_ID','Family current V1','Proposed family (unapproved)','Calculation class','Calculation class status','Proposed class review','Class proposal status','Review flag']]+[[r[0],r[2],r[3],None,'UNASSESSED',r[5],r[6],r[7]] for r in rows]
ws4.get_range('A1:H1').format={'fill':'#172A41','font':{'color':'#FFFFFF','bold':True},'row_height':30}
for col,width in [('A',14),('B',27),('C',37),('D',25),('E',28),('F',43),('G',26),('H',20)]:ws4.get_range(f'{col}1:{col}210').format.column_width=width
ws4.freeze_panes.freeze_rows(1)
output=DST/'NVDA_209_CALCULATION_CLASS_REVIEW_20261014.xlsx'
SpreadsheetFile.export_xlsx(book).save(str(output))
# check export readback
bk=SpreadsheetFile.import_xlsx(Blob.load(str(output)))
back=bk.worksheets.get_item('209 Row Audit').get_range('A2:A210').values
assert [r[0] for r in back]==[f'D{i:03d}' for i in range(1,210)]
status=bk.worksheets.get_item('02 Field Preview Only').get_range('D2:E210').values
assert all(not row[0] and row[1]=='UNASSESSED' for row in status)
assert sum(counts.values())==209 and len(flagged&set(assign_map))==len(flagged)
print(json.dumps(summary,indent=2))
print('Review workbook:',output)
