import os
from pathlib import Path
import shlex
import shutil
import subprocess
import tempfile

out = Path(__file__).parent
source = Path('/workspace/scratch/83dd7c79f14f/NVDA_V2_CLEAN_RECOVERED_REPO_20261022')
root = Path(tempfile.mkdtemp(prefix='d015-implementation-v2-')) / 'repo'
out.joinpath('private_path.txt').write_text(str(root) + '\n')
python = '/workspace/scratch/83dd7c79f14f/d015-final-runtime-xl670J/dev/bin/python'
env = os.environ.copy()
env['PYTHONPATH'] = str(root / 'tools') + ':' + str(root / 'src')
def run(label, args, cwd):
    r = subprocess.run(args, cwd=cwd, env=env, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out.joinpath(label + '.log').write_text('$ cd ' + str(cwd) + '\n$ ' + shlex.join(args) + '\n' + r.stdout + f'\nEXIT={r.returncode}\n')
    print(label, r.returncode, r.stdout, flush=True)
    if r.returncode:
        raise SystemExit(r.returncode)
run('00_environment', [python, '-c', "import platform,sqlite3,importlib.metadata as m; actual=(platform.python_version(),sqlite3.sqlite_version,*(m.version(x) for x in ('pytest','mypy','ruff','PyYAML'))); print(actual); assert actual==('3.12.14','3.53.1','9.0.3','1.20.1','0.15.11','6.0.3')"], source)
run('01_clone', ['git', 'clone', '--no-hardlinks', str(source), str(root)], source)
run('02_checkout', ['git', 'checkout', '--detach', 'ef4ff63f790987a2f54e2ba796038e1eae8ee8d6'], root)
run('03_boundary', [python, str(out / 'boundary.py'), str(root)], root)
run('04_strict', [python, 'tools/run_product_proof_gate.py', '--aggregate', 'neutral_market_measurement_truth_d015'], root)
shutil.copyfile(out.parent / 'd015-implementation-review/direct_public.py', out / 'direct_public.py')
run('05_direct_public', [python, str(out / 'direct_public.py'), str(root)], root)
