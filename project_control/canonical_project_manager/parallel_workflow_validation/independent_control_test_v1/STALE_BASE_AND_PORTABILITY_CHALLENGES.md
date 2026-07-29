# Independent failure challenges

## Stale-base challenge

Scenario: a lane worker starts from a commit other than the exact PM source commit, while retaining the expected branch name. Expected rejection: source archive SHA, exact commit, ancestry, changed-path boundary and reconstruction checks fail; the candidate cannot be accepted merely because its branch name matches. Result: the briefs and registry require exact source archive/SHA/branch/commit plus reconstructable ancestry, so this stale-base case is deterministically rejected.

## Portability reconstruction challenge

Scenario: a tester archive contains reports and patches but omits `changes.bundle`, or the bundle does not include reconstructable PM-source ancestry. Expected rejection: package member validation, `git bundle verify`, fresh reconstruction and exact commit checks fail. Result: each tester brief requires `MANIFEST.json`, verified `changes.bundle`, evidence members and `RECONSTRUCTION.txt`, with fresh reconstruction before return, so a report-only or ancestry-broken package is deterministically rejected.
