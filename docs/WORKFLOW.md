# Roles, evidence, and follow-up

## The smallest useful split

HQ retains the existing Hermes team assignment tools.
Jules handles a narrow repository maintenance scope through its native functions.
AGY summarizes a fixed evidence bundle during the weekly check.
Neither Jules nor AGY becomes a new supervisor.

The operator can add `templates/hq-policy.md` to existing HQ instructions after review.
The kit does not overwrite a profile, permissions, memory, or existing policy.

## Three AGY situations

| Situation | Trigger | Work |
| --- | --- | --- |
| Routine | No selected fingerprint changed | Short status from fixed checks |
| Change | A selected file changed, appeared in the selection, or left the selection | Summarize only the affected component labels |
| Concrete problem | HQ issues a separate bounded brief | Investigate one question with explicit access and a stop condition |

The first accepted run creates a baseline. It does not claim there were no prior changes.
A missing selected file blocks acceptance and preserves the previous baseline.
File hashes detect bytes changing. They do not identify the meaning of a change.
The weekly adapter sends no file contents, diffs, filenames, or hashes to AGY.
Its change review therefore summarizes check outcomes and labels. It cannot review a code diff.
For a content review, HQ must explicitly supply a permitted, sanitized diff in a separate investigation.

Routine and change models come from local configuration.
Choose them from the account's working catalog, not from this project's examples.
For a difficult problem, HQ can choose a more capable available model in the separate brief.
Use a second review only when the question justifies it.
The weekly run uses one main agent and requests no helpers.
A separate investigation can allow at most two native helpers for independent questions.
The kit does not test helper model inheritance or separate helper effort.

## Progress that remains useful

The adapter retains one previous successful report, local fingerprints, check exit codes, and one open problem label.
It stores the running state before model execution.
It uses a filesystem lock to prevent overlapping runs that use the same state directory.
It accepts no more than five bullet lines and 150 words.
It saves only bounded report text and selected metadata, not raw CLI events or command output.

The adapter clears its open problem when the selected checks and files no longer report it.
This field tracks a current observation, not an incident backlog.
HQ can use the synthetic `examples/handover.json` format for a separate operational handover.
Keep actual handovers outside Git.

The handover should answer four questions:

1. What was last verified?
2. What remains open?
3. Where is the task or session evidence?
4. What is HQ's next action?

## Jules evidence

A useful result includes the exact test command, actual result, changed files, limitation, and any PR reference.
Use accessible branches and PRs to check overlap before selecting a change.
If overlap cannot be established, report that limitation and skip the selected change.
Native task scheduling does not prove notification delivery or code correctness.
HQ or the operator reviews the diff and test evidence before applying code.
The public kit does not include the original installation's private Jules MCP adapter or approval ledger.

## Bounds and errors

Each weekly adapter run starts at most one AGY analysis call.
It starts at most two `/usage` queries with a 25-second process timeout each.
Each selected check has a timeout of at most 30 seconds, with at most four checks.
The analysis process has a timeout of at most 105 seconds and a native wait of at most 90 seconds.
These defaults allow at most 275 seconds of sequential subprocess waits, plus local I/O and process overhead.
They are not a hard wall-clock deadline, provider token budget, or request-count guarantee.

A process timeout kills the local process group. It does not prove cancellation of a provider-side request.
The adapter starts no immediate retry or error-triggered model switch.
It rejects results that report tool use. That rejection cannot undo a tool action.
The observed event format is not proof of complete runtime tool isolation.
If an account, permission, quota, or CLI failure occurs, HQ investigates it through the normal route.
