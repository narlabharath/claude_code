# §10 s-memory · Evidence

**Section role:** demo + explanation  
**Last verified:** 2026-05-23

## Inline evidence

- [CLAUDE.md spec (project memory file, read at session start)]: sourced from `https://docs.anthropic.com/en/docs/claude-code/memory` · `last-verified: 2026-05-23`
- [AGENTS.md description and scope]: sourced from `dev/CLAUDE_CODE_DOCS_AUDIT.md` · `last-verified: 2026-05-23`
- [Memory file hierarchy (global → project → local)]: sourced from official memory docs page · `last-verified: 2026-05-23`
- [Sample CLAUDE.md content]: drawn from `delivery/assets/` sample CLAUDE.md template and from this repo's own `CLAUDE.md` · `last-verified: 2026-05-23`

## Sandbox-captured artifacts (if any)

None saved. B8 TODO: capture a session showing `claude` loading CLAUDE.md at startup (context-loading output).

## Anthropic assets embedded

- `context-loading.svg` — downloaded from Anthropic docs CDN to `delivery/assets/Images/context-loading.svg` during Session 043. Embedded in §10 body. `last-verified: 2026-05-23`

## Notes

- The `context-loading.svg` asset must be re-verified against `delivery/assets/Images/` in B8 — confirm file is present and the `<img>` src path in §10 is correct.
- AGENTS.md is documented as the OpenAI-compatible variant of CLAUDE.md. Both are read; CLAUDE.md takes project-level precedence.
