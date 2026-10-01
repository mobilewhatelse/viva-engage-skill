# Approach and architecture

## Why drive the web UI?

| Option | Strengths | Limits for "fill an environment as many users" |
|---|---|---|
| Legacy REST API (reached via Entra-registered apps) | Stable for reading and basic posting | Platform is being retired for new scenarios; one delegated token per acting user; no guaranteed coverage of newer content types |
| Microsoft Graph Viva Engage APIs | Modern, supported direction | Coverage is still growing; each acting user needs consent; admin-only features (roles, pinning, events) may be missing - verify the current docs before relying on it |
| Admin scripts (PowerShell / CLI) | Good for community and membership administration | Not for conversation content as a user |
| Community MCP servers | Convenient for reading, searching, replying from a chat | Typically read/reply only, one identity |
| **Playwright against the web UI** | Every content type, every role, no app registration, no admin consent | Depends on UI structure; needs sign-in per user; slower |

UI automation is the right tool when the goal is *realistic content from many identities* (demo, training, screenshots, UI tests). Prefer an API when you only need to read, export, or post as a single service identity.

## Architecture that worked

```
run.py                    CLI: --phase N, --only-key, --limit, --dry-run, --headed, --retry-errors, --skip-no-session
config.yaml               UI labels (EN/DE), timeouts, community landing URLs, reaction name map
substitutes.yaml          optional: stand-in users per role (see viva-engage-engagement)
src/session.py            one browser context per user, automatic sign-in when the saved session is invalid
src/engage.py             navigation, join, thread lookup, text typing with mentions, image upload
src/handlers/*.py         one module per content family (posts, comments, polls/praise, threads, admin)
src/excel_store.py        thin wrapper over openpyxl: eligible rows, set_result, shared workbook per file
state.json                permalinks and "done" markers (never committed)
.auth/                    recorded sessions (never committed)
.env                      shared demo password (never committed)
errors/                   screenshot per failed item (never committed)
```

### The runner loop

1. Read the sheet; keep rows with `Active = Yes` and `Status = Pending` (plus `Error` with `--retry-errors`).
2. Decide the acting user per row (the row's user, or a stand-in).
3. **Group rows by acting user** - one browser context per user instead of one per row. Keep `Sequence` order inside a user.
4. For each row: run the handler, write `Status` (`Posted` / `Done` / `Error` + message) and save the workbook after every item.
5. On an exception: screenshot to `errors/<key>.png`, status `Error`, continue with the next row.

A single browser (`chromium.launch`) with one `new_context(storage_state=...)` per user is much faster than launching a browser per user.

### Dry run first

`--dry-run` should print *who would do what* (including stand-in assignments) without opening a browser. Always run it before a bulk run.

## Phases

Content depends on earlier content (a comment needs a post, a reply needs a comment, a best answer needs an answer). The order that worked is in [demo-seeding-playbook.md](demo-seeding-playbook.md).

## What to keep out of the repository

Recorded sessions, `.env`, the state file, spreadsheets with real names/addresses, screenshots of the environment, and run logs. Put them in `.gitignore` from the first commit.
