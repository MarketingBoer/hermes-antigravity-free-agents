# Privacy and provenance

## Explicit selection

This directory is a new standalone package.
It contains selected generic behavior, rewritten instructions, configurable examples, and synthetic fixtures.
It contains no copied repository history or upstream runtime.
The release allowlist is `PUBLIC_FILES.txt`.
The local package checker scans that allowlist and flags unexpected non-cache files.

| Selected source concept | Public form |
| --- | --- |
| HQ keeps team assignment | An optional policy fragment |
| Daily mocked Jules maintenance | An editable task template |
| Bounded weekly AGY check | A configurable Python adapter |
| Native AGY role declaration | A generic English role |
| Saved progress and evidence limits | Local state behavior and synthetic examples |
| Original regression cases | New portable subprocess tests |
| Free native model advice for HQ | An on-demand adapter and optional Hermes skill |

Private management files, runtime patches, learning material, account configuration, connectors, memory banks, credentials, logs, reports, and recovery archives are excluded.
The public adapter does not call or import the private management repository.
The private adapter source was not submitted for an external review during this packaging task.

## Data sent for a consultation

The on-demand adapter sends the question and context supplied through stdin to the selected AGY model.
It sends the consultation instructions and role declaration as well.
It does not automatically collect repository files or Hermes memory.
The operator or HQ must review and minimize the supplied context.
Unlike the weekly summary, a consultation can include source excerpts or sanitized failure details.
An input-size limit is not a privacy filter.

The adapter reads AGY's native local credit setting without modifying it.
It blocks when automatic credit use is enabled or the setting cannot be interpreted.
The native CLI still uses its existing account authentication and global configuration.
The adapter returns the model, response, token count, pre-run quota fraction, and credit-setting check in stdout.
It does not create a separate durable consultation log.
HQ can keep the selected result through its existing private workflow.
Native AGY logs can still exist outside this kit.

## Data sent for a weekly summary

The adapter supplies public component labels, selected check exit codes, a baseline indicator, and explicit evidence limits.
It also supplies the previous successful short report and one open problem label.
The selected model and agent name enter the native CLI command.
Private file paths, file hashes, file contents, and raw assertion output do not enter the prompt.
Use non-sensitive labels and keep prior reports free of sensitive information.

AGY itself can read user configuration, use existing authentication, and create native logs outside this kit.
The adapter's prompt rules do not isolate the underlying CLI from your account or filesystem.
Model output can be incorrect. The checker does not guarantee that future model-generated text is free of sensitive content.

## Local storage

`state.json` contains fingerprints, check codes, the latest report, the previous successful report, and execution metadata.
The adapter creates a new state directory with mode 0700 and new state files with mode 0600.
Existing directory permissions remain the operator's responsibility.
The package scanner does not inspect your private runtime state.
Keep the state directory and configuration outside public releases.
Do not add credentials to the configuration or command arguments.

The checker looks for common key formats, private key blocks, account identifiers, private network addresses, personal home paths, and operational IDs.
It is a heuristic, not a complete secret detector.
Review selected files manually before each release.
An ignore rule alone does not make a file safe to publish.

## License

MIT permits reuse and modification with a short attribution requirement.
It suits a small kit of templates and Python glue that others may adapt to their own repositories.
The included license covers only material the project contributors have the right to license.
The release uses the included MIT license and contributor attribution.
Hermes, Jules, and Antigravity remain subject to their own licenses and service terms.
This independent project claims no official affiliation.
