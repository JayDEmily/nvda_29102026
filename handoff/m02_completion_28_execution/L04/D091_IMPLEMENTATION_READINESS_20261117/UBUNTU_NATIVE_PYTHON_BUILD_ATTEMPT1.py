
#!/usr/bin/env python3
"""Build isolated CPython 3.13.5 against official SQLite 3.54.1. No product tests, no system installs."""
from pathlib import Path
import hashlib, json, subprocess, shutil, os, tarfile, urllib.request, time, shlex, sys
root=Path("/home/jds/nvda_python3135_sqlite3541_20261117")
root.mkdir(parents=True, exist_ok=True)
report=root/"build_receipt.json"
repo=Path("/home/jds/nvda_d091_finite_adequacy_20261116")
sqlite_original=Path("/home/jds/nvda_d091_runtime_20261117")
src_sqlite=sqlite_original/"sqlite-autoconf-3540100"
cp_archive=root/"Python-3.13.5.tar.xz"
cp_source=root/"Python-3.13.5"
prefix=root/"python"
sqlite_prefix=root/"sqlite"
deps=root/"deps"
debs=root/"debs"
debs.mkdir(exist_ok=True)
receipt={"kind":"ISOLATED_NON_PRODUCT_CPYTHON3135_SQLITE3541_UBUNTU_BUILD","scope":"no system package install; no product tests","repository_head":subprocess.check_output(["git","-C",str(repo),"rev-parse","HEAD"],text=True).strip(),"python_url":"https://www.python.org/ftp/python/3.13.5/Python-3.13.5.tar.xz","sqlite_official_sha256_expected":"926ef8d3eab93fbf6e06011901273eec076b25594a4e1cdadd50c987f4f6d64e","sqlite_source_id_expected":"2026-10-16 14:45:20 555e07ef33f69a0957d24d8e555b702464a131d6f1607f4c3c1e4551e8e6ca76","steps":[]}
def say(s):
    print(s,flush=True)
def h(path, algo="sha256"):
    z=getattr(hashlib,algo)()
    with open(path,"rb") as f:
        for block in iter(lambda:f.read(1048576),b""):z.update(block)
    return z.hexdigest()
def save():
    report.write_text(json.dumps(receipt,indent=2,sort_keys=True)+"\\n")
def run(cmd,**kwargs):
    say("EXEC: "+" ".join(map(str,cmd)))
    p=subprocess.run(cmd,**kwargs)
    say("EXIT: "+str(p.returncode))
    if p.returncode:raise RuntimeError(f"exit={p.returncode}: {cmd}")
    return p
try:
    say("STAGE SOURCE: check pinning and stage exact SQLite library")
    original_reference=json.loads((repo/"handoff/m02_completion_28_execution/L00/R2_SQLITE_3541_RUNTIME_VERIFIED.json").read_text())
    assert h(sqlite_original/"sqlite-autoconf-3540100.tar.gz")==original_reference["source_archive_sha256"]
    assert h(src_sqlite/"sqlite3.c","sha3_256")==original_reference["sqlite3_c_sha3_256"]
    (sqlite_prefix/"include").mkdir(parents=True,exist_ok=True)
    (sqlite_prefix/"lib").mkdir(parents=True,exist_ok=True)
    for name in ("sqlite3.h","sqlite3ext.h"):
        shutil.copy2(src_sqlite/name,sqlite_prefix/"include"/name)
    lib=sqlite_prefix/"lib/libsqlite3.so.0"
    shutil.copy2(sqlite_original/"libsqlite3.so.0",lib)
    sym=sqlite_prefix/"lib/libsqlite3.so"
    if not sym.exists():sym.symlink_to(lib.name)
    receipt["sqlite_library_sha256"]=h(lib)
    receipt["sqlite3_header_sha256"]=h(sqlite_prefix/"include/sqlite3.h")
    receipt["sqlite_library_source_archive_sha256"]=h(sqlite_original/"sqlite-autoconf-3540100.tar.gz")
    receipt["steps"].append("sqlite source archive SHA256, source sqlite3.c SHA3 and private library copied")
    save()
    say("STAGE DEPS: fetch Ubuntu development packages to user-owned folder, never install into system")
    names=["libssl-dev","libffi-dev","libbz2-dev","liblzma-dev","libreadline-dev","libncurses-dev"]
    packages=[]
    for name in names:
        found=list(debs.glob(name+"_*_amd64.deb"))
        if not found:
            run(["apt","download",name],cwd=debs)
            found=list(debs.glob(name+"_*_amd64.deb"))
        if not found:raise RuntimeError("apt downloaded no file for "+name)
        p=found[0];run(["dpkg-deb","-x",str(p),str(deps)])
        packages.append({"name":name,"deb":p.name,"sha256":h(p),"bytes":p.stat().st_size})
    receipt["apt_downloaded_not_system_installed"]=packages
    archlib=deps/"usr/lib/x86_64-linux-gnu"
    archlib.mkdir(parents=True,exist_ok=True)
    # Keep unmodified host runtime shared libraries as dynamic dependencies; put user-only aliases for symlink resolution.
    for name in ["libssl.so.3","libcrypto.so.3"]:
        link=archlib/name
        if not link.exists():link.symlink_to(Path("/usr/lib/x86_64-linux-gnu")/name)
    receipt["steps"].append("unprivileged Ubuntu .deb downloads and user-owned extraction of dev headers")
    save()
    say("STAGE PYTHON: download official pinned CPython source")
    if not cp_archive.exists():
        with urllib.request.urlopen(receipt["python_url"],timeout=90) as incoming,open(cp_archive,"wb") as out:
            shutil.copyfileobj(incoming,out)
    receipt["python_archive_sha256"]=h(cp_archive)
    receipt["python_archive_bytes"]=cp_archive.stat().st_size
    if not cp_source.exists():
        with tarfile.open(cp_archive,"r:xz") as tf:tf.extractall(root,filter="data")
    receipt["python_source_version_header"]=next(iter((cp_source/"Include/patchlevel.h").read_text().splitlines())) # full path pinned by downloaded archive
    save()
    say("STAGE CONFIGURE: create isolated Ubuntu build with explicit SQLite 3.54.1")
    deps_include=deps/"usr/include"
    deps_include_arch=deps/"usr/include/x86_64-linux-gnu"
    cflags=f"-I{deps_include} -I{deps_include_arch}"
    linkflags=f"-L{archlib} -Wl,-rpath,{archlib}"
    sqlite_cflags=f"-I{sqlite_prefix}/include"
    sqlite_libs=f"-L{sqlite_prefix}/lib -Wl,-rpath,{sqlite_prefix}/lib -lsqlite3"
    env=dict(os.environ,CPPFLAGS=cflags,LDFLAGS=linkflags,LIBSQLITE3_CFLAGS=sqlite_cflags,LIBSQLITE3_LIBS=sqlite_libs)
    conf=["./configure","--prefix="+str(prefix),"--with-ensurepip=install","--without-static-libpython"]
    receipt["configure_env"]={k:env[k] for k in ("CPPFLAGS","LDFLAGS","LIBSQLITE3_CFLAGS","LIBSQLITE3_LIBS")}
    receipt["configure_command"]=conf
    with open(root/"configure.log","w") as output:
        result=subprocess.run(conf,cwd=cp_source,env=env,stdout=output,stderr=subprocess.STDOUT,text=True)
    receipt["configure_exit_code"]=result.returncode
    save()
    if result.returncode:raise RuntimeError("configure failed; see "+str(root/"configure.log"))
    say("STAGE BUILD: Python 3.13.5 with 2 jobs; capture build log")
    with open(root/"make.log","w") as output:
        result=subprocess.run(["make","-j2"],cwd=cp_source,env=env,stdout=output,stderr=subprocess.STDOUT,text=True)
    receipt["make_exit_code"]=result.returncode
    save()
    if result.returncode:raise RuntimeError("make failed; see "+str(root/"make.log"))
    say("STAGE INSTALL: install into private prefix only")
    with open(root/"install.log","w") as output:
        result=subprocess.run(["make","install"],cwd=cp_source,env=env,stdout=output,stderr=subprocess.STDOUT,text=True)
    receipt["install_exit_code"]=result.returncode
    save()
    if result.returncode:raise RuntimeError("make install failed; see "+str(root/"install.log"))
    receipt["installed_python_path"]=str(prefix/"bin/python3.13")
    receipt["installed_python_sha256"]=h(prefix/"bin/python3.13")
    receipt["steps"].append("configure, make -j2 and private-prefix install succeeded; NO product test performed")
    receipt["build_complete"]=True
    save()
    say("BUILD_COMPLETE "+str(prefix/"bin/python3.13"))
except BaseException as exc:
    receipt["build_complete"]=False
    receipt["error"]=f"{type(exc).__name__}: {exc}"
    save()
    say("BUILD_FAILED "+receipt["error"])
    raise
