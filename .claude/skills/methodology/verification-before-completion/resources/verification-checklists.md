# Verification Checklists

This document provides comprehensive checklists for verifying different types of work.

## Testing Verification Checklist

### Before Claiming Tests Pass
- [ ] Run full test suite (no filters)
- [ ] Verify exit code is 0
- [ ] Check for any skipped tests
- [ ] Note total test count
- [ ] Verify expected number of tests
- [ ] Check test coverage if required
- [ ] Review any warnings
- [ ] Verify all test suites pass
- [ ] Check for flaky tests
- [ ] Run tests on clean environment

### Test Types Checklist
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] E2E tests pass
- [ ] Performance tests meet criteria
- [ ] Security tests pass
- [ ] Accessibility tests pass
- [ ] Visual regression tests pass

### Coverage Checklist
- [ ] Overall coverage meets requirement
- [ ] Critical files have required coverage
- [ ] New code is covered
- [ ] Edge cases are covered
- [ ] Error paths are tested

## Build Verification Checklist

### Before Claiming Build Succeeds
- [ ] Run clean build (remove artifacts first)
- [ ] Verify exit code is 0
- [ ] Check all expected artifacts created
- [ ] Verify no build errors
- [ ] Check build time is acceptable
- [ ] Verify bundle size if required
- [ ] Check for build warnings
- [ ] Test artifacts work correctly
- [ ] Verify production build
- [ ] Check asset optimization

### Build Types
- [ ] Development build works
- [ ] Production build optimized
- [ ] Static assets generated
- [ ] Source maps generated (if needed)
- [ ] Manifest files updated
- [ ] Environment variables set correctly

## Bug Fix Verification Checklist

### Red-Green Cycle
- [ ] Reproduce original bug (it fails)
- [ ] Write test that captures bug
- [ ] Apply fix
- [ ] Verify test passes
- [ ] Check for regressions
- [ ] Run full test suite
- [ ] Test edge cases around fix
- [ ] Verify performance not degraded

### Bug Categories
- [ ] Logic bug fixed
- [ ] UI bug fixed
- [ ] Performance bug improved
- [ ] Security vulnerability patched
- [ ] Memory leak fixed
- [ ] Race condition resolved
- [ ] Deadlock eliminated

## Feature Implementation Checklist

### Requirements Verification
- [ ] All functional requirements met
- [ ] All non-functional requirements met
- [ ] Acceptance criteria satisfied
- [ ] Business rules implemented
- [ ] Edge cases handled
- [ ] Error scenarios covered

### Quality Assurance
- [ ] Code follows standards
- [ ] Documentation updated
- [ ] Tests written for new code
- [ ] Performance acceptable
- [ ] Security considerations addressed
- [ ] Accessibility compliance checked
- [ ] Error handling implemented

### Integration Checklist
- [ ] Works with existing code
- [ ] No breaking changes
- [ ] APIs documented
- [ ] Database migrations handled
- [ ] Configuration updated
- [ ] Deployment process tested

## Code Review Verification Checklist

### Before Merging
- [ ] Code reviewed by peer
- [ ] All comments addressed
- [ ] No TODO/FIXME left
- [ ] Secrets not committed
- [ ] Dependencies updated
- [ ] License headers present
- [ ] Changelog updated

### Automated Checks
- [ ] Linting passes
- [ ] Type checking passes
- [ ] Tests pass on CI
- [ ] Security scan passes
- [ ] Dependency check passes

## Deployment Verification Checklist

### Pre-deployment
- [ ] All tests passing in CI
- [ ] Build successful
- [ ] Environment variables configured
- [ ] Database migrations ready
- [ ] Rollback plan prepared
- [ ] Monitoring configured
- [ ] Documentation updated

### Post-deployment
- [ ] Application starts successfully
- [ ] Health checks passing
- [ ] Key endpoints responding
- [ ] Database connected
- [ ] No error spikes in logs
- [ ] Performance metrics normal
- [ ] User functionality verified

## Performance Verification Checklist

### Before Claiming Performance Improved
- [ ] Baseline measured
- [ ] Improvement quantified
- [ ] Load tests pass
- [ ] Memory usage checked
- [ ] CPU usage monitored
- [ ] Database queries optimized
- [ ] Caching working
- [ ] No regressions introduced

### Performance Metrics
- [ ] Response time improved
- [ ] Throughput increased
- [ ] Resource usage optimized
- [ ] Scalability tested
- [ ] Concurrent users handled
- [ ] Burst traffic managed

## Security Verification Checklist

### Before Claiming Secure
- [ ] Authentication implemented correctly
- [ ] Authorization checks in place
- [ ] Input validation added
- [ ] Output encoding used
- [ ] SQL injection prevented
- [ ] XSS protection active
- [ ] CSRF protection enabled
- [ ] HTTPS enforced
- [ ] Secrets not exposed
- [ ] Security audit passed

### Security Tests
- [ ] Penetration test passed
- [ ] Vulnerability scan clean
- [ ] Dependency audit passed
- [ ] OWASP Top 10 addressed
- [ ] Data encryption active
- [ ] Logging and monitoring enabled

## Documentation Verification Checklist

### Before Claiming Documentation Complete
- [ ] All APIs documented
- [ ] Examples provided
- [ ] Installation instructions clear
- [ ] Troubleshooting guide exists
- [ ] Changelog updated
- [ ] README updated
- [ ] Code comments adequate
- [ ] Architecture diagram included

### Documentation Quality
- [ ] Documentation builds without errors
- [ ] Links are working
- [ ] Examples are tested
- [ ] Screenshots up-to-date
- [ ] Version information correct
- [ ] Contributing guidelines clear

## Database Verification Checklist

### Before Claiming Database Changes Complete
- [ ] Migration script tested
- [ ] Rollback script ready
- [ ] Data backup created
- [ ] Migration applied successfully
- [ ] Data integrity verified
- [ ] Performance tested
- [ ] Indexes created
- [ ] Foreign keys maintained
- [ ] Permissions updated

### Data Verification
- [ ] Schema matches expectations
- [ ] Constraints enforced
- [ ] Triggers working
- [ ] Procedures updated
- [ ] Views correct
- [ ] Sample data valid
- [ ] No orphaned records

## Monitoring Verification Checklist

### Before Claiming Monitoring Ready
- [ ] Metrics collected
- [ ] Dashboards configured
- [ ] Alerts set up
- [ ] Logging implemented
- [ ] Error tracking active
- [ ] Performance monitoring enabled
- [ ] Health checks configured
- [ ] SLA monitoring active

## Configuration Verification Checklist

### Before Claiming Configuration Complete
- [ ] Environment variables set
- [ ] Configuration files valid
- [ ] Default values appropriate
- [ ] Sensitive data externalized
- [ ] Validation rules defined
- [ ] Documentation updated
- [ ] Test configurations provided

## API Verification Checklist

### Before Claiming API Ready
- [ ] All endpoints implemented
- [ ] Request/response schemas valid
- [ ] Error handling complete
- [ ] Status codes correct
- [ ] Authentication required
- [ ] Rate limiting configured
- [ ] Versioning strategy defined
- [ ] Documentation generated
- [ ] Contract tests passing

## Quick Verification Templates

### Simple Task Verification
```markdown
## Task: [Name]

### Verification:
- [ ] Tests: `npm test` → [X passing, Y failing]
- [ ] Build: `npm run build` → [Success/Failed]
- [ ] Lint: `npm run lint` → [Clean/Errors]

### Result:
✓ Task complete - [specific verification results]
```

### Complex Feature Verification
```markdown
## Feature: [Name]

### Requirements Check:
- [ ] Req 1: [Description] → [How verified]
- [ ] Req 2: [Description] → [How verified]
- [ ] Req 3: [Description] → [How verified]

### Automated Tests:
- Unit: [X/Y] passing
- Integration: [X/Y] passing
- E2E: [X/Y] passing

### Manual Verification:
- [ ] Scenario 1: [Result]
- [ ] Scenario 2: [Result]

### Conclusion:
✓ Feature complete, all requirements verified
```

### Bug Fix Verification
```markdown
## Bug: [Description]

### Reproduction:
- [ ] Original bug reproduced
- [ ] Test case written
- [ ] Test fails before fix

### Fix Verification:
- [ ] Fix implemented
- [ ] Test passes after fix
- [ ] No regression
- [ ] Edge cases covered

### Conclusion:
✓ Bug fixed, verified with test coverage
```

## Verification Anti-patterns to Avoid

1. **Trusting without verifying**
   - Never assume based on code review
   - Always run actual tests/commands

2. **Partial verification**
   - Don't test only happy path
   - Include edge cases and errors

3. **Outdated verification**
   - Don't rely on old test results
   - Run fresh verification

4. **Vague claims**
   - Include specific numbers and evidence
   - Be precise about what was verified

5. **Missing baseline**
   - Measure before for improvements
   - Quantify changes made