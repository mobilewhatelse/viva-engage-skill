# Viva Engage Skills - Claude Code + GitHub Copilot

A skill collection compatible with both **Claude Code** and **GitHub Copilot**, packaging field-tested, copy-pasteable patterns for automating **Viva Engage** (the successor of Yammer) through its web UI with Playwright - so that realistic content can be created, decorated, and administered in the name of many different users.

No project-specific, person-specific, or organization-specific content - just the mechanics of the platform, distilled from a real end-to-end seeding project: posts, questions, announcements, polls, praise, comments, replies, mentions, images, topics, reactions, votes, best answers, member roles, pinning, events, community info, and favorites.

## Relationship to existing resources

As of this writing (October 2026) there is **no officially maintained Viva Engage skill collection** from Microsoft for Claude Code or GitHub Copilot. Related things that do exist, none of which cover this ground:

- Microsoft's general agent-skill collections (Azure SDKs, Microsoft 365 agent development, Copilot Studio) - they do not contain Viva Engage content.
- Administration scripts for Viva Engage communities and users (PowerShell) - good for environment-wide administration, not for creating conversation content as a user.
- A Microsoft 365 command-line interface skill - covers command-line administration, not UI-level content creation.
- Community MCP servers that let a chat assistant browse, search, and reply - typically one identity, read/reply only.

This collection is therefore a **complement**: it fills the gap of *UI-level content creation and community administration as many different users*, which is what demos, training environments, screenshots, and UI tests need. If you only need to read or export data, or act as one service identity, prefer an API-based approach.

## Using these skills

### Claude Code CLI / GitHub Copilot CLI (plugin marketplace)
```
/plugin marketplace add mobilewhatelse/viva-engage-skill
/plugin install viva-engage@viva-engage-skill
```
Gives you `/plugin update` and version tracking - see [CHANGELOG.md](CHANGELOG.md).

### Claude Code (file-based, no plugin install)
Add this repo as a skills source in your project's `.claude/settings.json`, or reference individual skill files directly in chat. Skills are in `.github/skills/<skill-name>/SKILL.md`.

### GitHub Copilot (VS Code)
Clone or add this repo. Copilot auto-discovers skills from `.github/skills/` and exposes them as slash commands (for example `/viva-engage-content`). Requires VS Code with the GitHub Copilot extension in agent mode.

### Both
Skills use the shared `SKILL.md` format with only the portable frontmatter fields `name`, `description`, and `license`, so the files load unchanged in both tools. Harness-specific fields are deliberately left out (GitHub Copilot reports unknown properties as unsupported); `tools/check_skills.py` enforces this.

## Skills in this repo

Four skills that build on each other. Start with `viva-engage-automation`; the other three reference it.

### `viva-engage-automation` - foundation

Why and how to drive Viva Engage through its web UI: architecture of an Excel-driven, phase-based runner; one recorded browser session per user plus automatic sign-in; what to do when accounts are forced into multi-factor registration; locator strategy for a UI with fake placeholders, portals and generated class names; idempotency with a status column, a state file and thread permalinks; a phase order for seeding a complete demo environment; troubleshooting.

Entry point: [`.github/skills/viva-engage-automation/SKILL.md`](.github/skills/viva-engage-automation/SKILL.md)

| Reference | Content |
|---|---|
| [`approach-and-architecture.md`](.github/skills/viva-engage-automation/references/approach-and-architecture.md) | UI automation versus APIs, runner layout, grouping by user, dry runs, what never to commit |
| [`sessions-and-login.md`](.github/skills/viva-engage-automation/references/sessions-and-login.md) | Recorded sessions, automatic sign-in selectors, why `is_visible(timeout=...)` does not wait, the forced multi-factor registration screen and the administrative levers that can cause it, headed versus headless, locale |
| [`locators-and-reliability.md`](.github/skills/viva-engage-automation/references/locators-and-reliability.md) | The comment box that is not a placeholder, role-based names, tagging containers with a DOM script, feed cards, sidebar look-alikes, intercepted clicks, waits, typing, transient "page isn't loading" errors, pacing, environment gotchas |
| [`idempotency-and-state.md`](.github/skills/viva-engage-automation/references/idempotency-and-state.md) | Three layers of duplicate protection, capturing permalinks, displayed versus typed titles, shared workbook objects, single-writer rule, crash recovery |
| [`demo-seeding-playbook.md`](.github/skills/viva-engage-automation/references/demo-seeding-playbook.md) | Data model, phase order and why, verifying like a user, making the community look used, hard limits |
| [`troubleshooting.md`](.github/skills/viva-engage-automation/references/troubleshooting.md) | Symptom -> cause -> fix table |

### `viva-engage-content` - posts, questions, announcements, polls, praise, comments, replies, mentions, images, topics

Exact controls, labels and gotchas of each composer: a discussion, a question with its own required title field and "Ask" button, an announcement as a discussion with the megaphone switch (admin only, no title field), polls with dynamically appearing answer inputs, praise with recipient search and no badge picker, comments that need the real editor and the Post button (Enter does not submit), one-level replies with a pre-filled mention, real @mentions via the people picker, image upload through the file chooser, generating demo images from HTML, and adding or creating topics.

Entry point: [`.github/skills/viva-engage-content/SKILL.md`](.github/skills/viva-engage-content/SKILL.md)

| Reference | Content |
|---|---|
| [`posts-questions-announcements.md`](.github/skills/viva-engage-content/references/posts-questions-announcements.md) | Landing page, narrow Join matching, discussion, question, announcement, finding the new card and its permalink, duplicate protection |
| [`polls-and-praise.md`](.github/skills/viva-engage-content/references/polls-and-praise.md) | Poll composer and voting basics, praise composer, recipients without sessions, no badge picker |
| [`comments-replies-mentions.md`](.github/skills/viva-engage-content/references/comments-replies-mentions.md) | Comment/answer flow, replies, mention typing helper, verification |
| [`images-and-topics.md`](.github/skills/viva-engage-content/references/images-and-topics.md) | File chooser upload, HTML-rendered demo images, SVG gotcha, the topic dialog in full detail |

### `viva-engage-engagement` - reactions, votes, best/verified answers, stand-in users

Reaction picker and name mapping (Like, Love, Laugh, Celebrate, Thank, Sad), toggling behaviour, poll voting with exact option text, who can mark best or verified answers and how the menu is built, and a planning algorithm that keeps interactions correct when fewer accounts can sign in than the plan has personas: no self-directed actions, one action per user per target, deterministic and persisted assignments, skipping instead of duplicating.

Entry point: [`.github/skills/viva-engage-engagement/SKILL.md`](.github/skills/viva-engage-engagement/SKILL.md)

| Reference | Content |
|---|---|
| [`reactions-and-votes.md`](.github/skills/viva-engage-engagement/references/reactions-and-votes.md) | Hover picker, reaction mapping, poll vote flow, realistic distributions |
| [`best-and-verified-answers.md`](.github/skills/viva-engage-engagement/references/best-and-verified-answers.md) | Who can mark, the "Mark as" menu, what to verify, planning |
| [`stand-in-users.md`](.github/skills/viva-engage-engagement/references/stand-in-users.md) | Rules, algorithm sketch, variants per content type, what not to do |

### `viva-engage-community-admin` - members, roles, pins, info, events, favorites

Adding members and setting Admin / Community expert roles (including the entry point that changes its label and why the role must be read from the role button only), pinning conversations (feed menu only) and links, the community info editor with its second Save button, favorites and the look-alike buttons in the navigation, and the event form with read-only date and time pickers.

Entry point: [`.github/skills/viva-engage-community-admin/SKILL.md`](.github/skills/viva-engage-community-admin/SKILL.md)

| Reference | Content |
|---|---|
| [`members-and-roles.md`](.github/skills/viva-engage-community-admin/references/members-and-roles.md) | Entry points, invite flow, role menu, pitfalls, verification |
| [`pins-info-favorites.md`](.github/skills/viva-engage-community-admin/references/pins-info-favorites.md) | Pin conversation, pin link, info text, favorite star selection by position |
| [`events.md`](.github/skills/viva-engage-community-admin/references/events.md) | Form layout, input order, calendar and time pickers, success detection |

## Core principles

- Drive the UI the way a user does, with **role- and text-based locators**; tag containers with a small DOM script instead of relying on generated class names.
- **Idempotent by construction:** a status column, a state file with permalinks, and an existence check in the UI before creating anything.
- **Terminal write:** an action is not done until the state-changing click ran *and* the result is visible - the log line "posted" proves nothing.
- **Missing controls usually mean missing roles**, not broken locators.
- **Plan uniqueness before opening a browser** (one reaction/vote per user per target), and prefer `Skipped` over duplicates.
- **No secrets in code or repositories:** passwords in an ignored `.env`, recorded sessions in an ignored folder, personas and content in local spreadsheets.
- **Honest limits:** no backdating, no automatic Copilot summaries, no community creation, UI changes over time - re-probe the DOM when a locator fails.

## Content policy

This repository intentionally contains no user names, e-mail addresses, passwords, tokens, environment or organization names, identifiers, or links. Examples use placeholders. See [CLAUDE.md](CLAUDE.md) and the check script in `tools/`.

## License

MIT - see [LICENSE](LICENSE).
