# Changelog

## v0.2.0 — 2026-11-18

### Added

- A token-free role check in both adapters.
  Before quota or model use, they ask AGY's agent catalog (`/agents`) whether the role is listed.
  The consultation adapter blocks with `agent-not-discovered`.
  The weekly adapter records `agy-agent-missing`, saves progress, and starts no analysis.
  A misplaced or unreadable role file now stops the run with a clear reason instead of failing later.
- Offline tests for the role check and the template layout. The suite now has 33 tests.

### Changed

- The free model guide was rechecked on 2026-11-18.
  Google moved the removal of Claude Opus 4.6, Claude Sonnet 4.6, and GPT-OSS 120B from the free tier to 18 November 2026.
  Gemini 3.8 Flash (Low, Medium, High) is the free choice from then on.
- The agent templates follow the layout of AGY's official custom-agent example, with a `# System Prompt` section after the front matter.
  The heading is optional. Roles installed from v0.1.0 keep working.
- The setup guides now say to install roles as regular files. The consultation adapter already rejects a symlinked role.
- README and project page updated for this release.

### Upgrade from v0.1.0

No change to an installed role is required.
Pull the new scripts. The adapters then confirm on every run that AGY lists your role.
You can check it yourself with `agy agents` in the workspace.

## v0.1.0 — 2026-10-26

First public preview.
