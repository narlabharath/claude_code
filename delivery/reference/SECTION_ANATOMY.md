# Section Anatomy

Every major section follows the same shape. The goal is consistency without flattening the content: each section should feel predictable to navigate, but dense enough to teach something concrete.

Use this sequence:

1. Opening hook
2. `h2` title
3. Intro
4. Optional Mermaid diagram
5. Body
6. Takeaway
7. Hands-on pointer

The progress pill (`.section-meta` + `.progress-indicator`) sits above that sequence as section chrome. Keep it in every major section, but treat the list above as the teaching anatomy.

---

## 1. Canonical sequence

| Block | Required | Purpose | Typical length |
|---|---|---|---|
| Opening hook | Yes | State the question or tension the section resolves. | 1 sentence |
| `h2` title | Yes | Name the section clearly and match the navigation label. | 2–6 words |
| Intro | Yes | Explain what this section covers and why it matters. | 2–3 sentences |
| Mermaid diagram | Only when needed | Show a flow, loop, role chain, or architecture that would be clumsy in prose. | 1 diagram |
| Body | Yes | Carry the real teaching content: prompts, examples, outputs, explanation, and failure modes. | 2–5 subsections |
| Takeaway | Yes | Leave one rule of thumb the reader should remember. | 1 sentence |
| Hands-on pointer | Yes | Point to the matching practice artifact. | 1 sentence + link |

---

## 2. What belongs in each block

### Opening hook

Use `.opening-hook` for the single sentence that frames the section.

- Ask the question the section answers, or name the mistake it prevents.
- Keep it specific.
- Do not turn it into a paragraph.

Good shape:

- "Why does the operating loop start with inspection instead of editing?"
- "What breaks when a task is broad but the scope is not fenced?"

Weak shape:

- "This section talks about many important ideas."

### `h2` title

The title should match the progress pill and the quicknav label. Do not restate the hook. The hook creates tension; the title names the topic.

### Intro

Use the intro to answer three questions quickly:

1. What is this section about?
2. When would you reach for this technique?
3. What should the reader look for in the rest of the section?

This is the setup, not the full explanation. Keep it short.

### Optional Mermaid diagram

Add a Mermaid block when the idea has shape:

- a sequence
- a loop
- a role chain
- a comparison with directional flow
- a small architecture

Skip the diagram when a short paragraph is clearer.

Rule of thumb: if the explanation needs three or more sentences to describe movement from one step or actor to another, use Mermaid.

### Body

The body holds the real teaching content. Split it into 2–5 subsections with `h3` headings when needed. The body is where the section earns its space.

The body should normally include:

- when to use this
- the prompt or command to try
- sample output, transcript, screenshot, or expected behavior
- explanation of what happened
- common failure modes
- optional deeper dive content in an expandable block

Use components only when they carry more information than plain prose:

- Use a table for a comparison or matrix.
- Use a split layout for exactly two parallel states: before/after, good/bad, with/without.
- Use cards only when there are three or more compact parallel summaries.
- Use a callout for a rule, warning, or critical limit.
- Use a code block for anything the reader might copy.
- Use an expandable for the deeper dive, not for required content.

Digestibility rule:

- Do not default to professor-mode formatting just because the content is technical.
- If a less-technical reader would understand the same point faster as a visual progression, colored card set, comparison, or concrete scenario scene, prefer that over dense tables or long prose.
- Use tables when the table is genuinely the clearest form, not just because the information is structured.

### Takeaway

Use exactly one `.takeaway-box` per section.

- Reduce the section to one rule of thumb.
- Keep it short enough to scan.
- Do not repeat the whole intro.

### Hands-on pointer

End the section with one `.notebook-pointer` linking to the matching hands-on artifact.

- Point to one clear next action.
- Use the real path or folder name.
- Do not use this block for internal section jumps.

---

## 3. Mapping the seven required content types

Every demo section needs seven content types. This is where they usually sit inside the anatomy.

| Content type | Where it appears |
|---|---|
| What it teaches | Opening hook + intro + takeaway |
| When you would use it | Intro or first body subsection |
| Prompt(s) to try | Body, usually in a code block |
| Sample output / expected behavior | Body, as transcript, screenshot, snippet, or comparison |
| Explanation | Body, near the example it explains |
| Common failure modes | Body, usually a warning callout, mistake box, table, or comparison |
| Optional deeper dive | Body, inside an expandable block |

The takeaway is not a substitute for the explanation. The explanation does the technical work; the takeaway leaves the memory anchor.

---

## 4. Component rules inside the body

Follow the existing design system. These are the selection rules that matter most at section level:

- Do not add a component only for visual variety.
- Use one strong component at a time when a plain paragraph cannot carry the idea cleanly.
- If a diagram is only three boxes in a line, cut it.
- If a tab set hides content that should stay visible, cut it.
- If a card contains only one weak sentence, cut it.
- If the section has no prompt, no output, or no failure mode, the section is incomplete even if it looks finished.

Preferred body patterns:

- Explanation + code block + output snippet
- Short intro + Mermaid + explanation
- Split layout for bad prompt / good prompt
- Table for failure signals and what they mean
- Expandable for transcript, full prompt pack, or detailed rationale

---

## 5. Canonical HTML skeleton

```html
<section id="s-example" class="section">
  <div class="section-meta">
    <span class="progress-indicator">Section N of 10 · Part X</span>
  </div>

  <div class="opening-hook">
    <span>One sentence that frames the section.</span>
  </div>

  <h2>Section title</h2>

  <p>
    Two or three sentences explaining what this section covers, when it
    matters, and what to look for below.
  </p>

  <div class="diagram diagram-medium">
    <pre class="mermaid">
      flowchart LR
        A[Inspect] --> B[Plan] --> C[Edit] --> D[Verify] --> E[Review]
    </pre>
  </div>

  <h3>When to use it</h3>
  <p>Describe the scenario.</p>

  <h3>Prompt to try</h3>
  <div class="code-container">
    <div class="code-header"><span>text</span></div>
    <pre><code class="language-text">Exact prompt text goes here.</code></pre>
  </div>

  <h3>What to notice</h3>
  <p>Explain why the example works.</p>

  <div class="callout callout-warning">
    <strong>Failure mode:</strong> name what commonly goes wrong.
  </div>

  <div class="expandable">
    <div class="expandable-header">
      <span>Deeper dive</span>
      <span class="expandable-icon">▾</span>
    </div>
    <div class="expandable-content">
      <p>Optional transcript, code, or extended explanation.</p>
    </div>
  </div>

  <div class="takeaway-box">
    <h4>The takeaway</h4>
    <p>One rule of thumb to remember.</p>
  </div>

  <div class="notebook-pointer">
    Try it in <a href="../hands-on/s-example/">delivery/hands-on/s-example/</a>.
  </div>
</section>
```

Use the diagram block only when the section needs it. The rest of the sequence stays stable.

---

## 6. Section-level checks

Before calling a section finished, confirm:

- The hook, title, intro, takeaway, and hands-on pointer are all present.
- The body includes a real prompt and a real output or expected behavior.
- The body names at least one failure mode.
- Any deeper dive content is optional and hidden by default.
- Any diagram explains real structure, not decoration.
- The section can be scanned top-to-bottom without guessing where the example or takeaway lives.

Consistency matters more than novelty. A reader should know where to look before reading the first sentence.
