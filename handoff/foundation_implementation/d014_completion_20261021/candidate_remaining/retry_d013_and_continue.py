"""Continue unreached checks only after separately observed complete direct D013."""
from pathlib import Path
source = Path('/workspace/scratch/56b9974b28a0/validate_d014_candidate.py').read_text()
source = source.replace("    ('d014', 'neutral_market_measurement_truth_d014'),\n", '')
source = source.replace("    ('d013', 'neutral_market_measurement_truth_d013'),\n", '')
assert b'observed aggregate outcome: exit=0' in Path('/workspace/scratch/56b9974b28a0/d013-direct-recovery.log').read_bytes()
start = source.index('commands.extend([')
end = source.index("assert not git('status'", start)
source = source[:start] + source[end:]
source = source.replace("head = git('rev-parse', 'HEAD')", "head = git('rev-parse', 'HEAD')\nassert head == 'b0a61a7f960b1cff4f95605347db2773d1078c65'")
source = source.replace("reason='mandatory exact-candidate validation under root 7.3.4'", "reason='incomplete D013 output recovery then unreached mandatory 7.3.4 checks; prior same-candidate D014 retained'")
exec(compile(source, '/workspace/scratch/56b9974b28a0/validate_d014_candidate.py', 'exec'))
