
"""Restore missing _ssl/_hashlib by explicit user-local OpenSSL configure inputs."""
from pathlib import Path
import json,os,subprocess,shutil,hashlib
R=Path("/home/jds/nvda_python3135_sqlite3541_20261117")
src=R/"Python-3.13.5"
receipt=R/"build_receipt.json"
d=json.loads(receipt.read_text())
shutil.copy2(src/"config.log",R/"config_attempt1.log")
env=dict(os.environ,**d["configure_env"])
archlib=R/"deps/usr/lib/x86_64-linux-gnu"
env.update({"OPENSSL_LDFLAGS":f"-L{archlib} -Wl,-rpath,{archlib}", "OPENSSL_LIBS":"-lssl -lcrypto","OPENSSL_INCLUDES":f"-I{R}/deps/usr/include"})
d["attempt3_openssl_env"]={k:env[k] for k in ("OPENSSL_LDFLAGS","OPENSSL_LIBS","OPENSSL_INCLUDES")}
for label,cmd in [("configure_openssl",d["configure_command"]),("make_openssl",["make","-j2"]),("install_openssl",["make","install"])]:
    with open(R/(label+".log"),"w") as log:
        p=subprocess.run(cmd,cwd=src,env=env,stdout=log,stderr=subprocess.STDOUT,text=True)
    d[label+"_exit"]=p.returncode
    receipt.write_text(json.dumps(d,indent=2,sort_keys=True)+"\n")
    print(label+" EXIT",p.returncode,flush=True)
    if p.returncode:
        print("FAILED see",R/(label+".log"),flush=True)
        raise SystemExit(1)
py=R/"python/bin/python3.13"
d["installed_python_sha256"]=hashlib.sha256(py.read_bytes()).hexdigest()
d["build_complete"]=True
d["openss_l_reconfigured"]=True
receipt.write_text(json.dumps(d,indent=2,sort_keys=True)+"\n")
print("REBUILD_COMPLETE",py,flush=True)
