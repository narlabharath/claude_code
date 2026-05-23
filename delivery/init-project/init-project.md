<!-- transcription:illegible: pre-Step-0 intro/frontmatter not captured in photos — first visible line on page 1 is "Initialize or upgrade the project logging system." -->

<!-- page 1 — 20260523_090101.jpg -->

Initialize or upgrade the project logging system.

## Step 0: Detect fresh install vs upgrade

Check if `.claude/.init-version` exists.

If it does NOT exist → this is a FRESH INSTALL. Proceed with all steps below normally.

If it DOES exist → this is an UPGRADE or UPDATE. Read the version number (`<old_version>`).

If version starts with `2.` (e.g., `2.0`, `2.0.1`) → this is a PATCH UPDATE (applying fixes to v2.x). Follow this exact sequence:

1. Read the changelog. The changelog ships alongside this command file. Read it from the user's Claude Code commands directory:
   - On macOS / Linux: `~/.claude/commands/init-project-changelog.md`
   - On Windows: `%USERPROFILE%\.claude\commands\init-project-changelog.md` (PowerShell: `$env:USERPROFILE\.claude\commands\init-project-changelog.md`)

   If the changelog file does not exist there, tell the user: "Cannot find init-project-changelog.md in ~/.claude/commands/. Re-run the one-time install step from the README (copy both init-project.md and init-project-changelog.md into ~/.claude/commands/) and try /init-project again." Then STOP.

   Find the entry that upgrades FROM `<old_version>`. If `<old_version>` is `2.0`, find the `2.0.1` entry first, then chain through `2.0.2`, etc. If already at the latest version listed, tell the user "Already at latest version" and STOP.
2. Present changes to user. Show them the "What changed" summary from each changelog entry that applies. Ask: "Apply these updates? (y/n)" — wait for approval before proceeding.
3. Apply file updates. For EACH file listed in the changelog entry's "Files to update" and "Unchanged files" sections:
   - DELETE the existing file first (do NOT read it, do NOT compare it)
   - WRITE the new version using the content from the corresponding template Step below
   - Do NOT skip any file. Do NOT decide a file is "already current". Every listed file gets deleted and rewritten.
4. PRESERVE everything NOT listed: `docs/project-log/`, `CLAUDE.md`, `.claude/sessions/`
5. Update version. Write the new version number to `.claude/.init-version`
6. Report. Tell the user: "Updated from v`<old_version>` to v`<new_version>`. Changes applied: [summary from changelog]. Docs and session data preserved."

STOP HERE — do not proceed with the full setup steps below.

<!-- page 2 — 20260523_090116.jpg -->

If version is below `2.0` → this is a MAJOR UPGRADE. Follow the v2.0 upgrade sequence:

### v2.0 Upgrade Sequence

1. Rename existing docs for safety: `mv docs/project-log/ docs/project-log-v1/`
   - This preserves all historical data while we set up the v2.0 structure
2. Create fresh v2.0 doc structure: Create new `docs/project-log/` with empty v2.0 doc templates (same files as Step 1 below)
3. Transfer historical content: For each file in `docs/project-log-v1/`:
   - Read the old file content
   - Import it into the corresponding new `docs/project-log/` file under a `## Pre-v2.0 History` section
   - This preserves all historical decisions, experiments, discussions, timeline entries
4. Overwrite hooks with v2.0 code:
   - Write all 4 files from Step 4 below: `session_utils.py`, `check-milestone.py`, `precompact-save.py`, `session-end-save.py`
5. Overwrite commands with v2.0 versions:
   - Write both files from Step 3 below: `milestone.md`, `deep-review.md`
6. Rebuild CLAUDE.md:
   - Read existing CLAUDE.md
   - Extract user-customized sections: Owner, Description, Current Focus, Next Steps, Known Issues, Recent Milestones (preserve their content)
   - Write fresh v2.0 CLAUDE.md template (Step 2 below) with v2.0 session policies (breadcrumb, per-session docs, Deep Review Status)
   - Re-insert the user's customized content into the appropriate sections
   - This gives a clean v2.0 CLAUDE.md without losing user data
7. Update settings.local.json: Write from Step 5 below (includes CWD bug fix with absolute paths)
<!-- page 3 — 20260523_090132.jpg -->
8. Clean up legacy state files: Delete these (hooks no longer read them):
   - `.claude/.last-active`
   - `.claude/.discussion-cache`
   - `.claude/.msg-counter`
   - `.claude/.hook-watermark`
   - `.claude/.session-id`
   - `.claude/.conv-counter`
   - Do NOT delete `.claude/.init-version` — we're about to update it
9. Preserve per-session state: Existing `.claude/sessions/*/state.json` kept — v2.0 hooks add `timeline.md` alongside on first message
10. Update version: Write `2.0` to `.claude/.init-version`
11. Clean up v1 backup: Delete `docs/project-log-v1/` (data has been transferred)
12. Add upgrade entry: Append to `docs/project-log/timeline.md`: `| <today> | [upgrade] Migrated from v<old_version> to v2.0. Per-session docs enabled. Historical data imported. |`
13. Report and stop: Tell the user what was upgraded. Tell them: "Start a new session for v2.0 hooks to take effect."

STOP HERE — do not proceed with the full setup steps below.

For fresh installs only, continue below.

First, run `ls` on the current directory to see what exists. IMPORTANT constraints:

- Do NOT read files outside the current project directory. Do NOT navigate to sibling or parent directories.
- If the directory is empty or near-empty, skip exploration — ask the user for a brief project description instead, or use placeholder text.
- If there are files, do a quick scan (file names and structure only) to understand the project type. Do NOT launch deep exploration agents on empty folders.
- Only read files within THIS directory to populate CLAUDE.md descriptions.

Then set up everything below.

<!-- page 4 — 20260523_090140.jpg -->

## Step 1: Create `docs/project-log/` files (PRESERVE if exists)

Create `docs/project-log/` directory with these 4 files. If a file already exists, do NOT overwrite it.

`docs/project-log/timeline.md`:

```markdown
# Project Timeline

> Append-only log. Each entry is a milestone — decisions, evidence, artifacts, or direction changes.
> `[auto]` entries are written by hooks. Manual entries are written by Claude via `/milestone` or `/deep-review`.

| Date | Summary |
|------|---------|
| <today> | Project logging system initialized. |
```

`docs/project-log/decisions.md`:

```markdown
# Decisions Log

> Key design decisions with rationale. Updated via `/deep-review`.
```

`docs/project-log/experiments.md`:

```markdown
# Experiments & Results

> Objective, setup, results, verdict. Updated via `/deep-review`.
```

<!-- page 5 — 20260523_090149.jpg -->

`docs/project-log/discussions.md`:

```markdown
# Discussions

> Architecture and approach discussions. Updated via `/deep-review`.
```

## Step 2: Create lean `CLAUDE.md` (PRESERVE if exists)

Create `CLAUDE.md` at the project root. If CLAUDE.md already exists, do NOT overwrite it. Populate from what you found in the project:

```markdown
# <Project Name>

- **Owner**: <from git config or ask>
- **Created**: <today>
- **Status**: Active
- **Description**: <1-2 lines based on what you found>

## Current Focus

- <initial setup tasks based on what you found>

## Working Policies

### Session Start (do this FIRST before any other work)
- Read `.claude/.current-session-path` to find your session directory
- Check `{session_dir}/timeline.md` for this session's recent entries
- Check `docs/project-log/timeline.md` for the last cross-session entry date
- If the last shared entry is from a previous day, note the gap

### Mid-Session
<!-- page boundary: CLAUDE.md fenced block continues on page 6 -->

<!-- page 6 — 20260523_090157.jpg -->
- `check-milestone.py` hook auto-saves to your session's `timeline.md` (no action needed)
- After major decisions: run `/milestone` to clean up your session's docs
- Your session docs are at the path in `.claude/.current-session-path`

### Before Compaction (safety net)
- `precompact-save.py` hook auto-saves transcript data to per-session docs (deterministic)
- Check Deep Review Status below — if risk is high, run `/deep-review` first

### General
- Keep this file under 120 lines — detailed content goes in `docs/project-log/`

## Recent Milestones

| Date | Summary |
|------|---------|
| <today> | Project logging system initialized. |

> Full timeline: `docs/project-log/timeline.md`

## Next Steps

1. <based on what you found in the project>

## Known Issues

- Hook `systemMessage` doesn't surface in VSCode extension (confirmed platform limitation)

## Deep Review Status

- **Last run:** never
- **Unmerged sessions:** unknown
- **Risk:** unknown
<!-- page 7 — 20260523_090221.jpg -->
> Updated by `/deep-review`. If risk is high, run `/deep-review` before continuing.

## Key Paths

- `.claude/.current-session-path` — breadcrumb to current session directory
- `.claude/sessions/{sid}/` — per-session docs (timeline, discussions, state)
- `docs/project-log/` — shared docs (merged by `/deep-review` only)
- `.claude/commands/` — slash commands (`/milestone`, `/deep-review`)
- `.claude/hooks/` — `check-milestone.py`, `precompact-save.py`, `session-end-save.py`, `session_utils.py`

## Deep Docs

- Per-session timeline: `{read .claude/.current-session-path}/timeline.md`
- Per-session discussions: `{read .claude/.current-session-path}/discussions.md`
- Shared timeline (merged): `docs/project-log/timeline.md`
- Shared decisions: `docs/project-log/decisions.md`
- Shared experiments: `docs/project-log/experiments.md`
- Shared discussions: `docs/project-log/discussions.md`
```

## Step 3: Create `.claude/commands/` (OVERWRITE — always use latest)

`.claude/commands/milestone.md`:

```markdown
Log milestones and clean up the timeline.

## Steps

0. Read `.claude/.current-session-path` to find your session directory. All work in steps 1-5 operates on **that session's files**, not shared docs.
1. Read `{session_dir}/timeline.md` to see existing entries for this session.
<!-- page 8 — 20260523_090232.jpg -->
2. Review what was accomplished since the last milestone or cleanup.
3. **Add milestones** (see quality rules below).
4. **Clean up [auto] entries** (see cleanup rules below).
5. **MANDATORY — Update `{session_dir}/discussions.md`:**
   a. Read `{session_dir}/state.json` field `discussion_cache` for recent topic names
   b. Scan `{session_dir}/timeline.md` for any `[auto] Discussion:` entries
   c. Review the current conversation context for discussion threads since last milestone
   d. For each discussion thread found: write a summary to `{session_dir}/discussions.md` with context (what sparked it), key points, and conclusion
      a. If NO discussions found from any source, skip — but always check all 3 sources before deciding there are none
6. Do NOT remove manual entries unless clearly wrong. Do NOT change dates.
7. Update "Recent Milestones" in `CLAUDE.md` (last 5 entries).
8. Update "Current Focus" / "Next Steps" in `CLAUDE.md` if needed.
9. Optionally append a 1-line summary to shared `docs/project-log/timeline.md` (e.g., `| <today> | [milestone] Session work summary |`). This keeps shared docs useful between deep-reviews.
10. Reset this session's state only: read `{session_dir}/state.json`, set `msg_count` to 0 and `milestone_fired` to false. Keep all other fields (watermark, conv_count, etc.).
11. Report: milestones added, [auto] entries removed/rewritten, final entry count.

## Quality Rules for Milestones

### Right level of depth
Each milestone entry should answer: **what changed and why it matters**.
- TOO BRIEF: `| 2026-03-03 | Fixed bug. |` — what bug? why does it matter?
- TOO VERBOSE: `| 2026-03-03 | Fixed the path separator mismatch bug in check-milestone.py where Windows backslashes weren't matching forward slashes in deduplication logic, causing duplicate auto entries to appear every time the hook ran. |` — this is a paragraph, not a milestone.
- RIGHT: `| 2026-03-03 | Fixed hook path separator bug (`\` vs `/`) — was causing duplicate [auto] entries on every message. |` — clear what, clear why, one line.

### Topic grouping (don't under-club or over-club)
- **Under-clubbing** (too granular): Don't create separate entries for every single file edit if they're all part of one logical change. "Updated hook" + "Updated settings" + "Updated CLAUDE.md" = one milestone if they're all part of the same effort.
<!-- page 9 — 20260523_090247.jpg -->
- **Over-clubbing** (too merged): Don't lump unrelated changes into one entry. "Fixed bugs and added features and updated docs" — these are 3 separate milestones if they're independent efforts.
- **Rule of thumb**: One entry per *logical unit of work*. A logical unit = one problem solved, one feature added, one decision made, one direction change.

### What IS a milestone
- A decision made (and why)
- A problem identified or solved
- A feature/capability added
- A direction change
- A significant discovery or learning

### What is NOT a milestone
- Individual file edits (unless the file itself IS the milestone)
- Routine updates to CLAUDE.md or timeline.md
- Internal hook/config changes (unless they fix a real problem)
- Repetitive cleanup passes

## Cleanup Rules for [auto] Entries

- If a manual entry covers the same file/topic → **remove** the [auto] entry
- If an [auto] entry references deleted/renamed files → **remove** it
- If an [auto] entry has garbled or irrelevant explanation → **rewrite** with proper description OR **remove** if the manual entries already cover it
- If multiple [auto] entries cover the same logical change → **merge** into one or replace with a manual entry
- Keep [auto] entries that cover files/topics NOT mentioned in any manual entry — they're the only record
```

`.claude/commands/deep-review.md`:

```markdown
Perform a deep review of the project log. This is the comprehensive documentation pass.
<!-- page 10 — 20260523_090258.jpg -->
In v2.0, this command is the ONLY path from per-session docs → shared docs. It merges all unmerged sessions, then enriches shared docs.

## Steps

### Phase 1: Merge per-session docs into shared docs

0. Read `.claude/.current-session-path` to find the current session directory.
1. Scan `.claude/sessions/*/` for ALL session directories. For each, read `state.json` and check `merged` status and `last_active` timestamp. Report: N total sessions, M unmerged.
2. For each session where `merged` is NOT true in state.json:
   a. Read `{session_dir}/timeline.md`, `{session_dir}/discussions.md`, `{session_dir}/code-changes.md` (if they exist)
   b. **Enrich per-session discussions before merge:** IF `{session_dir}/discussions.md` is empty or has only the header, check `{session_dir}/state.json` for `discussion_cache` topics AND scan `{session_dir}/timeline.md` for `[auto] Discussion:` entries. Use these as seeds to write discussion summaries into `{session_dir}/discussions.md` before merging. This ensures no discussion content is lost even if `/milestone` was never run that session.
   c. Create a `## Session {sid} — {date range}` section in `docs/project-log/timeline.md`
   d. Enrich the raw [auto] entries into proper milestones within each section (apply milestone quality rules)
   e. Merge discussion content into a `## Session {sid}` section in `docs/project-log/discussions.md`
   f. Deduplicate entries about the same file operations across sessions
   g. Set `"merged": true` and `"merged_at": "{timestamp}"` in that session's `state.json`
3. For already-merged sessions whose `{session_dir}/timeline.md` was modified AFTER `merged_at`, re-merge those sessions (the session continued after last merge).

### Phase 2: Enrich shared docs (existing logic)

4. Read ALL shared doc files:
   - `docs/project-log/timeline.md` (now contains merged session sections)
   - `docs/project-log/decisions.md`
   - `docs/project-log/experiments.md`
<!-- page 11 — 20260523_090305.jpg -->
   - `docs/project-log/discussions.md` (now contains merged session sections)
   - `docs/project-log/code-changes.md` (if exists)
5. Check recent file changes and project state for context.
6. Update each document following the quality rules below. Decisions and experiments are cross-session (no session sections — these are analytical, not mechanical).
7. Update `CLAUDE.md`:
   - Current Focus, Next Steps, Known Issues, Recent Milestones (last 5)
   - Deep Review Status section: `Last /deep-review: <today>. Unmerged sessions: 0. Risk: low.`
8. Reset ALL sessions' counters: iterate `.claude/sessions/*/state.json`, set `msg_count` to 0 and `milestone_fired` to false. Keep all other fields.
9. Summarize what was added/changed in each file.

## Document-Specific Rules

### timeline.md — What happened
Follow the `/milestone` quality rules. One entry per logical unit of work. Organized with `## Session {sid}` sections — each session's milestones grouped together. Pre-v2.0 entries stay under a `## Pre-v2.0 History` section.

### decisions.md — Why we chose this path

**Each decision entry must have:**
- **Date** and **context** (what problem led to this decision)
- **The decision** itself (what we chose)
- **Alternatives considered** (what else we could have done — at least 2)
- **Rationale** (why this option won over the others)
- **Status** (implemented, proposed, reversed, superseded)

**Topic grouping:**
- One entry per decision point, not per file change
<!-- page 12 — 20260523_090319.jpg -->
- If 5 related micro-decisions are part of one bigger design choice, write ONE entry for the design choice with the micro-decisions as sub-points
- If 2 unrelated decisions happened in the same conversation, write TWO separate entries

**Depth:**
- TOO BRIEF: `Decided to use watermark system.` — no context, no alternatives, no rationale
- TOO VERBOSE: 3 paragraphs explaining every thought process step — this is a log, not an essay
- RIGHT: Context (2-3 sentences) → Decision (1 sentence) → Alternatives (bullet list) → Rationale (2-3 sentences) → Status

### experiments.md — What we tested and what happened

**Each experiment entry must have:**
- **Objective** (what we were trying to learn/verify)
- **Setup** (what we did — numbered steps, specific enough to reproduce)
- **Results** (what actually happened — be specific, include data if available)
- **Verdict** (what we concluded — did it work? what did we learn?)

**Topic grouping:**
- One entry per distinct test/experiment
- If you ran the same test 3 times with tweaks, that's ONE experiment with iterations, not 3 experiments
- If you tested 2 completely different approaches, that's 2 experiments

**Depth:**
- Setup should be specific enough that someone could re-run the experiment
- Results should include actual outputs/behaviors, not just "it worked" or "it failed"
- Verdict should state the lesson learned, not just pass/fail

### discussions.md — The reasoning behind the work

Organized with `## Session {sid}` sections after merge. Each section contains that session's conversation summaries.
<!-- page 13 — 20260523_090327.jpg -->

**Each discussion entry should capture:**
- **Context** (what question or problem sparked the discussion)
- **Key points** (the main arguments, insights, or realizations)
- **Conclusion** (what was decided or what direction was taken)
- **Who said what** (if a user insight drove a direction change, credit it)

**Topic grouping:**
- Group by conversation THREAD, not by individual messages
- A back-and-forth about "should we use blocking hooks?" is ONE discussion entry even if it spans 10 messages
- A conversation that covers hooks AND then switches to a completely different topic = TWO entries

**Depth:**
- Capture the reasoning that would be lost if context compacts
- Don't transcribe the conversation — summarize the thinking
- Highlight insights that changed direction (e.g., "User pointed out X, which led to pivoting from Y to Z")

### code-changes.md — Auto-populated by PreCompact hook
- Per-session code-changes are in `{session_dir}/code-changes.md`
- During merge (Phase 1), these get organized into session sections in shared `docs/project-log/code-changes.md`
- Only check it for reference when writing other entries

## General Quality Rules

1. **Don't waste tokens**: If a topic is already well-documented in one file, don't duplicate it in another. Cross-reference instead: "See Decision D5 for rationale."
2. **Don't skip topics**: Every significant conversation thread and every non-trivial file change should appear in at least one doc file.
3. **Write for future sessions**: A future Claude with no context should understand what happened and why by reading these docs.
4. **Number your entries**: Use sequential IDs (D1, D2... for decisions; E1, E2... for experiments) so they can be cross-referenced.
5. **Don't duplicate existing entries**: Read what's already there before adding. Add only NEW content since the last deep review.
```

## Step 4: Create hooks (OVERWRITE — always use latest)

IMPORTANT: These hooks write to per-session doc files directly. They do NOT rely on `systemMessage` (which doesn't surface in VSCode extension). v2.0 hooks write ONLY to per-session directories — no shared file writes, no file locking needed.

`.claude/hooks/session_utils.py` — Shared utility module (NEW in v2.0):

```python
"""Shared utilities for v2.0 per-session hooks.

Used by: check-milestone.py, session-end-save.py, precompact-save.py
"""
import json, os, re

<!-- page 14 — 20260523_090343.jpg -->
# ----------------------------------------------------------------------
# Constants
# ----------------------------------------------------------------------

SKIP_PATTERNS = (
    '.claude/hooks/', '.claude/commands/', '.claude/settings',
    '.claude/', '.claude/sessions/', 'hook-debug', 'NUDGE.md', 'transcript-',
    'CLAUDE.md', 'docs/project-log/', 'docs/system-status',
    'docs/how-hooks-work', 'docs/hook-reliability',
)

CONVERSATION_THRESHOLD = 3   # Log discussion after this many user messages with no file ops
ENRICHMENT_REMINDER = 15     # Suggest /milestone after this many total messages
DEEP_REVIEW_REMINDER = 30    # Suggest /deep-review after this many total messages

# ----------------------------------------------------------------------
<!-- transcription:illegible: section header between constants block and `def get_session_dir` — likely a "# Sessions" or "# Paths" comment banner. Page 15 starts mid-function. -->
<!-- page 15 — 20260523_090353.jpg -->
def get_session_dir(project_root, session_id):
    """Get or create per-session directory under .claude/sessions/{sid[:8]}/."""
    sid = re.sub(r'[^a-zA-Z0-9_-]', '', session_id[:8]) if session_id else 'unknown'
    sid = sid or 'unknown'
    session_dir = os.path.join(project_root, '.claude', 'sessions', sid)
    os.makedirs(session_dir, exist_ok=True)
    return session_dir


# ----------------------------------------------------------------------
# State I/O
# ----------------------------------------------------------------------

def load_state(session_dir):
    """Load per-session state from state.json. Returns defaults if missing."""
    path = os.path.join(session_dir, 'state.json')
    if os.path.exists(path):
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            pass
    return {
        'watermark': 0,
        'msg_count': 0,
        'milestone_fired': False,
        'conv_count': 0,
        'topic': '',
    }


def save_state(session_dir, state):
    """Save per-session state to state.json."""
    <!-- page 16 — 20260523_090353.jpg — RECOVERED page, was missing from original batch sequence -->
    try:
        with open(os.path.join(session_dir, 'state.json'), 'w') as f:
            json.dump(state, f)
    except OSError:
        pass


# ----------------------------------------------------------------------
# Breadcrumb (NEW in v2.0)
# ----------------------------------------------------------------------

def write_breadcrumb(project_root, session_dir):
    """Write current session path to .claude/.current-session-path.

    This lets Claude (via CLAUDE.md / /milestone) find the active session dir.
    Written on every UserPromptSubmit, before Claude processes the message.
    """
    breadcrumb = os.path.join(project_root, '.claude', '.current-session-path')
    rel_path = os.path.relpath(session_dir, project_root).replace('\\', '/')
    try:
        with open(breadcrumb, 'w', encoding='utf-8') as f:
            f.write(rel_path)
    except OSError:
        pass


# ----------------------------------------------------------------------
# Path helpers
# ----------------------------------------------------------------------

<!-- page 17 — 20260523_090400.jpg (previously labelled page 16) -->
def normalize_path(file_path):
    """Normalize a file path to relative, forward-slash format."""
    parts = file_path.replace('\\', '/')
    cwd = os.getcwd().replace('\\', '/')
    if cwd in parts:
        parts = parts[len(cwd):].lstrip('/')
    return parts.replace('\\', '/')
```

`.claude/hooks/check-milestone.py` — UserPromptSubmit hook (runs every user message):

```python
#!/usr/bin/env python3
"""UserPromptSubmit hook: auto-append timeline entries for file ops AND conversations.

v2.0: Full per-session docs. All writes go to per-session timeline.md.
- No shared file writes (no locking needed)
- Breadcrumb written on every message for Claude to find session dir
- No v1.1 migration, no stale cleanup

Two types of auto-entries:
1. File operations: pairs Write/Edit tool calls with Claude's preceding explanation
2. Conversation topics: when significant chat happens without file ops, logs user topics as discussion milestones

Key design:
- Watermark: only processes NEW transcript lines since last run
- Path normalization: always forward slashes
- Deduplication: skips files/topics already in per-session timeline
- Conversation threshold: logs a discussion entry after N user messages without file ops
"""
import json, os, re, sys
from datetime import datetime
<!-- page 17 — 20260523_090406.jpg -->

# Import shared utilities
sys.path.insert(0, os.path.dirname(__file__))
from session_utils import (
    get_session_dir, load_state, save_state, write_breadcrumb,
    normalize_path, SKIP_PATTERNS, CONVERSATION_THRESHOLD,
    ENRICHMENT_REMINDER, DEEP_REVIEW_REMINDER,
)


# ----------------------------------------------------------------------
# Text processing helpers (check-milestone specific)
# ----------------------------------------------------------------------

def clean_explanation(text):
    if not text:
        return ''
    flat = text.replace('\n', ' ').replace('\r', ' ')
    flat = re.sub(r'\*\*([^*]+)\*\*', r'\1', flat)
    flat = re.sub(r'`([^`]+)`', r'\1', flat)
    flat = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'\1', flat)
    flat = re.sub(r'\s+', ' ', flat).strip()

    for sent in re.split(r'(?<=[.!?])\s+', flat):
        sent = sent.strip()
        if len(sent) < 15:
            continue
        if sent.startswith(('|', '#', '>', '"', '---', '==')):
            continue
        return sent[:120].rstrip('.')
    return ''


<!-- page 18 — 20260523_090411.jpg -->
def extract_user_topic(text):
    """Extract a clean topic from a user message."""
    if not text:
        return ''
    if text.strip().startswith(('<ide_', '<system-reminder>', '<ide_opened_file>')):
        return ''
    clean = re.sub(r'<[^>]+>', '', text)
    flat = clean.replace('\n', ' ').replace('\r', ' ')
    flat = re.sub(r'\s+', ' ', flat).strip()
    if not flat or len(flat) < 10:
        return ''
    for sent in re.split(r'(?<=[.!?])\s+', flat):
        sent = sent.strip()
        if len(sent) > 10 and not sent.startswith(('|', '#', '>')):
            return sent[:100]
    if len(flat) > 10:
        return flat[:100]
    return ''


# ----------------------------------------------------------------------
# Transcript parser
# ----------------------------------------------------------------------

def parse_transcript(transcript_path, start_line=0):
    """Parse transcript for file ops AND conversation topics since watermark."""
    file_entries = []
    user_topics = []
    last_assistant_text = ''
    max_line = 0
    user_msg_count = 0

    with open(transcript_path, 'r', encoding='utf-8', errors='replace') as f:
<!-- page 19 — 20260523_090419.jpg -->
        for line_num, line in enumerate(f):
            max_line = line_num

            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except (json.JSONDecodeError, ValueError):
                continue

            msg = obj.get('message', {})
            if not isinstance(msg, dict):
                continue

            role = msg.get('role', '')
            content = msg.get('content', [])
            if not isinstance(content, list):
                continue

            for block in content:
<!-- page 20 — 20260523_090431.jpg -->
                if not isinstance(block, dict):
                    continue

                if role == 'assistant' and block.get('type') == 'text':
                    text = block.get('text', '').strip()
                    if len(text) > 10:
                        last_assistant_text = text

                if line_num < start_line:
                    continue

                if role == 'user' and block.get('type') == 'text':
                    text = block.get('text', '').strip()
                    if len(text) > 5:
                        topic = extract_user_topic(text)
                        if topic:
                            user_topics.append(topic)
                            user_msg_count += 1

                if role == 'assistant' and block.get('type') == 'tool_use':
                    name = block.get('name', '')
                    if name not in ('Write', 'Edit', 'NotebookEdit'):
                        continue

                    inp = block.get('input', {})
                    path = inp.get('file_path', inp.get('notebook_path', ''))
                    if not path:
                        continue

                    short = normalize_path(path)
                    if any(s in short for s in SKIP_PATTERNS):
                        continue
<!-- page 21 — 20260523_090438.jpg -->

                    file_entries.append({
                        'path': short,
                        'tool': name,
                        'explanation': clean_explanation(last_assistant_text),
                    })
                    user_msg_count = 0
                    user_topics = []

    seen = {}
    for entry in file_entries:
        seen[entry['path']] = entry
    deduped_files = list(seen.values())

    conversation_entry = None
    if user_msg_count >= CONVERSATION_THRESHOLD and user_topics:
        best_topic = max(user_topics, key=len)
        conversation_entry = best_topic

    return deduped_files, conversation_entry, max_line


def path_in_text(path, text):
    forward = path.replace('\\', '/')
    backward = path.replace('/', '\\')
    return (f"`{forward}`" in text or
            f"`{backward}`" in text or
            f"`{os.path.basename(path)}`" in text)
<!-- page 22 — 20260523_090446.jpg -->

# ----------------------------------------------------------------------
# Session timeline helpers
# ----------------------------------------------------------------------

def init_session_timeline(session_dir, today):
    """Create per-session timeline.md if it doesn't exist, with a [session-start] marker.

    The marker is written here (not in main) so it can never be skipped by a stale
    state.json: timeline.md existence is the single source of truth for 'session begun'.
    """
    path = os.path.join(session_dir, 'timeline.md')
    if not os.path.exists(path):
        with open(path, 'w', encoding='utf-8') as f:
            f.write("# Session Timeline\n\n| Date | Summary |\n|------|---------|\n")
            f.write(f"| {today} | [session-start] New session. |\n")


def init_session_discussions(session_dir):
    """Create per-session discussions.md if it doesn't exist."""
    path = os.path.join(session_dir, 'discussions.md')
    if not os.path.exists(path):
        with open(path, 'w', encoding='utf-8') as f:
            f.write("# Session Discussions\n\n> Auto-populated by hooks. Enriched by /milestone.\n\n")


# ----------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------

def main():
    try:
        input_data = json.load(sys.stdin)
        transcript_path = input_data.get('transcript_path', '')
        project_root = input_data.get('cwd', os.getcwd())
        session_id = input_data.get('session_id', '')
        today = datetime.now().strftime('%Y-%m-%d')

        if not transcript_path or not os.path.exists(transcript_path):
<!-- page 23 — 20260523_090450.jpg — page overlap; page 23 re-shows the def main() opening already transcribed from page 22, then continues from `print(json.dumps({}))` -->
            print(json.dumps({}))
            sys.exit(0)

        # --- Per-session setup ---
        session_dir = get_session_dir(project_root, session_id)
        state_file = os.path.join(session_dir, 'state.json')
        is_new_session = not os.path.exists(state_file)

        if is_new_session:
            state = load_state(session_dir)
            save_state(session_dir, state)  # Create state.json
        else:
            state = load_state(session_dir)

        # Write breadcrumb on EVERY message (before Claude processes)
        write_breadcrumb(project_root, session_dir)

        # Initialize per-session doc files (timeline carries [session-start] on creation)
        init_session_timeline(session_dir, today)
        init_session_discussions(session_dir)

        # Read per-session timeline (not shared)
        timeline_path = os.path.join(session_dir, 'timeline.md')
        with open(timeline_path, 'r', encoding='utf-8') as f:
<!-- page 24 — 20260523_090455.jpg -->
            existing_text = f.read()

        # --- Cross-day resume detection (from per-session state) ---
        if not is_new_session:
            last_date = state.get('last_date', '')
            if last_date and last_date != today:
                marker = f"| {today} | [session-resume] Same session resumed. Last active: {last_date}. |\n"
                with open(timeline_path, 'a', encoding='utf-8') as f:
                    f.write(marker)
                existing_text += marker

        # (The [session-start] marker is written by init_session_timeline on creation,
        # so existing_text already contains it from the read above.)

        # --- Parse transcript for file ops and conversation ---
        watermark = state.get('watermark', 0)
        file_entries, conversation_entry, max_line = parse_transcript(
            transcript_path, start_line=watermark
        )
        state['watermark'] = max_line + 1

        new_lines = []

        # Add file operation entries (no sid tag — implicit from directory)
        had_file_ops = False
        for e in file_entries:
            had_file_ops = True
            if not path_in_text(e['path'], existing_text):
                tool = 'Created' if e['tool'] == 'Write' else 'Edited'
                if e['explanation']:
                    new_lines.append(f"| {today} | [auto] {tool} `{e['path']}` — {e['explanation']} |\n")
                else:
                    new_lines.append(f"| {today} | [auto] {tool} `{e['path']}` |\n")
<!-- page 25 — 20260523_090502.jpg — Gap A reconstructed from sibling pattern in precompact-save.py update_timeline; needs photo verification -->
        # Persisted conversation counter
        conv_count = state.get('conv_count', 0)
        conv_topic = state.get('topic', '')

        current_prompt = input_data.get('prompt', '')
        if current_prompt and len(current_prompt) > 10:
            current_topic = extract_user_topic(current_prompt)
        else:
            current_topic = conversation_entry or ''

        if had_file_ops:
            conv_count = 0
            conv_topic = ''
        else:
            conv_count += 1
            if current_topic:
                conv_topic = current_topic

        if conv_count >= CONVERSATION_THRESHOLD and conv_topic:
            if conv_topic[:40] not in existing_text:
                new_lines.append(f"| {today} | [auto] Discussion: {conv_topic} |\n")
            conv_count = 0
            conv_topic = ''

        state['conv_count'] = conv_count
        state['topic'] = conv_topic

        # Periodic enrichment reminder
        msg_count = state.get('msg_count', 0)
        milestone_fired = state.get('milestone_fired', False)
        msg_count += 1

        if msg_count >= DEEP_REVIEW_REMINDER:
<!-- page 26 — 20260523_090507.jpg -->
            new_lines.append(
                f"| {today} | [reminder] Consider running `/deep-review` — {msg_count} messages since last deep review. |\n"
            )
            msg_count = 0
            milestone_fired = False
        elif msg_count >= ENRICHMENT_REMINDER and not milestone_fired:
            new_lines.append(
                f"| {today} | [reminder] Consider running `/milestone` — {msg_count} messages since last enrichment. |\n"
            )
            milestone_fired = True

        state['msg_count'] = msg_count
        state['milestone_fired'] = milestone_fired

        # Save per-session state
        save_state(session_dir, state)

        # Append new entries to per-session timeline (no locking needed)
        if new_lines:
            with open(timeline_path, 'a', encoding='utf-8') as f:
                for line in new_lines:
                    f.write(line)

        print(json.dumps({}))
    except Exception:
        print(json.dumps({}))
    sys.exit(0)


if __name__ == '__main__':
    main()
```

`.claude/hooks/precompact-save.py` — PreCompact hook (thorough save before context loss):

```python
<!-- page 27 — 20260523_090514.jpg -->
#!/usr/bin/env python3
"""PreCompact hook: THOROUGH session save before context compaction.

v2.0: All writes go to per-session directory. No shared file writes.

This is the LAST CHANCE to save session knowledge before Claude forgets.
Saves to per-session dir:
1. timeline.md       — file ops with context + compaction marker
2. discussions.md    — structured conversation summary grouped by topic flow
3. code-changes.md   — file content snapshots
4. transcript.jsonl  — raw transcript backup
5. Cleans up duplicate [auto] entries in per-session timeline
6. Writes info-loss warning if unmerged sessions exist
"""
import json, os, re, sys, shutil
from datetime import datetime

# Import shared utilities
sys.path.insert(0, os.path.dirname(__file__))
from session_utils import (
    get_session_dir, load_state, save_state, normalize_path, SKIP_PATTERNS,
)


# ----------------------------------------------------------------------
# Text processing helpers (precompact-specific)
# ----------------------------------------------------------------------

<!-- page 28 — 20260523_090518.jpg -->
def clean_text(text):
    if not text:
        return ''
    flat = text.replace('\n', ' ').replace('\r', ' ')
    flat = re.sub(r'\*\*([^*]+)\*\*', r'\1', flat)
    flat = re.sub(r'`([^`]+)`', r'\1', flat)
    flat = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'\1', flat)
    return re.sub(r'\s+', ' ', flat).strip()


def first_sentence(text, max_len=150):
    flat = clean_text(text)
    for sent in re.split(r'(?<=[.!?])\s+', flat):
        sent = sent.strip()
        if len(sent) < 15:
            continue
        if sent.startswith(('|', '#', '>', '"', '---', '==')):
            continue
        return sent[:max_len].rstrip('.')
    return flat[:max_len] if flat else ''


def path_in_text(path, text):
    forward = path.replace('\\', '/')
    backward = path.replace('/', '\\')
    return (f"`{forward}`" in text or
            f"`{backward}`" in text or
            f"`{os.path.basename(path)}`" in text)


<!-- page 29 — 20260523_090522.jpg -->
# ----------------------------------------------------------------------
# Transcript parser
# ----------------------------------------------------------------------

def parse_full_transcript(transcript_path):
    """Parse entire transcript into structured data."""
    file_ops = []
    code_changes = []
    conversations = []
    last_assistant_text = ''
    last_user_text = ''

    with open(transcript_path, 'r', encoding='utf-8', errors='replace') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except (json.JSONDecodeError, ValueError):
                continue

            msg = obj.get('message', {})
            if not isinstance(msg, dict):
                continue

            role = msg.get('role', '')
            content = msg.get('content', [])
            if not isinstance(content, list):
                continue

            for block in content:
                if not isinstance(block, dict):
                    continue

                if role == 'assistant' and block.get('type') == 'text':
                    text = block.get('text', '').strip()
                    if len(text) > 10:
                        last_assistant_text = text

                if role == 'user' and block.get('type') == 'text':
                    text = block.get('text', '').strip()
                    if len(text) > 10:
                        last_user_text = text

                if role != 'assistant' or block.get('type') != 'tool_use':
                    continue
                name = block.get('name', '')
                if name not in ('Write', 'Edit', 'NotebookEdit'):
<!-- page 30 — 20260523_090527.jpg — Gap B reconstructed from sibling parse_transcript pattern in check-milestone.py; needs photo verification -->
                    continue
                inp = block.get('input', {})
                path = inp.get('file_path', inp.get('notebook_path', ''))
                if not path:
                    continue
                short = normalize_path(path)
                if any(s in short for s in SKIP_PATTERNS):
                    continue

                explanation = first_sentence(last_assistant_text)
                file_ops.append({
                    'path': short,
                    'tool': name,
                    'explanation': explanation,
                })

                file_content = inp.get('content', inp.get('new_source', ''))
                if name == 'Edit':
                    old = inp.get('old_string', '')
                    new = inp.get('new_string', '')
                    file_content = f"--- EDIT ---\nOld:\n{old[:500]}\nNew:\n{new[:500]}"
                code_changes.append({
                    'path': short,
                    'tool': name,
                    'explanation': explanation,
                    'content': file_content[:3000] if file_content else '',
                })

        if last_user_text and last_assistant_text:
            conversations.append({
                'user': last_user_text[:500],
                'assistant': last_assistant_text[:2000],
            })

        seen = {}
        for op in file_ops:
<!-- page 31 — 20260523_090531.jpg -->
            seen[op['path']] = op
        return list(seen.values()), conversations, code_changes


# ----------------------------------------------------------------------
# Per-session output functions (all write to session_dir, not shared docs)
# ----------------------------------------------------------------------

def update_timeline(session_dir, file_ops, today):
    """Add missing file ops + compaction marker to per-session timeline."""
    timeline_path = os.path.join(session_dir, 'timeline.md')
    if not os.path.exists(timeline_path):
        with open(timeline_path, 'w', encoding='utf-8') as f:
            f.write("# Session Timeline\n\n| Date | Summary |\n|------|---------|\n")

    with open(timeline_path, 'r', encoding='utf-8') as f:
        existing = f.read()

    new_entries = []
    for op in file_ops:
        if not path_in_text(op['path'], existing):
            tool = 'Created' if op['tool'] == 'Write' else 'Edited'
            if op['explanation']:
                new_entries.append(f"| {today} | [auto] {tool} `{op['path']}` — {op['explanation']} |")
            else:
                new_entries.append(f"| {today} | [auto] {tool} `{op['path']}` |")

    if '[compaction-save]' not in existing:
        new_entries.append(f"| {today} | [compaction-save] Context compacted. Auto-saved {len(file_ops)} file ops, transcript backed up. |")

    if new_entries:
<!-- page 32 — 20260523_090534.jpg — overlaps page 31's tail; continuing from where new_entries gets written -->
        with open(timeline_path, 'a', encoding='utf-8') as f:
            for entry in new_entries:
                f.write(entry + '\n')


def update_discussions(session_dir, conversations, today, session_id='unknown'):
    """Write rich conversation pairs to per-session discussions.md."""
    disc_path = os.path.join(session_dir, 'discussions.md')
    if not os.path.exists(disc_path):
        with open(disc_path, 'w', encoding='utf-8') as f:
            f.write("# Session Discussions\n\n> Auto-populated by PreCompact hook.\n\n")

    if not conversations:
        return

    with open(disc_path, 'r', encoding='utf-8') as f:
        existing = f.read()

    session_header = f"## Pre-compaction Save — {today} ({session_id[:8]})"
    if session_header in existing:
        return

    ranked = sorted(conversations, key=lambda c: len(c['assistant']), reverse=True)
    key_exchanges = ranked[:5]

<!-- page 33 — 20260523_090537.jpg -->
    topics = []
    for conv in conversations:
        topic = conv['user'].replace('\n', ' ').strip()[:150]
        if topic and len(topic) > 10:
            topics.append(topic)

    unique_topics = []
    for t in topics:
        short = t[:40]
        if not any(short in ut for ut in unique_topics):
            unique_topics.append(t)

    summary = f"\n{session_header}\n\n"
    summary += f"**Session: {len(conversations)} exchanges, {len(unique_topics)} topics**\n\n"
    summary += "### Topics\n\n"
    for i, t in enumerate(unique_topics[:20], 1):
        summary += f"{i}. {t}\n"
    if len(unique_topics) > 20:
        summary += f"\n(+{len(unique_topics) - 20} more)\n"
    summary += "\n### Key Exchanges\n\n"
    for i, ex in enumerate(key_exchanges, 1):
        user_q = ex['user'].replace('\n', ' ').strip()[:200]
        assistant_clean = clean_text(ex['assistant'])[:500]
        summary += f"**Q{i}:** {user_q}\n\n"
        summary += f"**A{i}:** {assistant_clean}\n\n"
    summary += "---\n"

    with open(disc_path, 'a', encoding='utf-8') as f:
        f.write(summary)


<!-- page 34 — 20260523_090540.jpg -->
def save_code_changes(session_dir, code_changes, today, session_id='unknown'):
    """Save code change snapshots to per-session code-changes.md."""
    changes_path = os.path.join(session_dir, 'code-changes.md')
    if not os.path.exists(changes_path):
        with open(changes_path, 'w', encoding='utf-8') as f:
            f.write("# Code Changes Log\n\n> Auto-saved by PreCompact hook.\n\n")

    if not code_changes:
        return

    with open(changes_path, 'r', encoding='utf-8') as f:
        existing = f.read()

    session_header = f"## Compaction {today} ({session_id[:8]})"
    if session_header in existing:
        return

    seen = {}
    for change in code_changes:
        seen[change['path']] = change
    deduped = list(seen.values())

    entry = f"\n{session_header}\n\n**{len(deduped)} files changed:**\n\n"
    for change in deduped:
        tool = 'Created' if change['tool'] == 'Write' else 'Edited'
        entry += f"### {tool}: `{change['path']}`\n\n"
        if change['explanation']:
            entry += f"**Why:** {change['explanation']}\n\n"
        if change['content']:
            lines = change['content'].split('\n')[:50]
            content_preview = '\n'.join(lines)
            if len(change['content'].split('\n')) > 50:
                content_preview += f"\n... (+{len(change['content'].split(chr(10))) - 50} more lines)"
            entry += f"```\n{content_preview}\n```\n\n"
<!-- page 35 — 20260523_090542.jpg -->
    entry += "---\n"

    with open(changes_path, 'a', encoding='utf-8') as f:
        f.write(entry)


def save_raw_transcript(session_dir, transcript_path):
    """Copy raw transcript to per-session dir."""
    dump_path = os.path.join(session_dir, 'transcript.jsonl')
    try:
        shutil.copy2(transcript_path, dump_path)
    except Exception:
        pass


def cleanup_auto_entries(session_dir):
    """Remove duplicate [auto] entries from per-session timeline (keep last per file)."""
    timeline_path = os.path.join(session_dir, 'timeline.md')
    if not os.path.exists(timeline_path):
        return
<!-- page 36 — 20260523_090545.jpg — overlaps page 35 (save_raw_transcript + cleanup_auto_entries opening). Continuing from inside cleanup_auto_entries. -->

    with open(timeline_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    auto_lines = {}
    for i, line in enumerate(lines):
        if '[auto]' not in line:
            continue
        match = re.search(r"`([^`]+)`", line)
        if match:
            path = match.group(1).replace('\\', '/')
            if path in auto_lines:
                auto_lines[path] = ('replace', auto_lines[path][1], i)
            else:
                auto_lines[path] = ('keep', i)

<!-- page 37 — 20260523_090554.jpg -->
    remove_indices = set()
    for path, info in auto_lines.items():
        if info[0] == 'replace':
            remove_indices.add(info[1])

    if remove_indices:
        new_lines = [l for i, l in enumerate(lines) if i not in remove_indices]
        with open(timeline_path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)


# ----------------------------------------------------------------------
# Info-loss warning
# ----------------------------------------------------------------------

def count_unmerged_sessions(project_root, current_sid):
    """Count unmerged sessions and their total message count."""
    sessions_dir = os.path.join(project_root, '.claude', 'sessions')
    if not os.path.exists(sessions_dir):
        return 0, 0
    unmerged_count = 0
    total_msgs = 0
    try:
        for sid_dir in os.listdir(sessions_dir):
            state_path = os.path.join(sessions_dir, sid_dir, 'state.json')
            if os.path.exists(state_path):
                try:
                    with open(state_path) as f:
                        st = json.load(f)
                    if not st.get('merged', False):
                        unmerged_count += 1
<!-- page 38 — 20260523_090559.jpg -->
                        total_msgs += st.get('msg_count', 0)
                except (json.JSONDecodeError, OSError):
                    pass
    except OSError:
        pass
    return unmerged_count, total_msgs


# ----------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------

def main():
    try:
        input_data = json.load(sys.stdin)
        transcript_path = input_data.get('transcript_path', '')
        session_id = input_data.get('session_id', 'unknown')
        project_root = input_data.get('cwd', os.getcwd())
        today = datetime.now().strftime('%Y-%m-%d')

        # Get per-session directory
        session_dir = get_session_dir(project_root, session_id)
        state = load_state(session_dir)

        if transcript_path and os.path.exists(transcript_path):
            file_ops, conversations, code_changes = parse_full_transcript(transcript_path)

            # ALL writes go to per-session dir
            update_timeline(session_dir, file_ops, today)
            update_discussions(session_dir, conversations, today, session_id)
            save_code_changes(session_dir, code_changes, today, session_id)
            save_raw_transcript(session_dir, transcript_path)
            cleanup_auto_entries(session_dir)
<!-- page 39 — 20260523_090602.jpg — Gap C reconstructed from defined-but-uncalled functions; needs photo verification -->
        sid = re.sub(r'[^a-zA-Z0-9_-]', '', session_id[:8]) if session_id else 'unknown'
        unmerged, total_msgs = count_unmerged_sessions(project_root, sid)
        if unmerged > 0:
            timeline_path = os.path.join(session_dir, 'timeline.md')
            warning = f"| {today} | [warning] Context compacted. {unmerged} unmerged sessions with ~{total_msgs} messages. Run `/deep-review` to preserve cross-session knowledge. |\n"
            with open(timeline_path, 'a', encoding='utf-8') as f:
                f.write(warning)

        # Mark precompact as done in state
        state['precompact_saved'] = True
        save_state(session_dir, state)

        print(json.dumps({
            "systemMessage": "**[pre-compaction save]** Auto-save complete (per-session)."
        }))
    except Exception:
        print(json.dumps({}))
    sys.exit(0)


if __name__ == '__main__':
    main()
```

`.claude/hooks/session-end-save.py` — Stop hook (timestamp + discussion cache to per-session state):

```python
#!/usr/bin/env python3
"""Stop hook: saves last-active timestamp + discussion cache to per-session state.

v2.0: All writes go to per-session state.json. No shared files written.

Runs after every Claude response. Does:
<!-- page 40 — 20260523_090604.jpg -->
v2.0: All writes go to per-session state.json. No shared files written.

Runs after every Claude response. Does:
1. Updates last_active + last_date in per-session state.json
2. Saves recent user topics to discussion_cache field in state.json
"""
import json, os, sys
from datetime import datetime

# Import shared utilities
sys.path.insert(0, os.path.dirname(__file__))
from session_utils import get_session_dir, load_state, save_state


def extract_recent_topics(transcript_path, last_n_lines=200):
    """Extract user topics from the last N lines of transcript."""
    topics = []
    try:
        with open(transcript_path, 'r', encoding='utf-8', errors='replace') as f:
            lines = f.readlines()

        for line in lines[-last_n_lines:]:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except (json.JSONDecodeError, ValueError):
                continue

            msg = obj.get('message', {})
            if not isinstance(msg, dict):
                continue
            if msg.get('role') != 'user':
<!-- page 41 — 20260523_090607.jpg -->
                continue

            content = msg.get('content', [])
            if not isinstance(content, list):
                continue

            for block in content:
                if isinstance(block, dict) and block.get('type') == 'text':
                    text = block.get('text', '').strip()
                    if len(text) > 10:
                        topic = text.replace('\n', ' ').strip()[:150]
                        topics.append(topic)
    except Exception:
        pass
    return topics


def main():
    try:
        input_data = json.load(sys.stdin)
        project_root = input_data.get('cwd', os.getcwd())
<!-- page 42 — 20260523_090610.jpg -->
        session_id = input_data.get('session_id', 'unknown')
        transcript_path = input_data.get('transcript_path', '')
        today = datetime.now().strftime('%Y-%m-%d')
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Get per-session directory and load state
        session_dir = get_session_dir(project_root, session_id)
        state = load_state(session_dir)

        # 1. Update last-active in per-session state
        state['last_active'] = now
        state['last_date'] = today

        # 2. Save rolling discussion cache to per-session state
        if transcript_path and os.path.exists(transcript_path):
            topics = extract_recent_topics(transcript_path)
            if topics:
                unique = list(dict.fromkeys(topics))[-20:]
                state['discussion_cache'] = {
                    'timestamp': now,
                    'topics': unique,
                }

        save_state(session_dir, state)
<!-- page 43 — 20260523_090613.jpg — overlap; continues from save_state through end of session-end-save.py and into Step 5 -->

        print(json.dumps({}))
    except Exception:
        print(json.dumps({}))
    sys.exit(0)


if __name__ == '__main__':
    main()
```

## Step 5: Register hooks (OVERWRITE — always use latest)

IMPORTANT (CWD bug fix): Hook commands must use absolute paths via a `cd` prefix. If any Bash command during a session runs `cd` to a subdirectory, the shell CWD shifts and relative paths in hooks break. Use the current working directory (the project root where you're running right now) as `<PROJECT_ROOT>` below.

Create `.claude/settings.local.json` — replace `<PROJECT_ROOT>` with the actual absolute path to this project:

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
<!-- page 44 — 20260523_090615.jpg -->
        "hooks": [
          {
            "type": "command",
            "command": "cd \"<PROJECT_ROOT>\" && python .claude/hooks/check-milestone.py",
            "timeout": 10
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "cd \"<PROJECT_ROOT>\" && python .claude/hooks/session-end-save.py",
            "timeout": 5
          }
        ]
      }
    ],
<!-- page 45 — 20260523_090617.jpg -->
    "PreCompact": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "cd \"<PROJECT_ROOT>\" && python .claude/hooks/precompact-save.py",
            "timeout": 10
          }
        ]
      }
    ]
  }
}
```
<!-- page 47 — 20260523_090619.jpg — confirms JSON closing braces match page 45; settings.local.json ends here -->

## Step 6: Write version file

Create `.claude/.init-version` with:

```
2.0.2
```

This tracks which version of init-project was used to set up this project. Useful for upgrades.
<!-- page 48 — 20260523_090621.jpg -->

## Step 7: Confirm

List all created files and confirm the setup. Tell the user:

- **Version: 2.0.2**
- **What's new in v2.0:** Per-session docs (each session gets its own timeline, discussions, code-changes). No more shared file contention between sessions. Breadcrumb system lets `/milestone` find the right session automatically.
- **Automatic (no action needed):** Hooks auto-save file ops, conversations, and session state to per-session directories
- **Manual enrichment:** `/milestone` to clean up your session's docs, `/deep-review` to merge all sessions into shared docs
- **Lifecycle coverage:** Session start detection, cross-day resume, every-message tracking, periodic reminders (15/30 msgs), pre-compaction thorough save, session-end timestamps, info-loss warnings
- **Start a new session for hooks to take effect**
<!-- page 49 — 20260523_090622.jpg — visually identical to page 48 in the photo set; final page boundary. -->
