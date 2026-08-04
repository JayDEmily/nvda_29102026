# AGENTS.md — Architecture Kernel Operating Map

This repository is a behaviour-neutral, extensible architecture kernel.

Authority order:

1. direct user instruction;
2. `docs/architecture/ARCHITECTURE_KERNEL_RESET_BRIEF.md`;
3. the active `PLANS.md`;
4. the architecture documents under `docs/architecture/`;
5. admitted proof configuration under `config/proof/`;
6. source, schemas, templates and tests.

Operating laws:

- Former packages, tests, receipts and Git history are historical evidence, not active business authority.
- Runtime modules, protocols, governance planes, application shells, technical kernels and architecture surfaces are distinct categories and must not be conflated.
- A runtime module is admitted only after a clear semantic ownership boundary, typed public seam and declared dependency set exist.
- Cross-owner imports must use the target owner’s declared public seam. Private cross-owner imports are prohibited.
- Registries are declarative authority and validation input; they are not runtime service locators.
- A placeholder, framework or bootstrap registry row does not prove implementation.
- Ambiguity must be recorded as unresolved. Do not invent architecture or business behaviour.
- Production behaviour and capability development are outside this reset.
- Mechanical validation proves only the structural propositions it exercises.

Required validation:

```bash
uv sync --locked --extra dev --offline
python tools/validate_architecture.py
python tools/check_dependencies.py
python tools/check_public_seams.py
python tools/run_promotion_gate.py --set architecture_kernel
```

Read `PLANS.md` before mutation. Keep material claims tied to paths, command output, commits or artefacts.
