# ⚡ Hermes × AGY — Zero-Cost Antigravity Agents in Your Hermes Workflow

## Give Hermes free AI backup.

**Put Antigravity's free model allowance to work inside your Hermes workflow.**
Ask HQ for a code review, a debugging hypothesis, or a second opinion.
AGY runs the selected model through your existing sign-in.
HQ gets the answer back and keeps control of the work.

**No separate model API key. No paid AGY subscription required for the free tier. No fee from this kit.**

> Ask free Opus to challenge this design.
>
> Have Flash find the first bug in this function.
>
> Give me a second opinion before I change this code.

These are example requests after you install the optional Hermes skill.
The kit connects Hermes to the official AGY CLI. It does not replace Hermes' own primary model.

### Free models, checked 26 October 2026

| Available in the free tier | Use it for |
| --- | --- |
| **Gemini 3.8 Flash**, Low / Medium / High | Focused questions, first reviews, and routine summaries |
| **Claude Opus 4.6 Thinking** | An independent architecture or debugging opinion |
| **Claude Sonnet 4.6 Thinking** | A focused code review or test proposal |
| **GPT-OSS 120B** | Another model's view on a concrete question |

**The Opus 4.6, Sonnet 4.6, and GPT-OSS entries are scheduled for removal on 2 November 2026.**
Google's [current model table](https://antigravity.google/docs/models) lists that date.
The adapter checks your live model list before every consultation.
Use the models your free account actually offers today.
The suggested uses above are workflow choices, not benchmark results.

Google lists the Individual plan at **[$0/month](https://antigravity.google/pricing)** with a weekly allowance.
Read [what is free, current models, and quota rules](docs/FREE-MODELS.md).
Free access has usage limits. Paid credit overages are optional and must stay off for quota-only use.

## From one Hermes request to a model answer

```text
You: Ask AGY to review this function.
                |
           Hermes HQ
       one selected task
                |
         consult.py
     live models + quota check
                |
       official AGY CLI
       your existing login
                |
   selected available free model
                |
   answer + model + token evidence
                |
        HQ reviews the result
```

The on-demand adapter sends one question and the context you explicitly supply.
It returns a JSON receipt with the model, response, token count, and pre-run quota fraction.
It stops if credit overages are enabled, the model disappears, or quota is empty or unknown.
It makes one analysis attempt. It does not buy credits or switch providers after failure.

## Try the kit offline

Use Linux and Python 3.11 or newer.
No account, credentials, dependency installation, or live agent is needed for these checks.

```sh
python3 scripts/demo.py
python3 -m unittest discover -s tests -v
python3 scripts/check_package.py
```

The demo shows two synthetic maintenance rounds.
The tests also exercise the on-demand path through a fake local AGY process.
They cover model availability, separate quota groups, rejected actions, and one-call failure behavior.
These offline checks do not consume a service allowance.

## Connect Hermes to AGY

Follow the [Hermes + AGY guide](docs/HERMES-AGY.md).
It sets up a dedicated consultant role and an optional `agy-consult` Hermes skill.
You keep your existing Hermes profile, terminal tool, and AGY login.

The manual adapter accepts JSON through stdin:

```sh
python3 scripts/consult.py --model gemini-3.8-flash-low --workspace /absolute/path/to/agy-workspace < examples/consultation.json
```

Prepare the workspace first. Choose a model from your current `agy models` list.
The example task is synthetic.
A real consultation sends the supplied context to the selected service.

## Put it to work

| What you want | What the kit gives you |
| --- | --- |
| A second opinion before a risky change | One focused AGY consultation, with the selected model recorded |
| A bug hypothesis from a small excerpt | An explicit question and context, with no repository import |
| A regression-test idea | A reviewable recommendation that HQ can check |
| A short weekly evidence report | The resumable weekly adapter and existing Hermes scheduler |
| Optional daily code maintenance | A bounded Jules task template using its native scheduler |

HQ owns coordination and follow-up.
AGY advises on the selected task.
Jules is optional for the separate maintenance workflow.
You do not need Jules to use free AGY advice from Hermes.

## What is included

- [Native Hermes skill template](templates/agy-consult/SKILL.md) for on-demand AGY advice.
- [Consultation adapter](scripts/consult.py) with live model and quota checks.
- [AGY consultant role](templates/hermes-consultant.agent.md) and [synthetic task](examples/consultation.json).
- [Free model guide](docs/FREE-MODELS.md), with dated official sources.
- [Weekly adapter](scripts/weekly.py) with saved progress and overlap protection.
- [Maintenance setup](docs/SETUP.md), [HQ policy](templates/hq-policy.md), and [optional Jules template](templates/jules-daily.md).
- Offline subprocess tests, a demo, and an explicit public-file privacy checker.

Only the Python standard library is needed.
There is no new scheduler, supervisor, model proxy, or credential store.

## Proof and boundaries

The [verification record](docs/VERIFICATION.md) separates offline tests, prior installation evidence, and live checks.
The [privacy guide](docs/PRIVACY.md) explains exactly which consultation data leaves your machine.

The consultation role requests no tools. The adapter rejects observed tools or helpers after execution.
That does not create a security sandbox or undo an action.
Use a clean workspace and selected sanitized context.
A model answer and a successful response status do not prove that a fix works.
HQ still checks evidence before changes, merge, or deployment.

The Individual tier provides free AGY usage within its allowance.
The adapter checks the native credit setting. It does not attest your subscription or reserve quota.
Your existing Hermes hosting and primary model remain separate.
Availability and weekly limits can change.
The kit uses supported native interfaces and does not bypass limits or subscription rules.

## Official projects

- [Hermes Agent](https://github.com/NousResearch/hermes-agent) and [documentation](https://hermes-agent.nousresearch.com/docs/)
- [Antigravity pricing](https://antigravity.google/pricing), [model table](https://antigravity.google/docs/models), and [headless CLI](https://antigravity.google/docs/cli/headless/)
- [Optional Jules Scheduled Tasks](https://jules.google/docs/scheduled-tasks/)

Independent community kit. No official affiliation is claimed.

## License

[MIT](LICENSE). Upstream tools retain their own licenses and service terms.
