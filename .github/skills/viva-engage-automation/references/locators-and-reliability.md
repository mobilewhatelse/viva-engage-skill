# Locators and reliability

Viva Engage is a React/Fluent UI app with generated CSS class names, portals, and controls that only exist after a click. These rules came from real failures.

## 1. A visible "placeholder" is often not a placeholder

The comment box shows the text *"Write a comment"*, but it is a plain `DIV` with no `placeholder` attribute, no `contenteditable`, no `role`. `get_by_placeholder`, `[placeholder=...]`, and XPath on `@placeholder` all find nothing. Clicking it replaces it with the real editor:

```python
box_text = re.compile(r"^(Write a comment|<other UI languages>)$", re.I)
await page.get_by_text(box_text).last.click()                         # the fake placeholder
editor = page.get_by_role("textbox", name=re.compile("Write a comment", re.I)).last
await editor.wait_for(state="visible")
```

The real editor is `role=textbox`, `contenteditable`, with an accessible name equal to the old placeholder text, and it brings its own **Post** button. **Enter does not submit** (it inserts a new line).

Lesson: when a locator fails on something you can see, dump the DOM around it (tag, role, aria-label, contenteditable, parents) before changing the strategy:

```python
info = await page.evaluate("""() => [...document.querySelectorAll('div,span,button')]
  .filter(e => e.childElementCount === 0 && e.textContent.trim() === 'Write a comment')
  .map(e => ({tag: e.tagName, role: e.getAttribute('role'), parent: e.parentElement?.tagName}))""")
```

## 2. Prefer roles and accessible names

Buttons carry informative labels that include the author and the item kind:

- `Like - <author>'s post`, `Like - <author>'s answer`, `Reply - <author>'s comment`
- `Comment - ...` on posts, `Answer - ...` on questions
- `Mark answer as best or verified`, `More actions`, `View more message options`
- `Add to favorites` / `Remove from favorites`

Use `get_by_role("button", name=re.compile(r"^Like - "))` rather than icons or classes. Buttons may exist twice in the DOM (a main button and a dropdown trigger) - use `.first`.

## 3. Tag a container with a tiny DOM script

To act on "the comment that contains this text" (reply, react, mark as best), find the deepest element containing the text, climb to the smallest ancestor that also contains a Like button, and tag it:

```python
TAG_JS = r"""(snippet) => {
  document.querySelectorAll('[data-demo-c]').forEach(e => e.removeAttribute('data-demo-c'));
  const norm = s => (s || '').replace(/\s+/g, ' ').trim().toLowerCase();
  const t = norm(snippet);
  const hits = [...document.querySelectorAll('div,span,p')].filter(e => norm(e.innerText).includes(t));
  const deepest = hits.filter(e => !hits.some(o => o !== e && e.contains(o)));
  for (const el of deepest) {
    let e = el;
    while (e && e !== document.body) {
      if (e.querySelector('button[aria-label^="Like -"]')) { e.setAttribute('data-demo-c', '1'); return true; }
      e = e.parentElement;
    }
  }
  return false;
}"""
ok = await page.evaluate(TAG_JS, text[:60])
comment = page.locator('[data-demo-c="1"]')
await comment.get_by_role("button", name=re.compile(r"^Reply - ")).first.click()
```

In the community feed every post card is an `<li>` containing exactly one comment box and a timestamp link to the thread. `leaf.closest('li')` is a reliable card boundary; the right-hand "Top questions" widget is outside those `<li>` elements, so it cannot produce false matches.

## 4. Sidebar widgets repeat titles

The same question title can appear in the feed card and in a right-hand "Top questions" list (as a link). When matching by title, restrict the match to feed cards (see above) or to the thread page, never to "any element with this text".

## 5. Portals, dialogs, and intercepted clicks

Composer, topic dialogs, and menus render in portals. Symptoms and fixes:

- *"<div class='fui-DialogContent'> intercepts pointer events"*: another dialog or popup is still open. Close it, or `locator.focus()` the target instead of clicking, or click with `force=True` only when you know why.
- Menus: `role=menuitem`; their entries combine title and description in one element, so `get_by_text("Best answer", exact=True)` fails. Use `page.locator("[role^=menuitem]").filter(has_text="Best answer")`.
- Dropdown lists (for example event times) are `role=option` inside a `listbox`.

## 6. Waiting rules

- `locator.is_visible(timeout=...)` ignores the timeout. Use `wait_for(state="visible")` in `try/except`.
- Prefer waiting for a *state change* over fixed sleeps: the editor became hidden, the text appeared, the URL left the "new" page.
- After submitting a post/comment, wait for the editor to detach **and** for the text to be visible, then continue.
- `expect(button).to_be_enabled()` before clicking Post: the button stays disabled until the editor has content.

## 7. Typing

- `page.keyboard.type(text, delay=4)` into a focused `contenteditable` is reliable; `locator.fill()` works for `<input>`/`<textarea>` only.
- Newlines typed with `\n` create paragraphs (`"title\n\nbody"` renders a blank line between).
- `Control+End` moves the caret to the end - needed after the editor pre-filled a mention in a reply.
- Clearing a search box that is a combobox: `Control+A`, `Backspace` - not `fill("")` after the previous text was typed by the keyboard.

## 8. Transient server errors

The app occasionally renders a blank page with *"This page isn't loading right now. Please try again in a few minutes."* Wrap every navigation:

```python
async def goto_robust(page, url, tries=5):
    for attempt in range(tries):
        await page.goto(url, wait_until="domcontentloaded")
        await page.wait_for_timeout(1500)
        if not await page.get_by_text(re.compile(r"isn't loading right now", re.I)).count():
            return
        await page.wait_for_timeout(5000 * (attempt + 1))
    raise RuntimeError("page keeps failing to load")
```

## 9. Pacing

Randomized pauses of roughly 0.5-2 s between actions look less like a burst and avoid rate-related hiccups. Use `await page.wait_for_timeout(...)`, not `time.sleep` (which blocks the event loop).

## 10. Environment gotchas

- Do not name your helper script `inspect.py` (or any standard-library module name) - it shadows the standard library and breaks `asyncio` imports in the same folder.
- On Windows consoles set `PYTHONIOENCODING=utf-8`, otherwise German umlauts in log output look garbled although the data is fine.
- `page.locator("input:visible")` is Playwright selector syntax. It is **not** valid inside `document.querySelectorAll` in `page.evaluate`.
- Long-running foreground commands may time out in tooling; run bulk phases in the background with output redirected to a log file and poll the log.
