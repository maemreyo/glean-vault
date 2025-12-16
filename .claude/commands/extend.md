# /extend - Extend Explored Features

## Purpose

Add new capabilities to features that have been explored with `/how`. Leverages comprehensive documentation to understand existing architecture and safely extend functionality while maintaining consistency.

**"Build on proven foundations"** - Extend features while preserving established patterns.

## Aliases

```bash
/extend [feature] --with=[capability]
/extend-feature [feature] --with=[capability]
```

## Usage

```bash
# Add new capability to existing feature
/extend "authentication" --with="2FA support"

# Extend with specific feature
/extend "payment" --feature="refund workflow"

# Preview plan first
/extend "calculator" --with="currency conversion" --preview
```

## Arguments

- `feature`: Feature name (will look for docs in `docs/<feature>/`) or explicit path
- `--with` / `--feature`: Capability or feature to add (required)

## Flags

| Flag | Description | Example |
|------|-------------|---------|
| `--from=path` | Explicit docs folder | `--from=docs/auth/` |
| `--with=desc` | Capability description | `--with="2FA support"` |
| `--feature=desc` | Alternative to --with | `--feature="export PDF"` |
| `--preview` | Preview plan without executing | `--preview` |
| `--skip-review` | Skip code review gates | `--skip-review` |

---

## Integration with /how

Works seamlessly with `/how` exploration output:

```bash
# Step 1: Explore existing feature
/how "authentication"
→ docs/authentication/phase-1-discovery-structure.md
→ docs/authentication/phase-2-analysis.md

# Step 2: Extend with new capability
/extend "authentication" --with="2FA support"
→ Reads docs/authentication/
→ Plans extension respecting existing architecture
→ Implements 2FA while preserving auth patterns
→ Updates docs/authentication/README.md with extension history
```

---

## Workflow

Extending: **$FEATURE** with **$CAPABILITY**

{{ if --from provided }}
**Source docs**: `$FROM_PATH`
{{ else }}
**Source docs**: `docs/$FEATURE/` (auto-detected)
{{ endif }}

**New capability**: `$CAPABILITY`

{{ if --preview }}
**Mode**: Preview plan only
{{ else }}
**Mode**: Plan + Execute
{{ endif }}

---

### Phase 1: Load Existing Documentation 📖

**Goal**: Understand current implementation

**Duration**: 5-10 minutes

---

**Steps**:

1. **Locate documentation**
   ```bash
   {{ if --from provided }}
   DOCS_PATH="$FROM_PATH"
   {{ else }}
   DOCS_PATH="docs/$(echo "$FEATURE" | tr '[:upper:]' '[:lower:]' | tr ' ' '-')/"
   {{ endif }}
   ```

2. **Verify documentation exists**
   ```bash
   if [ ! -d "$DOCS_PATH" ]; then
     echo "❌ Documentation not found: $DOCS_PATH"
     echo "💡 Run: /how \"$FEATURE\" first"
     exit 1
   fi
   ```

3. **Read exploration documents**
   - `phase-1-discovery-structure.md` → File locations, architecture, dependencies
   - `phase-2-analysis.md` → Current capabilities, patterns, business logic

4. **Extract current state**

**Dispatch Documentation Reader SubAgent**:

```markdown
Documentation Reader SubAgent

GOAL: Understand current feature implementation

INPUT:
- Documentation path: $DOCS_PATH
- Feature: $FEATURE

---

SUBTASK 1.1: Read Current Architecture (5 min)

**Steps**:
1. Read phase-1-discovery-structure.md
2. Extract:
   - Current file inventory
   - Current folder structure
   - Component hierarchy
   - State management approach
   - API integration points
   - Testing structure
   - Dependencies

**Output**: Current architecture summary

---

SUBTASK 1.2: Identify Current Capabilities (5 min)

**Steps**:
1. Read phase-2-analysis.md
2. List:
   - Current features implemented
   - Business logic present
   - API endpoints available
   - Data models defined
   - Patterns used
   - Key insights

**Output**: Current capability inventory

---

SUBTASK 1.3: Note Integration Points (3 min)

**Steps**:
1. Identify where new capability would integrate:
   - Which components to modify
   - New components needed
   - API changes required
   - Database changes needed

**Output**: Integration point analysis

---

OUTPUT: Return current state understanding

```markdown
📋 CURRENT STATE ANALYSIS

Feature: $FEATURE
Documentation: $DOCS_PATH

---

## Current Architecture

Folder Structure:
```
src/features/$feature/
├── components/
│   ├── $FeatureHeader.tsx
│   ├── $FeatureContent.tsx
│   └── $FeatureList.tsx
├── hooks/
│   ├── use$Feature.ts
│   └── use$FeatureQuery.ts
├── api/
│   └── $featureApi.ts
└── types/
    └── $feature.types.ts
```

State Management: React Query + react-hook-form
Testing: Jest + RTL (~65% coverage)

---

## Current Capabilities

Features:
- ✅ User login/logout
- ✅ Password reset
- ✅ Session management
- ✅ JWT token refresh

API Endpoints:
- POST /api/auth/login
- POST /api/auth/logout
- POST /api/auth/refresh
- POST /api/auth/reset-password

Data Models:
- User (with auth fields)
- Session
- RefreshToken

---

## Integration Points for Extension

To add "$CAPABILITY", will need to:
- Modify: LoginForm component (add 2FA input)
- Add: TwoFactorSetup component (new)
- Modify: authApi (add 2FA endpoints)
- Add: twoFactorApi (new endpoints)
- Modify: User type (add 2FA fields)
- Add: Database migration (2FA tables)

Dependencies on:
- Existing auth flow
- User management
- Session handling

---

CURRENT STATE LOADED ✅
```
```

**Return**: Current state analysis

---

### Phase 2: Plan Extension 📋

**Goal**: Create detailed plan for new capability

**Duration**: 15-25 minutes

---

**Dispatch Planner SubAgent**:

```markdown
Planner SubAgent - Extension Planning

GOAL: Create detailed plan to add "$CAPABILITY" to $FEATURE

INPUT:
- Current state: [from Phase 1]
- New capability: "$CAPABILITY"
- Must preserve: Existing patterns and architecture

CONSTRAINTS:
- MUST maintain existing architecture
- MUST follow current patterns
- MUST NOT break existing functionality
- MUST include tests

---

SUBTASK 2.1: Analyze Extension Requirements (10 min)

**Steps**:
1. Break down "$CAPABILITY" into specific requirements:
   - What features are needed?
   - What UI changes required?
   - What API changes needed?
   - What data changes required?

2. Identify dependencies:
   - What existing code to modify
   - What new code to create
   - What external libraries needed

**Output**: Requirements breakdown

---

SUBTASK 2.2: Design Integration Strategy (10 min)

**Steps**:
1. Plan where extension fits in current architecture
2. Identify modification points:
   - Components to modify
   - Components to create
   - Hooks to modify
   - Hooks to create
   - API endpoints to add
   - Types to extend

3. Ensure compatibility:
   - No breaking changes to existing API
   - Backward compatible data changes
   - Optional vs required changes

**Output**: Integration strategy

---

SUBTASK 2.3: Create Implementation Plan (10-15 min)

**Steps**:
1. Break into phases:
   - Phase A: Foundation (types, API contracts)
   - Phase B: Backend (API, business logic)
   - Phase C: Frontend (components, hooks)
   - Phase D: Testing
   - Phase E: Documentation

2. Create detailed task list:
   - File-by-file breakdown
   - Clear acceptance criteria
   - Verification steps

3. Note preservation requirements:
   - What must not change
   - What to keep compatible

**Output**: Detailed implementation plan

---

OUTPUT: Return complete extension plan

```markdown
📋 EXTENSION PLAN

Feature: $FEATURE
New Capability: "$CAPABILITY"
Estimated time: 3-5 hours

---

## Requirements

### Core Requirements
1. Enable 2FA for user accounts
2. Support TOTP (Time-based One-Time Password)
3. Backup codes for account recovery
4. Optional (not mandatory) for all users

### Technical Requirements
1. QR code generation for authenticator apps
2. TOTP verification
3. Backup code generation and validation
4. Database persistence for 2FA secrets

---

## Architecture Changes

### Minimal (Preserve Existing)
- ✅ Keep current auth flow
- ✅ Keep JWT authentication
- ✅ 2FA as optional layer

### New Components
```
src/features/authentication/
├── components/
│   ├── TwoFactorSetup.tsx       [NEW]
│   ├── TwoFactorVerify.tsx      [NEW]
│   └── BackupCodes.tsx          [NEW]
├── hooks/
│   ├── useTwoFactor.ts          [NEW]
│   └── useBackupCodes.ts        [NEW]
├── api/
│   └── twoFactorApi.ts          [NEW]
└── types/
    └── two-factor.types.ts      [NEW]
```

### Modified Components
```
src/features/authentication/
├── components/
│   └── LoginForm.tsx            [MODIFY - add 2FA step]
├── hooks/
│   └── useAuth.ts               [MODIFY - check 2FA status]
└── types/
    └── auth.types.ts            [EXTEND - add 2FA fields]
```

---

## Implementation Plan

### Phase A: Foundation (30 min)

**Task A.1**: Create type definitions
- File: `types/two-factor.types.ts`
- Define: TwoFactorSecret, BackupCode, TwoFactorStatus
- Estimate: 10 min

**Task A.2**: Extend User type
- File: `types/auth.types.ts`
- Add: `twoFactorEnabled`, `twoFactorSecret`
- Estimate: 5 min

**Task A.3**: Database migration
- Add 2FA fields to User table
- Create BackupCodes table
- Estimate: 15 min

---

### Phase B: API Layer (1 hour)

**Task B.1**: Create 2FA API client
- File: `api/twoFactorApi.ts`
- Endpoints: setup, verify, disable, generateBackup
- Estimate: 20 min

**Task B.2**: Add API endpoints (backend)
- POST /api/auth/2fa/setup
- POST /api/auth/2fa/verify
- POST /api/auth/2fa/disable
- POST /api/auth/2fa/backup-codes
- Estimate: 40 min

---

### Phase C: Hooks (45 min)

**Task C.1**: Create useTwoFactor hook
- File: `hooks/useTwoFactor.ts`
- Functions: setup, verify, disable
- Uses: React Query
- Estimate: 25 min

**Task C.2**: Create useBackupCodes hook
- File: `hooks/useBackupCodes.ts`
- Functions: generate, validate
- Estimate: 20 min

---

### Phase D: Components (1.5 hours)

**Task D.1**: TwoFactorSetup component
- File: `components/TwoFactorSetup.tsx`
- Features: QR code display, secret entry, verify
- Estimate: 40 min

**Task D.2**: TwoFactorVerify component
- File: `components/TwoFactorVerify.tsx`
- Features: Code input, backup code option
- Estimate: 30 min

**Task D.3**: BackupCodes component
- File: `components/BackupCodes.tsx`
- Features: Display codes, download, regenerate
- Estimate: 20 min

**Task D.4**: Modify LoginForm
- Add 2FA verification step after password
- Only show if user has 2FA enabled
- Estimate: 30 min

---

### Phase E: Testing (1 hour)

**Task E.1**: Unit tests for hooks
**Task E.2**: Component tests
**Task E.3**: Integration tests
**Task E.4**: E2E flow test

---

### Phase F: Documentation (30 min)

**Task F.1**: Update exploration docs
- Re-run /how or manually update phase-3
- Document new 2FA capability

**Task F.2**: API documentation
**Task F.3**: User guide

---

## Preservation Checklist

⚠️ **MUST PRESERVE**:
- [ ] Existing login flow works without 2FA
- [ ] JWT auth unchanged
- [ ] Session management unchanged
- [ ] All existing tests pass
- [ ] Backward compatible API
- [ ] No breaking changes to User type

---

## Verification Plan

**After each phase**:
1. Run existing tests → must pass
2. Run new tests → must pass
3. Verify no breaking changes
4. Code review

**Final verification**:
1. User can log in without 2FA (existing flow)
2. User can enable 2FA
3. 2FA verification works
4. Backup codes work
5. User can disable 2FA
6. All tests passing (old + new)

---

EXTENSION PLAN COMPLETE ✅
```
```

**Return**: Complete extension plan

---

{{ if --preview }}

### Phase 3: Preview Plan 👁️

**Display plan to user for review**

```markdown
📋 EXTENSION PLAN PREVIEW

Feature: $FEATURE
Capability: "$CAPABILITY"

---

## What Will Be Added

New Components (3):
- TwoFactorSetup.tsx (~150 lines)
- TwoFactorVerify.tsx (~100 lines)
- BackupCodes.tsx (~80 lines)

New Hooks (2):
- useTwoFactor.ts (~60 lines)
- useBackupCodes.ts (~40 lines)

New API Client:
- twoFactorApi.ts (~90 lines)

Modified Files (3):
- LoginForm.tsx (add 2FA step)
- useAuth.ts (check 2FA status)
- auth.types.ts (extend with 2FA fields)

---

## Estimated Effort

- Implementation: 3-5 hours
- Testing: 1 hour
- Documentation: 30 minutes
- **Total**: ~4-6.5 hours

---

## Impact Analysis

✅ Non-breaking: Existing login flow unchanged
✅ Optional: 2FA not mandatory
✅ Backward compatible: Works with existing users
✅ Testable: Can verify without affecting production

---

To execute this plan:
/extend "$FEATURE" --with="$CAPABILITY"
(without --preview flag)
```

**END** (no execution)

{{ else }}

### Phase 3: Execute Plan 🏗️

**Goal**: Implement the extension

**Duration**: Based on plan estimate (3-6 hours for 2FA example)

---

**Use `/execute-plan` workflow**

```markdown
Execute plan using existing /execute-plan command

INPUT:
- Extension plan: [from Phase 2]
- Current codebase: [analyzed in Phase 1]

PROCESS:
1. Create TodoWrite from plan tasks
2. Execute tasks sequentially
3. Code review after each phase
4. Verify preservation requirements
5. Run tests continuously

CONSTRAINTS:
- Follow existing patterns exactly
- Run existing tests after each change
- If existing tests fail → rollback, fix, retry
- Code review gates mandatory

---

For detailed execution, see:
`.claude/commands/execute-plan.md`

---

Execution uses same workflow as /execute-plan:
- Fresh subagent per task group
- TDD approach where applicable
- Code review between phases
- Verification at each step
```

**Dispatch to /execute-plan** with plan from Phase 2

---

### Phase 4: Update Documentation 📝

**Goal**: Update exploration docs with new capability

**Duration**: 10-15 minutes

---

**Steps**:

1. **Update README.md** in docs folder
   ```bash
   # Append to docs/$FEATURE/README.md
   ```

2. **Add extension history**:
   ```markdown
   ## Extensions
   
   This feature has been extended with the following capabilities:
   
   ### $CAPABILITY (added on [date])
   - **Added by**: `/extend` command
   - **Files created**: {{ count }} new files
   - **Files modified**: {{ count }} files
   - **Status**: ✅ Complete
   
   **What was added**:
   - {{ list new components }}
   - {{ list new hooks }}
   - {{ list new API endpoints }}
   
   **Integration points**:
   - {{ how it integrates with existing code }}
   
   **Backward compatibility**: ✅ Preserved
   ```

3. **Optional: Create extension log**
   - Create `docs/$FEATURE/extensions/$capability.md`
   - Document detailed changes

**Output**: Documentation updated with extension history

{{ endif }}

---

## Completion

```markdown
✅ EXTENSION COMPLETE

Feature: $FEATURE
Capability Added: "$CAPABILITY"
Documentation: ✅ Updated in docs/$FEATURE/README.md

---

## What Was Added

Files Created: {{ count }} new files
Files Modified: {{ count }} files
Lines Added: ~{{ lines }} lines
Tests Added: {{ count }} tests

---

## Verification

✅ All existing tests passing
✅ New tests passing  
✅ No breaking changes
✅ Code review approved
✅ Documentation updated

---

## Next Steps

1. **Test the new capability manually**
   ```bash
   pnpm dev
   # Try new feature in UI
   ```

2. **Deploy to staging** (if ready)
   ```bash
   /ship "Add $CAPABILITY to $FEATURE"
   ```

3. **Monitor** for issues
   - Check error logs
   - Verify backward compatibility
   - Ensure existing users unaffected

---

🎉 Feature successfully extended!
```

---

## Success Criteria

- [ ] Exploration docs loaded
- [ ] Extension plan created
- [ ] Plan reviewed (if preview mode)
- [ ] Implementation complete (if not preview)
- [ ] All tests passing (old + new)
- [ ] No breaking changes
- [ ] Code review approved
- [ ] Documentation updated

---

## Examples

### Example 1: Add 2FA to Authentication

```bash
/extend "authentication" --with="2FA support"
```

**Output**:
```
Loading docs from docs/authentication/...

Current capabilities:
- Login/logout
- Password reset
- Session management
- JWT tokens

Planning extension for "2FA support"...

Plan created:
- 3 new components
- 2 new hooks
- 1 new API client
- 3 modified files
- Estimate: 4-6 hours

Executing plan...

Phase A: Foundation ✅ (30 min)
Phase B: API Layer ✅ (1 hour)
Phase C: Hooks ✅ (45 min)
Phase D: Components ✅ (1.5 hours)
Phase E: Testing ✅ (1 hour)
Phase F: Documentation ✅ (30 min)

Total: 4.5 hours

All tests passing: ✅ 45 passing (15 new)
Breaking changes: None
Code review: Approved

✅ 2FA successfully added to authentication!
```

### Example 2: Add Export Feature

```bash
/extend "reports" --feature="PDF export"
```

**What happens**:
1. Reads docs/reports/ 
2. Plans PDF export capability
3. Adds export button to UI
4. Implements PDF generation
5. Tests export functionality
6. Updates docs

### Example 3: Preview Mode

```bash
/extend "calculator" --with="currency conversion" --preview
```

**Output**:
```
📋 Extension Plan Preview

Would add currency conversion to calculator

New components:
- CurrencySelector.tsx
- ExchangeRateProvider.tsx

Modified:
- CalculatorForm.tsx (add currency dropdowns)
- calculatorLogic.ts (add conversion)

Estimated: 2-3 hours

To execute: /extend "calculator" --with="currency conversion"
```

---

## Related Commands

- `/how [feature]` - Explore code (prerequisite)
- `/apply [source] --to=[target]` - Clone patterns
- `/test-from [feature]` - Generate tests
- `/refactor-from [feature]` - Refactor code

---

## Pro Tips

1. **Always explore first**:
   ```bash
   /how "feature"      # Understand current state
   /extend "feature"   # Then extend
   ```

2. **Use preview** for complex extensions:
   ```bash
   /extend "feature" --with="complex capability" --preview
   # Review plan before executing
   ```

3. **Keep extensions focused**:
   - One capability at a time
   - Clear, specific description
   - Avoid scope creep

4. **Document as you go**:
   - Update exploration docs
   - Create extension changelog
   - Note design decisions

5. **Test existing functionality**:
   - Run full test suite after extension
   - Manual testing of old features
   - Ensure no regressions

---

## Common Extension Patterns

### Adding Optional Features
```bash
/extend "auth" --with="social login (Google, GitHub)"
# → Adds as optional auth methods
# → Preserves existing email/password
```

### Adding Workflow Steps
```bash
/extend "checkout" --with="gift message step"
# → Adds new step to existing flow
# → Maintains current checkout process
```

### Adding Data Export
```bash
/extend "reports" --feature="CSV/PDF export"
# → Adds export capabilities
# → Keeps existing report viewing
```

### Adding Integrations
```bash
/extend "notifications" --with="Slack integration"
# → Adds Slack as notification channel
# → Preserves existing email/SMS
```

---

**Remember**: Extensions should be additive, not destructive. Preserve existing functionality while adding new capabilities!
