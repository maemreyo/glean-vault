# /task-verify - Verify Task Implementation

## Purpose

Run verification tests for the current or specific task. Executes test commands defined in the plan and reports results. Does NOT modify code - only validates that implementation works correctly.

**"Trust, but verify"** - Prove your code works before marking complete.

## Aliases

```bash
/task-verify [plan-file]
/verify-task [plan-file]
/tv [plan-file]
```

## Usage

```bash
# Verify current/last executed task
/task-verify plans/multi-theme.md

# Verify specific task
/task-verify plans/feature.md --task=A.1

# Verify entire phase
/task-verify plans/feature.md --phase=A

# Run specific test types
/task-verify plans/feature.md --unit --security

# Verbose output with full test logs
/task-verify plans/feature.md --task=B.2 --verbose
```

## Arguments

- `$ARGUMENTS`: Path to implementation plan markdown file

## Flags

| Flag | Description | Example |
|------|-------------|---------|
| `--task=ID` | Verify specific task | `--task=A.1` |
| `--phase=ID` | Verify all tasks in phase | `--phase=A` |
| `--unit` | Run unit tests only | `--unit` |
| `--integration` | Run integration tests only | `--integration` |
| `--e2e` | Run E2E tests only | `--e2e` |
| `--security` | Run security scans | `--security` |
| `--verbose` | Show full test output | `--verbose` |
| `--suggest-fix` | Suggest fixes if tests fail | `--suggest-fix` |

---

## Core Philosophy

**Read-Only Validation**:
- Runs tests defined in plan
- Reports pass/fail status
- Suggests fixes (doesn't auto-fix)

**Developer Decides**:
- Shows clear error messages
- Offers fix suggestions
- Developer implements fixes manually

---

## Workflow

### Step 1: Identify Verification Target (1-2 min)

```markdown
Target Identifier

GOAL: Determine what to verify

{{ if --task provided }}
Mode: Single Task Verification
- Load task {{ task ID }}
- Extract verification command

{{ else if --phase provided }}
Mode: Phase Verification  
- Load all tasks in Phase {{ phase ID }}
- Aggregate verification commands

{{ else }}
Mode: Latest Task Verification
- Find most recently executed task
- (Last task before first [ ] or last modified file)

{{ endif }}

OUTPUT: Verification target(s)
```

---

### Step 2: Extract Verification Commands (2-3 min)

```markdown
Command Extractor

GOAL: Get test commands from plan

STEPS:

1. Read task(s) from plan

2. Extract "Verify:" section:
   ```markdown
   ### A.1: Task Name
   ...
   - **Verify**: npm test theme-security
   ```

3. Parse command type:
   {{ if contains "npm test" }}
   Type: Jest/Vitest tests
   {{ else if contains "npm run lint" }}
   Type: Linting
   {{ else if contains "npm run build" }}
   Type: Build verification
   {{ else if contains "npm run type-check" }}
   Type: TypeScript validation
   {{ endif }}

4. {{ if no verify command in plan }}
   ⚠️ WARNING: No verification command specified
   → Use default: npm test
   {{ endif }}

5. {{ if --unit or --integration or --e2e }}
   Override with specific test type:
   - --unit: npm test -- --testPathPattern=unit
   - --integration: npm test -- --testPathPattern=integration
   - --e2e: npm run test:e2e
   {{ endif }}

OUTPUT: Test command(s) to run
```

---

### Step 3: Run Verification (5-30 min depending on tests)

```markdown
Test Runner

GOAL: Execute verification commands and capture results

FOR EACH verification command:

STEP 3.1: Pre-check (1 min)

1. Verify dependencies installed:
   - Check node_modules exists
   - {{ if missing }}
     Run: npm install
   {{ endif }}

2. Check test files exist:
   - {{ if test command mentions specific file }}
     Verify file exists
   {{ endif }}

STEP 3.2: Execute Test Command (5-30 min)

1. Run command:
   ```bash
   {{ verification command }}
   ```

2. Capture:
   - Exit code (0 = pass, non-zero = fail)
   - stdout (test output)
   - stderr (error messages)
   - Duration

3. Parse results:
   {{ if Jest/Vitest }}
   - Tests passed: {{ X }}
   - Tests failed: {{ Y }}
   - Coverage: {{ Z% }}
   - Failed test names
   {{ else if TypeScript }}
   - Errors: {{ count }}
   - Warnings: {{ count }}
   - Error locations
   {{ else if ESLint }}
   - Errors: {{ count }}
   - Warnings: {{ count }}
   - Rule violations
   {{ else if Build }}
   - Success: {{ yes/no }}
   - Bundle size: {{ size }}
   - Build time: {{ duration }}
   {{ endif }}

OUTPUT: Test results per command
```

---

### Step 4: Analyze Results (2-5 min)

```markdown
Results Analyzer

GOAL: Interpret test results and identify issues

STEPS:

1. Determine overall status:
   - ✅ ALL PASSED: All tests green
   - ⚠️ PARTIAL: Some tests passed, some failed
   - ❌ ALL FAILED: All tests failed
   - 🔴 ERROR: Tests couldn't run (setup issue)

2. For failures, categorize:
   - Test assertion failures (logic bugs)
   - TypeScript errors (type issues)
   - Lint errors (code style)
   - Build errors (configuration)
   - Runtime errors (crashes)

3. Extract error details:
   - Error messages
   - Stack traces
   - File locations (file:line:col)

4. {{ if --suggest-fix }}
   Analyze common patterns:
   - Missing imports → Suggest adding import
   - Type errors → Suggest type fixes
   - Undefined variables → Suggest declaration
   - Test failures → Suggest code logic fix
   {{ endif }}

OUTPUT: Analysis report
```

---

## Output Format

### Case 1: All Tests Pass ✅

```markdown
═══════════════════════════════════════════════
✅ VERIFICATION PASSED

**Task**: {{ task ID }}: {{ description }}
{{  if --phase }}
**Phase**: {{ phase ID }} ({{ X }} tasks)
{{ endif }}
**Duration**: {{ time taken }}

═══════════════════════════════════════════════

## Test Results

{{ for each test command }}
✅ {{ command name }}
   - Tests: {{ passed }}/{{ total }}
   - Coverage: {{ coverage% }}
   - Duration: {{ duration }}
{{ endfor }}

═══════════════════════════════════════════════

## Quality Metrics

- TypeScript: ✅ No errors
- ESLint: ✅ Clean
- Build: ✅ Success ({{ bundle size }})
- Tests: ✅ {{ total }} passed

═══════════════════════════════════════════════

## Next Steps

**Mark task complete**:
```bash
/task-done {{ plan file }} --task={{ task ID }}
```

This will:
1. Mark [x] in plan
2. Git commit changes
3. Show next task

═══════════════════════════════════════════════
```

---

### Case 2: Some/All Tests Fail ❌

```markdown
═══════════════════════════════════════════════
❌ VERIFICATION FAILED

**Task**: {{ task ID }}: {{ description }}
**Duration**: {{ time taken }}
**Status**: {{ X }}/{{ Y }} checks passed

═══════════════════════════════════════════════

## Failed Checks

{{ for each failed test }}
❌ {{ test name }}
   **File**: `{{ file path }}`
   **Line**: {{ line number }}
   **Error**: {{ error message }}
   
   ```
   {{ stack trace or error context }}
   ```

{{ if --suggest-fix }}
   **Suggested Fix**:
   ```typescript
   {{ suggested code change }}
   ```
{{ endif }}

{{ endfor }}

═══════════════════════════════════════════════

{{ if --verbose }}
## Full Test Output

```
{{ complete test output }}
```
{{ endif }}

═══════════════════════════════════════════════

## Recommendations

{{ if TypeScript errors }}
1. Fix type errors:
   - Run: npx tsc --noEmit
   - Address type mismatches
{{ endif }}

{{ if test assertion failures }}
2. Fix logic bugs:
   - Review failed assertions
   - Update implementation
   - Re-run: /task-verify {{ plan file }} --task={{ task ID }}
{{ endif }}

{{ if lint errors }}
3. Fix code style:
   - Run: npm run lint --fix
   - Address remaining violations
{{ endif }}

═══════════════════════════════════════════════

## Next Steps

**Option 1: Fix manually**
1. Review errors above
2. Update code in {{ file path }}
3. Re-run: /task-verify {{ plan file }}

**Option 2: Re-implement task**
1. Run: /task-execute {{ plan file }} --task={{ task ID }}
2. Apply different approach
3. Verify again

**Option 3: Skip for now**
- Task will remain [ ] in plan
- Can return to it later

═══════════════════════════════════════════════
```

---

## Examples

### Example 1: Verify Current Task

```bash
/task-verify plans/multi-theme.md
```

Runs verification for last executed task.

### Example 2: Verify Specific Task

```bash
/task-verify plans/feature.md --task=A.1
```

Runs tests for task A.1.

### Example 3: Verify Entire Phase

```bash
/task-verify plans/feature.md --phase=A
```

Runs all verification commands for Phase A.

### Example 4: Security Scan Only

```bash
/task-verify plans/feature.md --security
```

Runs security-specific tests.

### Example 5: Verbose Output with Fix Suggestions

```bash
/task-verify plans/feature.md --task=B.2 --verbose --suggest-fix
```

---

## Integration

### Typical Workflow

```bash
# After executing task
/task-execute plan.md --task=A.1

# Verify implementation
/task-verify plan.md

# If pass, mark done
/task-done plan.md --task=A.1

# If fail, fix and re-verify
# (fix code manually)
/task-verify plan.md --task=A.1
```

### CI/CD Integration

```bash
# In CI pipeline
/task-verify plan.md --phase=A --security --verbose
exit_code=$?
```

---

## Safety Features

1. **Read-Only**: Never modifies code
2. **Clear Error Messages**: Exact file/line locations
3. **Suggestion Mode**: Offers fixes without applying
4. **Verbose Mode**: Full debug output when needed
5. **Targeted Testing**: Run only specific test types

---

## Success Criteria

- [ ] Extracts verification commands from plan
- [ ] Runs test commands correctly
- [ ] Captures and parses test output
- [ ] Reports clear pass/fail status
- [ ] Shows error details with locations
- [ ] Suggests fixes when --suggest-fix
- [ ] Handles different test frameworks

---

## Related Commands

- `/task-execute` - Implement the task
- `/task-done` - Mark complete after verification
- `/task-next` - Show next task
- `/task-progress` - Overall progress

---

## Pro Tips

1. **Always verify before marking done**:
   ```bash
   /task-execute plan.md --task=A.1
   /task-verify plan.md
   /task-done plan.md --task=A.1
   ```

2. **Use --suggest-fix for quick guidance**:
   ```bash
   /task-verify plan.md --suggest-fix
   ```

3. **Target specific test types in large projects**:
   ```bash
   /task-verify plan.md --unit  # Fast feedback
   /task-verify plan.md --e2e   # Full validation
   ```

4. **Verbose mode for debugging**:
   ```bash
   /task-verify plan.md --task=B.3 --verbose
   ```

---

**Remember**: Green tests = confidence. Always verify before moving on! ✅
