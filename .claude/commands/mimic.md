# /mimic (The Clone Trooper) 👯

## Purpose

Rapidly implement new features by **replicating patterns** from existing code. This command enforces adherence to project standards by treating existing code as the "Golden Template".

**Required Skills**: `pattern-analysis`
**References**:
- `.claude/skills/methodology/pattern-analysis/SKILL.md`

## Usage

```bash
/mimic "Make Edit Loan page like Edit Savings page" --target=src/loan/edit
/mimic "Create new API endpoint for Products based on Users endpoint"
```

## Workflow

### Phase 1: PATTERN MATCH (Explorer Subagent) 🔍

**Goal**: Extract the "DNA" of the Reference Feature.

#### Subtask 1.1: Locate Reference & Source (5-10 min)

**Context**:
- Identify exactly what we are copying.
- Identify the boundaries of the feature.

**Steps**:
1. Find the files for the Reference Feature (e.g., `src/pages/savings/edit`).
2. Identify the "Root" files (Page component, Controller, etc.).
3. Identify dependencies (Components, Hooks, Utils).

**Example Output**:
```markdown
Reference Architecture:
- Entry: src/pages/SavingEdit.tsx
- Logic: src/hooks/useSavingForm.ts
- UI: src/components/SavingCard.tsx
- API: src/api/savings.ts
```

#### Subtask 1.2: Pattern Extraction (15-20 min)

**Guidance**: Use `pattern-analysis` skill.

**Steps**:
1. Analyze the Reference Files.
2. Extract **Structural Patterns**:
   - How are folders organized?
   - How are files named? (PascalCase vs kebab-case)
3. Extract **Code Patterns**:
   - Imports (What libraries are standard?)
   - State Management (Zustand? Context?)
   - Error Handling (Try/catch? Error Boundaries?)
   - Typing (DTOs? Interfaces?)

**Example Output**:
```markdown
Pattern DNA:
- **Structure**: Feature-folder architecture.
- **Form**: Uses `react-hook-form` + `zod` schema.
- **API**: Returns `Promise<ApiResponse<T>>`.
- **UI**: Uses `Tailwind` utility classes.
```

> **REVIEW GATE**: Does the DNA Report capture *structural* patterns? If it just lists files, RETRY.

---

### Phase 2: ADAPT (Analyzer Subagent) 🧬

**Goal**: Create a Blueprint for the new feature.

#### Subtask 2.1: Semantic Mapping (10 min)

**Context**:
- We need to translate "Reference Language" to "Target Language".

**Steps**:
1. Map terms from Reference -> Target.
2. Identify Business Logic differences.

**Example Output**:
```markdown
Transformation Dictionary:
- Key Term: `Saving` -> `Loan`
- Field: `interestRate` -> `loanPeriod`
- Function: `calculateYield` -> `calculateRepayment`
- API Path: `/savings` -> `/loans`
```

#### Subtask 2.2: Blueprint Generation (15-20 min)

**Context**:
- A detailed list of files to be created.

**Steps**:
1. Create a file list for the Target.
2. For each file, describe the changes required.
3. **Constraint**: Must keep the SAME folder structure and separation of concerns.

**Example Output**:
```markdown
Blueprint:
1. `src/pages/LoanEdit.tsx`:
   - Copy `SavingEdit.tsx`
   - Replace `useSavingForm` with `useLoanForm`
   - Update titles to "Edit Loan"

2. `src/hooks/useLoanForm.ts`:
   - Copy `useSavingForm.ts`
   - Update Zod schema to `LoanSchema`
   - Update default values
```

> **REVIEW GATE**: Does the Blueprint respect the Reference Architecture exactly?

---

### Phase 3: REPLICATE (Executor Subagent) 🏗️

**Goal**: Generate the new code.

#### Subtask 3.1: Skeleton Generation (10 min)

**Steps**:
1. Create directories.
2. Create empty files matching the Blueprint.
3. Verify paths.

#### Subtask 3.2: Code Generation (20-30 min)

**Steps**:
1. Generate content for each file.
2. **Technique**: "Cloning" - start with the Reference code pattern.
3. Apply the **Transformation Dictionary**.
4. **Constraint**: Ensure all imports are updated to the new context (don't import `Saving` in `Loan` file).

#### Subtask 3.3: Linting & Integrity Check (5-10 min)

**Steps**:
1. Check for "Leftovers" (e.g., forgot to rename `Saving` to `Loan` in a comment or variable).
2. Verify TypeScript compilation (if applicable).
3. Verify no unused imports.

## Success Criteria

- [ ] New feature has exact same structure as Reference.
- [ ] New feature uses same libraries/patterns.
- [ ] No "Copy-Paste" errors (leftover names).
- [ ] Compiles without errors.
