---
name: build-demo
description: Build or continue the Viva Engage demo from the spreadsheets, phase by phase, with verification.
agent: 'Viva Engage Demo Builder'
argument-hint: 'optional: a phase name or "all" (default: continue with the next open phase)'
---
Continue building the Viva Engage demo.

1. Check prerequisites: spreadsheets validate, recorded sessions exist for the admin and the acting users, the
   communities exist.
2. Determine the next open phase from the status columns (or use the phase given as argument).
3. Do a dry run, then one item, then the whole phase, in the background with a log file.
4. Ask the subagent to verify the phase; fix findings; then report the status table and what comes next.
