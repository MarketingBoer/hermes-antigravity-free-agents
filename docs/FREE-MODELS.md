# Free AGY models for Hermes

Checked against Google's public pricing and model table on 2026-10-26.

## What is free

Antigravity's Individual plan costs **$0 per month**.
It includes the CLI and a weekly model allowance.
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
| Claude Opus 4.6 Thinking | `claude-opus-4-6-thinking` | Scheduled for removal on **2026-11-02** |
| Claude Sonnet 4.6 Thinking | `claude-sonnet-4-6` | Scheduled for removal on **2026-11-02** |
| GPT-OSS 120B Medium | `gpt-oss-120b-medium` | Scheduled for removal on **2026-11-02** |

The identifiers were observed in one installed AGY 1.4.7 account.
Run `agy models` in your own account before choosing an identifier.
The consultation adapter repeats this check before every analysis.

Google's model table lists Gemini 4 Argon and Claude 5.5 variants under paid plans.
This kit does not label those models free or select them automatically.
The general plans page is less specific about third-party access than the model table.
Use the model table and your current CLI list for model-specific decisions.

## Make the allowance useful

Choose a model for one concrete question:

- Use Flash for a short explanation, a first review, or routine evidence summaries.
- Use an available Opus or Sonnet model for an independent review or a difficult design question.
- Use another available model to compare a specific disputed conclusion.

These are workflow choices, not measured model rankings.
HQ supplies the context and reviews the result.
The adapter returns the selected model, token evidence, and the quota group with its pre-run remaining fraction.
It does not silently replace an unavailable model.

## Stay inside free use

The Individual plan has weekly limits.
Google does not promise a fixed number of prompts for every task.
Longer tasks and more expensive models can consume the allowance faster.
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

- [Pricing: Individual $0/month](https://antigravity.google/pricing)
- [Model availability by plan and announced removals](https://antigravity.google/docs/models)
- [Plans, quota refresh, and credit overages](https://antigravity.google/docs/plans)
- [CLI credit settings](https://antigravity.google/docs/cli/credits/)
- [Settings location and credit use off by default](https://antigravity.google/docs/settings/)
- [Native model quota command](https://antigravity.google/docs/cli/commands/usage/)
- [Headless CLI and streaming results](https://antigravity.google/docs/cli/headless/)

Check these sources again when availability changes.
