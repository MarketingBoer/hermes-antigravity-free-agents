# Verification record

Package review date: 2026-10-26.
This record describes observed results and remaining limits.
It is not a product certification or a claim about other accounts.

## Portable package

The offline checks run on Linux with the installed Python 3.12 interpreter.
The adapter requires Python 3.11+ because it uses `hashlib.file_digest`.
Local release preparation did not execute Python 3.11.
The hosted test matrix covers Python 3.11 and 3.12. Inspect its Actions result separately.
No package installation is required. Only the Python standard library is imported.

The test suite runs local child processes with a fake AGY command and synthetic data.
Result: 30 tests passed on local Python 3.12.
The two-round demo and the selected-file privacy check also passed.
The consultation tests exercise the real wrapper with a synthetic native CLI process.
They cover live model-list selection, separate quota groups, credit-setting checks, and blocked results without retries.
An independent local review found two execution-bound defects during packaging.
Both fixes passed focused regressions and a second review.
It checks these behaviors:

- An accepted first report creates a baseline with a private state file.
- The prompt excludes watched file paths, contents, and fingerprints.
- Changed files select the configured change model.
- The next run receives the previous successful report.
- Empty, malformed, oversized, verbose, or wrong-type answers keep the prior baseline.
- Reported tool use blocks acceptance.
- A failed usage query starts no analysis.
- A failed usage query clears previous per-run analysis metadata.
- Excessive model output terminates the local process group during reading.
- A selected FIFO blocks acceptance without waiting for a writer.
- An analysis timeout blocks acceptance without a retry.
- Corrupt local state is preserved.
- An existing process lock prevents another run.
- A failed assertion keeps the baseline and records one open problem label.
- A missing selected file prevents a model call.
- Invalid configuration causes no command execution.
- A missing AGY executable gives a short blocked report.
- Package selection rejects missing files, unknown files, symlinks, and parent-path entries.
- Synthetic privacy leaks trigger the checker without echoing their contents.

## On-demand consultation: real AGY smoke test

Release preparation ran one synthetic code-review question through `scripts/consult.py` and the native AGY 1.4.7 CLI.
The explicit model was `claude-opus-4-6-thinking`.
The adapter returned `status: "ok"` with 3,597 total tokens.
The stream confirmed the requested model and reported no tool or helper actions.
The local credit-use setting was omitted, which uses the documented default: off.
The native third-party quota group showed a positive remaining fraction before execution.
No separate provider API key or subscription change was used for this invocation.

The task contained only the public synthetic example, not private source or account data.
The response identified empty input as a concrete failure in that example and suggested an explicit return policy.
HQ must still evaluate the proposed policy and regression case.
This run proves one native adapter invocation, not model correctness or invoice accounting.
The optional Hermes skill was reviewed through a separate instruction-following scenario.
It was not installed into a live Hermes profile or exercised by a real HQ turn.

The [free model guide](FREE-MODELS.md) records the official pricing and availability sources checked on 2026-10-26.
Current third-party models have an announced removal date of 2026-11-02.
This package makes no continuing availability promise for them.

## Public offline CI

The GitHub workflow runs only synthetic tests, the demo, and the package checker on Python 3.11 and 3.12.
It uses read-only repository permissions and no account secrets.
The declared matrix is not itself evidence that a run passed. Inspect the repository's Actions results.

The workflow pins these official actions, checked through GitHub's tag API on 2026-10-26:

- [actions/checkout](https://github.com/actions/checkout), [v6.0.2](https://github.com/actions/checkout/releases/tag/v6.0.2), commit `de0fac2e4500dabe0009e67214ff5f5447ce83dd`.
- [actions/setup-python](https://github.com/actions/setup-python), [v6](https://github.com/actions/setup-python/tree/v6), commit `ece7cb06caefa5fff74198d8649806c4678c61a1`.

The offline demo runs two successful synthetic rounds with temporary state.
The package checker checks all allowlisted UTF-8 files and flags unexpected non-cache files.
The release review also uses a private denylist outside this directory.
These checks are heuristic. Manual review of selected content is still necessary.

## Original installation: documented prior evidence

The original working pattern used Hermes v0.22.0 and AGY 1.4.7 on Linux.
This was one installation with local Hermes patches and account-specific access.
Those runtime patches are not part of this kit.
The packaging session rechecked the installed Hermes version and relevant CLI help.
It did not start a real model run, modify a schedule, or test another account.

Available prior evidence records a real AGY Low summary and Medium summaries through a manually triggered native Hermes cron job.
It records saved progress reaching a later round and no tool calls in those summaries.
A separate synthetic native conversation-resume and helper probe also succeeded in that installation.
The portable adapter does not implement native conversation resume or helpers.
Exact helper model inheritance and separate helper effort remain unproven.

The original Jules daily schedule was saved and active in the inspected interface.
The first actual scheduled run and notification delivery were not yet observed in the available evidence.
The original AGY future weekly schedule was also not yet observed firing at its planned date.
Manual cron execution is evidence of manual execution, not of a future scheduled run.

## Not tested or promised

- A fresh full-service installation of this portable package, including its optional Hermes skill.
- A full Jules-to-HQ-to-AGY autonomous loop or automatic HQ polling.
- A real Jules patch produced by the new public task template.
- Future scheduled execution or message delivery.
- Complete AGY tool isolation or automatic rollback of tool actions.
- Recall quality, backup restoration, or complete permissions against a policy.
- Universal model availability, subscriptions, quotas, or provider costs.
- macOS, Windows, or different CLI versions.

The owner approved MIT publication before this release preparation.
