# Viva Engage Skill Repo

This repo contains skills compatible with both **Claude Code** and **GitHub Copilot**.
Skills live in `.github/skills/<skill-name>/SKILL.md`.

## When adding or modifying skills

Every `SKILL.md` must use **only the frontmatter fields that both Claude Code and GitHub Copilot document**:

```yaml
---
name: viva-engage-<skill-name>
description: <one or two sentences - what it covers and when to invoke it>
license: MIT
---
```

- `name` (must equal the folder name; lowercase letters, digits, hyphens; max 64) and `description` (10-1024 characters, plain single-line text without `: ` or ` #`) are required.
- `license` is optional but harmless.
- **Do not add other fields.** `argument-hint`, `user-invocable`, `disable-model-invocation`, and `allowed-tools` are not understood by every harness; GitHub Copilot reports them as unsupported properties. `allowed-tools` also pre-approves shell access, which these documentation-only skills do not need.

Run `python tools/check_skills.py` before every commit - it enforces this.

## Structure

Each skill lives in its own subdirectory with a `SKILL.md` entry point and a `references/` folder of focused markdown files. The `SKILL.md` links to the reference files - load only the one relevant to the current task, not all of them upfront.

## Content policy (hard rules)

This repository is public. It must never contain:

- user names, e-mail addresses, passwords, tokens, session files, or any credential value
- environment, organization, customer, community, or project names or identifiers (IDs, GUIDs, domains)
- hyperlinks or URLs of any kind (write install commands as `owner/repo`, refer to products by name)
- screenshots or exports of a real environment

Examples use placeholders (`<community>`, `Firstname Lastname`, `<permalink>`). Path *patterns* such as `/main/threads/<id>` are fine; real IDs are not. Use neutral wording ("environment", "organization") and never name a real one.

Run the checks before every commit:

```
python tools/check_clean.py
python tools/check_skills.py
```

It fails on URLs, e-mail addresses, domain names, GUIDs, long opaque identifiers, credential assignments, and one environment-specific word. Keep any private deny-list of real names *outside* this repository.

## Plugin marketplace - checklist when adding a new skill

`.claude-plugin/marketplace.json` is the only thing that makes a skill folder discoverable through `/plugin install`. Whenever a skill is added or meaningfully changed:

1. Add the skill's folder path to the `skills` array of the `viva-engage` plugin entry (one plugin bundles every skill in this repo).
2. Bump **both** `version` fields (`metadata.version` and the plugin's `version`) so an existing install's `/plugin update` notices the change.
3. Add a line to `CHANGELOG.md`.
4. Update the skill table in `README.md`.

The file-based install paths (Claude Code `.claude/settings.json`, Copilot auto-discovery of `.github/skills/`) do not read `marketplace.json`.
