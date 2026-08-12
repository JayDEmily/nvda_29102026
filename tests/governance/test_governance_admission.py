from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
VALIDATOR = ROOT / "tools/validate_governance.py"


def load_validator():
    assert VALIDATOR.is_file(), "Unit 5 seam: tools/validate_governance.py is not implemented yet"
    spec = importlib.util.spec_from_file_location("validate_governance", VALIDATOR)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def git_repo(tmp_path: Path) -> tuple[Path, str, str]:
    repo = tmp_path / "repo"
    repo.mkdir()
    subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
    subprocess.run(["git", "config", "user.email", "audit@example.invalid"], cwd=repo, check=True)
    subprocess.run(["git", "config", "user.name", "Audit Test"], cwd=repo, check=True)
    (repo / "base.txt").write_text("base\n")
    subprocess.run(["git", "add", "base.txt"], cwd=repo, check=True)
    subprocess.run(["git", "commit", "-qm", "base"], cwd=repo, check=True)
    base = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=repo, text=True).strip()
    (repo / "docs").mkdir()
    (repo / "docs/example.md").write_text("candidate\n")
    subprocess.run(["git", "add", "docs/example.md"], cwd=repo, check=True)
    subprocess.run(["git", "commit", "-qm", "candidate"], cwd=repo, check=True)
    candidate = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=repo, text=True).strip()
    runtime_dir = repo / ".git/nvda_runtime_identity"
    runtime_dir.mkdir(parents=True)
    receipts = [worker_runtime_receipt(), reviewer_runtime_receipt()]
    (runtime_dir / "receipts.jsonl").write_text(
        "".join(json.dumps(item, sort_keys=True, separators=(",", ":")) + "\n" for item in receipts)
    )
    return repo, base, candidate


def semantic_index_repo(tmp_path: Path) -> tuple[Path, dict, dict]:
    repo = tmp_path / "index-repo"
    repo.mkdir()
    subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
    subprocess.run(["git", "config", "user.email", "audit@example.invalid"], cwd=repo, check=True)
    subprocess.run(["git", "config", "user.name", "Audit Test"], cwd=repo, check=True)
    (repo / "authority/source").mkdir(parents=True)
    source = repo / "authority/source/source.md"
    source.write_text("authoritative source\n")
    source_sha = hashlib.sha256(source.read_bytes()).hexdigest()
    (repo / "authority/AUTHORITY_MANIFEST.md").write_text(
        "# Authority\n\n| Artefact | Role | SHA-256 |\n|---|---|---|\n"
        f"| `authority/source/source.md` | Source | `{source_sha}` |\n"
    )
    subprocess.run(["git", "add", "."], cwd=repo, check=True)
    subprocess.run(["git", "commit", "-qm", "authority"], cwd=repo, check=True)
    base = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=repo, text=True).strip()
    (repo / "docs/governance").mkdir(parents=True)
    index = {
        "schema_version": "1.0.0",
        "status": "ACCEPTED",
        "admission_id": "ADM-INDEX-001",
        "note": "accepted",
        "entries": [
            {
                "entry_id": "IDX-1",
                "proposition": "Bound source proposition",
                "authority_refs": [{"path": "authority/source/source.md", "sha256": source_sha}],
                "dependencies": [],
            }
        ],
    }
    (repo / "docs/governance/SEMANTIC_INDEX.json").write_text(
        json.dumps(index, indent=2, sort_keys=True) + "\n"
    )
    subprocess.run(["git", "add", "."], cwd=repo, check=True)
    subprocess.run(["git", "commit", "-qm", "semantic index"], cwd=repo, check=True)
    candidate = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=repo, text=True).strip()
    admission_record = {
        "schema_version": "1.0.0",
        "admission_id": "ADM-INDEX-001",
        "record_type": "SEMANTIC_RESULT",
        "disposition": "ACCEPTED",
        "proposition_id": "RAW_SIGNAL_SEMANTIC_INDEX_V1",
        "authority_ref": {"admission_id": "AUTH-INDEX", "sha256": "a" * 64},
        "work_order_id": "WO-INDEX",
        "attempt_id": "ATT-INDEX",
        "review_id": "REV-INDEX",
        "accepted_base_commit": base,
        "candidate_commit": candidate,
        "candidate_sha256": None,
        "artifact_path": "docs/governance/SEMANTIC_INDEX.json",
        "artifact_sha256": canonical_sha(index),
        "admitted_at_utc": "2026-08-12T00:00:00Z",
    }
    return repo, index, admission_record


def canonical_sha(record: dict) -> str:
    payload = json.dumps(record, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def runtime_receipt(
    *, receipt_id: str, agent_id: str, role: str, transcript: str, turn_id: str
) -> dict:
    return {
        "schema_version": "1.0.0",
        "source": "CODEX_SUBAGENT_LIFECYCLE_HOOK_V1",
        "session_id": "session-1",
        "turn_id": turn_id,
        "agent_id": agent_id,
        "agent_type": role,
        "agent_transcript_path": transcript,
        "start_event_sha256": "1" * 64,
        "stop_event_sha256": "2" * 64,
        "disposition": "COMPLETED",
        "receipt_id": receipt_id,
    }


def runtime_ref(receipt: dict) -> dict:
    return {"receipt_id": receipt["receipt_id"], "sha256": canonical_sha(receipt)}


def worker_runtime_receipt() -> dict:
    return runtime_receipt(
        receipt_id="RID-WORKER",
        agent_id="agent-worker-1",
        role="semantic_worker",
        transcript="/runtime/worker-1.jsonl",
        turn_id="turn-worker",
    )


def reviewer_runtime_receipt() -> dict:
    return runtime_receipt(
        receipt_id="RID-REVIEWER",
        agent_id="agent-reviewer-2",
        role="semantic_reviewer",
        transcript="/runtime/reviewer-2.jsonl",
        turn_id="turn-reviewer",
    )


def authority(*, proposition_id: str = "PROP-001", admission_id: str = "AUTH-001") -> dict:
    return {
        "schema_version": "1.0.0",
        "admission_id": admission_id,
        "record_type": "AUTHORITY",
        "disposition": "ACCEPTED",
        "jurisdiction": "DOMAIN_SEMANTICS",
        "proposition_id": proposition_id,
        "accepted_git_commit": "a" * 40,
        "admitted_at_utc": "2026-08-12T00:00:00Z",
    }


def accepted_records(*records: dict) -> dict[str, dict]:
    return {record["admission_id"]: record for record in records}


def work_order(*, authority_record: dict | None = None) -> dict:
    auth = authority_record or authority()
    return {
        "schema_version": "1.0.0",
        "work_order_id": "WO-001",
        "work_order_admission_id": "WOADM-001",
        "gate": "GATE1B",
        "stage": "SEMANTIC_DERIVATION",
        "proposition_id": auth["proposition_id"],
        "authority_ref": {"admission_id": auth["admission_id"], "sha256": canonical_sha(auth)},
        "authority_status": "GOVERNED",
        "accepted_base_commit": "a" * 40,
        "commissioned_role": "semantic_worker",
        "allowed_mutations": [],
        "proof_class": "SEMANTIC",
        "falsifier": "Find accepted source evidence that contradicts the proposition.",
        "pass_means": "The bounded semantic proposition survives independent falsification.",
        "pass_does_not_mean": "Any implementation or downstream gate is accepted.",
        "dependencies": [],
        "stop_conditions": ["Stop on any authority conflict or unsupported semantic inference."],
    }


def work_order_admission(*, wo: dict | None = None, authority_record: dict | None = None) -> dict:
    auth = authority_record or authority()
    item = wo or work_order(authority_record=auth)
    return {
        "schema_version": "1.0.0",
        "admission_id": item["work_order_admission_id"],
        "record_type": "WORK_ORDER_DELEGATION",
        "disposition": "ACCEPTED",
        "proposition_id": item["proposition_id"],
        "authority_ref": copy.deepcopy(item["authority_ref"]),
        "work_order_id": item["work_order_id"],
        "work_order_sha256": canonical_sha(item),
        "accepted_base_commit": item["accepted_base_commit"],
        "commissioned_role": item["commissioned_role"],
        "allowed_mutations": copy.deepcopy(item["allowed_mutations"]),
        "proof_class": item["proof_class"],
        "admitted_at_utc": "2026-08-12T00:00:00Z",
    }


def records_for_work_order(auth: dict, wo: dict, *extra: dict) -> dict[str, dict]:
    delegation = work_order_admission(wo=wo, authority_record=auth)
    return accepted_records(auth, delegation, *extra)


def attempt(*, wo: dict | None = None) -> dict:
    item = wo or work_order()
    return {
        "schema_version": "1.0.0",
        "attempt_id": "ATT-001",
        "work_order_id": item["work_order_id"],
        "actor_id": "agent-worker-1",
        "actor_role": item["commissioned_role"],
        "actor_thread_id": "/runtime/worker-1.jsonl",
        "actor_runtime_ref": runtime_ref(worker_runtime_receipt()),
        "accepted_base_commit": item["accepted_base_commit"],
        "candidate_commit": "b" * 40,
        "candidate_sha256": None,
        "actual_changed_paths": [],
        "proof_results": [
            {"command": "semantic-falsification", "outcome": "PASS", "evidence_sha256": "c" * 64}
        ],
    }


def review(*, wo: dict | None = None, att: dict | None = None) -> dict:
    item = wo or work_order()
    candidate = att or attempt(wo=item)
    return {
        "schema_version": "1.0.0",
        "review_id": "REV-001",
        "work_order_id": item["work_order_id"],
        "attempt_id": candidate["attempt_id"],
        "reviewer_id": "agent-reviewer-2",
        "reviewer_thread_id": "/runtime/reviewer-2.jsonl",
        "reviewer_runtime_ref": runtime_ref(reviewer_runtime_receipt()),
        "candidate_commit": candidate["candidate_commit"],
        "candidate_sha256": candidate["candidate_sha256"],
        "authority_ref": copy.deepcopy(item["authority_ref"]),
        "authority_re_read": True,
        "legitimacy": "AUTHORISED",
        "proof_quality": "PROVEN",
        "falsification_evidence": ["Re-derived authority and attempted a contradiction."],
        "limitations": [],
    }


def admission(*, wo: dict | None = None, att: dict | None = None, rev: dict | None = None) -> dict:
    item = wo or work_order()
    candidate = att or attempt(wo=item)
    audit = rev or review(wo=item, att=candidate)
    return {
        "schema_version": "1.0.0",
        "admission_id": "ADM-001",
        "record_type": "SEMANTIC_RESULT",
        "disposition": "ACCEPTED",
        "proposition_id": item["proposition_id"],
        "authority_ref": copy.deepcopy(item["authority_ref"]),
        "work_order_id": item["work_order_id"],
        "attempt_id": candidate["attempt_id"],
        "review_id": audit["review_id"],
        "accepted_base_commit": item["accepted_base_commit"],
        "candidate_commit": candidate["candidate_commit"],
        "candidate_sha256": candidate["candidate_sha256"],
        "admitted_at_utc": "2026-08-12T00:00:00Z",
    }


def test_required_governance_schemas_exist_and_are_strict_objects():
    for name in ["semantic_index", "work_order", "attempt_record", "review"]:
        data = json.loads((ROOT / "schemas" / f"{name}.schema.json").read_text())
        assert data["type"] == "object"
        assert data["additionalProperties"] is False
        assert data["required"]


def test_pending_semantic_index_is_not_an_accepted_proposition_source():
    module = load_validator()
    data = json.loads((ROOT / "docs/governance/SEMANTIC_INDEX.json").read_text())
    with pytest.raises(module.GovernanceError, match="not accepted"):
        module.accepted_semantic_index_entries(data)


def test_accepted_semantic_index_requires_real_admission_and_exact_source_binding(tmp_path):
    module = load_validator()
    repo, index, adm = semantic_index_repo(tmp_path)
    entries = module.accepted_semantic_index_entries(
        index, admissions={adm["admission_id"]: adm}, repo_root=repo
    )
    assert set(entries) == {"IDX-1"}


def test_nonexistent_semantic_index_admission_is_rejected(tmp_path):
    module = load_validator()
    repo, index, _ = semantic_index_repo(tmp_path)
    with pytest.raises(module.GovernanceError, match="semantic index admission"):
        module.accepted_semantic_index_entries(index, admissions={}, repo_root=repo)


def test_semantic_index_admission_must_bind_exact_index_bytes(tmp_path):
    module = load_validator()
    repo, index, adm = semantic_index_repo(tmp_path)
    bad = copy.deepcopy(adm)
    bad["artifact_sha256"] = "0" * 64
    with pytest.raises(module.GovernanceError, match="index hash"):
        module.accepted_semantic_index_entries(
            index, admissions={bad["admission_id"]: bad}, repo_root=repo
        )


def test_semantic_index_source_ref_must_be_admitted_and_byte_exact(tmp_path):
    module = load_validator()
    repo, index, adm = semantic_index_repo(tmp_path)
    bad_index = copy.deepcopy(index)
    bad_index["entries"][0]["authority_refs"][0]["sha256"] = "0" * 64
    (repo / "docs/governance/SEMANTIC_INDEX.json").write_text(
        json.dumps(bad_index, indent=2, sort_keys=True) + "\n"
    )
    subprocess.run(["git", "add", "docs/governance/SEMANTIC_INDEX.json"], cwd=repo, check=True)
    subprocess.run(["git", "commit", "-qm", "bad source ref"], cwd=repo, check=True)
    bad_adm = copy.deepcopy(adm)
    bad_adm["candidate_commit"] = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=repo, text=True
    ).strip()
    bad_adm["artifact_sha256"] = canonical_sha(bad_index)
    with pytest.raises(module.GovernanceError, match="source authority"):
        module.accepted_semantic_index_entries(
            bad_index, admissions={bad_adm["admission_id"]: bad_adm}, repo_root=repo
        )


def test_role_mismatch_rejected():
    module = load_validator()
    auth = authority()
    wo = work_order(authority_record=auth)
    att = attempt(wo=wo)
    att["actor_role"] = "integration_auditor"
    with pytest.raises(module.GovernanceError, match="role"):
        module.validate_attempt(wo, att)


def test_review_of_attempt_a_cannot_admit_attempt_b():
    module = load_validator()
    auth = authority()
    wo = work_order(authority_record=auth)
    att_a = attempt(wo=wo)
    att_b = copy.deepcopy(att_a)
    att_b["attempt_id"] = "ATT-002"
    att_b["candidate_commit"] = "d" * 40
    rev = review(wo=wo, att=att_a)
    adm = admission(wo=wo, att=att_b, rev=rev)
    with pytest.raises(module.GovernanceError, match="attempt"):
        module.validate_admission(wo, att_b, rev, adm)


def test_schema_valid_but_unauthorised_work_order_rejected():
    module = load_validator()
    auth = authority()
    wo = work_order(authority_record=auth)
    wo["authority_status"] = "REQUIRES_ACCEPTANCE"
    with pytest.raises(module.GovernanceError, match="GOVERNED"):
        module.validate_work_order(
            wo, records_for_work_order(auth, wo), accepted_base_commit="a" * 40
        )


def test_proof_quality_pass_cannot_overcome_legitimacy_rejection():
    module = load_validator()
    auth = authority()
    wo = work_order(authority_record=auth)
    att = attempt(wo=wo)
    rev = review(wo=wo, att=att)
    rev["legitimacy"] = "NOT_AUTHORISED"
    adm = admission(wo=wo, att=att, rev=rev)
    with pytest.raises(module.GovernanceError, match="legitimacy"):
        module.validate_admission(wo, att, rev, adm)


def test_candidate_commit_mismatch_rejected():
    module = load_validator()
    auth = authority()
    wo = work_order(authority_record=auth)
    att = attempt(wo=wo)
    rev = review(wo=wo, att=att)
    rev["candidate_commit"] = "f" * 40
    with pytest.raises(module.GovernanceError, match="candidate"):
        module.validate_review(wo, att, rev)


def test_dependencies_must_reference_accepted_admission_ids():
    module = load_validator()
    auth = authority()
    wo = work_order(authority_record=auth)
    wo["dependencies"] = ["ADM-MISSING"]
    with pytest.raises(module.GovernanceError, match="dependency"):
        module.validate_work_order(
            wo, records_for_work_order(auth, wo), accepted_base_commit="a" * 40
        )


def test_rejected_record_cannot_become_current_by_active_path_placement():
    module = load_validator()
    rejected = authority(admission_id="AUTH-REJECTED")
    rejected["disposition"] = "REJECTED"
    wo = work_order(authority_record=rejected)
    with pytest.raises(module.GovernanceError, match="accepted authority"):
        module.validate_work_order(
            wo,
            records_for_work_order(rejected, wo),
            accepted_base_commit="a" * 40,
        )


def test_admitted_state_disagreement_with_git_or_admission_fails_closed():
    module = load_validator()
    gate0 = {
        "admission_id": "GATE0-001",
        "disposition": "GATE0_PASS",
        "proven_commit": "a" * 40,
    }
    state = {
        "operational_status": "GATE0_PASS",
        "candidate_control_commit": "a" * 40,
        "gate0_proven_commit": "a" * 40,
        "latest_admission_id": "GATE0-001",
    }
    module.validate_admitted_state_binding(
        state, current_git_parent="a" * 40, admissions={"GATE0-001": gate0}
    )
    bad = copy.deepcopy(state)
    bad["candidate_control_commit"] = "b" * 40
    with pytest.raises(module.GovernanceError, match="Git"):
        module.validate_admitted_state_binding(
            bad, current_git_parent="a" * 40, admissions={"GATE0-001": gate0}
        )


def test_work_order_cannot_self_promote_new_programme_rule():
    module = load_validator()
    auth = authority(proposition_id="EXISTING-RULE")
    wo = work_order(authority_record=auth)
    wo["proposition_id"] = "NEW-PROGRAMME-RULE"
    with pytest.raises(module.GovernanceError, match="proposition"):
        module.validate_work_order(
            wo, records_for_work_order(auth, wo), accepted_base_commit="a" * 40
        )


def test_authority_hash_must_bind_exact_admitted_record():
    module = load_validator()
    auth = authority()
    wo = work_order(authority_record=auth)
    wo["authority_ref"]["sha256"] = "0" * 64
    with pytest.raises(module.GovernanceError, match="hash"):
        module.validate_work_order(
            wo, records_for_work_order(auth, wo), accepted_base_commit="a" * 40
        )


def test_work_order_requires_exact_admitted_delegation():
    module = load_validator()
    auth = authority()
    wo = work_order(authority_record=auth)
    with pytest.raises(module.GovernanceError, match="delegation"):
        module.validate_work_order(wo, accepted_records(auth), accepted_base_commit="a" * 40)


def test_work_order_delegation_binds_exact_scope_and_bytes():
    module = load_validator()
    auth = authority()
    wo = work_order(authority_record=auth)
    records = records_for_work_order(auth, wo)
    module.validate_work_order(wo, records, accepted_base_commit="a" * 40)
    widened = copy.deepcopy(wo)
    widened["allowed_mutations"] = ["docs/other.md"]
    with pytest.raises(module.GovernanceError, match=r"work order hash|scope"):
        module.validate_work_order(widened, records, accepted_base_commit="a" * 40)


@pytest.mark.parametrize("frozen_path", ["AGENTS.md", "PLANS.md"])
def test_even_exact_delegation_cannot_authorise_frozen_programme_authority(frozen_path):
    module = load_validator()
    auth = authority()
    wo = work_order(authority_record=auth)
    wo["allowed_mutations"] = [frozen_path]
    records = records_for_work_order(auth, wo)
    with pytest.raises(module.GovernanceError, match="frozen programme authority"):
        module.validate_work_order(wo, records, accepted_base_commit="a" * 40)


def test_root_governance_files_declare_frozen_authority_boundary():
    agents = (ROOT / "AGENTS.md").read_text()
    plans = (ROOT / "PLANS.md").read_text()
    assert "**FROZEN**" in agents
    assert "**FROZEN**" in plans
    assert "No work order or delegation may authorise mutation" in agents
    assert "must fail closed" in plans


def test_valid_transaction_is_admissible_only_after_independent_review():
    module = load_validator()
    auth = authority()
    wo = work_order(authority_record=auth)
    att = attempt(wo=wo)
    rev = review(wo=wo, att=att)
    adm = admission(wo=wo, att=att, rev=rev)
    records = records_for_work_order(auth, wo)
    module.validate_work_order(wo, records, accepted_base_commit="a" * 40)
    module.validate_attempt(wo, att)
    module.validate_review(wo, att, rev)
    module.validate_admission(wo, att, rev, adm)


def test_reviewer_thread_must_be_fresh_from_worker_thread():
    module = load_validator()
    wo = work_order()
    att = attempt(wo=wo)
    rev = review(wo=wo, att=att)
    rev["reviewer_thread_id"] = att["actor_thread_id"]
    with pytest.raises(module.GovernanceError, match="thread"):
        module.validate_review(wo, att, rev)


def test_state_advance_is_not_exposed_as_a_separate_bypass_api():
    module = load_validator()
    assert not hasattr(module, "advance_state_after_admission")
    assert hasattr(module, "execute_admission_transaction")


def test_canonical_transaction_derives_git_binding_before_state_advance(tmp_path):
    module = load_validator()
    repo, base, candidate = git_repo(tmp_path)
    auth = authority()
    wo = work_order(authority_record=auth)
    wo["accepted_base_commit"] = base
    wo["allowed_mutations"] = ["docs/example.md"]
    att = attempt(wo=wo)
    att["accepted_base_commit"] = base
    att["candidate_commit"] = candidate
    att["actual_changed_paths"] = ["docs/example.md"]
    rev = review(wo=wo, att=att)
    adm = admission(wo=wo, att=att, rev=rev)
    records = records_for_work_order(auth, wo)
    state = {
        "latest_admission_id": "ADM-OLD",
        "candidate_control_commit": base,
        "current_work_order": "WO-001",
        "current_attempt": "ATT-001",
        "first_blocker": "DEF-OLD",
        "unrelated": "preserved",
    }
    updated = module.execute_admission_transaction(
        repo,
        state,
        wo,
        att,
        rev,
        adm,
        admissions=records,
        accepted_base_commit=base,
    )
    assert updated["latest_admission_id"] == adm["admission_id"]
    assert updated["candidate_control_commit"] == candidate
    assert updated["current_work_order"] is None
    assert updated["current_attempt"] is None
    assert updated["first_blocker"] is None
    assert updated["unrelated"] == "preserved"


def test_canonical_transaction_rejects_fictitious_candidate_commit(tmp_path):
    module = load_validator()
    repo, base, _ = git_repo(tmp_path)
    auth = authority()
    wo = work_order(authority_record=auth)
    wo["accepted_base_commit"] = base
    att = attempt(wo=wo)
    att["accepted_base_commit"] = base
    att["candidate_commit"] = "f" * 40
    rev = review(wo=wo, att=att)
    adm = admission(wo=wo, att=att, rev=rev)
    with pytest.raises(module.GovernanceError, match="candidate commit"):
        module.validate_admission_transaction(
            repo,
            wo,
            att,
            rev,
            adm,
            admissions=records_for_work_order(auth, wo),
            accepted_base_commit=base,
        )


def test_canonical_transaction_rejects_self_declared_unreceipted_worker_identity(tmp_path):
    module = load_validator()
    repo, base, candidate = git_repo(tmp_path)
    auth = authority()
    wo = work_order(authority_record=auth)
    wo["accepted_base_commit"] = base
    wo["allowed_mutations"] = ["docs/example.md"]
    att = attempt(wo=wo)
    att["accepted_base_commit"] = base
    att["candidate_commit"] = candidate
    att["actual_changed_paths"] = ["docs/example.md"]
    att["actor_id"] = "forged-worker"
    rev = review(wo=wo, att=att)
    adm = admission(wo=wo, att=att, rev=rev)
    with pytest.raises(module.GovernanceError, match="runtime identity"):
        module.validate_admission_transaction(
            repo,
            wo,
            att,
            rev,
            adm,
            admissions=records_for_work_order(auth, wo),
            accepted_base_commit=base,
        )


def test_canonical_transaction_requires_distinct_authenticated_runtime_receipts(tmp_path):
    module = load_validator()
    repo, base, candidate = git_repo(tmp_path)
    auth = authority()
    wo = work_order(authority_record=auth)
    wo["accepted_base_commit"] = base
    wo["allowed_mutations"] = ["docs/example.md"]
    att = attempt(wo=wo)
    att["accepted_base_commit"] = base
    att["candidate_commit"] = candidate
    att["actual_changed_paths"] = ["docs/example.md"]
    rev = review(wo=wo, att=att)
    rev["reviewer_id"] = att["actor_id"]
    rev["reviewer_thread_id"] = att["actor_thread_id"]
    rev["reviewer_runtime_ref"] = copy.deepcopy(att["actor_runtime_ref"])
    adm = admission(wo=wo, att=att, rev=rev)
    with pytest.raises(module.GovernanceError, match="independent"):
        module.validate_admission_transaction(
            repo,
            wo,
            att,
            rev,
            adm,
            admissions=records_for_work_order(auth, wo),
            accepted_base_commit=base,
        )


def test_candidate_git_parent_and_actual_diff_are_mechanically_bound():
    module = load_validator()
    wo = work_order()
    wo["allowed_mutations"] = ["docs/example.md"]
    att = attempt(wo=wo)
    att["actual_changed_paths"] = ["docs/example.md"]
    module.validate_git_candidate_binding(
        wo,
        att,
        candidate_commit=att["candidate_commit"],
        candidate_parent=wo["accepted_base_commit"],
        changed_paths=["docs/example.md"],
    )
    with pytest.raises(module.GovernanceError, match="parent"):
        module.validate_git_candidate_binding(
            wo,
            att,
            candidate_commit=att["candidate_commit"],
            candidate_parent="f" * 40,
            changed_paths=["docs/example.md"],
        )
    with pytest.raises(module.GovernanceError, match="changed paths"):
        module.validate_git_candidate_binding(
            wo,
            att,
            candidate_commit=att["candidate_commit"],
            candidate_parent=wo["accepted_base_commit"],
            changed_paths=["docs/other.md"],
        )


def test_attempt_declaration_cannot_hide_an_extra_git_changed_path():
    module = load_validator()
    wo = work_order()
    wo["allowed_mutations"] = ["docs/example.md"]
    att = attempt(wo=wo)
    att["actual_changed_paths"] = ["docs/example.md"]
    with pytest.raises(module.GovernanceError, match="changed paths"):
        module.validate_git_candidate_binding(
            wo,
            att,
            candidate_commit=att["candidate_commit"],
            candidate_parent=wo["accepted_base_commit"],
            changed_paths=["docs/example.md", "docs/hidden.md"],
        )
