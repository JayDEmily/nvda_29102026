# Method and Source Pins

Status: bootstrap source manifest for `NVDA-LIFECYCLE-CONTROL-001`.

## 1. Project Lifecycle Methodology

- Source package: `PROJECT_LIFECYCLE_METHODOLOGY_ACCEPTED_MAIN_FULL_GIT_20260919.tar.gz`
- Package SHA-256: `f32e35484f004442331210a796581fc4c1a161bfb7aff074f7ce769510d4b1c4`
- Repository branch observed: `main`
- Git commit: `443e4870df9fe8b63f6ad6471e02508d78be6974`
- Jurisdiction: outer Project lifecycle / Gate semantics.

## 2. NVIDIA Implementation Admission source

- Source package: `NVDA_IMPLEMENTATION_ADMISSION_FINAL_ACCEPTED_FULL_GIT_20260919.tar(1).gz`
- Package SHA-256: `9e23177ceb3407acd137f56e1ff3ae4fc3b91eb3a431da5295f8e02deaf377a7`
- Repository branch observed: `main`
- Git commit: `f64cf4c3f04e8e02ea368defb6d89d0f3ed0df7b`
- Observed terminal role: accepted implementation-ready brief -> independently challenged BICP; stops before implementation work order, product tests and code.
- Project use: source evidence for the already-executed Implementation Admission result and its reusable admission procedure. The macro Project will adopt/reconcile the existing terminal handoff rather than rerun it.
- Provenance caveat: current `main` is IA-24 commit `f64cf4c3f04e8e02ea368defb6d89d0f3ed0df7b`, but `admission/BICP_ACCEPTED.md` and `admission/IA_CLOSEOUT.md` still contain terminal-gate-pending wording. G02 must resolve that authority state explicitly.

## 3. CODE-001 design lineage

- Source package: `NVDA_CODE_001_BICP_TO_CODE_METHOD_FULL_GIT_20260919.tar(2).gz`
- Package SHA-256: `f7b2a53a5c7abff9322e8fc216d571266a1de9919902b536d81f1e79d80663cb`
- Repository branch observed: `main`
- Git commit: `e580ee4450c51e98d254f9604708ee34a4912e66`
- Git tree: `f0f36444b13b6952e1e66974cac3698e63c858d4`
- Method status observed: `PROPOSED DESIGN V0`.
- Repository ExecPlan status observed: methodology formalisation only; independent methodology challenge remains outstanding.
- Project use: reusable design lineage and supporting methodology source. It is not the active execution binding for G03; the accepted operational successor plan in the VI-06 implementation workspace is the bound specialist authority for the current run.

## 4. NVIDIA VI-06 concrete implementation/reference-run evidence

- Source package: `NVDA_VI06_COMPLETE_HANDOFF_20260919.tar(1).gz`
- Package SHA-256: `843dfcd5435e4738d3c7a87a8472207600dce0316306bad3ff18de1960b2f6c6`
- Git bundle: `NVDA_VI06_BLOCKED_FULL_GIT.bundle`
- Bundle HEAD / blocked branch commit: `d095954c16a9818eadb60d6364148229f2dc4558`
- Branch: `work/vi-06-iwo-independent-challenge`
- Observed role: concrete accepted successor-workflow execution and current G03 implementation workspace. Its root `EXEC_PLAN.md` records explicit programme acceptance of the successor methodology and is the active specialist operational authority bound by `G03-BIND-001`.

## 5. PCM / bounded control identity


- External PCM repository/version supplied here: `NONE`.
- Bootstrap control: `control/CONTROL_PROFILE.md` in this repository.
- Authority: temporary project-local equivalent control mechanism under PLM Gate 00 bootstrap law.
- Migration condition: if an external accepted PCM is supplied/selected, create an explicit methodology migration record before it governs active work.
