# Set up the small workflow

For free on-demand model advice from Hermes, start with [Hermes + AGY](HERMES-AGY.md).
This page configures the optional weekly maintenance and Jules workflows.
Read [free models and quotas](FREE-MODELS.md) before selecting AGY model identifiers.

The offline demo does not need this procedure.
This procedure configures your own installation when you choose to activate it.
The kit does not perform these steps automatically.

## 1. Prepare an explicit local configuration

Open a shell in the source directory.
Copy the example to a local file in the same directory as the example.

```sh
cp config/maintenance-kit.example.json config/maintenance-kit.local.json
```

Edit the copy before a real run.
The `.local.json` suffix excludes it from Git.

| Field | Meaning |
| --- | --- |
| `state_dir` | Private durable state outside the source tree |
| `workspace` | Dedicated AGY working directory with only the supplied role |
| `agy_command` | Argument list for the installed `agy` executable |
| `models.routine` | Exact AGY model name for a routine run |
| `models.changed` | Exact AGY model name for a changed component |
| `components` | One to sixteen public labels mapped to explicit local files |
| `checks` | One to four public labels, argument lists, and timeouts |
| `analysis_timeout_seconds` | Process timeout from 1 to 105 seconds, default 105 |

The example watches this kit's policy and role templates. Replace those paths with the relevant files from your own installation.
Relative file paths resolve from the configuration file's directory.
Path fields expand `~` and environment variables. Model names expand environment variables.
Command arguments do not expand variables or invoke a shell. Use literal absolute paths in production command arguments.
An unset environment variable blocks validation.

Run `agy models` to inspect available names in your own account.
Set both model fields to exact names you can use.
The example accepts `AGY_ROUTINE_MODEL` and `AGY_CHANGE_MODEL` from the environment.
For scheduled runs, literal model strings in the private configuration are simpler.
A shell export does not update an already running gateway's environment.
Do not append an effort flag just because the model name contains an effort tier.
Select a more capable model for changes only when your account supports it.

The example check runs `hermes --version`. A zero exit code proves CLI availability only.
Add your existing read-only assertions when you need meaningful health or policy checks.
For example, use an absolute Python interpreter and your existing learning-check script as separate command arguments.
The kit does not include that installation-specific script or assume a particular memory provider.
If you add a health assertion, make the command return nonzero for an unhealthy response.
The adapter discards command stdout and stderr. It sends only the check label and exit code to AGY.

Review every check command before use.
The operator selects trusted commands that read only the intended data.
The adapter runs those commands with the invoking user's permissions. It does not sandbox them.

Check the configuration without execution or state writes:

```sh
python3 scripts/weekly.py --config config/maintenance-kit.local.json --check-config
```

Validation checks structure and values. It does not test file readability, authentication, or model access.

## 2. Install the AGY role in the dedicated workspace

Create the configured workspace directory.
Create `.agents/agents/maintenance-check/` inside that directory.
Copy `templates/maintenance-check.agent.md` to its `agent.md` file.
Do not copy private instructions, memory, transcripts, or source repositories into the workspace.

Check agent discovery from that workspace with the installed `agy agents` command.
The expected role name is `maintenance-check`.
If discovery differs, stop and consult your installed version's official agent documentation.
Do not substitute a general-purpose agent silently.

The role requests `tools: []` and `commandExecutionPolicy: off`.
These declarations are not proof of complete tool isolation.
AGY can also have user-level configuration and native logs outside this workspace.
Use a suitable account and filesystem boundary for your own risk model.

## 3. Run one manual summary

Check that watched files and existing assertion commands contain the intended scope.
Use public component labels such as `hq-policy` or `memory-health`.
Do not use customer names, account identifiers, or sensitive hostnames as labels.

The following command invokes AGY through your existing login and may consume your account allowance:

```sh
python3 scripts/weekly.py --config config/maintenance-kit.local.json
```

Read the report and inspect the local `state.json`.
An accepted run has `status: "ok"` and a `fingerprints` baseline.
A blocked run has `status: "blocked"` and keeps the previous accepted baseline.
Missing watched files prevent an AGY call. Failed checks prevent baseline acceptance.
Exit code zero means the adapter produced a report, including a blocked report.
Exit code two means configuration or local state failed validation or local I/O failed.
Do not use process exit code zero alone as proof that checks passed.

The adapter saves the previous successful report as context for the next call.
It starts a new AGY conversation. It does not use native conversation resume or migrate memory.
If state is corrupt, preserve the file for local inspection. The adapter does not replace it automatically.

## 4. Use the existing Hermes scheduler

Check that the intended HQ profile and gateway are already configured.
Use that profile's `HERMES_HOME` explicitly when profile selection is ambiguous.
Do not add another scheduler or gateway service.

Copy `scripts/weekly.py` as a regular file to the intended profile's `scripts/maintenance-weekly.py`.
Copy your reviewed local configuration to the same directory as `maintenance-kit.json`.
Convert all component paths to absolute paths before that copy.
Relative paths would otherwise resolve from the new configuration directory.
Use an absolute AGY executable path and absolute assertion executable paths in the copied configuration.
Check the script copy against the reviewed source after each change.
Hermes can reject script symlinks that resolve outside its allowed scripts directory.

Inspect the installed `hermes cron create --help` first.
The example below creates a paused job with local delivery.
Run it only when you intend to add a job to your own installation.

```sh
hermes cron create '15 9 * * 1' --name maintenance-kit-weekly --script maintenance-weekly.py --no-agent --deliver local --paused
```

The path is relative to the selected profile's scripts directory.
`--no-agent` skips an additional Hermes model turn. The Python adapter still invokes AGY once when inputs permit it.
If Hermes' interpreter is older than Python 3.11, use its supported `--interpreter` option with a suitable absolute Python path.
Inspect the stored job before activation.
Check the interpreted timezone and next-run date in your installed Hermes version.
Do not assume that a cron expression alone specifies a timezone.

Use native cron controls to test the paused job if your installed version supports this operation.
Check one delivered report and the local state.
Choose an existing permitted delivery route if local delivery is insufficient.
Keep real chat identifiers in your private job configuration.
Resume the reviewed job through native cron controls when ready.
Record its identifier and first actual scheduled execution outside Git.
An outbound `hermes send` notification is not evidence that HQ began a task.

## 5. Configure Jules with its native Scheduled Tasks

Use the official [Scheduled Tasks guide](https://jules.google/docs/scheduled-tasks/).
Select the intended repository and base branch in the official Jules interface.
Read `templates/jules-daily.md` before replacing its fields.
Set the code and test paths that the task may change.
List known overlapping work, or write `none` after you check it.
The operator must authorize this exact scope before the automatic task is activated.

Create one daily schedule with the completed task text.
Check for an existing equivalent schedule before submitting it.
Check the displayed time, timezone, and active state after saving.
Use Jules' native notification option if available.
Do not add a separate notification service for this kit.

Automatic Scheduled Tasks can execute without the interactive plan-approval step.
Keep the existing approval rules for other Jules tasks.
The included template grants no automatic merge, deployment, or direct push to the base branch.

Inspect the first real scheduled execution, activities, test result, and any diff or PR.
Do not infer a working schedule from its saved form alone.
Do not infer completed code from a session status alone.
Check notification delivery separately.
If a submit result is uncertain, inspect the current schedule and sessions before retrying.

## Stop or update

Pause the native Hermes job or Jules schedule using the same official interface that owns it.
The kit installs no additional process to stop.
For adapter changes, rerun the offline suite and replace only the reviewed script copy.
Keep local progress and private configuration outside the public repository.
