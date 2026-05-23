# EVIDENCE — §5 s-verify-review: Verify, review, and manage context

**Sandbox:** `claude-code-sandbox/dev/tier1-basics/` (continuation from §4 — fix applied)  
**Starting state:** Fix applied to `src/calc.py:16`; repo now passes all 4 tests  
**Capture method:** `python -m pytest` (direct) + known diff (one-line change)  
**Date:** 2026-05-23

---

## E-01 — Verify: test output after fix

**Command:**
```
python -m pytest tests/ -v
```

**Output (verbatim):**
```
============================= test session starts =============================
platform win32 -- Python 3.12.0, pytest-9.0.3, pluggy-1.6.0
collected 4 items

tests/test_calc.py::test_add PASSED                                      [ 25%]
tests/test_calc.py::test_subtract PASSED                                 [ 50%]
tests/test_calc.py::test_multiply PASSED                                 [ 75%]
tests/test_calc.py::test_running_total PASSED                            [100%]

============================== 4 passed in 0.05s ==============================
```

**What to notice:** Verification is a command, not a feeling. 4/4 pass means the change is safe — not "it looks right."

---

## E-02 — Review: the diff

**What the human reviews before accepting:**
```diff
--- a/src/calc.py
+++ b/src/calc.py
@@ -13,6 +13,6 @@
 def running_total(items):
     """Return a list of cumulative totals for each position in items."""
     totals = []
-    for i in range(len(items) - 1):   # BUG: off-by-one — last item is never included
+    for i in range(len(items)):
     totals.append(sum(items[:i + 1]))
     return totals
```

**What the human checks:**
- Is this the only line changed?
- Does the change match the proposal from the Plan step?
- Does removing the comment make the intent clearer?
- Any side-effects visible from this diff?

**What to notice:** One line changed. Diff is the contract. The review is brief because the scope was bounded in the Plan step — if the scope had been left open, the diff could have been much larger.

---

## E-03 — Manage context: what the agent used

For this single-file, 4-function repo the context footprint was minimal:
- Files read: `src/calc.py`, `tests/test_calc.py`, `README.md`
- No CLAUDE.md, no `.claude/`, no prior session context
- Total context consumed: well under 5% of the context window

**What to notice (for the section):** The agent needed exactly the files named in the shaped prompt. Giving it the whole filesystem, open tabs, or unrelated files would not have improved the output — and would have left less context window for the loop continuation.

**Link for learners:** Anthropic's interactive context-window simulator:  
https://docs.anthropic.com/en/docs/claude-code/contexts

---

## Claims this evidence supports

| Claim in §5 | Evidence row |
|---|---|
| "Verify = run the tests, not eyeball the code" | E-01 |
| "Review = read the diff, check scope matches proposal" | E-02 |
| "Bounded scope = short diff = fast review" | E-02 |
| "Right context, not all context" | E-03 |
