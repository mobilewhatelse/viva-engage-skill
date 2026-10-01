# Stand-in users

Sometimes only some demo accounts can sign in automatically (the others are forced into multi-factor registration, or their password is unknown). The roles those accounts should play can be taken over by accounts that do have a recorded session. This is a conscious trade-off: authorship in the demo no longer matches the planned persona. Say so in your hand-over notes.

## Rules the planner must guarantee

1. **A stand-in is chosen by role similarity.** Keep an ordered preference list per original user in a config file; pick the first that does not violate rules 2-4.
2. **Never self-directed:** a stand-in must not comment on a post it authored, praise itself, or react to its own comment when the plan said someone else would.
3. **One action per (user, target)** for reactions and votes, and **one comment per user per post** if the data assumes distinct commenters. Otherwise a reaction toggles off or a vote is rejected.
4. **Admin-only content goes to an admin stand-in** (announcements, pinning, topic creation, best answers). If the original persona had the admin role, choose a stand-in with the admin role.
5. **The assignment is deterministic and persisted** (state file: `substitutes[rowKey] = account or null`). Later phases (replies to a comment, reactions on a post) must resolve the *same* stand-in for the same key.
6. **Exhausted pool means skip.** When all candidates are taken for a target, store `null` and set the row to `Skipped` with a reason. Do not fall back to duplicates for reactions and votes.

## Algorithm sketch

```python
def assign_unique(rows_pending, rows_all, group_of, base_taken, can_sign_in, prefer, pool):
    for group, pending in group_by(rows_pending, group_of):
        taken = set(base_taken(group))                       # e.g. the target's author
        for row in rows_all_in(group, rows_all):             # includes already finished rows
            if row.key in done:           taken.add(done[row.key].user)
            elif row.key in substitutes:  taken.add(substitutes[row.key])
            elif can_sign_in(row.user):   taken.add(row.user)
        for row in sorted(pending, key=sequence):
            if can_sign_in(row.user):
                row.actor = row.user
            else:
                if row.key not in substitutes:
                    candidate = first(c for c in prefer[row.user] + pool if c not in taken)
                    substitutes[row.key] = candidate         # may be None
                    if candidate: taken.add(candidate)
                row.actor = substitutes[row.key]             # None -> Skipped
```

Variants:

- **Authors of posts:** `taken` is empty; just choose the best role match (and the admin stand-in for announcements).
- **Comments:** `taken` starts with the post's effective author.
- **Replies:** `taken` starts with the parent comment's effective author (replies often address them by name).
- **Reactions/votes:** the group is the target (`post:<key>` or `comment:<key>`, or the poll key).

## Practical numbers

With 8 usable accounts and 19 planned personas, polls with 10-13 planned votes will lose a few rows to `Skipped`, which is acceptable; the poll still shows a believable distribution.

## What not to do

- Do not rotate through stand-ins randomly per run: the same persona must map to the same stand-in everywhere.
- Do not hide the substitution: print `Stand-in X (instead of Y)` in dry-run output and keep the original persona name in the spreadsheet.
- Do not use this to impersonate real people outside a demo; it is for fictitious personas in a test or demo environment you own.
