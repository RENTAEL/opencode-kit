---
name: pair
description: "Two agents collaborate on one task: the **Driver** writes code while the **Navigator** reviews in real-time, catching mistakes early. Roles are clearly separated ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the Driver focuses on implementation, the Navigator on quality, correctness, and strategic direc..."
---
# Pair Programming

Two agents collaborate on one task: the **Driver** writes code while the **Navigator** reviews in real-time, catching mistakes early. Roles are clearly separated ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the Driver focuses on implementation, the Navigator on quality, correctness, and strategic direction.

## When to Use

- Complex implementation that benefits from real-time code review
- Learning or onboarding ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the Navigator provides guidance while the Driver builds
- Critical code where mistakes are expensive (security, auth, data handling)
- Refactoring where you want a second pair of eyes on every change
- Tasks where the developer needs strategic guidance while coding

**Do not use when:**
- The task is trivial and well-understood ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â delegate to a single executor
- You need parallel execution of independent tasks ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â use `ultrawork` instead
- The task is purely research or planning ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â use `/ideation` instead
- You need a full autonomous pipeline ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â use `autopilot` instead

## Workflow

### Phase 1: Setup

1. Understand the task and break it into small, implementable steps
2. Establish the communication protocol between Driver and Navigator
3. Define the session scope and success criteria

### Phase 2: Driver Writes Code

The `@executor` (Driver) works on one small unit at a time:

1. Reads the relevant code and understands the context
2. Implements the next unit of work
3. After each change, announces what was done and waits for Navigator feedback
4. Does not proceed to the next unit until the Navigator approves

**Driver rules:**
- Work in small increments ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â one function, one component, one file at a time
- Announce each change before moving on
- Accept Navigator feedback without defensiveness
- Focus on implementation, not strategic decisions (those are the Navigator's domain)

### Phase 3: Navigator Reviews

The `@code-reviewer` (Navigator) reviews each change in real-time:

1. Reviews the code the Driver just wrote
2. Checks for:
   - Correctness ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â does the code do what it's supposed to?
   - Edge cases ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â are null, empty, error states handled?
   - Style ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â does it match project conventions?
   - Security ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â are there any obvious vulnerabilities?
   - Testability ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â is the code structured for testing?
3. Provides feedback:
   - **Approves**: "Looks good, proceed to the next unit"
   - **Requests changes**: "This needs fixing before proceeding ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â [specific issue]"
   - **Raises concern**: "This approach might cause issues later ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â consider [alternative]"

**Navigator rules:**
- Review immediately after each Driver change ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â no batching reviews
- Be specific: "Line 42: missing null check on user input" not "this needs work"
- Focus on the code, not the person
- Consider strategic direction: is this approach leading to a good overall design?
- Do not write code ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the Navigator's job is review, not implementation

### Phase 4: Fix & Iterate

1. Driver addresses Navigator feedback
2. Driver re-announces the change
3. Navigator re-reviews
4. Loop until Navigator approves
5. Proceed to the next unit of work

### Phase 5: Final Review

1. Navigator does a comprehensive review of all changes
2. Run full test suite and build
3. Verify no regressions
4. Report summary

## Role Switching (Optional)

For longer sessions, consider switching roles periodically:
- Switch every 30-60 minutes
- The Driver becomes Navigator and vice versa
- This keeps both agents engaged and brings fresh perspective

## Communication Protocol

```
Driver: "Implementing the validateEmail function. It takes a string and returns boolean."
        [writes code]
        "Done. Here's the implementation: [shows code]. Navigator, please review."

Navigator: "Looks good overall. Two things:
           1. Line 15: the regex doesn't handle international domains ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â add unicode support
           2. Line 22: missing test for empty string input
           Fix those and proceed."

Driver: "Fixed both issues. Regex updated, test added for empty string. Re-review?"
```

## Constraints

- **Strict role separation**: The Driver writes code. The Navigator reviews code. Neither does the other's job.
- **No batching**: The Navigator reviews each change immediately, not in batches at the end.
- **Small increments**: Each Driver change should be reviewable in under 2 minutes.
- **No silent approval**: The Navigator must explicitly approve each change before the Driver proceeds.
- **Respect the process**: This is slower than solo coding but produces higher quality. Do not shortcut the review cycle.

## Reminder

Driver/Navigator pair programming.
