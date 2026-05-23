# §16 s-discipline — Evidence Log

## What's captured / embedded

### Anthropic asset: context-loading.svg
- **Source**: `https://mintcdn.com/claude-code/6yTCYq1p37ZB8-CQ/images/context-loading.svg`
  (retrieved from `code.claude.com/docs/en/features-overview`)
- **Local path**: `delivery/assets/Images/context-loading.svg`
- **Usage**: Tab 1 (blue) — embedded inline with caption attributing `code.claude.com/docs/en/features-overview`
- **Last verified**: Session 043

### Redirect: context-window simulator
- **Target**: `https://anthropic.com/claude-code` (placeholder; actual simulator URL = `code.claude.com/docs/en/features-overview`)
- **Usage**: Tab 2 (orange) — card with outbound link, presented as a redirect per D-021
- **Decision**: D-021 (embed where assets exist; redirect for interactive tools)

### Handover structure example
- **Source**: `dev/sessions/session-042-html-build.md` — §0 structure (goal, sections in-scope, context budget, handover rule) used as a code-block illustration in Tab 3 (green)
- **Curated in section**: Yes — real text from the session note, not a mock

## Acceptance criteria met
- [x] Tab 1: model selection 3-cards + embedded SVG
- [x] Tab 2: 50% rule 2 scenario cards + simulator redirect card
- [x] Tab 3: dark pre block showing real handover structure
- [x] Expandable: "When to override the 50% rule"
- [x] Section-footer → §17
- [x] No data-stub attribute
