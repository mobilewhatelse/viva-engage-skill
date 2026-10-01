# Demo seeding playbook

How to fill a Viva Engage demo environment so it looks alive, in the order that avoids dependency problems.

## Data model (spreadsheets)

One sheet per content family, each with `Sequence`, `Active`, a stable key column, the acting user, the content, and `Status` / `ResultURL` / `ErrorMessage`:

| Sheet | Key | Notes |
|---|---|---|
| Memberships | (community + user) | role: Member / Admin / Expert |
| Posts | PostKey | type: Discussion / Question / Announcement; community; title; body; topic |
| Polls / Praise | PostKey | polls: question + up to four options; praise: recipient + text |
| Comments | CommentKey | refers to PostKey |
| Replies | ReplyKey | refers to ParentCommentKey (+ PostKey) |
| Votes | VoteKey | refers to a poll PostKey + option text |
| Reactions | ReactionKey | TargetType Post/Comment, TargetKey, reaction name |
| BestAnswers | CommentKey | the answer to mark |
| Topics / Pins / Events / CommunityInfo / NewPosts / Favorites | per sheet | supplement workbook |

Write content in the audience's language and make it plausible: questions that invite several answers, answers that disagree a little, announcements that mention events, praise with a concrete reason.

## Phase order

| # | Phase | Why here |
|---|---|---|
| 0 | Members and roles | Admin and expert roles must exist before announcements and best answers |
| 1 | Posts (discussion, question, announcement) | Everything else attaches to posts |
| 2 | Polls and praise | Also posts; needed before votes and comments on them |
| 3 | Comments | Need their posts |
| 12 | Supplement posts (mentions, images) | New posts that later phases can decorate |
| 4 | Replies | Need their parent comments |
| 5 | Poll votes | Need polls |
| 6 | Reactions | Need posts and comments; the biggest phase, run it late |
| 7 | Best answers | Need answers |
| 8 | Topics | Need posts (also for the supplement posts) |
| 9 | Pin posts and links | Need posts |
| 10 | Events | Independent |
| 11 | Community info | Independent |
| 13 | Favorites | Independent |

Within a phase, group by acting user. Keep `Sequence` order per user. Run `--dry-run`, then `--limit 1` / `--only-key X`, then the whole phase.

## Verify like a user

- Open the permalink as a **different** user and take a screenshot; compare with what you expected (badge, chips, counts, "pinned" label, event card in the sidebar).
- Check the community landing page: member count, expert list, info text, events widget, "Top questions" with best-answer badges, pinned items.
- Look at the first item of every new content type manually before running a hundred of them.

## Make it look used

- Reactions spread across several users and several reaction kinds; a few posts with none.
- Some questions **without** answers (for an "unanswered" view), some with a best answer.
- Polls with uneven results.
- A few posts with images, mentions, and topics; one or two pinned.
- Events a few weeks in the future with a short description.
- Opening threads as other users raises the "Seen by" counts naturally.

## Hard limits

- No backdating: everything is "just now" (timestamps cannot be set from the UI).
- No automatic Copilot summaries; they depend on licensing and are generated on demand.
- Live events with a meeting/broadcast require the meeting integration; plain asynchronous events work.
- You cannot create communities with this material beyond what the UI offers; community creation is not covered.

## Cleaning up

Deleting is a per-item UI action (post menu -> Delete) or an admin export/delete script. Plan duplicates away instead of cleaning them (existence checks), and never seed in a production environment.
