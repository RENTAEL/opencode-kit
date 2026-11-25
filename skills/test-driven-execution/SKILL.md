---
name: test-driven-execution
description: "Enforce the rule: a feature is not done when code is written — it is done when the tests pass."
---
<!--
  TÃƒÆ’Ã…â€œRKÃƒÆ’Ã¢â‚¬Â¡E AÃƒÆ’Ã¢â‚¬Â¡IKLAMA
  ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬
  Bu skill, implementasyon kodu yazmadan ÃƒÆ’Ã‚Â¶nce "baÃƒâ€¦Ã…Â¸arÃƒâ€žÃ‚Â± kriterleri"ni ve test senaryolarÃƒâ€žÃ‚Â±nÃƒâ€žÃ‚Â±
  tanÃƒâ€žÃ‚Â±mlar. Agent, kodu belirsiz bir tanÃƒâ€žÃ‚Â±ma deÃƒâ€žÃ…Â¸il ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â somut testleri geÃƒÆ’Ã‚Â§mek iÃƒÆ’Ã‚Â§in yazar.
  KÃƒâ€žÃ‚Â±rmÃƒâ€žÃ‚Â±zÃƒâ€žÃ‚Â±ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢YeÃƒâ€¦Ã…Â¸ilÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢Refactor dÃƒÆ’Ã‚Â¶ngÃƒÆ’Ã‚Â¼sÃƒÆ’Ã‚Â¼nÃƒÆ’Ã‚Â¼ uygular. "Bence ÃƒÆ’Ã‚Â§alÃƒâ€žÃ‚Â±Ãƒâ€¦Ã…Â¸Ãƒâ€žÃ‚Â±yor" yerine "testler geÃƒÆ’Ã‚Â§iyor" der.

  NE ZAMAN: Her yeni feature veya bug fix'ten ÃƒÆ’Ã‚Â¶nce. Test spec olmadan kod yazÃƒâ€žÃ‚Â±lmaz.
  ÃƒÆ’Ã¢â‚¬Â¡IKTI:    GeÃƒÆ’Ã‚Â§en testler, coverage raporu, "Task Complete" ÃƒÆ’Ã‚Â¶zeti.
-->

# Test-Driven Execution Skill

## When to Trigger

- At the start of any feature or task from a plan
- When a bug fix is requested (test first, then fix)
- When a subagent is about to implement a module
- When "done" is ambiguous and needs a clear definition

## Philosophy

> "A feature is not done when code is written. It is done when the tests pass."

Tests written *before* code serve three purposes:
1. They force clarity on what "correct" actually means
2. They prevent the agent from drifting into over-engineering
3. They provide instant verification that the task is complete

## Step-by-Step Process

### 1. Extract Acceptance Criteria

Read the task description and extract every "must" and "should":

**Example task:** *"Add a user registration endpoint"*

Extracted criteria:
- Must accept `email`, `password`, `name` in request body
- Must return 201 on success with the created user (excluding password)
- Must return 400 if email is already registered
- Must return 422 if fields are missing or invalid
- Must hash the password before storing

### 2. Write the Test Specification

Before writing any implementation, write the tests (or test outlines):

#### For unit tests:

```javascript
describe('registerUser()', () => {
  it('creates a user with hashed password', async () => { ... })
  it('throws DuplicateEmailError if email already exists', async () => { ... })
  it('throws ValidationError if email format is invalid', async () => { ... })
  it('never stores plaintext password', async () => { ... })
})
```

#### For integration/API tests:

```javascript
describe('POST /api/auth/register', () => {
  it('returns 201 and user object (without password) on success', async () => { ... })
  it('returns 400 when email already registered', async () => { ... })
  it('returns 422 when required fields missing', async () => { ... })
})
```

#### For UI/E2E tests:

```
Scenario: Successful registration
  Given I am on the /register page
  When I fill in valid email, password, and name
  And I click "Create Account"
  Then I should be redirected to /dashboard
  And I should see "Welcome, <name>"
```

### 3. Confirm Tests Fail (Red)

Run the tests *before* writing any implementation:

```bash
npm test
# or
pytest
# etc.
```

**Expected:** All new tests fail. This confirms the tests are correctly detecting the absence of the feature. If a test passes before implementation, the test is wrong ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â fix it.

### 4. Write the Minimum Implementation (Green)

Now implement the feature. The goal is simple: **make the tests pass**.

Rules during implementation:
- Write only what is needed to pass the tests ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â nothing more
- If you find yourself writing code with no corresponding test, stop and write the test first
- Don't optimize yet ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â correctness first

```bash
# Keep running tests as you go
npm test --watch
```

### 5. Refactor (Refactor)

Once all tests pass:
- Clean up the code (naming, structure, duplication)
- Run tests again after every refactor step to confirm nothing broke
- Add edge case tests for anything discovered during implementation

### 6. Define the Done Checklist

A task is complete when:

- [ ] All acceptance criteria from Step 1 have a corresponding test
- [ ] All tests pass (`npm test` exits with code 0)
- [ ] No test is skipped (no `.skip`, `xtest`, `# noqa`)
- [ ] Code coverage for the new module is ÃƒÂ¢Ã¢â‚¬Â°Ã‚Â¥ 80% (check with `--coverage`)
- [ ] No existing tests were broken by this change

### 7. Report Completion

```
## Task Complete: <feature name>

**Tests written:** <N>
**Tests passing:** <N>/<N>
**Coverage:** <X>%
**Acceptance criteria covered:**
  ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ Creates user with hashed password
  ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ Returns 400 on duplicate email
  ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ Returns 422 on validation failure
  ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ Never stores plaintext password

**Not covered (and why):**
  ÃƒÂ¢Ã…Â¡Ã‚Â ÃƒÂ¯Ã‚Â¸Ã‚Â Email delivery test ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â skipped, requires mock SMTP setup
```

## Test Naming Convention

Test names must read as requirements:

ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ `it('returns 400 when email already exists')`
ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ `it('never exposes password in API response')`
ÃƒÂ¢Ã‚ÂÃ…â€™ `it('test email duplicate')`
ÃƒÂ¢Ã‚ÂÃ…â€™ `it('works correctly')`

If you can't name the test clearly, the requirement isn't clear enough ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â clarify before writing.

## Rules

- **No implementation before test spec.** The spec can be pseudocode / outlines, but it must exist.
- **A failing test is not a failure** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â it is a correctly written test in the red phase.
- **Never delete a test to make the suite pass.** Fix the code or fix the test ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â with justification.
- **Integration tests are not optional** for public-facing APIs.
- **Coverage % is a proxy, not a goal.** 100% coverage with meaningless assertions is worse than 70% with real ones.
