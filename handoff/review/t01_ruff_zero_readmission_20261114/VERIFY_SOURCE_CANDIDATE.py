#!/usr/bin/env python3
"""Read-only reproducibility check for T01 UNADMITTED seven-claim Ruff repair.

Never executes a product-proof test, advances an admission, or changes files.
"""
from __future__ import annotations

import ast
import hashlib
import itertools
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
REGISTER = Path(__file__).with_name("PROPOSED_SUCCESSOR_GENERATIONS.json")
RUFF = ROOT / ".venv/bin/ruff"
RISK_SUFFIXES = {
    "test_five_minute_realised_volatility.py",
    "test_thirty_minute_realised_volatility.py",
    "test_five_day_realised_volatility.py",
    "test_ten_day_realised_volatility.py",
}


def git(*args: str) -> bytes:
    return subprocess.check_output(("git", *args), cwd=ROOT)


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def normalise_source(raw: bytes, relative: str) -> tuple[list[str], str]:
    tree = ast.parse(raw.decode("utf-8"), filename=relative)
    imports = sorted(
        ast.unparse(node)
        for node in tree.body
        if isinstance(node, (ast.Import, ast.ImportFrom))
        and not (
            isinstance(node, ast.ImportFrom)
            and node.module == "itertools"
            and {name.name for name in node.names} == {"pairwise"}
        )
    )

    class NormalisePairwise(ast.NodeTransformer):
        def visit_Call(self, node: ast.Call) -> ast.AST:
            self.generic_visit(node)
            if (
                relative.rsplit("/", 1)[-1] in RISK_SUFFIXES
                and isinstance(node.func, ast.Name)
                and node.func.id == "pairwise"
                and len(node.args) == 1
                and not node.keywords
                and isinstance(node.args[0], ast.Name)
                and node.args[0].id == "SAMPLES"
            ):
                return ast.Call(
                    func=ast.Name(id="zip", ctx=ast.Load()),
                    args=[
                        ast.Name(id="SAMPLES", ctx=ast.Load()),
                        ast.Subscript(
                            value=ast.Name(id="SAMPLES", ctx=ast.Load()),
                            slice=ast.Slice(lower=ast.Constant(1)),
                            ctx=ast.Load(),
                        ),
                    ],
                    keywords=[],
                )
            return node

    tree.body = [node for node in tree.body if not isinstance(node, (ast.Import, ast.ImportFrom))]
    return imports, ast.dump(NormalisePairwise().visit(tree), include_attributes=False)


def check() -> None:
    data = json.loads(REGISTER.read_text(encoding="utf-8"))
    assert data["schema_version"] == "REVIEW-ONLY-1.0"
    assert data["status"] == "UNADMITTED_CANDIDATE_REQUIRES_FRESH_ADEQUACY_AND_ADMISSION"
    assert data["not_an_active_generation"] is True
    assert data["active_admission_pointers_modified"] is False

    base = data["comparison_base_commit"]
    source = data["compliant_source_commit"]
    assert git("merge-base", "--is-ancestor", source, "HEAD") == b""
    changed = sorted(git("diff", "--name-only", base, source).decode().splitlines())
    assert changed == sorted(data["candidate_source_paths"]) and len(changed) == 7

    for rel in changed:
        actual = (ROOT / rel).read_bytes()
        original = git("show", f"{base}:{rel}")
        committed = git("show", f"{source}:{rel}")
        assert actual == committed and actual != original, rel
        assert normalise_source(original, rel) == normalise_source(actual, rel), rel
        if rel.rsplit("/", 1)[-1] in RISK_SUFFIXES:
            prior_tree = ast.parse(original, filename=rel)
            assignment = next(
                n for n in prior_tree.body
                if isinstance(n, ast.Assign)
                and any(isinstance(t, ast.Name) and t.id == "SAMPLES" for t in n.targets)
            )
            assert isinstance(assignment.value, ast.Call)
            gen = assignment.value.args[0]
            assert isinstance(gen, ast.GeneratorExp)
            samples = ast.literal_eval(gen.generators[0].iter)
            assert tuple(zip(samples, samples[1:])) == tuple(itertools.pairwise(samples)), rel
        print("SOURCE_AST_EQUIVALENT", rel, sha256(original), sha256(actual))

    claims = data["claims"]
    assert len(claims) == 7
    seen: set[str] = set()
    proposed_changed: list[str] = []
    for item in claims:
        claim = item["claim_id"]
        assert claim not in seen
        seen.add(claim)
        assert item["pending_independent_adequacy_review_ref"] is None
        assert item["pending_owner_admission_authority_ref"] is None

        pointer_path = item["admission_path"]
        raw_pointer = (ROOT / pointer_path).read_bytes()
        assert raw_pointer == git("show", f"{base}:{pointer_path}")
        pointer = json.loads(raw_pointer)["current_generation"]
        assert pointer == item["predecessor_pointer"]

        gen_raw = (ROOT / pointer["path"]).read_bytes()
        assert sha256(gen_raw) == pointer["sha256"]
        assert gen_raw == git("show", f"{base}:{pointer['path']}")
        previous = json.loads(gen_raw)
        assert previous["claim_id"] == claim
        assert previous["generation"] == item["predecessor_generation_number"]

        draft = item["proposed_generation_record_REVIEW_ONLY_INCOMPLETE_AUTHORITY"]
        assert draft["generation"] == previous["generation"] + 1
        assert draft["previous_generation"] == pointer
        assert draft["adequacy_review_ref"] is None
        assert draft["admission_authority_ref"] is None
        assert not (ROOT / item["proposed_generation_path"]).exists()
        for key in previous.keys():
            if key in ("generation", "previous_generation", "family_files", "support_files",
                       "adequacy_review_ref", "admission_authority_ref"):
                continue
            assert draft[key] == previous[key], (claim, key)
        original_by_path = {
            row["path"]: row["sha256"]
            for kind in ("family_files", "support_files")
            for row in previous[kind]
        }
        changed_rows = []
        for kind in ("family_files", "support_files"):
            assert [row["path"] for row in draft[kind]] == [row["path"] for row in previous[kind]]
            for row in draft[kind]:
                rel = row["path"]
                expected = sha256((ROOT / rel).read_bytes())
                assert row["sha256"] == expected, (claim, rel)
                if original_by_path[rel] != expected:
                    changed_rows.append(rel)
                    proposed_changed.append(rel)
        assert changed_rows == item["changed_hash_paths"] and len(changed_rows) == 1

        print("DRAFT_ONLY", claim, "proposed_gen", draft["generation"],
              "predecessor_sha", pointer["sha256"], "changed", changed_rows[0])
    assert sorted(proposed_changed) == changed

    assert RUFF.is_file(), "BLOCKED: locked Ruff must be installed in this checkout"
    version = subprocess.check_output((str(RUFF), "--version"), text=True).strip()
    assert version == "ruff 0.15.11", version
    completed = subprocess.run((str(RUFF), "check", "src", "tests", "tools"),
                               cwd=ROOT, text=True, capture_output=True)
    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert "All checks passed!" in completed.stdout

    assert not git("status", "--porcelain"), "candidate checkout must be clean"
    print("VERIFIED", len(changed), "compliant source files /", len(claims),
          "UNADMITTED draft transitions / zero Ruff findings")
    print("NO_PRODUCT_PROOF_EXECUTED; NO_ACTIVE_POINTER_ADVANCED; NOT_ADMITTED")


if __name__ == "__main__":
    try:
        check()
    except (AssertionError, OSError, ValueError, subprocess.CalledProcessError) as exc:
        print("CANDIDATE_VERIFICATION_BLOCKED_OR_FAILED:", repr(exc), file=sys.stderr)
        sys.exit(1)
