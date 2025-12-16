# /auto-plan - Intelligent Planning with Automatic Exploration

## Purpose

**Smart planning that ALWAYS explores code first**. No manual exploration needed - this command automatically runs the full workflow: explore → analyze → plan using dedicated subagents for each phase.

**Philosophy**: You can't plan well without understanding existing code. This command enforces exploration-first planning.

## Usage

```bash
# Simple - auto-detects everything
/auto-plan "salary calculator"

# Specify source directory
/auto-plan "authentication" --source=old-app/auth

# Save outputs
/auto-plan "payment flow" \
  --output=plans/payment-migration.md \
  --analysis=docs/payment-analysis.md

# Type hint for better context
/auto-plan "user dashboard" --type=react
```

## Arguments

- `$ARGUMENTS`: Feature name or description to plan (will auto-explore old implementation)

## Flags

| Flag | Description | Example |
|------|-------------|---------|
| `--source=path` | Source directory to explore | `--source=old-app/features/auth` |
| `--output=path` | Save plan to file | `--output=plans/migration.md` |
| `--analysis=path` | Save exploration analysis | `--analysis=docs/analysis.md` |
| `--type=TYPE` | Type hint: react/api/utility/component | `--type=react` |
| `--skip-review` | Skip review gates (faster, less safe) | `--skip-review` |

---

## Core Methodology

**Reference**: `.claude/skills/methodology/intelligent-planning/SKILL.md`

### "3 Fresh Subagents + Review Gates = Complete Context, Quality Plans"

This command uses **3 dedicated subagents** in sequence:

```
Subagent 1: EXPLORER → Review Gate → 
Subagent 2: ANALYZER → Review Gate → 
Subagent 3: PLANNER → Final Review → 
Complete Plan ✅
```

Each subagent:
- ✅ Fresh context (no pollution from previous phases)
- ✅ Specialized focus (exploration, analysis, or planning)
- ✅ Quality gate before proceeding
- ✅ Can be retried independently if needed

---

## Automated Workflow

Execute for: **$ARGUMENTS**

{{ if --source provided }}
**Source directory**: `$SOURCE_PATH`
{{ else }}
**Source**: Auto-detect
{{ endif }}

**Auto-Generated Paths** (if not specified):
- Folder: `docs/[feature-slug]/`
- Plan: `docs/[feature-slug]/plan.md`
- Analysis: `docs/[feature-slug]/analysis.md`

**Action**: Verify `docs/[feature-slug]/` folder exists. If not, create it.

{{ if --output provided }}
**Override Plan Path**: `$OUTPUT_PATH`
{{ endif }}
{{ if --analysis provided }}
**Override Analysis Path**: `$ANALYSIS_PATH`
{{ endif }}

---

### Phase 1: EXPLORE (Explorer Subagent) 🔍

**Dispatch fresh subagent for code exploration**

```markdown
Explorer Subagent - Detailed Workflow:

GOAL: Find and thoroughly document existing implementation of "$ARGUMENTS"

INPUT:
- Feature query: "$ARGUMENTS"
{{ if --source provided }}
- Source directory: $SOURCE_PATH
{{ else }}
- Auto-detect source
{{ endif }}
{{ if --type provided }}
- Type hint: $TYPE (react/api/utility)
{{ endif }}

---

SUBTASK 1.1: Locate Source Code (5-10min)

**Context**:
- Need to find all files related to "$ARGUMENTS"
- May be in multiple locations
- Need both implementation and supporting files

**Steps**:
1. {{ if --source provided }}
   Search in specified directory: $SOURCE_PATH
   {{ else }}
   Auto-detect using search patterns:
   - Search file names for: "$ARGUMENTS", variations
   - Search code content for: "$ARGUMENTS", related terms
   - Check common locations:
     - old-app/
     - legacy/
     - src/features/
     - app/modules/
     - Previous version directories
   {{ endif }}

2. Find all related files:
   - Main implementation files
   - Component files (if React)
   - Hook files
   - Utility/helper files
   - Type definitions
   - API clients/routes
   - Test files
   - Configuration files

3. Create file inventory:
   ```
   Main Files:
   - [path/to/main-component.tsx] (250 lines)
   - [path/to/secondary.tsx] (120 lines)
   
   Supporting Files:
   - [path/to/hooks.ts] (80 lines)
   - [path/to/types.ts] (50 lines)
   - [path/to/utils.ts] (100 lines)
   
   Tests:
   - [path/to/test.test.ts] (150 lines)
   
   API:
   - [path/to/api.ts] (60 lines)
   ```

**Expected Output**: Complete list of files to analyze

---

SUBTASK 1.2: Analyze File Structure (5-10min)

**Context**:
- Need to understand how code is organized
- Identify main entry points
- Map file relationships

**Steps**:
1. Map component/module hierarchy
2. Identify entry points (main files)
3. Note file organization pattern:
   - Feature-based?
   - Type-based?
   - Flat structure?

**Example Output**:
```
Structure:
old-app/modules/Tools/SalaryConversion/
├── index.tsx (entry point)
├── SalaryBanner/ (component)
│   └── index.tsx
├── SalaryContent/ (main logic component)
│   └── index.tsx
├── types.ts (interfaces)
├── api.ts (API client)
└── style.module.scss
```

---

SUBTASK 1.3: Extract Business Logic (15-20min)

**Context**:
- This is CRITICAL - the core functionality
- Must capture exact formulas, algorithms, rules
- Note line numbers for future reference

**Steps**:
1. For each main file, identify:
   - Calculation functions
   - Business rules
   - Validation logic
   - Constants and configuration
   - Formulas and algorithms

2. Document with line numbers:
   ```
   Business Logic Found:
   
   1. Tax Calculation (CRITICAL)
      Location: SalaryContent/index.tsx (lines 65-120)
      Formula: Progressive tax brackets
      Brackets: 7 levels (5%, 10%, 15%, 20%, 25%, 30%, 35%)
      Input: taxable income
      Output: total tax amount
      
   2. Insurance Calculation
      Location: SalaryContent/index.tsx (lines 35-50)
      Employee rates: SI 8%, HI 1.5%, UI 1%
      Employer rates: SI 17.5%, HI 3%, UI 1%
      Base: Insurance salary (may differ from gross)
      
   3. Allowance Deduction
      Location: SalaryContent/index.tsx (lines 45-48)
      Self: 11,000,000 VND/month
      Dependent: 4,400,000 VND per person
      Legal requirement (cannot change)
   ```

3. Extract constants:
   ```
   Constants:
   - TAX_BRACKETS: [exact values]
   - INSURANCE_RATES: [exact percentages]
   - ALLOWANCES: [exact amounts]
   - REGIONAL_MINIMUMS: [4 zones]
   ```

**Expected Output**: Complete business logic documentation with line references

---

SUBTASK 1.4: Analyze Data Models (10-15min)

**Context**:
- Need to understand data structures
- Interfaces, types, schemas
- Input/output formats

**Steps**:
1. Find type definitions:
   - TypeScript interfaces
   - Zod schemas
   - PropTypes
   - API request/response types

2. Document all fields:
   ```
   Data Model: ISalary
   Location: types.ts (lines 10-35)
   
   Fields:
   - gross: number (gross salary)
   - net: number (net salary)
   - social_insurance: number
   - health_insurance: number
   - unemployment_insurance: number
   - total_insurance: number
   - family_allowances: number (11M)
   - dependent_family_allowances: number (4.4M × count)
   - taxable_income: number
   - income: number (pre-tax)
   - personal_income_tax: number[] (7 brackets)
   - total_personal_income_tax: number
   - org_social_insurance: number (employer)
   - org_health_insurance: number (employer)
   - org_unemployment_insurance: number (employer)
   - total_org_payment: number (employer cost)
   ```

3. Note validation rules:
   - Min/max constraints
   - Required fields
   - Conditional logic

**Expected Output**: Complete data model documentation

---

SUBTASK 1.5: Map Dependencies (5-10min)

**Context**:
- Need to know what libraries/packages are used
- Identify integration points
- Note internal dependencies

**Steps**:
1. External dependencies (package.json):
   ```
   External:
   - react-hook-form@7.x (form handling)
   - zod@3.x (validation)
   - zustand@4.x (state management)
   - axios@1.x (HTTP client)
   ```

2. Internal dependencies:
   ```
   Internal:
   - @/components/ui/Button
   - @/components/ui/Input
   - @/lib/api/client
   - @/hooks/useAuth
   ```

3. API integrations:
   ```
   API Endpoints:
   - POST https://api-dev.finzone.vn/tools/salary
     Input: { salary, dependants, zone, type, insurance_level }
     Output: ISalary object
   ```

**Expected Output**: Complete dependency map

---

SUBTASK 1.6: Identify Technical Patterns (10-15min)

**Context**:
- How is code structured?
- What patterns are used?
- How does data flow?

**Steps**:
1. Architecture pattern:
   - Container/Presentational?
   - Feature-based organization?
   - Hooks pattern?

2. State management:
   - useState?
   - Context?
   - Zustand/Redux?
   - React Query?

3. Form handling:
   - react-hook-form?
   - Formik?
   - Manual?

4. API communication:
   - Fetch?
   - Axios?
   - React Query?
   - SWR?

5. Styling:
   - CSS Modules?
   - Tailwind?
   - Styled Components?

**Expected Output**:
```
Technical Patterns:

Architecture:
- Container/Presentational split
- SalaryContent = container (logic)
- SalaryBanner = presentational (UI)

State:
- Zustand store (useSalaryConversionStore)
- Local state for UI (useState)

Forms:
- react-hook-form for form management
- Zod for validation schemas

API:
- Axios for HTTP requests
- POST to backend for calculations
- Backend handles complex math

Styling:
- SCSS modules (style.module.scss)
```

---

SUBTASK 1.7: Analyze Test Coverage (5-10min)

**Context**:
- What tests exist?
- What's tested? What's NOT tested?
- Test frameworks/libraries used

**Steps**:
1. Find test files:
   - __tests__/ directories
   - *.test.ts(x) files
   - *.spec.ts(x) files

2. Analyze coverage:
   ```
   Tests Found:
   - SalaryContent.test.tsx (

50 lines)
     Tests: Basic rendering, form submission
     Coverage: ~23%
     
   Missing Tests:
   - Tax calculation logic
   - Insurance calculations
   - Edge cases (min/max values)
   - Regional variations
   - Error states
   ```

**Expected Output**: Test coverage assessment

---

SUBTASK 1.8: Note Issues & Improvements (5-10min)

**Context**:
- What could be better?
- Technical debt?
- TODO/FIXME comments?

**Steps**:
1. Scan for TODO/FIXME comments
2. Identify code smells:
   - Large files (>200 lines)
   - Complex functions
   - Duplicate code
   - Missing error handling
   - No TypeScript types (any)

3. Performance issues:
   - Unnecessary re-renders
   - Missing memoization
   - Large bundle size

**Expected Output**:
```
Issues Found:

⚠️  Code Quality:
   - SalaryContent/index.tsx: 250 lines (too large)
   - Missing TypeScript strict mode
   - Multiple `any` types

⚠️  Testing:
   - Only 23% coverage
   - No edge case tests
   - No integration tests

⚠️  Performance:
   - No memoization on calculations
   - Re-renders on every keystroke

TODO Comments:
   - "TODO: Add error handling for API failures"
   - "FIXME: Validate insurance salary separately"
```

---

SUBTASK 1.9: Compile Exploration Report (5min)

**Context**:
- Aggregate all findings
- Create structured report
- Ready for Analyzer subagent

**Steps**:
1. Combine all subtask outputs
2. Organize by category
3. Highlight critical items
4. Add file references

**Output Format** (return to main agent):
```markdown
📋 EXPLORATION REPORT

Feature: "$ARGUMENTS"
Source: [detected/specified path]
Files Analyzed: X files
Time: ~60-90 minutes of analysis

---

## File Inventory

Main Implementation:
- old-app/salary/SalaryContent/index.tsx (250 lines) *
- old-app/salary/SalaryBanner/index.tsx (80 lines)
- old-app/salary/types.ts (50 lines)

Supporting:
- old-app/salary/api.ts (60 lines)
- old-app/salary/validation.ts (40 lines)

Tests:
- old-app/salary/__tests__/SalaryContent.test.tsx (50 lines)
  Coverage: 23%

---

## Business Logic (CRITICAL)

1. Tax Calculation ⚠️  
   File: SalaryContent/index.tsx (lines 65-120)
   Type: Progressive 7-bracket algorithm
   Rates: 5%, 10%, 15%, 20%, 25%, 30%, 35%
   MUST PRESERVE: Exact algorithm

2. Insurance Deductions ⚠️  
   File: SalaryContent/index.tsx (lines 35-50)
   Employee: SI 8%, HI 1.5%, UI 1%
   Employer: SI 17.5%, HI 3%, UI 1%
   MUST PRESERVE: Legal rates

3. Allowances ⚠️  
   File: SalaryContent/index.tsx (lines 45-48)
   Self: 11,000,000 VND
   Dependent: 4,400,000 VND each
   MUST PRESERVE: Legal amounts

[... complete business logic ...]

---

## Data Models

ISalary Interface:
[complete type definition]

---

## Technical Patterns

Architecture: Container/Presentational
State: Zustand
Forms: react-hook-form + zod
API: Axios → Backend calculation
Styling: SCSS Modules

---

## Dependencies

External: react-hook-form, zod, zustand, axios
Internal: @/components/ui, @/lib/api
API: POST https://api-dev.finzone.vn/tools/salary

---

## Test Coverage

Current: 23%
Tests: Basic rendering only
Missing: Logic tests, edge cases, integration

---

## Issues & Improvements

Code Quality: Large files, missing types
Testing: Low coverage
Performance: No memoization
TODOs: 3 found

---

## Critical Files for Migration

Must reference during planning:
1. SalaryContent/index.tsx (all business logic)
2. types.ts (data models)
3. api.ts (API integration)

---

EXPLORATION COMPLETE ✅
Ready for Analysis Phase
```
```

**Return**: Complete exploration report to main agent

---

**Review Gate 1**: Check Exploration Completeness

```markdown
{{ if not --skip-review }}
Review Exploration:
✅ Core business logic found and documented?
✅ Data models identified?
✅ Dependencies clear?
✅ Edge cases noted?
✅ Integration points mapped?

{{ if incomplete }}
  → Re-dispatch Explorer with refined query
  → Specify additional directories
{{ else }}
  → Proceed to Analysis Phase ✅
{{ endif }}
{{ else }}
  → Proceed to Analysis Phase (review skipped)
{{ endif }}
```

---

### Phase 2: ANALYZE (Analyzer Subagent) 📊

**Dispatch fresh subagent for requirement extraction**

```markdown
Analyzer Subagent - Detailed Workflow:

GOAL: Extract actionable requirements and patterns from exploration report

INPUT:
- Exploration Report from Explorer Subagent (Phase 1)
- Contains: File inventory, business logic, data models, patterns, dependencies

---

SUBTASK 2.1: Extract Core Requirements (15-20min)

**Context**:
- Need to convert exploration findings into clear requirements
- Focus on WHAT must be implemented, not HOW
- Prioritize by criticality

**Steps**:
1. Read exploration report thoroughly
2. For each business logic item, create requirement:
   ```
   From Exploration:
   "Tax Calculation: 7 progressive brackets (5%-35%)"
   
   → Requirement:
   REQ-1: Tax Calculation Engine
   Priority: CRITICAL
   Type: Business Logic
   Description: System must calculate personal income tax using 7 progressive brackets
   Details:
   - Bracket 1: 0-5M VND @ 5%
   - Bracket 2: 5M-10M @ 10%
   - Bracket 3: 10M-18M @ 15%
   - Bracket 4: 18M-32M @ 20%
   - Bracket 5: 32M-52M @ 25%
   - Bracket 6: 52M-80M @ 30%
   - Bracket 7: >80M @ 35%
   Source: old-app/salary/SalaryContent/index.tsx:65-120
   Verification: Outputs must match old system exactly
   ```

3. Categorize requirements:
   - CRITICAL (🔴): Business logic, legal requirements
   - IMPORTANT (🟡): Core features, user experience
   - NICE-TO-HAVE (🟢): Enhancements, optimizations

**Expected Output**:
```markdown
Requirements Extracted:

🔴 CRITICAL Requirements:

REQ-1: Tax Calculation Engine
- 7 progressive tax brackets
- Must return identical results to old system
- Source: SalaryContent/index.tsx:65-120

REQ-2: Insurance Deduction Calculation
- Employee: SI 8%, HI 1.5%, UI 1%
- Employer: SI 17.5%, HI 3%, UI 1%
- Configurable insurance salary base
- Source: SalaryContent/index.tsx:35-50

REQ-3: Allowance Deductions
- Self: 11,000,000 VND/month
- Dependent: 4,400,000 VND/person/month
- Legal requirement (cannot change values)
- Source: SalaryContent/index.tsx:45-48

REQ-4: Regional Minimum Validation
- 4 regional zones with different minimums
- Zone I: 4,680,000 | II: 4,160,000
- Zone III: 3,640,000 | IV: 3,250,000
- Source: validation.ts

🟡 IMPORTANT Requirements:

REQ-5: Gross ↔ Net Conversion
- Bidirectional calculation
- Gross → Net (forward)
- Net → Gross (iterative reverse calculation)

REQ-6: Detailed Breakdown Display
- Show all deduction line items
- Employee vs Employer costs
- Tax bracket breakdown

REQ-7: Input Validation
- Salary range: 1M - 1B VND
- Dependents: 0-10
- Required fields validation

🟢 NICE-TO-HAVE:

REQ-8: Real-time Calculation
- Calculate as user types
- Debounced input

REQ-9: Comparison View
- Show before/after scenarios
- Multiple calculation comparison
```

---

SUBTASK 2.2: Identify Preservation Requirements (10-15min)

**Context**:
- CRITICAL: Determine what MUST NOT change
- Business logic, legal requirements, expected behaviors
- Mark for special attention in planning

**Steps**:
1. Review critical business logic from exploration
2. Mark items that must preserve exact behavior:
   ```
   MUST PRESERVE:
   
   1. Tax Bracket Values
      Values: [5M@5%, 10M@10%, 18M@15%, 32M@20%, 52M@25%, 80M@30%, ∞@35%]
      Reason: Legal requirement (Vietnamese tax law)
      Source: SalaryContent/index.tsx:65-73
      Verification: Test against known outputs
      Impact if wrong: Incorrect tax calculations, legal issues
   
   2. Insurance Rates
      Employee: SI 8%, HI 1.5%, UI 1%
      Employer: SI 17.5%, HI 3%, UI 1%
      Reason: Legal requirement (Social insurance law)
      Source: SalaryContent/index.tsx:35-40
      Verification: Match exact percentages
      Impact if wrong: Incorrect deductions, compliance violation
   
   3. Allowance Amounts
      Self: 11,000,000 VND
      Dependent: 4,400,000 VND
      Reason: Legal requirement (updated annually by law)
      Source: SalaryContent/index.tsx:45-48
      Verification: Use 2024 legal values
      Impact if wrong: Incorrect taxable income
   
   4. Progressive Tax Algorithm
      Formula: Calculate each bracket separately, accumulate
      Reason: Legal requirement for tax calculation method
      Source: SalaryContent/index.tsx:65-120
      Verification: Compare outputs with old system
      Impact if wrong: All high-income tax calculations wrong
   ```

3. Document verification approach:
   - Unit tests with known inputs/outputs
   - Comparison with old system
   - Test cases for each bracket/rule

**Expected Output**:
```markdown
PRESERVATION REQUIREMENTS:

Critical Items (MUST NOT CHANGE):

1. Tax Brackets ⚠️  
   - Values are legal requirements
   - Test: All 7 brackets with edge cases
   - Verify: Output matches old system exactly

2. Insurance Rates ⚠️  
   - Percentages mandated by law
   - Test: Employee and employer calculations
   - Verify: Deductions match old system

3. Allowances ⚠️  
   - Legal values for 2024
   - Test: Self + dependent calculations
   - Verify: Amounts match exactly

4. Calculation Algorithm ⚠️  
   - Progressive tax method required
   - Test: Multiple income levels
   - Verify: Results identical to old system

Verification Strategy:
- Create test suite with 20+ known scenarios
- Compare all outputs with old system
- Test edge cases (min salary, max brackets)
- Verify rounding behavior matches
```

---

SUBTASK 2.3: Analyze Technical Patterns & Architecture (10-15min)

**Context**:
- Need to understand HOW old system was built
- Identify patterns to replicate or improve
- Not exact code, but architectural approach

**Steps**:
1. Review technical patterns from exploration
2. Analyze architecture decisions:
   ```
   Architecture Analysis:
   
   Component Structure:
   - Pattern: Container/Presentational
   - Container (SalaryContent): Handles logic, state, API
   - Presentational (SalaryBanner): Pure UI display
   - Assessment: ✅ Good separation, replicate this
   
   State Management:
   - Pattern: Zustand store
   - Usage: Global salary calculation state
   - Assessment: ✅ Appropriate for this use case
   - Decision: Keep Zustand or migrate to React Query?
   
   Form Handling:
   - Pattern: react-hook-form + zod
   - Validation: Schema-based with zod
   - Assessment: ✅ Modern best practice
   - Decision: Keep this pattern
   
   API Communication:
   - Pattern: Backend calculation
   - Rationale: Complex math server-side
   - Assessment: ✅ Appropriate (reduces client complexity)
   - Decision: Keep backend calculation
   
   Data Flow:
   User Input → Validation → API → State Update → UI
   Assessment: ✅ Clear, unidirectional
   Decision: Preserve this flow
   ```

3. Identify patterns to KEEP vs IMPROVE:
   ```
   KEEP (Good patterns):
   - Container/Presentational split
   - Backend calculation approach
   - react-hook-form + zod validation
   - Detailed breakdown display
   
   IMPROVE (Technical debt):
   - Split large SalaryContent component
   - Add strict TypeScript types
   - Improve test coverage
   - Add error boundaries
   - Add loading states
   ```

**Expected Output**:
```markdown
Technical Pattern Analysis:

Architecture:
✅ KEEP: Container/Presentational pattern
✅ KEEP: Feature-based file organization
✅ KEEP: Backend calculation approach

State Management:
✅ KEEP: Zustand store pattern
⚠️  CONSIDER: React Query for server state?

Forms:
✅ KEEP: react-hook-form + zod
✅ KEEP: Schema-based validation

API:
✅ KEEP: POST to backend for calculation
✅ KEEP: Backend handles complex math

Data Flow:
✅ KEEP: Input → Validate → API → State → UI
✅ KEEP: Unidirectional flow

Component Design:
⚠️  IMPROVE: Split large components
✅ KEEP: Breakdown display pattern
⚠️  IMPROVE: Add loading/error states

Type Safety:
⚠️  IMPROVE: Enable strict TypeScript
⚠️  IMPROVE: Remove `any` types
✅ KEEP: ISalary interface structure

Testing:
❌ IMPROVE: Increase coverage (23% → 80%+)
❌ ADD: Unit tests for calculations
❌ ADD: Integration tests for flow

Recommended Approach:
- Preserve proven patterns
- Improve technical debt areas
- Add missing features (tests, types, error handling)
```

---

SUBTASK 2.4: Map Data Flow & Integration Points (10min)

**Context**:
- How does data move through the system?
- What are integration points?
- Where are external dependencies?

**Steps**:
1. Trace data flow from exploration:
   ```
   Data Flow Map:
   
   1. User Input Phase:
      Component: SalaryContent (form)
      Data: { salary, dependents, zone, type, insurance_level }
      Validation: Zod schema (client-side)
      State: Local form state (react-hook-form)
   
   2. Submission Phase:
      Trigger: Form submit
      Action: API call preparation
      Data transform: Form values → API payload
   
   3. API Phase:
      Endpoint: POST /tools/salary
      Payload: { salary, dependants, zone, type, insurance_level }
      Backend: Complex calculation server-side
      Response: ISalary object (all calculated values)
   
   4. State Update Phase:
      Store: Zustand useSalaryConversionStore
      Action: Update with API response
      State: salary calculation result
   
   5. Display Phase:
      Component: Result breakdown display
      Data: From Zustand store
      Rendering: Detailed line items
   ```

2. Identify integration points:
   ```
   Integration Points:
   
   External:
   - API: https://api-dev.finzone.vn/tools/salary
   - Libraries: react-hook-form, zod, zustand, axios
   
   Internal:
   - UI Components: @/components/ui (Button, Input)
   - API Client: @/lib/api
   - Type Definitions: @/types
   
   Browser APIs:
   - LocalStorage: (if storing preferences)
   - Clipboard: (if copy feature exists)
   ```

**Expected Output**:
```markdown
Data Flow Analysis:

Flow Stages:
1. Input → 2. Validate → 3. API → 4. State → 5. Display

Detailed Flow:
User types salary
  ↓ (react-hook-form)
Form state updated
  ↓ (zod validation)
Client-side validation
  ↓ (on submit)
API POST request
  ↓ (backend calculation)
Server calculates taxes, insurance, etc
  ↓ (response)
ISalary object returned
  ↓ (zustand action)
Store updated
  ↓ (React re-render)
UI displays breakdown

Integration Points:
- API: Backend calculation service
- UI Library: shadcn/ui components
- Form: react-hook-form + zod
- State: Zustand store

External Dependencies:
- API endpoint (must be available)
- Backend calculation logic (separate service)

Migration Considerations:
- Preserve API contract
- Keep data flow unidirectional
- Maintain state management approach
- Update UI components to new library
```

---

SUBTASK 2.5: Identify Gaps & Improvements (5-10min)

**Context**:
- What's missing from old implementation?
- What should we add/improve?
- Balance preservation with enhancement

**Steps**:
1. Review issues from exploration
2. Categorize improvements:
   ```
   Improvements Needed:
   
   Testing (HIGH PRIORITY):
   - Current: 23% coverage
   - Target: 80%+ coverage
   - Add: Unit tests for all calculations
   - Add: Integration tests for full flow
   - Add: Edge case testing
   
   Code Quality (MEDIUM):
   - Split SalaryContent.tsx (250 lines → 50-80 line components)
   - Enable TypeScript strict mode
   - Remove all `any` types
   - Add JSDoc comments
   
   Error Handling (MEDIUM):
   - Add error boundaries
   - Better API error handling
   - User-friendly error messages
   - Retry logic for API failures
   
   UX Improvements (LOW):
   - Loading states during calculation
   - Skeleton loaders
   - Debounced input
   - Better form feedback
   
   Accessibility (MEDIUM):
   - ARIA labels
   - Keyboard navigation
   - Screen reader support
   - Focus management
   
   Performance (LOW):
   - Memoize complex calculations
   - Optimize re-renders
   - Code splitting
   ```

**Expected Output**:
```markdown
Gap Analysis & Improvements:

Must Add (Missing Features):
1. Comprehensive test suite
   - Current: 23% coverage, basic only
   - Need: 80%+ with edge cases
   - Tests for each tax bracket
   - Tests for insurance calculations
   - Integration tests for full flow

2. Error Handling
   - API error handling
   - Validation error display
   - Error boundaries
   - Retry mechanisms

3. Loading States
   - Show during API calls
   - Disable form during calculation
   - Skeleton loaders

4. Accessibility
   - ARIA labels on all inputs
   - Keyboard navigation
   - Screen reader support

Should Improve (Technical Debt):
1. Component Size
   - SalaryContent: 250 lines → split
   - Extract calculation logic
   - Separate form from display

2. Type Safety
   - Enable TypeScript strict
   - Remove `any` types
   - Add stricter type guards

3. Code Organization
   - Extract hooks
   - Separate utilities
   - Better file structure

Nice to Have (Enhancements):
1. Performance
   - Memoize calculations
   - Debounce input
   - Code splitting

2. UX
   - Real-time calculation
   - Comparison mode
   - Export results

Priority Order:
1. Testing (enables safe refactoring)
2. Error handling (production readiness)
3. Type safety (maintainability)
4. Component splitting (readability)
5. Accessibility (inclusive design)
6. Performance (user experience)
```

---

SUBTASK 2.6: Create Migration Strategy (10min)

**Context**:
- How to migrate safely?
- What order makes sense?
- Balance risk vs value

**Steps**:
1. Determine migration approach:
   ```
   Migration Strategy:
   
   Approach: Incremental replacement
   Reason: Large component, high risk
   
   Phase 1: Foundation
   - Create type definitions
   - Extract constants (tax brackets, rates)
   - Set up utilities
   - Risk: Low
   - Value: Enables all other work
   
   Phase 2: Core Logic
   - Tax calculation function
   - Insurance calculation
   - Allowance calculation
   - Risk: High (critical business logic)
   - Value: High (core functionality)
   - Strategy: Test-heavy, verify against old system
   
   Phase 3: Components
   - Form component
   - Display component
   - Layout component
   - Risk: Medium
   - Value: Medium
   - Strategy: Reuse patterns from old system
   
   Phase 4: Integration
   - API integration
   - State management
   - Navigation/routing
   - Risk: Medium
   - Value: High (brings it all together)
   
   Phase 5: Testing
   - Unit tests
   - Integration tests
   - E2E tests
   - Risk: Low
   - Value: High (safety net)
   
   Phase 6: Polish
   - Accessibility
   - Performance
   - Error handling
   - Risk: Low
   - Value: Medium
   ```

2. Identify dependencies:
   - Phase 1 → Phase 2 (need types and constants)
   - Phase 2 → Phase 3 (need logic before UI)
   - Phase 3 → Phase 4 (need components to integrate)
   - All → Phase 5 (tests need implementation)
   - All → Phase 6 (polish needs complete feature)

**Expected Output**:
```markdown
Migration Strategy:

Approach: Incremental, test-driven migration

Phases:
1. Foundation (low risk, high value)
2. Core Logic (high risk, high value) ← TEST HEAVILY
3. Components (medium risk, medium value)
4. Integration (medium risk, high value)
5. Testing (low risk, high value)
6. Polish (low risk, medium value)

Risk Mitigation:
- Test core logic against old system outputs
- Incremental integration
- Feature flags for rollout
- Parallel running (old + new) initially

Success Criteria:
- All calculations match old system
- 80%+ test coverage
- No regressions
- Performance maintained or better
- Accessibility improved

Timeline Estimate:
- Foundation: 45 min
- Core Logic: 2 hours (includes extensive testing)
- Components: 1.5 hours
- Integration: 1 hour
- Testing: 1 hour
- Polish: 45 min
Total: 6-8 hours
```

---

SUBTASK 2.7: Compile Analysis Report (5min)

**Context**:
- Aggregate all analysis findings
- Create structured report for Planner
- Highlight critical items

**Steps**:
1. Combine all subtask outputs
2. Organize by priority
3. Add actionable recommendations

**Output Format** (return to main agent):
```markdown
📊 ANALYSIS REPORT

Feature: "$ARGUMENTS"
Based on: Exploration Report
Time: ~60-80 minutes of analysis

---

## Requirements Summary

Total Requirements: 9 (4 Critical, 3 Important, 2 Nice-to-have)

🔴 CRITICAL (4):
1. Tax Calculation Engine (7 brackets)
2. Insurance Deduction Calculation
3. Allowance Deductions
4. Regional Minimum Validation

🟡 IMPORTANT (3):
5. Gross ↔ Net Conversion
6. Detailed Breakdown Display
7. Input Validation

🟢 NICE-TO-HAVE (2):
8. Real-time Calculation
9. Comparison View

---

## Preservation Requirements ⚠️  

MUST PRESERVE (CRITICAL):

1. Tax Bracket Values
   - 7 levels: 5%, 10%, 15%, 20%, 25%, 30%, 35%
   - Legal requirement
   - Source: SalaryContent/index.tsx:65-73
   - Verification: Match old system outputs exactly

2. Insurance Rates
   - Employee: 8%, 1.5%, 1% (total 10.5%)
   - Employer: 17.5%, 3%, 1% (total 21.5%)
   - Legal requirement
   - Source: SalaryContent/index.tsx:35-40

3. Allowance Amounts
   - Self: 11,000,000 VND
   - Dependent: 4,400,000 VND
   - Legal requirement
   - Source: SalaryContent/index.tsx:45-48

4. Progressive Tax Algorithm
   - Calculate each bracket separately
   - Accumulate total tax
   - Source: SalaryContent/index.tsx:65-120

---

## Technical Patterns

KEEP (Proven patterns):
✅ Container/Presentational architecture
✅ Backend calculation approach
✅ react-hook-form + zod validation
✅ Zustand state management
✅ Detailed breakdown display

IMPROVE (Technical debt):
⚠️  Split large components (250 lines → 50-80)
⚠️  Add strict TypeScript
⚠️  Increase test coverage (23% → 80%+)
⚠️  Add error handling
⚠️  Add loading states

---

## Data Flow

Input → Validate → API → State → Display

Integration Points:
- API: Backend calculation service
- UI: shadcn/ui components
- State: Zustand store
- Forms: react-hook-form + zod

---

## Gap Analysis

Must Add:
1. Comprehensive tests (priority 1)
2. Error handling (priority 2)
3. Loading states
4. Accessibility features

Should Improve:
1. Component organization
2. Type safety
3. Code structure

---

## Migration Strategy

Approach: Incremental, test-driven

Phases:
1. Foundation (types, constants)
2. Core Logic (calculations) ← TEST HEAVILY
3. Components (UI)
4. Integration (API, state)
5. Testing (comprehensive)
6. Polish (a11y, performance)

Estimate: 6-8 hours
Risk: Medium
Confidence: High

---

## Recommendations for Planning

1. **Start with Foundation**
   - Create types first
   - Extract constants
   - Set up structure

2. **Test Core Logic Extensively**
   - Write tests BEFORE implementing
   - Compare outputs with old system
   - Cover all edge cases

3. **Preserve Critical Business Logic**
   - Copy exact values (tax brackets, rates)
   - Verify algorithm matches
   - Document preservation items

4. **Improve Incrementally**
   - Fix technical debt while migrating
   - Add missing tests
   - Improve types and structure

5. **Verify Continuously**
   - Test against old system throughout
   - Check calculations match
   - Ensure no regressions

---

ANALYSIS COMPLETE ✅
Ready for Planning Phase
```
```

**Return**: Complete analysis report to main agent

---

**Review Gate 2**: Check Analysis Clarity

```markdown
{{ if not --skip-review }}
Review Analysis:
✅ All business rules extracted?
✅ Preservation items clearly marked?
✅ Patterns identified?
✅ No ambiguous requirements?

{{ if unclear or incomplete }}
  {{ if user input needed }}
    → Pause and ask user for clarification
  {{ else }}
    → Re-dispatch Analyzer with refined focus
  {{ endif }}
{{ else }}
  → Proceed to Planning Phase ✅
{{ endif }}
{{ else }}
  → Proceed to Planning Phase (review skipped)
{{ endif }}
```

---

### Phase 3: PLAN (Planner Subagent) 📋

**Dispatch fresh subagent for detailed plan generation**

```markdown
Planner Subagent - Detailed Workflow:

GOAL: Generate execution-ready migration plan with TDD micro-tasks

INPUT:
- Analysis Report from Analyzer Subagent (Phase 2)
- Exploration Report from Explorer Subagent (Phase 1)
- Contains: Requirements, preservation items, patterns, migration strategy

---

SUBTASK 3.1: Design Plan Structure (10-15min)

**Context**:
- Need to organize work into logical phases
- Follow dependency order (types before logic, logic before UI)
- Align with migration strategy from analysis

**Steps**:
1. Review migration strategy from analysis
2. Create phase structure:
   ```
   Phase 1: Foundation & Setup
   - Why first: Enables all other work
   - What: Types, constants, utilities, project structure
   - Risk: Low
   - Duration: 30-60 min
   
   Phase 2: Core Business Logic
   - Why here: Critical functionality, needs heavy testing
   - What: Tax calculation, insurance, allowances, validation
   - Risk: HIGH (business logic)
   - Duration: 2-3 hours
   - Special: Test against old system extensively
   
   Phase 3: UI Components
   - Why after logic: Needs working logic to test against
   - What: Form components, display components, layout
   - Risk: Medium
   - Duration: 1-2 hours
   
   Phase 4: Integration
   - Why here: Brings everything together
   - What: API client, state management, routing
   - Risk: Medium
   - Duration: 1 hour
   
   Phase 5: Comprehensive Testing
   - Why near end: Needs implemented features
   - What: Unit tests, integration tests, E2E
   - Risk: Low
   - Duration: 1-1.5 hours
   
   Phase 6: Polish & Production Ready
   - Why last: Nice-to-haves, enhancements
   - What: Accessibility, performance, error handling, docs
   - Risk: Low
   - Duration: 30-60 min
   ```

3. Note dependencies:
   - Phase 1 → Phase 2 (need types for logic)
   - Phase 2 → Phase 3 (need logic for UI)
   - Phase 3 → Phase 4 (need components for integration)
   - All → Phase 5 (need implementation for testing)

**Expected Output**:
```markdown
Plan Structure:

6 Phases (sequential):
1. Foundation (45min) - Types, constants, utils
2. Core Logic (2h) - Calculations ← HIGH RISK, HEAVY TESTING
3. Components (1.5h) - UI implementation
4. Integration (1h) - API, state, routing
5. Testing (1h) - Comprehensive test suite
6. Polish (45min) - A11y, performance, docs

Total Estimate: 6-8 hours
```

---

SUBTASK 3.2: Generate Foundation Phase Tasks (15-20min)

**Context**:
- Foundation = types, constants, utilities
- Must reference old code for exact values
- Enable all subsequent work

**Steps**:
1. For each requirement from analysis, create foundation tasks
2. Use TDD micro-task format (from analysis):
   ```
   Task Format:
   - File: Explicit path
   - Context: Reference to old code (file + lines)
   - Strategy: How to approach (not exact code)
   - Acceptance Criteria: Checkboxes
   - PRESERVE: Critical items from analysis
   - Expected: Test result
   - Time: 5-15 min per task
   ```

3. Example tasks:
   ```
   Task 1.1: Create ISalary Interface
   File: src/types/salary.ts
   Context: Old interface at old-app/salary/types.ts:10-35
   Strategy:
   1. Read old ISalary interface
   2. Copy all field definitions
   3. Add strict TypeScript types (no any)
   4. Add JSDoc comments for complex fields
   Acceptance:
   - [ ] All fields from old interface present
   - [ ] Strict types (no any)
   - [ ] JSDoc on all fields
   - [ ] Compiles without errors
   Expected: ✅ TypeScript compile success
   Time: 10 min
   
   Task 1.2: Define Tax Bracket Constants
   File: src/lib/salary/constants.ts
   Context: Tax logic at old-app/salary/SalaryContent/index.tsx:65-73
   ⚠️  MUST PRESERVE:
   Tax bracket values are LEGAL REQUIREMENTS
   - Bracket 1: 0-5M @ 5%
   - Bracket 2: 5M-10M @ 10%
   - Bracket 3: 10M-18M @ 15%
   - Bracket 4: 18M-32M @ 20%
   - Bracket 5: 32M-52M @ 25%
   - Bracket 6: 52M-80M @ 30%
   - Bracket 7: >80M @ 35%
   Source: SalaryContent/index.tsx:65-73
   Strategy:
   1. Create constants file
   2. Copy EXACT values from old code
   3. Add TypeScript `as const` assertion
   4. Export for use in calculator
   5. Write test to verify values match old system
   Acceptance:
   - [ ] 7 brackets defined
   - [ ] Values match old system exactly
   - [ ] TypeScript const assertion
   - [ ] Test passes
   Expected: ✅ Values verified against old code
   Time: 15 min
   ```

**Expected Output**:
```markdown
Phase 1: Foundation & Types [45 min]

Task 1.1: Create ISalary Interface (10m)
[Full task details with context, strategy, PRESERVE notes]

Task 1.2: Define Tax Bracket Constants (15m)
[Full task details...]

Task 1.3: Define Insurance Rate Constants (10m)
[Full task details...]

Task 1.4: Define Allowance Constants (5m)
[Full task details...]

Task 1.5: Create Regional Zone Constants (5m)
[Full task details...]
```

---

SUBTASK 3.3: Generate Core Logic Phase Tasks (20-30min)

**Context**:
- CRITICAL phase - business logic calculations
- Must preserve exact behavior from old system
- HEAVY testing required
- Reference preservation items from analysis

**Steps**:
1. For each critical requirement, create test-first tasks
2. Each calculation function gets multiple tasks:
   - Test task (write failing test)
   - Implementation task (make test pass)
   - Additional tests (edge cases)
   - Verification against old system

3. Mark preservation items explicitly

**Example Output**:
```markdown
Phase 2: Core Business Logic [2 hours]

⚠️  CRITICAL PHASE: Business logic must match old system exactly

Task 2.1: Test - Tax Calculation Basic (10m)
File: src/lib/salary/__tests__/calculate-tax.test.ts
Context: Test against known outputs from old system
Strategy:
1. Create test file
2. Write test cases with known inputs/outputs:
   - Input: 6,900,000 VND taxable income
   - Expected: 440,000 VND tax
   - Breakdown: (5M × 5%) + (1.9M × 10%) = 250k + 190k
3. Run test → ❌ Expected to fail (no implementation yet)
Acceptance:
- [ ] Test file created
- [ ] At least 3 test cases
- [ ] Tests fail (function doesn't exist)
Expected: ❌ Tests fail (expected)
Time: 10 min

Task 2.2: Implement - Tax Calculation Function (30m)
File: src/lib/salary/calculate-tax.ts
Context: Algorithm from old-app/salary/SalaryContent/index.tsx:65-120
⚠️  MUST PRESERVE:
- Progressive tax algorithm
- Bracket-by-bracket calculation
- Exact rounding behavior (if any)
Strategy:
1. Study old calculateTax function carefully
2. Understand progressive algorithm:
   - For each bracket, calculate tax on amount in that bracket
   - Accumulate total
   - Handle edge cases (0 income, max brackets)
3. Implement same algorithm (not exact code, same logic)
4. Run tests → ✅ Should pass
Acceptance:
- [ ] Function implemented
- [ ] All brackets handled correctly
- [ ] Tests pass
- [ ] Outputs match old system
- [ ] Pure function (no side effects)
Expected: ✅ All tests pass
Time: 30 min

Task 2.3: Test - Tax Calculation Edge Cases (15m)
File: src/lib/salary/__tests__/calculate-tax.test.ts
Context: Cover all brackets and edge cases
Strategy:
1. Add tests for:
   - Zero income → 0 tax
   - Exactly on bracket boundary (5M, 10M, etc.)
   -  Each bracket individually
   - Very high income (uses bracket 7)
   - Negative input (should error or return 0)
2. Run tests
Acceptance:
- [ ] Edge case tests added
- [ ] All 7 brackets tested
- [ ] All tests pass
Expected: ✅ Tests pass
Time: 15 min

Task 2.4: Verify Against Old System (10m)
File: src/lib/salary/__tests__/calculate-tax.test.ts
Context: Final verification with 10+ scenarios from old system
Strategy:
1. Run old system with 10+ different inputs
2. Record outputs
3. Add tests with same inputs
4. Verify outputs match EXACTLY
Acceptance:
- [ ] 10+ verification tests
- [ ] All outputs match old system
- [ ] Edge cases verified
Expected: ✅ 100% match with old system
Time: 10 min

[Repeat pattern for Insurance, Allowances, Regional validation...]
```

---

SUBTASK 3.4: Generate Component Phase Tasks (15-20min)

**Context**:
- UI implementation
- Follow patterns from old system
- Use new component library (if specified)

**Expected Output Summary**:
```markdown
Phase 3: Components [1.5 hours]

Component-based task groups:

Group 1: Form Component (45m)
- Task 3.1: Test - Form Rendering
- Task 3.2: Implement - Form Component
- Task 3.3: Test - Form Validation
- Task 3.4: Implement - Validation Logic

Group 2: Display Component (30m)
- Task 3.5: Test - Display Rendering
- Task 3.6: Implement - Display Component
- Task 3.7: Test - Breakdown Display

Group 3: Layout (15m)
- Task 3.8: Implement - Page Layout
```

---

SUBTASK 3.5: Generate Integration Phase Tasks (10min)

**Expected Output**:
```markdown
Phase 4: Integration [1 hour]

Task 4.1: API Client Setup (20m)
Task 4.2: State Management (20m)
Task 4.3: Connect Components to State (20m)
```

---

SUBTASK 3.6: Generate Testing Phase Tasks (10min)

**Expected Output**:
```markdown
Phase 5: Comprehensive Testing [1 hour]

Task 5.1: Unit Test Coverage Review (15m)
Task 5.2: Integration Tests (30m)
Task 5.3: E2E Flow Test (15m)
```

---

SUBTASK 3.7: Generate Polish Phase Tasks (5-10min)

**Expected Output**:
```markdown
Phase 6: Polish & Production Ready [45 min]

Task 6.1: Add Accessibility (15m)
Task 6.2: Performance Optimization (15m)
Task 6.3: Error Handling (10m)
Task 6.4: Documentation (5m)
```

---

SUBTASK 3.8: Add Cross-Cutting Sections (10min)

**Context**:
- Preservation checklist
- Execution instructions
- Verification strategy

**Steps**:
1. Create preservation checklist from analysis:
  ```
   ## Preservation Checklist
   
   Before executing:
   - [ ] Read old implementation: old-app/salary/
   - [ ] Understand tax calculation algorithm
   - [ ] Note exact values: tax brackets, insurance rates, allowances
   - [ ] Review regional minimums
   
   Critical sections (MUST NOT CHANGE):
   - ✅ Tax brackets: [exact values]
   - ✅ Insurance rates: Employee 10.5%, Employer 21.5%
   - ✅ Allowances: 11M + 4.4M per dependent
   - ✅ Progressive tax algorithm
   ```

2. Add execution instructions:
   ```
   ## Execution Instructions
   
   1. Save this plan:
      {{ if --output }}
      Already saved to: $OUTPUT_PATH
      {{ else }}
      Save manually before executing
      {{ endif }}
   
   2. Execute with subagents:
      ```bash
      /execute-plan {{ $OUTPUT_PATH or 'plan-file.md' }}
      ```
   
   3. During execution:
      - Reference old code frequently (file + line numbers provided)
      - Test outputs against old system
      - Verify PRESERVE sections carefully
      - Commit after each logical group
   
   4. After execution:
      - Run full test suite
      - Compare calculations with old system
      - Test all edge cases
      - Verify no regressions
   ```

3. Add verification strategy:
   ```
   ## Verification Strategy
   
   Critical Verification Points:
   1. Tax calculation outputs match old system (100%)
   2. Insurance deductions identical
   3. Allowance calculations correct
   4. Regional validation works
   5. All edge cases handled
   
   How to Verify:
   - Create test suite with 20+ known scenarios
   - Run old system, record outputs
   - Run new system, compare
   - All outputs must match exactly
   ```

**Expected Output**: Complete cross-cutting sections added to plan

---

SUBTASK 3.9: Compile Complete Plan (5-10min)

**Context**:
- Organize all tasks into final plan
- Add metadata (estimate, risk, confidence)
- Format for /execute-plan compatibility

**Steps**:
1. Combine all task groups
2. Add plan header:
   ```
   # Migration Plan: [Feature Name]
   
   **Generated by**: /auto-plan
   **Based on**: Exploration + Analysis of [source path]
   **Date**: [current date]
   **Estimate**: 6-8 hours
   **Risk**: Medium
   **Confidence**: High
   
   ## Context Summary
   
   Migrating [feature] from old implementation:
   - Source: [path]
   - Critical: [key business logic]
   - Patterns: [technical patterns to keep]
   - Improvements: [what we're fixing]
   ```

3. Add all phases in order
4. Add cross-cutting sections
5. Format for execution

**Output Format** (return to main agent):
```markdown
# Migration Plan: Salary Calculator

**Generated by**: /auto-plan
**Based on**: Exploration + Analysis of old-app/salary/
**Estimate**: 6-8 hours | **Risk**: Medium | **Confidence**: High

---

## Context Summary

Migrating salary calculator from old implementation:
- Source: old-app/modules/Tools/SalaryConversion/
- Critical: Tax calculation (7 brackets), Insurance (10.5% + 21.5%), Allowances
- Patterns: Zustand, react-hook-form, zod (keeping these)
- Improvements: Tests (23% → 80%), Split components, TypeScript strict

---

## Phase 1: Foundation & Types [45min]

### Task 1.1: Create ISalary Interface (10m)

**File**: `src/types/salary.ts`

**Context**:
- Old interface: old-app/salary/types.ts (lines 10-35)
- Must include all fields from old implementation

**Strategy**:
1. Read old ISalary interface
2. Copy all field definitions
3. Add strict TypeScript types (no `any`)
4. Add JSDoc comments

**Acceptance Criteria**:
- [ ] All fields from old interface present
- [ ] Strict TypeScript types used
- [ ] JSDoc documentation
- [ ] Exports correctly

**Expected**: ✅ TypeScript compiles without errors

[... 40+ more detailed tasks with full context ...]

---

## Preservation Checklist

Before executing this plan:
- [ ] Read old implementation thoroughly
- [ ] Understand tax calculation algorithm
- [ ] Note insurance rate percentages
- [ ] Verify allowance amounts
- [ ] Review regional minimum wages

Critical sections to preserve:
- ✅ Tax bracket values and progressive calculation
- ✅ Insurance rates (employee + employer)
- ✅ Allowance amounts (legal requirements)
- ✅ Regional validation logic

---

## Execution Instructions

1. **Save this plan**: {{ if --output }}Already saved to $OUTPUT_PATH{{ else }}Save before executing{{ endif }}

2. **Execute with subagents**:
   ```bash
   /execute-plan {{ $OUTPUT_PATH or 'plan.md' }}
   ```

3. **During execution**:
   - Reference old code frequently
   - Test outputs against old system
   - Verify PRESERVE sections carefully
   - Commit after each logical group

4. **After execution**:
   - Verify calculations match old system
   - Test all edge cases
   - Compare outputs with old implementation

---

## Verification Strategy

Critical Items:
- Tax calculations (must match 100%)
- Insurance deductions (exact percentages)
- Allow ances (legal values)
- Regional validation

Method:
- Test suite with 20+ scenarios
- Compare with old system outputs
- Verify edge cases
- Check rounding behavior

---

Plan ready for execution! ✅
```

**Return**: Complete execution-ready plan to main agent
**Estimate**: 6-8 hours | **Risk**: Medium | **Confidence**: High

---

## Context Summary

Migrating salary calculator from old implementation:
- Source: old-app/modules/Tools/SalaryConversion/
- Critical: Tax calculation (7 brackets), Insurance (10.5% + 21.5%), Allowances
- Patterns: Zustand, react-hook-form, zod
- Improvements: Tests (23% → 80%), Split components, TypeScript strict

---

## Phase 1: Foundation & Types [45min]

### Task 1.1: Create ISalary Interface (10m)

**File**: `src/types/salary.ts`

**Context**:
- Old interface: old-app/salary/types.ts (lines 10-35)
- Must include all fields from old implementation
- Add strict TypeScript types

**Strategy**:
1. Read old ISalary interface
2. Copy all field definitions
3. Add JSDoc comments
4. Export type

**Acceptance Criteria**:
- [ ] All fields from old interface present
- [ ] Strict TypeScript types (no `any`)
- [ ] JSDoc documentation
- [ ] Exports correctly

**Expected**: ✅ TypeScript compiles without errors

---

### Task 1.2: Define Tax Bracket Constants (15m)

**File**: `src/lib/salary/constants.ts`

**Context**:
- Old tax logic: old-app/salary/SalaryContent/index.tsx (lines 65-73)
- 7 progressive tax brackets
- CRITICAL: Must match exactly

**⚠️  MUST PRESERVE**:
```typescript
// DO NOT CHANGE THESE VALUES - Legal requirement
export const TAX_BRACKETS = [
  { max: 5_000_000, rate: 0.05 },      // 5%
  { max: 10_000_000, rate: 0.10 },     // 10%
  { max: 18_000_000, rate: 0.15 },     // 15%
  { max: 32_000_000, rate: 0.20 },     // 20%
  { max: 52_000_000, rate: 0.25 },     // 25%
  { max: 80_000_000, rate: 0.30 },     // 30%
  { max: Infinity, rate: 0.35 },       // 35%
] as const;
```

**Strategy**:
1. Create constants file
2. Copy EXACT values from old code
3. Add TypeScript `as const` for type safety
4. Export for calculator use

**Test**:
Write test that verifies values match old implementation exactly

**Expected**: ✅ Values identical, tests pass

---

[... 40 more detailed tasks ...]

---

## Preservation Checklist

Before executing this plan:
- [ ] Read old implementation thoroughly
- [ ] Understand tax calculation algorithm
- [ ] Note insurance rate percentages
- [ ] Verify allowance amounts
- [ ] Review regional minimum wages

Critical sections to preserve:
- ✅ Tax bracket values and progressive calculation
- ✅ Insurance rates (employee + employer)
- ✅ Allowance amounts (legal requirements)
- ✅ Regional validation logic

---

## Execution Instructions

1. **Save this plan**: Already saved to $OUTPUT_PATH

2. **Execute with subagents**:
   ```bash
   /execute-plan $OUTPUT_PATH
   ```

3. **During execution**:
   - Reference old code frequently
   - Test outputs against old system
   - Verify PRESERVE sections carefully
   - Commit after each logical group

4. **After execution**:
   - Verify calculations match old system
   - Test all edge cases
   - Compare outputs with old implementation

---

Plan ready for execution! ✅
```

---

**Final Review Gate**: Check Plan Quality

```markdown
{{ if not --skip-review }}
Review Plan:
✅ Complete task breakdown?
✅ File paths explicit?
✅ Context references present?
✅ PRESERVE notes included?
✅ Acceptance criteria clear?
✅ Ready for /execute-plan?

{{ if issues found }}
  → Revise plan (re-dispatch Planner with fixes)
{{ else }}
  → Save and present plan to user ✅
{{ endif }}
{{ else }}
  → Save plan (review skipped)
{{ endif }}
```

---

### Phase 4: Save & Present 💾

```markdown
{{ if --output provided }}
1. Save plan to: $OUTPUT_PATH
{{ endif }}

{{ if --analysis provided }}
2. Save exploration + analysis to: $ANALYSIS_PATH
{{ endif }}

3. Display summary to user:
   - Files explored
   - Key findings
   - Plan overview
   - Execution instructions
```

---

## Output Summary

After running `/auto-plan "[feature]"`, you get:

### 1. Exploration Summary
```markdown
🔍 Explored:
- Files: 12 analyzed
- Key logic: Tax calc, Insurance, Allowances
- Patterns: Zustand, react-hook-form, zod
- Issues: Low tests (23%), large components
```

### 2. Analysis Summary
```markdown
📊 Analysis:
- Business rules: 4 critical, 6 important
- Must preserve: Tax formula, Insurance rates, Allowances
- Can improve: Tests, component size, types
- Patterns: Container/Presentational, API-based calculation
```

### 3. Complete Plan
```markdown
📋 Plan Generated:
- Phases: 6
- Tasks: 42 micro-tasks (2-5 min each)
- Estimate: 6-8 hours
- Files: 15 to create/modify
- Risk: Medium
- Ready for: /execute-plan
```

### 4. Next Steps
```markdown
✅ Plan ready!

Execute:
  /execute-plan plans/[feature]-migration.md

Or review first:
  Open: plans/[feature]-migration.md
  Check: Preservation notes, task breakdown
  Then: /execute-plan
```

---

## Examples

### Example 1: Simple Auto-Planning

```bash
/auto-plan "salary calculator"
```

**What happens**:
```
🔍 Phase 1: Exploring...
   Found: old-app/modules/Tools/SalaryConversion/
   Analyzed: 12 files, 8 components, 3 hooks
   ✅ Exploration complete

📊 Phase 2: Analyzing...
   Extracted: 10 business requirements
   Identified: 5 patterns
   Preserved: 4 critical sections
   ✅ Analysis complete

📋 Phase 3: Planning...
   Generated: 6 phases, 42 tasks
   Estimated: 6-8 hours
   ✅ Plan complete

💾 Displaying plan in chat...

Ready for: /execute-plan (plan in chat)
```

### Example 2: Save to Files

```bash
/auto-plan "payment processing" \
  --output=plans/payment-migration.md \
  --analysis=docs/payment-analysis.md
```

**Output**:
- `plans/payment-migration.md`: Complete execution plan
- `docs/payment-analysis.md`: Exploration + analysis report
- Chat: Summary and next steps

### Example 3: Specific Source

```bash
/auto-plan "user authentication" \
  --source=legacy/auth-v2 \
  --type=react \
  --output=plans/auth-migration.md
```

**What happens**:
1. Explores: `legacy/auth-v2/` (no auto-detection needed)
2. Analyzes: With React context (hooks, components)
3. Plans: React-optimized task breakdown
4. Saves: Complete plan to file

### Example 4: Quick No-Review Mode

```bash
/auto-plan "simple utility function" --skip-review
```

**Faster but less safe**:
- Skips review gates
- No quality checks between phases
- Direct exploration → analysis → planning
- Use only for simple, low-risk tasks

---

## Benefits Over Other Commands

| Feature | /explore + /plan | /plan-react --auto-explore | /plan-migration | **/auto-plan** |
|---------|------------------|----------------------------|-----------------|----------------|
| **Auto-explore** | ❌ Manual 2 steps | ⚠️ Optional flag | ✅ Migration only | ✅ Always |
| **Subagents** | ❌ None | ⚠️ Partial | ⚠️ Single phase | ✅ 3 phases |
| **Review gates** | ❌ No | ❌ No | ❌ No | ✅ Yes (3 gates) |
| **Universal** | ✅ Yes | ⚠️ React-focused | ⚠️ Migration only | ✅ Yes |
| **Fresh context** | N/A | ⚠️ Partial | ⚠️ Single context | ✅ Per phase |
| **Quality** | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

---

## When to Use

✅ **Use /auto-plan when**:
- Migrating from old codebase
- Reimplementing existing feature
- Need complete understanding before planning
- Want highest quality planning
- Don't want to remember multi-step workflow

✅ **Use other commands when**:
- `/explore-codebase`: Only need exploration, no plan
- `/plan-react --context`: Already have spec/analysis
- `/plan-migration`: Migration-specific features needed
- `/plan-feature`: Building new feature (no old code)

---

## Pro Tips

1. **Let it auto-detect**: Don't specify --source unless needed
2. **Save important plans**: Always use --output for execution
3. **Save analysis for team**: Use --analysis for documentation
4. **Trust the exploration**: Review gates ensure quality
5. **Compare with old system**: Plan includes test verification steps

---

## Execution Integration

After planning:

```bash
# 1. Generate plan
/auto-plan "feature" --output=plans/feature.md

# 2. Execute with subagents
/execute-plan plans/feature.md

# 3. Verify completeness
/verify-against-spec [spec-if-available] --code=src/features/feature
```

---

## Related Commands

```bash
/explore-codebase [feature]     # Manual exploration only
/plan-react [feature]           # Plan without auto-explore
/plan-migration [feature]       # Migration-specific planning
/execute-plan [plan-file]       # Execute generated plan
```

---

## Troubleshooting

### Exploration Not Finding Code

```bash
# Specify source explicitly
/auto-plan "feature" --source=exact/path/to/old/code
```

### Plan Too Generic

```bash
# Add type hint
/auto-plan "dashboard" --type=react
```

### Need to Review Analysis First

```bash
# Save analysis, review, then plan separately
/auto-plan "feature" --analysis=docs/review-this.md
# Review docs/review-this.md
# Then use /plan-react --context=docs/review-this.md if need to adjust
```

---

**Philosophy**: Exploration-first planning creates better plans. This command enforces that philosophy automatically. 🎯
