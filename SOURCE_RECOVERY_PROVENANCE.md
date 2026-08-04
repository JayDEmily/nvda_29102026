# Successor Brief Recovery Provenance

The 37 successor briefs were recovered as actual Markdown blobs from the full Git object history of the supplied checkpoint repository, not reconstructed from filenames or worker notes.

- Source checkpoint: `NVDA_BEHAVIOUR_REGISTER_46404A4_20260804_FULL_HISTORY.tar.gz`
- Source repository path in that archive: `Nvda11/`
- Source branch at extraction: `work/behaviour-register-v1`
- Recovery method: enumerate `git rev-list --objects --all` entries matching `var/audit/briefs/*.md`, then extract each exact blob with `git cat-file blob <sha>`.
- Recovered document count: **37**

`SOURCE_MANIFEST.tsv` records each original repository path, Git blob SHA, recovered chronology and packaged SHA-256.

The presence of a blob in Git history proves historical existence and byte identity. It does not prove that the document is active design authority. Authority is adjudicated proposition by proposition under `AGENTS.md`.
