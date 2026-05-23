# Optional prompts for `s-why`

Use these prompts if you want a quick fit-check before the rest of Part 1. They are an optional activity, not evidence backing the framing section itself.

## Prompt A — too vague

```text
Explain Claude Code and tell me how to use it.
```

Use this once so you can see the failure mode. It usually produces general advice, not a next action tied to the repo in front of you.

## Prompt B — fit-check the repo before editing

```text
You are in a real repo. Before suggesting edits, inspect the files that define the work:
- CLAUDE.md
- dev/batches/B1.md
- delivery/reference/SECTION_ANATOMY.md
- dev/TASKS.md
- delivery/walkthrough.html

Then answer in four short parts:
1. Which artifact in this repo is the best target for Claude Code right now?
2. Which files should be inspected before any edit is proposed?
3. What result should be verified before the work is accepted?
4. What is one sign that the prompt was too vague?

Keep the answer grounded in the files you inspected. Do not give a feature tour.
```

## How to adapt the fit-check prompt

Replace the file list with the artifacts that actually define the task:

- code change: source file, tests, task tracker, local rules
- docs change: source notes, style guide, target document, acceptance checklist
- data task: schema, notebook or script, sample data, success metric

The pattern stays the same: artifact, inspection target, verification target, failure signal.
