# Sample output for Prompt B

Prompt:

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

Representative response shape:

```text
1. Best artifact right now: `delivery/walkthrough.html`, because the skeleton and section IDs already exist and the next unfinished unit is the `s-why` section.

2. Inspect before editing: `CLAUDE.md` for repo rules, `dev/batches/B1.md` for the section goal, `delivery/reference/SECTION_ANATOMY.md` for the section shape, `dev/TASKS.md` for live status, and the `s-why` stub in `delivery/walkthrough.html`.

3. Verify before accepting: the rendered section includes the seven required content types, every visible claim traces to `delivery/hands-on/s-why/EVIDENCE.md`, and the section is no longer marked with `data-stub="true"`.

4. Sign the prompt was too vague: the answer talks about Claude Code in general terms and never names repo files, the artifact to change, or the acceptance check.
```

What to notice:

- The answer starts with a concrete artifact, not a generic capability list.
- Inspection happens before editing.
- Verification is part of the first response, not an afterthought.
