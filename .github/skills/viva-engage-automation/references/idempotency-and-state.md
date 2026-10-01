# Idempotency and state

A seeding run touches hundreds of items and will be interrupted. Design so that restarting is always safe.

## Three layers of protection

1. **Status column per row** in the spreadsheet: `Pending` -> `Posted` / `Done`, `Error` (+ `ErrorMessage`), `Skipped`. A run processes only `Active = Yes` and `Pending` (plus `Error` with a `--retry-errors` flag).
2. **State file** (`state.json`, ignored by git) with permalinks and markers:
   ```json
   {
     "posts":       {"<PostKey>":    {"url": "/main/threads/<id>", "title": "...", "community": "...", "author": "<account>"}},
     "comments":    {"<CommentKey>": {"thread": "<permalink>", "user": "<account>", "post": "<PostKey>"}},
     "done":        {"<ActionKey>":  {"user": "<account>"}},
     "substitutes": {"<RowKey>": "<account or null>"}
   }
   ```
3. **Existence check in the UI** right before creating anything: search the target feed (or thread) for the title/text; if found, record it and move on.

Use all three: the spreadsheet is the human-visible truth, the state file makes lookups instant and survives a hand-edited spreadsheet, and the UI check protects against both being wrong.

## Capture permalinks once

Every post has a timestamp link `a[href*="/main/threads/"]` inside its card. After publishing, find the new card in the community feed and read that `href`; afterwards open threads directly:

```python
HARVEST_JS = r"""(labels) => {
  const L = labels.map(s => s.toLowerCase());
  const isBox = e => e.childElementCount === 0 && L.includes((e.textContent || '').trim().toLowerCase());
  const out = [], seen = new Set();
  for (const leaf of document.querySelectorAll('div,span,p,button')) {
    if (!isBox(leaf)) continue;
    const card = leaf.closest('li');
    if (!card) continue;
    const a = card.querySelector('a[href*="/main/threads/"]');
    if (!a) continue;
    const href = a.getAttribute('href');
    if (seen.has(href)) continue;
    seen.add(href);
    out.push({href, text: card.innerText});
  }
  return out;
}"""
```

Match a card by normalized title: `needle in norm(card_text)[: len(needle) + 250]`. A **substring** match is deliberate: a question's displayed title gets a trailing `?`, and a discussion's title is just the first paragraph of the body.

Scroll to load more cards (`page.mouse.wheel(0, 1600)` after moving the mouse over the feed) and stop when the card count does not grow for three scrolls.

## Titles you typed are not always the titles shown

- Questions: the title field accepts text; the UI shows it as typed. If the source data has no trailing `?`, decide once (append it) and store the *displayed* title.
- Discussions and announcements have no separate title: the "title" is the first paragraph. Search with the title as a substring.
- Polls: the question text is the match text. Praise: there is no title - match on the first ~50 characters of the praise text.

## Excel handling

- Keep **one workbook object per file** in the process (cache by path). Two `ExcelStore` instances on the same file would each save their own in-memory copy and overwrite each other.
- Save after every item; close the file in Excel while a run is active (a locked file makes `save()` fail).
- Never regenerate the workbook from scratch - formatting and other sheets must survive.
- Regenerate a "supplement" workbook only when it does not exist, so status columns are never lost.

## Single writer rule

Never run two runner processes at the same time that both write the same state file or spreadsheet: each does read-modify-write and the later write silently discards the earlier one. Read-only dry runs and screenshot probes are fine. Chain phases sequentially (`for ph in ...; do run.py --phase $ph; done`).

## Resuming after a crash

- Killing a process during `wb.save()` can corrupt a workbook - verify every workbook still opens after an abort.
- Rows that failed before the click stay `Pending`/`Error`; rows that failed *after* the click (text posted but verification timed out) are caught by the existence check on the next run.

## Uniqueness that the UI enforces

A user can react or vote **once** per target; clicking again toggles the reaction off or is rejected. Therefore the planner must guarantee one action per (user, target) before any browser starts. See `viva-engage-engagement`.
