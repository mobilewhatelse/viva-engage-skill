# Images, attachments, topics

## Attach an image to a post

The composer toolbar has **Add images or videos**. It opens a native file chooser; use Playwright's chooser API:

```python
async with page.expect_file_chooser() as chooser:
    await page.get_by_role("button", name=re.compile(r"Add images or videos", re.I)).last.click()
file_chooser = await chooser.value
await file_chooser.set_files(path_to_image)
await page.wait_for_timeout(5000)          # give the upload and thumbnail time before clicking Post
```

Attach the image **after** typing the text and **before** clicking Post. The post card then shows the image below the text and a lightbox on click.

Large images make the page taller; later steps that scroll or hover may need `scroll_into_view_if_needed()`.

## Generate demo images without any image library

Render small HTML pages with Playwright and screenshot them. 1200x630 works well for feeds. Useful demo visuals: a ring-style technology radar (SVG), a colored status table (heatmap), a left-to-right process diagram with boxes and arrows.

```python
await page.set_content(html)            # self-contained HTML with inline CSS/SVG
await page.screenshot(path="assets/diagram.png")      # viewport 1200 x 630
```

SVG gotcha: write attributes quoted and elements closed explicitly (`<circle r="50"></circle>`). Unquoted attributes such as `r=50/` swallow the slash, the shape silently does not render, and you only notice in the screenshot.

Keep generated images generic - no logos, names, or real figures.

## Topics

Topics are tags with a name and a description, managed by admins. They are added to an **existing post** from the post menu.

Entry points:

- Thread page, post menu (`View more message options`): **Add topics** - or **Edit topics** when the post already has some.
- Typing `#word` into the post body is *not* the mechanism used here.

Dialog behaviour (current builds):

1. A search box (`Add topics to your post to increase its visibility`) filters topics as you type.
2. A matching topic shows up as a **result card** (not necessarily `role=option`). Click the text hit.
3. If nothing matches, *create a new topic* appears; it opens **Create new topic** with *Topic name* and a **required Description**, then **Create topic**.
4. If the topic exists but your search did not list it, the dialog says *"The topic X already exists"* - cancel and click the result instead.
5. The search text **stays** in the box after you pick a topic; clear it (`Control+A`, `Backspace`) before typing the next one, otherwise names concatenate.

```python
topics = [t for t in topics if not await page.get_by_text(t, exact=True).count()]   # already on the post?
if not topics:
    return "already present"
await page.get_by_role("button", name="View more message options").first.click()
await page.get_by_role("menuitem", name=re.compile(r"Add topics|Edit topics")).first.click()
box = page.locator("input[aria-label*='Add topics'], input[placeholder*='Add topics']")
for topic in topics:
    await box.first.focus()                         # click can be intercepted after the first topic
    await page.keyboard.press("Control+A"); await page.keyboard.press("Backspace")
    await page.keyboard.type(topic, delay=60)
    await page.wait_for_timeout(2500)
    hit = page.get_by_text(re.compile(rf"^\s*#?\s*{re.escape(topic)}\s*$", re.I))
    if await hit.count():
        await hit.last.click()
    else:
        await page.get_by_text("create a new topic").first.click()
        await page.get_by_placeholder("Enter topic name").fill(topic)
        await page.get_by_placeholder("Describe this topic").fill(f"Community topic {topic}")
        await page.get_by_role("button", name="Create topic").click()
    await page.wait_for_timeout(2000)
```

- Topic names without spaces (CamelCase) behave best.
- Topic chips then render below the post text; they are also shown in the feed card.
- Only admins can create topics; run this step with an admin session.
- Topics on posts are visible in search and group content by theme - add 1-2 per post.
