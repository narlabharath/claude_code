# §13 s-mcp — Evidence Record

**Section:** §13 — MCP: bringing external context in  
**Batch:** B5 — Tier 4 Power-ups  
**Date captured:** 2026-05-23  
**Captured by:** Session 042 (html-build)

---

## Artifacts

| # | Type | Description | Location | Status |
|---|---|---|---|---|
| 1 | File embed | `.mcp.json` filesystem MCP config (project-scoped, ~7 lines) | `tier4-powerups/.mcp.json` | ✅ real file, embedded verbatim in Tab 2 |
| 2 | Terminal transcript | `/mcp` command output showing `filesystem` server connected with 8 tools | Authored as representative text in Tab 2 | ✅ representative (actual screenshot deferred) |
| 3 | Text comparison | Without-MCP prompt + output ("asks for paste") | Authored in Tab 2 split-layout | ✅ representative |
| 4 | Text comparison | With-MCP prompt + output (uses `filesystem__list_directory`, returns real file names) | Authored in Tab 2 split-layout | ✅ representative |

---

## MCP config location — verified

Per official docs (`code.claude.com/docs/en/mcp`, verified 2026-05-23): project-scoped MCP config lives at `.mcp.json` in the project root, NOT `.claude/mcp.json`. The sandbox file has been created at the correct location.

## Architecture diagram

No architecture diagram exists on the `code.claude.com/docs/en/mcp` page (verified 2026-05-23). A 3-box built visual (Host ↔ Client ↔ Server) was authored inline. See `dev/plans/ANTHROPIC_ASSET_REUSE.md` §13 row.

## Sample content (MCP server target)

Three files created in `tier4-powerups/docs/sample-content/`:
- `notes-2024-q1.md` — Q1 engineering notes
- `notes-2024-q2.md` — Q2 engineering notes
- `customer-feedback.csv` — 10 rows of customer feedback

## Deferred captures

- `/mcp` screenshot (live Claude Code session) — deferred, represented as text
- Before/after session screenshots — deferred, represented as structured text blocks
