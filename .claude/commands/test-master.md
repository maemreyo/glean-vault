# /test-master (The QA Lead) 🛡️

## Purpose

Comprehensive test generation that goes beyond happy paths. It uses an adversarial "Attacker Mindset" to fortify code, creating robust test suites that cover edge cases and error states.

**Required Skills**: `comprehensive-testing`
**References**:
- `.claude/skills/methodology/comprehensive-testing/SKILL.md`

## Usage

```bash
# Test specific target
/test-master "Cover the Salary Calculation logic" --target=src/utils/salary.ts

# Test recent changes
/test-master --recent=1                    # Last commit only
/test-master --recent=3                    # Last 3 commits
/test-master --commit=abc123               # Specific commit
/test-master --commit=abc123..def456       # Commit range
/test-master --target=src/utils/salary.ts --recent=2  # Recent changes to specific file
```

## Flags

| Flag | Description | Example |
|------|-------------|---------|
| `--target` | Specific file or directory to test | `--target=src/utils/` |
| `--recent=N` | Test changes from last N commits | `--recent=3` |
| `--commit=ID` | Test changes from specific commit | `--commit=abc123` |
| `--commit=RANGE` | Test changes from commit range | `--commit=abc123..def456` |
| `--mode` | Test generation mode (unit/integration/e2e) | `--mode=integration` |
| `--coverage` | Generate coverage reports | `--coverage` |
| `--save=PATH` | Save test plan to file | `--save=test-plan.md` |

## Workflow

### When Testing Recent Changes (--recent or --commit)

Before the standard workflow, the test-master first analyzes recent changes:

#### Pre-Phase 0: CHANGE DETECTION 🔍

**Goal**: Identify what changed and prioritize testing accordingly.

**Steps**:
1. **Git Analysis**:
   - Run `git log --oneline -N` to get commit messages
   - Run `git diff --name-only HEAD~N..HEAD` to identify changed files
   - For specific commits: `git show --name-only --format="" COMMIT_ID`

2. **Impact Assessment**:
   - Categorize changes: Business Logic, UI/UX, API, Configuration, Tests
   - Identify critical paths affected by changes
   - Detect breaking changes or risky modifications

3. **Test Prioritization**:
   ```
   Priority 1: Business Logic & API changes
   Priority 2: Database schema & security changes
   Priority 3: UI/UX changes
   Priority 4: Configuration & utility changes
   ```

**Example Output**:
```markdown
Recent Changes Analysis:
- Commits: 3 (abc123, def456, ghi789)
- Files Changed: 5 files
  - src/api/auth.js (Priority 1 - Authentication logic)
  - src/models/user.js (Priority 2 - Schema change)
  - tests/auth.test.js (Priority 1 - Test update needed)
- Risk Level: HIGH (Authentication changes)
```

### Phase 1: HUNT (Explorer Subagent) 🏹

**Goal**: Map the surface area for logic and vulnerabilities.

#### Subtask 1.1: Control Flow Analysis (10-15 min)

**Context**:
- We need to know every possible path code can take.

**Steps**:
1. Read the Target File.
2. Identify **Branching Points**: `if`, `else`, `switch`, ternary operators.
3. Identify **Looping**: `for`, `while`, `map`, `reduce`.
4. Identify **Exits**: `return`, `throw`.

**Example Output**:
```markdown
Control Flow Map:
- Function `calculateTax`:
  - Branch 1: `income < 0` (Early exit)
  - Loop: `brackets.forEach`
  - Exit: Returns number
```

#### Subtask 1.2: Input/Output & State Analysis (10 min)

**Context**:
- What goes in, what comes out, what global state is touched?

**Steps**:
1. List all arguments and their types.
2. List all implicit inputs (dependency injection, environment vars).
3. List return types.

**Example Output**:
```markdown
I/O Analysis:
- Input: `income` (number), `config` (object)
- Output: `CalculatedTax` (object) OR throws `ValidationError`
```

---

### Phase 2: ATTACK (Analyzer Subagent) ⚔️

**Goal**: Devise test scenarios to break the code.

#### Subtask 2.1: Scenario Generation (15-20 min)

**Guidance**: Use `comprehensive-testing` skill.

**For Recent Changes (--recent/--commit)**:

**Steps**:
1. **Regression Scenarios**:
   - What functionality did this change break?
   - What existing behavior must remain unchanged?
   - Test the "before" vs "after" behavior explicitly.

2. **Integration Scenarios**:
   - How does this change interact with dependent modules?
   - Test new code with existing code paths.
   - Test edge cases at integration boundaries.

3. **Breaking Change Verification**:
   - Test deprecated functionality (if applicable).
   - Verify error messages are clear for broken usage.
   - Test migration paths (if schema/API changed).

**For Standard Target (--target)**:

**Steps**:
1. **Happy Path**: Standard valid input.
2. **Edge Cases**:
   - Null/Undefined (if applicable).
   - Empty values (strings, arrays).
   - Boundaries (0, -1, MAX_SAFE_INTEGER).
3. **Type Mismatch**: (If JS/Runtime) Pass string to number.
4. **State**: Call function in invalid object state (e.g. `submit` before `init`).

**Example Output**:
```markdown
Attack Matrix (Recent Changes):
1. Scenario: Old API call -> Expect: Deprecation warning + success
2. Scenario: New API call -> Expect: Success with enhanced response
3. Scenario: Mixed old/new calls -> Expect: Consistent behavior
4. Scenario: Migration path -> Expect: Smooth upgrade

Attack Matrix (Standard):
1. Scenario: Income = -5000 -> Expect: Throw "Negative Income"
2. Scenario: Income = 0 -> Expect: Tax = 0
3. Scenario: Income = 100M -> Expect: High Bracket Calculation
4. Scenario: Config = null -> Expect: Use defaults OR Throw
```

#### Subtask 2.2: Mock Design (10 min)

**Steps**:
1. Identify external dependencies found in Phase 1.
2. Define Mock Behavior for each scenario.
   - "Mock DB returns success"
   - "Mock DB throws ConnectionError"

> **REVIEW GATE**: Do the scenarios cover at least 3 "Failure Modes" (Error paths)? If only happy paths, RETRY.

---

### Phase 3: STRATEGIZE (Planner Subagent) ♟️

**Goal**: Plan implementation details.

#### Subtask 3.1: Test Stack Selection (5 min)

**Steps**:
1. Check existing tests to determine framework (Jest/Vitest/Playwright).
2. Decide functionality tier: Unit (isolate) vs Integration (connect).

#### Subtask 3.2: Implementation Plan (10 min)

**Steps**:
1. Draft the `describe` / `it` structure.
2. Plan the setup/teardown (`beforeEach`).

---

### Phase 4: FORTIFY (Executor Subagent) 🛡️

**Goal**: Implement the test suite.

#### Subtask 4.1: Test Skeleton (5 min)

**Action**: Create test file (e.g., `src/utils/salary.test.ts`).

#### Subtask 4.2: Implementation (20-30 min)

**Steps**:
1. Write test cases for each scenario in the Matrix.
2. **Pattern**: Arrange (Mock) -> Act (Call) -> Assert (Expect).
3. **Constraint**: Ensure tests are independent (no shared state).

#### Subtask 4.3: Verification (10 min)

**Steps**:
1. Run the new tests.
2. Verify all pass.
3. (Optional) Run with `--coverage`.

## Success Criteria

### For Recent Changes (--recent/--commit)

- [ ] All changed files have corresponding tests
- [ ] Regression tests verify existing behavior
- [ ] Breaking changes are clearly tested
- [ ] Integration points with dependent modules tested
- [ ] Migration paths (if any) are tested
- [ ] Deprecation warnings work correctly

### For Standard Target (--target)

- [ ] Happy path covered.
- [ ] At least 3 Edge cases/Boundary values covered.
- [ ] At least 1 Error case covered.
- [ ] Mocks properly clean up after themselves.

## Examples

### Example 1: Testing Last Commit

```bash
/test-master --recent=1
```

**Output**:
```
Recent Changes Analysis:
- Commit: feat(auth): Add OAuth2 authentication
- Files Changed: 2 files
  - src/api/oauth.js (Priority 1 - New OAuth endpoint)
  - src/services/auth.js (Priority 1 - Authentication service)
- Risk Level: HIGH (New authentication flow)

Generated tests:
- src/api/oauth.test.ts (15 test cases)
- src/services/auth.oauth.test.ts (12 test cases)
- integration/oauth-flow.test.ts (8 test cases)
```

### Example 2: Testing Specific Commit with Coverage

```bash
/test-master --commit=abc123 --coverage --mode=integration
```

**Output**:
```
Analyzing commit: abc123 - "fix(db):修复用户查询的SQL注入漏洞"

Recent Changes Analysis:
- Files Changed: 1 file
  - src/models/user.js (Priority 1 - Security fix)
- Risk Level: CRITICAL (SQL injection fix)

Test Coverage Report:
- src/models/user.test.js: 95% coverage
- New security tests: 6 scenarios
- Regression tests: 12 scenarios
```

### Example 3: Testing Recent Changes to Specific File

```bash
/test-master --target=src/utils/validation.js --recent=3
```

**Output**:
```
Recent Changes in validation.js:
- 2 commits touched this file
- Added email validation function
- Updated phone number validation

Generated Tests:
- test/validation/email.test.ts (8 tests)
- test/validation/phone.test.ts (6 tests)
- test/validation/regression.test.ts (15 tests)
```

### Example 4: Full Commit Range Analysis

```bash
/test-master --commit=v1.0.0..v1.1.0 --save=test-plan.md
```

**Output**:
```
Analyzing release v1.0.0 to v1.1.0...

Recent Changes Summary:
- 47 commits analyzed
- 23 files changed
- 3 breaking changes detected
- 5 new features added

Test Plan saved to: test-plan.md
Priority: CRITICAL (Major release with breaking changes)
```

## Tips

1. **After Deployments**: Always run `/test-master --recent=1` after deploying to verify nothing broke
2. **Before Releases**: Use `/test-master --commit=v1.0.0..HEAD` for comprehensive release testing
3. **Security Fixes**: Combine with `--persona=security` for thorough vulnerability testing
4. **Performance Changes**: Add `--persona=performance` to test performance implications
