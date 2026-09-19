# NVDA Architecture Kernel

This repository is the behaviour-neutral structural kernel for the NVDA codebase. It defines the architectural object taxonomy, registries, ownership/dependency/public-seam laws, lifecycle, composition skeleton, proof admission and promotion machinery required before future product capability is implemented.

It contains no admitted NVIDIA trading/business module. `config/architecture/modules.yaml` and `config/architecture/surfaces.yaml` remain empty unless separately admitted under current authority.

The semantic-to-implementation-ready-brief methodology is upstream and separate from this repository. The kernel must accept an explicitly accepted implementation-ready brief without importing or duplicating that upstream methodology.
The generic ingress boundary binds exact brief bytes by SHA-256, records external implementation acceptance and a bounded create/modify architecture projection, and fails closed rather than repairing missing domain meaning.

Start with `GUARDRAILS.md`, `AGENTS.md`, and the explicitly accepted root `EXEC_PLAN.md`.
