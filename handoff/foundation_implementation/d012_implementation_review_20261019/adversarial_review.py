"""Bounded independent storage/control adversaries; disposable copies only."""
import hashlib
import json
import os
import shutil
import sqlite3
import subprocess
import sys
import tarfile
from pathlib import Path

from direct_review import BASE, BRIEF, exact, f

SOURCE = Path('/workspace/scratch/d549b6d808a9/g52-recovery/repository')
def encoding(doc):
    return json.dumps(doc, sort_keys=True, ensure_ascii=True, separators=(',', ':')).encode()

def storage():
    for mode in ('equation', 'representation', 'lineage_representation', 'hash', 'index', 'logical_hash'):
        clone = BASE / ('corrupt-' + mode + '.sqlite')
        with sqlite3.connect(BASE / 'writer-exited.sqlite') as src, sqlite3.connect(clone) as dst:
            src.backup(dst)
        with sqlite3.connect(clone) as conn:
            name, sql = conn.execute("SELECT name,sql FROM sqlite_schema WHERE type='trigger' AND name='mmt_occurrence_v1_update'").fetchone()
            conn.execute('DROP TRIGGER ' + name)
            row = conn.execute('SELECT payload FROM mmt_occurrence_v1').fetchone()
            doc = json.loads(row[0])
            if mode == 'equation': doc['result'] = {'kind':'decimal','sign':0,'digits':'10100','exponent':-2}
            if mode == 'representation': doc['result'] = {'kind':'decimal','sign':0,'digits':'2','exponent':0}
            if mode == 'lineage_representation': doc['raw_input_lineage'][0]['canonical_value'] = {'kind':'decimal','sign':0,'digits':'100','exponent':0}
            if mode in ('equation', 'representation', 'lineage_representation'):
                payload = encoding(doc)
                conn.execute('UPDATE mmt_occurrence_v1 SET payload=?,content_sha256=?', (payload, hashlib.sha256(payload).hexdigest()))
            elif mode == 'hash': conn.execute("UPDATE mmt_occurrence_v1 SET content_sha256=?", ('0'*64,))
            elif mode == 'index': conn.execute("UPDATE mmt_occurrence_v1 SET derived_signal_id='D011'")
            else: conn.execute("UPDATE mmt_occurrence_v1 SET logical_identity_sha256=?", ('0'*64,))
            conn.execute(sql)
        try:
            f.create_reader(admission=f.OwnerAdmissionV1('M02', BRIEF), storage=f.SQLiteReadStorageV1(str(clone)))
        except f.PersistenceFailureV1 as exc:
            assert not exc.outcome_uncertain
            print('PASS independent persisted corruption refusal:', mode)
        else: raise AssertionError('corruption accepted: ' + mode)

def control():
    root = BASE / 'control-copy'
    root.mkdir()
    # Exact source/config/proof candidate, no Worker copying fixture or reseal.
    archive = subprocess.Popen(['git','archive','5a7bcfe252a633ec8d13d9a9e2fbe1709b0ea188'], cwd=SOURCE, stdout=subprocess.PIPE)
    with tarfile.open(fileobj=archive.stdout, mode='r|') as stream:
        stream.extractall(root, filter='data')
    assert archive.wait() == 0
    sys.path.insert(0, str(SOURCE / 'tools'))
    from product_proof_claims import load_product_proof_claim
    names = ('raw_signal_occurrence_truth_sqlite', 'neutral_market_measurement_truth_pilot', 'neutral_market_measurement_truth_d012')
    for name in names:
        claim = load_product_proof_claim(root, name)
        assert claim.state == 'READY_FOR_PROOF'
        print('PASS actual direct loader', name, claim.generation_sha256)
    descriptor = root / 'config/product_proof/market_measurement_d012/claim.json'
    original = descriptor.read_bytes()
    doc = json.loads(original); doc['extra'] = True
    descriptor.write_bytes(encoding(doc))
    for name in names[:2]:
        try: load_product_proof_claim(root, name)
        except ValueError as exc:
            assert 'descriptor' in str(exc)
        else: raise AssertionError('original claim accepted malformed extension')
    descriptor.write_bytes(original)
    print('PASS malformed optional extension rejects both original selected claims')
    # Exercise absence through an explicit move of just disposable copied paths.
    descriptor.rename(BASE / 'saved-control-descriptor.json')
    (root / 'tests/product/market_measurement_d012').rename(BASE / 'saved-control-proof')
    for name in names[:2]: assert load_product_proof_claim(root, name).state == 'READY_FOR_PROOF'
    orphan = root / 'tests/product/market_measurement_d012/nested/helper.py'
    orphan.parent.mkdir(parents=True)
    orphan.write_text('# unowned Python source, absent descriptor\n')
    for name in names[:2]:
        try: load_product_proof_claim(root, name)
        except ValueError as exc:
            assert 'unowned' in str(exc)
        else: raise AssertionError('original claim hid orphan nested support')
    print('PASS descriptor-absent original universe READY, then nested support rejects both original selected claims')

if __name__ == '__main__':
    storage(); control(); print('ALL INDEPENDENT ADVERSARIES PASS')
