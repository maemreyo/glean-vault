# Impact Analysis Skill

## Overview

**Skill Name**: `impact-analysis`  
**Category**: Methodology  
**Purpose**: Systematically analyze and quantify the impact of changes, fixes, or features on codebase, performance, users, and business outcomes

## Core Principles

### 1. Multi-Dimensional Impact Assessment

**Impact Dimensions**:
```
Technical Impact
├─ Code Quality (coverage, complexity, maintainability)
├─ Performance (speed, memory, scalability)
├─ Security (vulnerabilities, attack surface)
├─ Reliability (error rate, uptime, stability)
└─ Architecture (coupling, cohesion, patterns)

User Impact
├─ Experience (usability, accessibility, delight)
├─ Performance (load times, responsiveness)
├─ Functionality (features, capabilities)
└─ Trust (security, privacy, transparency)

Business Impact
├─ Risk (regulatory, security, operational)
├─ Cost (development, maintenance, infrastructure)
├─ Revenue (conversion, retention, expansion)
└─ Efficiency (team velocity, deployment frequency)
```

### 2. Impact Quantification

**Measurement Framework**:
```
Quantitative Metrics
├─ Absolute: "Reduced load time by 805ms"
├─ Relative: "95% faster than before"
├─ Comparative: "Now faster than industry avg (200ms vs 500ms)"
└─ Trend: "Performance improving 10% week-over-week"

Qualitative Metrics
├─ Severity: [critical, high, medium, low]
├─ Scope: [system-wide, module, function, line]
├─ Certainty: [confirmed, likely, possible, uncertain]
└─ Urgency: [immediate, soon, eventually, optional]
```

## Impact Analysis Process

### Phase 1: Baseline Measurement

**Capture Before State**:
```bash
# Code metrics
npx cloc src/                      # Lines of code
npm run coverage                   # Test coverage
npm run complexity                 # Cyclomatic complexity

# Performance metrics
ab -n 1000 -c 10 http://api/endpoint   # Response times
node --prof app.js                      # CPU profiling
node --inspect --trace-gc app.js        # Memory profiling

# Security metrics
npm audit                          # Dependencies
snyk test                          # Vulnerabilities
eslint --security                  # Code patterns

# Quality metrics
sonar-scanner                      # Technical debt
eslint --format json               # Linting issues
prettier --check src/              # Formatting issues
```

**Baseline Report**:
```json
{
  "baseline": {
    "timestamp": "2024-01-15T10:00:00Z",
    "code_quality": {
      "lines_of_code": 15420,
      "test_coverage": 45,
      "cyclomatic_complexity": 8.2,
      "linting_errors": 23,
      "technical_debt_minutes": 320
    },
    "performance": {
      "api_response_p50": 850,
      "api_response_p95": 1200,
      "api_response_p99": 1800,
      "memory_usage_mb": 145,
      "cpu_usage_percent": 35
    },
    "security": {
      "critical_vulnerabilities": 2,
      "high_vulnerabilities": 5,
      "medium_vulnerabilities": 12,
      "dependency_issues": 8
    }
  }
}
```

### Phase 2: Change Implementation & Measurement

**Track Changes**:
```javascript
class ImpactTracker {
  constructor() {
    this.changes = [];
    this.metrics = {
      before: {},
      after: {},
      delta: {}
    };
  }
  
  recordChange(change) {
    this.changes.push({
      type: change.type,
      description: change.description,
      files: change.files,
      timestamp: new Date(),
      metrics: {
        lines_added: change.stats.additions,
        lines_removed: change.stats.deletions,
        files_changed: change.files.length
      }
    });
  }
  
  async measureImpact() {
    this.metrics.after = await captureMetrics();
    this.metrics.delta = calculateDelta(
      this.metrics.before,
      this.metrics.after
    );
    return this.metrics;
  }
}
```

### Phase 3: Delta Calculation & Analysis

**Impact Calculation**:
```python
def calculate_impact(before, after):
    impact = {
        'improvements': [],
        'regressions': [],
        'neutral': []
    }
    
    for metric, value_after in after.items():
        value_before = before.get(metric, 0)
        delta = value_after - value_before
        percent_change = (delta / value_before * 100) if value_before else 0
        
        change = {
            'metric': metric,
            'before': value_before,
            'after': value_after,
            'delta': delta,
            'percent_change': percent_change,
            'direction': 'up' if delta > 0 else 'down' if delta < 0 else 'same'
        }
        
        # Classify based on metric type (higher is better vs lower is better)
        if is_positive_change(metric, delta):
            impact['improvements'].append(change)
        elif is_negative_change(metric, delta):
            impact['regressions'].append(change)
        else:
            impact['neutral'].append(change)
    
    return impact
```

## Application in `/fix-issues` Command

### 1. Per-Issue Impact Tracking

```markdown
## Issue: [ISS-005] N+1 Query in Dashboard

### Measurements

**Before Fix**:
- Query count: 103 queries per request
- Response time: 850ms (p95)
- Database CPU: 45%
- Cache hit rate: 20%

**After Fix**:
- Query count: 3 queries per request (JOIN)
- Response time: 45ms (p95)
- Database CPU: 8%
- Cache hit rate: N/A (not needed)

### Impact Analysis

**Performance Impact**: 🟢 MAJOR IMPROVEMENT
- Response time: -805ms (-95%)
- Query count: -100 queries (-97%)
- Database load: -37 percentage points (-82%)

**Code Quality Impact**: 🟢 IMPROVEMENT
- Complexity: +5 lines, but more maintainable
- Readability: Improved (single JOIN vs loop)
- Database design: Added index (2KB overhead)

**User Impact**: 🟢 SIGNIFICANT
- Dashboard loads 18x faster
- Reduced server costs ~$200/month
- Better UX, especially for users with slow connections

**Risk**: 🟡 LOW
- Database migration needed (5 minutes downtime)
- Index maintenance cost (negligible)
- No breaking changes
```

### 2. Aggregate Impact Report

```markdown
# 📊 Aggregate Impact Report

## Summary

**Total Issues Fixed**: 12
**Time Period**: 2024-01-15 10:00 - 12:15 (2h 15m)

---

## Technical Impact

### Code Quality
| Metric | Before | After | Delta | Change |
|--------|--------|-------|-------|--------|
| Test Coverage | 45% | 72% | +27pp | 🟢 +60% |
| Linting Errors | 23 | 0 | -23 | 🟢 -100% |
| Cyclomatic Complexity | 8.2 | 7.1 | -1.1 | 🟢 -13% |
| Technical Debt | 320min | 180min | -140min | 🟢 -44% |
| Lines of Code | 15,420 | 15,890 | +470 | 🟡 +3% |

**Analysis**: Significant quality improvements with minimal code growth. 
Test coverage nearly doubled. All linting issues resolved.

---

### Performance
| Metric | Before | After | Delta | Change |
|--------|--------|-------|-------|--------|
| API Response (p50) | 850ms | 45ms | -805ms | 🟢 -95% |
| API Response (p95) | 1200ms | 98ms | -1102ms | 🟢 -92% |
| Memory Usage | 145MB | 123MB | -22MB | 🟢 -15% |
| CPU Usage | 35% | 28% | -7pp | 🟢 -20% |
| Database Queries | 103/req | 3/req | -100 | 🟢 -97% |

**Analysis**: Dramatic performance improvements, especially in database 
operations. Response times now well within acceptable range (<100ms).

---

### Security
| Metric | Before | After | Delta | Change |
|--------|--------|-------|-------|--------|
| Critical Vulnerabilities | 2 | 0 | -2 | 🟢 -100% |
| High Vulnerabilities | 5 | 1 | -4 | 🟢 -80% |
| Medium Vulnerabilities | 12 | 8 | -4 | 🟢 -33% |
| Security Score (0-100) | 62 | 89 | +27 | 🟢 +44% |

**Analysis**: All critical vulnerabilities resolved (SQL injection, 
exposed secrets). Remaining issues are low priority.

---

### Reliability
| Metric | Before | After | Delta | Change |
|--------|--------|-------|-------|--------|
| Error Rate | 2.3% | 0.4% | -1.9pp | 🟢 -83% |
| Unhandled Exceptions | 15/day | 0/day | -15 | 🟢 -100% |
| Memory Leaks | 1 known | 0 known | -1 | 🟢 -100% |
| Uptime (last 7d) | 99.2% | 99.8% | +0.6pp | 🟢 +0.6% |

**Analysis**: Significantly more stable. Error handling improvements 
eliminated unhandled exceptions.

---

## User Impact

### Experience Improvements
- **Dashboard**: 18x faster load time (850ms → 45ms)
  - Impact: Users see data immediately, no loading spinner
  - Benefit: Reduced bounce rate, increased engagement

- **Authentication**: New test coverage eliminates login bugs
  - Impact: Fewer failed login attempts
  - Benefit: Better first impression, reduced support tickets

- **Search**: SQL injection fix + input validation
  - Impact: No more error messages on special characters
  - Benefit: More reliable search, better trust

### Accessibility
- No direct accessibility improvements in this batch
- Recommendation: Add accessibility audit to next sprint

---

## Business Impact

### Risk Reduction
| Risk Type | Before | After | Impact |
|-----------|--------|-------|--------|
| Security Breach | High (2 critical) | Low (0 critical) | 🟢 Major reduction |
| Data Loss | Medium (no backups) | Low (added) | 🟢 Reduced |
| Compliance | At risk (PCI) | Compliant | 🟢 Critical |
| Downtime | Medium (leaks) | Low (fixed) | 🟢 Reduced |

**Financial Risk Impact**: Estimated $50K-500K liability reduction 
from security vulnerabilities alone.

### Cost Impact
| Area | Change | Annual Impact |
|------|--------|---------------|
| Server Costs | -15% CPU, -15% RAM | 🟢 -$2,400/year |
| Database Costs | -97% queries | 🟢 -$3,600/year |
| Support Tickets | -50% error-related | 🟢 -$12,000/year |
| Developer Time | +2h fixed, -20h future | 🟢 -$7,200/year |
| **Total** | | 🟢 **-$25,200/year** |

### Revenue Impact (Estimated)
| Metric | Change | Revenue Impact |
|--------|--------|----------------|
| Conversion Rate | +0.5% (faster load) | 🟢 +$18,000/year |
| Customer Retention | +2% (fewer bugs) | 🟢 +$45,000/year |
| Premium Upgrades | +1% (better perf) | 🟢 +$8,000/year |
| **Total** | | 🟢 **+$71,000/year** |

**Net Business Impact**: +$96,200/year (cost savings + revenue increase)

---

## Developer Experience Impact

### Productivity
- Linting errors eliminated → Less time fixing style issues
- Test coverage improved → Fewer bugs in production
- Documentation added → Easier onboarding

**Estimated Time Savings**: 5-8 hours/week per developer

### Code Maintainability
| Aspect | Before | After | Impact |
|--------|--------|-------|--------|
| Time to understand code | 15min | 10min | 🟢 -33% |
| Time to add feature | 3h | 2h | 🟢 -33% |
| Time to fix bug | 1.5h | 1h | 🟢 -33% |
| Onboarding time | 2 weeks | 1.5 weeks | 🟢 -25% |

---

## Long-Term Impact Projection

### 3-Month Outlook
- Maintained test coverage will prevent ~15 bugs
- Performance improvements reduce server costs by ~$1,800
- Security posture enables enterprise customer acquisition

### 6-Month Outlook
- Technical debt reduction improves feature velocity by ~20%
- Lower error rates improve customer satisfaction scores
- Code quality improvements reduce time-to-market

### 12-Month Outlook
- Foundation for scalability (efficient queries, good tests)
- Reduced maintenance burden enables team growth
- Security compliance opens new market opportunities

---

## Confidence Levels

| Impact Category | Confidence | Rationale |
|----------------|------------|-----------|
| Performance Gains | 🟢 High (95%) | Directly measured, reproducible |
| Cost Savings | 🟡 Medium (70%) | Based on current usage patterns |
| Revenue Impact | 🟡 Medium (60%) | Correlation, not causation |
| User Satisfaction | 🟡 Medium (65%) | Improved metrics, need surveys |
| Risk Reduction | 🟢 High (90%) | Security scan results clear |

---

## Recommendations

### Immediate Actions
1. **Monitor production metrics** for 48h to confirm improvements
2. **Run regression tests** to ensure no hidden issues
3. **Update documentation** with new performance characteristics

### Short-term (1-2 weeks)
1. **User survey** to measure satisfaction improvement
2. **A/B test** to quantify conversion rate change
3. **Cost analysis** to validate server savings estimates

### Long-term (1-3 months)
1. **Continuous monitoring** of key metrics
2. **Regular impact reviews** to validate projections
3. **Adjust estimates** based on actual data
```

## Impact Visualization

### Impact Dashboard
```markdown
# Visual Impact Summary

## 🎯 Key Wins

┌─────────────────────────────────────────┐
│ Performance: 18x FASTER                 │
│ ████████████████████░ 95% improvement  │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ Security: 100% Critical Issues Resolved │
│ ████████████████████ All fixed         │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ Test Coverage: 45% → 72%                │
│ █████████████░░░░░░░ +27pp              │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ Cost Savings: $25K/year                 │
│ ████████░░░░░░░░░░░░ Estimated          │
└─────────────────────────────────────────┘

## 📈 Trends

Before Fix:    █░░░░░░░░░░  Performance
After Fix:     ███████████  Performance

Before Fix:    ██████░░░░░  Security
After Fix:     ███████████  Security

Before Fix:    ████░░░░░░░  Code Quality
After Fix:     █████████░░  Code Quality
```

## Impact Scoring Framework

**Overall Impact Score**: Weighted average of dimensions

```javascript
function calculateImpactScore(impacts) {
  const weights = {
    security: 0.30,      // Highest weight - security is critical
    performance: 0.25,   // High weight - user experience
    reliability: 0.20,   // High weight - stability matters
    quality: 0.15,       // Medium weight - maintainability
    cost: 0.10           // Lower weight - often estimated
  };
  
  let totalScore = 0;
  for (const [dimension, weight] of Object.entries(weights)) {
    const score = impacts[dimension].score; // 0-100
    totalScore += score * weight;
  }
  
  return {
    score: totalScore,
    grade: getGrade(totalScore),
    interpretation: getInterpretation(totalScore)
  };
}

function getGrade(score) {
  if (score >= 90) return 'A+ (Exceptional)';
  if (score >= 80) return 'A (Excellent)';
  if (score >= 70) return 'B (Good)';
  if (score >= 60) return 'C (Acceptable)';
  return 'D (Needs Improvement)';
}
```

## Integration with Other Skills

- **`pattern-analysis`**: Identify recurring impact patterns
- **`sequential-thinking`**: Predict downstream effects
- **`verification-before-completion`**: Validate impact measurements
- **`root-cause-tracing`**: Understand why impacts occurred
- **`performance-optimization`**: Measure optimization results

## Best Practices

### 1. Measure Early and Often
```bash
# Before making changes
npm run benchmark:before

# After each significant change
npm run benchmark:after

# Compare results
npm run benchmark:compare
```

### 2. Use Multiple Data Sources
```
Quantitative Data:
├─ Metrics (coverage, performance, errors)
├─ Logs (usage patterns, error rates)
└─ Benchmarks (before/after comparisons)

Qualitative Data:
├─ User feedback (surveys, support tickets)
├─ Code reviews (maintainability, readability)
└─ Team input (developer experience)
```

### 3. Consider Second-Order Effects
```
Direct Impact: Fixed N+1 query → Faster response
├─ Second-order: Users stay longer on site
│  └─ Third-order: Higher conversion rate
│
└─ Second-order: Reduced server load
   └─ Third-order: Lower infrastructure costs
      └─ Fourth-order: Budget for new features
```

### 4. Document Uncertainty
```markdown
## Impact Estimate Confidence

**High Confidence (90-100%)**:
- Response time improvement: Measured directly
- Test coverage increase: Calculated from reports

**Medium Confidence (60-80%)**:
- Cost savings: Based on current usage patterns
- User satisfaction: Correlation with metrics

**Low Confidence (30-50%)**:
- Revenue impact: Multiple confounding factors
- Long-term maintainability: Requires time to validate
```

## When to Apply This Skill

- ✅ Before/after major changes
- ✅ When fixing performance issues
- ✅ After security vulnerability remediation
- ✅ When justifying technical decisions
- ✅ For stakeholder reporting
- ✅ During retrospectives and reviews