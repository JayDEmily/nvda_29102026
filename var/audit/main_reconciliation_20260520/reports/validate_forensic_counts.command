python3 - <<"PY"
import json, collections
from pathlib import Path
records=json.loads(Path("var/audit/atlas_source_code_forensic_20260520/NVDA10_ATLAS_SOURCE_CODE_FORENSIC_PER_ID_V2.json").read_text())["records"]
counts=collections.Counter(r.get("classification") for r in records)
assert len(records)==1716, len(records)
assert counts["mapped_existing_in_source_code"]==508, counts
assert counts["mapped_added_to_source_code"]==80, counts
assert counts["mapped_not_migrated"]==1128, counts
print("records=1716")
print(dict(counts))
PY
