# Changelog

## 0.1.0

- Initial release with four skills:
  - `viva-engage-automation` - approach, recorded sessions and automatic sign-in, forced multi-factor registration, locator and reliability rules, idempotency and state, seeding playbook, troubleshooting.
  - `viva-engage-content` - discussions, questions, announcements (megaphone switch), polls, praise, comments, replies, @mentions, image upload, topics.
  - `viva-engage-engagement` - reactions, poll votes, best/verified answers, stand-in user planning.
  - `viva-engage-community-admin` - members and roles, pinning, links, community info, favorites, events.
- Added `.claude-plugin/marketplace.json` for installation via `/plugin marketplace add`.
- Added `tools/check_clean.py`, a guard against URLs, e-mail addresses, domains, identifiers, credentials, and environment-specific wording.
