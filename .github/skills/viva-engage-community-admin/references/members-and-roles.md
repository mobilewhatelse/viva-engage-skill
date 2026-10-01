# Members and roles

## Open the member management page

From the community landing page, in the right column under **People**:

- **Assign experts** - shown while the community has no experts.
- **Add user** (the person-plus icon next to the avatar row) - shown once experts exist.
- **View all** / **View all members** - opens the list as well.

Match all of them:

```python
btn = page.get_by_role("button", name=re.compile(r"Assign experts|^Add user$"))
await btn.first.wait_for(state="visible", timeout=20000)      # retry once or twice after a reload
await btn.first.click()
await page.get_by_placeholder(re.compile(r"Invite or search")).wait_for(state="visible")
```

The page has two tabs, **Settings** and **Members**. The Members tab lists *Name, Title, Role* with a role dropdown and a remove icon per row.

## Add a member

```python
row = page.locator("[role=row], tr").filter(has_text=display_name).first
if await row.count() == 0:
    box = page.get_by_placeholder(re.compile(r"Invite or search"))
    await box.fill(display_name)
    await page.wait_for_timeout(2500)                          # suggestions: "Suggested members and guests for this community"
    hit = page.locator("[role=row], tr").filter(has_text=display_name).first
    await hit.wait_for(state="visible")
    await hit.get_by_role("button").last.click()               # the plus icon at the end of the row
    await box.fill("")                                         # back to the member list
```

- Search by the full display name; the suggestion row shows name, title, and the role the person will get (*Member*).
- Members can also **join themselves** (the *Join* button) - only people without a recorded session need adding by an admin.
- A CSV import exists on the same page for very large lists.

## Set a role

Each row has a role button whose text is the current role (*Member*, *Admin and Member*, ...). Clicking it opens a menu titled *Additional roles*:

| Menu item | Meaning |
|---|---|
| **Admin** | Governance over the community (announcements, pinning, member management, topics) |
| **Community expert** | Subject-matter expert (can mark best/verified answers; shown in the *Community expert* section) |

```python
row = page.locator("[role=row], tr").filter(has_text=display_name).first
role_btn = row.get_by_role("button", name=re.compile(r"Member|Admin|expert", re.I)).first
current = (await role_btn.inner_text()).lower()             # read ONLY this button, never the whole row
if "admin" not in current:
    await role_btn.click()
    item = page.locator("[role^=menuitem]").filter(has_text="Admin").first
    await item.wait_for(state="visible", timeout=6000)      # retry the click once if the menu does not show
    await item.click()
```

Rules learned the hard way:

- **Never decide "already admin" from the row text.** Job titles ("IT Admin") and names ("... Administrator") contain "admin". Use the role button's text.
- A user who needs **two roles** gets them one after the other; re-locate the row after each change (the DOM re-renders) and retry the menu click once if it does not open.
- Roles listed in a spreadsheet as `Owner` have no menu entry; the creator is already owner/admin.
- After assigning experts, the entry-point label changes (see above), and a **Community expert (N)** block appears in the right column.

## Verifying

- Member count in the right column ("Community members (N)").
- Admin shield badge on avatars / `<name> - Admin` in the avatar tooltip.
- *Community expert (N)* block present.
- The admin-only *Admin actions* section is visible when signed in as that user.
