"""Stdlib documentary SQLite probes; independent DDL, no authored helper import."""
import sqlite3
from pathlib import Path

HERE = Path(__file__).parent
DEF = 'mmt_raw_ratio_definition_v1'
CFG = 'mmt_raw_ratio_configuration_v1'
OCC = 'mmt_raw_ratio_occurrence_v1'
COLUMNS = {
 DEF: [('owner_namespace','TEXT'),('derived_signal_id','TEXT'),('calculation_definition_version','TEXT'),('payload','BLOB'),('content_sha256','TEXT')],
 CFG: [('owner_namespace','TEXT'),('kind','TEXT'),('context_id','TEXT'),('version','TEXT'),('payload','BLOB'),('content_sha256','TEXT')],
 OCC: [('derived_occurrence_id','TEXT'),('owner_object_id','TEXT'),('owner_namespace','TEXT'),('implementation_brief_sha256','TEXT'),('derived_signal_id','TEXT'),('calculation_definition_version','TEXT'),('subject_instrument','TEXT'),('effective_as_of_utc','TEXT'),('knowledge_cutoff_utc','TEXT'),('logical_identity_payload','BLOB'),('logical_identity_sha256','TEXT'),('payload','BLOB'),('content_sha256','TEXT')],
}
KEYS={DEF:'owner_namespace,derived_signal_id,calculation_definition_version',CFG:'owner_namespace,kind,context_id,version',OCC:'derived_occurrence_id'}
def ddl(name, table, mode='normal'):
    parts=[n+' '+t+' NOT NULL' for n,t in COLUMNS[table]]
    if table==CFG and mode!='configuration-check':
        parts.append("CHECK(kind IN ('parameter','selection','unit','raw_mapping'))")
    if mode.endswith('primary-key'):
        if table==DEF:
            parts.append('UNIQUE('+KEYS[table]+')')
    else:
        parts.append('PRIMARY KEY('+KEYS[table]+')')
    if table==OCC and mode!='occurrence-foreign-key':
        parts.append('FOREIGN KEY(owner_namespace,derived_signal_id,calculation_definition_version) REFERENCES '+DEF+'(owner_namespace,derived_signal_id,calculation_definition_version)')
    return 'CREATE TABLE '+name+'('+','.join(parts)+') STRICT'

for mode, target in [('definition-primary-key',DEF),('configuration-primary-key',CFG),('occurrence-primary-key',OCC),('configuration-check',CFG),('occurrence-foreign-key',OCC)]:
    with sqlite3.connect(HERE/(mode+'.sqlite')) as db:
        db.execute('PRAGMA application_id=0x4E560004')
        db.execute('PRAGMA user_version=1')
        for table in COLUMNS:
            db.execute(ddl(table,table))
        db.execute('INSERT INTO '+DEF+' VALUES(?,?,?,?,?)',('ns','D014','v1',b'def','hash'))
        for kind in ('parameter','selection','unit','raw_mapping'):
            db.execute('INSERT INTO '+CFG+' VALUES(?,?,?,?,?,?)',('ns',kind,'id','1',b'cfg','hash'))
        db.execute('INSERT INTO '+OCC+' VALUES('+','.join('?'*13)+')',('id','M02','ns','brief','D014','v1','NVDA','time','time',b'logical','hash',b'occ','hash'))
        for table in COLUMNS:
            for action in ('UPDATE','DELETE'):
                db.execute('CREATE TRIGGER '+table+'_'+action.lower()+' BEFORE '+action+' ON '+table+" BEGIN SELECT RAISE(ABORT,'immutable raw-ratio record'); END")
        rows={t:db.execute('SELECT * FROM '+t).fetchall() for t in COLUMNS}
        triggers=dict(db.execute("SELECT name,sql FROM sqlite_schema WHERE type='trigger'"))
        old_info=db.execute('PRAGMA table_info('+target+')').fetchall()
        for name in triggers:
            db.execute('DROP TRIGGER '+name)
        db.execute(ddl('independent_rebuild',target,mode))
        db.execute('INSERT INTO independent_rebuild SELECT * FROM '+target)
        db.execute('DROP TABLE '+target)
        db.execute('ALTER TABLE independent_rebuild RENAME TO '+target)
        for sql in triggers.values():
            db.execute(sql)
        assert rows == {t:db.execute('SELECT * FROM '+t).fetchall() for t in COLUMNS}
        assert triggers == dict(db.execute("SELECT name,sql FROM sqlite_schema WHERE type='trigger'"))
        info=db.execute('PRAGMA table_info('+target+')').fetchall()
        assert [r[1:4] for r in info] == [r[1:4] for r in old_info]
        assert db.execute('PRAGMA foreign_key_check').fetchall()==[]
        assert db.execute('PRAGMA integrity_check').fetchall()==[('ok',)]
        assert db.execute('PRAGMA application_id').fetchone()==(0x4E560004,)
        assert db.execute('PRAGMA user_version').fetchone()==(1,)
        assert db.execute('PRAGMA journal_mode').fetchone()==('delete',)
        assert all(db.execute('SELECT strict FROM pragma_table_list WHERE name=?',(t,)).fetchone()==(1,) for t in COLUMNS)
        if mode.endswith('primary-key'):
            assert all(r[5]==0 for r in info)
        elif mode=='configuration-check':
            db.execute('INSERT INTO '+CFG+' VALUES(?,?,?,?,?,?)',('ns','forbidden','id','1',b'cfg','hash'))
        else:
            assert db.execute('PRAGMA foreign_key_list('+OCC+')').fetchall()==[]
        print(mode, 'VALID_DOWNGRADE fullrows/columnlayout/triggers/profile/STRICT preserved; fkcheck clean; integrity ok')
print('DOCUMENTARY_ONLY: no project/test/helper import or execution')
