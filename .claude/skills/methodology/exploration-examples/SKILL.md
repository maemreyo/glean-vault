---
name: Exploration Examples
description: This skill provides practical examples, workflow patterns, and troubleshooting guidance for codebase exploration. Use when you need real-world examples of exploration workflows, want to understand common patterns, or need help troubleshooting exploration issues.
version: 1.0.0
---

# Exploration Examples and Workflows

## Overview

Collection of practical examples demonstrating codebase exploration in real scenarios. This skill provides patterns, troubleshooting guides, and integration examples for effective exploration.

**Key concepts:**
- Real-world exploration scenarios
- Common workflow patterns
- Output examples and templates
- Troubleshooting common issues
- Integration with other commands

## Common Exploration Patterns

### Pattern 1: New Feature Onboarding
**When to use**: Team member needs to understand existing feature
**Command**: `/how "feature-name" --output=docs/onboarding/`

**Expected outcome**:
- Complete understanding of feature architecture
- Documentation for new team members
- Quick reference for common tasks

### Pattern 2: Pre-Refactor Analysis
**When to use**: Planning refactoring of legacy code
**Command**: `/how "legacy-feature" --comprehensive`

**Expected outcome**:
- Critical business logic identification
- MUST PRESERVE items documentation
- Refactoring recommendations

### Pattern 3: Security Audit
**When to use**: Security review of sensitive features
**Command**: `/how "payment-flow" --comprehensive`

**Expected outcome**:
- Security vulnerability assessment
- OWASP compliance check
- Security recommendations

### Pattern 4: Performance Investigation
**When to use**: Investigating performance bottlenecks
**Command**: `/how "slow-feature" --comprehensive`

**Expected outcome**:
- Performance bottleneck identification
- Optimization recommendations
- Resource usage analysis

## Real-World Examples

### Example 1: Authentication System

**Scenario**: Understanding JWT-based authentication
```bash
/how "authentication" --source=src/features/auth
```

**Phase 1 Output**:
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

**Phase 2 Output**:
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

### Example 2: E-commerce Cart with Recent Changes

**Scenario**: Understanding recent cart changes
```bash
/how "shopping cart" --recent=5 --plan=docs/cart-improvements.md
```

**Git Analysis Output**:
```markdown
## Recent Changes (Last 5 commits)
1. `feat(cart): Add persistent storage` - 3 files changed
2. `fix(cart): Fix quantity validation` - 1 file changed
3. `refactor(cart): Extract to custom hook` - 2 files changed

## Plan Comparison
- ✅ Persistent storage implemented (80% complete)
- ⚠️ Inventory check missing from plan
- ❌ Coupon system not started
```

### Example 3: API Integration

**Scenario**: Understanding third-party API integration
```bash
/how "Stripe integration" --include-external --comprehensive
```

**Output with External Research**:
```markdown
--- External Context ---
### Stripe Library Analysis
- Library: `stripe@14.9.0`
- Pattern: Using Stripe Elements for PCI compliance
- Best practice: Never handle raw card data
- Integration: Webhook signature verification required

### Security Requirements
- PCI DSS compliance via Stripe Elements
- Webhook endpoint must verify signatures
- Error handling must not leak sensitive data
```

## Output Templates

### Phase 1 Template
```markdown
📋 PHASE 1: DISCOVERY & STRUCTURE REPORT

Topic: "[Feature Name]"
Files Found: X files

--- File Inventory ---
### Categories
- Main Implementation: X files
- Components: Y files
- Utilities: Z files

--- Architecture ---
**Pattern**: [Identified pattern]
**State Management**: [Solution used]
**Data Flow**: [Flow description]
```

### Phase 2 Template
```markdown
📋 PHASE 2: CODE ANALYSIS REPORT

--- Business Logic ---
### Critical Functions
[Documentation with locations]

--- Security & Safety ---
[Vulnerability assessment]

--- Key Insights ---
[Patterns, tech debt, recommendations]
```

### README Template
```markdown
# [Feature] - Codebase Exploration

**Explored**: [Date]

## Quick Links
- [Phase 1](./phase-1-discovery-structure.md)
- [Phase 2](./phase-2-analysis.md)

## Overview
[Brief summary]

## Key Findings
### Architecture
[Pattern identified]

### Recommendations
1. [Top recommendation]
2. [Second recommendation]
```

## Troubleshooting Guide

### Common Issues and Solutions

**Issue**: "Phase 1 found no files"
```bash
# Try broader search terms
/how "auth" --comprehensive

# Or specify source
/how "authentication" --source=src/
```

**Issue**: "Too many unrelated files"
```bash
# Narrow the scope
/how "login" --source=src/features/auth

# Or use more specific terms
/how "user authentication flow"
```

**Issue**: "Need to understand integration"
```bash
# Include external research
/how "stripe integration" --include-external --comprehensive
```

**Issue**: "Phase taking too long"
```bash
# Run specific phases
/how "feature" --phases=1

# Review results before continuing
```

### Error Recovery

**Agent Timeout**:
1. Check if analyzing very large files
2. Split into smaller tasks
3. Focus on critical files first

**Incomplete Analysis**:
1. Review available results
2. Re-run with focused scope
3. Document gaps found

**Memory Issues**:
1. Use `--phases=1` to split work
2. Narrow source directory
3. Exclude test files if not needed

## Integration Examples

### Complete Workflow
```bash
# 1. Explore feature
/how "payment flow" --comprehensive

# 2. Apply patterns to new feature
/apply "payment flow" --to="subscription management"

# 3. Generate tests
/test-from "payment flow" --coverage=90

# 4. Document improvements
/doc "subscription management" --based-on="payment flow"
```

### Team Onboarding
```bash
# Generate onboarding docs
/how "user management" --output=docs/onboarding/

# Share with team
echo "Read docs/onboarding/README.md for feature overview"
```

### Pre-Refactor Preparation
```bash
# Document before refactoring
/how "legacy checkout" --comprehensive

# Use as refactoring guide
refactor-from "legacy checkout" --goal="extract-business-logic"
```

## Best Practices

### Effective Exploration
1. **Be specific**: "user authentication" > "auth"
2. **Use --source** when location is known
3. **Add --comprehensive** for complex features
4. **Include --plan** to compare with implementation
5. **Use --recent** to understand changes

### Documentation
1. Review generated docs immediately
2. Add custom notes for team
3. Link related explorations
4. Update as code evolves

### Team Collaboration
1. Store exploration docs in shared location
2. Reference in PR descriptions
3. Include in onboarding materials
4. Use for architecture decisions

## Additional Resources

### References
- **`codebase-exploration`** - Core methodology
- **`exploration-documentation`** - Documentation patterns
- **`pattern-analysis`** - Pattern extraction for `/apply`

### Command Integration
This skill enhances:
- `/how` - Primary exploration command
- `/apply` - Uses exploration patterns
- `/test-from` - Tests based on findings
- `/refactor-from` - Refactors with understanding

## Examples Directory

See `examples/exploration-workflows.md` for:
- Detailed real-world examples
- Complete output samples
- Advanced workflow patterns
- Integration scenarios