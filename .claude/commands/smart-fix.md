# /smart-fix (The Detective) 🐞

## Purpose

Intelligent, subagent-driven debugging that focuses on **Root Cause Analysis** rather than symptom fixing. It enforces a Trace-Diagnose-Prescribe-Cure workflow.

**Required Skills**: `systematic-debugging`, `root-cause-tracing`
**References**: 
- `.claude/skills/methodology/systematic-debugging/SKILL.md`
- `.claude/skills/methodology/root-cause-tracing/SKILL.md`

## Usage

```bash
/smart-fix "error message or description"
/smart-fix --logs=path/to/log.txt
```

## Core Methodology

### "Trace Backwards, Fix Forwards"

This command enforces a strict 4-phase investigative process:
1.  **TRACE**: Find where the bad data *originated*, not where it crashed.
2.  **DIAGNOSE**: Prove *why* it happened (Hypothesis testing).
3.  **PRESCRIBE**: Plan a fix that prevents recurrence (Regression Test).
4.  **CURE**: Execute and verify.

---

## Automated Workflow

### Phase 1: TRACE (Explorer Subagent) 🕵️

**Goal**: Trace the error backward to its origin.

**Context**:
- We have a symptom (e.g., "Crash at line 50").
- We need the source (e.g., "Bad input from API at line 10").

#### Subtask 1.1: Error Analysis & Environment Check (5-10 min)

**Context**:
- Understand key error details (Type, Message, Stack).
- Check relevant config files.

**Steps**:
1. Read the error message provided by user or log file.
2. Check `package.json` for relevant dependency versions.
3. Check `.env` or config files (if relevant to error).
4. **CRITICAL**: Do NOT start fixing. Just understand the crash.

**Example Output**:
```markdown
Error Analysis:
- Type: TypeError (Cannot read property 'map' of undefined)
- Location: src/components/UserList.tsx:25
- Stack: 
  - UserList.tsx:25
  - Page.tsx:40
- Environment: React 18, TypeScript 5
```

#### Subtask 1.2: Backward Tracing (15-20 min)

**Guidance**: Use the `root-cause-tracing` skill.

**Steps**:
1. Open the file where the error occurred (`UserList.tsx`).
2. Identify the variable causing the crash (`users` array is undefined).
3. **Trace BACKWARDS**:
   - Who passed `users`? -> Checked `Page.tsx`.
   - Where did `Page.tsx` get it? -> Checked `useUsers()` hook.
   - Where did `useUsers()` get it? -> API call to `/api/users`.
4. Identify the "Immediate Cause" vs "Root Source".
   - Immediate: `UserList` doesn't check for undefined.
   - Root: API returned valid JSON but missing `data` field.

**Example Output**:
```markdown
Trace Path:
1. Crash at `UserList.tsx:25` (accessing `users.map`)
2. `users` prop passed from `Page.tsx:40`
3. `Page.tsx` gets data from `useUsers.ts` hook
4. `useUsers.ts` returns `data` from Axios response
5. ⚠️ SUSPICION: API response structure changed, `data.users` is now just `data`.
```

#### Subtask 1.3: Trace Report Generation (5 min)

**Output**: A Markdown report mapping the "Path of Destruction".

> **REVIEW GATE**: Does the Trace Report identify a specific *upstream* source? If it just identifies the crash line, RETRY Subtask 1.2.

---

### Phase 2: DIAGNOSE (Analyzer Subagent) 🧠

**Goal**: Formulate and verify the Root Cause Hypothesis.

#### Subtask 2.1: Hypothesis Generation (10 min)

**Guidance**: Use `sequential-thinking` skill.

**Steps**:
1. Formulate 3 distinct hypotheses.
   - A: Code Logic (The code handles data wrong).
   - B: Data Drift (The data shape changed).
   - C: Environment (Version mismatch, config missing).
2. Rank by probability based on Trace Report.

**Example Output**:
```markdown
Hypotheses:
A. API Schema Change (High): Backend changed response format.
B. Frontend Bug (Medium): `useUsers` default value is null, not [].
C. Network Flake (Low): Request failed but wasn't caught.
```

#### Subtask 2.2: Evidence Verification (Dry Run) (10-15 min)

**Steps**:
1. Mentally "step through" the code with the suspected bad data.
2. Check for existing tests that *should* have caught this.
3. Verify if Types match Runtime reality (e.g., TS says `User[]` but runtime is `undefined`).

**Output**: Confirmed Root Cause.
"Root Cause: `useUsers` hook types the response as `User[]` but the API now returns `{ items: User[] }`. TS didn't catch it because of `as` casting."

> **REVIEW GATE**: Is the Root Cause proven with potential evidence (or strong logic)?

---

### Phase 3: PRESCRIBE (Planner Subagent) 📝

**Goal**: Plan the surgical fix and the regression test.

#### Subtask 3.1: Design The "Red" Test (10 min)

**Context**: TDD is mandatory for bug fixes. Since we can't always run full CI, we need a "reproduction case".

**Steps**:
1. Design a test case that replicates the *exact* conditions of the bug.
2. If E2E is too slow, mock the specific input (e.g., Mock the API response to return the "bad" shape).

**Example Output**:
```typescript
// Proposed Test (src/hooks/useUsers.test.ts)
it('should handle new API response shape', () => {
  mockApi.get.mockResolvedValue({ items: [] }); // Simulating new shape
  const { result } = renderHook(() => useUsers());
  expect(result.current.users).toEqual([]); // Currently fails (undefined)
});
```

#### Subtask 3.2: Design The Fix (10 min)

**Steps**:
1. Plan the fix at the **Root Source** (Update the Hook to handle new shape).
2. Plan "Defense-in-Depth" (Add optional chaining `?.` in UI).
3. **Constraints**: 
    - Do NOT break existing functionality.
    - Do NOT just wrap in `try/catch`.

---

### Phase 4: CURE (Executor Subagent) 💊

**Goal**: Apply fix and verify.

#### Subtask 4.1: The Reproduction (15 min)

**Steps**:
1. Create/Modify the test file.
2. Run the test.
3. **Verification**: It MUST fail. (If it passes, we didn't reproduce the bug).

#### Subtask 4.2: The Fix (15 min)

**Steps**:
1. Apply the planned code changes.
2. Run the test again.
3. **Verification**: It MUST pass.

#### Subtask 4.3: Regression Check (10 min)

**Steps**:
1. Run ALL related tests (e.g., `npm test src/components/UserList`).
2. Verify no side effects.

## Success Criteria

- [ ] Bug reproduced with a "Red" test.
- [ ] Fix applied at Root Cause (not just symptom).
- [ ] "Red" test turns "Green".
- [ ] No regressions in related components.
