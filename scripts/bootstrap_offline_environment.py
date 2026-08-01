#!/usr/bin/env python3
"""Create the locked project environment from accepted offline wheelhouse archives."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import time
import zipfile
from pathlib import Path

EXPECTED_PYTHON = (3, 13, 5)
ACCEPTED_RUNTIME_SHA256 = "6e4459f4e5508303bdb2e03bcca7701ee72e640f36a716c20b3cd6b0c09b0b42"
ACCEPTED_DEV_SHA256 = "d71a1f5f22aaaa588a59012833c8d797258ea1505feec37e77d7948c818cc249"
ACCEPTED_RUNTIME_SIZE = 64_398_120
ACCEPTED_DEV_SIZE = 15_199_214
BUILD_REQUIREMENTS = ("hatchling==1.29.0", "editables==0.6")


class BootstrapError(RuntimeError):
    """Raised when offline environment evidence or bootstrap invariants fail."""


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify_archive(
    path: Path, expected_sha256: str, expected_size: int | None
) -> dict[str, object]:
    path = path.expanduser().resolve()
    if not path.is_file():
        raise BootstrapError(f"archive not found: {path}")
    actual_size = path.stat().st_size
    if expected_size is not None and actual_size != expected_size:
        raise BootstrapError(
            "archive size mismatch for " f"{path}: expected {expected_size}, got {actual_size}"
        )
    actual_sha256 = sha256_file(path)
    if actual_sha256 != expected_sha256:
        raise BootstrapError(
            "SHA-256 mismatch for " f"{path}: expected {expected_sha256}, got {actual_sha256}"
        )
    return {
        "path": str(path),
        "size_bytes": actual_size,
        "sha256": actual_sha256,
    }


def safe_extract_zip(archive: Path, destination: Path) -> None:
    destination.mkdir(parents=True, exist_ok=False)
    destination_root = destination.resolve()
    with zipfile.ZipFile(archive) as handle:
        for member in handle.infolist():
            member_path = (destination / member.filename).resolve()
            if not member_path.is_relative_to(destination_root):
                raise BootstrapError(
                    f"unsafe ZIP member escapes extraction root: {member.filename}"
                )
        handle.extractall(destination)


def find_wheelhouse(extracted_root: Path) -> Path:
    candidates = sorted(
        path.resolve() for path in extracted_root.rglob("wheelhouse") if path.is_dir()
    )
    if len(candidates) != 1:
        raise BootstrapError(
            "expected exactly one wheelhouse under " f"{extracted_root}, found {candidates}"
        )
    if not any(candidates[0].glob("*.whl")):
        raise BootstrapError(f"wheelhouse contains no wheels: {candidates[0]}")
    return candidates[0]


def run_checked(command: list[str], *, cwd: Path) -> None:
    try:
        subprocess.run(command, cwd=cwd, check=True)
    except subprocess.CalledProcessError as exc:
        raise BootstrapError(
            f"command failed with exit {exc.returncode}: {' '.join(command)}"
        ) from exc


def git_identity(repo_root: Path) -> dict[str, object]:
    def output(*args: str) -> str:
        completed = subprocess.run(
            ["git", *args],
            cwd=repo_root,
            check=True,
            capture_output=True,
            text=True,
        )
        return completed.stdout.strip()

    return {
        "commit": output("rev-parse", "HEAD"),
        "branch": output("branch", "--show-current"),
        "dirty": bool(output("status", "--porcelain")),
    }


def write_receipt(
    *,
    repo_root: Path,
    runtime_evidence: dict[str, object],
    dev_evidence: dict[str, object],
    commands: list[list[str]] | None,
    lock_export_sha256: str | None,
    status: str,
) -> Path:
    receipt_path = repo_root / "var/proof_receipts/offline_environment.json"
    receipt_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema_version": 2,
        "status": status,
        "created_at_epoch": time.time(),
        "python": sys.version.split()[0],
        "python_executable": sys.executable,
        "git": git_identity(repo_root),
        "uv_lock_sha256": sha256_file(repo_root / "uv.lock"),
        "pyproject_sha256": sha256_file(repo_root / "pyproject.toml"),
        "lock_export_sha256": lock_export_sha256,
        "runtime_archive": runtime_evidence,
        "dev_archive": dev_evidence,
        "commands": commands,
    }
    receipt_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return receipt_path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runtime-zip", type=Path, required=True)
    parser.add_argument("--dev-zip", type=Path, required=True)
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--uv", default="uv")
    parser.add_argument("--replace-venv", action="store_true")
    parser.add_argument("--verify-only", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if sys.version_info[:3] != EXPECTED_PYTHON:
        raise BootstrapError(
            "expected Python " f"{EXPECTED_PYTHON}, got {sys.version_info[:3]}: {sys.executable}"
        )

    repo_root = args.repo_root.expanduser().resolve()
    for marker in ("pyproject.toml", "uv.lock", ".python-version"):
        if not (repo_root / marker).is_file():
            raise BootstrapError(f"repo marker missing: {repo_root / marker}")
    if (repo_root / ".python-version").read_text(encoding="utf-8").strip() != "3.13.5":
        raise BootstrapError(".python-version is not 3.13.5")

    runtime_evidence = verify_archive(
        args.runtime_zip, ACCEPTED_RUNTIME_SHA256, ACCEPTED_RUNTIME_SIZE
    )
    dev_evidence = verify_archive(args.dev_zip, ACCEPTED_DEV_SHA256, ACCEPTED_DEV_SIZE)

    if args.verify_only:
        receipt_path = write_receipt(
            repo_root=repo_root,
            runtime_evidence=runtime_evidence,
            dev_evidence=dev_evidence,
            commands=None,
            lock_export_sha256=None,
            status="ARCHIVES_VERIFIED",
        )
        print(f"offline_archives=PASS receipt={receipt_path}")
        return 0

    uv_path = shutil.which(args.uv)
    if uv_path is None:
        raise BootstrapError(f"uv executable not found: {args.uv}")

    venv_path = repo_root / ".venv"
    if venv_path.exists():
        if not args.replace_venv:
            raise BootstrapError(
                f"{venv_path} already exists; pass --replace-venv " "for a fresh environment"
            )
        if venv_path.resolve() != (repo_root / ".venv").resolve():
            raise BootstrapError(f"refusing to remove unexpected venv path: {venv_path}")
        shutil.rmtree(venv_path)

    commands: list[list[str]] = []
    extraction_parent = repo_root / "var/offline_wheelhouse"
    extraction_parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(
        prefix="accepted-", dir=extraction_parent
    ) as temporary_directory:
        temporary_root = Path(temporary_directory)
        runtime_root = temporary_root / "runtime"
        dev_root = temporary_root / "dev"
        requirements_path = temporary_root / "requirements.current-lock.txt"
        safe_extract_zip(Path(runtime_evidence["path"]), runtime_root)
        safe_extract_zip(Path(dev_evidence["path"]), dev_root)
        runtime_wheelhouse = find_wheelhouse(runtime_root)
        dev_wheelhouse = find_wheelhouse(dev_root)

        export_command = [
            uv_path,
            "export",
            "--frozen",
            "--extra",
            "dev",
            "--no-editable",
            "--no-hashes",
            "--no-emit-project",
            "--output-file",
            str(requirements_path),
        ]
        commands.append(export_command)
        run_checked(export_command, cwd=repo_root)
        lock_export_sha256 = sha256_file(requirements_path)

        venv_command = [
            uv_path,
            "venv",
            "--python",
            sys.executable,
            "--no-managed-python",
            str(venv_path),
        ]
        commands.append(venv_command)
        run_checked(venv_command, cwd=repo_root)

        venv_python = venv_path / "bin/python"
        find_links = [
            "--find-links",
            str(runtime_wheelhouse),
            "--find-links",
            str(dev_wheelhouse),
        ]
        offline_flags = ["--offline", "--no-index", "--no-cache"]

        dependency_command = [
            uv_path,
            "pip",
            "install",
            "--python",
            str(venv_python),
            *offline_flags,
            *find_links,
            "--requirements",
            str(requirements_path),
        ]
        commands.append(dependency_command)
        run_checked(dependency_command, cwd=repo_root)

        build_command = [
            uv_path,
            "pip",
            "install",
            "--python",
            str(venv_python),
            *offline_flags,
            *find_links,
            *BUILD_REQUIREMENTS,
        ]
        commands.append(build_command)
        run_checked(build_command, cwd=repo_root)

        project_command = [
            uv_path,
            "pip",
            "install",
            "--python",
            str(venv_python),
            *offline_flags,
            *find_links,
            "--no-build-isolation",
            "--no-deps",
            str(repo_root),
        ]
        commands.append(project_command)
        run_checked(project_command, cwd=repo_root)

    venv_python = venv_path / "bin/python"
    if not venv_python.is_file():
        raise BootstrapError(f"environment Python missing after install: {venv_python}")
    check_command = [uv_path, "pip", "check", "--python", str(venv_python)]
    commands.append(check_command)
    run_checked(check_command, cwd=repo_root)
    version_command = [str(venv_python), "--version"]
    commands.append(version_command)
    run_checked(version_command, cwd=repo_root)
    (venv_path / ".install.stamp").touch()

    receipt_path = write_receipt(
        repo_root=repo_root,
        runtime_evidence=runtime_evidence,
        dev_evidence=dev_evidence,
        commands=commands,
        lock_export_sha256=lock_export_sha256,
        status="PASS",
    )
    print(f"offline_environment=PASS receipt={receipt_path}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except BootstrapError as exc:
        print(f"offline_environment=FAIL {exc}", file=sys.stderr)
        raise SystemExit(2) from exc
