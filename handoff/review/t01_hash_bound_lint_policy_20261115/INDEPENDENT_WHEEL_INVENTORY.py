#!/usr/bin/env python3
"""Read-only inspection of PR14's four newly vendored binary wheels."""
from __future__ import annotations
import argparse
import base64
import csv
import hashlib
import io
import json
from pathlib import Path
import subprocess
import tomllib
import zipfile

BASE = "ded4b98e1e5999d1ddf2f067e660b691917bcd71"
HEAD = "831471d69afd092779a6810ee570285182be88a8"


def main() -> None:
    p=argparse.ArgumentParser()
    p.add_argument("--candidate", type=Path, required=True)
    a=p.parse_args()
    root=a.candidate.resolve()
    assert subprocess.check_output(["git","rev-parse","HEAD"],cwd=root,text=True).strip()==HEAD
    changed=subprocess.check_output(
        ["git","diff","--name-only",BASE,HEAD,"--","vendor/wheels"],cwd=root,text=True
    ).splitlines()
    assert len(changed)==4,changed
    lock=tomllib.loads((root/"uv.lock").read_text())
    assert lock["requires-python"]=="==3.13.5"
    lock_paths=[row["path"] for pkg in lock["package"] for row in pkg.get("wheels",[])]
    inventory=[]
    for rel in changed:
        wheel=root/rel
        raw=wheel.read_bytes()
        assert wheel.name in lock_paths
        with zipfile.ZipFile(io.BytesIO(raw)) as archive:
            assert archive.testzip() is None
            names=set(archive.namelist())
            rec_files=[x for x in names if x.endswith(".dist-info/RECORD")]
            assert len(rec_files)==1
            record_rows=list(csv.reader(io.StringIO(archive.read(rec_files[0]).decode())))
            counts={"sha256_record_verified":0,"unhashed_record_rows":0}
            for row in record_rows:
                assert len(row)==3
                name,h,size=row
                assert name in names, name
                value=archive.read(name)
                if size:assert len(value)==int(size)
                if h:
                    method,digest=h.split("=",1)
                    assert method=="sha256", (rel,method)
                    expected=base64.urlsafe_b64encode(hashlib.sha256(value).digest()).rstrip(b"=").decode()
                    assert digest==expected, (rel,name)
                    counts["sha256_record_verified"]+=1
                else:
                    counts["unhashed_record_rows"]+=1
            assert counts["sha256_record_verified"]>0
            meta=[x for x in names if x.endswith(".dist-info/METADATA")]
            assert len(meta)==1
            text=archive.read(meta[0]).decode("utf-8")
            distro=next(line.partition(": ")[2] for line in text.splitlines() if line.startswith("Name: "))
            version=next(line.partition(": ")[2] for line in text.splitlines() if line.startswith("Version: "))
        inventory.append({"path":rel,"sha256":hashlib.sha256(raw).hexdigest(),
                          "size_bytes":len(raw),"distribution":distro,"version":version,
                          **counts,"archive_crc_pass":True})
    print(json.dumps({"status":"PASS_ARCHIVE_AND_RECORD_INTEGRITY",
      "candidate":HEAD,"changed_wheels":len(inventory),
      "lock_registry":"vendor/wheels","uv_lock_contains_individual_wheel_sha256":False,
      "third_party_publisher_provenance_verified":False,
      "product_tests_executed":False,"wheels":inventory},indent=2))


if __name__=="__main__":
    main()
