---
name: viva-engage-community-admin
description: Administer a Viva Engage community through the web UI with Playwright - add members and set the Admin and Community expert roles, pin conversations and links, set the community info text, create events (date picker and time list), and mark communities as favorites, including the entry-point label changes and the traps around each control. Use when the user wants to set up or dress a Viva Engage community as an admin, or when an admin control cannot be found.
license: MIT
---

# Viva Engage community administration

Mechanics for the **admin side** of a community. Read `viva-engage-automation` first. No organization-specific content.

## When to use this

- Add **members** in bulk and set **Admin** / **Community expert** roles: [references/members-and-roles.md](references/members-and-roles.md).
- **Pin** conversations and links, set the **Info** text, mark **favorites**: [references/pins-info-favorites.md](references/pins-info-favorites.md).
- Create **events** (date and time pickers are not typeable): [references/events.md](references/events.md).

## Workflow

1. Sign in as an **admin of that community** (the right-hand column shows an *Admin actions* section only for admins). A control that is missing means the role is missing.
2. Navigate by the community's stored landing URL and **wait for the right-hand column to finish loading** - some sections (stars, summary, events) render a few seconds after the feed.
3. Make each admin action **idempotent**: read the current state first (member already listed, role already present, topic/link/pin already there) and only then change it.
4. Save status per row; verify visually on the community page.

## Admin controls at a glance

| Goal | Where | Notes |
|---|---|---|
| Add member / set roles | Right column *People* -> **Assign experts** (or **Add user** once experts exist) -> Members tab | Search by name, click the plus at the end of the suggestion row; role is a dropdown in the member row |
| Pin a conversation | Post menu in the **feed** (not on the thread page) -> *Pin conversation* | Shows a *Pinned conversation/announcement* header |
| Pin a link | Right column *Pinned links and files* -> **Pin link** | Dialog: Address + Title + OK |
| Community info | Right column *Info* -> **Add community info** / **Edit** | Settings page with a rich-text *Community information* editor and its **own Save** button |
| Event | Right column *Admin actions* -> **Create event** | Full page form, not a dialog |
| Favorite | Heart icon in the community header | Left-navigation items have look-alike star buttons |

## Core principles

- **Roles gate everything.** Verify roles in the member list when a control is absent.
- **Entry points change their label** depending on state (*Assign experts* -> *Add user*). Match both.
- **Read the role from the role button, not from the whole row.** Names and job titles contain words like "Admin".
- **Dress the community like a real one:** description, info text, an upcoming event, a pinned welcome post, a pinned link, a few experts.
