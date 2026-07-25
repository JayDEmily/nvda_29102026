"""Deterministic vocabulary synonym-candidate audit.

Canonical labels and lawful aliases are recognised globally.  A human disposition
of a noncanonical phrase applies only to the exact evidenced occurrence: path,
line, normalised phrase, and unchanged source-line context hash.  A new path,
new line occurrence, or changed context is escalated again.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from pathlib import Path
from typing import Iterator

from nvda_desk.schemas.vocabulary import (
    VocabularyCandidate,
    VocabularyCandidateAction,
    VocabularyCandidateClassification,
    vocabulary_document_from_dict,
)
from nvda_desk.vocabulary_builder import build_canonical_payload, governed_source_hashes

OUTPUT_PATH = Path("var/vocabulary/synonym_candidates.json")
STAMP_PATH = Path("data/vocabulary/vocabulary_touch_stamp.json")
RESOLVED_OCCURRENCES_PATH = Path(
    "project_control/canonical_project_manager/units/PM-010/"
    "P1_CANDIDATE_SEMANTIC_DISPOSITION_REGISTER.tsv"
)
SCAN_PATHS = [Path("src"), Path("tests"), Path("docs"), Path("config")]
ALLOWED_EXTENSIONS = {".py", ".md", ".yaml", ".yml", ".json", ".toml"}
IDENTIFIER_PATTERN = re.compile(r"\b[A-Za-z][A-Za-z0-9]*(?:[_-][A-Za-z0-9]+)+\b")
MARKDOWN_HEADING_PATTERN = re.compile(r"^#{1,6}\s+(.+?)\s*$")
INLINE_CODE_PATTERN = re.compile(r"`([^`\n]{2,80})`")
QUOTED_LABEL_PATTERN = re.compile(r"[\"']([^\"'\n]{2,80})[\"']")


def _normalise(value: str) -> str:
    return re.sub(r"[_\-\s]+", " ", value.strip().casefold())


def _compact_normalise(value: str) -> str:
    return re.sub(r"[_\-\s]+", "", value.strip().casefold())


def _context_hash(source_context: str) -> str:
    return hashlib.sha256(source_context.encode("utf-8")).hexdigest()


def _fingerprint() -> str:
    items = governed_source_hashes()
    if RESOLVED_OCCURRENCES_PATH.exists():
        items[str(RESOLVED_OCCURRENCES_PATH)] = hashlib.sha256(
            RESOLVED_OCCURRENCES_PATH.read_bytes()
        ).hexdigest()
    blob = json.dumps(items, sort_keys=True).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()


def _load_document() -> dict:
    payload = build_canonical_payload()
    vocabulary_document_from_dict(payload)
    return payload


def _lexicon(payload: dict) -> tuple[set[str], set[str], list[tuple[str, str, str, str]]]:
    """Return canonical/alias exact tokens only.

    Disallowed and other noncanonical phrases are deliberately excluded.  Their
    treatment is occurrence-specific and comes from the disposition register.
    """

    exact_tokens: set[str] = set()
    compact_exact_tokens: set[str] = set()
    entries: list[tuple[str, str, str, str]] = []
    for entry in payload["entries"]:
        label = entry["canonical_label"]
        slug = entry["canonical_slug"]
        canonical_norm = _normalise(label)
        for token in [label, slug, *entry.get("allowed_aliases", [])]:
            exact_tokens.add(_normalise(token))
            compact_exact_tokens.add(_compact_normalise(token))
        entries.append((slug, label, canonical_norm, entry.get("category", "")))
    return exact_tokens, compact_exact_tokens, entries


def _looks_like_bounded_label(value: str) -> bool:
    stripped = value.strip()
    if not stripped or len(stripped) > 80:
        return False
    if "\n" in stripped or stripped.endswith((".", ":", ";")):
        return False
    words = stripped.split()
    return 1 <= len(words) <= 8


def _occurrence(
    *,
    path: Path,
    raw_phrase: str,
    line_number: int,
    column_start: int,
    source_context: str,
    occurrence_kind: str,
) -> dict[str, str | int]:
    context_sha256 = _context_hash(source_context)
    normalised_phrase = _normalise(raw_phrase)
    identity_blob = "\0".join(
        [str(path), str(line_number), str(column_start), normalised_phrase, context_sha256]
    ).encode("utf-8")
    return {
        "occurrence_id": "VOC-OCC-" + hashlib.sha256(identity_blob).hexdigest()[:16],
        "path": str(path),
        "raw_phrase": raw_phrase,
        "line": line_number,
        "column": column_start + 1,
        "source_context": source_context,
        "context_sha256": context_sha256,
        "occurrence_kind": occurrence_kind,
    }


def _iter_candidates() -> Iterator[dict[str, str | int]]:
    """Yield explicit label occurrences with stable path/line/context evidence."""

    for base in SCAN_PATHS:
        if not base.exists():
            continue
        for path in sorted(base.rglob("*")):
            if not path.is_file() or path.suffix not in ALLOWED_EXTENSIONS:
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            lines = text.splitlines()
            line_offsets: list[int] = []
            offset = 0
            for line in text.splitlines(keepends=True):
                line_offsets.append(offset)
                offset += len(line)
            if text and (not line_offsets or len(line_offsets) < len(lines)):
                line_offsets.append(offset)

            emitted: set[tuple[int, int, str]] = set()

            for match in IDENTIFIER_PATTERN.finditer(text):
                line_number = text.count("\n", 0, match.start()) + 1
                line_index = line_number - 1
                source_context = lines[line_index] if line_index < len(lines) else ""
                if source_context.startswith(("Projection metadata:", "Projection document notes:")):
                    continue
                line_start = text.rfind("\n", 0, match.start()) + 1
                column_start = match.start() - line_start
                raw = match.group(0)
                if path.suffix == ".py":
                    prefix = text[line_start : match.start()]
                    if re.search(r"\bdef\s+$", prefix):
                        raw = "def " + raw
                key = (line_number, column_start, _normalise(raw))
                if key not in emitted:
                    emitted.add(key)
                    yield _occurrence(
                        path=path,
                        raw_phrase=raw,
                        line_number=line_number,
                        column_start=column_start,
                        source_context=source_context,
                        occurrence_kind="identifier",
                    )

            for line_number, line in enumerate(lines, start=1):
                if line.startswith(("Projection metadata:", "Projection document notes:")):
                    continue
                if path.suffix == ".md":
                    heading = MARKDOWN_HEADING_PATTERN.match(line)
                    if heading and _looks_like_bounded_label(heading.group(1)):
                        raw = heading.group(1)
                        column_start = heading.start(1)
                        key = (line_number, column_start, _normalise(raw))
                        if key not in emitted:
                            emitted.add(key)
                            yield _occurrence(
                                path=path,
                                raw_phrase=raw,
                                line_number=line_number,
                                column_start=column_start,
                                source_context=line,
                                occurrence_kind="markdown_heading",
                            )
                    for match in INLINE_CODE_PATTERN.finditer(line):
                        raw = match.group(1)
                        if _looks_like_bounded_label(raw):
                            key = (line_number, match.start(1), _normalise(raw))
                            if key not in emitted:
                                emitted.add(key)
                                yield _occurrence(
                                    path=path,
                                    raw_phrase=raw,
                                    line_number=line_number,
                                    column_start=match.start(1),
                                    source_context=line,
                                    occurrence_kind="inline_code",
                                )
                if path.suffix in {".json", ".yaml", ".yml", ".toml", ".py"}:
                    for match in QUOTED_LABEL_PATTERN.finditer(line):
                        raw = match.group(1)
                        if _looks_like_bounded_label(raw):
                            key = (line_number, match.start(1), _normalise(raw))
                            if key not in emitted:
                                emitted.add(key)
                                yield _occurrence(
                                    path=path,
                                    raw_phrase=raw,
                                    line_number=line_number,
                                    column_start=match.start(1),
                                    source_context=line,
                                    occurrence_kind="quoted_label",
                                )


def _is_identifier_like(raw_phrase: str) -> bool:
    return (
        " " not in raw_phrase
        and "_" not in raw_phrase
        and "-" not in raw_phrase
        and raw_phrase != raw_phrase.lower()
    )


def _is_protocol_identifier_fragment(
    raw_phrase: str,
    candidate: str,
    target: str,
    category: str,
) -> bool:
    if category != "protocol_field" or "_" not in raw_phrase:
        return False
    candidate_parts = candidate.split()
    target_parts = target.split()
    if not set(target_parts) <= set(candidate_parts):
        return False
    extra_parts = set(candidate_parts) - set(target_parts)
    return len(extra_parts) <= 1


def _is_python_function_declaration_identifier_fragment(
    path: str,
    raw_phrase: str,
    candidate: str,
    target: str,
) -> bool:
    if not path.endswith(".py") or "_" not in raw_phrase:
        return False
    if not raw_phrase.lstrip().startswith("def "):
        return False
    candidate_parts = candidate.split()
    target_parts = target.split()
    if candidate_parts[:1] != ["def"]:
        return False
    return candidate_parts[1:] == target_parts


def _candidate_slug_from_phrase(phrase: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "_", phrase.strip().casefold()).strip("_")
    if not slug:
        raise ValueError("candidate phrase must yield a non-empty slug")
    return slug


def _escalation_classification(phrase: str, nearest_slug: str) -> dict[str, str | None]:
    return VocabularyCandidateClassification(
        action=VocabularyCandidateAction.QUARANTINE,
        candidate_slug=_candidate_slug_from_phrase(phrase),
        matched_slug=nearest_slug,
        reason="near-match synonym candidate requires LLM escalation before vocabulary admission",
    ).to_dict()


def _escalation_admission_review(phrase: str, nearest_slug: str) -> dict:
    candidate = VocabularyCandidate(
        candidate_slug=_candidate_slug_from_phrase(phrase),
        candidate_label=phrase,
    )
    classification = VocabularyCandidateClassification(
        action=VocabularyCandidateAction.QUARANTINE,
        candidate_slug=candidate.candidate_slug,
        matched_slug=nearest_slug,
        reason="near-match synonym candidate requires LLM escalation before vocabulary admission",
    )
    return {
        "status": "quarantined",
        "candidate_slug": candidate.candidate_slug,
        "plan": {
            "classification": classification.to_dict(),
            "proposed_entry": None,
            "alias_candidates": [],
            "quarantine_reason": classification.reason,
        },
        "error": classification.reason,
    }


def _candidate_score(candidate: str, target: str) -> int:
    c_parts = candidate.split()
    t_parts = target.split()
    if candidate == target:
        return 100
    if candidate.replace(" ", "") == target.replace(" ", ""):
        return 98
    if len(c_parts) == len(t_parts) and set(c_parts) == set(t_parts):
        return 95
    if abs(len(c_parts) - len(t_parts)) == 1:
        smaller = set(c_parts) if len(c_parts) < len(t_parts) else set(t_parts)
        larger = set(c_parts) if len(c_parts) > len(t_parts) else set(t_parts)
        if smaller <= larger and len(smaller) >= 2:
            return 93
    return 0


def _resolved_occurrence_keys() -> set[tuple[str, int, int, str, str]]:
    if not RESOLVED_OCCURRENCES_PATH.exists():
        return set()
    keys: set[tuple[str, int, int, str, str]] = set()
    with RESOLVED_OCCURRENCES_PATH.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        required = {
            "path",
            "line",
            "column",
            "phrase",
            "context_sha256",
            "audit_resolution_effect",
        }
        if reader.fieldnames is None or not required <= set(reader.fieldnames):
            return set()
        for row in reader:
            if row["audit_resolution_effect"] != "suppress_same_occurrence_only":
                continue
            try:
                line = int(row["line"])
                column = int(row["column"])
            except ValueError:
                continue
            keys.add((row["path"], line, column, _normalise(row["phrase"]), row["context_sha256"]))
    return keys


def build_report() -> dict:
    payload = _load_document()
    exact_tokens, compact_exact_tokens, entries = _lexicon(payload)
    resolved_keys = _resolved_occurrence_keys()
    fingerprint = _fingerprint()
    previous_stamp = {}
    if STAMP_PATH.exists():
        previous_stamp = json.loads(STAMP_PATH.read_text(encoding="utf-8"))
    current_touched = previous_stamp.get("fingerprint") != fingerprint

    candidates: list[dict] = []
    for occurrence in _iter_candidates():
        raw_phrase = str(occurrence["raw_phrase"])
        if _is_identifier_like(raw_phrase):
            continue
        phrase = _normalise(raw_phrase)
        compact_phrase = _compact_normalise(raw_phrase)
        if len(phrase) < 8 or phrase in exact_tokens or compact_phrase in compact_exact_tokens:
            continue
        best = None
        best_score = 0
        for slug, label, target, category in entries:
            score = _candidate_score(phrase, target)
            if score:
                if _is_protocol_identifier_fragment(raw_phrase, phrase, target, category):
                    score = 0
                if _is_python_function_declaration_identifier_fragment(
                    str(occurrence["path"]), raw_phrase, phrase, target
                ):
                    score = 0
            if score > best_score:
                best = (slug, label)
                best_score = score
        if best is None or best_score < 93:
            continue
        resolved_key = (
            str(occurrence["path"]),
            int(occurrence["line"]),
            int(occurrence["column"]),
            phrase,
            str(occurrence["context_sha256"]),
        )
        if resolved_key in resolved_keys:
            continue
        candidates.append(
            {
                "occurrence_id": occurrence["occurrence_id"],
                "phrase": phrase,
                "raw_phrase": raw_phrase,
                "nearest_slug": best[0],
                "nearest_label": best[1],
                "score": best_score,
                "path": occurrence["path"],
                "line": occurrence["line"],
                "column": occurrence["column"],
                "source_context": occurrence["source_context"],
                "context_sha256": occurrence["context_sha256"],
                "occurrence_kind": occurrence["occurrence_kind"],
                "resolution_required": "llm_escalation",
            }
        )

    sorted_candidates = sorted(
        candidates,
        key=lambda item: (
            -item["score"],
            item["path"],
            item["line"],
            item["column"],
            item["phrase"],
        ),
    )
    return {
        "schema_version": "v2_occurrence_scoped",
        "trigger": "vocabulary_governance",
        "vocabulary_touched": current_touched,
        "fingerprint": fingerprint,
        "resolved_occurrence_count": len(resolved_keys),
        "candidates": sorted_candidates,
        "candidate_classifications": [
            {
                "occurrence_id": item["occurrence_id"],
                "phrase": item["phrase"],
                "path": item["path"],
                "line": item["line"],
                "context_sha256": item["context_sha256"],
                "nearest_slug": item["nearest_slug"],
                "classification": _escalation_classification(
                    str(item["phrase"]), str(item["nearest_slug"])
                ),
                "admission_review": _escalation_admission_review(
                    str(item["phrase"]), str(item["nearest_slug"])
                ),
            }
            for item in sorted_candidates
        ],
    }


def write_report() -> dict:
    report = build_report()
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return report


def write_stamp() -> None:
    report = build_report()
    if report["candidates"]:
        raise RuntimeError(
            "cannot update vocabulary touch stamp while synonym candidates require LLM escalation"
        )
    STAMP_PATH.parent.mkdir(parents=True, exist_ok=True)
    STAMP_PATH.write_text(
        json.dumps({"fingerprint": report["fingerprint"]}, indent=2) + "\n",
        encoding="utf-8",
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check-clean",
        action="store_true",
        help="write the audit report and fail if unresolved synonym candidates exist",
    )
    parser.add_argument(
        "--write-stamp",
        action="store_true",
        help="advance the vocabulary touch stamp only when the audit is clean",
    )
    args = parser.parse_args(argv)

    if args.write_stamp:
        write_stamp()
        print("vocabulary_touch_stamp=UPDATED")
        return 0

    report = build_report() if args.check_clean else write_report()
    candidate_count = len(report["candidates"])
    print(
        "vocabulary_synonym_audit=PASS"
        f" candidates={candidate_count}"
        f" vocabulary_touched={report['vocabulary_touched']}"
        f" resolved_occurrences={report['resolved_occurrence_count']}"
    )
    if args.check_clean and candidate_count:
        print("vocabulary_synonym_audit=BLOCKED unresolved_candidates=" + str(candidate_count))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
