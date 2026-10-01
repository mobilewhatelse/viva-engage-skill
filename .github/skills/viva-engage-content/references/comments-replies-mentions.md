# Comments, answers, replies, mentions

## Open the thread by permalink

```python
await goto_robust(page, BASE_URL + permalink)                      # retry on "isn't loading right now"
box_text = re.compile(r"^(Write a comment)$", re.I)
await page.get_by_text(box_text).last.wait_for(state="visible", timeout=60000)
```

A thread page has exactly one top-level comment box. Open a thread directly instead of scrolling the feed - it is faster and unambiguous.

## Comment / answer

```python
if await page.get_by_text(text[:60]).count():                       # already there?
    return "existing"
await page.get_by_text(box_text).last.click()                       # fake placeholder -> real editor
editor = page.get_by_role("textbox", name=re.compile("Write a comment", re.I)).last
await editor.wait_for(state="visible")
await editor.click()
await type_text(page, text)                                         # handles @mentions, see below
post = page.get_by_role("button", name=re.compile(r"^Post$")).last
await expect(post).to_be_enabled()
await post.click()
await editor.wait_for(state="hidden", timeout=60000)               # closes after a successful post
await page.get_by_text(text[:60]).first.wait_for(state="visible", timeout=60000)
```

- On a **question**, the same box creates an **answer**; the post action reads "Answer" instead of "Comment".
- **Enter does not submit** - click *Post*.
- Collapsed older comments ("Show N comments") are not in the DOM; the state file is the second line of defence against duplicates.

## Reply to a comment

Each comment has `Like - <author>'s comment|answer`, `Reply - <author>'s ...`, `More actions`, and (for admins/experts/the asker) `Mark answer as best or verified`.

```python
comment = await tag_comment(page, parent_text)                      # see locators-and-reliability (TAG_JS)
await comment.get_by_role("button", name=re.compile(r"^Reply - ")).first.click()
editor = page.get_by_role("textbox", name=re.compile(r"Write a reply", re.I)).last
await editor.wait_for(state="visible"); await editor.click()
await page.keyboard.press("Control+End")                            # editor is pre-filled with the parent author's mention
await page.keyboard.type(" " + reply_text, delay=4)
await page.get_by_role("button", name=re.compile(r"^Post$")).last.click()
await editor.wait_for(state="hidden")
```

- Replies are **one level deep**; there is no reply-to-reply.
- Replies are shown collapsed under the comment ("1 reply"), so check the state file rather than the page to avoid double replies.
- The parent author is mentioned automatically (a chip below the editor). Write the reply so that it reads naturally after that mention.
- A reply author should differ from the parent comment's author when the text addresses them by name.

## Real @mentions

Typing `@Firstname Lastname` opens a people picker. Pick the entry, otherwise the text stays plain:

```python
MENTION = re.compile(r"@([A-ZÄÖÜ][\wäöüß-]+(?: [A-ZÄÖÜ][\wäöüß-]+)?)")

async def type_text(page, text, delay=4):
    pos = 0
    for m in MENTION.finditer(text):
        await page.keyboard.type(text[pos:m.start()], delay=delay)
        name = m.group(1)
        await page.keyboard.type("@" + name, delay=40)               # slow typing lets the picker filter
        option = page.locator("[role=option]:visible").filter(has_text=name).first
        try:
            await option.wait_for(state="visible", timeout=5000)
            await option.click()
            await page.keyboard.type(" ", delay=delay)
        except Exception:
            pass                                                     # no match: leave as plain text
        pos = m.end()
    await page.keyboard.type(text[pos:], delay=delay)
```

- The mentioned person must exist and be visible to the acting user.
- A mention creates an `@` notification for that person and a small `@N` marker on the post header - a nice demo detail.
- A mention can leave a double space in the rendered text; harmless.
- Make the regex match the text style of your language; names ending a sentence with punctuation are fine because the character class stops at the punctuation.
- Use mentions in at least a few comments and posts so the notification experience is visible.

## Verifying

Open the thread as a different user and check: comment author and text, "1 reply" under the parent, the mention rendered as a highlighted name, the `@` marker on the post header.
