---
name: viva-engage-automation
description: Foundation for automating Viva Engage through its web UI with Playwright - why UI automation, per-user browser sessions and automatic sign-in, robust locators for a UI that uses fake placeholders and portals, idempotent Excel-driven runners with a state file, retry rules, troubleshooting, and a phase order for seeding a demo environment. Use when the user wants to script, seed, or test Viva Engage (formerly Yammer) content as different users, or when a Viva Engage automation misbehaves.
allowed-tools: [shell]
argument-hint: "what should be created or changed in Viva Engage, and as which users (real sessions, or demo accounts)?"
user-invocable: true
---

# Viva Engage automation (foundation)

This skill packages field-tested patterns for driving **Viva Engage** (the successor of Yammer) through its web UI with **Playwright for Python**, so that content can be created *in the name of many different users*.

It contains no organization- or person-specific content - only the mechanics of the platform, distilled from a real end-to-end seeding project (posts, questions, announcements, polls, praise, comments, replies, reactions, votes, best answers, topics, pins, events, member roles).

This is the **entry skill**. The other skills in this collection build on it:

| Skill | Use it for |
|---|---|
| `viva-engage-content` | Creating posts, questions, announcements, polls, praise, comments, replies, mentions, images, topics |
| `viva-engage-engagement` | Reactions, poll votes, best/verified answers, one-action-per-user constraints, stand-in users |
| `viva-engage-community-admin` | Members and roles, experts, pinning, links, events, community info, favorites |

## When to use this

- You need to **fill a Viva Engage environment with realistic content** (demo, training, test, screenshots) and every item must come from the right person. See [references/approach-and-architecture.md](references/approach-and-architecture.md).
- You need **per-user sign-in without clicking through MFA every time**, or the environment forces a "keep your account secure" registration screen. See [references/sessions-and-login.md](references/sessions-and-login.md).
- A **locator does not find a control that is clearly visible** (comment box, composer, menu item), a click is intercepted, or the page sometimes shows "This page isn't loading right now". See [references/locators-and-reliability.md](references/locators-and-reliability.md).
- You want a runner that can be **stopped and restarted without duplicating posts**. See [references/idempotency-and-state.md](references/idempotency-and-state.md).
- You are planning a **complete seeding run** and need the right order of phases, test-data design, and honest limits (no backdating, no Copilot features). See [references/demo-seeding-playbook.md](references/demo-seeding-playbook.md).
- Something errors and you want the cause fast: [references/troubleshooting.md](references/troubleshooting.md).

## Prerequisites

- Python 3.10+ with `playwright`, `openpyxl`, `PyYAML`, `python-dotenv`; run `playwright install chromium` once.
- Demo or test accounts you are allowed to sign in as. Never use this against real users' accounts.
- For environments with enforced multi-factor authentication: either pre-recorded browser sessions per user, or an environment configuration that does not force registration for the demo accounts (see the sessions reference).

## Workflow

1. **Decide the approach.** The official APIs (the legacy REST API, now reached through Entra-registered apps, and the newer Microsoft Graph Viva Engage APIs) cover a growing but incomplete set of content types, their coverage and permissions keep changing, and acting as many different users needs delegated consent per user. Check the current coverage first; if you need every content type (polls, praise, announcements, best answers, topics, pinning, events) as many users with nothing but a sign-in, UI automation is the pragmatic route. See [references/approach-and-architecture.md](references/approach-and-architecture.md).
2. **Get a session per user** (`storage_state` JSON) - recorded once, refreshed automatically. See [references/sessions-and-login.md](references/sessions-and-login.md).
3. **Resolve targets by permalink, not by scrolling.** Every post has a stable thread permalink (`/main/threads/<id>`); capture it once and reuse it. See [references/idempotency-and-state.md](references/idempotency-and-state.md).
4. **Use role- and text-based locators and tag containers with a small DOM script** instead of fragile CSS classes. See [references/locators-and-reliability.md](references/locators-and-reliability.md).
5. **Run in phases, group work by user, save status after every item.** See [references/demo-seeding-playbook.md](references/demo-seeding-playbook.md).
6. **Verify with a screenshot as a different user** than the one who created the content - the log line "posted" only proves the click happened.

## Core principles

- **UI automation acts as the user.** Content appears under that user's name, with that user's permissions. A control that is missing (for example the announcement switch) usually means a missing role, not a broken locator.
- **Never put passwords, tokens, environment names, or user lists into code or into a repository.** Read a shared demo password from an ignored `.env` file, keep recorded sessions in an ignored folder, and keep the user/content data in spreadsheets that stay local.
- **Idempotent by construction.** A status column per row plus a state file with permalinks means a crashed run can simply be started again.
- **"Terminal write":** an action is not done until the state-changing click ran *and* the result is visible (editor closed, text present, badge shown). Describing what should happen is not the same as making it happen.
- **One process at a time per state file and per spreadsheet.** Two runners that load, modify, and save the same file silently overwrite each other's results.
- **Viva Engage cannot backdate content.** Everything appears as "just now"; plan demos accordingly.
