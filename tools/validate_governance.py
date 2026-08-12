from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


class GovernanceError(RuntimeError):
    pass


ACCEPTED_DISPOSITIONS = {"ACCEPTED", "GATE0_PASS"}
KNOWN_ROLES = {
    "project_manager",
    "integration_auditor",
    "semantic_worker",
    "semantic_reviewer",
    "normative_writer",
    "test_author",
    "implementation_worker",
}
PROOF_CLASSES = {"MECHANICAL", "SEMANTIC", "BOTH"}


def canonical_sha(record: dict[str, Any]) -> str:
    payload = json.dumps(record, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def _require(record: dict[str, Any], fields: set[str], label: str) -> None:
    missing = sorted(fields - record.keys())
    if missing:
        raise GovernanceError(f"{label} missing required fields: {', '.join(missing)}")


def _candidate_binding(record: dict[str, Any], label: str) -> tuple[str | None, str | None]:
    commit = record.get("candidate_commit")
    digest = record.get("candidate_sha256")
    if not commit and not digest:
        raise GovernanceError(f"{label} has no candidate commit or content hash")
    return commit, digest


def _is_accepted(record: dict[str, Any]) -> bool:
    return record.get("disposition") in ACCEPTED_DISPOSITIONS


def accepted_semantic_index_entries(index: dict[str, Any]) -> dict[str, dict[str, Any]]:
    if index.get("status") != "ACCEPTED" or not index.get("admission_id"):
        raise GovernanceError("semantic index is not accepted")
    entries = index.get("entries")
    if not isinstance(entries, list):
        raise GovernanceError("semantic index entries are malformed")
    result: dict[str, dict[str, Any]] = {}
    for entry in entries:
        entry_id = entry.get("entry_id")
        if not entry_id or entry_id in result:
            raise GovernanceError("semantic index has missing or duplicate entry ID")
        if not entry.get("authority_refs"):
            raise GovernanceError(f"semantic index entry {entry_id} has no source authority")
        result[entry_id] = entry
    for entry_id, entry in result.items():
        for dependency in entry.get("dependencies", []):
            if dependency not in result:
                raise GovernanceError(
                    f"semantic index entry {entry_id} has unknown dependency {dependency}"
                )
    return result


def validate_work_order(
    work_order: dict[str, Any],
    admissions: dict[str, dict[str, Any]],
    *,
    accepted_base_commit: str,
) -> None:
    _require(
        work_order,
        {
            "work_order_id",
            "gate",
            "stage",
            "proposition_id",
            "authority_ref",
            "authority_status",
            "accepted_base_commit",
            "commissioned_role",
            "allowed_mutations",
            "proof_class",
            "falsifier",
            "pass_means",
            "pass_does_not_mean",
            "dependencies",
            "stop_conditions",
        },
        "work order",
    )
    if work_order["authority_status"] != "GOVERNED":
        raise GovernanceError("executable work order authority_status must be GOVERNED")
    if work_order["accepted_base_commit"] != accepted_base_commit:
        raise GovernanceError("work order accepted base does not match admitted Git base")
    if work_order["commissioned_role"] not in KNOWN_ROLES:
        raise GovernanceError("work order commissioned role is unknown")
    if work_order["proof_class"] not in PROOF_CLASSES:
        raise GovernanceError("work order proof class is invalid")
    if not work_order["stop_conditions"]:
        raise GovernanceError("work order requires an explicit stop condition")
    if work_order["pass_means"] == work_order["pass_does_not_mean"]:
        raise GovernanceError("work order PASS boundary is not discriminating")

    authority_ref = work_order["authority_ref"]
    authority_id = authority_ref.get("admission_id")
    authority = admissions.get(authority_id)
    if not authority or not _is_accepted(authority):
        raise GovernanceError("work order does not reference an accepted authority admission")
    if canonical_sha(authority) != authority_ref.get("sha256"):
        raise GovernanceError("work order authority hash does not bind the admitted record")
    if authority.get("proposition_id") != work_order["proposition_id"]:
        raise GovernanceError("work order proposition is not the admitted authority proposition")

    for dependency_id in work_order["dependencies"]:
        dependency = admissions.get(dependency_id)
        if not dependency or not _is_accepted(dependency):
            raise GovernanceError(f"work order dependency is not admitted: {dependency_id}")


def validate_attempt(work_order: dict[str, Any], attempt: dict[str, Any]) -> None:
    _require(
        attempt,
        {
            "attempt_id",
            "work_order_id",
            "actor_id",
            "actor_role",
            "actor_thread_id",
            "accepted_base_commit",
            "candidate_commit",
            "candidate_sha256",
            "actual_changed_paths",
            "proof_results",
        },
        "attempt",
    )
    if attempt["work_order_id"] != work_order["work_order_id"]:
        raise GovernanceError("attempt work order mismatch")
    if attempt["actor_role"] != work_order["commissioned_role"]:
        raise GovernanceError("attempt actor role does not match commissioned role")
    if attempt["accepted_base_commit"] != work_order["accepted_base_commit"]:
        raise GovernanceError("attempt accepted base mismatch")
    _candidate_binding(attempt, "attempt")
    unexpected = set(attempt["actual_changed_paths"]) - set(work_order["allowed_mutations"])
    if unexpected:
        raise GovernanceError(f"attempt changed paths outside authority: {sorted(unexpected)}")


def validate_review(
    work_order: dict[str, Any], attempt: dict[str, Any], review: dict[str, Any]
) -> None:
    _require(
        review,
        {
            "review_id",
            "work_order_id",
            "attempt_id",
            "reviewer_id",
            "reviewer_thread_id",
            "candidate_commit",
            "candidate_sha256",
            "authority_ref",
            "authority_re_read",
            "legitimacy",
            "proof_quality",
            "falsification_evidence",
            "limitations",
        },
        "review",
    )
    if review["work_order_id"] != work_order["work_order_id"]:
        raise GovernanceError("review work order mismatch")
    if review["attempt_id"] != attempt["attempt_id"]:
        raise GovernanceError("review attempt mismatch")
    if review["reviewer_id"] == attempt["actor_id"]:
        raise GovernanceError("reviewer identity is not independent from worker")
    if review["reviewer_thread_id"] == attempt["actor_thread_id"]:
        raise GovernanceError("reviewer thread is not independent from worker")
    if review["authority_re_read"] is not True:
        raise GovernanceError("review does not record independent authority re-read")
    if review["authority_ref"] != work_order["authority_ref"]:
        raise GovernanceError("review authority reference does not match work order")
    if _candidate_binding(review, "review") != _candidate_binding(attempt, "attempt"):
        raise GovernanceError("review candidate binding does not match attempt candidate")
    if not review["falsification_evidence"]:
        raise GovernanceError("review contains no falsification evidence")


def validate_admission(
    work_order: dict[str, Any],
    attempt: dict[str, Any],
    review: dict[str, Any],
    admission: dict[str, Any],
) -> None:
    validate_attempt(work_order, attempt)
    validate_review(work_order, attempt, review)
    _require(
        admission,
        {
            "admission_id",
            "record_type",
            "disposition",
            "proposition_id",
            "authority_ref",
            "work_order_id",
            "attempt_id",
            "review_id",
            "accepted_base_commit",
            "candidate_commit",
            "candidate_sha256",
            "admitted_at_utc",
        },
        "admission",
    )
    if admission["record_type"] != "SEMANTIC_RESULT":
        raise GovernanceError("semantic transaction has wrong admission record type")
    if admission["work_order_id"] != work_order["work_order_id"]:
        raise GovernanceError("admission work order mismatch")
    if admission["attempt_id"] != attempt["attempt_id"]:
        raise GovernanceError("admission attempt mismatch")
    if admission["review_id"] != review["review_id"]:
        raise GovernanceError("admission review mismatch")
    if admission["proposition_id"] != work_order["proposition_id"]:
        raise GovernanceError("admission proposition mismatch")
    if admission["authority_ref"] != work_order["authority_ref"]:
        raise GovernanceError("admission authority mismatch")
    if admission["accepted_base_commit"] != work_order["accepted_base_commit"]:
        raise GovernanceError("admission accepted base mismatch")
    if _candidate_binding(admission, "admission") != _candidate_binding(attempt, "attempt"):
        raise GovernanceError("admission candidate binding does not match attempt candidate")
    if admission["disposition"] == "ACCEPTED":
        if review["legitimacy"] != "AUTHORISED":
            raise GovernanceError("admission cannot overcome review legitimacy rejection")
        if review["proof_quality"] != "PROVEN":
            raise GovernanceError("admission cannot overcome unproven proof quality")


def advance_state_after_admission(
    state: dict[str, Any], admission: dict[str, Any]
) -> dict[str, Any]:
    if not _is_accepted(admission):
        raise GovernanceError("rejected record cannot advance admitted state")
    updated = dict(state)
    updated["latest_admission_id"] = admission["admission_id"]
    if admission.get("record_type") == "SEMANTIC_RESULT" and admission.get("candidate_commit"):
        updated["candidate_control_commit"] = admission["candidate_commit"]
    updated["current_work_order"] = None
    updated["current_attempt"] = None
    updated["first_blocker"] = None
    return updated


def validate_admitted_state_binding(
    state: dict[str, Any],
    *,
    current_git_parent: str,
    admissions: dict[str, dict[str, Any]],
) -> None:
    latest_id = state.get("latest_admission_id")
    if not latest_id:
        raise GovernanceError("ADMITTED_STATE has no latest admission ID")
    latest = admissions.get(latest_id)
    if not latest or not _is_accepted(latest):
        raise GovernanceError("ADMITTED_STATE latest admission is absent or not accepted")
    admitted_candidate = state.get("candidate_control_commit")
    if admitted_candidate != current_git_parent:
        raise GovernanceError(
            "ADMITTED_STATE admitted candidate disagrees with Git admission-control parent"
        )
    if state.get("operational_status") == "GATE0_PASS":
        if latest.get("disposition") != "GATE0_PASS":
            raise GovernanceError("GATE0_PASS state does not bind a Gate 0 admission")
        if latest.get("proven_commit") != admitted_candidate:
            raise GovernanceError(
                "Gate 0 admission proven commit disagrees with admitted candidate"
            )
        if state.get("gate0_proven_commit") != admitted_candidate:
            raise GovernanceError(
                "ADMITTED_STATE Gate 0 proven commit disagrees with admitted candidate"
            )
    elif latest.get("record_type") == "SEMANTIC_RESULT":
        if latest.get("candidate_commit") != admitted_candidate:
            raise GovernanceError("semantic admission candidate disagrees with admitted candidate")


def _repo_root() -> Path:
    out = subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True)
    return Path(out.strip()).resolve()


def validate_repository_static(root: Path) -> None:
    for rel in [
        "schemas/semantic_index.schema.json",
        "schemas/work_order.schema.json",
        "schemas/attempt_record.schema.json",
        "schemas/review.schema.json",
        "schemas/admission_record.schema.json",
        "schemas/admitted_state.schema.json",
        "docs/governance/SEMANTIC_INDEX.json",
        "docs/governance/ADMITTED_STATE.json",
    ]:
        data = json.loads((root / rel).read_text())
        if not isinstance(data, dict):
            raise GovernanceError(f"governance JSON is not an object: {rel}")
    index = json.loads((root / "docs/governance/SEMANTIC_INDEX.json").read_text())
    if index.get("status") == "PENDING":
        if index.get("admission_id") is not None or index.get("entries") != []:
            raise GovernanceError("pending semantic index must be empty and unadmitted")
    elif index.get("status") == "ACCEPTED":
        accepted_semantic_index_entries(index)
    else:
        raise GovernanceError("semantic index has invalid status")

    state = json.loads((root / "docs/governance/ADMITTED_STATE.json").read_text())
    if state.get("operational_status") == "CANDIDATE_FOR_INDEPENDENT_AUDIT":
        if state.get("current_work_order") is not None or state.get("current_attempt") is not None:
            raise GovernanceError("construction candidate cannot claim active admitted work")
        if state.get("latest_admission_id") is not None:
            raise GovernanceError("construction candidate cannot claim a latest admission")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--static", action="store_true", required=True)
    args = parser.parse_args(argv)
    del args
    try:
        validate_repository_static(_repo_root())
        print("PASS: Gate 1+ governance substrate validation")
        return 0
    except (GovernanceError, OSError, ValueError, KeyError, subprocess.CalledProcessError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
