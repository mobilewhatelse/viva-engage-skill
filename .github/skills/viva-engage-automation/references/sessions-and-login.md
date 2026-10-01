# Sessions and sign-in

## One recorded session per user

Playwright can save and restore everything a browser needs to be signed in:

```python
# record once (headed, human completes MFA)
context = await browser.new_context()
page = await context.new_page()
await page.goto(BASE_URL)
...  # sign in, wait until the home feed is visible
await context.storage_state(path=f".auth/{safe_name}.json")

# reuse (headless is fine)
context = await browser.new_context(
    storage_state=f".auth/{safe_name}.json",
    viewport={"width": 1440, "height": 1000},
    locale="en-US",            # makes visible labels deterministic
)
```

Derive the file name from the account identifier by lowercasing and replacing every character outside `[a-z0-9_.-]` with `_`. Keep `.auth/` out of version control: those files are bearer credentials.

## Detect an expired or missing session

After `page.goto(BASE_URL)` the app redirects to the identity provider when the session is invalid. Wait for either target:

```python
await page.wait_for_url(re.compile(r"/main|login\."), timeout=30000)
signed_in = "/main" in page.url
```

## Automatic sign-in with a shared demo password

For demo accounts that share one password, sign in automatically and save the session. Read the password from an ignored `.env` (`ENGAGE_PASSWORD`), never from code:

```python
await page.locator('input[name="loginfmt"]').wait_for(state="visible", timeout=15000)   # NOT is_visible(timeout=...)
await page.locator('input[name="loginfmt"]').fill(account)
await page.locator("#idSIButton9").click()                                                # "Next"
await page.locator('input[name="passwd"]').wait_for(state="visible", timeout=20000)
await page.locator('input[name="passwd"]').fill(password)
await page.locator("#idSIButton9").click()                                                # "Sign in"
# "Stay signed in?" appears for some accounts; click "Yes" if it shows up, then poll until the app URL is reached
```

Poll in a loop (until a deadline) instead of fixed sleeps: reached the app -> done; password error element visible -> fail with a clear message; "Stay signed in" visible -> click `#idSIButton9`.

Gotcha: `locator.is_visible(timeout=...)` **does not wait** - the `timeout` argument is ignored and it answers immediately. Use `wait_for(state="visible")` inside `try/except` when you need to wait.

## The "Let's keep your account secure" screen

If, after the correct password, the identity provider shows *"Let's keep your account secure - We'll help you set up another way to verify it's you"* with only **Next**, the account is forced into multi-factor **registration**. Automation cannot and should not complete that. The password was accepted; the environment is demanding MFA setup for this account.

Things to check in the environment's administration settings (in this order of likelihood). Each is an administration decision - make it deliberately, and only in a demo environment:

1. **Authentication methods -> Registration campaign**: if enabled for all users it nudges (and sometimes forces) registration. Setting it to disabled helps for the "nudge" case but did not remove a *mandatory* prompt in the observed environment.
2. **Microsoft Entra ID Protection -> MFA registration policy** (needs the premium licence tier): when enabled for all users it makes registration mandatory.
3. **Per-user MFA** (legacy): users set to *Enabled/Enforced* must register.
4. **Security defaults vs. Conditional Access**: security defaults cannot be toggled while any Conditional Access policy exists. Pre-built policies that target only external partner/vendor accounts are *not* the cause for normal member accounts - leave them alone.
5. **Sign-in logs of the affected user** (Interactive and Non-interactive tabs) show which policy demanded MFA; logs can lag by several minutes.
6. **Temporary Access Pass**: if enabled as an authentication method, an administrator can generate a one-time or multi-use code per user; signing in with it satisfies strong authentication and avoids per-user phone setup.

If none of that is acceptable, use **stand-in users** (see `viva-engage-engagement`): do the work with accounts that already have a recorded session.

## Headless vs. headed

- Headless for bulk runs.
- `--headed` for the first recording of a session, when MFA needs a human, and when debugging a locator.
- Set a longer sign-in deadline in headed mode so a human has time (several minutes).

## Locale

Create contexts with `locale="en-US"`. Visible labels ("Write a comment", "Post", "Like") are then predictable. If you must support another UI language, keep every label in a config list and match any of them with a regular expression.

## Security hygiene

- Do not print the password, not even its length, in logs that get shared.
- Do not pass credentials on a command line; environment variables from `.env` only.
- Treat `.auth/*.json` like passwords.
