# ChatGPT → GitHub → independent ChatGPT: Windows UI Automation handover

**Operational protocol and failure report — 10 November 2026 (Melbourne).**

**Evidence status:** One fully verified disposable end-to-end round trip. This is **not** proof of unattended, repeated-run reliability; it grants no NVIDIA product-test, merge, gate or acceptance authority.

## 1. Architecture and result

A worker writes a self-contained, commit-pinned handover into the relevant GitHub repository. A new ChatGPT conversation (preferably within the `NVDA_6.1` ChatGPT project) receives one short message:

> Check the latest NVIDIA GitHub handover and carry out the authorised next task.

The new thread uses personal context/project instructions to help **discover** the correct work, but must verify the repository, current governing instructions, exact branch, instruction commit, authorised scope and output branch **from GitHub**. After execution, the original worker or commissioning thread independently fetches the result and validates the Git diff. Conversation history is not the durable handover. A result marked PASS is still subject to the governing independent acceptance mechanism.

**Verified control path:**

ChatGPT Remote Desktop Commander connector → Remote MCP → local Desktop Commander Windows agent → Windows PowerShell → `UIAutomationClient` / Win32 foreground focus → logged-in Chrome → ChatGPT accessibility controls.

The native Windows UI route did not need DOM injection, changes to Chrome CSP, extension debugging, remote Chrome DevTools Protocol or stored login credentials.

**Observed exact test:**

| Checkpoint | Evidence |
| --- | --- |
| General Chrome chat | Located enabled `Ask ChatGPT` editor, typed/read back `hello`, confirmed enabled `Send`, pressed Enter once, observed `You said: hello` then `Hello. What can I help you with?` |
| NVDA project chat | Opened the project URL, found enabled `New chat in NVDA_6.1` editor, typed/read back the short handover instruction, confirmed `Send`, pressed Enter **once**, saw the posted message and subsequent assistant response |
| GitHub discovery | The new thread found `experiment/chatgpt-handoff-arithmetic-20261110-01` and instruction SHA `5dd6ecc6...` although the short prompt contained neither identifier |
| New thread's work | Read `What is 10 plus 10?`, answered `20`, created and committed exactly one new result file |
| Independent readback | Fetch of result content, output commit, GitHub comparison, and Windows `git ls-remote --heads` all confirmed the output |

**Immutable input instruction:** [`ARITHMETIC_TEST_20261110.md` at `5dd6ecc6f8ad56d030a24eba8caaf48b7a7fecb4`](https://github.com/JayDEmily/nvda_29102026/blob/5dd6ecc6f8ad56d030a24eba8caaf48b7a7fecb4/handoff/automation_probes/ARITHMETIC_TEST_20261110.md).

**Immutable output:** [`ARITHMETIC_TEST_20261110_RESULT.md` at `18090360b24fca36721cfa939d88a7cdc799b73f`](https://github.com/JayDEmily/nvda_29102026/blob/18090360b24fca36721cfa939d88a7cdc799b73f/handoff/automation_probes/ARITHMETIC_TEST_20261110_RESULT.md).

**Output commit:** [`18090360b24fca36721cfa939d88a7cdc799b73f`](https://github.com/JayDEmily/nvda_29102026/commit/18090360b24fca36721cfa939d88a7cdc799b73f).

GitHub compare `5dd6ecc6...18090360` showed `ahead_by=1`, `behind_by=0`, `total_commits=1` and **one added result file** (16 lines added, zero deleted). Remote `git ls-remote` confirmed the experiment branch's resulting SHA exactly. This was a **transport demonstration**, not a NVIDIA programme test.

## 2. Mandatory preparation: GitHub first

1. Identify the correct GitHub repository and current accepted source branch. Read `GUARDRAILS.md`, all applicable `AGENTS.md` / overrides, the active `EXEC_PLAN.md` and task-specific authorities **in full**. Do not equate newest branch with accepted authority.
2. Finish only the authorised worker work. Commit/push and independently verify its exact source commit, files and status in GitHub.
3. Commit a **separate self-contained handover** identifying: repository, instruction ref/path/SHA, target source SHA, precise tester role, allowed operations, exclusions, acceptance checks, named output path/branch, receipt and unresolved issues. A worker cannot award itself acceptance or grant authority the programme has not given.
4. Fetch/read the new handover file and its GitHub commit *before* launching the tester. For the 10 November probe, the worker created the isolated `experiment/chatgpt-handoff-arithmetic-20261110-01` branch from `main` and staged only `handoff/automation_probes/ARITHMETIC_TEST_20261110.md` at `5dd6ecc6...`.
5. Do not re-use the toy arithmetic task as real NVIDIA work. It is retained solely as a proven cross-thread transport witness.

## 3. Exact Windows UI interaction protocol

**Prerequisites:** Remote Desktop Commander online on `DESKTOP-I188O30` (or current authorised Windows machine); existing authenticated Chrome profile; correct ChatGPT account/project; PowerShell supporting `UIAutomationClient` and `System.Windows.Forms`. Use Remote Desktop Commander's `start_process` to run PowerShell on **Windows**, not a WSL Chromium/DOM automation script.

**Stage A — launch an NVDA project window.** Successful command:

~~~powershell
Start-Process -FilePath 'C:\Program Files\Google\Chrome\Application\chrome.exe' -ArgumentList @('--new-window','https://chatgpt.com/g/g-p-6ad546f307e88191b64b94d0851da624-nvda-6-1/project')
~~~

**Stage B — discover the live target.** The successful project window was titled `ChatGPT - NVDA_6.1 - Google Chrome`. Its accessible editor was `New chat in NVDA_6.1`, in contrast to the ordinary fresh chat editor `Ask ChatGPT`. Do not hardcode the Windows HWND, virtual desktop coordinates, UI index, project tab or accessible name without a fresh check.

Successful inspection used these native primitives (execute and examine output before any typing):

~~~powershell
Add-Type -AssemblyName UIAutomationClient
$root = [System.Windows.Automation.AutomationElement]::RootElement
$windows = $root.FindAll([System.Windows.Automation.TreeScope]::Children,[System.Windows.Automation.Condition]::TrueCondition)
foreach ($w in $windows) {
  if ($w.Current.Name -like '*NVDA_6.1*Google Chrome*') {
    Write-Output ('WINDOW='+$w.Current.Name+' HWND='+$w.Current.NativeWindowHandle)
    $elements = $w.FindAll([System.Windows.Automation.TreeScope]::Descendants,[System.Windows.Automation.Condition]::TrueCondition)
    foreach ($e in $elements) {
      if ($e.Current.ControlType -eq [System.Windows.Automation.ControlType]::Edit) {
        Write-Output ('EDIT='+$e.Current.Name+' ENABLED='+$e.Current.IsEnabled+' OFF='+$e.Current.IsOffscreen)
      }
    }
  }
}
~~~

**Stage C — focus, type and read back.** Require **one uniquely identified**, enabled, non-offscreen project editor, with value empty except for its placeholder. Bring that window to the foreground with a Windows `user32.dll` `SetForegroundWindow(IntPtr)` P/Invoke, call `editor.SetFocus()`, and confirm `GetForegroundWindow()` returns that window's **current** handle. Only then:

~~~powershell
Add-Type -AssemblyName System.Windows.Forms
$prompt = 'Check the latest NVIDIA GitHub handover and carry out the authorised next task.'
[System.Windows.Forms.SendKeys]::SendWait($prompt)
$actual = $editor.GetCurrentPattern([System.Windows.Automation.ValuePattern]::Pattern).Current.Value.Trim()
if ($actual -cne $prompt) { throw 'Readback mismatch: do not submit.' }
~~~

The Windows `$editor` variable above is the **live element found in Stage B**; the actual test executed stages as separate, inspectable PowerShell calls, re-enumerating the editor rather than assuming variables persist between Remote Desktop calls. **This snippet is explanatory, not a separately executed one-shot script.** In the proven call, the readback equalled the exact short prompt.

Before submission, re-enumerate descendants and require exactly **one** enabled, visible `ControlType.Button` named `Send`. Confirm the intended Chrome HWND remains foreground. Submit **one** Enter:

~~~powershell
[System.Windows.Forms.SendKeys]::SendWait('{ENTER}')
~~~

**Stage D — verify delivery.** Re-read the live accessibility tree. The project test displayed a conversation item with the exact submitted prompt. The independent thread then showed a response, discovered the correct GitHub branch/commit and eventually produced its completed reply. **Do not resubmit** if the action's outcome is uncertain: inspect the open chat first.

`SendKeys` has special encoding for characters including `+`, `^`, `%` and braces. The proven short prompt contained none. Arbitrary multiline text requires independent escaping/readback validation. Multiple external monitors produced unusual/off-screen window rectangles during earlier inspection; targeting accessible elements and live HWND avoided coordinate assumptions.

## 4. Fresh thread reads, works and commits

The new independent thread should:

1. Use any relevant personal/project context only to **locate** the work; inspect current GitHub governing files and target refs itself.
2. Identify the specific pending instruction file and pinned source commit, not merely “most recent commit”.
3. Check whether the requested result already exists; do not silently write a duplicate.
4. Perform the **exact authorised task**. For the arithmetic probe: `10 + 10 = 20` with one sentence of calculation.
5. Create the specified output file on the specified branch, recording input location/SHA, answer, scope and result; commit it; report output commit and link. Do not merge, promote, rewrite history, alter product code or claim programme acceptance.
6. Report `BLOCKED` with precise missing evidence, tool permission or unmet authority when the task cannot legitimately continue.

The commissioning thread then **independently** fetches the new GitHub file and commit, compares input→output commit, confirms allowed paths only, and checks remote branch SHA. The successful Windows verification command was:

~~~powershell
git ls-remote --heads https://github.com/JayDEmily/nvda_29102026.git refs/heads/experiment/chatgpt-handoff-arithmetic-20261110-01
~~~

Result: `18090360b24fca36721cfa939d88a7cdc799b73f`. Conversation “PASS”, product-test “PASS”, independent review and **programme acceptance** are distinct propositions.

## 5. Earlier failed/incomplete approaches: evidence versus hypotheses

| Observation | Verified | Not established |
| --- | --- | --- |
| Browser connector | A prior Browser-host route rejected `chatgpt.com`, and the accessible Browser connector offered tab-reading actions rather than native desktop input. | Not a system-wide Chrome/Windows automation ban. |
| WSL launcher | `/home/jds/nvda_open_chat.sh` opened the NVDA project via Windows `chrome.exe --new-window` and explicitly said: “It does not automate ChatGPT input or Send.” Execution printed “Opening in existing browser session.” | Opening a window did **not** prove a message was sent. |
| Earlier UI Automation probe | Around 19:15 Melbourne time an initial inspection found 66 elements, largely Chrome controls, without identifying the ChatGPT composer; a completed submission was not observed. | Why the editor was missing was **not** established; later project UI inspection found a valid editor. |
| Chrome CSP DevTools error | An inline script at `runner.html:366` was blocked with a CSP SHA-256 hash. | Ownership and causal connection to chat failure **unknown**; SHA-256 was a script hash, not a chat-prompt rejection; do not disable CSP on this evidence. |
| ChatGPT extension error | Chrome extension version `1.26.1102.11740` contained `js-kernel-offscreen.html`; screenshot reported a Statsig networking/Response-construction error. | No verified causal connection with Remote Desktop Commander's separate MCP/Windows control route. |
| Desktop Commander local log | `C:\Users\james\.desktop-commander-device\remote-tue.log` included some `CHANNEL_ERROR` transport warnings and later connected/ready state and successful tool calls. | Not evidence that ChatGPT rejected a prompt. The agent log is not a full browser network trace. |
| Chrome focus/window changes | Numerous authenticated Chrome windows were present. A window's title/content could change; some windows had very unusual multi-monitor coordinates. | An old window handle or fixed mouse coordinate is not a safe send target. |
| Successful Windows UIA method | Actual editor → focus → type → readback → Send enabled → one Enter → posted message → assistant reply → GitHub commit → GitHub readback. | One bounded PASS does not certify repeated unattended operation. |

**Supported diagnosis:** Earlier work launched Chrome but did not demonstrate a complete user-input/send/readback chain. The successful method explicitly used native Windows accessibility controls for those missing steps. Claims that CSP, Statsig, host restriction, or Chrome itself **caused** the earlier missing submission are not supported by the inspected evidence.

## 6. Limits and future reuse

- This is an **operational transport procedure**, not a new ExecPlan or a change to accepted tests, governance or NVIDIA source authority.
- Preserve authenticated browser session; do not extract/copy tokens, cookies or passwords into GitHub, logs or macros.
- Use **one** exact prompt, **one** deliberate submit, and readback. On uncertainty or failure stop dependent automation and diagnose rather than retrying blindly.
- If the browser UI changes, inspect the current accessibility tree afresh; do not assume selectors and window titles remain stable.
- A **packaged persistent one-click macro**, automatic retries, unattended multiple-run reliability, extension-independent behaviour in all environments and independent acceptance of future real NVIDIA work remain **untested** by this probe.
- This runbook is committed to the **default main branch**. Existing work and historical branches have their own root `AGENTS.md` and do not acquire new lines automatically. Future workers must inspect the applicable branch authority and may explicitly read this main-branch operating procedure where relevant.

**Completion boundary:** one independently pinned GitHub input, one new NVDA_6.1 project chat and short prompt, one new task/result commit and independently verified return.