# EVIDENCE — §3 s-loop: What using Claude Code well looks like

**Sandbox:** `claude-code-sandbox/dev/tier1-basics/`  
**Starting state:** Fresh repo, `pytest` shows 1 failing test (`test_running_total`), no `.claude/`, no `CLAUDE.md`  
**Capture method:** `claude --print` (single-turn, Claude Code CLI v2.1.142)  
**Date:** 2026-05-23

---

## E-01 — Inspection output (Inspect step)

**Prompt used (exact):**
```
Explore this repo. Show me the file structure, read the source code and tests,
identify any failing tests, and give me the root cause. Do not edit anything.
```

**Output (verbatim):**
```
## Structure
README.md
src/calc.py        # add, subtract, multiply, running_total
tests/test_calc.py # tests for all four

## Failing test
`test_running_total` fails. (`test_add`, `test_subtract`, `test_multiply` pass.)

- `running_total([1, 2, 3])` returns `[1, 3]`, expected `[1, 3, 6]`
- `running_total([10, 20])` returns `[10]`, expected `[10, 30]`

## Root cause
`src/calc.py:16` — off-by-one in the loop bound:

    for i in range(len(items) - 1):

This iterates 0..len(items)-2, so the cumulative sum for the final element
is never appended. The fix would be `range(len(items))`.
```

**What to notice:** Claude Code reads the full file tree, runs the test, and identifies the root cause — not just the symptom — before any edit is proposed.

---

## E-02 — Plan step (shaped prompt proposing a fix)

**Prompt used (exact):**
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

**What to notice:** Agent proposes a minimal, scoped change with explicit reasoning — exactly the Plan step behavior.

---

## E-03 — Edit step (the change)

**Change applied to `src/calc.py`:**
```diff
-    for i in range(len(items) - 1):   # BUG: off-by-one — last item is never included
+    for i in range(len(items)):
```

Single line changed. No other files touched.

---

## E-04 — Verify step (test output after fix)

**Command:**
```
python -m pytest tests/ -v
```

**Output (verbatim):**
```
============================= test session starts =============================
platform win32 -- Python 3.12.0, pytest-9.0.3
collected 4 items

tests/test_calc.py::test_add PASSED                                      [ 25%]
tests/test_calc.py::test_subtract PASSED                                 [ 50%]
tests/test_calc.py::test_multiply PASSED                                 [ 75%]
tests/test_calc.py::test_running_total PASSED                            [100%]

============================== 4 passed in 0.05s ==============================
```

**What to notice:** All 4 pass. The fix was local to the identified line. Tests are the verification — not visual inspection.

---

## Claims this evidence supports

| Claim in §3 | Evidence row |
|---|---|
| "Inspect first — read the repo before touching it" | E-01 |
| "Plan step produces a scoped proposal before edits" | E-02 |
| "Edit step is the smallest change that fixes the stated problem" | E-03 |
| "Verify step runs the tests — not visual inspection" | E-04 |
| "Review step: human checks diff before accepting" | E-03 (diff visible, one line) |
