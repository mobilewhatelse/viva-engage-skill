# Best answers and verified answers

Questions have **answers** (comments on a question). Two markers exist:

| Marker | Meaning in the UI | Who can set it |
|---|---|---|
| **Best answer** | "Helpful and insightful response" | Community admin, community expert, or the person who asked the question |
| **Verified answer** | "Response validated by a community expert" | Community expert / admin |

Plain members do not see the control at all - not seeing `Mark answer as best or verified` means the account has no such role in that community.

## Controls

Each answer has a split button with a checkmark whose accessible name is **Mark answer as best or verified**. It opens a menu titled *Mark as* with two menu items (each combines title and description in one element):

```python
answer = await tag_comment(page, answer_text)
await answer.get_by_role("button", name=re.compile(r"Mark answer as best or verified", re.I)).first.click()
item = page.locator("[role^=menuitem]").filter(has_text="Best answer").first      # or "Verified answer"
await item.wait_for(state="visible")
await item.click()
```

`get_by_text("Best answer", exact=True)` fails because the element's text is "Best answer" plus its description. Filter menu items instead.

## Results to look for

- The question card gets a green **Best answer** badge in the header area.
- In the community sidebar *Top questions* shows a "Best answer" pill under that question.
- Answers marked as best are pinned to the top of the thread in the full view.

## Which account should mark it?

- Use an **admin session** for all of it unless you deliberately want each community expert to act (that needs the expert role assigned first - see `viva-engage-community-admin`).
- The asker can mark too, which makes a realistic story ("the asker accepted this answer"); it is optional.
- If the control is missing, check the role in the community's member list before debugging locators.

## Planning

- Mark exactly one best answer per question.
- Leave some questions unanswered and some answered-but-unmarked - that is what real communities look like and lets *unanswered* views demo.
- Mark after all answers exist (answers are created in the comment phase).
