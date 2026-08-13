# External Lineage Index

Review date: 2026-08-04.

The entries below distinguish direct repository authority, external corroboration and project-specific synthesis. Vendor sources inform the kernel only through these recorded adaptations.

| Kernel feature | Lineage classification | Official source lineage | Project-specific adaptation |
|---|---|---|---|
| Modular monolith, bounded responsibilities and clear interfaces | `EXTERNAL_CORROBORATION` | Google Cloud Architecture Framework, “Promote modular design”; AWS Prescriptive Guidance, decomposition by subdomain; Microsoft common web application architectures; IBM module partitioning | No service split is required. Semantic ownership remains independent of package count or deployment topology. |
| Ports/adapters, dependency inversion and explicit composition | `EXTERNAL_CORROBORATION` | AWS hexagonal architecture; Microsoft Clean Architecture/common web application architectures; Google modular interfaces | Applied inside one Python distribution. The registry is not a dependency-injection container or service locator. |
| Anti-corruption translation at external boundaries | `EXTERNAL_CORROBORATION` | AWS and Microsoft Anti-Corruption Layer pattern guidance | Translation belongs to the application shell/adapters and cannot acquire domain decisions. |
| Public/internal interface distinction in Python | `DIRECT_LANGUAGE_CONSTRAINT` | Python PEP 8, “Public and Internal Interfaces”; Python import system reference | Python conventions are insufficient for enforcement, so the repository adds AST-based public-seam validation. |
| Packaging metadata and build authority | `DIRECT_LANGUAGE_ECOSYSTEM` | Python PEP 621 and Python Packaging Authority specifications | `pyproject.toml` and the regenerated lock define the minimal install surface. |
| Requirement/proposition-derived tests and traceability | `EXTERNAL_CORROBORATION` | IBM requirements-based testing; Google test sizes; Microsoft Well-Architected testing; AWS CI/CD test-layer guidance | Exact physical-path admission, independent tier/lifecycle and one registry-derived aggregate set are project-specific controls. |
| Immutable identifier history and explicit supersession | `PROJECT_SPECIFIC_SYNTHESIS` | Microsoft and IBM architecture-decision guidance provide analogues | Category prefixes, monotonic unbounded suffixes and non-reuse are kernel-specific laws. |
| M/P/G/A/K/S taxonomy | `PROJECT_SPECIFIC` | No direct vendor lineage claimed | Created to prevent semantic owners, carriers, governance, shells, mechanisms and cross-cutting views from being conflated. |
| Tier A/B/C plus lifecycle | `PROJECT_SPECIFIC` | Vendor test levels are analogues only | Exact meanings and promotion mechanics are repository-native. |

## Official source locations

- Google modular design: https://docs.cloud.google.com/architecture/framework/performance-optimization/promote-modular-design
- AWS subdomain decomposition: https://docs.aws.amazon.com/prescriptive-guidance/latest/modernization-decomposing-monoliths/decompose-subdomain.html
- AWS hexagonal architecture: https://docs.aws.amazon.com/prescriptive-guidance/latest/hexagonal-architectures/overview.html
- AWS anti-corruption layer: https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/acl.html
- AWS CI/CD tests: https://docs.aws.amazon.com/prescriptive-guidance/latest/strategy-cicd-litmus/tests-for-cicd-pipelines.html
- Microsoft common web application architectures: https://learn.microsoft.com/en-us/dotnet/architecture/modern-web-apps-azure/common-web-application-architectures
- Microsoft anti-corruption layer: https://learn.microsoft.com/en-us/azure/architecture/patterns/anti-corruption-layer
- Microsoft testing: https://learn.microsoft.com/en-us/azure/well-architected/operational-excellence/testing
- IBM module partitioning: https://www.ibm.com/docs/en/baw/25.0.x?topic=libraries-partitioning-modules
- IBM requirements-based testing: https://www.ibm.com/docs/en/engineering-lifecycle-management-suite/test-management/7.1.0?topic=requirements-based-testing
- Python PEP 8: https://peps.python.org/pep-0008/
- Python PEP 621: https://peps.python.org/pep-0621/
- Python import system: https://docs.python.org/3/reference/import.html
