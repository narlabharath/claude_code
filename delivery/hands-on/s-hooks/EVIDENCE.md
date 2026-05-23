# §12 s-hooks · Evidence

**Section role:** demo  
**Last verified:** 2026-05-23

## Inline evidence

- [Hook event types (PreToolUse, PostToolUse, Notification, Stop, SubagentStop)]: sourced from `https://docs.anthropic.com/en/docs/claude-code/hooks` · `last-verified: 2026-05-23`
- [hooks configuration in settings.json]: sourced from official hooks docs · `last-verified: 2026-05-23`
- [Hook shell script examples (logging, enforcement, notification)]: authored; consistent with hooks docs patterns · `last-verified: 2026-05-23`
- [Matcher patterns (`.*`, `Write`, `Bash`)]: sourced from hooks docs tool-name matching section · `last-verified: 2026-05-23`

## Sandbox-captured artifacts (if any)

None saved. B8 TODO: capture live hook execution log output to show pre/post event sequence.

## Anthropic assets embedded

None. §12 uses authored code blocks.

## Notes

- Hook scripts must be executable (`chmod +x`) on Mac/Linux. On Windows, PowerShell scripts require execution policy consideration. §12 notes this in the failure modes tab.
- `jq` dependency in hook examples is optional but common. The examples in §12 show both with and without `jq` variants.
- Hook events are documented in Claude Code hooks reference. Event names verified 2026-05-23.
