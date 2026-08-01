# M11 K16/K17 C-PROOF validation

Proposition: `M11-K16-K17-PORTFOLIO-LIFECYCLE-V1`.
Public seam: `PositionState`, `PortfolioSnapshot`, `LifecycleDecision`, `CloseReceipt`, `PortfolioLifecycleService`.
Reference arithmetic/action-law cases must pass. Production cases are expected red only because `nvda_desk.m11_portfolio_lifecycle` is absent. Independent adversarial review is required before Gate D.

Hardened expected-red result: `3 passed / 20 failed`. The 20 production-facing failures are
caused only by the absent canonical package. The separate review record lists the admitted
adversarial additions.
