# VS Code examples: agent and prompt around the skills

Skills are on-demand knowledge. They cannot restrict tools or start subagents - that is what **custom agents** and
**prompt files** are for. These files show one way to combine them in VS Code with GitHub Copilot.

| File | Copy to | Purpose |
|---|---|---|
| `agents/viva-engage-demo-builder.agent.md` | `.github/agents/` | Agent with a fixed tool set (read, search, edit, execute, agent, todo) that follows the skills and may use the verifier as a subagent |
| `agents/viva-engage-verifier.agent.md` | `.github/agents/` | Subagent only (`user-invocable: false`), read-only plus execute for checks |
| `prompts/build-demo.prompt.md` | `.github/prompts/` | Slash command `/build-demo` that runs the agent through the next open phase |

Notes:

- They live under `examples/` on purpose so that they are not active in this repository. Copy them into your own
  project and adapt the names, tools, and phases.
- Tool names follow the VS Code documentation (`read`, `search`, `edit`, `execute`, `agent`, `todo`). Listing `agents`
  requires the `agent` tool in `tools`.
- The skills themselves stay tool-free and portable between Claude Code and GitHub Copilot.
- These examples have not been exercised in every Copilot surface (VS Code, CLI, cloud agent). Treat them as a starting point.
