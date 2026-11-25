---
name: opro
description: "Generate prompt variations, test each against a benchmark task, and identify the best-performing variant."
---
# OPRO ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Optimization by PROmpting

Generate prompt variations, test each against a benchmark task, and identify
the best-performing variant.

## ÃƒÂ¢Ã…Â¡Ã‚Â ÃƒÂ¯Ã‚Â¸Ã‚Â Cost Warning

OPRO generates multiple prompt candidates and tests each one. The total cost
depends on the number of candidates ÃƒÆ’Ã¢â‚¬â€ benchmark tasks. **This costs many API
calls.** The user must explicitly confirm before proceeding.

## When to Use

- User invokes `/ideate-hub opro`
- User asks for "prompt optimization" or "OPRO"
- Periodic maintenance of agent prompts or skill descriptions
- **Never auto-invoke** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â always get confirmation

## Workflow

1. **Show warning** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Present the cost warning:
   > "OPRO generates prompt variations and tests each against a benchmark. This
   > costs many API calls (candidates ÃƒÆ’Ã¢â‚¬â€ benchmark tasks). Proceed? (yes/no)"

2. **On confirmation** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Identify what to optimize:
   - Which prompt or instruction set?
   - What is the goal? (clarity, completeness, conciseness, accuracy)
   - What benchmark task will test it?

3. **Generate candidates** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Create 3-5 distinct variations. Each should
   differ in meaningful ways (tone, structure, specificity, examples).

4. **Test each candidate** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Run each candidate against the benchmark task.
   For each run, measure:
   - Output quality (correctness, completeness)
   - Output length (token efficiency)
   - Number of follow-up questions needed
   - Whether acceptance criteria were met

5. **Analyze results** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Which candidate performed best? Why? What patterns
   correlate with better performance?

6. **Report** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Present the winning variation with performance data, what made
   it better, and optionally apply it if the user approves.

## Output Format

```
## OPRO Report: [Prompt Name]

### Configuration
- **Candidates tested:** 5
- **Benchmark task:** [description]
- **Evaluation criteria:** [criteria]

### Results

| Variation | Quality | Token Eff. | Follow-ups | Overall |
|-----------|---------|------------|------------|---------|
| Original  | 7/10    | 4/10       | 2          | 5/10    |
| A: [desc] | 9/10    | 7/10       | 0          | 8/10    |
| B: [desc] | 8/10    | 9/10       | 1          | 8/10    |
| C: [desc] | 6/10    | 8/10       | 3          | 5/10    |

### Winner
**Variation [X]** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â [description of the winning approach]

**Why it won:** [evidence-based analysis of what made it better]

### Apply?
[ ] Apply the winning variation? (user decides)
```

## Anti-Patterns

- **Auto-running**: Starting OPRO without user confirmation. Always warn first.
- **Minimal variations**: Changing one word and calling it a new candidate.
  Each variation should be structurally different.
- **Trivial benchmark**: Testing against a trivial task that doesn't stress
  the prompt. The benchmark should be representative of real usage.
- **Ignoring context fit**: Picking the variation with the highest score
  without checking if it still integrates well with surrounding instructions.
