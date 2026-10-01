---
name: viva-engage-engagement
description: Drive Viva Engage interactions through the web UI with Playwright - reactions on posts and comments (hover picker and name mapping), poll votes, marking best or verified answers, the one-action-per-user rule, and how to plan stand-in users when some accounts cannot sign in. Use when the user wants to make a Viva Engage community look used (likes, votes, best answers) or hits toggling and duplicate-action problems.
license: MIT
---

# Viva Engage engagement

Mechanics for **interactions on existing content**: reactions, poll votes, best/verified answers - and the planning logic that keeps them correct when several roles are played by fewer real sessions.

Read `viva-engage-automation` first (sessions, locators, idempotency). No organization-specific content.

## When to use this

- Add **reactions** to posts and comments, or map spreadsheet reaction names to the reactions the UI offers: [references/reactions-and-votes.md](references/reactions-and-votes.md).
- Cast **poll votes**: same reference.
- Mark **best answers** or **verified answers**, understand who sees the control: [references/best-and-verified-answers.md](references/best-and-verified-answers.md).
- Some accounts cannot sign in (forced MFA registration) and their activity must be played by others without creating **duplicates, self-comments, or toggled-off reactions**: [references/stand-in-users.md](references/stand-in-users.md).

## Workflow

1. **Check that the target exists** (permalink in the state file; comment recorded as posted). Leave the row pending otherwise.
2. **Plan the acting user per row before opening a browser.** Enforce: one reaction and one vote per user per target, never the author of the target for self-directed actions, and a deterministic assignment that is stored so later runs agree.
3. **Group by acting user**, open each thread by permalink, perform the action, record the user in the `done` map.
4. **Verify** with a screenshot as another user: reaction summary ("A and N others"), poll bars with counts, a *Best answer* badge on the question and in the community's *Top questions* list.

## Core principles

- **Reactions toggle.** Clicking the same reaction again removes it; a different reaction replaces it. Plan uniqueness up front instead of detecting it in the UI.
- **Only some roles can mark answers.** Admins, community experts, and the person who asked can; plain members cannot. Use an admin session for it.
- **Map names, do not guess.** The UI offers a fixed set of reactions (Like, Love, Laugh, Celebrate, Thank, Sad). A spreadsheet word that is not in the set (for example "Insightful") needs an explicit mapping.
- **Skipped is a valid outcome.** If a poll with 13 planned votes only has 8 distinct accounts available, 5 rows become `Skipped` with a reason; do not force duplicates.
