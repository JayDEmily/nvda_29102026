import sys,sysconfig,sqlite3,_sqlite3,hashlib,pathlib,json,importlib.metadata,subprocess,tempfile
out={'scope':'non-product disposable environment mechanisms only','python':sys.version,'executable':sys.executable,'python_sha256':hashlib.sha256(pathlib.Path(sys.executable).resolve().read_bytes()).hexdigest(),'sqlite_version':sqlite3.sqlite_version,'sqlite_extension':_sqlite3.__file__,'extension_sha256':hashlib.sha256(pathlib.Path(_sqlite3.__file__).read_bytes()).hexdigest(),'packages':{d.metadata['Name']:d.version for d in importlib.metadata.distributions()},'uv':subprocess.check_output(['uv','--version'],text=True).strip()}
out['ldd']=subprocess.check_output(['ldd',_sqlite3.__file__],text=True)
for line in out['ldd'].splitlines():
 if 'libsqlite3' in line:
  p=pathlib.Path(line.split('=>')[1].strip().split()[0]);out['loaded_library']={'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
with tempfile.TemporaryDirectory() as d:
 p=pathlib.Path(d)/'non_product.sqlite';c=sqlite3.connect(p);c.execute('pragma foreign_keys=on');c.execute('pragma busy_timeout=0');mode=c.execute('pragma journal_mode=delete').fetchone()[0];c.execute('pragma synchronous=extra')
 c.executescript('create table p(id integer primary key) strict; create table q(id integer references p(id)) strict; create trigger immutable before update on p begin select raise(abort,"immutable"); end;')
 checks={'strict_tables':True,'journal_delete':mode=='delete','synchronous_extra':c.execute('pragma synchronous').fetchone()[0]==3,'busy_timeout_zero':c.execute('pragma busy_timeout').fetchone()[0]==0,'foreign_keys_on':c.execute('pragma foreign_keys').fetchone()[0]==1}
 try:c.execute('insert into q values(99)');checks['foreign_key_refusal']=False
 except sqlite3.IntegrityError:checks['foreign_key_refusal']=True
 c.rollback();c.execute('begin immediate');c.execute('insert into p values(1)');c.commit()
 try:c.execute('update p set id=2');checks['trigger_refusal']=False
 except sqlite3.IntegrityError:checks['trigger_refusal']=True
 c.rollback();out['source_id']=c.execute('select sqlite_source_id()').fetchone()[0];out['compile_options']=[r[0] for r in c.execute('pragma compile_options')];checks['integrity']=c.execute('pragma integrity_check').fetchone()[0]=='ok';c.close()
 c=sqlite3.connect(f'file:{p}?mode=ro',uri=True);checks['readonly_durable_reopen']=c.execute('select id from p').fetchall()==[(1,)];c.close();out['checks']=checks
print(json.dumps(out,indent=2))
