# PR preflight workflow receipt

Status: PR_PREFLIGHT_WORKFLOW_COMMITTED_TO_MAIN

Repository: `JayDEmily/nvda10`
Target branch: `main`
Starting main SHA: `fd100e2fcf70931f407cef43d7118185ac20ca88`

## File added

- `.github/workflows/pr-preflight.yml`

## Placement decision

GitHub Actions workflow YAML belongs under `.github/workflows/`, not beside repo-root `AGENTS.md` or `PLANS.md`.

The workflow delegates to the repo-root Makefile so executable gate logic remains in one place.

## Triggers

- `pull_request` targeting `main`
- `push` to `main`
- manual `workflow_dispatch`

## Gates run

```bash
make install
make compile
make test
make pr-preflight
make bridge-blueprint-check
```

## Non-claims

This receipt does not claim the workflow has run successfully yet. It records only that the workflow file was added to `main`.
