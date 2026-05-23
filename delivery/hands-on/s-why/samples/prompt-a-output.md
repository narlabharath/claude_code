# Sample output for Prompt A

Prompt:

```text
Explain Claude Code and tell me how to use it.
```

Typical response shape:

```text
Claude Code can inspect files, answer questions, propose edits, and help review code.
Give it clear instructions, enough context about your project, and a concrete task.
You can ask it to explain a file, generate a change, or help debug an issue.
```

Why this is weak:

- It never names the artifact to change.
- It never names the files to inspect.
- It never tells you what result to verify before you accept the work.
- It describes the tool in general terms instead of grounding the next step in the repo.
