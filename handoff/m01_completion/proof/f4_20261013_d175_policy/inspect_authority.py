"""Read-only D175 authority/history census; emits JSON, never alters authority."""

import csv
import hashlib
import json
import subprocess
import tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
AUTH = ROOT / "handoff/m01_completion/authority"
rows = {r["derived_id"]: r for r in csv.DictReader((AUTH / "NVDA_DERIVED_SIGNAL_CATALOGUE.csv").open())}
seen = set()


def visit(did):
    if did in seen:
        return
    seen.add(did)
    for parent in filter(None, rows[did]["derived_dependencies"].split(";")):
        visit(parent)


visit("D175")
raw = sorted({rid for did in seen for rid in rows[did]["raw_dependencies"].split(";") if rid})


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


archive = ROOT.parent / "project_sources/09-NVDA_IMPLEMENTATION_ADMISSION_PM_HANDOVER_FULL_GIT_20260913.tar-1-.gz"
matches = []
scanned = 0
with tarfile.open(archive, "r:gz") as handle:
    for member in handle:
        if not member.isfile() or "/.git/" in member.name or not member.name.endswith((".md", ".csv", ".py", ".json", ".yaml", ".yml")):
            continue
        body = handle.extractfile(member).read().decode("utf-8", errors="replace")
        scanned += 1
        for line, content in enumerate(body.splitlines(), 1):
            if "D175" in content or "active_limits_currency" in content:
                matches.append({"member": member.name, "line": line, "text": content})

out = {
    "base": git("rev-parse", "HEAD"),
    "effective_catalogue_sha256": hashlib.sha256((AUTH / "NVDA_DERIVED_SIGNAL_CATALOGUE.csv").read_bytes()).hexdigest(),
    "direct_row": rows["D175"],
    "closure_including_D175": sorted(seen),
    "closure_raw_ids": raw,
    "closure_rows": {did: rows[did] for did in sorted(seen)},
    "source_history": git("log", "--all", "--format=%H %s", "-G", "D175|CVaR_currency|stress_loss", "--", "src/nvda_desk/derived_signal_calculation_truth/_stage1.py"),
    "authority_history": git("log", "--all", "--format=%H %s", "-G", "D175|capital_limit|liquidity_limit|active_limit", "--", "handoff/m01_completion/authority"),
    "newly_available_admission_archive": {"sha256": hashlib.sha256(archive.read_bytes()).hexdigest(), "text_members_scanned": scanned, "literal_matches": matches, "scope": "active text members only; not Git objects, binary attachments or a complete financial-policy audit"},
}
print(json.dumps(out, indent=2))
