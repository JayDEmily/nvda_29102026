# D080 exact L02 aligned-history joint-fit implementation brief — 28 November 2026

Jurisdiction M02-C28-D080; claim neutral_market_measurement_truth_d080; family m02_l02_joint_fit_d080; exact nonfungible allocation 5. Conditional inert preparation ONLY, pending independent binding/admission review. Base d2448b4e93281b9ca3db158497e3fe503816b0c7, tree 05ab6d0461cc3866039adf3752cbb7a8efe6e4fa. Owner exact64 grant and independent R1 policy/finite34 review control. This brief does not authorise installation, proof authoring, source edits, registration or any execution.

## Exact own adopted profile

~~~json
{
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
}
~~~

## Exact authority and actual committed parent pins

Authority files (path to SHA256):
~~~json
{
  "handoff/m02_completion_28_execution/L01a/ALIGNED_HISTORY_SOURCE_POLICY_PROPOSED_20261126.json": "9ba56098c273007980c893db39931ac86e7a3185bbb665f8c3f1e14f99b72af1",
  "handoff/m02_completion_28_execution/L01a/ALIGNED_HISTORY_FINITE_SPECIMENS_PROPOSED_20261126.json": "bb03481de75e1820c7aff61777a4a3aa4f676440ec03e373a05c032a0417c76d",
  "handoff/m02_completion_28_execution/L01a/ALIGNED_HISTORY_JOINT_FIT_FINITE_CASES_PROPOSED_20261126.json": "3be150f2998b4187a81720b424c848099edeba7a9f638ae90d9aae95d4c5d5c1",
  "handoff/m02_completion_28_execution/L01a/G01_PARTITION_REMAP_20261128/PATH_ONLY_SUCCESSOR_AUTHORITY.json": "11d90adf234d5195d3bd31a6b42df9b046c4ad53690cb279ef071d52b3049aa7",
  "handoff/m02_completion_28_execution/TEST_EVIDENCE_LEDGER.json": "5d1ac21a0cf62fe98efe5d4bd5c510094d139e6ae6bd3fc85d10924d67189c89",
  "handoff/m02_completion_28_execution/OWNER_CONSOLIDATED_64_CONDITIONAL_EXECUTION_GRANT_20261127.json": "6a71f52981fc01da42f9c27726547d0d1ddd69851561479a007aeb30ebd95a41",
  "handoff/m02_completion_28_execution/L01a/D079_D080_D081_JOINT_FIT_BINDING_PREPARATION_COMMISSION_20261128.md": "a357343cf523bcb6545033168c333a63cd43eb60e8d0142d25ac93a0ee370e1a"
}
~~~

Independent exact review refs, commits, trees and report SHA256:
~~~json
[
  {
    "commit": "1190b50d43755ffd71629d11ba1846894a113771",
    "tree": "6899f27e39e5c34aa626be0f419da1041edf5926",
    "review_ref": "refs/heads/review/pm-l01a-aligned-history-policy-finite34-r1-20261126",
    "path": "handoff/m02_completion_28_execution/L01a/INDEPENDENT_ALIGNED_HISTORY_JOINT_FIT_POLICY_FINITE34_R1_VERDICT_20261126.md",
    "sha256": "fddeb50391f51afeccb339798c88e8b756768308a6111275d109a1bd2463dc8e"
  },
  {
    "commit": "22a14402bb5df8651e9136b6d00d94f657a07afd",
    "tree": "b32f50aee4e96347d9468749f47a956b60135b0a",
    "review_ref": "refs/heads/review/trial-cac-nvidia-l01a-implementation-20261127",
    "path": "handoff/m02_completion_28_execution/L01a/INDEPENDENT_CAC_TRIAL_ALIGNED_HISTORY_D071_D075_IMPLEMENTATION_VERDICT_20261127.md",
    "sha256": "6c354b51ccd42bf7230a457102f68cbf498f3ded4eae11a90b5765d9567af34b"
  },
  {
    "commit": "5da8986e88d777975edae36fc65eaf8a229e29e4",
    "tree": "059362c14f0d62a99baf07b429e4dbf779e6b3f8",
    "review_ref": "refs/heads/review/trial-cac-nvidia-g01-partition-remap-20261128",
    "path": "handoff/m02_completion_28_execution/L01a/INDEPENDENT_CAC_TRIAL_G01_PROSPECTIVE_PARTITION_REMAP_VERDICT_20261128.md",
    "sha256": "0aab07086e35fe266bcf20f3dfba2934164c39188c641d6dc14318ebc72900e7"
  },
  {
    "commit": "44f538d5b3412d95e8fdad80d17ed74a82aca221",
    "tree": "627c54e5331660881d53692e4e78c8148aeb5c15",
    "review_ref": "refs/heads/review/trial-cac-nvidia-l01a-remapped-installation-20261128",
    "path": "handoff/m02_completion_28_execution/L01a/INDEPENDENT_CAC_TRIAL_ALIGNED_HISTORY_D071_D075_REMAPPED_INSTALLATION_VERDICT_20261128.md",
    "sha256": "4eee01ea905ccbc803c88288f3757c7fd546509f740cddc17fff8e672faa58e5"
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
  }
]
~~~

Direct ordered parents D075/D071/D076/D077; transitive D072/D073/D074. All seven actual parent registrations, including own briefs, bindings, contracts, proof family, claim/pointer/generation, and parent profile:
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
  }
}
~~~

Actual shared source paths and SHA256, unchanged from independently reviewed D077 candidate 253526238d3bfc163e42d0dcbdc79a17c41ff5eb:
~~~json
{
  "src/nvda_desk/market_measurement_truth/api.py": "4fa8240011abb76e7f2349b698639f81f775dd24b8704858a5cf3ea51f2a6f97",
  "src/nvda_desk/market_measurement_truth/_aligned_history_source.py": "f967e122a3ff138401c891987763af37c64b6500ed39672e692b5eb40abbb8cd",
  "src/nvda_desk/market_measurement_truth/_aligned_history_returns.py": "24265ff5b03a35f87aea1b609b578e88d636d786fe25d29c6df69d3dd8a86c46",
  "src/nvda_desk/market_measurement_truth/_aligned_history_codec.py": "c04e6c3e9dd46e2fe0e84f4bdbdb5d300c2cb443534251c179847fef28f7395c",
  "src/nvda_desk/market_measurement_truth/_native_codec.py": "b3d247b4396073d5059e674b9392c03e1b9ce3e418b9a9f1df56417255847759",
  "src/nvda_desk/market_measurement_truth/_record_store.py": "882a61238b74ba5aa2ffacf95d0587633392722d2336a3954681c6ac0a86f0ef",
  "src/nvda_desk/market_measurement_truth/_log_return.py": "3478d5b0e8361f6339c9a0ec5bb70343f2e687338dad0947f7d8a86c0ebf47cf",
  "src/nvda_desk/raw_signal_occurrence_truth/api.py": "cda0dfe957ce6a51a486cbacb78f3f1b50ec9abac4458f8e69b659bf43b0f01d",
  "tools/product_proof_claims.py": "6fde0f0ab02afd0bf7e6b2d8b960f2ca796f10572ba32642a4d46b7ba6d0943b"
}
~~~

## Required common estimator and actual parent seam

Actual parents are the committed public aligned-history producers and ordinary readers, not synthetic D values or an invented adapter. Construct exact sealed raw history sources with each parent's own admission via create_aligned_history_source; create_aligned_history_owner for D071-D075 with empty predecessor tuple, and for D076/D077 with source=None and concrete ordered parent SQLiteReadStorageV1 tuples (D072,D071) and (D073,D074,D072). Materialise via the exact AlignedHistoryRequestV1. Reopen via create_aligned_history_reader and get_derived_occurrence of each exact requested ID; no latest, implicit join, private SQL, injected parent result or mock producer. Current committed AlignedHistoryOccurrenceV1 retains original typed raw records and projections or nested actual typed parent envelopes, with definitions, profile, selection, context, asof, cutoff and first calculated_at. Existing codec.encode includes the first calculated_at in complete canonical bytes even when the identity omits own calculated_at. The current durable reader semantically recomputes each parent and canonical byte equality. Existing RecordState preserves first append and allows ordinary read-only reopen. Getter/list filtering alone does not guarantee first-calculation visibility; the future joint-fit guard must check it explicitly.

Require one common checked four-role row routine and one shared exact joint estimator across all three coefficient producers; no independent univariate fit. Use only ordered D075/NVDA, D071/SPY, D076 relative tech and D077 relative semiconductor history parents. Require exactly six ordered slots S1..S6 for S6 origin or S2..S7 for S7 origin, only exact admitted windows, four distinct IDs per row, 24 distinct IDs across sample. Cross-row duplication must reach semantic refusal after legal request shape. Validate requested IDs, actual typed roles, profile/definition, subject, aligned slot/asof/cutoff/context/parameter/selection, local arithmetic/units and nested parent causality. Require both mandatory shared-parent groups with the SAME full canonical byte comparison predicate: direct D071 versus nested D071 of D076; nested D072 of D076 versus nested D072 of D077. Require actual ID AND exact full stored payload equality including first calculated_at, not only matching IDs, values, hashes or corpus labels. Both groups must execute on live and durable routes. Check all 24 actual parent knowledge cutoffs and first calculated_at <= fit decision cutoff (not later now); respect nested relative producer causal checks. Normal raw cutoff T+1, underlying first T+2, relative first T+3, fit cutoff T+4, calculation T+5, now>=cutoff. Apply exact admitted clock variants only.

Only after both shared comparisons collapse each row to five actual underlying records and ten distinct original facts. Collect all 60 actual selected typed originals with required role/frame keys across six rows; verify each full actual native canonical original and projection using the committed parent law. Invoke the existing Authority.check_corpus intersection over the complete union, not six isolated per-row intersections. Reject missing, duplicate or extra keys or empty common original-content membership, no seal labels or oracle-as-input. Validate before rank/conditioning; reuse common row, visibility, corpus functions for all live and durable coefficients. D078 must be able to reuse these functions in a separately commissioned future stage, not implemented or admitted here.

Derive a using unchanged _log_return._logarithm for positive ln(101/100) canonical 50 significant digit half-even bounded rational log; convert actual Decimal return and relative ExactRatioV1 to exact Fraction, never ambient Decimal/float arithmetic. X=[1,D071/a,D076/a,D077/a], y=D075/a, G=X^T X, h=X^T y. Exactly four columns, six rows; bounded domain and reduced Fraction numerator/denominator bit length <=4096 each step. Exact Fraction Gauss-Jordan, first nonzero pivot at or below current row, swap, normalise and eliminate other rows ascending; solve full rank 4 and inverse, determinant and exact infinity condition of G. Refuse rank deficiency, then condition >50; inclusive 50 required. No tolerance, regularisation, rescale workaround, pseudoinverse or switch estimator. Canonical reduced exact ratios, positive denominator, zero 0/1; actual intercept a times normalised intercept, slopes unchanged. Independent oracles must never be runtime data.

Append only the new typed fit API: AlignedFitRowRequestV1, AlignedFitRequestV1, AlignedFitManifestV1, AlignedCoefficientOccurrenceV1, AlignedCoefficientReadsV1/OwnerV1 and create_aligned_coefficient_owner/reader; exact per-signal own admission and four concrete ordered history read stores. Proposed signatures/fields must be fixed by separate authoring review. One exact shared fit profile t01-l01a-shared-joint-ols/1, policy, model/numeric version, origin/cutoff, six typed ordered actual rows, IDs and recomputed canonical payload hashes, exact determinant/condition, named intercept and named full three slopes. mmtafit1:SHA256 explicit tagged versioned canonical fit envelope excluding fit_id, identical full manifest across all components for same actual sample; no role or component calculation time in shared identity. mmtacoef1:SHA256 typed component envelope excluding own id/calculated_at, binding own request/profile/definition, chosen role, entire fit and result. Preserve actual parent evidence, not hashes alone. Reuse unchanged RecordState and native canonical typed envelopes; exact semantic decode/revalidation and byte re-encode on ordinary read-only reopen, reconstruct shared guard, corpus, estimator, identity and result from retained actual nested facts; no current-store dependency or oracle substitution. Same-owner replay returns original bytes and first timestamp, one durable row; business refusal returns None without append, technical persistence failures propagate. Separate fresh stores per signal/specimen/case. Do not widen existing public/legacy DTOs or registries. Validation order is exactly the adopted joint_fit.validation_order, including both shared-parent comparisons and availability before complete selected original corpus.

The current actual public parent seam satisfies preparation prerequisites documentarily, including full original content and exact first-time payloads. New fit API/implementation/codec remain future obligations, not existing capabilities. No product acceptance inferred. All seven history registrations preserved; actual parent product acceptance and sole Tester remain prerequisites before any child execution.


## Future bounded changed paths (not authorised for modification now)

- src/nvda_desk/market_measurement_truth/api.py (append only)
- src/nvda_desk/market_measurement_truth/_aligned_joint_fit.py (new common fit implementation, exact shared helpers and own component routing)
- tools/product_proof_claims.py (own fixed additive route only, dormant until separately reviewed registration)
- tests/product/m02_completion_28_prospective/d080/test_signal.py
- handoff/m02_completion_28_execution/L01a/ALIGNED_HISTORY_D080_PROOF_CONTRACT.json
- implementation/authority/T01_ALIGNED_HISTORY_D080_AUTHORITY_BINDING.yaml
- config/product_proof/m02_aligned_history_d080/{claim.json,admission.json,generations/0001.json}

Any later shared implementation edit must preserve all previous source, ordinary reader ABI, codec, parent/legacy and G01 semantics; serialise shared changes and independently review the exact delta. No D078, D004/D085 or G01 R2 expansion. No active binding/registration, source/proof modification, collection or execution in this commission.

## Exact finite allocation and reached witness laws

### D080-CONTROLLED-SUCCESS — JOINT_FIT_AND_DURABLE_REOPEN

Original node: `tests/product/m02_completion_28/d080/test_signal.py::test_d080_joint_success`

Remapped node: `tests/product/m02_completion_28_prospective/d080/test_signal.py::test_d080_joint_success`

Exact original case SHA256: 1d0c100fedac2fccd61076cbaef7911113ef4c176fc36c2b96dbf635a0065cb8

Exact positive success and unchanged replay per finite case

Independent oracle (assert only, never input):
~~~json
{
  "fit_manifest_oracle": "oracle_only_not_inputs.fit_oracles.A",
  "actual_component_ratio": [
    3,
    34
  ],
  "actual_intercept_and_vector": [
    [
      24875827132920207120538393860651854221699024850147,
      10625000000000000000000000000000000000000000000000000
    ],
    [
      -11,
      34
    ],
    [
      3,
      34
    ],
    [
      -14,
      17
    ]
  ],
  "condition_ratio": [
    1269,
    34
  ],
  "actual_parent_members": 24,
  "actual_selected_underlying_members": 30,
  "actual_selected_original_facts": 60,
  "excluded_slots": [
    "S0",
    "S7"
  ],
  "actual_component_rows": 1,
  "durability": "Exact actual six-row manifest, full typed role and original evidence, actual common vector/fit ID independently computed; exact component and first timestamp. Later retry after actual S7 available same bytes and only one durable component row; ordinary reader after dropping live histories."
}
~~~
### D080-CONTROLLED-REACHED_REFUSAL — RANK

Original node: `tests/product/m02_completion_28/d080/test_signal.py::test_d080_rank_deficient`

Remapped node: `tests/product/m02_completion_28_prospective/d080/test_signal.py::test_d080_rank_deficient`

Exact original case SHA256: 8c5b75831d2a653f0155e31980a8a74eec963271f8ad3ce4444866357b73dbce

All six complete actual lawful rows, all canonical exact inputs, zero semiconductor column, rank deficient, no missing member or time mismatch.

Independent oracle (assert only, never input):
~~~json
{
  "fit_manifest_oracle": "oracle_only_not_inputs.fit_oracles.RANK",
  "determinant": [
    0,
    1
  ],
  "expected": "None, exact complete actual lawful six-row source roster reached rank; no coefficient row in writer/reopened store. No fallback estimator. Actual parent histories unchanged.",
  "actual_component_rows": 0
}
~~~
### D080-CONDITIONING-REFUSAL — CONDITION

Original node: `tests/product/m02_completion_28/d080/test_signal.py::test_d080_outside_conditioning_domain`

Remapped node: `tests/product/m02_completion_28_prospective/d080/test_signal.py::test_d080_outside_conditioning_domain`

Exact original case SHA256: c05346a2e639b7ca2ac7fc69d63187ad463ea8997186e0620cd8fb8342140c13

Actual complete lawful full-rank cohort, no missing/duplicate/time/source mismatch. Independent exact normalized Gram determinant 9 and condition 208/3 >50; otherwise finite inputs.

Independent oracle (assert only, never input):
~~~json
{
  "actual_component_rows": 0,
  "determinant": [
    9,
    1
  ],
  "condition": [
    208,
    3
  ],
  "expected": "None after full-rank reached condition guard. No ridge, rescaling/tolerance trick or rank misclassification. Empty writer/reopened coefficient store, actual parents preserved."
}
~~~
### D080-CONDITION-INCLUSIVE-BOUNDARY — CONDITION_INCLUSIVE_BOUNDARY_AND_DURABLE_REOPEN

Original node: `tests/product/m02_completion_28/d080/test_signal.py::test_d080_condition_inclusive_boundary`

Remapped node: `tests/product/m02_completion_28_prospective/d080/test_signal.py::test_d080_condition_inclusive_boundary`

Exact original case SHA256: 32c77a4005cc88a2e4e93b21bd083097e60bd3e45bcf470955046dc8a3ab79ee

Actual S6 fit S1..S6 full rank and exact condition equals 50, not merely below. All required actual rows and original membership legal, no use of expected numerical input. Inclusive boundary must emit.

Independent oracle (assert only, never input):
~~~json
{
  "exact_boundary_fit_oracle_only_not_input": {
    "ordered_slots": [
      "S1",
      "S2",
      "S3",
      "S4",
      "S5",
      "S6"
    ],
    "design_normalized": [
      [
        [
          1,
          1
        ],
        [
          -1,
          1
        ],
        [
          0,
          1
        ],
        [
          1,
          2
        ]
      ],
      [
        [
          1,
          1
        ],
        [
          0,
          1
        ],
        [
          1,
          1
        ],
        [
          -1,
          2
        ]
      ],
      [
        [
          1,
          1
        ],
        [
          1,
          1
        ],
        [
          0,
          1
        ],
        [
          -1,
          1
        ]
      ],
      [
        [
          1,
          1
        ],
        [
          1,
          1
        ],
        [
          -1,
          1
        ],
        [
          -1,
          2
        ]
      ],
      [
        [
          1,
          1
        ],
        [
          0,
          1
        ],
        [
          -1,
          1
        ],
        [
          0,
          1
        ]
      ],
      [
        [
          1,
          1
        ],
        [
          -1,
          1
        ],
        [
          1,
          1
        ],
        [
          1,
          1
        ]
      ]
    ],
    "target_normalized": [
      [
        0,
        1
      ],
      [
        1,
        1
      ],
      [
        0,
        1
      ],
      [
        1,
        1
      ],
      [
        -1,
        1
      ],
      [
        0,
        1
      ]
    ],
    "gram_normalized": [
      [
        [
          6,
          1
        ],
        [
          0,
          1
        ],
        [
          0,
          1
        ],
        [
          -1,
          2
        ]
      ],
      [
        [
          0,
          1
        ],
        [
          4,
          1
        ],
        [
          -2,
          1
        ],
        [
          -3,
          1
        ]
      ],
      [
        [
          0,
          1
        ],
        [
          -2,
          1
        ],
        [
          4,
          1
        ],
        [
          1,
          1
        ]
      ],
      [
        [
          -1,
          2
        ],
        [
          -3,
          1
        ],
        [
          1,
          1
        ],
        [
          11,
          4
        ]
      ]
    ],
    "rhs_normalized": [
      [
        1,
        1
      ],
      [
        1,
        1
      ],
      [
        1,
        1
      ],
      [
        -1,
        1
      ]
    ],
    "determinant": [
      27,
      1
    ],
    "condition_ratio": [
      50,
      1
    ],
    "normalized_intercept_and_slopes": [
      [
        5,
        27
      ],
      [
        37,
        54
      ],
      [
        29,
        54
      ],
      [
        2,
        9
      ]
    ],
    "actual_intercept_and_vector": [
      [
        24875827132920207120538393860651854221699024850147,
        13500000000000000000000000000000000000000000000000000
      ],
      [
        37,
        54
      ],
      [
        29,
        54
      ],
      [
        2,
        9
      ]
    ]
  },
  "actual_component_ratio": [
    29,
    54
  ],
  "actual_intercept_and_vector": [
    [
      24875827132920207120538393860651854221699024850147,
      13500000000000000000000000000000000000000000000000000
    ],
    [
      37,
      54
    ],
    [
      29,
      54
    ],
    [
      2,
      9
    ]
  ],
  "condition_ratio": [
    50,
    1
  ],
  "actual_parent_members": 24,
  "actual_selected_underlying_members": 30,
  "actual_selected_original_facts": 60,
  "excluded_slots": [
    "S0",
    "S7"
  ],
  "actual_component_rows": 1,
  "durability": "Actual D080 exact beta 29/54, complete exact fit intercept and vector, actual common identity/manifests and original lineage. Ordinary reopened reader returns first actual bytes; later same-request replay after actual S7 histories normal returns first timestamp and exactly one row. No other coefficient or residual target call."
}
~~~
### D080-FIT-ROW-MISALIGNMENT — PARENT_ROW_ALIGNMENT

Original node: `tests/product/m02_completion_28/d080/test_signal.py::test_d080_fit_row_misalignment`

Remapped node: `tests/product/m02_completion_28_prospective/d080/test_signal.py::test_d080_fit_row_misalignment`

Exact original case SHA256: 9185ff34bb138f2bde3dd66d3eee73b5e7566fa255869e20ccc0a0e272542f3b

Actual all seven prior S0..S6 complete A histories. Original S3 D077 exists. Substitute only actual distinct, present, lawful and fit-cutoff-available D077 S0 in requested S3 row; D077 S0 is otherwise excluded and not duplicated in training. Exact six row slots/four IDs each, 24 distinct IDs, role and profile correct. Wrong frame only, must reach fit alignment before shared-payload/corpus/numeric checks.

Independent oracle (assert only, never input):
~~~json
{
  "actual_component_rows": 0,
  "expected": "None after actual four-role fit row alignment; no duplicate/missing pre-refusal, infer latest, re-fit subset, or source correction.",
  "durability": "Actual all lawful parent stores retained with exact prior payloads; target coefficient returns None, writer and ordinary reopened component history empty; no result or correction/fallback. No additional target calls.",
  "requested_slot": "S3",
  "actual_D077_slot": "S0",
  "actual_unique_member_ids": 24,
  "all_requested_parent_ids_present": true
}
~~~

Exact original complete case objects are pinned by SHA256 of UTF-8 canonical JSON (sorted keys, compact separators, ensure_ascii=False); complete setup/clock/oracle fields in original inventory and reconciled ledger remain mandatory, not replaced by this brief. Only physical path remap is permitted. Do not merge, parameterise away, substitute, add or execute these distinct allocated cases. All 64 holds, 67 historical accepted results, seven history registrations, D145 PAUSED, G01 R2 unadopted and sole Tester retained. Independent exact binding/admission review must precede binding installation or inert proof authoring.
