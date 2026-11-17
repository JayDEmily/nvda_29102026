
#!/usr/bin/env python3
"""Bounded repair to private linker aliases after first recorded make failure."""
from pathlib import Path
import hashlib, json, os, subprocess
R=Path("/home/jds/nvda_python3135_sqlite3541_20261117")
arch=R/"deps/usr/lib/x86_64-linux-gnu"
rep_path=R/"build_receipt.json"
raw=rep_path.read_text()
d,_=json.JSONDecoder().raw_decode(raw)
(R/"build_attempt1_failed_receipt.txt").write_text(raw)
d["attempt1"]={"status":"FAILED", "mechanism":"private dev libbz2.so symlink resolves to absent local .so.1.0; linker falls back to non-PIC static libbz2.a", "make_exit_code":d.get("make_exit_code"),"log_path":str(R/"make.log")}
aliases=[]
for link in arch.iterdir():
    if not link.is_symlink() or link.exists():
        continue
    target=os.readlink(link)
    if target.startswith("/"):
        continue
    missing=link.parent/target
    system=Path("/usr/lib/x86_64-linux-gnu")/target
    if not missing.exists() and not missing.is_symlink() and system.exists():
        missing.symlink_to(system)
        aliases.append({"link":str(link),"target":target,"user_created_reference":str(missing),"system_existing_target":str(system)})
print("ALIASES "+json.dumps(aliases),flush=True)
d["private_runtime_linker_aliases"]=aliases
src=R/"Python-3.13.5";pfx=R/"python"
env=dict(os.environ,**d["configure_env"])
with open(R/"make_attempt2.log","w") as log:
    p=subprocess.run(["make","-j2"],cwd=src,env=env,stdout=log,stderr=subprocess.STDOUT,text=True)
d["attempt2_make_exit"]=p.returncode
print("MAKE_EXIT",p.returncode,flush=True)
if p.returncode==0:
    with open(R/"install_attempt2.log","w") as log:
        p=subprocess.run(["make","install"],cwd=src,env=env,stdout=log,stderr=subprocess.STDOUT,text=True)
    d["attempt2_install_exit"]=p.returncode
    print("INSTALL_EXIT",p.returncode,flush=True)
    if p.returncode==0:
        exe=pfx/"bin/python3.13"
        h=hashlib.sha256(exe.read_bytes()).hexdigest()
        d["installed_python_path"]=str(exe)
        d["installed_python_sha256"]=h
        d["build_complete"]=True
        d.pop("error",None)
else:
    d["build_complete"]=False
rep_path.write_text(json.dumps(d,indent=2,sort_keys=True)+"\n")
if not d.get("build_complete",False):raise SystemExit(1)
print("BUILD_COMPLETE",d["installed_python_path"],flush=True)
