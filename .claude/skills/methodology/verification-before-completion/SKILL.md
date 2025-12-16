---
name: verification-before-completion
description: Mandatory verification process before claiming any task is complete. Enforces evidence-based completion through 5-step process: IDENTIFY command, EXECUTE fully, READ complete output, VERIFY matches claim, then CLAIM with evidence. Use when verifying tests pass, builds succeed, bugs are fixed, or marking any task complete.
---

# Verification Before Completion

## Quick Start

1. **IDENTIFY** the verification command
2. **EXECUTE** the command fully
3. **READ** complete output carefully
4. **VERIFY** output matches claim
5. **CLAIM** with specific evidence

## Instructions

### When to Use This Skill
✅ **Always before claiming**:
- Tests pass/fail
- Build succeeds/fails
- Bug is fixed
- Task is complete
- Feature is implemented

### Core Principle
**Evidence over assumptions** - Never claim without verification.

### The 5-Step Verification Process

#### Step 1: IDENTIFY
What specific command proves your claim?
```markdown
Claim: "Tests pass" → Command: npm test
Claim: "Build succeeds" → Command: npm run build
Claim: "Lint clean" → Command: npm run lint
```

#### Step 2: EXECUTE
Run the command freshly - no cached results:
```bash
npm test  # Full run, not partial
```

#### Step 3: READ
Read complete output and exit codes:
- Check exit code (0 = success)
- Note pass/fail counts
- Look for errors or warnings

#### Step 4: VERIFY
Does output match your claim?
```
Claim: "All tests pass"
Output: "42 passing, 0 failing"
Result: ✓ Verified
```

#### Step 5: CLAIM
Now make the claim with evidence:
```
✓ All tests pass (42 passing, 0 failing) - verified at [timestamp]
```

## Examples

For detailed examples, see [verification-examples.md](resources/verification-examples.md).

Quick reference:
- **Test verification**: Run `npm test`, verify zero failures
- **Build verification**: Run `npm run build`, verify exit code 0
- **Bug fix verification**: Reproduce bug, fix, verify fix works

## Required Validations

### Testing Verification
```bash
# Run full test suite
npm test

# Must verify:
- Zero failures
- Expected test count
- No unexpected skipped tests
```

### Build Verification
```bash
# Run full build
npm run build

# Must verify:
- Exit code 0
- Build artifacts created
- No build errors
```

### Bug Fix Verification
Must complete red-green cycle:
```bash
# 1. Reproduce bug
npm test -- --grep "bug scenario"  # Should fail

# 2. Apply fix

# 3. Verify fix
npm test -- --grep "bug scenario"  # Should pass
```

## Requirements Verification
Create checklist for each requirement:
```markdown
Requirements:
- [ ] Req 1: User login (Test: test_login_flow)
- [ ] Req 2: Password reset (Test: test_reset_password)
- [ ] Req 3: Session expiry (Test: test_session_timeout)
```

For detailed verification checklists, see [verification-checklists.md](resources/verification-checklists.md).

## Best Practices

### 🔍 Verification Mindset

#### Always Verify Independently
- Don't trust memory of previous runs
- Don't assume based on related successes
- Run fresh verification each time

#### Be Specific in Claims
```
Vague: "Tests should pass"
Specific: "All 156 tests pass (verified just now)"
```

#### Include Evidence
- Numbers and counts
- Exit codes
- Timestamps
- Specific outputs

### ✅ What to Verify

#### Before Claiming Tests Pass
- Run full test suite
- Check for skipped tests
- Verify test coverage if required
- Note any warnings

#### Before Claiming Build Success
- Run clean build (rm -rf dist && build)
- Check all artifacts created
- Verify no build errors
- Check bundle size if relevant

#### Before Claiming Bug Fixed
- Reproduce original failure
- Apply fix
- Verify fix works
- Check for regressions
- Run red-green cycle if possible

#### Before Claiming Task Complete
- Verify all requirements met
- Check related functionality works
- Run acceptance tests if available
- Document verification results

### 🚫 Common Anti-patterns

#### Assuming Based on Code
```markdown
❌ BAD: "I added the null check, so it should work"
✅ GOOD: "Added null check, verified by running tests - all pass"
```

#### Partial Verification
```markdown
❌ BAD: "Ran one test, it passed"
✅ GOOD: "Ran full test suite, all 156 tests pass"
```

#### Trust Without Verification
```markdown
❌ BAD: "Agent said it's fixed"
✅ GOOD: "Agent completed fix, I verified by running tests"
```

#### Vague Claims
```markdown
❌ BAD: "Done!"
✅ GOOD: "Complete: tests pass (156/156), build succeeds, requirements met"
```

## Requirements

### Prerequisites
- Access to command line/terminal
- Understanding of project's build/test processes
- Ability to interpret test results and build outputs

### Dependencies
- Test framework (Jest, Vitest, Pytest, etc.)
- Build tools (Webpack, Vite, etc.)
- Linting/formatting tools

### Tools
- Terminal with command history
- CI/CD dashboard for build status
- Test coverage reporters
- Bundle analyzers for build verification

## Common Verification Commands

### JavaScript/TypeScript
```bash
npm test          # Run tests
npm run test:coverage  # Test with coverage
npm run build      # Production build
npm run lint       # Code quality
npm run typecheck  # TypeScript checking
```

### Python
```bash
pytest            # Run tests
pytest --cov     # With coverage
python -m build   # Build package
flake8            # Linting
mypy              # Type checking
```

### General
```bash
git status        # Check changes
git diff          # Review modifications
```

## Verification Checklist

Before claiming ANY task is complete:

- [ ] Identified verification command
- [ ] Executed command fully
- [ ] Read complete output
- [ ] Verified output matches claim
- [ ] Claim includes specific evidence
- [ ] No assumptions made
- [ ] Related functionality checked

For comprehensive checklists by category, see [verification-checklists.md](resources/verification-checklists.md).