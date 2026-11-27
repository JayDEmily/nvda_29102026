
#!/usr/bin/env python3
"""Bounded runtime qualification only. Does not execute NVIDIA product tests."""
from pathlib import Path
import subprocess, json, hashlib, os, sys
R=Path("/home/jds/nvda_python3135_sqlite3541_20261117")
repo=Path("/home/jds/nvda_d091_finite_adequacy_20261116")
py=R/"python/bin/python3.13"
lib=R/"sqlite/lib/libsqlite3.so.0"
source=R/"Python-3.13.5.tar.xz"
receipt=R/"qualification_receipt.json"
report={"schema":"NVDA_ISOLATED_CPYTHON_3135_SQLITE_3541_NONPRODUCT_QUALIFICATION_V1","scope":"non-product SQLite runner and original bounded nine mechanism probes only","product_tests_executed":0,"no_system_install":True}
def h(p):
    z=hashlib.sha256()
    with open(p,"rb") as f:
        for b in iter(lambda:f.read(1048576),b""):z.update(b)
    return z.hexdigest()
try:
    assert py.exists(), "new isolated python binary missing"
    report["python_sha256"]=h(py)
    report["python_source_archive_sha256"]=h(source)
    report["sqlite_library_sha256"]=h(lib)
    inspect_code="""import json,sys,sqlite3,_sqlite3,ssl,sysconfig,importlib.metadata
with sqlite3.connect(':memory:') as c:
    sid=c.execute('select sqlite_source_id()').fetchone()[0]
    opts=[r[0] for r in c.execute('pragma compile_options')]
print(json.dumps({'python':sys.version,'executable':sys.executable,'sqlite_version':sqlite3.sqlite_version,'sqlite_source_id':sid,'_sqlite3_origin':_sqlite3.__spec__.origin,'_sqlite3_file':getattr(_sqlite3,'__file__',None),'ssl':ssl.OPENSSL_VERSION,'compile_options':opts,'pip':importlib.metadata.version('pip')}))
"""
    env=dict(os.environ)
    uvbin="/home/jds/Rowing 2026_V2/tooling/bin"
    env["PATH"]=uvbin+":"+env.get("PATH","")
    p=subprocess.run([str(py),"-c",inspect_code],env=env,capture_output=True,text=True)
    report["inspection_exit"]=p.returncode
    report["inspection_stderr"]=p.stderr
    assert p.returncode==0,p.stderr
    report["inspection"]=json.loads(p.stdout)
    so=report["inspection"]["_sqlite3_file"]
    assert so and Path(so).exists(),"sqlite extension not dynamically inspectable"
    report["_sqlite3_sha256"]=h(Path(so))
    link=subprocess.run(["ldd",so],capture_output=True,text=True)
    report["ldd_exit"]=link.returncode
    report["ldd"]=link.stdout
    assert link.returncode==0
    lines=[x for x in link.stdout.splitlines() if "libsqlite3" in x]
    report["sqlite_ldd_lines"]=lines
    assert lines,"no direct sqlite link"
    report["linked_correct_private_sqlite"]=str(lib) in lines[0]
    assert report["linked_correct_private_sqlite"],"active _sqlite3 linked wrong SQLite library"
    report["python_pinned"]=report["inspection"]["python"].startswith("3.13.5")
    report["sqlite_pinned"]=report["inspection"]["sqlite_version"]=="3.54.1"
    report["source_id_matched"]=report["inspection"]["sqlite_source_id"]=="2026-10-16 14:45:20 555e07ef33f69a0957d24d8e555b702464a131d6f1607f4c3c1e4551e8e6ca76"
    assert all((report["python_pinned"],report["sqlite_pinned"],report["source_id_matched"]))
    probe=repo/"handoff/astra_adr_completion_20261115/procedures/runtime_probe.py"
    p=subprocess.run([str(py),str(probe)],env=env,capture_output=True,text=True)
    report["original_probe_exit_code"]=p.returncode
    report["original_probe_stderr"]=p.stderr
    if p.returncode==0:
        report["original_probe"]=json.loads(p.stdout)
        report["all_original_feature_checks_passed"]=all(report["original_probe"]["checks"].values())
        report["original_probe_source_id_matched"]=report["original_probe"]["source_id"]==report["inspection"]["sqlite_source_id"]
        report["original_probe_library_sha256_matched"]=report["original_probe"].get("loaded_library",{}).get("sha256")==report["sqlite_library_sha256"]
    else:
        report["all_original_feature_checks_passed"]=False
        report["original_probe_source_id_matched"]=False
        report["original_probe_library_sha256_matched"]=False
    report["nonproduct_mechanism_qualification_pass"]=all((report["linked_correct_private_sqlite"],report["python_pinned"],report["sqlite_pinned"],report["source_id_matched"],report["all_original_feature_checks_passed"],report["original_probe_source_id_matched"],report["original_probe_library_sha256_matched"]))
    report["product_runner_acceptance"]="NOT_GRANTED_SEPARATE_TESTER_CLAIM_GENERATION_AND_RECEIVER_OUTSTANDING"
except BaseException as e:
    report["nonproduct_mechanism_qualification_pass"]=False
    report["error"]=f"{type(e).__name__}: {e}"
finally:
    receipt.write_text(json.dumps(report,indent=2,sort_keys=True)+"\n")
    print(json.dumps({k:report.get(k) for k in ("python_sha256","sqlite_library_sha256","python_pinned","sqlite_pinned","source_id_matched","linked_correct_private_sqlite","original_probe_exit_code","all_original_feature_checks_passed","original_probe_library_sha256_matched","nonproduct_mechanism_qualification_pass","error")},indent=2),flush=True)
    print("RECEIPT_PATH",receipt)
if not report["nonproduct_mechanism_qualification_pass"]:
    raise SystemExit(1)
