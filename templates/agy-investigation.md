# Focused investigation template

HQ must replace every {{FIELD}} before a separate investigation.
This template does not extend the weekly adapter's permissions.

Investigate one problem: {{QUESTION}}.
Use only this evidence and these permitted paths: {{EVIDENCE_AND_PATHS}}.
Use these permitted tools: {{TOOLS}}.
Do not change files or services unless the task explicitly authorizes that action.
Stop after {{TIME_LIMIT}} or when {{STOP_CONDITION}} occurs.
Do not retry a permission, account, or quota failure.
Do not change models to bypass a failure.

Use one main agent.
Use at most two native helpers only if independent research is useful and permitted.
Each helper must not create more helpers.
Keep these unresolved limits explicit: {{KNOWN_LIMITS}}.

Return at most five English bullets.
Separate observed facts from hypotheses.
State the affected component, evidence, uncertainty, and one next action for HQ.
Do not claim that health proves recall or that backup presence proves recovery.
HQ retains task assignment and the existing approval rules.
