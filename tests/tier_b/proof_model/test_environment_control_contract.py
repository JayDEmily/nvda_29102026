from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]


def _read(path: str) -> str:
    return (REPO_ROOT / path).read_text(encoding="utf-8")


def test_make_install_is_frozen_non_editable_and_lock_owned() -> None:
    makefile = _read("Makefile")

    assert "INSTALL_INPUTS := pyproject.toml uv.lock .python-version" in makefile
    assert "$(UV) sync --frozen --extra dev --no-editable" in makefile
    assert "pip install -e" not in makefile
    assert "pip install --upgrade pip" not in makefile


def test_lockfile_uses_portable_public_package_origins() -> None:
    lockfile = _read("uv.lock")

    assert "applied-caas-gateway" not in lockfile
    assert 'registry = "https://pypi.org/simple"' in lockfile
    assert "https://files.pythonhosted.org/packages/" in lockfile


def test_installed_package_smoke_imports_from_site_packages_outside_repo() -> None:
    makefile = _read("Makefile")

    assert ".PHONY: installed-package-smoke" in makefile
    assert 'tmp_dir="$$(mktemp -d)"' in makefile
    assert '$(abspath $(PYTHON))" -I -c' in makefile
    assert 'sysconfig.get_paths()["purelib"]' in makefile
    assert "module.is_relative_to(purelib)" in makefile


def test_pr_ci_uses_pinned_uv_and_authoritative_promotion_gate() -> None:
    workflow = _read(".github/workflows/pr-preflight.yml")

    assert "astral-sh/setup-uv@08807647e7069bb48b6ef5acd8ec9567f424441b" in workflow
    assert 'version: "0.11.16"' in workflow
    assert 'cache-dependency-glob: "uv.lock"' in workflow
    assert "run: make install" in workflow
    assert "run: make installed-package-smoke" in workflow
    assert "run: make promotion-gate" in workflow
    assert "run: make test" not in workflow
    assert "cache: pip" not in workflow


def test_remote_patch_ci_delegates_authority_and_gates_before_push() -> None:
    workflow = _read(".github/workflows/apply-remote-bridge-patch.yml")

    assert "run: make promotion-check" in workflow
    assert "run: make promotion-gate" in workflow
    assert "git push origin" in workflow
    assert workflow.index("run: make promotion-gate") < workflow.index("git push origin")
    assert "proof['schema_version']" not in workflow
    assert "block_id" not in workflow
    assert "proof.get('blocks'" not in workflow
    assert "tier_a_test_count" not in workflow
    assert "registered_retained_seed_tier_a" not in workflow
