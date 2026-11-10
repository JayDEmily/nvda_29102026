# Disposable ChatGPT-to-GitHub handover probe — 10 November 2026

## Scope and authority
This is a user-authorised, isolated **automation transport test**, not NVIDIA product work, a review or a programme acceptance. Do not alter NVIDIA implementation, governance, test evidence, main, accepted branches or other files. Do not merge this branch.

Repository: `JayDEmily/nvda_29102026`
Input branch: `experiment/chatgpt-handoff-arithmetic-20261110-01`
This instruction file: `handoff/automation_probes/ARITHMETIC_TEST_20261110.md`
Required output file: `handoff/automation_probes/ARITHMETIC_TEST_20261110_RESULT.md`
Output branch: **the same** `experiment/chatgpt-handoff-arithmetic-20261110-01`.

## Task for the newly launched independent ChatGPT thread
1. Locate this branch and read this instruction in GitHub; read repository-level governing instructions in their applicable scope.
2. Answer the following question: **What is 10 plus 10?** Give the numerical result and a one-sentence calculation.
3. Create the required output file on the specified output branch, recording: the question, result, calculation, input instruction location, input commit SHA, output branch, and a statement that no NVIDIA code or accepted branches were changed.
4. Commit the new output file to that branch. Report the new commit SHA and GitHub file link to the conversation.
5. Do not modify any other file, open a pull request, merge, or attempt real NVIDIA testing.

The purpose is to prove a new chat can independently discover a GitHub instruction and write the answer to GitHub, without inheriting the coder chat context. If any tool/permission step fails, report the precise point of failure rather than claiming success.
