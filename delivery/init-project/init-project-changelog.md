# init-project changelog

Read by `/init-project` during patch updates. Each entry below applies the upgrade from the previous version to itself.

For each entry the `/init-project` upgrade path uses:

- **What changed** — summary shown to the user for approval.
- **Files to update** — files whose Step body in `init-project.md` has changed; these get deleted and rewritten.
- **Unchanged files** — files explicitly held stable in this release; listed so the upgrade walker leaves them alone.

If no entry exists that upgrades FROM `<old_version>`, `/init-project` reports "Already at latest version" and stops.

---

## v2.0.2 (2026-03-09) — upgrades from v2.0.1

**What changed:**

- The `/init-project` command now reads this changelog during patch updates so it can apply changes precisely instead of rewriting every file.
- Fixed live slash command files (`milestone.md`, `deep-review.md`) that had drifted out of sync with the canonical package.

**Files to update:**

- `.claude/commands/milestone.md` (Step 3)
- `.claude/commands/deep-review.md` (Step 3)
- `.claude/.init-version` (Step 6 — write `2.0.2`)

**Unchanged files:**

- `.claude/hooks/session_utils.py`
- `.claude/hooks/check-milestone.py`
- `.claude/hooks/precompact-save.py`
- `.claude/hooks/session-end-save.py`
- `.claude/settings.local.json`
- `CLAUDE.md` (Step 2 — preserved)
- `docs/project-log/*.md` (Step 1 — preserved)

---

## v2.0.1 (2026-03-08) — upgrades from v2.0

**What changed:**

- `/deep-review` now enriches empty per-session `discussions.md` from `state.json`'s `discussion_cache` and any `[auto] Discussion:` timeline entries before merging into shared docs.
- `/milestone` now mandates a discussion update with an explicit list of data sources to consult (state cache, timeline auto entries, current conversation context).

**Files to update:**

- `.claude/commands/milestone.md` (Step 3)
- `.claude/commands/deep-review.md` (Step 3)
- `.claude/.init-version` (Step 6 — write `2.0.1`)

**Unchanged files:**

- `.claude/hooks/session_utils.py`
- `.claude/hooks/check-milestone.py`
- `.claude/hooks/precompact-save.py`
- `.claude/hooks/session-end-save.py`
- `.claude/settings.local.json`
- `CLAUDE.md` (Step 2 — preserved)
- `docs/project-log/*.md` (Step 1 — preserved)

---

## v2.0 (2026-03-06) — upgrades from v1.x

> Note: the v2.0 upgrade is handled by the dedicated "v2.0 Upgrade Sequence" inside `init-project.md` Step 0 (not by walking this changelog). This entry exists so the changelog ladder reads cleanly; do not run a patch update through it.

**What changed:**

- Major redesign: per-session doc architecture. Each Claude session gets its own folder under `.claude/sessions/{sid}/` with private `timeline.md`, `discussions.md`, `state.json`, and (on PreCompact) `code-changes.md` + `transcript.jsonl`.
- Breadcrumb file `.claude/.current-session-path` lets `/milestone` find the active session.
- `/deep-review` is now the only path from per-session docs into the shared `docs/project-log/`.
- Hooks rewritten to write only to per-session directories — no shared-file contention, no file locking.
- Settings now use absolute-path `cd` prefixes to defend against CWD shifts during a session.

**Files touched (full rewrite):**

- `.claude/hooks/session_utils.py` (NEW)
- `.claude/hooks/check-milestone.py`
- `.claude/hooks/precompact-save.py`
- `.claude/hooks/session-end-save.py`
- `.claude/commands/milestone.md`
- `.claude/commands/deep-review.md`
- `.claude/settings.local.json`
- `CLAUDE.md` (template refresh, user content preserved)
- `.claude/.init-version` → `2.0`

**Preserved:**

- `docs/project-log/` (historical entries moved to `## Pre-v2.0 History` sections during the migration).
- `.claude/sessions/*/state.json` (existing per-session state kept; v2.0 hooks add `timeline.md` alongside on first message).
