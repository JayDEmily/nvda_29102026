"""Build/restore a distinctly identified L00 transfer package; never run product code."""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tarfile

BASE = '97f944d51ab9e403250fe76910e2754b50425c73'
ORIGINAL_ARCHIVE = '4d02c82894513bff8d07af7a2af6a151cd3f5f14ece581ac0bf0d87ea9ed0430'
ORIGINAL_BUNDLE = '91db4a1989bff366c1f547c5776ca886c276b6b1310027ae929aa1cd1efee4b9'
REVIEWED = 'e19c2df9b21777ae467b628c2fa1d36e137a1072'
INTAKE = '3b0aa1b775f660d57aa5c7f14fef3e69b8c5b6b4'
BRANCH = 'refs/heads/execution/accepted-r1-20261030'


def run(*args: str, cwd: Path, log: Path | None = None) -> str:
    result = subprocess.run(args, cwd=cwd, text=True, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, check=False)
    if log is not None:
        with log.open('a') as stream:
            stream.write('$ ' + ' '.join(args) + '\n' + result.stdout + '\n')
    if result.returncode:
        raise RuntimeError(f'command failed ({result.returncode}): {args}: {result.stdout}')
    return result.stdout.strip()


def sha(path: Path) -> str:
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def write(path: Path, data: object) -> None:
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + '\n')



def complete_additive_header(path: Path, refs: dict[str, str], base_repo: Path) -> dict:
    """Advertise exact source refs omitted by Git at the excluded baseline.

    Bundle v2 separates textual prerequisite/ref declarations from an unchanged
    Git-generated pack. Every added ref must already exist in the verified base.
    Native Git verify/fetch/fsck and full ref readback remain mandatory.
    """
    temp = path.with_suffix('.header-complete')
    with path.open('rb') as source:
        lines = []
        while True:
            line = source.readline()
            if not line:
                raise RuntimeError('unterminated bundle header')
            if line == b'\n':
                break
            lines.append(line)
        if lines[0] != b'# v2 git bundle\n':
            raise RuntimeError('only documented SHA1 bundle v2 header is supported')
        declared = {}
        for line in lines[1:]:
            if line.startswith(b'-'):
                continue
            tip, name = line.decode().strip().split(' ', 1)
            if name in declared:
                raise RuntimeError('duplicate bundle ref')
            declared[name] = tip
        missing = {name: tip for name, tip in refs.items() if name not in declared}
        for name, tip in missing.items():
            run('git', 'cat-file', '-e', tip, cwd=base_repo)
        for name, tip in declared.items():
            if name != 'HEAD' and refs.get(name) != tip:
                raise RuntimeError('Git-generated header/source mismatch: ' + name)
        pack_hash = hashlib.sha256()
        with temp.open('wb') as dest:
            dest.writelines(lines)
            for name, tip in sorted(missing.items()):
                dest.write(f'{tip} {name}\n'.encode())
            dest.write(b'\n')
            while block := source.read(1024 * 1024):
                pack_hash.update(block)
                dest.write(block)
    temp.replace(path)
    with path.open('rb') as stream:
        while stream.readline() != b'\n':
            pass
        after_hash = hashlib.file_digest(stream, 'sha256').hexdigest()
    if after_hash != pack_hash.hexdigest():
        raise RuntimeError('Git-generated pack bytes changed')
    actual = run('git', 'bundle', 'list-heads', str(path), cwd=base_repo)
    advertised = {line.split()[1]: line.split()[0] for line in actual.splitlines()}
    if {name: tip for name, tip in advertised.items() if name != 'HEAD'} != refs:
        raise RuntimeError('completed additive header does not declare every source ref')
    return {'format': 'git-bundle-v2', 'method': 'Exact source-reference header completion; prerequisite and pack bytes retained',
            'added_base_satisfied_refs': missing, 'added_count': len(missing),
            'advertised_named_ref_count': len(refs), 'pack_sha256_before': pack_hash.hexdigest(),
            'pack_sha256_after': after_hash}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--target', required=True)
    parser.add_argument('--original-archive', type=Path)
    args = parser.parse_args()
    repo = Path.cwd()
    if run('git', 'status', '--porcelain', '--untracked-files=all', cwd=repo):
        raise RuntimeError('packaging requires a clean committed checkout')
    out = args.output.resolve()
    out.mkdir(parents=True, exist_ok=False)
    payload = out / 'handover'
    payload.mkdir()
    target = run('git', 'rev-parse', args.target + '^{commit}', cwd=repo)
    if run('git', 'rev-parse', 'HEAD', cwd=repo) != target:
        raise RuntimeError('checkout must equal exact target')
    for ancestor in (BASE, REVIEWED, INTAKE):
        run('git', 'merge-base', '--is-ancestor', ancestor, target, cwd=repo)
    tree = run('git', 'rev-parse', target + '^{tree}', cwd=repo)
    original_rows = json.loads((repo / 'handoff/m02_completion_28_execution/L00/ORIGINAL_BASELINE_REFS.json').read_text())
    original = {row['ref']: row['tip'] for row in original_rows}
    if len(original) != 66:
        raise RuntimeError('original historical named ref count is not66')
    remote_text = run('git', 'ls-remote', '--refs', 'origin', cwd=repo)
    remote = {line.split()[1]: line.split()[0] for line in remote_text.splitlines()}
    if remote.get(BRANCH) != target:
        raise RuntimeError('remote execution branch changed: do not export stale candidate')
    # Use an isolated export repository. Never alter checkout/GitHub original refs.
    export = out / 'export.git'
    run('git', 'init', '--bare', str(export), cwd=repo)
    run('git', 'fetch', '--no-tags', str(repo), '+refs/*:refs/source/*', cwd=export)
    for name, tip in {**remote, **original}.items():
        if name in original and name in remote and original[name] != remote[name]:
            raise RuntimeError('original/current exact ref namespace conflict: ' + name)
        run('git', 'cat-file', '-e', tip, cwd=export)
        run('git', 'update-ref', name, tip, cwd=export)
    prior_manifest = json.loads((repo / 'handoff/m02_completion_28_execution/L00/L00_MANIFEST.json').read_text())
    worker = prior_manifest['refs']
    for name, tip in worker.items():
        run('git', 'update-ref', 'refs/worker-e19/' + name.removeprefix('refs/'), tip, cwd=export)
    run('git', 'symbolic-ref', 'HEAD', BRANCH, cwd=export)
    base_repo = out / 'baseline.git'
    run('git', 'init', '--bare', str(base_repo), cwd=repo)
    run('git', 'fetch', '--no-tags', str(export), *[tip + ':' + ref for ref, tip in original.items()], cwd=base_repo)
    run('git', 'symbolic-ref', 'HEAD', 'refs/heads/work/downstream-reconciliation-20261028', cwd=base_repo)
    original_obtained = args.original_archive is not None
    base_name = 'NVDA_M02_L00_RECONSTRUCTED_66REF_BASE.bundle'
    if original_obtained:
        if sha(args.original_archive) != ORIGINAL_ARCHIVE:
            raise RuntimeError('original archive SHA256 mismatch')
        base_name = 'NVDA_DOWNSTREAM_RECONCILIATION_L00_CHECKPOINT_20261028_FULL_HISTORY.bundle'
        with tarfile.open(args.original_archive, 'r:gz') as archive:
            matches = [m for m in archive.getmembers() if m.isfile() and Path(m.name).name == base_name]
            if len(matches) != 1:
                raise RuntimeError('original embedded bundle not unique')
            stream = archive.extractfile(matches[0])
            if stream is None:
                raise RuntimeError('original bundle unreadable')
            with (out / base_name).open('wb') as dest:
                shutil.copyfileobj(stream, dest)
        if sha(out / base_name) != ORIGINAL_BUNDLE:
            raise RuntimeError('original embedded bundle SHA256 mismatch')
        shutil.copyfile(args.original_archive, out / 'NVDA_DOWNSTREAM_RECONCILIATION_L00_CHECKPOINT_20261028.tar.gz')
    else:
        run('git', 'bundle', 'create', str(out / base_name), '--all', cwd=base_repo)
    delta_name = 'NVDA_M02_COMPLETION28_L00_ADDITIVE_FROM_97f944d51ab9.bundle'
    run('git', 'bundle', 'create', str(out / delta_name), '--all', '^' + BASE, cwd=export)
    current_text = run('git', 'for-each-ref', '--format=%(objectname) %(refname)', cwd=export)
    refs = {line.split()[1]: line.split()[0] for line in current_text.splitlines()}
    completion = complete_additive_header(out / delta_name, refs, base_repo)
    write(out / 'ADDITIVE_HEADER_COMPLETION.json', completion)
    snapshot = {'target': target, 'tree': tree, 'fixed_baseline': BASE,
                'original66': original, 'remote_snapshot': remote,
                'retained_worker_e19_snapshot': worker, 'exported_refs': refs,
                'original_archive_obtained': original_obtained,
                'original_archive_expected_sha256': ORIGINAL_ARCHIVE,
                'original_bundle_expected_sha256': ORIGINAL_BUNDLE,
                'original_path_verification': 'PERFORMED' if original_obtained else 'NOT_PERFORMED_ORIGINAL_BINARY_UNAVAILABLE',
                'new_package_not_original_worker_archive': True}
    write(payload / 'CURRENT_REF_MANIFEST.json', snapshot)
    write(payload / 'ORIGINAL_BASELINE_REFS.json', original_rows)
    (payload / 'L00_TRACKED_BLOBS.txt').write_text(run('git', 'ls-tree', '-r', '--full-tree', target, cwd=repo) + '\n')
    (payload / 'ALL_EXPORTED_REFS.txt').write_text(current_text + '\n')
    shutil.copytree(repo / 'handoff/m02_completion_28_execution', payload / 'handoff/m02_completion_28_execution')
    for name in ('GUARDRAILS.md', 'AGENTS.md', 'EXEC_PLAN.md'):
        (payload / 'repository-evidence').mkdir(exist_ok=True)
        shutil.copyfile(repo / name, payload / 'repository-evidence' / name)
    shutil.copyfile(out / delta_name, payload / delta_name)
    (payload / 'RESTORE.md').write_text(f'''# L00 successor transfer: exact candidate {target}\n\nThis is a NEW successor handover, not the original worker12-member archive or original baseline bytes. Original binary obtained: {original_obtained}. Base commit remains {BASE}.\n\n1. Verify this archive and external {base_name} against SHA256SUMS.txt, then verify every unpacked file against MEMBER_SHA256SUMS.txt. Reject unsafe archive paths/symlinks; no archived instructions need execution.\n2. Start a NEW empty repository: `git init --bare restored.git`. In it run `git bundle verify /absolute/path/{base_name}`, then `git fetch /absolute/path/{base_name} 'refs/*:refs/*'`.\n3. Verify the additive in that repository: `git bundle verify /absolute/path/{delta_name}`, then `git fetch /absolute/path/{delta_name} 'refs/*:refs/*'`. Do not force overwrite refs. Required original refs must already agree.\n4. `git symbolic-ref HEAD {BRANCH}`. Check exact HEAD {target}, tree {tree}, all66 original tips, all exported refs in CURRENT_REF_MANIFEST.json and complete `git ls-tree -r --full-tree HEAD` against L00_TRACKED_BLOBS.txt. Check required ancestors {BASE}, {REVIEWED} and {INTAKE}; run `git fsck --full`.\n5. Compare all loose handoff/ and repository-evidence/ files with target Git blobs. Source namespaces distinguish historical worker refs from current remote refs. Never fetch into an existing GitHub repository or overwrite historical/remote branch tips.\n\nA missing original baseline is not repaired by claiming another bundle has its SHA. The declared fallback reconstructs original66 exact names/tips with a new full-history bundle under the already recorded section5 strategy. Independently evaluate whether that satisfies the current commission before L00 release. No product tests/installations/downstream work are authorised by this transfer. D145 stays paused.\n''')
    for path in payload.rglob('*'):
        if not path.is_file():
            continue
        relative = path.relative_to(payload).as_posix()
        committed = relative if relative.startswith('handoff/') else (path.name if relative.startswith('repository-evidence/') else None)
        if committed is not None:
            raw = subprocess.check_output(['git', 'show', target + ':' + committed], cwd=repo)
            if hashlib.sha256(raw).hexdigest() != sha(path):
                raise RuntimeError('loose/committed byte mismatch: ' + committed)
    assets = {p.name: {'sha256': sha(p), 'bytes': p.stat().st_size} for p in out.iterdir() if p.is_file()}
    loose = {str(p.relative_to(payload)): {'sha256': sha(p), 'bytes': p.stat().st_size} for p in payload.rglob('*') if p.is_file()}
    manifest = {'schema': 'L00_TRANSFER_SUCCESSOR_V1', 'target': target, 'tree': tree,
                'fixed_baseline': BASE, 'original_archive_obtained': original_obtained,
                'original_path_verification': snapshot['original_path_verification'],
                'assets': assets, 'members_excluding_manifest_and_member_sums': loose,
                'self_hash_policy': 'Manifest has no self hash. Archive hash is external. MEMBER_SHA256SUMS includes this manifest, not itself.',
                'release_status': 'PENDING_INDEPENDENT_REVIEW_NOT_L00_ACCEPTANCE'}
    write(payload / 'L00_MANIFEST.json', manifest)
    sums = ''.join(f'{sha(p)}  {p.relative_to(payload)}\n' for p in sorted(payload.rglob('*')) if p.is_file())
    (payload / 'MEMBER_SHA256SUMS.txt').write_text(sums)
    logs = out / 'PRODUCER_RESTORE_COMMANDS.log'
    restored = out / 'producer-restored.git'
    run('git', 'init', '--bare', str(restored), cwd=repo, log=logs)
    run('git', 'bundle', 'verify', str(out / base_name), cwd=restored, log=logs)
    run('git', 'fetch', str(out / base_name), 'refs/*:refs/*', cwd=restored, log=logs)
    for name, tip in original.items():
        if run('git', 'rev-parse', name, cwd=restored) != tip:
            raise RuntimeError('original tip mismatch before additive: ' + name)
    run('git', 'bundle', 'verify', str(out / delta_name), cwd=restored, log=logs)
    run('git', 'fetch', str(out / delta_name), 'refs/*:refs/*', cwd=restored, log=logs)
    run('git', 'symbolic-ref', 'HEAD', BRANCH, cwd=restored, log=logs)
    if run('git', 'rev-parse', 'HEAD', cwd=restored) != target or run('git', 'rev-parse', 'HEAD^{tree}', cwd=restored) != tree:
        raise RuntimeError('restored HEAD/tree mismatch')
    for name, tip in refs.items():
        if run('git', 'rev-parse', name, cwd=restored) != tip:
            raise RuntimeError('restored ref mismatch: ' + name)
    if run('git', 'ls-tree', '-r', '--full-tree', target, cwd=restored) + '\n' != (payload / 'L00_TRACKED_BLOBS.txt').read_text():
        raise RuntimeError('tracked blob inventory mismatch')
    for ancestor in (BASE, REVIEWED, INTAKE):
        run('git', 'merge-base', '--is-ancestor', ancestor, target, cwd=restored, log=logs)
    run('git', 'fsck', '--full', cwd=restored, log=logs)
    archive_path = out / 'NVDA_M02_COMPLETION28_L00_SUCCESSOR_HANDOVER.tar.gz'
    with archive_path.open('wb') as raw, gzip.GzipFile(fileobj=raw, mode='wb', mtime=0, filename='') as zipped:
        with tarfile.open(fileobj=zipped, mode='w') as archive:
            for path in sorted(payload.rglob('*')):
                if path.is_file():
                    info = archive.gettarinfo(str(path), arcname=str(path.relative_to(payload)))
                    info.uid = info.gid = info.mtime = 0
                    info.uname = info.gname = ''
                    with path.open('rb') as stream:
                        archive.addfile(info, stream)
    shutil.copyfile(payload / 'L00_MANIFEST.json', out / 'L00_MANIFEST.json')
    shutil.copyfile(payload / 'CURRENT_REF_MANIFEST.json', out / 'CURRENT_REF_MANIFEST.json')
    shutil.copyfile(payload / 'L00_TRACKED_BLOBS.txt', out / 'L00_TRACKED_BLOBS.txt')
    shutil.copyfile(payload / 'RESTORE.md', out / 'RESTORE.md')
    receipt = {'target': target, 'tree': tree, 'original66_verified': 66,
               'exported_refs_verified': len(refs), 'current_remote_refs_verified': len(remote),
               'tracked_blob_listing_equal': True, 'both_bundle_verify_exit_code': 0,
               'fsck_full_exit_code': 0, 'ancestry_checked': [BASE, REVIEWED, INTAKE],
               'original_path_verification': snapshot['original_path_verification'],
               'independence': 'PRODUCER_VALIDATION_ONLY', 'l00_released': False}
    write(out / 'PRODUCER_RESTORE_RECEIPT.json', receipt)
    (out / 'SHA256SUMS.txt').write_text(''.join(f'{sha(p)}  {p.name}\n' for p in sorted(out.iterdir()) if p.is_file() and p.name != 'SHA256SUMS.txt'))
    print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    main()
