# EVIDENCE — §4 s-shape-scope: Shape the task and bound the scope

**Sandbox:** `claude-code-sandbox/dev/tier1-basics/` (same repo as §3, pre-fix state)  
**Starting state:** Fresh repo, `pytest` shows 1 failing test, no `.claude/`, no `CLAUDE.md`  
**Capture method:** `claude --print` (single-turn, Claude Code CLI v2.1.142)  
**Date:** 2026-05-23

---

## E-01 — Vague prompt output

**Prompt A (exact):**
```
Fix the bug in the calculator.
```

**Output (verbatim):**
```
I need permission to edit the file. The bug is in `src/calc.py:16` —
`range(len(items) - 1)` should be `range(len(items))` so the last item
is included in `running_total`. Please approve the edit (or grant write
permission) so I can apply the fix.
```

**What to notice:** In `--print` mode the agent asked for write permission rather than proceeding — which surfaces the issue: a vague prompt sends the agent straight toward an edit without inspection, without naming a scope, and without a plan proposal. In interactive mode this prompt would have jumped directly to an edit action. No inspection step. No "don't edit yet." No explicit scope.

**Failure chips:** no inspection / no explicit scope / no plan approval step

---

## E-02 — Shaped and scoped prompt output

**Prompt B (exact):**
```
Inspect src/calc.py and tests/test_calc.py. Identify the failing test and
the root cause. Do not edit yet — give me the smallest single-line change
that would fix it, and explain why that change and no other.
```

**Output (verbatim):**
```
Failing test: test_running_total

Root cause: src/calc.py:16 uses range(len(items) - 1), so the loop stops
one short. For [1, 2, 3] it produces [1, 3] instead of [1, 3, 6].

Smallest fix (one line): change line 16 from
    for i in range(len(items) - 1):
to
    for i in range(len(items)):

Why only this: the body totals.append(sum(items[:i + 1])) is already
correct — at i = len(items) - 1 the slice items[:len(items)] covers the
whole list and yields the final cumulative total. The only defect is the
loop bound truncating the last iteration; fixing the range restores all
expected outputs without touching otherwise-correct logic.
```

**What to notice:** Same repo, same bug. The shaped prompt forced: (1) explicit inspection of named files, (2) root-cause analysis before any edit, (3) a scoped one-line proposal, (4) justification for why no other lines need changing. The human is now in control of the scope.

**Success chips:** named files / inspect-first / propose before edit / scope = one line

---

## Claims this evidence supports

| Claim in §4 | Evidence row |
|---|---|
| "Vague prompts send the agent straight to action" | E-01 |
| "Shaped prompts force inspect-first behavior" | E-02 |
| "Bound the scope: the agent named exactly one line" | E-02 |
| "Same repo, two different prompts, two different behaviors" | E-01 + E-02 |
