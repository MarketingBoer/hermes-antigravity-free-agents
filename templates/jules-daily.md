# Daily maintenance task template

Replace every {{FIELD}} before use.
Do not treat this template as operator authorization.
Use automatic Scheduled Tasks only after the operator authorizes this exact scope.

---

Daily mocked regression maintenance for {{REPOSITORY}}, starting from {{BASE_BRANCH}}.

The operator authorized automatic execution of this specific daily task on {{AUTHORIZATION_DATE}}.
Do not request plan approval or routine input for work within this scope.
This authorization does not apply to other tasks or repositories.

Select at most one missing regression test or one small, reproducible defect.
Keep work within {{CODE_AND_TEST_PATHS}}.
Read the current source and existing tests before you select work.
Check accessible open pull requests and remote branches for overlapping work.
Do not claim access to unavailable Jules sessions.
Do not duplicate existing work.
If overlap is uncertain, report the limitation without making the selected change.
Exclude the known work listed here: {{KNOWN_WORK_OR_NONE}}.

Do not change architecture, dependencies, credentials, permissions, or deployment files.
Use mocks for authentication, network requests, and all external services.
Do not use real customer data or credentials.
Do not access unrelated services or repositories.

For a defect, demonstrate a failing mocked regression test before the correction where feasible.
Make the smallest correction that passes the relevant tests.
For a missing test, explain the behavior that the test protects.
Run the relevant tests.
If no useful change meets this scope, report that result.
Do not invent work.
If blocked, report the blocker without routine questions.

Provide a reviewable diff.
Use the native pull request export when changes are ready.
Do not merge, enable automatic merge, deploy, or push directly to {{BASE_BRANCH}}.

Write a concise English report for every run.
State the outcome: changed, no useful change, skipped duplicate, or blocked.
Include the reason and changed files.
Include actual test commands and results.
State limitations and any pull request URL.
Do not claim that changes reached the base branch or production.
