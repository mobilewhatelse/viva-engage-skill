# Troubleshooting

| Symptom / message | Cause | Fix |
|---|---|---|
| Comment box "not found" although clearly visible | The visible "Write a comment" is a text `DIV`, not a placeholder | Click the text; then use the new `role=textbox` editor |
| Comment typed but nothing happens after Enter | Enter inserts a newline | Click the editor's **Post** button (wait until enabled) |
| Wrong post commented / first post of the feed commented | Matched the sidebar "Top questions" entry, or the page wrapper | Match inside a feed card (`li`) or open the permalink |
| `Locator.click: Timeout` on "Join" and the browser lands on an admin settings page | A banner button *"Join preview"* matched a loose `^Join` pattern | Match `^(Join)( community .*)?$` |
| Sign-in times out after the password step; screen says "Let's keep your account secure" | Environment forces MFA registration | See `sessions-and-login.md`; or use stand-in users |
| `is_visible(timeout=...)` returns False immediately | The timeout argument is ignored | `wait_for(state="visible")` in try/except |
| "This page isn't loading right now" screenshot | Transient server error | `goto_robust` with retry and backoff |
| `<div class="fui-DialogContent"> intercepts pointer events` | Another dialog is open or a popup overlaps | Close it, `focus()` the field, or fix the step order |
| Menu item "Best answer" not found by text | Title and description share one element | `locator("[role^=menuitem]").filter(has_text=...)` |
| Menu has no "Add topics" but "Edit topics" | The post already has topics | Match `Add topics\|Edit topics`; skip topics already present |
| "The topic X already exists" in the create-topic dialog | Search results list it as a card, not as `role=option` | Click the text hit; create only if there is truly no hit |
| Second topic is appended to the first one's search text | Combobox keeps the typed text | `Control+A`, `Backspace` before typing the next topic |
| "Assign experts" missing on the community page | Once experts exist the entry is labelled **Add user** | Match both labels |
| Role never applied for users named "... Admin..." | Role check looked at the whole row text (name/title contain "admin") | Read only the role dropdown button's text |
| Favorite set on the wrong community | `.last` of "Add to favorites" was a left-navigation item | Choose the star by position (x greater than the navigation width) after the header has loaded |
| Event date field "not editable" | Date and time are pickers | Date: calendar popup, day button has an aria-label like `15, October, 2026`; time: click, then `role=option` |
| Event step "succeeds" but nothing verified | `wait_for_url` regex also matched the "new event" URL | Wait for `!location.href.includes('/new')` |
| Second click on a reaction removed it | Reactions toggle | Plan one action per user per target |
| Two runs, results missing in the spreadsheet or state | Both processes saved over each other | One writer at a time |
| `ImportError: cannot import name 'AbstractEventLoop'` | A local file shadows a standard-library module (for example `inspect.py`) | Rename the script |
| Garbled umlauts in the console | Console code page | `PYTHONIOENCODING=utf-8`; the data itself is fine |
| `PermissionError` on saving the workbook | File open in Excel | Close it |
| `SyntaxError` in `page.evaluate` for `input:visible` | Playwright-only selector syntax inside DOM code | Use plain CSS and filter by `offsetParent` in JS |
