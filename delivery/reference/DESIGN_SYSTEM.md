# Design System

The canonical guide to component use for the Claude Code Walkthrough. Every demo HTML section is built from the components catalogued here, and every authoring brief cites this file. The "Core Standard" rule from [CLAUDE.md](../../CLAUDE.md) applies on top of everything below: components carry information density, layout makes it scannable, decorative use is a bug.

This spec documents only what exists in [delivery/assets/template.html](../assets/template.html). If a class isn't in that CSS, it isn't in this doc.

---

## 1. Palette

Fluent-derived tokens declared as CSS variables in `template.html` (`:root`, lines 17–43). Don't introduce ad-hoc hex codes; reuse the variable or the semantic equivalent.

| Token | Hex | Semantic meaning |
|---|---|---|
| `--ms-blue` | `#0078D4` | Primary brand. Headings, links, primary chrome, info accent. |
| `--ms-blue-dark` | `#005A9E` | Hover state for blue, deeper emphasis. |
| `--ms-green` | `#107C10` | Success, "after" panels, positive outcomes. |
| `--ms-orange` | `#F7630C` | Warning, capability risk, attention. |
| `--ms-red` | `#D13438` | Critical, safety risk, mistakes. |
| `--ms-purple` | `#5C2D91` | Hands-on / pointer accent, ops category. |
| `--text-primary` | `#2B2B2B` | Body text, h3/h4 headings. |
| `--text-secondary` | `#605E5C` | Meta text, captions, subdued copy. |
| `--bg-white` | `#FFFFFF` | Page background. |
| `--bg-light` | `#F3F2F1` | Code background, even-row table stripe. |
| `--bg-lighter` | `#FAF9F8` | Section card background, callout fill, diagram surround. |
| `--border-color` | `#EDEBE9` | Default border. |
| `--highlight-yellow` | `#FFF100` | Inline highlight only. |

**Rule:** don't reassign these. Don't repaint a callout to a colour that contradicts its variant. If you need a new colour, escalate — don't invent one inline.

---

## 2. Typography

Single family, weight-based hierarchy. Body line-height 1.6.

| Element | Size | Weight | Family |
|---|---|---|---|
| `h1` | 20px | 600 | Segoe UI stack |
| `h2` | 28px | 600 | Segoe UI stack — coloured `--ms-blue` |
| `h3` | 22px | 600 | Segoe UI stack |
| `h4` | 18px | 600 | Segoe UI stack |
| `h5` | 13px | 600 | Segoe UI — uppercase, letter-spaced |
| Body (`body`, `p`) | 16px | 400 | Segoe UI stack |
| Inline `code` | 14px | 400 | Consolas, Courier New, monospace |
| `pre` / code block | 14px | 400 | Consolas, Courier New, monospace |

Sans family: `'Segoe UI', -apple-system, BlinkMacSystemFont, system-ui, sans-serif`.
Mono family: `Consolas, 'Courier New', monospace`.

`h2` is reserved for section titles. `h3` opens a sub-area inside a section. `h4` heads a component (takeaway box title, split panel header). Don't skip levels.

---

## 3. Layout

| Property | Value |
|---|---|
| `.container` max-width | 1360px |
| `.container` padding | 2rem 2rem (top/bottom · left/right) |
| Right padding (≥841px) | `clamp(195px, calc(15vw + 2rem), 245px)` to clear the floating quicknav |
| `.section` padding | 2rem, 12px radius, soft shadow |
| Sticky header width | 1200px inner max-width |
| Quicknav breakpoint | hidden ≤840px; sized via `clamp()` ≥841px |
| Mobile breakpoint | ≤768px — cards collapse to 1 col, split-layout stacks, h2 → 22px |
| Tablet breakpoint | 769–1024px — card grid drops to 2 columns |
| Site-subtitle breakpoint | hidden ≤1280px |

Print styles strip nav/copy buttons and disable section animation.

---

## 4. Chrome elements

**Sticky header (`.site-header`)** — pinned to top, z-index 100, holds brand on the left and `.nav-parts` on the right. Contains the scroll-progress bar as a child.

**Scroll progress bar (`.scroll-progress`)** — thin blue bar (`--ms-blue`) anchored at the bottom edge of the header, width set by JS to reflect document scroll position.

**Sticky horizontal nav (`.nav-parts`)** — part-level navigation inside the header. The currently active part gets `.active` (filled blue). Hover state is subtle background only; no underlines.

**Skip-nav (`.skip-link`)** — visually hidden above the viewport, becomes visible on focus. Lets keyboard users jump straight to `#main`. Required for accessibility.

**Quicknav (`.section-quicknav` / `.sqn-panel` / `.sqn-list`)** — floating right-rail list of sections within the current part. Hidden ≤840px. Active item gets `.sqn-active`; draft items render as `.sqn-draft` (non-link, muted).

**Footer (`.site-footer`)** — closing block with tagline, link columns under `.footer-h` headers, and a "next session" line in `.footer-next`. No marketing copy.

---

## 5. Component library

Every component below has been verified against the CSS in `template.html`.

### 5.1 Section meta — `.section-meta` + `.progress-indicator`

The first row inside a `.section`: a small blue pill with the section number and Part.

- **Use when:** opening any numbered section in the demo HTML.
- **Don't use for:** sub-headings inside a section, or any non-numbered block.

```html
<div class="section-meta">
  <span class="progress-indicator">Section 3 of 12 · Part 2</span>
</div>
```

The CSS also defines `.reading-time` for an optional "X min read" badge. We don't use it in this walkthrough — reading-time estimates are unreliable for technical material and we'd rather not commit to numbers we can't trust.

### 5.2 Opening hook — `.opening-hook`

Single centred blue line at the top of a section that frames the question the section answers.

- **Use when:** you want one sentence to anchor the entire section before the body begins.
- **Don't use for:** body prose, multi-sentence intros, or anything you'd want left-aligned.

```html
<div class="opening-hook">
  <span class="icon">🎯</span>
  <span>Why does Claude Code need a CLAUDE.md at the repo root?</span>
</div>
```

### 5.3 Callouts — `.callout` + variant

Four variants, distinguished by left-border colour. Background is always `--bg-lighter`.

| Class | Border colour | Use for |
|---|---|---|
| `.callout-info` | `--ms-blue` | Teaching anchor, "rule of thumb", neutral note. |
| `.callout-success` | `--ms-green` | Positive pattern, what to do, confirmed outcome. |
| `.callout-warning` | `--ms-orange` | Watch-out, common pitfall that's recoverable. |
| `.callout-critical` | `--ms-red` | Hard rule, security risk, "do not". |

- **Use when:** a rule, warning, or anchor deserves to break out of prose.
- **Don't use for:** ordinary paragraphs, decorative emphasis, or stacking three in a row to colour-block a page.

```html
<div class="callout callout-warning">
  <strong>Watch-out:</strong> auto-compaction triggers near the 200k context
  limit — hand over at 50% instead.
</div>
```

### 5.4 Takeaway box — `.takeaway-box`

Yellow-gradient block with a heading and one supporting line. One per section, near the end.

- **Use when:** there is exactly one sentence the learner must walk away with.
- **Don't use for:** lists of takeaways, summaries, or any block longer than two sentences.

```html
<div class="takeaway-box">
  <span class="icon">💡</span>
  <h4>The takeaway</h4>
  <p>Match the model tier to the task; don't burn Opus on lint fixes.</p>
</div>
```

### 5.5 Hands-on pointer — `.notebook-pointer`

Purple-accented pointer that links a theory section to its hands-on artefact. The CSS class remains `.notebook-pointer` (inherited from the source template); the doc-facing name is "Hands-on pointer" because this project ships hands-on docs, not notebooks. The `::before` pseudo-element injects a 📓 glyph automatically.

- **Use when:** pointing from a concept section to the matching activity under `delivery/hands-on/`.
- **Don't use for:** internal section links, decorative banners, or anything that isn't a hands-on cross-reference.

```html
<div class="notebook-pointer">
  Try this yourself in
  <a href="../hands-on/demo-03-claude-md.md">Demo 3 — authoring CLAUDE.md</a>.
</div>
```

### 5.6 Card grid — `.card-grid` + `.example-card`

Three-column grid (2 columns on tablet, 1 column on mobile). Each card has a coloured left border. Variants present in CSS:

| Variant | Left border |
|---|---|
| `.example-card.blue` | `--ms-blue` |
| `.example-card.orange` | `--ms-orange` |
| `.example-card.purple` | `--ms-purple` |
| `.example-card.green` | `--ms-green` |
| `.example-card.red` | `--ms-red` |
| `.example-card.subdued` | thinner border, `--bg-lighter` fill |

Card internals use `.card-icon` (36px, centred) and `.card-title` (17px, centred, 600).

- **Use when:** at-a-glance summaries — one card per demo, role, command, failure mode, or rule.
- **Don't use for:** narrative content, single items (use a callout), or items that need more than ~3 lines of body text.

```html
<div class="card-grid">
  <div class="example-card blue">
    <div class="card-icon">🧭</div>
    <div class="card-title">Planning</div>
    <p>Use high-tier models; expect more thinking, fewer edits.</p>
  </div>
  <div class="example-card green">
    <div class="card-icon">🛠️</div>
    <div class="card-title">Execution</div>
    <p>Lower tier is fine when scope is well-defined.</p>
  </div>
</div>
```

### 5.7 Split layout — `.split-layout` + `.split-panel`

Two-column side-by-side. Each panel is bordered, with an `h4` header underlined in blue. Stacks vertically ≤768px.

- **Use when:** before/after, with/without, manual-vs-agent, good/bad — any direct comparison of exactly two options.
- **Don't use for:** three or more options (use a table or card grid), or non-parallel content.

```html
<div class="split-layout">
  <div class="split-panel">
    <h4>Without CLAUDE.md</h4>
    <p>Claude re-discovers conventions every session.</p>
  </div>
  <div class="split-panel">
    <h4>With CLAUDE.md</h4>
    <p>Claude follows the rules from message one.</p>
  </div>
</div>
```

### 5.8 Expandable — `.expandable` + `.expandable-header` + `.expandable-content`

Blue header bar that toggles `.open` on click; content area animates max-height. Used for deep dives kept hidden by default.

- **Use when:** long prompt examples, full code listings, optional "deeper dive" content that would otherwise overwhelm the section.
- **Don't use for:** content the learner must see, or critical warnings.

```html
<div class="expandable">
  <div class="expandable-header">
    <span>Full transcript</span>
    <span class="expandable-icon">▾</span>
  </div>
  <div class="expandable-content">
    <p>… full session log here …</p>
  </div>
</div>
```

### 5.9 Specialty boxes — `.quiz-box` / `.case-study` / `.mistake-box` / `.example`

Four pre-styled containers for specific narrative moments. Use sparingly — one per section at most.

| Class | Visual | Use when |
|---|---|---|
| `.quiz-box` | Blue gradient, blue border | A "test yourself" prompt with a hidden answer. |
| `.case-study` | Purple gradient, purple border | A short real-world walk-through with a named outcome. |
| `.mistake-box` | Red gradient, red border | A worked anti-pattern: what someone tried, why it failed. |
| `.example` | Plain `--bg-lighter` panel, subtle border | A neutral worked example without colour weight. |

- **Don't use for:** general callouts (use `.callout`), comparisons (use `.split-layout`), or decorative colour-blocking.

```html
<div class="mistake-box">
  <h4>What went wrong</h4>
  <p>The team committed `.env` because no pre-commit hook gated it.</p>
</div>
```

### 5.10 Tables — plain `<table>`

Styled globally: blue header row (white text), even-row stripe in `--bg-light`, hover in `--bg-lighter`, soft shadow. No special wrapper class is required (a `.table-wrapper` exists for horizontal scroll on wide tables).

- **Use when:** comparisons, matrices, structured field-by-field data, command references.
- **Don't use for:** layout, lists that aren't comparing anything, or single-column data (use a list).

```html
<table>
  <thead><tr><th>Command</th><th>Effect</th></tr></thead>
  <tbody>
    <tr><td><code>/clear</code></td><td>Reset context.</td></tr>
    <tr><td><code>/compact</code></td><td>Summarise prior turns.</td></tr>
  </tbody>
</table>
```

### 5.11 Code blocks — `.code-container` + `.code-header` + `<pre><code>`

Wrap `<pre>` in `.code-container`. Add a `.code-header` with a language label and an optional `.copy-button`. Always tag the language on the inner `<code>`.

- **Use when:** any prompt, settings.json, hook script, or command definition the learner might copy.
- **Don't use for:** inline single-token references (use plain `<code>`), pseudo-code without a label, or commentary that isn't runnable.

```html
<div class="code-container">
  <div class="code-header">
    <span>bash</span>
    <button class="copy-button">Copy</button>
  </div>
  <pre><code class="language-bash">claude --resume session-042</code></pre>
</div>
```

### 5.12 Diagrams / Mermaid — `.diagram` + size modifier + `.mermaid`

Diagram wrapper with three size variants: `.diagram-small` (≤600px), `.diagram-medium` (≤800px), `.diagram-large` (≤1000px). Wrapper has a `--bg-lighter` background, 1rem padding, centred. A `.mermaid-figure` variant adds a `<figcaption>` for captioned diagrams. A `.mermaid-fallback` block is available for browsers without JS.

- **Use when:** any non-trivial flow, loop, role chain, sequence, or architecture. Per CLAUDE.md: if you wrote 3+ sentences describing a sequence, it should be a diagram.
- **Don't use for:** a three-box line that adds nothing to a sentence, or decorative shapes.

```html
<div class="diagram diagram-medium">
  <pre class="mermaid">
    flowchart LR
      A[Plan] --> B[Execute] --> C[Review]
  </pre>
</div>
```

---

## 6. Component selection cheat sheet

| If you need to show… | Use this component |
|---|---|
| A flow, sequence, or architecture | Mermaid diagram (`.diagram`) |
| A side-by-side comparison of two things | Split layout (`.split-layout`) |
| Three or more parallel summaries | Card grid (`.card-grid` + `.example-card`) |
| A field-by-field comparison or command list | Table |
| A teaching anchor or "rule of thumb" | Callout info (`.callout-info`) |
| A pitfall that's recoverable | Callout warning (`.callout-warning`) |
| A hard rule or security risk | Callout critical (`.callout-critical`) |
| The single sentence to remember | Takeaway box (`.takeaway-box`) |
| A pointer to a hands-on doc | Hands-on pointer (`.notebook-pointer`) |
| A long transcript or optional deeper dive | Expandable (`.expandable`) |
| A worked anti-pattern | Mistake box (`.mistake-box`) |
| A short narrative walk-through with an outcome | Case study (`.case-study`) |
| A self-test prompt | Quiz box (`.quiz-box`) |
| A runnable prompt, config, or script | Code block (`.code-container`) |
| Section number + Part | Section meta (`.section-meta`) |
| The one sentence that frames the section | Opening hook (`.opening-hook`) |

---

## 7. Decorative-use ban

From [CLAUDE.md](../../CLAUDE.md) "Core Standard":

> **Decorative use is a bug.** A card with no information density, a tab group that's just a list with extra clicks, a mermaid diagram that's three boxes in a line — these are anti-patterns. If a plain paragraph carries the idea, use a paragraph.

Every component must earn its place. Before placing one, ask: what information does this carry that a sentence wouldn't? If the answer is "it looks nice," delete it.

---

## 8. Cross-references

- [CLAUDE.md](../../CLAUDE.md) — Core Standard, voice rules, the component-palette table that this doc expands.
- [dev/DELIVERY_PLAN.md §2](../../dev/DELIVERY_PLAN.md) — per-section component conventions and the seven content types every demo section must include.
- [dev/DELIVERY_PLAN.md §10](../../dev/DELIVERY_PLAN.md) — decisions log, including D-008 on the design-system rebrand.
- [delivery/assets/template.html](../assets/template.html) — the CSS source of truth. If this doc and the CSS disagree, the CSS wins; file a fix to this doc.
