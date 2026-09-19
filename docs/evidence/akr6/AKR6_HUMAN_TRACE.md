# AKR-6 human semantic and executable trace

Status: NON-NORMATIVE REHEARSAL EVIDENCE.

## Exact external authority

The rehearsal uses the external file `AKR6_ACCEPTED_IMPLEMENTATION_BRIEF.md` without copying or rewriting its text into the active repository. Its exact SHA-256 is:

`938debe255d68668b0ae60f021d679fc8e3022be6eb050e7f3cd6112818fd342`

The repository validator can prove byte identity and binding structure. It cannot prove that the human/programme acceptance is legitimate; that remains higher authority.

## Bounded architecture judgement from the exact brief

The exact brief establishes the following facts needed for this rehearsal:

- it assigns one coherent Raw Signal Occurrence Truth semantic ownership boundary to `raw_signal_occurrence_truth` and uses the historical label `M16` for that owner;
- it names `A00` as the sole initial consumer/caller and states that A00 owns construction, adapter translation and top-level lifecycle rather than Raw Signal meaning;
- it states that `P01` and `K01` remain non-active and are not contract consumers;
- it contains literal `G02` vocabulary-governance requirements and historical/upstream identifiers;
- it leaves final package naming/version metadata as a Remaining Unknown.

Under the current steady-state taxonomy, a coherent domain decision/transformation/policy/lifecycle owner is category `M`. Current higher authority also establishes that literal historical identifiers in the external brief do not allocate current post-reset identifiers and that the inherited `G02` vocabulary-governance allocation is `DO_NOT_CARRY_FORWARD` rather than a current or retired identity.

The minimal AKR-6 projection intent is therefore:

```yaml
targets:
  - action: create
    category: M
    name: raw_signal_occurrence_truth
  - action: modify
    object_id: A00
```

No numeric identifier is supplied for the create intent. No package or public-seam name is supplied. `P01`, `K01` and `G02` are not current projection targets for this bounded rehearsal.

## Human trace through the repository-facing path

The active template expresses the same create/modify contract as the binding schema: create carries category plus responsibility name and modify carries an existing object identifier. The schema forbids a caller-supplied numeric identifier on create. The implementation-authority validator verifies exact brief bytes, resolves create candidates through the post-reset candidate resolver, then validates create/modify state against current architecture state.

The candidate resolver consults current registered identifiers, current retired identifiers, durable post-reset implementation allocations and earlier candidates in the same request. It does not consult the historical identifier crosswalk or the former product catalogue. The current `M` namespace has no consumed identifier, so this exact create intent resolves non-durably to `M00`. `A00` is currently registered and is therefore a lawful modify target.

Repository-native execution against the exact brief produced:

```text
PASS: implementation authority brief_sha256=938debe255d68668b0ae60f021d679fc8e3022be6eb050e7f3cd6112818fd342
candidate_targets: create:raw_signal_occurrence_truth->M00, modify:A00
```

This is candidate resolution only. The rehearsal does not write `M00` into an architecture registry or the implementation-allocation history. Re-running against unchanged state may resolve the same candidate again.

## Stop boundary

AKR-6 does not establish that all downstream implementation questions in the external brief are currently resolved. It does not materialise the brief's `G02` wording, choose final package/public-seam paths, derive behavioural proof, write business code, durably allocate `M00`, or compose runtime behaviour. Those are outside this rehearsal and require separately authorised downstream work.

The reset brief now carries a prominent historical/non-governing banner that distinguishes its preserved imperative `G02` and former-product wording from current steady-state authority.
