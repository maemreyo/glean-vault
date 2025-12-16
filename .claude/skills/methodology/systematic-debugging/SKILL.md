---
name: systematic-debugging
description: Four-phase debugging methodology: Root Cause Investigation, Pattern Analysis, Hypothesis Testing, Implementation. Core principle: "NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST". Use when debugging bug reports with unclear cause, production errors, test failures, intermittent issues, or complex multi-component failures.
---

# Systematic Debugging

## Quick Start

1. **Investigate First**: Read errors, reproduce bug, gather evidence
2. **Analyze Patterns**: Find working code, identify differences
3. **Form & Test Hypothesis**: Make specific theory, test with minimal changes
4. **Implement Fix**: Write test first, fix root cause, verify no regressions

## Instructions

### When to Use This Skill
✅ **Perfect for**:
- Bug reports with unclear cause
- Production errors without obvious source
- Tests failing unexpectedly
- Intermittent/flaky issues
- Complex multi-component failures

❌ **NOT for**:
- Simple syntax errors (fix directly)
- Missing imports (add directly)
- Clear, single-location issues

### Core Principle
**"NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST"**

Never skip straight to fixing. Always investigate first.

### Phase 1: Root Cause Investigation

#### 1.1 Read Error Messages Carefully
Document exactly:
- The full error message
- Complete stack trace with line numbers
- Variable values shown in error
- Context when error occurred

#### 1.2 Reproduce Consistently
```markdown
Steps to reproduce:
1. Open URL: [specific URL]
2. Click: [specific element]
3. Fill form with: [specific data]
4. Submit form
5. Error appears: [exact error]
```

#### 1.3 Track Recent Changes
```bash
# Check recent commits
git log --oneline -20

# Check recent deployments
git log --since="1 week ago" --author="[author]"

# Find when it last worked
git bisect start
git bisect bad HEAD
git bisect good [last-working-commit]
```

#### 1.4 Gather Evidence
- Collect relevant logs
- Check monitoring/metrics
- Review related code changes
- Note any environmental factors

#### 1.5 Add Instrumentation (if needed)
```typescript
// Add at system boundaries
console.error('[DEBUG] Phase 1 - Input:', JSON.stringify(input));
console.error('[DEBUG] Phase 1 - After validation:', JSON.stringify(validated));
console.error('[DEBUG] Phase 1 - Before database:', JSON.stringify(query));
```

### Phase 2: Pattern Analysis

#### 2.1 Find Working Code
- Look for similar functionality that works
- Check previous versions of the code
- Find reference implementations
- Review documentation

#### 2.2 Study Reference Thoroughly
- How does working version handle this case?
- What dependencies does it use?
- What assumptions does it make?
- What's the key difference?

#### 2.3 Identify Key Differences
- Configuration differences
- Data structure differences
- Environment differences
- API version differences

### Phase 3: Hypothesis Testing

#### 3.1 Form Specific Hypothesis
"Bug occurs because [specific reason] when [specific condition]"

#### 3.2 Create Minimal Test
```typescript
// Isolate the specific issue
describe('Bug hypothesis test', () => {
  it('reproduces the exact issue', () => {
    const input = { /* exact failing input */ };
    const result = functionUnderTest(input);
    expect(result).toEqual({ /* expected result */ });
  });
});
```

#### 3.3 Test Hypothesis
- Make the smallest possible change
- Verify it reproduces the issue
- If wrong, go back to Phase 2

### Phase 4: Implementation

#### 4.1 Write Test First (TDD)
```typescript
// Test that will pass after fix
it('should handle [specific case] correctly', () => {
  const result = fixedFunction(testInput);
  expect(result).toBe(expectedOutput);
});
```

#### 4.2 Fix Root Cause Only
- Fix only the root cause identified
- Don't add unnecessary changes
- Keep fix minimal and focused

#### 4.3 Verify No Regressions
- Run full test suite
- Check related functionality
- Manual verification of critical paths

## Examples

For detailed debugging examples and case studies, see [debugging-examples.md](resources/debugging-examples.md).

## Required Tools

### Debugging Tools
- Terminal for log analysis
- IDE with debugger
- Browser DevTools
- Network analysis tools

### Version Control
- git bisect for finding breaking changes
- git blame for code history
- git log for change tracking

For detailed debugging techniques and tool-specific guides, see [debugging-techniques.md](resources/debugging-techniques.md).

## Common Debugging Patterns

### Binary Search Debugging
Use git bisect to find the exact commit that introduced the bug.

### Rubber Duck Debugging
Explain the problem line by line to identify gaps in understanding.

### Divide and Conquer
Isolate components to narrow down the source of the issue.

### Working Backwards
Start from the error and trace backwards through the execution path.

## Anti-patterns to Avoid

### Fixing Without Understanding
❌ Making changes that seem to work without knowing why
✅ Always understand the root cause before fixing

### Shotgun Debugging
❌ Changing multiple things at once
✅ Make one change at a time and test

### Ignoring Error Messages
❌ Skimming over error details
✅ Read and understand every part of the error

### Assuming Instead of Testing
❌ "This should fix it"
✅ "Let me test if this fixes the actual issue"

## Debugging Checklist

### Phase 1: Investigation
- [ ] Full error message documented
- [ ] Bug can be reproduced consistently
- [ ] Recent changes identified
- [ ] Relevant evidence collected
- [ ] Instrumentation added if needed

### Phase 2: Pattern Analysis
- [ ] Working reference found
- [ ] Key differences identified
- [ ] Pattern of failure understood
- [ ] Root cause hypothesis formed

### Phase 3: Hypothesis Testing
- [ ] Specific hypothesis stated
- [ ] Minimal test created
- [ ] Hypothesis validated/invalidated
- [ ] Root cause confirmed

### Phase 4: Implementation
- [ ] Test written before fix
- [ ] Root cause fixed
- [ ] Full test suite passes
- [ ] No regressions introduced