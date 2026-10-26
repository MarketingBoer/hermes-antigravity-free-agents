# Give Hermes access to free AGY model advice

The operator installs AGY and signs in through its official flow.
The operator uses the free Individual plan for free-tier execution.
Read [free models and quota](FREE-MODELS.md) before selecting a model.

This connection uses Hermes' existing terminal tool to call the native AGY CLI.
It does not register AGY as an OpenAI-compatible provider.
It does not replace Hermes' primary model or copy AGY credentials into Hermes.

## 1. Prepare the dedicated AGY workspace

Choose an absolute workspace path outside private source and memory directories.
Create `.agents/agents/hermes-consultant/` inside that workspace.
Copy `templates/hermes-consultant.agent.md` to its `agent.md` file.
Run `agy agents` from the workspace.
Check that `hermes-consultant` appears.

The role requests no tools and no helpers.
The adapter rejects observed actions after execution.
These checks do not create a security sandbox or undo an action.
Keep private material out of the workspace and prompt.

## 2. Test one consultation

Open a shell in the kit directory.
Inspect your current model list:

```sh
agy models
```

Choose an identifier from that result.
The following command uses the Flash Low identifier observed during release preparation.
Replace the workspace argument with your chosen absolute path.

```sh
python3 scripts/consult.py --model gemini-3.8-flash-low --workspace /absolute/path/to/agy-workspace < examples/consultation.json
```

The input is one UTF-8 JSON object with `question` and optional `context` strings.
The example is synthetic.
Unlike the weekly summary, a consultation sends the supplied context text to AGY.
Review and minimize that context before execution.

The adapter checks that native credit overages are off.
It checks the current model list and the selected quota group.
It starts one analysis only when both checks pass.
It uses the explicit model and the `hermes-consultant` role.
It never switches models after a failure.

An accepted response has `status: "ok"`, a model identifier, a positive token count, and a response.
The receipt also records the selected quota group and its pre-run remaining fraction.
Exit code zero means the response passed these structural checks.
It does not prove the advice is correct or that your subscription is free.
The `credit_overages` field records the local setting check before execution.

A blocked response has `status: "blocked"` and a short reason.
Exit code two means no acceptable response was returned.
An analysis failure can consume quota even when the adapter rejects the result.
The adapter discards native stderr instead of publishing diagnostics.
Inspect native private logs locally when you need detailed troubleshooting.

## 3. Install the optional Hermes skill

Select the intended Hermes profile.
Use that profile's existing skill directory.
Create a new `agy-consult` directory there.
Copy `templates/agy-consult/SKILL.md` into that directory.
Do not overwrite an existing skill with the same name.

Edit the copied skill's two configuration placeholders:

- `KIT_DIRECTORY`: the absolute path to this reviewed kit.
- `AGY_WORKSPACE`: the absolute path to the dedicated workspace.

Use the installed Hermes version's native skill discovery to check that `agy-consult` is available.
This public package does not install or change a live Hermes profile automatically.

## 4. Ask HQ for a concrete result

Example requests after installation:

> Ask free AGY Flash to review this function. Give me the first reproducible bug and one regression case.

> Ask the currently available free Opus model for a second opinion on this architecture. Use only the selected design excerpt.

> Ask AGY to explain this sanitized failure trace. Mark assumptions and propose one next check.

HQ uses its existing tools to select the permitted context.
HQ sends a JSON task to `scripts/consult.py` through stdin.
HQ records the returned model and result.
HQ evaluates the recommendation before any code change.

The skill does not create a separate automatic dispatcher or background service.
It does not grant AGY the Hermes team's tools, memory, or repository permissions.
The weekly adapter and optional Jules schedule remain separate workflows.
