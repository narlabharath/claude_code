# init-project — Automatic Documentation System for Claude Code

Keep a persistent record of everything that happens across Claude Code sessions — file changes, design decisions, experiments, and conversations — automatically.

**Version:** 2.0.2 | **Requires:** Claude Code VS Code extension + Python 3

---

## Table of Contents

| Section | What you'll learn |
| --- | --- |
| [The Problem](#the-problem) | Why this system exists |
| [How It Solves It](#how-it-solves-it) | What the system does at a high level |
| [Setup](#setup) | How to install (5 minutes, one-time) |
| [What Gets Created](#what-gets-created) | Every file, command, and hook that gets added to your project |
| [Daily Workflow](#daily-workflow) | What your day-to-day looks like after setup |
| [How It Works Under the Hood](#how-it-works-under-the-hood) | Data flow, two-layer architecture, per-session isolation |
| [Updating to a New Version](#updating-to-a-new-version) | How to apply future updates |
| [Limitations](#limitations) | What doesn't work or needs workarounds |
| [Troubleshooting](#troubleshooting) | Common issues and fixes |
| [What's in This Package](#whats-in-this-package) | The files you received and which ones are for you |
| [Changelog](#changelog) | Version history |

---

## The Problem

Claude Code has a limited context window. During long sessions, older parts of the conversation get "compacted" — Claude forgets them. When you close a session, everything starts fresh with no memory of what happened.

This means:

- **Decisions** you made (and why) are forgotten
- **Experiments** you ran (and their results) disappear
- **Discussions** about architecture or approach are lost
- **File changes** have no record of *why* they were made

You end up re-explaining context, re-debating decisions, and losing institutional knowledge every session.

```text
WITHOUT init-project                    WITH init-project

Session 1                               Session 1
┌─────────────────────┐                 ┌─────────────────────┐
│ Made design decision│                 │ Made design decision│
│ Ran 3 experiments   │                 │ Ran 3 experiments   │
│ Debugged auth flow  │                 │ Debugged auth flow  │
└──────────┬──────────┘                 └──────────┬──────────┘
           │                                       │ hooks auto-save
           ▼                                       ▼
      ┌─────────┐                       ┌────────────────────────┐
      │ LOST  ✗ │                       │ .claude/sessions/<sid>/│
      └─────────┘                       │ (this session's notes) │
                                        └──────────┬─────────────┘
                                                   │ you run /deep-review
                                                   ▼
                                        ┌──────────────────────┐
                                        │ docs/project-log/    │
                                        │ (shared, permanent)  │
                                        └──────────┬───────────┘
                                                   │
Session 2                               Session 2  │
┌─────────────────────┐                 ┌──────────┴──────────┐
│ "Why did we choose  │                 │ Claude reads        │
│  this approach?"    │                 │ project-log/ at     │
│ "What did we try?"  │                 │ session start       │
└─────────────────────┘                 └─────────────────────┘
```

Two storage tiers matter here: hooks write **per-session** notes automatically as Session 1 unfolds, and `/deep-review` is the explicit step that promotes that into the shared **project log** Session 2 will read. Skipping `/deep-review` means Session 1's notes stay private to that session — still recoverable, just not in the shared log yet.


---

## How It Solves It

This system installs a set of **hooks** (background Python scripts) and **slash commands** into your project. Once installed:

1. **Hooks automatically capture** file operations, conversation topics, and session transitions as they happen — no action needed from you
2. **Periodic reminders** nudge you to run cleanup commands at natural intervals (every ~15 messages)
3. **Two slash commands** (`/milestone` and `/deep-review`) let you enrich the auto-captured data with meaningful summaries, decisions, and experiment results
4. **CLAUDE.md gets updated** with milestones and working policies so Claude has context in future sessions

The result: a `docs/project-log/` folder in your project with a living history that Claude reads at the start of every session. Underneath it sits a per-session staging area that fills up automatically as you work — `/deep-review` is what merges that staging area into the shared log.

```text
                       PER-SESSION (auto)           SHARED (manual promotion)
                       ───────────────────          ──────────────────────────
┌──────────────────┐   ┌──────────────────────┐
│ You + Claude     │──▶│ Hooks                │
│ work on          │   │ check-milestone.py   │
│ your project     │   │ session-end-save.py  │
└──────────────────┘   │ precompact-save.py   │
                       │                      │
                       │ write to             │
                       │ .claude/sessions/    │
                       │   <sid>/             │
                       │ ├─ timeline.md       │
                       │ ├─ discussions.md    │
                       │ ├─ state.json        │
                       │ ├─ code-changes.md ◀ written by precompact only
                       │ └─ transcript.jsonl    (per-session, never shared)
                       └──────────┬───────────┘
                                  │
┌──────────────────┐              │ /milestone        ┌────────────────────┐
│ You run          │──▶ enriches per-session docs ───▶│ CLAUDE.md updated  │
│ /milestone       │   (cleans [auto] entries,        │ (Recent Milestones)│
└──────────────────┘   writes summaries)              └────────────────────┘

┌──────────────────┐              │ /deep-review      ┌────────────────────┐
│ You run          │──▶ merges all sessions ─────────▶│ docs/project-log/  │
│ /deep-review     │   into shared docs               │ ├─ timeline.md     │
└──────────────────┘   (the ONLY path                 │ ├─ decisions.md    │
                       to the shared log)             │ ├─ experiments.md  │
                                                      │ └─ discussions.md  │
                                                      │                    │
                                                      │ ← Claude reads     │
                                                      │   these next       │
                                                      │   session          │
                                                      └────────────────────┘
```

Two things to notice:

- **Hooks never write to `docs/project-log/` directly.** They only write to the per-session folder. This is why two parallel sessions can't corrupt each other.
- **`code-changes.md` and `transcript.jsonl` are per-session only** — they're the PreCompact safety net, captured at the moment context is about to be lost. They don't get merged into the shared log because they're already noisy by design; the shared log gets the cleaner, reviewed prose.

---

## Setup

> **Prerequisites:** Claude Code VS Code extension (installed and working) + Python 3 (hooks are Python scripts).

### Method A: Slash command (recommended)

**One-time install (per machine):**

```bash
# Mac/Linux
cp init-project.md ~/.claude/commands/init-project.md
```

```powershell
# Windows (PowerShell)
Copy-Item init-project.md "$env:USERPROFILE\.claude\commands\init-project.md"
```

You also need the changelog file for future updates:

```bash
# Mac/Linux
cp init-project-changelog.md ~/.claude/commands/init-project-changelog.md
```

```powershell
# Windows (PowerShell)
Copy-Item init-project-changelog.md "$env:USERPROFILE\.claude\commands\init-project-changelog.md"
```

**Per project:**

1. Open your project folder in VS Code
2. Start a Claude Code session
3. Type `/init-project`
4. Claude will create all files, hooks, and commands
5. **Start a new session** — hooks only take effect in new sessions

### Method B: Paste as message

If slash commands aren't working (see [Troubleshooting](#troubleshooting)), copy the entire content of `init-project.md` and paste it as a regular message to Claude.

---

## What Gets Created

After running `/init-project`, your project will have:

```text
your-project/
├── CLAUDE.md                       ← updated with working policies + milestones
├── docs/
│   └── project-log/                ← shared, merged by /deep-review only
│       ├── timeline.md
│       ├── decisions.md
│       ├── experiments.md
│       └── discussions.md
├── .claude/
│   ├── commands/
│   │   ├── milestone.md            ← slash commands
│   │   └── deep-review.md
│   ├── hooks/
│   │   ├── check-milestone.py      ← automation scripts
│   │   ├── precompact-save.py
│   │   ├── session-end-save.py
│   │   └── session_utils.py
│   ├── sessions/
│   │   └── {session-id}/           ← per-session private data
│   │       ├── timeline.md
│   │       ├── discussions.md
│   │       ├── state.json
│   │       ├── code-changes.md     ← written by precompact only
│   │       └── transcript.jsonl    ← raw backup, written by precompact only
│   ├── settings.local.json         ← hook registration
│   ├── .init-version               ← installed version (2.0.2)
│   └── .current-session-path       ← breadcrumb to active session
```

### Documentation files (`docs/project-log/` — shared, populated by `/deep-review`)

| File | What it stores |
| --- | --- |
| `timeline.md` | Central log — file ops, discussion topics, session markers, milestones (organized into `## Session <sid>` sections after merge) |
| `decisions.md` | Design decisions with context, alternatives, and rationale (cross-session, no session sections) |
| `experiments.md` | What was tested, how, results, and verdict (cross-session) |
| `discussions.md` | Conversation threads and Q&A pairs (organized into `## Session <sid>` sections after merge) |

Per-session files live separately under `.claude/sessions/<sid>/`:

| File | Written by | What it stores |
| --- | --- | --- |
| `timeline.md` | `check-milestone.py` (every prompt) + `precompact-save.py` | `[session-start]`, `[auto]` file ops, `[auto] Discussion:`, `[reminder]`, `[compaction-save]` |
| `discussions.md` | `precompact-save.py` + `/milestone` | Conversation summaries grouped by topic |
| `state.json` | `check-milestone.py` + `session-end-save.py` | Counters, watermark, last-active timestamp, discussion cache, merge status |
| `code-changes.md` | `precompact-save.py` only | File snapshots captured before context compaction |
| `transcript.jsonl` | `precompact-save.py` only | Raw transcript backup |

### Slash commands (`.claude/commands/`)

| Command | When to use it | What it does |
| --- | --- | --- |
| `/milestone` | Every ~15 messages, or after finishing a piece of work | Logs what was accomplished, cleans up auto-entries, updates CLAUDE.md |
| `/deep-review` | End of a long session, or periodically | Full documentation audit — merges session data, populates decisions/experiments/discussions |

### Hooks (`.claude/hooks/`) — the automation layer

| Hook | Runs on | What it does |
| --- | --- | --- |
| `check-milestone.py` | Every message you send | Logs file ops + conversation topics, detects new sessions, sends reminders |
| `precompact-save.py` | Before context compaction | Emergency save: timeline + discussions + code snapshots + transcript backup |
| `session-end-save.py` | After every Claude response | Writes timestamp + caches discussion data |

### Project configuration

- **`CLAUDE.md`** — Updated with working policies, recent milestones table, key paths, and session start instructions so Claude knows how to use the documentation system
- **`.claude/settings.local.json`** — Registers the hooks with Claude Code
- **`.claude/.init-version`** — Tracks which version is installed (used for updates)

### Per-session storage

Each Claude session gets its own folder (`.claude/sessions/{session-id}/`) containing a private `timeline.md`, `discussions.md`, and `state.json`. This prevents multiple sessions from stepping on each other's data. Only `/deep-review` merges per-session data into the shared `docs/project-log/`.

---

## Daily Workflow

Once set up, your workflow looks like this:

```text
        ┌─────────────────────────────────────┐
        │           START SESSION             │
        │ Claude reads CLAUDE.md +            │
        │ docs/project-log/ for context       │
        └────────────────┬────────────────────┘
                         │
                         ▼
        ┌─────────────────────────────────────┐
        │           WORK NORMALLY             │
        │ Hooks auto-capture in               │◀─┐
        │ background (no action needed)       │  │
        └────────────────┬────────────────────┘  │
                         │                       │
                         ▼                       │
        ┌─────────────────────────────────────┐  │
        │ ~15 messages? or done                │  │
        │ with a piece of work?               │  │
        └────┬─────────────────────────┬──────┘  │
             │ yes                     │ no      │
             ▼                         └─────────┘
        ┌─────────────────────────────────────┐
        │           RUN /milestone            │
        │ Clean up auto entries,              │
        │ write milestones, update            │
        │ CLAUDE.md                           │
        └────────────────┬────────────────────┘
                         │
                         ▼
        ┌─────────────────────────────────────┐
        │ ~30 messages? or end                 │
        │ of session?                         │
        └────┬─────────────────────────┬──────┘
             │ yes                     │ no
             ▼                         └─────────┐
        ┌─────────────────────────────────────┐  │
        │          RUN /deep-review           │  │
        │ Merge sessions,                     │  │
        │ populate all docs                   │  │
        └─────────────────────────────────────┘  │
                                                 ▼
                                          (back to work)
```

### Just work normally

Hooks run in the background on every message. You don't need to do anything special. File operations and conversation topics are captured automatically into your session's timeline.

### Run `/milestone` when reminded (or when you finish something)

At ~15 messages, you'll see a `[reminder]` entry in your session timeline suggesting you run `/milestone`. When you do:

- Claude reviews the auto-captured entries and writes meaningful milestone summaries
- Crude `[auto]` entries get cleaned up or replaced
- Your `CLAUDE.md` gets updated with what was accomplished
- Counters reset so you won't be reminded again until the next 15 messages

You can also run `/milestone` any time you finish a logical piece of work — you don't have to wait for a reminder.

### Run `/deep-review` for a full documentation pass

At ~30 messages, or at the end of a long session, run `/deep-review`. This is the comprehensive pass that:

- Merges all unmerged session data into the shared `docs/project-log/`
- Populates `decisions.md` with design decisions Claude observed during the session
- Populates `experiments.md` with any experiments and their results
- Enriches `discussions.md` with conversation threads and conclusions
- Updates the deep review status in `CLAUDE.md`

### Start a new session

When you open the project in a new session, Claude reads `CLAUDE.md` and sees:

- What was accomplished in previous sessions (milestones)
- Working policies for how to use the documentation system
- Where to find detailed history (`docs/project-log/`)

The hooks detect the new session automatically and create a fresh session folder.

---

## How It Works Under the Hood

### Data flow

```text
YOU + CLAUDE              HOOKS (automatic)            DOCS

Send a message ─────────▶ check-milestone.py
                          │
                          ├─ file edit?       ───▶ .claude/sessions/{id}/
                          │                        timeline.md [auto]
                          │
                          ├─ 3+ chat msgs?    ───▶ .claude/sessions/{id}/
                          │                        timeline.md [discussion]
                          │
                          ├─ new session?     ───▶ [session-start] marker
                          │
                          └─ 15 msgs?         ───▶ [reminder] → /milestone

Claude responds ────────▶ session-end-save.py
                          │
                          └─ timestamp        ───▶ state.json (last-active)

Context compaction ─────▶ precompact-save.py
                          │
                          └─ FULL SAVE        ───▶ timeline + discussions +
                                                   code snapshots + backup

You run /milestone ─────▶ Claude enriches    ───▶ session timeline cleaned
                                                   CLAUDE.md updated

You run /deep-review ───▶ Claude merges      ───▶ docs/project-log/*
                          all sessions             (shared, permanent)
```

### The two-layer design

```text
┌───────────────────────────────┐      ┌────────────────────────────────┐
│ LAYER 1: AUTO (hooks)         │      │ LAYER 2: MANUAL (commands)     │
│                               │      │                                │
│ Raw, fast, lossy              │      │ Reviewed, meaningful           │
│                               │      │                                │
│ • File paths + brief          │      │ • Milestone summaries          │
│   context                     │/milestone│ • Clean timeline           │
│ • Timestamps                  │─────▶│ • Updated CLAUDE.md            │
│ • Session markers             │      │                                │
│ • Discussion topics           │/deep-review│ • Design decisions       │
│                               │─────▶│ • Experiment results           │
│ Safety net — captures         │      │ • Discussion threads           │
│ everything, quality TBD       │      │ • Merged project history       │
└───────────────────────────────┘      └────────────────────────────────┘
```

### Per-session isolation

```text
Session A (you)               Session B (teammate)

.claude/sessions/             .claude/sessions/
/abc123/                      /def456/
├── timeline.md               ├── timeline.md
├── discussions.md            ├── discussions.md
└── state.json                └── state.json
       │                              │
       └──────────┬───────────────────┘
                  │
                  ▼  /deep-review
        ┌──────────────────────────┐
        │ docs/project-log/        │
        │ (shared, merged)         │
        │ ├── timeline.md          │
        │ ├── decisions.md         │
        │ ├── experiments.md       │
        │ └── discussions.md       │
        └──────────────────────────┘
```

Each session writes to its own folder. A breadcrumb file (`.claude/.current-session-path`) tells Claude which folder belongs to the current session. Multiple sessions can't corrupt each other's data, and `/deep-review` is the only path from per-session data into the shared docs.

---

## Updating to a New Version

When a new version of init-project is released:

1. Copy the updated `init-project.md` and `init-project-changelog.md` to `~/.claude/commands/`
2. Run `/init-project` in your project — it detects the existing installation and reads the changelog to know exactly what changed
3. Claude presents the changes for your approval, then applies them

Your documentation data (`docs/project-log/`, session folders) is **never overwritten** during updates.

---

## Limitations

1. **Reminders don't reach Claude directly.** The hook's `systemMessage` output is silently discarded by the VS Code extension (platform limitation). Reminders are written to `timeline.md` — Claude sees them when it next reads the file, but not as an inline prompt.
2. **Auto-captured entries vary in quality.** The hook grabs Claude's most recent text before each file write as context. This is approximate. Run `/milestone` to replace crude entries with meaningful ones.
3. **Only the first operation on a file is logged per session.** Intentional — prevents log spam when a file is edited many times.
4. **`decisions.md` and `experiments.md` are only populated by `/deep-review`.** These require Claude's judgment and can't be auto-captured meaningfully.

---

## Troubleshooting

### Slash commands crash with "process exited with code 1" (Windows)

**Cause:** A bug in certain builds of Claude Code 2.1.69 — the config lock mechanism fails with `EEXIST` on Windows.

**Fix:** Roll back to a previous Claude Code extension build. Set `"extensions.autoUpdate": false` in VS Code settings to prevent re-upgrading.

**Workaround:** Use Method B — paste `init-project.md` content as a regular message.

### Hooks don't seem to be running

- Make sure you started a new session after running `/init-project`. Hooks registered in `settings.local.json` only load when a session starts.
- Check that `.claude/settings.local.json` exists and contains hook entries.
- Verify Python 3 is available in your terminal — run `python --version` and confirm it reports `Python 3.x`. Hooks invoke `python` (not `python3`) because that's the standard name on Windows and on modern Mac/Linux setups with venvs.

### No auto entries appearing in timeline

- Send a few messages that involve file edits — the hook only logs file operations (creates/edits), not pure conversation.
- Check `.claude/sessions/` — there should be a folder for your current session with a `timeline.md` inside.

---

## What's in This Package

| File | For you? | Purpose |
| --- | --- | --- |
| `README.md` | Yes — you're reading it | This file. |
| `init-project.md` | No — it's instructions for Claude | The setup template. Install as a slash command or paste as a message. |
| `init-project-changelog.md` | No — read by the system | Version changelog used during updates so Claude knows what changed. |

---

## Changelog

### v2.0.2 (2026-03-09)

- Patch update mechanism: `/init-project` now reads a changelog file during updates to apply changes precisely
- Fixed live slash commands being out of sync with the package

### v2.0.1 (2026-03-08)

- `/deep-review` enriches empty discussions from cached data before merging
- `/milestone` discussion update now mandatory with explicit data sources

### v2.0 (2026-03-06)

- Major redesign: per-session doc architecture — each session gets its own folder
- Breadcrumb system for session isolation
- Only `/deep-review` merges per-session → shared docs
- Upgrade path from v1.x with automatic data migration

▸ Older versions
