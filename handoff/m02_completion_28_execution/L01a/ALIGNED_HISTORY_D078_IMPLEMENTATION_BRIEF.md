# D078 exact L03 aligned-history same-fit residual implementation brief — 28 November 2026

Jurisdiction M02-C28-D078; claim neutral_market_measurement_truth_d078; family m02_l03_same_fit_d078; exact nonfungible allocation five. Conditional inert preparation ONLY, pending independent binding/admission review. Base a283f7a538af6084f61a8e47add651ade525a180, tree b4dda031bda135c633aa6f478cf7200828e79e24. Own exact64 owner grant and independent R1 aligned-history policy/finite34 review control. No installation, source/proof edits, registration, import, collection or execution authorised by this brief.

## Exact own adopted profile and authority

~~~json
{
  "profile_ref": {
    "id": "t01-l01a-d078-joint-fit",
    "version": 1
  },
  "calculation_definition_version": "T01-D078-ALIGNED-JOINT-FIT-DEF-V1",
  "parameter_ref": {
    "id": "t01-l01a-joint-fit-parameters",
    "version": 1
  },
  "selection_ref": {
    "id": "t01-l01a-d078-selection",
    "version": 1
  },
  "subject": "NVDA",
  "members": [
    "NVDA",
    "SPY",
    "QQQ",
    "SMH",
    "SOXX"
  ],
  "raw_dependencies": [],
  "derived_dependencies": [
    "D075",
    "D071",
    "D076",
    "D077",
    "D079",
    "D080",
    "D081"
  ],
  "kernel": "K06_REGRESSION_DEPENDENCE",
  "parameter_profile": "P_REGRESSION",
  "equation": "D075-(alpha+D079*D071+D080*D076+D081*D077)",
  "units": "return",
  "result_shape": "exact_ratio",
  "future_own_brief_path": "handoff/m02_completion_28_execution/L01a/ALIGNED_HISTORY_D078_IMPLEMENTATION_BRIEF.md",
  "future_binding_path": "implementation/authority/T01_ALIGNED_HISTORY_D078_AUTHORITY_BINDING.yaml"
}
~~~

Exact remap (mapping authority only, not release):
~~~json
{
  "package": "aligned_history",
  "jurisdiction": "D078",
  "proof_id": "M02-C28-D078",
  "claim_id": "neutral_market_measurement_truth_d078",
  "family_id": "m02_l03_same_fit_d078",
  "original_root": "tests/product/m02_completion_28/d078",
  "original_family_path": "tests/product/m02_completion_28/d078/test_signal.py",
  "ordered_case_ids": [
    "D078-CONTROLLED-SUCCESS",
    "D078-CONTROLLED-REACHED_REFUSAL",
    "D078-CURRENT-ROW-MISALIGNMENT",
    "D078-NONPRIOR-FIT",
    "D078-COEFFICIENT-NOT-KNOWN-AT-RESIDUAL-CUTOFF"
  ],
  "original_ordered_nodes": [
    "tests/product/m02_completion_28/d078/test_signal.py::test_d078_same_fit_residual",
    "tests/product/m02_completion_28/d078/test_signal.py::test_d078_mixed_fit",
    "tests/product/m02_completion_28/d078/test_signal.py::test_d078_wrong_current_row",
    "tests/product/m02_completion_28/d078/test_signal.py::test_d078_nonprior_fit",
    "tests/product/m02_completion_28/d078/test_signal.py::test_d078_coefficient_unavailable_at_cutoff"
  ],
  "new_root": "tests/product/m02_completion_28_prospective/d078",
  "new_family_path": "tests/product/m02_completion_28_prospective/d078/test_signal.py",
  "new_ordered_nodes": [
    "tests/product/m02_completion_28_prospective/d078/test_signal.py::test_d078_same_fit_residual",
    "tests/product/m02_completion_28_prospective/d078/test_signal.py::test_d078_mixed_fit",
    "tests/product/m02_completion_28_prospective/d078/test_signal.py::test_d078_wrong_current_row",
    "tests/product/m02_completion_28_prospective/d078/test_signal.py::test_d078_nonprior_fit",
    "tests/product/m02_completion_28_prospective/d078/test_signal.py::test_d078_coefficient_unavailable_at_cutoff"
  ],
  "descriptor_directory": "config/product_proof/m02_aligned_history_d078",
  "own_brief_path": "handoff/m02_completion_28_execution/L01a/ALIGNED_HISTORY_D078_IMPLEMENTATION_BRIEF.md",
  "own_binding_path": "implementation/authority/T01_ALIGNED_HISTORY_D078_AUTHORITY_BINDING.yaml",
  "original_contract_path": "handoff/m02_completion_28_execution/L01a/ALIGNED_HISTORY_D078_PROOF_CONTRACT.json",
  "new_contract_path": "handoff/m02_completion_28_execution/L01a/ALIGNED_HISTORY_D078_PROOF_CONTRACT.json",
  "exact_case_count": 5,
  "exact_nonfungible_ceiling": 5,
  "scope": "MAPPING_AUTHORITY_ONLY",
  "execution_release": false
}
~~~

Authority files (path to SHA256):
~~~json
{
  "handoff/m02_completion_28_execution/L01a/ALIGNED_HISTORY_SOURCE_POLICY_PROPOSED_20261126.json": "9ba56098c273007980c893db39931ac86e7a3185bbb665f8c3f1e14f99b72af1",
  "handoff/m02_completion_28_execution/L01a/ALIGNED_HISTORY_FINITE_SPECIMENS_PROPOSED_20261126.json": "bb03481de75e1820c7aff61777a4a3aa4f676440ec03e373a05c032a0417c76d",
  "handoff/m02_completion_28_execution/L01a/ALIGNED_HISTORY_JOINT_FIT_FINITE_CASES_PROPOSED_20261126.json": "3be150f2998b4187a81720b424c848099edeba7a9f638ae90d9aae95d4c5d5c1",
  "handoff/m02_completion_28_execution/L01a/G01_PARTITION_REMAP_20261128/PATH_ONLY_SUCCESSOR_AUTHORITY.json": "11d90adf234d5195d3bd31a6b42df9b046c4ad53690cb279ef071d52b3049aa7",
  "handoff/m02_completion_28_execution/OWNER_CONSOLIDATED_64_CONDITIONAL_EXECUTION_GRANT_20261127.json": "6a71f52981fc01da42f9c27726547d0d1ddd69851561479a007aeb30ebd95a41",
  "handoff/m02_completion_28_execution/TEST_EVIDENCE_LEDGER.json": "5d1ac21a0cf62fe98efe5d4bd5c510094d139e6ae6bd3fc85d10924d67189c89",
  "handoff/m02_completion_28_execution/L01a/OWNER_G01_PROSPECTIVE_PARTITION_REMAP_AUTHORIZATION_20261128.json": "cbc85f756911a9f1a926f862284168acc6f83266f8f07c0b1b68e3e2547190ff",
  "handoff/m02_completion_28_execution/L01a/D078_SAME_FIT_BINDING_PREPARATION_COMMISSION_20261128.md": "22e67e9f126d434c239dbd3225f1f1cc4ae2f270cae7bdd6d6e50c1653288f10"
}
~~~

Independent remote review refs, commits, trees and report digests (source and registration clearance, not product acceptance):
~~~json
[
  {
    "commit": "1190b50d43755ffd71629d11ba1846894a113771",
    "tree": "6899f27e39e5c34aa626be0f419da1041edf5926",
    "review_ref": "refs/heads/review/pm-l01a-aligned-history-policy-finite34-r1-20261126",
    "path": "handoff/m02_completion_28_execution/L01a/INDEPENDENT_ALIGNED_HISTORY_JOINT_FIT_POLICY_FINITE34_R1_VERDICT_20261126.md",
    "sha256": "fddeb50391f51afeccb339798c88e8b756768308a6111275d109a1bd2463dc8e",
    "git_blob": "466a0398f26d9802ade17c7f9fbe91991bd7af96",
    "bytes": 14966
  },
  {
    "commit": "22a14402bb5df8651e9136b6d00d94f657a07afd",
    "tree": "b32f50aee4e96347d9468749f47a956b60135b0a",
    "review_ref": "refs/heads/review/trial-cac-nvidia-l01a-implementation-20261127",
    "path": "handoff/m02_completion_28_execution/L01a/INDEPENDENT_CAC_TRIAL_ALIGNED_HISTORY_D071_D075_IMPLEMENTATION_VERDICT_20261127.md",
    "sha256": "6c354b51ccd42bf7230a457102f68cbf498f3ded4eae11a90b5765d9567af34b",
    "git_blob": "bd60d43162d574b462c9147f479b78f1244a7342",
    "bytes": 11413
  },
  {
    "commit": "5da8986e88d777975edae36fc65eaf8a229e29e4",
    "tree": "059362c14f0d62a99baf07b429e4dbf779e6b3f8",
    "review_ref": "refs/heads/review/trial-cac-nvidia-g01-partition-remap-20261128",
    "path": "handoff/m02_completion_28_execution/L01a/INDEPENDENT_CAC_TRIAL_G01_PROSPECTIVE_PARTITION_REMAP_VERDICT_20261128.md",
    "sha256": "0aab07086e35fe266bcf20f3dfba2934164c39188c641d6dc14318ebc72900e7",
    "git_blob": "2e1156c10a3e0ed3f40d6bf6fa738d5440000c75",
    "bytes": 9815
  },
  {
    "commit": "44f538d5b3412d95e8fdad80d17ed74a82aca221",
    "tree": "627c54e5331660881d53692e4e78c8148aeb5c15",
    "review_ref": "refs/heads/review/trial-cac-nvidia-l01a-remapped-installation-20261128",
    "path": "handoff/m02_completion_28_execution/L01a/INDEPENDENT_CAC_TRIAL_ALIGNED_HISTORY_D071_D075_REMAPPED_INSTALLATION_VERDICT_20261128.md",
    "sha256": "4eee01ea905ccbc803c88288f3757c7fd546509f740cddc17fff8e672faa58e5",
    "git_blob": "866b88876a7e1c9656378483307fee190370b0b4",
    "bytes": 9274
  },
  {
    "commit": "2d912f65efaa60079f61fa4f42897d1a9d3aa834",
    "tree": "e7e8109b89c280887730512fb815b658330afef7",
    "review_ref": "refs/heads/review/trial-cac-nvidia-d076-implementation-20261128",
    "path": "handoff/m02_completion_28_execution/L01a/INDEPENDENT_D076_DOWNSTREAM_SOURCE_IMPLEMENTATION_APPLICABILITY_VERDICT_20261128.md",
    "sha256": "af639412072377a25d08c4151113fa6e560634a8c3d888315ddd24f6885924b2"
  },
  {
    "commit": "9a98501cbff8491c7eca51dd7af485ca0b889a96",
    "tree": "3de18833aa30c124b8536dd3179e6d4d77421748",
    "review_ref": "refs/heads/review/trial-cac-nvidia-d076-registration-installation-20261128",
    "path": "handoff/m02_completion_28_execution/L01a/INDEPENDENT_D076_DOWNSTREAM_REGISTRATION_INSTALLATION_VERDICT_20261128.md",
    "sha256": "8135c94837e7e2743e80f31823d2cfb153ae4295e562edeb315aba29b9aa6e52"
  },
  {
    "commit": "89354484f6c6caece4df8a316f4b5e5460bbd53f",
    "tree": "f72395efe5e09d7abcb0fe1e13e45ea85aed15bd",
    "review_ref": "refs/heads/review/trial-cac-nvidia-d077-implementation-20261128",
    "path": "handoff/m02_completion_28_execution/L01a/INDEPENDENT_D077_DOWNSTREAM_SOURCE_IMPLEMENTATION_AND_SHARED_SURFACE_VERDICT_20261128.md",
    "sha256": "288cefc0fb3665ad812f19b0564bedc0e38edcfdf16ee5b4561d567d10f534d6"
  },
  {
    "commit": "67bc48f2c673ef87041b145b6840f79510adb966",
    "tree": "6b2adf81c313ef86ad6dae55b4b1eceaf126a8c2",
    "review_ref": "refs/heads/review/trial-cac-nvidia-d077-registration-installation-20261128",
    "path": "handoff/m02_completion_28_execution/L01a/INDEPENDENT_D077_DOWNSTREAM_REGISTRATION_INSTALLATION_VERDICT_20261128.md",
    "sha256": "84a156876fc71998c4755caac28babc4aa29de2d5adfdbc31e559a376017501d"
  },
  {
    "commit": "40fd1f7ecb886f3cee2edfcc6028ec4dc9bfcf90",
    "tree": "1268deba6bd96f779a4773c74205d3eb6e523971",
    "review_ref": "refs/heads/review/trial-cac-nvidia-d079-d080-d081-implementation-20261128",
    "path": "handoff/m02_completion_28_execution/L01a/INDEPENDENT_D079_D080_D081_JOINT_FIT_SOURCE_IMPLEMENTATION_AND_SHARED_SURFACE_VERDICTS_20261128.md",
    "sha256": "c8fb5c1c219aae53cbc1e1b45e907025d6e5ec6b5fe205e7831a71b59346acd2",
    "git_blob": "00df6973ee41247682dc1726d874eabe874c397a",
    "bytes": 24304,
    "parent": "024de5cf1ab6618b8b32de4c756e132db0142638"
  },
  {
    "commit": "800ca04e5582e8aae469dabed21b4a9126778edf",
    "tree": "4054231277c749be29b8d4036736a658f0291abb",
    "review_ref": "refs/heads/review/trial-cac-nvidia-d079-d080-d081-authoring-20261128",
    "path": "handoff/m02_completion_28_execution/L01a/INDEPENDENT_D079_D080_D081_JOINT_FIT_INERT_PROOF_AUTHORING_VERDICTS_20261128.md",
    "sha256": "7da0e899a4092d84b754a72e0a5df40c5339240238bff3b77b9b86359ad4b130",
    "git_blob": "7a5259a08bed63ee64d5673fc4d8bb5d20ebb35a",
    "bytes": 15203,
    "parent": "a021be5e8881c34a7f10383d70e7766290276817"
  },
  {
    "commit": "4a28e0f3f12676364d6846ab3878e1869508e656",
    "tree": "ffbbb537697897f4f5b93a33794090ea782e4757",
    "review_ref": "refs/heads/review/trial-cac-nvidia-d079-d080-d081-registration-installation-20261128",
    "path": "handoff/m02_completion_28_execution/L01a/INDEPENDENT_D079_D080_D081_JOINT_FIT_REGISTRATION_INSTALLATION_VERDICTS_20261128.md",
    "sha256": "c16a282a30b8061e07f8b14472aa13709d6e30f21c26d3bbb46b50d57a432a7f",
    "git_blob": "8a8f96d45d5fc7f3dc8a57698db1eec0e75c519f",
    "bytes": 21687,
    "parent": "e44c578ff93f53e3825f0c1212a56a96e7fcf603"
  },
  {
    "commit": "da309cbbeff0c0005a831690713c6233161655aa",
    "tree": "90fa5be3d0db2c7e743afbbbe63c8c43c79cf6d9",
    "review_ref": "refs/heads/review/trial-cac-nvidia-d079-d080-d081-registration-preparation-20261128",
    "path": "handoff/m02_completion_28_execution/L01a/INDEPENDENT_D079_D080_D081_JOINT_FIT_REGISTRATION_PREPARATION_VERDICTS_20261128.md",
    "sha256": "a0efdb0f36c60513da511adcba093e338a04226efa1ae7957ee3d555f0a21414",
    "git_blob": "6e3e8fbd56adab30b69b8ebb79e77eabe6286b2a",
    "bytes": 20406,
    "parent": "fbe5ed5c91477ea23f16bf50309040e30d650096"
  },
  {
    "commit": "14748c0711286bd383f613e2ed2e171506fe0ced",
    "tree": "1c7e65c4232254200163e465ae217d2b89ca90b5",
    "review_ref": "refs/heads/review/trial-cac-nvidia-d079-d080-d081-bindings-20261128",
    "path": "handoff/m02_completion_28_execution/L01a/INDEPENDENT_D079_D080_D081_JOINT_FIT_BINDING_ADMISSION_VERDICTS_20261128.md",
    "sha256": "c324511425928ab36048d5e5c9d7510f8a48a2b2f2586e58dd07b7b8404c2f31",
    "git_blob": "961a66aa669abaee1878ad618c7a5dd0b1951dd9",
    "bytes": 13744,
    "parent": "eaa4816c360f9df1e1974570e1c7b161efe6d08c"
  }
]
~~~

Direct ordered actual current histories D075/D071/D076/D077 and actual coefficients D079/D080/D081; transitive D072/D073/D074. Each of the ten separately cleared parent registrations, including own brief, binding, contract, proof family, descriptor, pointer and generation, remains unchanged from its respective exact installation candidate:
~~~json
{
  "D071": {
    "profile": {
      "profile_ref": {
        "id": "t01-l01a-d071-history",
        "version": 1
      },
      "calculation_definition_version": "T01-D071-ALIGNED-HISTORY-DEF-V1",
      "parameter_ref": {
        "id": "t01-l01a-d071-parameters",
        "version": 1
      },
      "selection_ref": {
        "id": "t01-l01a-d071-selection",
        "version": 1
      },
      "subject": "SPY",
      "members": [
        "SPY"
      ],
      "raw_dependencies": [
        "R037",
        "R042"
      ],
      "derived_dependencies": [],
      "kernel": "K03_CHANGE_RETURN",
      "parameter_profile": "P_WINDOW",
      "equation": "ln(current/reference)",
      "units": "return",
      "result_shape": "scalar_decimal",
      "future_own_brief_path": "handoff/m02_completion_28_execution/L01a/ALIGNED_HISTORY_D071_IMPLEMENTATION_BRIEF.md",
      "future_binding_path": "implementation/authority/T01_ALIGNED_HISTORY_D071_AUTHORITY_BINDING.yaml"
    },
    "registration_candidate": "74b15dd32ffb56dd645337e3607d907b72d4f563",
    "files_sha256": {
      "handoff/m02_completion_28_execution/L01a/ALIGNED_HISTORY_D071_IMPLEMENTATION_BRIEF.md": "65f2d0f9135f291773ab6081ec76892a967315df3ecb9c1760a4e2687a296e5e",
      "implementation/authority/T01_ALIGNED_HISTORY_D071_AUTHORITY_BINDING.yaml": "30cbb5fe2f8a1b720bc58b55b05f3c88b736401f03d03199404444b60330dc03",
      "handoff/m02_completion_28_execution/L01a/G01_PARTITION_REMAP_20261128/ALIGNED_HISTORY_D071_PROOF_CONTRACT.json": "5f771b88c96699b9dd56b724e9e87df6f541706bdfff442842ee70d4daaedb30",
      "tests/product/m02_completion_28_prospective/support/d071-history/test_profile.py": "5c3a920006e9952e58e2e7ec6efe477e8e48e1f51bea9d6e6ff7744e6c3f20df",
      "config/product_proof/m02_aligned_history_d071/claim.json": "cea962241291786b3c2606cc56f003b77809352c7643408af88487e8200cb526",
      "config/product_proof/m02_aligned_history_d071/admission.json": "bcfbb089756d5a6ab21a2a5cd63991aaad1f609f81ebbebb89aa90f706f98fb5",
      "config/product_proof/m02_aligned_history_d071/generations/0001.json": "985625000ee98f9adfdf334e391ee19e767ac1b804e25b9eb209d9bf82a68dda"
    },
    "ordered_nodes": [
      "tests/product/m02_completion_28_prospective/support/d071-history/test_profile.py::test_d071_history_success",
      "tests/product/m02_completion_28_prospective/support/d071-history/test_profile.py::test_d071_missing_exact_reference"
    ]
  },
  "D072": {
    "profile": {
      "profile_ref": {
        "id": "t01-l01a-d072-history",
        "version": 1
      },
      "calculation_definition_version": "T01-D072-ALIGNED-HISTORY-DEF-V1",
      "parameter_ref": {
        "id": "t01-l01a-d072-parameters",
        "version": 1
      },
      "selection_ref": {
        "id": "t01-l01a-d072-selection",
        "version": 1
      },
      "subject": "QQQ",
      "members": [
        "QQQ"
      ],
      "raw_dependencies": [
        "R037",
        "R042"
      ],
      "derived_dependencies": [],
      "kernel": "K03_CHANGE_RETURN",
      "parameter_profile": "P_WINDOW",
      "equation": "ln(current/reference)",
      "units": "return",
      "result_shape": "scalar_decimal",
      "future_own_brief_path": "handoff/m02_completion_28_execution/L01a/ALIGNED_HISTORY_D072_IMPLEMENTATION_BRIEF.md",
      "future_binding_path": "implementation/authority/T01_ALIGNED_HISTORY_D072_AUTHORITY_BINDING.yaml"
    },
    "registration_candidate": "74b15dd32ffb56dd645337e3607d907b72d4f563",
    "files_sha256": {
      "handoff/m02_completion_28_execution/L01a/ALIGNED_HISTORY_D072_IMPLEMENTATION_BRIEF.md": "4f8214d1ca11eaf0769206f3f322c799f44883bd266e63748e937dea5602b739",
      "implementation/authority/T01_ALIGNED_HISTORY_D072_AUTHORITY_BINDING.yaml": "637ff9b90b916ee69ee956db28e191ef86be3764ce2004b5fc24e371fa5869df",
      "handoff/m02_completion_28_execution/L01a/G01_PARTITION_REMAP_20261128/ALIGNED_HISTORY_D072_PROOF_CONTRACT.json": "1b1974b23aa8e79b6c420b0cb32f09ad34220d7672d7239bc0b425ce14ff82e3",
      "tests/product/m02_completion_28_prospective/support/d072-history/test_profile.py": "20e86ceee72f6e4190137dbde967c44aedd824ca7a89d2120ba20432e91821a3",
      "config/product_proof/m02_aligned_history_d072/claim.json": "1260a7c77fe9ac48c07b44cb53c3830df4a0f6b6d77c1824d224325613eb5abb",
      "config/product_proof/m02_aligned_history_d072/admission.json": "095cfc8c92a2d54cdac2a2b2001add96c3ea200ac1768bbec658185b031c308d",
      "config/product_proof/m02_aligned_history_d072/generations/0001.json": "385a1499264023184f5ce9ba2ea0f17efa5bdaa57b449a79a412ae1d6b524936"
    },
    "ordered_nodes": [
      "tests/product/m02_completion_28_prospective/support/d072-history/test_profile.py::test_d072_history_success",
      "tests/product/m02_completion_28_prospective/support/d072-history/test_profile.py::test_d072_wrong_reference_role"
    ]
  },
  "D073": {
    "profile": {
      "profile_ref": {
        "id": "t01-l01a-d073-history",
        "version": 1
      },
      "calculation_definition_version": "T01-D073-ALIGNED-HISTORY-DEF-V1",
      "parameter_ref": {
        "id": "t01-l01a-d073-parameters",
        "version": 1
      },
      "selection_ref": {
        "id": "t01-l01a-d073-selection",
        "version": 1
      },
      "subject": "SMH",
      "members": [
        "SMH"
      ],
      "raw_dependencies": [
        "R037",
        "R042"
      ],
      "derived_dependencies": [],
      "kernel": "K03_CHANGE_RETURN",
      "parameter_profile": "P_WINDOW",
      "equation": "ln(current/reference)",
      "units": "return",
      "result_shape": "scalar_decimal",
      "future_own_brief_path": "handoff/m02_completion_28_execution/L01a/ALIGNED_HISTORY_D073_IMPLEMENTATION_BRIEF.md",
      "future_binding_path": "implementation/authority/T01_ALIGNED_HISTORY_D073_AUTHORITY_BINDING.yaml"
    },
    "registration_candidate": "74b15dd32ffb56dd645337e3607d907b72d4f563",
    "files_sha256": {
      "handoff/m02_completion_28_execution/L01a/ALIGNED_HISTORY_D073_IMPLEMENTATION_BRIEF.md": "a7234477d581e6cba27e470919fa092c4ed5054d5a1aa31d2019d8fa94d16f48",
      "implementation/authority/T01_ALIGNED_HISTORY_D073_AUTHORITY_BINDING.yaml": "867444cecdf23c191269b1b3856410cc1ee6e3b81b8730dafa6d6528b78d6e0a",
      "handoff/m02_completion_28_execution/L01a/G01_PARTITION_REMAP_20261128/ALIGNED_HISTORY_D073_PROOF_CONTRACT.json": "0105ec67828efed9019c75808c6d79315ddb7c9e0c9a8a666d49b46cf9fcfdb5",
      "tests/product/m02_completion_28_prospective/support/d073-history/test_profile.py": "3a5289c5d1933fcf6c84ae0d520f316d56c33ce87ca86433204776fc123e6c3a",
      "config/product_proof/m02_aligned_history_d073/claim.json": "8e61dc08aa7324bdf128419096ac4afb85731e047ca4bfcc2da377e2f0f4a084",
      "config/product_proof/m02_aligned_history_d073/admission.json": "8193931644b5870a6785afec07686721159878b3823c15c15a49966bc026db45",
      "config/product_proof/m02_aligned_history_d073/generations/0001.json": "005801524cd9787e72581b49c0305226930e7ddad319bbb3d829988ad6845a8c"
    },
    "ordered_nodes": [
      "tests/product/m02_completion_28_prospective/support/d073-history/test_profile.py::test_d073_history_success",
      "tests/product/m02_completion_28_prospective/support/d073-history/test_profile.py::test_d073_late_current"
    ]
  },
  "D074": {
    "profile": {
      "profile_ref": {
        "id": "t01-l01a-d074-history",
        "version": 1
      },
      "calculation_definition_version": "T01-D074-ALIGNED-HISTORY-DEF-V1",
      "parameter_ref": {
        "id": "t01-l01a-d074-parameters",
        "version": 1
      },
      "selection_ref": {
        "id": "t01-l01a-d074-selection",
        "version": 1
      },
      "subject": "SOXX",
      "members": [
        "SOXX"
      ],
      "raw_dependencies": [
        "R037",
        "R042"
      ],
      "derived_dependencies": [],
      "kernel": "K03_CHANGE_RETURN",
      "parameter_profile": "P_WINDOW",
      "equation": "ln(current/reference)",
      "units": "return",
      "result_shape": "scalar_decimal",
      "future_own_brief_path": "handoff/m02_completion_28_execution/L01a/ALIGNED_HISTORY_D074_IMPLEMENTATION_BRIEF.md",
      "future_binding_path": "implementation/authority/T01_ALIGNED_HISTORY_D074_AUTHORITY_BINDING.yaml"
    },
    "registration_candidate": "74b15dd32ffb56dd645337e3607d907b72d4f563",
    "files_sha256": {
      "handoff/m02_completion_28_execution/L01a/ALIGNED_HISTORY_D074_IMPLEMENTATION_BRIEF.md": "524b2d2a4aa94a0c1c55ea376650d14648af67c46e73763ce3e8cc0f2e9e0c0e",
      "implementation/authority/T01_ALIGNED_HISTORY_D074_AUTHORITY_BINDING.yaml": "f2a2208a73d291e614577eaf2b81ffd13d699c4efbc2eeeb6258569ac8aa1c34",
      "handoff/m02_completion_28_execution/L01a/G01_PARTITION_REMAP_20261128/ALIGNED_HISTORY_D074_PROOF_CONTRACT.json": "708f6dc03c755e68c8232f699d80b2b27d973b7e2406daacf4f5fdc3f34d8d79",
      "tests/product/m02_completion_28_prospective/support/d074-history/test_profile.py": "e96123115973c985a75b7b978aad8a9b2cd65c7f63488a0ca76da036627d63d9",
      "config/product_proof/m02_aligned_history_d074/claim.json": "622726a8fa4da0cc4890390335d6f159aacc823f9a13917a007f2ef77f1eb94a",
      "config/product_proof/m02_aligned_history_d074/admission.json": "3487dd8714d7a80177c5bf4ffdfe89ca822805b7088872bde9e5d582e74b03b3",
      "config/product_proof/m02_aligned_history_d074/generations/0001.json": "837f47a8850459ed3e6de43159c72906d82e81d048a23b3c968b38726e1be761"
    },
    "ordered_nodes": [
      "tests/product/m02_completion_28_prospective/support/d074-history/test_profile.py::test_d074_history_success",
      "tests/product/m02_completion_28_prospective/support/d074-history/test_profile.py::test_d074_ambiguous_current"
    ]
  },
  "D075": {
    "profile": {
      "profile_ref": {
        "id": "t01-l01a-d075-history",
        "version": 1
      },
      "calculation_definition_version": "T01-D075-ALIGNED-HISTORY-DEF-V1",
      "parameter_ref": {
        "id": "t01-l01a-d075-parameters",
        "version": 1
      },
      "selection_ref": {
        "id": "t01-l01a-d075-selection",
        "version": 1
      },
      "subject": "NVDA",
      "members": [
        "NVDA"
      ],
      "raw_dependencies": [
        "R037",
        "R042"
      ],
      "derived_dependencies": [],
      "kernel": "K03_CHANGE_RETURN",
      "parameter_profile": "P_WINDOW",
      "equation": "ln(current/reference)",
      "units": "return",
      "result_shape": "scalar_decimal",
      "future_own_brief_path": "handoff/m02_completion_28_execution/L01a/ALIGNED_HISTORY_D075_IMPLEMENTATION_BRIEF.md",
      "future_binding_path": "implementation/authority/T01_ALIGNED_HISTORY_D075_AUTHORITY_BINDING.yaml"
    },
    "registration_candidate": "74b15dd32ffb56dd645337e3607d907b72d4f563",
    "files_sha256": {
      "handoff/m02_completion_28_execution/L01a/ALIGNED_HISTORY_D075_IMPLEMENTATION_BRIEF.md": "24ec8f08faf1a61059cee69b8c675767345809ae6a0dd90ab852a2fc30977750",
      "implementation/authority/T01_ALIGNED_HISTORY_D075_AUTHORITY_BINDING.yaml": "50120c02327ed212e8821ac3795d4f64daa3e38d77ecd5c92c7b20f6a2ba8c3f",
      "handoff/m02_completion_28_execution/L01a/G01_PARTITION_REMAP_20261128/ALIGNED_HISTORY_D075_PROOF_CONTRACT.json": "6bfc41f1415ff9c68776f0ae79c6b35ec19cb3e0a16dc2a0706970be57dc8d8f",
      "tests/product/m02_completion_28_prospective/support/d075-history/test_profile.py": "4fdeed336e1fa67db77c577755d14810bf576cdbf72d393993d0c98e1802a94c",
      "config/product_proof/m02_aligned_history_d075/claim.json": "19d2f6e7c31089158bb7aa6fa4fafb00fd0448e4e8db1f16bbd581315dbbaf13",
      "config/product_proof/m02_aligned_history_d075/admission.json": "2d355fa058ad406c9855199c163cb48d5298b9f405d8e5f18d547384754bde5f",
      "config/product_proof/m02_aligned_history_d075/generations/0001.json": "18171abfb47452e2600f5169fa80a26c70d2b4a4045b0c167070356a954330ca"
    },
    "ordered_nodes": [
      "tests/product/m02_completion_28_prospective/support/d075-history/test_profile.py::test_d075_history_success",
      "tests/product/m02_completion_28_prospective/support/d075-history/test_profile.py::test_d075_original_units"
    ]
  },
  "D076": {
    "profile": {
      "profile_ref": {
        "id": "t01-l01a-d076-history",
        "version": 1
      },
      "calculation_definition_version": "T01-D076-ALIGNED-HISTORY-DEF-V1",
      "parameter_ref": {
        "id": "t01-l01a-d076-parameters",
        "version": 1
      },
      "selection_ref": {
        "id": "t01-l01a-d076-selection",
        "version": 1
      },
      "subject": "US_TECH_VS_BROAD",
      "members": [
        "QQQ",
        "SPY"
      ],
      "raw_dependencies": [],
      "derived_dependencies": [
        "D072",
        "D071"
      ],
      "kernel": "K02_ALGEBRA",
      "parameter_profile": "P_BASIC",
      "equation": "D072-D071",
      "units": "return_spread",
      "result_shape": "exact_ratio",
      "future_own_brief_path": "handoff/m02_completion_28_execution/L01a/ALIGNED_HISTORY_D076_IMPLEMENTATION_BRIEF.md",
      "future_binding_path": "implementation/authority/T01_ALIGNED_HISTORY_D076_AUTHORITY_BINDING.yaml"
    },
    "registration_candidate": "949904d4897da89fe644bc092b39ee523e9b96fc",
    "files_sha256": {
      "handoff/m02_completion_28_execution/L01a/ALIGNED_HISTORY_D076_IMPLEMENTATION_BRIEF.md": "c2b30721c0f535d00bb09cb801461ddf875966a93049c47fe572856f43fde480",
      "implementation/authority/T01_ALIGNED_HISTORY_D076_AUTHORITY_BINDING.yaml": "6f1324ab9922a1cd8b9994da931ee8f946d7d8666a758f8554269d092d006a80",
      "handoff/m02_completion_28_execution/L01a/ALIGNED_HISTORY_D076_PROOF_CONTRACT.json": "f18fa3573706bb48b28fd2f7ddb1e39a5ad51dd0ac76cb22e6b1db7c46b8aca5",
      "tests/product/m02_completion_28_prospective/support/d076-history/test_profile.py": "03afd668f2b0f85f276bf6df285b71cfc7ef181fd3e02d536d06c702aca6eecb",
      "config/product_proof/m02_aligned_history_d076/claim.json": "d6309aecacd15eb018b003b679b2c1c3964249c19f89ed7ffd0d21a1901832e8",
      "config/product_proof/m02_aligned_history_d076/admission.json": "b07d4c6be6d46c6766fd701e26bfbd9aaf3facd7e0c09e53c5e244be024b2f75",
      "config/product_proof/m02_aligned_history_d076/generations/0001.json": "011d0a9ad42926f85cbfb5e91e78ff83b9a8680d18a7c98a3198033f1ba01904"
    },
    "ordered_nodes": [
      "tests/product/m02_completion_28_prospective/support/d076-history/test_profile.py::test_d076_history_success",
      "tests/product/m02_completion_28_prospective/support/d076-history/test_profile.py::test_d076_wrong_parent_frame"
    ]
  },
  "D077": {
    "profile": {
      "profile_ref": {
        "id": "t01-l01a-d077-history",
        "version": 1
      },
      "calculation_definition_version": "T01-D077-ALIGNED-HISTORY-DEF-V1",
      "parameter_ref": {
        "id": "t01-l01a-d077-parameters",
        "version": 1
      },
      "selection_ref": {
        "id": "t01-l01a-d077-selection",
        "version": 1
      },
      "subject": "SEMIS_VS_TECH",
      "members": [
        "SMH",
        "SOXX",
        "QQQ"
      ],
      "raw_dependencies": [],
      "derived_dependencies": [
        "D073",
        "D074",
        "D072"
      ],
      "kernel": "K02_ALGEBRA",
      "parameter_profile": "P_BASIC",
      "equation": "(D073+D074)/2-D072",
      "units": "return_spread",
      "result_shape": "exact_ratio",
      "future_own_brief_path": "handoff/m02_completion_28_execution/L01a/ALIGNED_HISTORY_D077_IMPLEMENTATION_BRIEF.md",
      "future_binding_path": "implementation/authority/T01_ALIGNED_HISTORY_D077_AUTHORITY_BINDING.yaml"
    },
    "registration_candidate": "531fe3e5955e0e680e31cc6b983a625f6f36b747",
    "files_sha256": {
      "handoff/m02_completion_28_execution/L01a/ALIGNED_HISTORY_D077_IMPLEMENTATION_BRIEF.md": "88bdd385ff91432940f4d27a8cff2bce6af22a8c85b858f53ba2f674d3c30a3c",
      "implementation/authority/T01_ALIGNED_HISTORY_D077_AUTHORITY_BINDING.yaml": "7f1b9f882d815616aa8e2fe53d6069800c7524f375202bff4eea5a67bf91a735",
      "handoff/m02_completion_28_execution/L01a/ALIGNED_HISTORY_D077_PROOF_CONTRACT.json": "49c27e77c80a22382715753a14e48063edf532ab30965e85d7c12eca72c5334a",
      "tests/product/m02_completion_28_prospective/support/d077-history/test_profile.py": "3b31555bc6261ee32ab16b1ccb474cd09d164b642d37b99309a97fca4e2b019e",
      "config/product_proof/m02_aligned_history_d077/claim.json": "96ed7bf333ede3ed7d038b542c36cede906d6a1f7873ee4595ed4944595594d5",
      "config/product_proof/m02_aligned_history_d077/admission.json": "aff0d35a203980ed17b0cf70774055846e2c81865c0b694b6dcbb00972e65b10",
      "config/product_proof/m02_aligned_history_d077/generations/0001.json": "caab1dcd3876c09052fbe308b8d4af63271e114a2b1b8940a276a9ce212f2d8d"
    },
    "ordered_nodes": [
      "tests/product/m02_completion_28_prospective/support/d077-history/test_profile.py::test_d077_history_success",
      "tests/product/m02_completion_28_prospective/support/d077-history/test_profile.py::test_d077_missing_soxx_parent",
      "tests/product/m02_completion_28_prospective/support/d077-history/test_profile.py::test_d077_mixed_original_roster"
    ]
  },
  "D079": {
    "profile": {
      "profile_ref": {
        "id": "t01-l01a-d079-joint-fit",
        "version": 1
      },
      "calculation_definition_version": "T01-D079-ALIGNED-JOINT-FIT-DEF-V1",
      "parameter_ref": {
        "id": "t01-l01a-joint-fit-parameters",
        "version": 1
      },
      "selection_ref": {
        "id": "t01-l01a-d079-selection",
        "version": 1
      },
      "subject": "NVDA",
      "members": [
        "NVDA",
        "SPY",
        "QQQ",
        "SMH",
        "SOXX"
      ],
      "raw_dependencies": [],
      "derived_dependencies": [
        "D075",
        "D071",
        "D076",
        "D077"
      ],
      "kernel": "K06_REGRESSION_DEPENDENCE",
      "parameter_profile": "P_REGRESSION",
      "equation": "beta_market from joint OLS with intercept",
      "units": "beta",
      "result_shape": "exact_ratio",
      "future_own_brief_path": "handoff/m02_completion_28_execution/L01a/ALIGNED_HISTORY_D079_IMPLEMENTATION_BRIEF.md",
      "future_binding_path": "implementation/authority/T01_ALIGNED_HISTORY_D079_AUTHORITY_BINDING.yaml"
    },
    "registration_candidate": "b6b798d827d6b6acce0916ccf36896d878242bee",
    "files_sha256": {
      "handoff/m02_completion_28_execution/L01a/ALIGNED_HISTORY_D079_IMPLEMENTATION_BRIEF.md": "47b4c5d27d7ffc57710d70973825500524e3d9bbc179cc59df0d356381612127",
      "implementation/authority/T01_ALIGNED_HISTORY_D079_AUTHORITY_BINDING.yaml": "c90aec925d606bcf9537ffad014338a579ab856884d659a85dd4ecd10050cf54",
      "handoff/m02_completion_28_execution/L01a/ALIGNED_HISTORY_D079_PROOF_CONTRACT.json": "c578377c28db037bfb62a91dc80542b2d1ea737f1cdee00a35c58243f9f0f6f6",
      "tests/product/m02_completion_28_prospective/d079/test_signal.py": "4443fe1f612481dbb1048c2098d8eb02e3eb00c22e73a2944acae5b96ad89513",
      "config/product_proof/m02_aligned_history_d079/claim.json": "c1917cd966ac60bb6b5fad13100c623b19a10e8bf841ba8cf0762d4f105d5e68",
      "config/product_proof/m02_aligned_history_d079/admission.json": "4fc917d7456c36f47da0ab27e207916280ac946bec370eeedcfa7844d30b2607",
      "config/product_proof/m02_aligned_history_d079/generations/0001.json": "ea6323156db757e60be9a507ec34b3a0bc9565f4425f67db94fd070dc0b9a7a3"
    },
    "ordered_nodes": [
      "tests/product/m02_completion_28_prospective/d079/test_signal.py::test_d079_joint_success",
      "tests/product/m02_completion_28_prospective/d079/test_signal.py::test_d079_rank_deficient",
      "tests/product/m02_completion_28_prospective/d079/test_signal.py::test_d079_missing_member",
      "tests/product/m02_completion_28_prospective/d079/test_signal.py::test_d079_duplicate_member",
      "tests/product/m02_completion_28_prospective/d079/test_signal.py::test_d079_parent_unavailable_at_cutoff",
      "tests/product/m02_completion_28_prospective/d079/test_signal.py::test_d079_mixed_source_corpus"
    ]
  },
  "D080": {
    "profile": {
      "profile_ref": {
        "id": "t01-l01a-d080-joint-fit",
        "version": 1
      },
      "calculation_definition_version": "T01-D080-ALIGNED-JOINT-FIT-DEF-V1",
      "parameter_ref": {
        "id": "t01-l01a-joint-fit-parameters",
        "version": 1
      },
      "selection_ref": {
        "id": "t01-l01a-d080-selection",
        "version": 1
      },
      "subject": "NVDA",
      "members": [
        "NVDA",
        "SPY",
        "QQQ",
        "SMH",
        "SOXX"
      ],
      "raw_dependencies": [],
      "derived_dependencies": [
        "D075",
        "D071",
        "D076",
        "D077"
      ],
      "kernel": "K06_REGRESSION_DEPENDENCE",
      "parameter_profile": "P_REGRESSION",
      "equation": "beta_tech from joint OLS with intercept",
      "units": "beta",
      "result_shape": "exact_ratio",
      "future_own_brief_path": "handoff/m02_completion_28_execution/L01a/ALIGNED_HISTORY_D080_IMPLEMENTATION_BRIEF.md",
      "future_binding_path": "implementation/authority/T01_ALIGNED_HISTORY_D080_AUTHORITY_BINDING.yaml"
    },
    "registration_candidate": "b6b798d827d6b6acce0916ccf36896d878242bee",
    "files_sha256": {
      "handoff/m02_completion_28_execution/L01a/ALIGNED_HISTORY_D080_IMPLEMENTATION_BRIEF.md": "69f38747173cd464ae8586f919caa23f8ae754fbb1190b001675cae05e5a709e",
      "implementation/authority/T01_ALIGNED_HISTORY_D080_AUTHORITY_BINDING.yaml": "dcc6589fe36f091f4ea68da97b011ec67ea416e706e1ba9089da8223e1cd84d7",
      "handoff/m02_completion_28_execution/L01a/ALIGNED_HISTORY_D080_PROOF_CONTRACT.json": "432695b81c5d68a1cb4cb90b0c63d67b0f9dd02fb370a60266e827461a40dbbb",
      "tests/product/m02_completion_28_prospective/d080/test_signal.py": "da03c81d83fe2eed977cec552152ed515f04d4359242e33753b1d04a92b0c821",
      "config/product_proof/m02_aligned_history_d080/claim.json": "415842006ecc8502d1ab2787a41d2d5eb22111d59a7b8ffb120133202a9c9a8c",
      "config/product_proof/m02_aligned_history_d080/admission.json": "c62b03e0b0b15f1fb0789fa49d704b0f5baeaf17dc46f9386d05c9d55e159ad9",
      "config/product_proof/m02_aligned_history_d080/generations/0001.json": "2213976d56bbf0b29d62bd0de2e4d9290af388c0f61ce65447952ec591281b52"
    },
    "ordered_nodes": [
      "tests/product/m02_completion_28_prospective/d080/test_signal.py::test_d080_joint_success",
      "tests/product/m02_completion_28_prospective/d080/test_signal.py::test_d080_rank_deficient",
      "tests/product/m02_completion_28_prospective/d080/test_signal.py::test_d080_outside_conditioning_domain",
      "tests/product/m02_completion_28_prospective/d080/test_signal.py::test_d080_condition_inclusive_boundary",
      "tests/product/m02_completion_28_prospective/d080/test_signal.py::test_d080_fit_row_misalignment"
    ]
  },
  "D081": {
    "profile": {
      "profile_ref": {
        "id": "t01-l01a-d081-joint-fit",
        "version": 1
      },
      "calculation_definition_version": "T01-D081-ALIGNED-JOINT-FIT-DEF-V1",
      "parameter_ref": {
        "id": "t01-l01a-joint-fit-parameters",
        "version": 1
      },
      "selection_ref": {
        "id": "t01-l01a-d081-selection",
        "version": 1
      },
      "subject": "NVDA",
      "members": [
        "NVDA",
        "SPY",
        "QQQ",
        "SMH",
        "SOXX"
      ],
      "raw_dependencies": [],
      "derived_dependencies": [
        "D075",
        "D071",
        "D076",
        "D077"
      ],
      "kernel": "K06_REGRESSION_DEPENDENCE",
      "parameter_profile": "P_REGRESSION",
      "equation": "beta_semi from joint OLS with intercept",
      "units": "beta",
      "result_shape": "exact_ratio",
      "future_own_brief_path": "handoff/m02_completion_28_execution/L01a/ALIGNED_HISTORY_D081_IMPLEMENTATION_BRIEF.md",
      "future_binding_path": "implementation/authority/T01_ALIGNED_HISTORY_D081_AUTHORITY_BINDING.yaml"
    },
    "registration_candidate": "b6b798d827d6b6acce0916ccf36896d878242bee",
    "files_sha256": {
      "handoff/m02_completion_28_execution/L01a/ALIGNED_HISTORY_D081_IMPLEMENTATION_BRIEF.md": "cf2bf8c51611b8b5baf8a98d1f42fcecd63f069dd45b20dc9135844b99b6e90f",
      "implementation/authority/T01_ALIGNED_HISTORY_D081_AUTHORITY_BINDING.yaml": "a2dfca758a22fbe7898d7534a86d094457333ad74ef5022ffd0d968334183eae",
      "handoff/m02_completion_28_execution/L01a/ALIGNED_HISTORY_D081_PROOF_CONTRACT.json": "2a68e4250b30c5b9dd1afedf930d67dd7ee115830229850e2b1a832db7ea2265",
      "tests/product/m02_completion_28_prospective/d081/test_signal.py": "00fd94687c23b0d967a1e97228e513c0b8e92fa1398894647fedc4c8070ec82d",
      "config/product_proof/m02_aligned_history_d081/claim.json": "3da1c15a7f358beb23524c3bbc4e87de6c978af471407caf291ad4bb58683613",
      "config/product_proof/m02_aligned_history_d081/admission.json": "c8a09e1dea607dc2bee359a42e37daad85ab59cd20e60dd0a695f4177a59e984",
      "config/product_proof/m02_aligned_history_d081/generations/0001.json": "3e6c648336e6879879eb7d582adce055a138db931e89f6f83cbb297f0044e698"
    },
    "ordered_nodes": [
      "tests/product/m02_completion_28_prospective/d081/test_signal.py::test_d081_joint_success",
      "tests/product/m02_completion_28_prospective/d081/test_signal.py::test_d081_rank_deficient",
      "tests/product/m02_completion_28_prospective/d081/test_signal.py::test_d081_shared_parent_payload_mismatch"
    ]
  }
}
~~~

Current committed source surfaces, exact unchanged bytes of independently reviewed L02 source candidate f5f8a2b73ba1cf41fb4807e2f5544ec2e135c0bb (shared history code unchanged from D077):
~~~json
{
  "src/nvda_desk/market_measurement_truth/api.py": "d03b137181b529b187448e8e7a476223f0c2665c7267b11f29f52a28706560d8",
  "src/nvda_desk/market_measurement_truth/_aligned_joint_fit.py": "d7eb222791317c44e766de9d2d267710f99bc2b83b386f5afc7bd1c2703cf9d6",
  "src/nvda_desk/market_measurement_truth/_aligned_history_source.py": "f967e122a3ff138401c891987763af37c64b6500ed39672e692b5eb40abbb8cd",
  "src/nvda_desk/market_measurement_truth/_aligned_history_returns.py": "24265ff5b03a35f87aea1b609b578e88d636d786fe25d29c6df69d3dd8a86c46",
  "src/nvda_desk/market_measurement_truth/_aligned_history_codec.py": "c04e6c3e9dd46e2fe0e84f4bdbdb5d300c2cb443534251c179847fef28f7395c",
  "src/nvda_desk/market_measurement_truth/_native_codec.py": "b3d247b4396073d5059e674b9392c03e1b9ce3e418b9a9f1df56417255847759",
  "src/nvda_desk/market_measurement_truth/_record_store.py": "882a61238b74ba5aa2ffacf95d0587633392722d2336a3954681c6ac0a86f0ef",
  "src/nvda_desk/market_measurement_truth/_log_return.py": "3478d5b0e8361f6339c9a0ec5bb70343f2e687338dad0947f7d8a86c0ebf47cf",
  "src/nvda_desk/raw_signal_occurrence_truth/api.py": "cda0dfe957ce6a51a486cbacb78f3f1b50ec9abac4458f8e69b659bf43b0f01d",
  "tools/product_proof_claims.py": "1794f09ab2e292a2c2f202f61e177315b10a3d7f5a4f300d07363265779e3e17"
}
~~~

## Actual stable parent seam and required future D078 construction

Existing public create_aligned_history_source/owner/reader and AlignedHistoryRequestV1 produce exact D071-D075 underlying and D076/D077 relative histories. D076 ordered concrete D072/D071, D077 ordered D073/D074/D072. Each exact own admission and actual read-only store; ordinary get_derived_occurrence on requested identity, no implicit latest or private SQL. Current AlignedHistoryOccurrenceV1 contains exact original observations/projections or complete nested actual relative predecessors, role/profile/definition/selection/context, row cutoff and first calculated_at; ordinary durable reader semantically recomputes and compares full canonical bytes. No parent modification required.

Existing create_aligned_coefficient_owner and create_aligned_coefficient_reader with AlignedFitRequestV1/AlignedFitRowRequestV1, exact per-component admissions and four ordered actual history read stores yield AlignedCoefficientOccurrenceV1. Actual fit retains common fit_id, fit_profile_ref, source_policy_sha256, model_version, numeric_version, origin_slot, effective_as_of_utc, knowledge_cutoff_utc, ordered row_slots, all six actual typed rows, member IDs and complete canonical payload hashes, determinant, condition, intercept, beta_market, beta_tech, beta_semi as exact ratios. Each occurrence binds own component/definition/profile, result, fit, knowledge and first calculated_at. _fit_bytes encodes all nested actual histories and full named vector; _fit_identity excludes fit_id only, and component _identity excludes only own ID/calculated_at. Thus separately materialised components of identical actual sample carry exact same manifest despite own timestamp; actual different corpus/fit retains different full manifest. Ordinary read-only _store validates by full _produce recomputation from retained rows and compares _encode bytes; first calculation survives replay. Public getters can see lawful late first calculation; explicit decision-ceiling test remains mandatory. No inferred product acceptance.

Append only new AlignedResidualRequestV1, AlignedResidualOccurrenceV1, AlignedResidualReadsV1/OwnerV1 and create_aligned_residual_owner/reader. Separate exact own D078 admission and profile, seven ordered concrete read-only stores (D075,D071,D076,D077 and D079,D080,D081) and fresh distinct own SQLite write storage; no arbitrary injected predecessor adapter, no coefficient-owner authority substitution for D078. Exact S7 asof 2026-10-20T12:40:00Z, current history cutoff +1, residual allowed cutoff +4 or +7, now >= requested cutoff. Request fixes actual seven IDs, role/order, own definition/profile/parameter/selection/context; no inferred latest, no caller-provided numeric result, no mutable selected data. Actual typed coefficient local validity by their own unchanged exact admitted semantic producer/codec and ordinary reads; durable D078 validates nested coefficients by the same law, not by trusting their labels or hashes. All seven IDs distinct before lookup.

Exact residual validation order from adopted R1:
~~~json
[
  "REQUEST_SHAPE_PROFILE",
  "PARENT_ID_UNIQUENESS_AND_LOOKUP",
  "COEFFICIENT_LOCAL_VALIDITY_AND_ROLES",
  "SAME_FIT_ID_AND_EXACT_MANIFEST",
  "FIT_ORIGIN_STRICT_PRIOR",
  "COEFFICIENT_AVAILABILITY",
  "CURRENT_ROW_ALIGNMENT_AND_AVAILABILITY",
  "CURRENT_SOURCE_APPLICABILITY",
  "EXACT_RESIDUAL",
  "DURABLE_APPEND"
]
~~~

After actual local validity and roles, require identical actual fit ID AND exact canonical complete fit manifest bytes for all three (including actual sample, full intercept/vector, profile/policy/model/numeric lineage and cutoff). Actual named component result must equal manifest field for its role. Coherent alternative complete fit is not invalid merely for different label; do not reject genuine B on that basis. Then strict prior actual origin/asof before current S7 (separate from availability). Then check actual coefficient knowledge cutoff and first calculated_at <= residual decision cutoff for each of three using existing _aligned_joint_fit._visible; also actual fit cutoff <= residual cutoff. No later-now substitution; current row uses same ceiling.

For actual current row use unchanged _lookup_rows, _align_row, _shared_underlying, _same_parent, _visible, _row_originals and _checked_rows semantics (same common row path live and durable). _checked_rows needs actual parent authority context and frame metadata only; preserve exact D078 own authority independently and supply the existing exact parent authorities, not a fabricated coefficient or residual parent. Current row request is slot S7 and four exact ordered IDs; _align_row recomputes actual typed underlying or relative parent canonical bytes, context and slot. Both actual shared D071 and D072 comparisons require identical ID AND complete canonical payload including first calculation; no hash-only or value equivalence. Use _checked_rows against residual cutoff for all four current histories; reuse unchanged complete actual original-content corpus check _check_corpus over union of actual prior manifest S1..S6 originals plus current S7 (70 distinct originals, exact required keys, not independent per-row membership). Prior manifest is already locally validated; reconstruct selected originals by the same shared row/corpus law; no new parallel implementation or weakened visibility predicate. Do not rerun fit to obtain a residual or repair inconsistent input; local validation recomputes actual parent law only. Arithmetic uses the actual common intercept and actual named beta values, actual D075 minus intercept and all three actual factor contributions, exact Fraction and canonical reduced signed ratio with positive denominator, zero 0/1 and bounded intermediate 4096-bit rational arithmetic consistent with committed fit law. No float, fallback, clipping, oracle input or independent per-factor fit.

Durable D078 occurrence retains own request/definition/profile/selection/context, actual four current typed history and three coefficient typed nested canonical envelopes with full common manifest, exact signed reduced ratio, units return, shape exact_ratio, actual asof/cutoff/first calculated_at and exact policy/version. Explicit versioned canonical typed mapping envelope; mmtaresidual1:SHA256 excluding own ID/calculated_at only. Reuse unchanged RecordState and native/parent codecs; exact key/type reconstruction, semantic revalidation and byte re-encode on ordinary read-only reopen without live sources/owners/stores; same-owner replay returns original bytes and first timestamp, one durable row. Business refusal returns None and no append, technical persistence failure propagates. Fresh separate lawful stores per specimen/role/case. Retain all existing parent and legacy DTOs, source paths, proof/registrations and G01 routes unchanged; independently assess future additive changes and invalidation. No source edit now.

## Exact five held cases and reached invariants

### D078-CONTROLLED-SUCCESS — SAME_PRIOR_FIT_RESIDUAL_AND_DURABLE_REOPEN

Original node: `tests/product/m02_completion_28/d078/test_signal.py::test_d078_same_fit_residual`

Remapped node: `tests/product/m02_completion_28_prospective/d078/test_signal.py::test_d078_same_fit_residual`

Exact complete original case SHA256: b442c3215ea653bea9e3de82707478235390c7a11c8a122204273933a8409255

Exact successful same-fit residual and durable reopen/replay

Independent oracle (assert only, never input):
~~~json
{
  "actual_residual_ratio": [
    24875827132920207120538393860651854221699024850147,
    1000000000000000000000000000000000000000000000000000
  ],
  "normalized_residual": [
    5,
    2
  ],
  "actual_rows": 1,
  "expected": "Actual complete prior A triplet with common fit ID, actual current S7 row, exact signed 5a/2 return; use actual coefficients and common intercept, not refitting or zeroing. Preserve complete actual nested coefficients and current source facts. Later retry same first timestamp; ordinary read-only reopen after dropping live source/owners/parents; one row."
}
~~~

### D078-CONTROLLED-REACHED_REFUSAL — SAME_FIT_ID_AND_EXACT_MANIFEST

Original node: `tests/product/m02_completion_28/d078/test_signal.py::test_d078_mixed_fit`

Remapped node: `tests/product/m02_completion_28_prospective/d078/test_signal.py::test_d078_mixed_fit`

Exact complete original case SHA256: c0c2b4a5b0bca115e808c210bdbb58bf27085bdab61e9d112714a2945bf2f4a7

Two separately materialised full lawful prior triplets, same origin, cutoffs, numeric condition and profile, distinct actual fit IDs, all local payloads valid. B only changes actual NVDA S1 source value/ID; all current S7 raw/derived facts identical, actual S7 applicability common. No D078-B success call. Combine one actual B semi coefficient with two actual A coefficients.

Independent oracle (assert only, never input):
~~~json
{
  "actual_rows": 0,
  "expected": "None; request shape, roles, local validity, actual availability and current source applicable; actual one B coefficient differs in fit lineage. Refuse same-fit predicate, no arbitrary mismatch/fabricated ID, re-fit or fallback; writer/reopened residual store empty. Preserve both complete actual triplets and current facts."
}
~~~

### D078-CURRENT-ROW-MISALIGNMENT — CURRENT_ROW_ALIGNMENT_AND_AVAILABILITY

Original node: `tests/product/m02_completion_28/d078/test_signal.py::test_d078_wrong_current_row`

Remapped node: `tests/product/m02_completion_28_prospective/d078/test_signal.py::test_d078_wrong_current_row`

Exact complete original case SHA256: a3c118f8dda3ea0eef2c5a2ac727369a82efb665de19b3125a75fc0de7405650

Actual prior A triplet common valid, actual full S7 current row exists; also actual lawful D076 S6 exists and is available. Request substitutes exactly D076 S6 ID while retaining other three S7 current IDs; no malformed arity, role or missing parent.

Independent oracle (assert only, never input):
~~~json
{
  "actual_rows": 0,
  "expected": "None; valid same prior triplet and actual lawful current role from wrong row; reach row time/context/cutoff alignment, no inferred latest replacement. Empty writer/reopened residual store; all actual parents preserved."
}
~~~

### D078-NONPRIOR-FIT — FIT_ORIGIN_STRICT_PRIOR

Original node: `tests/product/m02_completion_28/d078/test_signal.py::test_d078_nonprior_fit`

Remapped node: `tests/product/m02_completion_28_prospective/d078/test_signal.py::test_d078_nonprior_fit`

Exact complete original case SHA256: dbf4c920d04de834f9f572503318f711f02c259086d98bc71e89c83b5e4476b9

Actual complete lawful conditioned C triplet fit S2..S7, determinant164, kappa1664/41, common fit ID, first calculation S7+5. Actual lawful current S7 row included in that fit. Residual cutoff +7, now +8: all actual parent and coefficient times <= cutoff; same coherent applicable source/row/profile and fit vector. Fit origin equals current, sole strict-prior violation.

Independent oracle (assert only, never input):
~~~json
{
  "actual_rows": 0,
  "condition": [
    1664,
    41
  ],
  "expected": "None; actual individually valid same fit available by allowed residual cutoff, origin equal current. No conditioning, missing input, future visibility or mixed-fit confound. No current-in-fit residual emission. Empty writer/reopened residual store, all actual histories and triplet retained."
}
~~~

### D078-COEFFICIENT-NOT-KNOWN-AT-RESIDUAL-CUTOFF — COEFFICIENT_AVAILABILITY

Original node: `tests/product/m02_completion_28/d078/test_signal.py::test_d078_coefficient_unavailable_at_cutoff`

Remapped node: `tests/product/m02_completion_28_prospective/d078/test_signal.py::test_d078_coefficient_unavailable_at_cutoff`

Exact complete original case SHA256: 57c268e9d79e7ed8c0a7bc8f1decae1ab9768d48bf842499ae89f3e224b71dd4

All three actual coefficient occurrences are valid, exact same common A fit manifest and fit origin S6 strictly prior to S7. D079/D080 actual first S6+5 visible; actual D081 first S7+5 is reader-visible at actual residual now but not S7+4 residual cutoff. All actual current four parents aligned and cutoff-visible. Only D081 actual first calculated_at fails; no mixed/nonprior/current row mismatch or wrong coefficient. Same common fit identity omits component own calculated_at.

Independent oracle (assert only, never input):
~~~json
{
  "actual_rows": 0,
  "actual_late_component": "D081",
  "actual_component_first_calculated_at": "2026-10-20T12:40:05Z",
  "actual_residual_cutoff": "2026-10-20T12:40:04Z",
  "expected": "None at actual coefficient cutoff visibility after same-fit and strictly prior origin. All actual lawful coefficients and current history preserved, empty writer and ordinary reopened residual store. No use of later actual now, substitution or refit."
}
~~~

Independent stdlib literal arithmetic only (normalise by a = unchanged canonical log(101/100); actual exact result ratio is the pinned oracle, not runtime input):
~~~json
{
  "A": [
    "51",
    "1269/34",
    [
      "4/17",
      "-11/34",
      "3/34",
      "-14/17"
    ]
  ],
  "B": [
    "51",
    "1269/34",
    [
      "8/17",
      "-151/102",
      "-25/51",
      "-28/17"
    ]
  ],
  "C_S7": [
    "164",
    "1664/41",
    [
      "2/41",
      "243/164",
      "67/82",
      "31/41"
    ]
  ],
  "normalized_residual": "5/2"
}
~~~
A/B differ only actual S1 NVDA R037 original, same S7 full actual source records and same Gram rank/condition, distinct valid actual fit manifests. C S7 full-rank det164, condition 1664/41 <=50, actual same current origin and available by +7. Actual late D081 keeps the prior S6 fit cutoff/manifest, first S7+5 only; actual residual +4 cutoff refuses after same fit/prior. D076 S6 wrong current row is a lawful distinct actual occurrence and must reach row alignment, not lookup failure. A success has nonzero normalized residual 5/2. Exact five original complete case objects pinned by sorted-key compact UTF-8 JSON SHA256; full setup/clock/oracle fields in original inventory and reviewed ledger mandatory, no merge or addition.

## Future bounded changed paths — NOT authorised now

- src/nvda_desk/market_measurement_truth/api.py (append-only new residual API).
- src/nvda_desk/market_measurement_truth/_aligned_residual.py (new exact own residual implementation; reuse unchanged shared fit/history/visibility/corpus guards).
- tools/product_proof_claims.py (one fixed additive own G01 route dormant pending separately reviewed registration).
- tests/product/m02_completion_28_prospective/d078/test_signal.py and handoff/m02_completion_28_execution/L01a/ALIGNED_HISTORY_D078_PROOF_CONTRACT.json (only separately commissioned proof authoring/installation).
- implementation/authority/T01_ALIGNED_HISTORY_D078_AUTHORITY_BINDING.yaml and config/product_proof/m02_aligned_history_d078/{claim.json,admission.json,generations/0001.json} (only later separately reviewed exact installation).

No proof/source change, installation or active registration here. Independent exact binding/admission review required before later binding installation and inert proof authoring. Product execution release remains false, actual independently accepted parent product evidence mandatory; sole strict Tester unchanged. Preserve 64 held and 67 historical accepted results, seven history and three L02 registrations, all parent/legacy/G01, D078 legacy, D004/D085 held, D145 PAUSED and G01 R2 unadopted, main and original branch.
