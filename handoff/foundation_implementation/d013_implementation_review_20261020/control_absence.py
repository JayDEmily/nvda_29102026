from pathlib import Path
from product_proof_claims import load_product_proof_claim
for name in ('neutral_market_measurement_truth_d013','neutral_market_measurement_truth_d012','neutral_market_measurement_truth_pilot','raw_signal_occurrence_truth_sqlite'):
    try:
        load_product_proof_claim(Path.cwd(),name)
    except ValueError as exc:
        assert 'unowned D013 extension Python source without descriptor' in str(exc),str(exc)
        print(name,'REJECT:',str(exc))
    else:
        raise AssertionError(name+' wrongly accepted descriptor-absent actual D013 source')
