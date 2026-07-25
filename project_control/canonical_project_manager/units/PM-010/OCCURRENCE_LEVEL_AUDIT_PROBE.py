from __future__ import annotations

import csv
import tempfile
from pathlib import Path

import nvda_desk.vocabulary_synonym_audit as audit

REGISTER = Path(
    "project_control/canonical_project_manager/units/PM-010/"
    "P1_CANDIDATE_SEMANTIC_DISPOSITION_REGISTER.tsv"
)


def main() -> int:
    with REGISTER.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    prior = next(row for row in rows if row["phrase"] == "field level")

    with tempfile.TemporaryDirectory(prefix="vocabulary_occurrence_probe_") as temp:
        probe_root = Path(temp)
        probe_path = probe_root / "new_normative_occurrence.md"
        # Same phrase and unchanged source-line context as an already dispositioned
        # occurrence, but at a new path.  Phrase-global suppression would hide it.
        probe_path.write_text(prior["source_context"] + "\n", encoding="utf-8")

        original_scan_paths = audit.SCAN_PATHS
        try:
            audit.SCAN_PATHS = [probe_root]
            report = audit.build_report()
        finally:
            audit.SCAN_PATHS = original_scan_paths

        matches = [
            item
            for item in report["candidates"]
            if item["path"] == str(probe_path) and item["phrase"] == prior["phrase"]
        ]
        if not matches:
            raise AssertionError(
                "new path occurrence of a previously dispositioned phrase was suppressed"
            )
        candidate = matches[0]
        if candidate["context_sha256"] != prior["context_sha256"]:
            raise AssertionError("probe did not preserve the dispositioned source context")
        if candidate["line"] != 1:
            raise AssertionError("probe candidate line is not the introduced occurrence")

        print("occurrence_level_audit_probe=PASS")
        print(f"previously_dispositioned_phrase={prior['phrase']}")
        print(f"previous_occurrence={prior['path']}:{prior['line']}:{prior['column']}")
        print(f"new_occurrence={candidate['path']}:{candidate['line']}:{candidate['column']}")
        print(f"unchanged_context_sha256={candidate['context_sha256']}")
        print("new_occurrence_reported=true")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
