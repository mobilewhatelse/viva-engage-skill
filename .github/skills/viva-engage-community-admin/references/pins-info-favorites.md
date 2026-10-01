# Pins, links, community info, favorites

## Pin a conversation

The menu entry **Pin conversation** exists in the post menu (`View more message options`) **in the community feed**. The thread page's menu does not contain it. Find the post's card by its permalink and open its menu:

```python
path = permalink                                              # "/main/threads/<id>"
card = page.locator("li").filter(has=page.locator(f'a[href="{path}"]'))
for _ in range(12):                                           # scroll until the card is rendered
    if await card.count(): break
    await page.mouse.move(700, 600); await page.mouse.wheel(0, 1600); await page.wait_for_timeout(1200)
await card.first.get_by_role("button", name="View more message options").first.click()
item = page.get_by_role("menuitem", name=re.compile(r"Pin conversation")).first
await item.wait_for(state="visible"); await item.click()
```

The post then moves to the top with a *Pinned conversation* (or *Pinned announcement*) header and a pin marker. Pinned posts are a good place for the welcome message and the most important announcement.

The same menu offers: *View analytics, Delete, Move, Close conversation, Close voting (polls), Bookmark, Copy link, Follow in inbox, View conversation, Add/Edit topics, Hide their messages*.

## Pin a link

Right column, section **Pinned links and files** -> **Pin link**:

```python
await page.get_by_role("button", name=re.compile(r"Pin link|Add a pinned resource")).first.click()
await page.locator("input[type=url]").first.fill(address)          # "Add a link" dialog: Address
await page.locator("[role=dialog] input[type=text]").last.fill(title)  # Title
await page.get_by_role("button", name="OK", exact=True).click()
```

The link then appears under *Pinned links and files* with its title. Use meaningful titles (a guideline, a reference, a landing page); keep link targets harmless and generic in demos.

## Community info text

Right column, **Info** -> **Add community info** (or **Edit** once set). It opens the community's **Settings** page. That page has several sections, each with its own **Save** button:

1. *Community details* (name, description) - its Save stays disabled until you change those fields.
2. *Community information* (rich-text editor) - the one you want.

```python
editor = page.get_by_role("textbox", name=re.compile(r"Community information editor"))
await editor.first.click()
await page.keyboard.press("Control+A")
await page.keyboard.type(info_text, delay=4)
save = page.get_by_role("button", name=re.compile(r"^Save$")).nth(1)      # second Save belongs to the info editor
await expect(save).to_be_enabled()
await save.click()
```

Using `.first` picks the disabled Save of the details section and the click times out.

The text then shows in the right column under **Info** (with an *Edit* link). Keep it 1-3 sentences: purpose, who it is for, how to get help.

## Favorites

The heart in the community header marks the community as a favorite for the signed-in user; favorites move to a **Favorites** group in the left navigation.

Traps:

- The left navigation also has `Add to favorites` / `Remove from favorites` buttons per community (appearing as an icon on hover). `get_by_role(...).last` or `.first` often hits one of those and favorites the **wrong** community.
- The header heart renders a few seconds after the feed. Wait for it (poll for up to ~20 s).
- Pick the header control by **position** (x larger than the left navigation width, around 400 px at a 1440 px viewport):

```python
async def header_star(page, label):
    buttons = page.get_by_role("button", name=label)
    for i in range(await buttons.count()):
        box = await buttons.nth(i).bounding_box()
        if box and box["x"] > 400:
            return buttons.nth(i)
```

- Already a favorite? The label is *Remove from favorites* - treat as done.
- To undo a wrong favorite, click the matching *Remove from favorites* in the left navigation (`force=True` may be needed because it only shows on hover).
