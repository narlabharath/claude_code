# Installing `/init-project`

Two-minute install. One time per machine.

## What you need

- Claude Code (VS Code extension or CLI) — installed and working.
- Python 3 available as `python` on your PATH. Check with `python --version` — it should report `Python 3.x`. If it reports Python 2 or `python` isn't found, install Python 3 first.

## Install

You're copying two files (`init-project.md` and `init-project-changelog.md`) into your Claude Code commands directory. After that, `/init-project` will appear as a slash command in every Claude Code session you start.

### macOS / Linux

```bash
mkdir -p ~/.claude/commands
cp init-project.md           ~/.claude/commands/init-project.md
cp init-project-changelog.md ~/.claude/commands/init-project-changelog.md
```

### Windows (PowerShell)

```powershell
$dst = Join-Path $env:USERPROFILE ".claude\commands"
New-Item -ItemType Directory -Path $dst -Force | Out-Null
Copy-Item .\init-project.md           "$dst\init-project.md"           -Force
Copy-Item .\init-project-changelog.md "$dst\init-project-changelog.md" -Force
```

That's it. The next Claude Code session you start will have `/init-project` available.

## Use it in a project

1. Open the project folder in VS Code (or `cd` there if using the CLI).
2. Start a Claude Code session.
3. Type `/init-project`.
4. When Claude finishes setting up the files, **close the session and start a new one**. Hooks only activate at session start, so the session that ran `/init-project` does not yet have hooks loaded.
5. In the new session, send any prompt. You should see:
   - `.claude/sessions/<sid>/timeline.md` containing a `[session-start]` row.
   - `.claude/.current-session-path` pointing at that session folder.

If those two files appear, the hooks are firing and you're set. Read `README.md` for the daily workflow (`/milestone` and `/deep-review`).

## Updating

When a new version drops, replace the two files in `~/.claude/commands/` with the updated copies. The next time you run `/init-project` in a project that already has it installed, Claude reads the changelog and walks you through the version-specific updates.

## Troubleshooting

See the **Troubleshooting** section in `README.md`. The two most common issues:

- **`/init-project` doesn't appear as a slash command** — make sure the file ended up at exactly `~/.claude/commands/init-project.md` (no trailing extension issues, no nested folder). Restart Claude Code afterwards.
- **Hooks don't seem to be running** — confirm you opened a **new** session after `/init-project` finished, and that `python` (not `python3`) resolves to Python 3 on your PATH.
