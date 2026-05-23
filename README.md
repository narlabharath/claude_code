# Claude Code Walkthrough

A 21-section walkthrough of Claude Code as a structured development partner — not a feature tour.

## What this is

Covers the full learning progression from *"why this exists"* to *"working at scale across multi-session projects."* The focus is on discipline: how to inspect, plan, edit, verify, and review; how to make that discipline stable across a project with `CLAUDE.md`, settings, hooks, MCP, skills, subagents, and the session-management patterns that hold long-running work together.

21 sections, 7 parts. Content-complete as of 2026-05-23.

## How to read it

Clone the repo, then open `delivery/walkthrough.html` in any browser. Works on `file://`. No build step. No dependencies. Side-rail nav lets you jump to any section.

```
git clone https://github.com/narlabharath/claude_code.git
cd claude_code
# open delivery/walkthrough.html in your browser
```

## Repository layout

| Path | What it is |
|---|---|
| `delivery/walkthrough.html` | The walkthrough — single HTML file, 21 sections, 7 Parts |
| `delivery/init-project/` | Installable session-management system (hooks + slash commands) |
| `delivery/hands-on/` | Per-section activity prompts and reference artifacts |
| `delivery/assets/` | Images and template |
| `delivery/reference/` | Design system and section anatomy specs |

## The session-management system

`delivery/init-project/` is a standalone installable package — hooks and slash commands that implement the working style taught in the walkthrough. See [`delivery/init-project/README.md`](delivery/init-project/README.md) for what it installs and [`delivery/init-project/INSTALL.md`](delivery/init-project/INSTALL.md) for setup steps.

## License

MIT — see [LICENSE](LICENSE).

Anthropic screenshots embedded in the walkthrough are from [docs.anthropic.com](https://docs.anthropic.com) and [code.claude.com/docs](https://code.claude.com/docs); attribution captions are included inline.
