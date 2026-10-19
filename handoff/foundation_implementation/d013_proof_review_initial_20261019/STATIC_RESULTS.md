# Bounded actual static results

Both commands executed from /workspace/scratch/d549b6d808a9/g52-recovery/repository; both exit0.

`/workspace/scratch/d549b6d808a9/g52-dev/bin/python /workspace/scratch/d549b6d808a9/d013-authored-proof-review-cdXhTW/static_review.py`

Four COMPILE_PASS outputs with hashes identical to REVIEW.md. SIX_FUNCTIONS:
test_d013_actual_predecessors_exact_ratio163;
test_d013_predecessor_compatibility_and_refusal316;
test_d013_exact_ratio_canonical_domain524;
test_d013_identity_versions_and_later_retry608;
test_d013_sqlite_recovery_faults_and_integrity830;
test_d013_additive_types_and_legacy_preservation1212.

PROJECTED_CASES2 +66*2 +12 +12 +20 +1 =179; no collection performed.
SOURCE_REVIEWED_NEGATIVE_SITES [(16,assignment),(17,assignment),(18,assignment),(19,attr-defined),(20,arg-type),(21,arg-type),(22,assignment)] COUNT7.

OLD_LOGICAL_KEYS independently extracted from both _catalogue.py and _sqlite.py:
owner_object_id,owner_namespace,implementation_brief_sha256,request,definition_content_sha256,parameter_set,input_selection_policy,unit_conventions,projection_mappings,raw_input_lineage.

NO_DOMAIN_EXECUTION_NO_IMPORTS_NO_MYPY_NO_COLLECTION.

`/workspace/scratch/d549b6d808a9/g52-dev/bin/python -m ruff check tests/product/market_measurement_d013`

All checks passed!
