# D002 ingress invocation correction

The first read-only ingress invocation omitted `repository_root`, so Python raised a call-signature TypeError before claim validation. `ingress.log` preserves that output. The declared function signature is `load_product_proof_claim(repository_root: Path, claim_id: str)`; the corrected call supplies `Path.cwd()` and writes separate output. No product code, proof or runtime case changed.
