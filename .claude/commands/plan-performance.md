# /plan-performance - Performance Optimization Planning

## Purpose

Create structured plans for performance optimization with profiling, measurement, and improvement strategies.

## Usage

```bash
/plan-performance [optimization target]
```

## Arguments

- `$ARGUMENTS`: Description of what to optimize (e.g., "speed up dashboard load time")

---

## Workflow

Create a performance optimization plan for: **$ARGUMENTS**

### Phase 1: Baseline & Profiling

1. **Establish Current Performance**
   - Measure current metrics
   - Identify bottlenecks
   - Document baseline

2. **Profiling**
   - Use performance profiling tools
   - Identify hot paths
   - Find memory leaks

3. **Set Targets**
   - Define performance goals
   - Identify priority areas
   - Set success metrics

### Phase 2: Analysis

1. **Root Cause Analysis**
   - Why is it slow?
   - What's consuming resources?
   - Where are the inefficiencies?

2. **Opportunity Identification**
   - Quick wins
   - High-impact changes
   - Trade-offs

### Phase 3: Implementation

1. **Prioritize Optimizations**
   - Impact vs effort matrix
   - Address critical path first
   - Incremental improvements

2. **Measure Each Change**
   - Before/after comparison
   - Regression testing
   - Benchmark validation

---

## Output Format

```markdown
## ⚡ Performance Plan: [Target]

**Current State**: [X]ms/[Y]MB | **Target**: [A]ms/[B]MB | **Improvement**: -Z%

### Baseline Metrics

**Before Optimization**:
| Metric | Value | Tool |
|--------|-------|------|
| Page Load Time | 4.2s | Lighthouse |
| First Contentful Paint | 2.1s | Chrome DevTools |
| Time to Interactive | 5.8s | Lighthouse |
| Bundle Size | 1.2MB | webpack-bundle-analyzer |
| API Response Time | 850ms | Network tab |
| Memory Usage | 120MB | Chrome DevTools |

**Bottlenecks Identified**:
1. 🔴 Large JavaScript bundle (800KB)
2. 🟡 Unoptimized images (2-3MB each)
3. 🟡 N+1 query problem in API
4. 🟠 No caching strategy

---

### Performance Targets

| Metric | Current | Target | Priority |
|--------|---------|--------|----------|
| Page Load | 4.2s | <2s | 🔴 High |
| FCP | 2.1s | <1s | 🔴 High |
| TTI | 5.8s | <3s | 🟡 Medium |
| Bundle Size | 1.2MB | <500KB | 🔴 High |

**Target Lighthouse Score**: 90+ (currently 65)

---

### Optimization Strategies

#### Quick Wins (1-2 hours) ⚡
| # | Optimization | Impact | Effort | Est Improvement |
|---|--------------|--------|--------|-----------------|
| 1 | Enable gzip compression | High | Low | -60% transfer size |
| 2 | Add browser caching headers | Medium | Low | -30% repeat loads |
| 3 | Lazy load images | High | Low | -40% initial load |
| 4 | Remove unused CSS/JS | Medium | Medium | -15% bundle size |

#### High-Impact Changes (4-8 hours) 🚀
| # | Optimization | Impact | Effort | Est Improvement |
|---|--------------|--------|--------|-----------------|
| 5 | Code splitting | High | Medium | -50% initial bundle |
| 6 | Image optimization | High | Medium | -70% image size |
| 7 | Implement CDN | High | Medium | -40% global latency |
| 8 | Database query optimization | High | High | -60% API time |

#### Long-term Improvements (1-2 weeks) 📈
| # | Optimization | Impact | Effort | Est Improvement |
|---|--------------|--------|--------|-----------------|
| 9 | Server-side caching (Redis) | High | High | -80% cache hits |
| 10 | Service workers for offline | Medium | High | Instant repeat visits |
| 11 | Migrate to Next.js SSR | High | High | -50% initial load |

---

### Tasks

#### Phase 1: Profiling & Analysis [Xh] 🔍
| # | Task | Size | Est |
|---|------|------|-----|
| 1 | Run Lighthouse audit | S | 15m |
| 2 | Profile with Chrome DevTools | M | 30m |
| 3 | Analyze bundle with webpack-bundle-analyzer | S | 20m |
| 4 | Check database query performance | M | 40m |
| 5 | Document baseline metrics | S | 20m |

#### Phase 2: Quick Wins [Xh] ⚡
| # | Task | Size | Est |
|---|------|------|-----|
| 6 | Enable compression (gzip/brotli) | S | 20m |
| 7 | Add cache headers | S | 15m |
| 8 | Implement lazy loading | M | 40m |
| 9 | Remove dead code | M | 35m |
| 10 | Measure improvements | S | 20m |

#### Phase 3: High-Impact [Xh] 🚀
| # | Task | Size | Est |
|---|------|------|-----|
| 11 | Set up code splitting | M | 45m |
| 12 | Optimize images (WebP, sizes) | M | 1h |
| 13 | Configure CDN | M | 45m |
| 14 | Optimize database queries | L | 2h |
| 15 | Add database indexes | M | 40m |
| 16 | Measure improvements | S | 25m |

#### Phase 4: Validation [Xh] ✅
| # | Task | Size | Est |
|---|------|------|-----|
| 17 | Performance regression tests | M | 45m |
| 18 | Load testing | M | 1h |
| 19 | Real user monitoring setup | M | 40m |
| 20 | Final Lighthouse audit | S | 15m |

---

### Optimization Details

**Bundle Size Reduction**:
```javascript
// Before: Import entire library
import _ from 'lodash'; // 70KB

// After: Import only what you need
import debounce from 'lodash/debounce'; // 2KB

// Use dynamic imports
const HeavyComponent = lazy(() => import('./HeavyComponent'));
```

**Image Optimization**:
```html
<!-- Before -->
<img src="hero.png" /> <!-- 3MB -->

<!-- After: Responsive images with WebP -->
<picture>
  <source srcset="hero-320.webp 320w, hero-640.webp 640w" type="image/webp" />
  <img src="hero-640.jpg" alt="Hero" loading="lazy" /> <!-- 200KB -->
</picture>
```

**Database Query Optimization**:
```sql
-- Before: N+1 query problem
SELECT * FROM posts;
-- Then for each post:
SELECT * FROM users WHERE id = post.author_id;

-- After: JOIN query
SELECT posts.*, users.name 
FROM posts 
LEFT JOIN users ON posts.author_id = users.id;
```

**Caching Strategy**:
```javascript
// API response caching
app.get('/api/data', async (req, res) => {
  const cacheKey = 'api:data';
  const cached = await redis.get(cacheKey);
  
  if (cached) {
    return res.json(JSON.parse(cached));
  }
  
  const data = await fetchData();
  await redis.setex(cacheKey, 3600, JSON.stringify(data)); // 1 hour
  res.json(data);
});
```

---

### Measurement & Validation

**Tools**:
- Lighthouse (automated audits)
- Chrome DevTools Performance tab
- webpack-bundle-analyzer
- React DevTools Profiler
- New Relic / Datadog (production monitoring)

**Before/After Comparison**:
```markdown
| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Load Time | 4.2s | 1.8s | -57% ✅ |
| FCP | 2.1s | 0.9s | -57% ✅ |
| Bundle | 1.2MB | 480KB | -60% ✅ |
| Lighthouse | 65 | 92 | +27pts ✅ |
```

**Regression Testing**:
```javascript
// Performance budget
const budgets = {
  loadTime: 2000, // ms
  bundleSize: 500000, // bytes
  fcp: 1000 // ms
};

// Fail build if budget exceeded
if (metrics.loadTime > budgets.loadTime) {
  throw new Error('Performance budget exceeded!');
}
```

---

### Monitoring & Alerts

**Real User Monitoring**:
```javascript
// Track Core Web Vitals
new PerformanceObserver((list) => {
  list.getEntries().forEach((entry) => {
    analytics.track('web-vital', {
      name: entry.name,
      value: entry.value
    });
  });
}).observe({ entryTypes: ['largest-contentful-paint', 'first-input'] });
```

**Alerts**:
- Load time > 3s for 5 minutes
- Error rate > 1%
- Memory usage > 200MB

---

### Success Criteria

- [ ] All target metrics achieved
- [ ] Lighthouse score ≥ 90
- [ ] No performance regressions
- [ ] Monitoring and alerts configured
- [ ] Documentation updated

---

### 🚀 Ready to Optimize?

Start with Phase 1 to establish baseline metrics before making changes.
```

---

## Performance Optimization Checklist

### Frontend
- [ ] Minimize JavaScript bundle
- [ ] Optimize images (WebP, lazy load)
- [ ] Enable compression
- [ ] Use CDN
- [ ] Code splitting
- [ ] Tree shaking
- [ ] Remove unused CSS

### Backend
- [ ] Database indexing
- [ ] Query optimization
- [ ] Caching (Redis/Memcached)
- [ ] Connection pooling
- [ ] Async processing
- [ ] API pagination
- [ ] Response compression

### Network
- [ ] HTTP/2 or HTTP/3
- [ ] Browser caching
- [ ] Preconnect/prefetch
- [ ] Reduce redirects
- [ ] Optimize DNS lookup

---

---

## Execution with Subagents

Performance optimization plans work well with `/execute-plan` and **subagent methodology**.

**Reference**: `.claude/skills/methodology/executing-plans/SKILL.md`

### Performance Optimization with Subagents

```
Phase 1: Profiling & Measurement
  → Subagent runs profilers
  → Identifies bottlenecks
  → Establishes baselines
  → Returns: Performance report
  ↓
Review: Bottlenecks identified correctly?
  ↓
Phase 2: Targeted Optimizations
  → Fresh subagent optimizes bottleneck 1
  → Measures improvement
  → Keeps tests passing
  → Returns: Optimized code + metrics
  ↓
Review: Performance improved? Tests pass?
  ↓
Phase 3: More Optimizations
  → Fresh subagent tackles bottleneck 2
  → Measures improvement
  → Returns: Results
  ↓
Phase 4: Verification
  → Subagent runs full benchmark suite
  → Verifies no regressions
  → Documents improvements
  ↓
Complete! ✅ Measurably faster
```

### Why Subagents for Performance?

- ✅ **Focused optimization**: One bottleneck at a time
- ✅ **Measured results**: Each phase includes benchmarks
- ✅ **Safety**: Tests verify correctness maintained
- ✅ **Isolated changes**: Easy to revert if optimization backfires
- ✅ **Data-driven**: Reviews check actual perf improvements

### Critical for Performance Work

When using `/execute-plan` for performance:

1. **Measure BEFORE and AFTER** each phase
2. **Tests MUST pass** (correctness > speed)
3. **Document metrics** (load time, memory, etc.)
4. **One optimization per phase** (easier to debug)
5. **Profile before optimizing** (no guessing)

### Example

```bash
# Generate performance plan
/plan-performance --save=plans/optimize-dashboard.md "speed up dashboard load time"

# Execute with measurements
/execute-plan plans/optimize-dashboard.md
# Each phase: profile → optimize → measure → review
```

---

## Related Commands

```bash
/plan           # General planning
/optimize       # Quick optimization tips
/debug          # Debug performance issues
```
