# Codebase Exploration Workflow Examples

Practical examples of using the codebase exploration methodology in real scenarios.

## Example 1: Authentication System Exploration

**Command**: `/how "authentication" --source=src/features/auth`

**Expected Workflow**:

### Phase 1: Discovery & Structure
```markdown
📋 PHASE 1: DISCOVERY & STRUCTURE REPORT

Topic: "authentication"
Files Found: 15 files

--- File Inventory ---

### Main Implementation (3 files)
- `src/features/auth/index.tsx` (120 lines) - Auth provider setup
- `src/features/auth/AuthContext.tsx` (85 lines) - Context provider
- `src/features/auth/useAuth.ts` (45 lines) - Auth hook

### Components (5 files)
- `src/features/auth/components/LoginForm.tsx` (95 lines)
- `src/features/auth/components/SignupForm.tsx` (110 lines)
- `src/features/auth/components/ProtectedRoute.tsx` (35 lines)

--- Architecture Pattern ---

**Style**: Context + Custom Hooks
- Centralized auth state in context
- useAuth hook for components
- ProtectedRoute HOC for route protection
```

### Phase 2: Code Analysis
```markdown
📋 PHASE 2: CODE ANALYSIS REPORT

--- Business Logic ---

### JWT Token Management (CRITICAL)
Location: `src/features/auth/AuthContext.tsx` (lines 25-45)
- Token storage in localStorage
- Auto-refresh before expiry
- Cleanup on logout

--- Security Findings ---

✅ Password hashing with bcrypt
✅ JWT with 15-minute expiry
⚠️ No CSRF protection (recommendation)
```

## Example 2: E-commerce Cart Feature

**Command**: `/how "shopping cart" --recent=5`

**Git Analysis Output**:
```markdown
## Recent Changes (Last 5 commits)
1. `feat(cart): Add persistent storage` - 3 files changed
2. `fix(cart): Fix quantity validation` - 1 file changed
3. `refactor(cart): Extract to custom hook` - 2 files changed

## Impact Assessment
- High impact: Persistent storage affects user experience
- Medium impact: Quantity fixes prevent edge cases
- Low impact: Refactoring improves maintainability
```

## Example 3: API Integration Analysis

**Command**: `/how "Stripe integration" --include-external`

**Phase 1 with External Research**:
```markdown
--- External Context ---

### Stripe Library Analysis
From Scout-External agent:
- Library: `stripe@14.9.0`
- Pattern: Using Stripe Elements for PCI compliance
- Best practice: Never handle raw card data
- Integration: Webhook signature verification required

### Security Requirements
- PCI DSS compliance via Stripe Elements
- Webhook endpoint must verify signatures
- Error handling must not leak sensitive data
```

## Example 4: Performance Investigation

**Command**: `/how "image processing" --comprehensive`

**Phase 2 Specialized Analysis**:
```markdown
--- Performance Analysis ---

### Image Processing Pipeline
Location: `src/utils/imageProcessor.ts` (lines 50-120)

**Algorithm Steps**:
1. Upload validation (size, type)
2. Resize to multiple dimensions
3. Optimize compression
4. Generate thumbnails
5. Upload to CDN

**Performance Metrics**:
- Original images: 2-5MB average
- Processed images: 200KB optimized
- Processing time: 3-5 seconds
- Memory usage: 50MB peak

--- Security Review ---

✅ File type validation using magic numbers
✅ Size limits enforced
✅ Sanitized file names
⚠️ No virus scanning (recommendation)
```

## Example 5: Legacy System Migration

**Command**: `/how "legacy checkout" --comprehensive --plan=migration-plan.md`

**Plan Comparison**:
```markdown
## Migration Plan vs Actual Implementation

### Completed (85%)
✅ Payment gateway migration
✅ New order management system
✅ Updated UI components
✅ Database schema migration

### Missing (15%)
❌ Gift card integration (not in plan)
❌ Multi-currency support (delayed)
❌ Analytics tracking (dependency issue)

### Technical Debt Found
- Old validation logic mixed with new
- Missing error boundaries
- Incomplete test coverage
```

## Common Patterns

### Pattern A: New Feature Onboarding
```bash
# Team member needs to understand feature
/how "user permissions" --output=docs/onboarding/

# Generated:
# docs/onboarding/phase-1-discovery-structure.md
# docs/onboarding/phase-2-analysis.md
# docs/onboarding/README.md
```

### Pattern B: Pre-Refactor Analysis
```bash
# Before refactoring legacy code
/how "legacy checkout" --comprehensive

# Use findings to:
- Identify critical business logic
- Note MUST PRESERVE items
- Plan migration strategy
- Create test coverage plan
```

### Pattern C: Security Audit
```bash
# Security-focused exploration
/how "payment flow" --comprehensive

# Automatically includes:
- Security Auditor agent findings
- OWASP compliance check
- Vulnerability assessment
```

### Pattern D: Performance Investigation
```bash
# Performance bottleneck analysis
/how "image upload" --comprehensive

# Focuses on:
- Algorithm complexity
- Resource usage
- Optimization opportunities
- Bottleneck identification
```

## Output Examples

### Complete Documentation Structure
```
docs/feature-exploration/
├── README.md                 # Quick overview and links
├── phase-1-discovery-structure.md  # File inventory, architecture
├── phase-2-analysis.md       # Business logic, patterns
├── recent-changes-analysis.md    # If --recent or --commit used
└── assets/                   # Diagrams, screenshots
    ├── architecture-diagram.png
    └── dependency-graph.png
```

### README.md Template
```markdown
# [Feature] - Codebase Exploration

**Explored**: 2025-01-15

## Quick Links
- [Phase 1: Discovery & Structure](./phase-1-discovery-structure.md)
- [Phase 2: Code Analysis](./phase-2-analysis.md)

## Overview
[Brief 2-3 sentence summary]

## Key Findings
### Architecture
- [Pattern identified]

### Technologies
- [Main libraries used]

### Critical Business Logic
- [Most important logic]

## Recommendations
1. [Top recommendation]
2. [Second recommendation]
```

## Troubleshooting Examples

### Issue: "Phase 1 found no files"
```bash
# Try broader search terms
/how "auth" --comprehensive

# Or specify source
/how "authentication" --source=src/
```

### Issue: "Too many unrelated files"
```bash
# Narrow the scope
/how "login" --source=src/features/auth

# Or use more specific terms
/how "user authentication flow"
```

### Issue: "Need to understand integration"
```bash
# Include external research
/how "stripe integration" --include-external --comprehensive
```

## Best Practices

1. **Be specific**: "user authentication" > "auth"
2. **Use --source** when you know the location
3. **Add --comprehensive** for complex features
4. **Include --plan** to compare with implementation
5. **Use --recent** to understand recent changes
6. **Add --include-external** for third-party integrations

## Integration with Other Commands

After exploration:
```bash
# Apply patterns to new feature
/apply "authentication" --to="user-profile"

# Extend with new capability
/extend "cart" --with="wishlist"

# Generate comprehensive tests
/test-from "payment" --coverage=90

# Refactor based on findings
/refactor-from "legacy checkout" --goal="extract-business-logic"
```