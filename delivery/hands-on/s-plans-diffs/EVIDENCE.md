# §8 s-plans-diffs · Evidence

**Section role:** demo  
**Last verified:** 2026-05-23

## Inline evidence

- [3-gate model (plan / diff / permission prompt)]: authored from first principles; consistent with Anthropic's agentic safety guidance at `https://docs.anthropic.com/en/docs/claude-code/security` · `last-verified: 2026-05-23`
- [Plan mode description and `--plan` flag]: sourced from `dev/CLAUDE_CODE_DOCS_AUDIT.md` · `last-verified: 2026-05-23`
- [Diff block format example]: authored to match Claude Code's standard unified diff output format; no sandbox capture · `last-verified: 2026-05-23`
- [Permission prompt tiers (Allow Once / Allow for Session / Always Allow / Deny)]: sourced from official permission-modes docs page · `last-verified: 2026-05-23`

## Sandbox-captured artifacts (if any)

None saved to `delivery/assets/`. B8 polish TODO:
- Capture a real plan output for a representative task
- Capture a permission prompt screenshot

## Anthropic assets embedded

- Possible hotlinks from mintcdn in §8 — verify and download to `delivery/assets/Images/` during B8.

## Notes

- The `--plan` flag behavior (outputs plan without executing) is verified against Claude Code CLI docs.
- Diff examples are synthetic but formatted as actual unified diff output. Replace with real captures in B8 if possible.
