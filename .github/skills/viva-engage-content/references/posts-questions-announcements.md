# Discussions, questions, announcements

## Community landing page

Open `BASE_URL + "/main/groups/<group-id>/all"` (store one URL per community; read them once from the left navigation of an account that is a member). Wait for the publisher:

```python
await page.get_by_role("button", name=re.compile(r"^(Discussion)$")).first.wait_for(state="visible", timeout=60000)
```

The publisher offers **Discussion, Question, Praise, Poll** (plus a *Drafts* icon). There is **no** Announcement button.

## Join first

A *Join* button appears at the top for non-members. Match it narrowly:

```python
join = page.get_by_role("button", name=re.compile(r"^(Join)( community .*)?$", re.I))
if await join.count() and await join.first.is_visible():
    await join.first.click()
    await join.first.wait_for(state="hidden", timeout=15000)
```

Do not use `^Join`: accounts with an admin role see a banner button called *Join preview* (community agent preview) that also starts with "Join" and navigates to environment admin settings.

## Discussion

```python
await page.get_by_role("button", name="Discussion", exact=True).first.click()      # opens the composer dialog
editor = page.locator('[contenteditable="true"]:visible').last
await editor.click()
await page.keyboard.type(f"{title}\n\n{body}", delay=4)
post = page.get_by_role("button", name=re.compile(r"^Post$")).last
await expect(post).to_be_enabled()
await post.click()
```

The composer is a dialog (portal). The toolbar of the composer holds *Bold, Italic, lists, link, code snippet*, then **Announcement**, mention, emoji, image, GIF, "Post". There is no separate title; the post card shows the first paragraph as the visible headline.

## Question

```python
await page.get_by_role("button", name="Question", exact=True).first.click()
title_field = page.get_by_placeholder("Ask a question (required)").first
await title_field.wait_for(state="visible")
await title_field.fill(title if title.endswith("?") else title + "?")                # store this displayed title
editor = page.locator('[contenteditable="true"]:visible').last                        # optional description
await editor.click(); await page.keyboard.type(body, delay=4)
await page.get_by_role("button", name=re.compile(r"^(Ask)$")).last.click()           # note: "Ask", not "Post"
```

Questions show a *QUESTION* label; replies to them are called **answers** ("Answer - <author>'s question"). Questions are what *Top questions*, best answers, and "unanswered" views are built on.

## Announcement

In current builds an announcement is a **discussion with the megaphone switch on**. It notifies community members (the composer shows an info bar saying how many people will be notified). It needs the **admin** role in that community.

```python
await page.get_by_role("button", name="Discussion", exact=True).first.click()
switch = page.get_by_role("button", name=re.compile(r"^Announcement$")).first
await switch.wait_for(state="visible", timeout=8000)     # missing -> the account is not an admin here
await switch.click()
editor = page.locator('[contenteditable="true"]:visible').last
await editor.click(); await page.keyboard.type(f"{title}\n\n{body}", delay=4)
await page.get_by_role("button", name=re.compile(r"^Post$")).last.click()
```

The resulting thread page shows an *Announcement posted in <community>* header. There is no title field, so put the headline in the first paragraph.

Older instructions that look for an "Announcement" type button next to Discussion/Question, or an "Add a title" field, do not match current builds.

## After submitting: find the card and the permalink

New cards appear at the top after a short delay; poll the feed up to ~12 s (reload once halfway) and read the timestamp link of the matching card. See `viva-engage-automation` -> idempotency for the harvest script. Store `{url, title, community, author}`.

## Duplicate protection

Before opening the composer, look for an existing card with the same title (substring match on the first characters of the card text). If it exists, return its permalink and mark the row done with mode "existing".

## Gotchas

- `get_by_role("button", name="Post")` can match several buttons; the composer's submit is the **last** one in the DOM.
- The submit button stays disabled until the editor has content - assert `to_be_enabled` before clicking.
- Do not type the title into the description editor of a question; the title field is separate and required.
- Titles with a trailing `?` for questions: decide once and store the displayed form.
- Posting into a community the account has not joined can silently work or fail depending on community privacy - join first.
