# Free AGY models for Hermes

Checked against Google's public pricing page and model table on 2026-11-18.

## What is free

Antigravity can be used without a subscription plan.
That free plan includes the CLI and a baseline agent quota that refreshes weekly.
You can use that allowance from Hermes through the installed AGY CLI.
You do not need a separate Anthropic, OpenAI, or Gemini API key for this route.
You do not need a paid AGY subscription for the models marked available to Free users below.

This project is MIT-licensed and adds no fee.
Your existing Hermes host and its own primary model remain separate from AGY's free allowance.

## Current free model choices

The official model table lists these models for **Free & Google AI Plus**:

| Model | Observed CLI identifier | Free availability |
| --- | --- | --- |
| Gemini 3.8 Flash Low | `gemini-3.8-flash-low` | Listed for the free tier |
| Gemini 3.8 Flash Medium | `gemini-3.8-flash-medium` | Listed for the free tier |
| Gemini 3.8 Flash High | `gemini-3.8-flash-high` | Listed for the free tier |
| Claude Opus 4.6 Thinking | `claude-opus-4-6-thinking` | Marked for removal on **2026-11-18** |
| Claude Sonnet 4.6 Thinking | `claude-sonnet-4-6` | Marked for removal on **2026-11-18** |
| GPT-OSS 120B Medium | `gpt-oss-120b-medium` | Marked for removal on **2026-11-18** |

Google moved the removal date of the three third-party models from 2026-11-02 to 2026-11-18.
After that date, plan on **Gemini 3.8 Flash** as the free choice.
An account may still list a removed model for a while. Treat the official table as the eligibility source.

The identifiers were observed in one installed AGY 1.5.9 account on 2026-11-18.
Run `agy models` in your own account before choosing an identifier.
The consultation adapter repeats this check before every analysis.

Google's model table lists Gemini 4 and Claude 5.5 models under paid plans.
This kit does not label those models free or select them automatically.

## Make the allowance useful

Choose a Flash level for one concrete question:

- Use **Flash Low** for a short explanation or a routine evidence summary.
- Use **Flash Medium** for a first code review or a regression-test idea.
- Use **Flash High** for an independent design opinion or a difficult debugging question.

These are workflow choices, not measured model rankings.
HQ supplies the context and reviews the result.
The adapter returns the selected model, token evidence, and the quota group with its pre-run remaining fraction.
It does not silently replace an unavailable model.

## Stay inside free use

The free plan has weekly limits.
Google does not promise a fixed number of prompts for every task.
Longer tasks and higher thinking levels can consume the allowance faster.
Models within a quota group share that group's limit.

The consultation adapter reads `/usage` before inference.
It stops when the selected group's remaining fraction is zero or cannot be interpreted.
It makes at most one analysis attempt per invocation.
It does not purchase credits, change accounts, upgrade a subscription, or retry through another provider.

For accounts with paid or promotional credits, inspect **Use G1 Credits / AI Credit Overages** in AGY's settings.
Turn off automatic credit use when you want quota-only execution.
The official CLI documentation identifies the setting as `useG1Credits: false`.
The consultation adapter reads that native setting before each invocation.
It blocks if automatic credit use is enabled, malformed, or unreadable.
An omitted setting uses the documented default: off.
The adapter does not change billing settings or attest your subscription and invoice.
A concurrent settings change after the check is outside this preflight check.
A positive quota snapshot is not a reservation. Other active AGY sessions can consume the same allowance.

## Official sources

- [Pricing: use Antigravity without a subscription plan](https://antigravity.google/pricing)
- [Model availability by plan and announced removals](https://antigravity.google/docs/models)
- [Plans, quota refresh, and credit overages](https://antigravity.google/docs/plans)
- [CLI credit settings](https://antigravity.google/docs/cli/credits/)
- [Settings location and credit use off by default](https://antigravity.google/docs/settings/)
- [Native model quota command](https://antigravity.google/docs/cli/commands/usage/)
- [Headless CLI and streaming results](https://antigravity.google/docs/cli/headless/)

Check these sources again when availability changes.
