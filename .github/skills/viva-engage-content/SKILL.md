---
name: viva-engage-content
description: Create Viva Engage content through the web UI with Playwright - discussions, questions, announcements (a discussion with the megaphone switch), polls, praise, comments, replies, real @mentions, image uploads, and topics, including how to find the new post's permalink and the exact controls, labels and gotchas of each composer. Use when the user wants to post, comment, or decorate conversations in Viva Engage as a specific user.
license: MIT
---

# Viva Engage content

Mechanics for **creating conversation content** in Viva Engage via Playwright. Read `viva-engage-automation` first for sessions, locator strategy, and idempotency; this skill adds the per-content-type details.

No organization-specific content. Examples use placeholders (`<community>`, `Firstname Lastname`).

## When to use this

- Publish a **discussion, question, or announcement** into a community: [references/posts-questions-announcements.md](references/posts-questions-announcements.md).
- Create a **poll** or a **praise** post: [references/polls-and-praise.md](references/polls-and-praise.md).
- Add **comments or answers**, **reply** to a comment, or write a real **@mention**: [references/comments-replies-mentions.md](references/comments-replies-mentions.md).
- Attach an **image**, generate demo images, or add **topics**: [references/images-and-topics.md](references/images-and-topics.md).

## Workflow

1. **Open the community feed** by its stored landing URL (`/main/groups/<id>/all`). Wait until the publisher buttons (Discussion / Question / Praise / Poll) are visible.
2. **Join the community first** if the account is not a member (a *Join* button sits next to the community title). Public communities let non-members see the composer, but join anyway so the member list is right.
3. **Existence check:** search the feed for the title/text and return the existing permalink if found.
4. **Open the composer** for the content type, fill it, wait for the submit button to be enabled, click it.
5. **Find the new card** in the feed, read its thread permalink, store it (`viva-engage-automation` -> idempotency).
6. **Mark the row done** and move on. Verify the first item of each type visually as another user.

## Content types at a glance

| Type | Entry control | Fields | Submit |
|---|---|---|---|
| Discussion | `Discussion` button (or click the publisher text) | one rich-text editor; title = first paragraph | `Post` |
| Question | `Question` button | required one-line title field ("Ask a question (required)") + optional description editor | `Ask` |
| Announcement | open the discussion composer, then the **megaphone** switch (`Announcement`) in the toolbar | like a discussion, no title field | `Post` |
| Poll | `Poll` button | question textbox, `Answer 1..n` inputs (more appear as you fill) | `Ask` |
| Praise | `Praise` button | recipient search + text | `Praise` |
| Comment | click the text "Write a comment" | rich-text editor | `Post` |
| Reply | `Reply - <author>'s comment` button | editor pre-filled with a mention of the parent author | `Post` |

## Core principles

- **Rely on the real controls you can see in the DOM**, not on assumptions from older Yammer/Engage versions. The announcement control, for example, is not a separate post type button in current builds.
- **Roles gate controls.** No megaphone switch = the account is not an admin of that community. Fix the role instead of the locator.
- **Never invent badges or fields.** The praise composer has no badge picker in current builds; do not wait for one.
- **Type, then verify:** the editor closing and the text appearing in the thread is the success signal.
- **Content realism matters more than volume.** Write text a colleague would write, in the audience's language.
