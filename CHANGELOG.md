# Changelog

## Unreleased

- Examples: `examples/vscode/` with a custom agent (fixed tool set, may call a subagent), a read-only verifier subagent, and a `/build-demo` prompt file - the supported way to combine the skills with tools and subagents in VS Code.
- Docs: added a "What is this for?" section at the top of the README (purpose, audience, what you get, what it is not, why the skills declare no tools or subagents).

## 0.1.1

- Fix: user feedback reported that the skills did not work in GitHub Copilot, whose harness does not understand some of the frontmatter properties (its documentation lists only `name`, `description`, `license`, and `allowed-tools` as text). Removed `allowed-tools`, `argument-hint`, and `user-invocable` from all four `SKILL.md` files; frontmatter is now only `name`, `description`, `license` (the portable set documented for Copilot and Claude Code).
- Added `tools/check_skills.py`, which fails on non-portable frontmatter fields, name/folder mismatches, over-long descriptions, and unsafe YAML in descriptions.
- Docs: corrected the README and CLAUDE.md statement that Copilot ignores the extra fields.

## 0.1.0

- Initial release with four skills:
  - `viva-engage-automation` - approach, recorded sessions and automatic sign-in, forced multi-factor registration, locator and reliability rules, idempotency and state, seeding playbook, troubleshooting.
  - `viva-engage-content` - discussions, questions, announcements (megaphone switch), polls, praise, comments, replies, @mentions, image upload, topics.
  - `viva-engage-engagement` - reactions, poll votes, best/verified answers, stand-in user planning.
  - `viva-engage-community-admin` - members and roles, pinning, links, community info, favorites, events.
- Added `.claude-plugin/marketplace.json` for installation via `/plugin marketplace add`.
- Added `tools/check_clean.py`, a guard against URLs, e-mail addresses, domains, identifiers, credentials, and environment-specific wording.
