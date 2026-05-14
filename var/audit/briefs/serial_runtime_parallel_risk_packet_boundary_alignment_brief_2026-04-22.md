# Serial Runtime → Parallel Risk Packet Boundary Alignment Brief

Date: 2026-04-22  
Status: Standalone execution brief  
Purpose: Align the repo to the admitted blueprint boundary without broadening architecture beyond scope.

---

## 1) Identity

You are executing a **bounded blueprint-alignment tranche**.

Your job is **not** to redesign the repo, push DMPV3 further upstream than the blueprint allows, or solve downstream capital deployment. Your job is to align the live codebase to the blueprint position already established:

- the **first deliberate DMP boundary** is **Serial runtime -> packet carriage**;
- **parallel risk ingress** must consume **bounded packets only**;
- parallel risk must **not** read serial internals directly;
- parallel risk must emit a **DMPV3 output packet**.

This tranche exists to make that admitted boundary real in the runtime path.

---

## 2) Objective

Move the repo from its current shape to the blueprint shape at one specific boundary.

### Required end state

1. The serial runtime emits an **admitted canonical DMPV3 packet set** as its real downstream boundary product.
2. Parallel risk ingress consumes **only** the admitted bounded packet inputs required by the blueprint.
3. Parallel risk output remains a lawful **DMPV3 packet**.
4. The path is proved on **one deterministic end-to-end route only**.
5. Work stops after that route is aligned and proved.

---

## 3) Binding architectural position

This brief is bound to the blueprint position already established in the V3 workbook referenced by `migration_prebuild/AGENTS.override.md`.

### The blueprint position to preserve

- Raw ingress remains **raw/native**, not DMPV3.
- Raw bundle -> prepared substrate remains **typed/native**.
- Prepared substrate -> cognition ingress bundle remains **typed/native**.
- Serial stage -> serial stage remains **internal typed flow / internal packet**, not a newly broadened DMP boundary.
- The **first deliberate DMP boundary** is **Serial runtime -> packet carriage**.
- Parallel risk consumes **bounded packet/envelope inputs only**.
- Parallel risk does **not** read native serial internals directly.
- Parallel risk uses **temporal packet plus selected stage packets**, not one giant everything-packet.

### Therefore

This tranche is **not** permitted to:

- push DMPV3 above the admitted serial runtime boundary;
- convert raw ingress, preparation, or cognition ingress into DMPV3 carriage;
- collapse parallel risk independence by letting it read serial internals directly;
- use one oversized packet as a substitute for bounded contractual packet inputs.

---

## 4) Current-state problem statement

The current repo state, as already established in prior analysis, is:

- upstream raw/prepared/cognition surfaces remain typed/native carriers;
- the serial runtime already emits stage packets, but those packets are not yet the fully admitted, enforced downstream boundary product for the target handoff;
- parallel risk ingress is still anchored to an earlier typed seam rather than being cleanly rebased onto the blueprint packet boundary;
- parallel risk output exists conceptually as packetised output, but the boundary must be made truthful and explicit in the admitted runtime path.

The problem is therefore **not** “invent DMPV3” and **not** “push DMPV3 everywhere”.

The problem is:

> make the blueprint’s admitted serial-runtime-to-parallel-risk packet boundary the actual live runtime contract.

---

## 5) Scope

This tranche is limited to the following six work steps.

### Step 1 — Freeze the boundary law

Freeze the exact admitted boundary to be implemented.

You must explicitly state and preserve:

- what remains typed/native;
- where DMPV3 begins;
- which packets are admitted for parallel risk consumption;
- what direct reads are forbidden.

Output of Step 1:

- a precise boundary statement written into the tranche report and any touched local authority surfaces required for truthful implementation;
- a concrete list of packet inputs parallel risk is allowed to consume.

### Step 2 — Promote the serial runtime packet set to the real boundary product

The serial runtime must emit the admitted packet set as the real downstream handoff product.

This means:

- the emitted packet family is not merely an after-the-fact trace artefact;
- the emitted packet family becomes the contractual downstream product of serial runtime for this boundary;
- the packet set is bounded and truthful.

Output of Step 2:

- one canonical admitted serial runtime packet set suitable for downstream packet consumption.

### Step 3 — Rebase parallel risk ingress onto bounded selected packets

Parallel risk ingress must be aligned to the packet boundary.

This means:

- remove reliance on the earlier typed seam as the admitted runtime boundary for parallel risk;
- make parallel risk consume the admitted **temporal packet plus selected stage packets**;
- preserve independence by forbidding direct reads of serial internals.

Output of Step 3:

- a packet-driven parallel risk ingress path that matches the blueprint.

### Step 4 — Keep parallel risk output packetised and bounded

Do not redesign the lane.

This step only requires:

- maintain lawful DMPV3 output;
- preserve bounded scope;
- do not widen into Stage B or Stage C unless already directly required by the admitted boundary and proven lawful.

Output of Step 4:

- packet in / packet out at the admitted blueprint boundary.

### Step 5 — Prove one deterministic end-to-end path only

Prove exactly one path:

`raw bundle -> prepared substrate -> cognition ingress bundle -> serial runtime -> admitted serial packet set -> parallel-risk packet ingress -> parallel-risk output packet`

The proof must show:

- upstream typed/native surfaces remain where the blueprint intends them to remain;
- DMPV3 begins at the admitted serial runtime boundary;
- parallel risk consumes bounded packets only;
- no direct serial-internal read survives;
- temporal semantics remain lawful across the path;
- the resulting parallel-risk output is a lawful DMPV3 packet.

Output of Step 5:

- one deterministic proof path with concrete evidence.

### Step 6 — Close out and stop

After the boundary is aligned and the one proof path passes, stop.

Do not spill into adjacent architecture ambitions.

Output of Step 6:

- closeout report;
- proof receipts;
- branch/tag closeout;
- explicit statement of what remains deferred.

---

## 6) Non-goals / prohibited expansion

This tranche must **not** do any of the following:

- no push of DMPV3 further upstream than the blueprint admits;
- no redesign of payload richness across all modules;
- no attempt to solve whether current strategy content is too thin in general;
- no Stage B / Stage C parallel-risk expansion unless this is unavoidably required and directly evidenced;
- no final-risk join work;
- no capital-deployment work;
- no trade placement work;
- no general repo-wide temporal rewrite beyond what is strictly required for this boundary to be truthful;
- no workbook-heavy blueprint maintenance;
- no creation of a second blueprint or “clean blueprint” artefact in this tranche.

---

## 7) Deliverables

This tranche must deliver the following, and only the following:

1. A bounded implementation on a new work branch.
2. A standalone tranche report in Markdown.
3. Code changes required to make the serial-runtime-to-parallel-risk boundary match the blueprint.
4. Tests and/or deterministic proof artefacts for the one admitted path.
5. A clean closeout tag on the accepted end commit.
6. A concise deferred-work statement listing what was intentionally not done.

### Not required in this tranche

- execution-ledger redesign;
- blueprint workbook redesign;
- workbook clean-up beyond any minimal truthful receipt obligation that is already mandatory in the repo process.

---

## 8) Definition of done

This tranche is done only if **all** of the following are true:

1. The implementation preserves the blueprint rule that the first deliberate DMP boundary is **Serial runtime -> packet carriage**.
2. Parallel risk ingress consumes **bounded packet inputs only**.
3. Parallel risk no longer relies on the earlier typed seam as the admitted runtime boundary.
4. Parallel risk does not read serial internals directly.
5. Parallel risk emits a lawful DMPV3 output packet.
6. One deterministic end-to-end path is proved.
7. The proof explicitly shows where typed/native carriage ends and where packet carriage begins.
8. The tranche does not broaden into final risk, capital deployment, or upstream DMP expansion.
9. The repo closes cleanly on an annotated tag.
10. The closeout report truthfully states both what was completed and what remains deferred.

If any one of the above is false, the tranche is not done.

---

## 9) Required evidence standard

All material claims in the closeout must be backed by direct evidence:

- file paths and line ranges for code changes;
- direct proof/test output;
- packet specimen artefacts if emitted;
- exact branch name, commit hashes, and tag name;
- explicit list of touched files;
- explicit statement that prohibited expansion did not occur.

Do not claim success based on intention, partial implementation, or inferred behaviour.

---

## 10) Baseline and branching

Start from the latest accepted closeout baseline that closed the Module 8 exactness supplementary tranche.

Create one new work branch for this tranche. Use a truthful branch slug derived from this brief title. Do not reuse an old branch. Do not batch this work into a larger tranche.

---

## 11) Return format

Return in this order:

1. **Known true before execution** — the boundary law and current-state gap this tranche is fixing.
2. **What changed** — exact files and exact boundary shift made.
3. **Proof** — the one deterministic path and its evidence.
4. **Deferred by design** — everything intentionally left for later.
5. **Closeout identifiers** — branch, head commit, annotated tag.

---

## 12) Practical execution instruction

Do not optimise for cleverness.

Optimise for:

- boundary truth;
- blueprint adherence;
- one clean modular packet handoff;
- one clean proof path;
- explicit stopping.

Once the admitted serial-runtime-to-parallel-risk packet boundary is real and proved, stop.
