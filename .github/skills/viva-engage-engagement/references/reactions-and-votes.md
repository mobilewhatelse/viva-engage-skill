# Reactions and poll votes

## Reaction picker

Every post and every comment has a **Like** button. Hovering over it shows the picker:

| Name in the picker | Notes |
|---|---|
| Like | A plain click on the Like button (no hover needed) |
| Love | |
| Laugh | |
| Celebrate | |
| Thank | The clapping-hands reaction |
| Sad | |
| More reactions | Opens a larger set |

Map your data's reaction vocabulary explicitly in configuration, for example:

```yaml
reaction_map:
  Like: Like
  Love: Love
  Celebrate: Celebrate
  Insightful: Thank        # not offered by the UI; pick the closest meaning on purpose
```

## Reacting

```python
async def react(page, thread_permalink, comment_text_or_none, reaction):
    await open_thread(page, thread_permalink)
    scope = page if comment_text_or_none is None else await tag_comment(page, comment_text_or_none)
    like = scope.get_by_role("button", name=re.compile(r"^Like - ")).first
    await like.scroll_into_view_if_needed()
    if reaction == "Like":
        await like.click()
    else:
        await like.hover()
        option = page.get_by_role("button", name=reaction, exact=True).last
        await option.wait_for(state="visible")
        await option.click()
    await page.wait_for_timeout(1000)
```

- On a thread page the **first** `Like - ...` button is the post's own; comments' buttons follow. For a comment, tag its container first (see `viva-engage-automation` -> locators).
- After a reaction, the button label changes (for example `Add reaction - Celebrate`) and the card shows a summary like "<user> and N others" with the reaction icons.
- Clicking the same reaction again **removes** it. Clicking a different one **replaces** it. So: at most one reaction per user per target.
- The post author may react to their own post, but a realistic demo avoids it.

## Poll votes

```python
await open_thread(page, poll_permalink)
radio = page.get_by_role("radio", name=option_text, exact=True)
if await radio.count() == 0:
    radio = page.get_by_label(option_text, exact=True)
await radio.first.check()
vote = page.get_by_role("button", name=re.compile(r"^Vote$")).first
await expect(vote).to_be_enabled()
await vote.click()
await page.get_by_text(re.compile(r"total vote", re.I)).first.wait_for(state="visible")
```

- Match option text **exactly** as typed when the poll was created.
- One vote per account per poll. The result bars then show counts ("5 votes", "1 vote").
- Admins can close voting from the post menu (*Close voting*).

## Choosing realistic data

- Spread reactions: most Likes, some Love/Celebrate/Thank, a few posts without any.
- Votes: one dominant option, a runner-up, a long tail, one option with zero.
- Do not let the same handful of accounts react to everything in the same order; vary by post.
- Reaction phases are the biggest (hundreds of items); run them last and in the background with a log file.
