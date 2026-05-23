# §11 s-settings · Evidence

**Section role:** demo + explanation  
**Last verified:** 2026-05-23

## Inline evidence

- [settings.json schema (allowedTools, disallowedTools, permissions, etc.)]: sourced from `https://docs.anthropic.com/en/docs/claude-code/settings` · `last-verified: 2026-05-23`
- [Permission modes description (default / auto-approve / manual)]: sourced from `https://docs.anthropic.com/en/docs/claude-code/permission-modes` · `last-verified: 2026-05-23`
- [Scope fencing examples (folder restrictions, tool deny-list)]: authored from first principles consistent with settings docs · `last-verified: 2026-05-23`
- [settings.json code example]: authored; matches schema documented at official settings page · `last-verified: 2026-05-23`

## Sandbox-captured artifacts (if any)

None. §11 uses authored code examples. B8 TODO: validate settings.json samples by running them against a live session.

## Anthropic assets embedded

None. All content is text-based.

## Notes

- Settings file location: `~/.claude/settings.json` (global) and `.claude/settings.json` (project). Both documented in §11.
- `allowedTools` / `disallowedTools` key names verified against Anthropic settings docs as of 2026-05-23. Schema may evolve — re-verify on next session update.
