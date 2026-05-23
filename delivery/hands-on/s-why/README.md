# Optional first activity — `s-why` fit-check

`§1 / s-why` is now a framing section, not a runnable demo. This folder is kept as an optional first activity for readers who want to do a quick fit-check before the rest of Part 1.

Use it before the first edit in a repo, or whenever a task feels broad enough that a generic prompt would waste time.

## What this activity is for

- testing whether your opening prompt is tied to a real artifact
- forcing inspection before edits are proposed
- deciding what result must be true before you accept the work

## Run the activity

1. Open [prompts.md](prompts.md).
2. Read `Prompt A` first so you can see the weak starting shape.
3. Run `Prompt B` in Claude Code inside a repo with real files.
4. Compare the answer against [samples/prompt-b-output.md](samples/prompt-b-output.md).
5. If the answer stays generic, compare it with [samples/prompt-a-output.md](samples/prompt-a-output.md) and tighten the prompt before you edit anything.

## What a useful answer contains

- the artifact to work on
- the files to inspect before editing
- the result to verify before accepting the change
- one signal that your prompt was too vague

If any of those are missing, stop and reshape the prompt.
