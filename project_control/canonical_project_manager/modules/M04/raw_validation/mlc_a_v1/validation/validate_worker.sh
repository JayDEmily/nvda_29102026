#!/usr/bin/env bash
set -u

SOURCE_COMMIT="ee67c752d14073a959fda478f31f4466b6952cae"
R1_WORKER_COMMIT="bf9f732869efb1c0f9befe4de8c0b179d12784fb"
EXPECTED_BRANCH="work/lane-2a-m04-mlc-a-v1"
RECORD="project_control/canonical_project_manager/modules/M04/M04_AUTHORITY_WORKER_RECORD_V1.md"
EVIDENCE_ROOT="project_control/canonical_project_manager/modules/M04/raw_validation/mlc_a_v1"
MANIFEST="${EVIDENCE_ROOT}/FULL_READ_MANIFEST.tsv"
HASH_MANIFEST="${EVIDENCE_ROOT}/FILE_SHA256.tsv"
LOCATOR_VALIDATOR="${EVIDENCE_ROOT}/validation/validate_locators.py"
WORKBOOK_VALIDATOR="${EVIDENCE_ROOT}/validation/inspect_workbook.mjs"
WORKBOOK_OUTPUT="${EVIDENCE_ROOT}/validation/WORKBOOK_LOCATOR_OUTPUT.jsonl"
failures=0

run_check() {
  local label="$1"
  shift
  printf '\n[%s]\n' "${label}"
  printf 'command:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local rc=$?
  printf 'exit_status: %s\n' "${rc}"
  if [ "${rc}" -ne 0 ]; then
    failures=$((failures + 1))
  fi
}

check_branch() {
  test "$(git branch --show-current)" = "${EXPECTED_BRANCH}"
}

check_source_ancestry() {
  git merge-base --is-ancestor "${SOURCE_COMMIT}" HEAD &&
    git merge-base --is-ancestor "${R1_WORKER_COMMIT}" HEAD
}

check_not_shallow() {
  test "$(git rev-parse --is-shallow-repository)" = "false" &&
    test ! -f .git/shallow
}

check_allowed_paths() {
  local path
  while IFS= read -r path; do
    [ -z "${path}" ] && continue
    case "${path}" in
      "${RECORD}"|"${EVIDENCE_ROOT}"/*) ;;
      *)
        printf 'disallowed_path=%s\n' "${path}"
        return 1
        ;;
    esac
  done < <(
    {
      git diff --name-only "${SOURCE_COMMIT}"
      git ls-files --others --exclude-standard
    } | sort -u
  )
}

check_manifest() {
  local rc=0
  local path reason read_status mutation_relevance expected actual
  while IFS=$'\t' read -r path reason read_status mutation_relevance expected; do
    [ "${path}" = "path" ] && continue
    if [ ! -f "${path}" ]; then
      printf 'missing_manifest_path=%s\n' "${path}"
      rc=1
      continue
    fi
    case "${read_status}" in
      READ_FULL|READ_SCOPED_EXACT_LOCATORS|READ_SCOPED_ACCEPTED_M04_K07_ROWS) ;;
      *)
        printf 'invalid_read_status=%s:%s\n' "${path}" "${read_status}"
        rc=1
        ;;
    esac
    if [ "${mutation_relevance}" = "MUTATE_R2" ]; then
      actual="$(git show "${R1_WORKER_COMMIT}:${path}" | sha256sum | awk '{print $1}')"
    elif [ "${mutation_relevance}" = "CREATE_R2" ]; then
      if git cat-file -e "${R1_WORKER_COMMIT}:${path}" 2>/dev/null; then
        actual="PRESENT"
      else
        actual="ABSENT"
      fi
    else
      actual="$(sha256sum "${path}" | awk '{print $1}')"
    fi
    if [ "${actual}" != "${expected}" ]; then
      printf 'manifest_hash_mismatch=%s expected=%s actual=%s\n' "${path}" "${expected}" "${actual}"
      rc=1
    fi
  done < "${MANIFEST}"
  return "${rc}"
}

check_evidence_hashes() {
  local rc=0
  local expected path actual
  if [ ! -f "${HASH_MANIFEST}" ]; then
    printf 'missing_hash_manifest=%s\n' "${HASH_MANIFEST}"
    return 1
  fi
  while IFS=$'\t' read -r expected path; do
    [ "${expected}" = "sha256" ] && continue
    [ "${expected}" = "SELF_EXCLUDED" ] && continue
    [ "${expected}" = "PHASE2_REFRESH_REQUIRED" ] && continue
    if [ ! -f "${path}" ]; then
      printf 'missing_evidence_path=%s\n' "${path}"
      rc=1
      continue
    fi
    actual="$(sha256sum "${path}" | awk '{print $1}')"
    if [ "${actual}" != "${expected}" ]; then
      printf 'evidence_hash_mismatch=%s expected=%s actual=%s\n' "${path}" "${expected}" "${actual}"
      rc=1
    fi
  done < "${HASH_MANIFEST}"
  return "${rc}"
}

check_required_authority_text() {
  grep -Fq 'Every packet role must eventually declare its minimum mandatory, optional, conditionally required, and not-applicable lineage subset.' docs/09.1_DMPV3_PROTOCOL_WORKING.md &&
    grep -Fq 'The producer must know which checks are required for the exact packet role and record their actual outcomes.' docs/09.1_DMPV3_PROTOCOL_WORKING.md &&
    grep -Fq 'Do not infer role-specific mandatory lineage or validation checks from default field values; Gate B must decide them semantically for each packet boundary.' docs/09.1_DMPV3_PROTOCOL_WORKING.md &&
    grep -Fq 'admits trace/run defaulting for a reference packet, while the Gate C test rejects missing caller-owned context' project_control/normative_authority_top_down_alignment/gate_c2_proof_envelopes/D-010.md &&
    grep -Fq 'PROPOSED_M04_AUTHORITY_V1_AWAITING_LANE_2AT' "${RECORD}" &&
    grep -Fq 'docs/11.1_NATIVE_ARCHITECTURE_BLUEPRINT_WORKING.md:50' "${RECORD}" &&
    ! grep -Fq 'docs/11.1_NATIVE_ARCHITECTURE_BLUEPRINT_WORKING.md:44' "${RECORD}" &&
    grep -Fq '.modules[] | select(.module_id=="M04") | .owns' "${RECORD}" &&
    ! grep -Fq '.modules[M04].owns' "${RECORD}"
}

check_exact_locator_coverage() {
  python3 "${LOCATOR_VALIDATOR}" >/dev/null
}

check_repaired_json_selector() {
  jq -e '.modules[] | select(.module_id=="M04") | .owns' \
    project_control/canonical_project_manager/architecture/Atlas_Architecture_Machine_Readable.json |
    grep -Fxq '"DMPV3 envelope validation and packet carriage only"'
}

check_workbook_locators() {
  local output dependency_link link_created rc
  test -n "${CODEX_PRIMARY_RUNTIME_NODE:-}" || return 1
  test -n "${CODEX_PRIMARY_RUNTIME_NODE_MODULES:-}" || return 1
  dependency_link="$(dirname "$(pwd)")/node_modules"
  link_created=0
  if [ ! -e "${dependency_link}" ]; then
    ln -s "${CODEX_PRIMARY_RUNTIME_NODE_MODULES}" "${dependency_link}" || return 1
    link_created=1
  fi
  output="$(mktemp)"
  "${CODEX_PRIMARY_RUNTIME_NODE}" "${WORKBOOK_VALIDATOR}" >"${output}"
  rc=$?
  if [ "${rc}" -eq 0 ]; then
    diff -u "${WORKBOOK_OUTPUT}" "${output}"
    rc=$?
  fi
  rm -f "${output}"
  if [ "${link_created}" -eq 1 ]; then
    unlink "${dependency_link}"
  fi
  return "${rc}"
}

printf 'Lane 2AW bounded validation\n'
printf 'source_commit=%s\n' "${SOURCE_COMMIT}"
printf 'expected_branch=%s\n' "${EXPECTED_BRANCH}"

run_check "status" git status --short --branch
run_check "branch" check_branch
run_check "source_ancestry" check_source_ancestry
run_check "complete_history" check_not_shallow
run_check "diff_check" git diff --check
run_check "allowed_changed_paths" check_allowed_paths
run_check "full_read_manifest" check_manifest
run_check "required_authority_text" check_required_authority_text
run_check "exact_locator_coverage" check_exact_locator_coverage
run_check "repaired_json_selector" check_repaired_json_selector
run_check "workbook_locators" check_workbook_locators
run_check "git_fsck" git fsck --full --no-dangling

if [ -f "${HASH_MANIFEST}" ]; then
  run_check "worker_evidence_hashes" check_evidence_hashes
else
  printf '\n[worker_evidence_hashes]\n'
  printf 'status: deferred until FILE_SHA256.tsv exists\n'
fi

printf '\nvalidation_failures=%s\n' "${failures}"
test "${failures}" -eq 0
