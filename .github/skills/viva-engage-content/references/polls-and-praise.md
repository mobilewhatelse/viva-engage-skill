# Polls and praise

## Poll

```python
await page.get_by_role("button", name=re.compile(r"^(Poll)$")).first.click()
q = page.get_by_role("textbox", name=re.compile(r"What is your question", re.I))
await q.wait_for(state="visible")
await q.click(); await page.keyboard.type(question, delay=4)
for i, option in enumerate(options, start=1):                    # 2-4 options worked; more fields appear as you fill
    field = page.get_by_placeholder(re.compile(rf"^Answer {i}$")).first
    await field.wait_for(state="visible")
    await field.fill(option)
submit = page.get_by_role("button", name=re.compile(r"^(Ask)$")).last      # polls are submitted with "Ask"
await expect(submit).to_be_enabled()
await submit.click()
```

- The composer starts with three answer inputs (`Answer 1..3`); filling the last one reveals the next.
- The poll card shows a **POLL** label, the options as radio buttons, a disabled **Vote** button until an option is chosen, and "N total votes . Go to results".
- Poll match text for the permalink lookup: the question.
- Admins can later close voting from the post menu (*Close voting*).

### Voting (see also `viva-engage-engagement`)

```python
radio = page.get_by_role("radio", name=option_text, exact=True)
await radio.first.check()
await page.get_by_role("button", name=re.compile(r"^Vote$")).first.click()
```

One vote per account per poll. Plan that before running (a user mapped onto two roles would vote twice and the second attempt changes or fails).

## Praise

```python
await page.get_by_role("button", name=re.compile(r"^(Praise)$")).first.click()
box = page.get_by_placeholder(re.compile(r"Who do you want to praise", re.I)).first
await box.click()
await page.keyboard.type(recipient_display_name, delay=40)
option = page.locator("[role=option]:visible").filter(has_text=recipient_display_name).first
await option.wait_for(state="visible"); await option.click()               # the recipient becomes a chip
editor = page.locator('[contenteditable="true"]:visible').last             # "Share what they've done."
await editor.click(); await page.keyboard.type(text, delay=4)
await page.get_by_role("button", name=re.compile(r"^(Praise)$")).last.click()
```

- The recipient must exist in the environment; they do **not** need a recorded session (only the author acts).
- In current builds there is **no badge picker**. Do not wait for one; if a data sheet has a badge column, either ignore it or mention the badge in the text.
- The card shows a **PRAISE** label and "Praised <recipient>".
- The author cannot sensibly praise themselves - when using stand-in users, check that the stand-in is not the recipient.
- Praise has no title; use the first ~50 characters of the text as the match key for the permalink lookup.

## Scoping gotchas

- The publisher row and the dialog both contain buttons named "Praise" / "Poll" / "Ask"; the dialog's submit is the last one in DOM order.
- `get_by_text(recipient)` can hit a hidden span elsewhere on the page; use the visible `role=option`.
