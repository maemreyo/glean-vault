# /plan-feature - Feature Development Plan

## Purpose

Create a structured plan for implementing new features, including UI/UX considerations, state management, and integration points.

## Usage

```bash
/plan-feature [feature description]
```

## Arguments

- `$ARGUMENTS`: Description of the feature to implement

---

## Workflow

Create a feature implementation plan for: **$ARGUMENTS**

### Phase 1: Feature Analysis

1. **User Story**
   - Who is this for?
   - What problem does it solve?
   - What's the expected outcome?

2. **Acceptance Criteria**
   - Define "done" clearly
   - List testable requirements
   - Identify edge cases

3. **UI/UX Considerations**
   - User flow mapping
   - Interaction patterns
   - Accessibility requirements
   - Responsive design needs

### Phase 2: Technical Design

1. **Architecture**
   - Component structure
   - State management approach
   - Data flow design

2. **Integration Points**
   - API requirements
   - Database changes
   - Third-party services

3. **Dependencies**
   - New libraries needed
   - Existing code to modify
   - Feature flags

### Phase 3: Implementation Tasks

Break down into phases:
1. Foundation (data models, API)
2. Core Logic (business rules)
3. UI Implementation (components)
4. Integration (connecting pieces)
5. Polish (UX, performance)

---

## Output Format

```markdown
## 🚀 Feature Plan: [Feature Name]

**Estimate**: X-Y hours | **Complexity**: [Low/Medium/High] | **Priority**: [P1/P2/P3]

### User Story

**As a** [user type]
**I want to** [action]
**So that** [benefit]

### Acceptance Criteria

- [ ] [Criterion 1 - testable statement]
- [ ] [Criterion 2]
- [ ] [Criterion 3]

---

### UI/UX Design

**User Flow**:
```
[Start] → [Step 1] → [Step 2] → [Decision Point]
                                    ↓
                              [Yes] → [Success]
                              [No]  → [Error State]
```

**Key Screens/Components**:
1. [Component A] - [Purpose]
2. [Component B] - [Purpose]

**Interactions**:
- Hover: [behavior]
- Click: [behavior]
- Error: [behavior]

**Accessibility**:
- [ ] Keyboard navigation
- [ ] Screen reader support
- [ ] Color contrast compliance

---

### Technical Design

**Component Structure**:
```
feature/
├── components/
│   ├── FeatureMain.tsx
│   ├── FeatureForm.tsx
│   └── FeatureList.tsx
├── hooks/
│   └── useFeature.ts
├── services/
│   └── featureApi.ts
├── types/
│   └── feature.types.ts
└── index.ts
```

**State Management**:
- Local state: [what]
- Global state: [what, using what library]
- Server state: [caching strategy]

**API Requirements**:
| Endpoint | Method | Purpose |
|----------|--------|---------|
| /api/feature | GET | Fetch list |
| /api/feature | POST | Create new |
| /api/feature/:id | PUT | Update |
| /api/feature/:id | DELETE | Remove |

---

### Tasks

#### Phase 1: Foundation [Xh] 🏗️
| # | Task | Size | Est |
|---|------|------|-----|
| 1 | Create data types and interfaces | S | 20m |
| 2 | Set up API service layer | M | 45m |
| 3 | Add database migration (if needed) | M | 30m |

#### Phase 2: Core Logic [Xh] ⚙️
| # | Task | Size | Est |
|---|------|------|-----|
| 4 | Implement business logic | M | 45m |
| 5 | Create custom hooks | M | 40m |
| 6 | Add validation | S | 25m |

#### Phase 3: UI Implementation [Xh] 🎨
| # | Task | Size | Est |
|---|------|------|-----|
| 7 | Build main component | L | 1h |
| 8 | Create form component | M | 45m |
| 9 | Add list/display component | M | 40m |
| 10 | Implement loading/error states | S | 25m |

#### Phase 4: Integration [Xh] 🔗
| # | Task | Size | Est |
|---|------|------|-----|
| 11 | Connect API to components | M | 35m |
| 12 | Add to routing/navigation | S | 20m |
| 13 | Integrate with existing features | M | 40m |

#### Phase 5: Polish [Xh] ✨
| # | Task | Size | Est |
|---|------|------|-----|
| 14 | Add animations/transitions | S | 25m |
| 15 | Responsive design tweaks | M | 35m |
| 16 | Accessibility audit & fixes | M | 40m |
| 17 | Performance optimization | S | 25m |

---

### Testing Strategy

**Unit Tests**:
- [ ] Business logic functions
- [ ] Custom hooks
- [ ] Utility functions

**Component Tests**:
- [ ] Render states (loading, error, success)
- [ ] User interactions
- [ ] Form validation

**Integration Tests**:
- [ ] API integration
- [ ] State updates
- [ ] Navigation flows

**E2E Tests**:
- [ ] Complete user flow
- [ ] Edge cases

---

### Feature Flag (if applicable)

```typescript
// Enable in feature flags
FEATURE_NEW_DASHBOARD: boolean

// Usage
if (featureFlags.FEATURE_NEW_DASHBOARD) {
  return <NewDashboard />;
}
```

**Rollout Plan**:
1. Internal testing (1 week)
2. Beta users (10%)
3. Gradual rollout (25% → 50% → 100%)

---

### Success Metrics

- [ ] Feature deployed without errors
- [ ] Acceptance criteria met
- [ ] Test coverage ≥80%
- [ ] No accessibility violations
- [ ] Performance: [specific metric]

---

### 🚀 Ready to Start?

Run `/execute-plan` or begin with Task #1.
```

---

## Feature-Specific Considerations

### For UI Features
- Include mockups or wireframes reference
- Note animation/transition requirements
- Specify responsive breakpoints

### For API Features
- Document request/response schemas
- Include error response formats
- Note rate limiting considerations

### For Data Features
- Include data migration plan
- Note backwards compatibility
- Specify rollback procedure

---

---

## Execution with Subagents

Plans from this command can be executed with `/execute-plan` using **subagent-driven methodology**.

**Reference**: `.claude/skills/methodology/executing-plans/SKILL.md`

### How It Works

1. **Save your plan**: Use `--save=path/to/plan.md` flag
2. **Execute with subagents**: `/execute-plan path/to/plan.md`
3. **Fresh subagent per phase**: Each major phase gets dedicated subagent
4. **Code review gates**: Review after each phase before proceeding
5. **Quality guaranteed**: Issues caught and fixed immediately

### Execution Flow

```
Feature Plan (from this command)
  ↓
Phase 1: Data Layer
  → Subagent implements
  → Reviewer checks
  → [Fix if needed]
  ↓
Phase 2: Business Logic  
  → Fresh subagent (clean context)
  → Reviewer checks
  → [Fix if needed]
  ↓
Phase 3: API Layer
  → Fresh subagent
  → Reviewer checks
  ↓
Phase 4: Integration
  → Fresh subagent
  → Final comprehensive review
  ↓
Complete! ✅
```

### Benefits

- ✅ Each phase gets focused attention
- ✅ Review gates prevent issues from cascading
- ✅ Failed phases can be retried independently
- ✅ Fresh context prevents carry-over mistakes
- ✅ Consistent quality across all phases

---

## Related Commands

```bash
/plan              # General planning
/plan-detailed     # TDD micro-tasks
/plan-refactor     # Improving existing code
```
