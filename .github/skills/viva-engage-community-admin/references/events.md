# Events

Right column of the community landing page, section **Admin actions** -> **Create event** (admins only). It opens a full page, not a dialog, which can take several seconds to render (first a skeleton).

## Form layout

| Field | Control | Notes |
|---|---|---|
| Title | text input, placeholder *Give your event a title.* | required |
| Start date / End date | read-only text field with a calendar popup | **not typeable** |
| Start time / End time | read-only combobox with a list | **not typeable** |
| About | textarea | shows on the event page and in the calendar invitation |
| Host this event in a storyline or community | collapsed section, preset to the community you came from | |
| Enable broadcast or meeting | toggle | off = text-based, asynchronous event |
| Roles, Who can attend, Calendar invitation, Engagement options | collapsed sections | defaults are fine |
| Create | button, disabled until the title is set | |

The time zone note under the dates shows the browser's time zone.

## Input order in the DOM

`input[type=text]` (visible): title (0), start date (1), start time (2), end date (3), end time (4). Index numbering depends on the search box not being a text input - dump `value` of all inputs once to confirm.

## Pick a date

Click the date field; a calendar popup opens. Each day is a button with an aria-label like `15, October, 2026`. If the target month is not shown, the popup's right-hand panel has month tiles (`Jan`, `Feb`, ...): click the tile, then the day.

```python
async def pick_date(page, field, d):                               # d: datetime.date
    day_label = f"{d.day}, {d.strftime('%B')}, {d.year}"
    await field.click()
    day = page.get_by_role("button", name=day_label, exact=True)
    for _ in range(2):
        try:
            await day.first.wait_for(state="visible", timeout=2500); break
        except Exception:
            await page.get_by_text(d.strftime("%b"), exact=True).last.click()
    await day.first.click()
```

## Pick a time

Click the time field; a listbox of half-hour steps opens (`12:00 AM`, `12:30 AM`, ...). Each entry is `role=option`:

```python
await field.click()
option = page.get_by_role("option", name="10:00 AM", exact=True)
await option.first.scroll_into_view_if_needed()
await option.first.click()
```

Use the 12-hour format the UI shows (`2:00 PM`).

## Create and verify

```python
await page.locator("textarea").first.fill(about)
create = page.get_by_role("button", name="Create", exact=True)
await expect(create).to_be_enabled()
await create.click()
# success = the "new event" page is left
await page.wait_for_function("() => !location.href.includes('/new')", timeout=60000)
```

A naive `wait_for_url` with a pattern such as `/events|/ama/` also matches the *new event* URL itself and returns too early.

Verify on the community landing page: the right column shows **Events** with the title and date/time (for example "Oct 15, 10:00 AM - 11:00 AM"). The event also gets its own page URL; the resulting page may include a meeting-style entry even for plain events.

## Content ideas

A review session, an expert talk, a quarterly steering meeting, a technology radar review - dated a few weeks ahead, with a two-sentence description that matches posts in the community.
