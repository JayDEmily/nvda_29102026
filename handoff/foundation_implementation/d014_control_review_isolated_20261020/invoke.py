"""Pinned same-process entrypoint with explicit candidate module provenance."""
import hashlib
import importlib
import json
from pathlib import Path
import runpy
import sqlite3
import sys

ROOT = Path(__file__).resolve().parent / 'candidate'
sys.path[:0] = [str(ROOT / 'tools'), str(ROOT / 'src')]
for name in ('product_proof_claims', 'nvda_desk.architecture.implementation_authority',
             'nvda_desk.architecture.registry', 'nvda_desk.architecture.schema'):
    module = importlib.import_module(name)
    path = Path(module.__file__).resolve()
    assert path.is_relative_to(ROOT), (name, path)
    print(json.dumps({'module': name, 'path': str(path),
                      'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}), flush=True)
assert hashlib.sha256((ROOT/'tools/product_proof_claims.py').read_bytes()).hexdigest() == 'b2670e26f51d4b6f4fc8c656c859b9e5d63ca9aadd84ff2f818ff06cd9bb118a'
print(json.dumps({'python': sys.version, 'executable': sys.executable,
                  'sqlite': sqlite3.sqlite_version, 'argv': sys.argv[1:]}), flush=True)
mode, target, *arguments = sys.argv[1:]
sys.argv = [target, *arguments]
try:
    if mode == 'module':
        runpy.run_module(target, run_name='__main__', alter_sys=True)
    else:
        runpy.run_path(str(ROOT / target), run_name='__main__')
finally:
    observed = {}
    for name, module in tuple(sys.modules.items()):
        if name.startswith('nvda_desk.') and getattr(module, '__file__', None):
            path = Path(module.__file__).resolve()
            assert path.is_relative_to(ROOT/'src'), (name, path)
            observed[name] = {'path': str(path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
    print(json.dumps({'final_source_modules': observed}, sort_keys=True), flush=True)
