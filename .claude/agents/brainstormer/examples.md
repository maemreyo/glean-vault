# Brainstorming Examples

This file contains complete worked examples showing how the Brainstormer Agent analyzes real problems.

<!-- Last updated: 2024-12-15 -->
<!-- Note: Technologies and patterns evolve. Review examples periodically. -->

---

## Example 1: API Caching Design

### User Request
"Design a caching strategy for our REST API. We're seeing high database load and slow response times."

### Step 0: Context Gathering
**Tools used:**
- `Glob("src/api/**/*.{js,ts}")` - Found 45 API endpoint files
- `Read("src/api/users/controller.ts")` - Sample endpoint makes 3 DB queries per request
- `Read("package.json")` - Currently using Express, PostgreSQL, no caching layer
- `WebSearch("REST API caching best practices 2024")` - Redis most common, CDN for static data

### Step 1: Understand the Problem
- **Core challenge**: High DB load causing 2-3s response times (target: <200ms)
- **Constraints**: 
  - Budget: $500/month for caching infrastructure
  - Team expertise: JavaScript, basic DevOps
  - Data: Mix of user-specific and frequently-accessed public data
- **Assumed constraint challenged**: "Must cache everything" → Actually only 20% of endpoints cause 80% of load

### Step 2: Generate Options

#### Option 1: Redis In-memory Cache
**Description**: Add Redis layer between API and PostgreSQL
**Pros**: 
- Fast (sub-ms lookups)
- Mature ecosystem
- Flexible TTL strategies
**Cons**: 
- Additional infrastructure cost (~$200/month)
- Cache invalidation complexity
- Learning curve for team
**Effort**: Medium (2-3 weeks)

#### Option 2: CDN Edge Caching
**Description**: Use Cloudflare/CloudFront to cache responses at edge
**Pros**: 
- Extremely fast for end-users
- Handles geographic distribution
- Low cost (~$50/month)
**Cons**: 
- Only works for public, non-personalized data
- Cache purging takes minutes
- Limited control over invalidation
**Effort**: Low (1 week)

#### Option 3: Application-level In-memory Cache
**Description**: Use Node.js `node-cache` or similar for in-process caching
**Pros**: 
- Zero infrastructure cost
- Simple implementation
- No network latency
**Cons**: 
- Cache not shared across instances (inconsistency)
- Memory limited per instance
- Lost on deployment
**Effort**: Low (3-4 days)

#### Option 4: Hybrid (Redis + CDN)
**Description**: Redis for user-specific, CDN for public data
**Pros**: 
- Best of both worlds
- Optimizes costs (CDN cheaper for public data)
- Clear separation of concerns
**Cons**: 
- Most complex to implement
- Two systems to monitor
- Higher initial effort
**Effort**: High (4-5 weeks)

#### Option 5: Database Query Optimization (No cache)
**Description**: Add indexes, optimize queries, use materialized views
**Pros**: 
- No new infrastructure
- Addresses root cause
- No cache invalidation issues
**Cons**: 
- May not achieve target latency
- Limited scalability ceiling
- Still hits DB for every request
**Effort**: Medium (2-3 weeks)

### Wild Card Ideas
- **GraphQL with DataLoader**: Batch and cache in single request cycle
- **Pre-compute common queries**: Nightly job to populate cache with popular data
- **WebSocket + Push updates**: Eliminate need for frequent polling requests

### Step 3: Comparison Matrix

| Criteria | Redis | CDN | In-memory | Hybrid | DB Optimization |
|----------|-------|-----|-----------|--------|-----------------|
| Latency Improvement | 5 | 5 | 4 | 5 | 3 |
| Cost | 3 | 5 | 5 | 2 | 5 |
| Complexity | 3 | 4 | 5 | 2 | 4 |
| Scalability | 5 | 5 | 2 | 5 | 3 |
| Team Fit | 4 | 4 | 5 | 3 | 5 |
| **Total** | **20** | **23** | **21** | **17** | **20** |

### Recommendation: Start with CDN + DB Optimization, then add Redis

**Rationale**:
1. **Phase 1 (Week 1-2)**: Implement CDN for public endpoints (40% of traffic) + optimize slow queries
   - Quick wins with minimal risk
   - Learn from production before bigger investment
2. **Phase 2 (Week 3-5)**: Add Redis for user-specific endpoints if targets not met
   - Data-driven decision based on Phase 1 metrics
   - Justified infrastructure cost with clear ROI

### Validation Artifact (Pseudo-code)

```javascript
// Phase 1: CDN + Optimization
// In API middleware
app.use((req, res, next) => {
  if (isPublicEndpoint(req.path)) {
    res.set('Cache-Control', 'public, max-age=300'); // 5min CDN cache
  } else {
    res.set('Cache-Control', 'private, no-cache');
  }
  next();
});

// Optimized query example
// Before: 3 separate queries
// After: 1 JOIN query with index
const getUserWithPosts = await db.query(`
  SELECT u.*, array_agg(p.*) as posts
  FROM users u
  LEFT JOIN posts p ON p.user_id = u.id
  WHERE u.id = $1
  GROUP BY u.id
`, [userId]);

// Phase 2: Redis layer (if needed)
const cachedUser = await redis.get(`user:${userId}`);
if (cachedUser) return JSON.parse(cachedUser);

const dbUser = await getUserWithPosts(userId);
await redis.setex(`user:${userId}`, 3600, JSON.stringify(dbUser));
return dbUser;
```

---

## Example 2: Performance Optimization

### User Request
"Our application is slow under load. 5,000 concurrent users crashes the system."

### Context Gathering
- `Read("monitoring/grafana-dashboard.json")` - CPU spikes to 95%, DB connections maxed
- `Read("src/services/report-generator.ts")` - Heavy computation in request path
- `WebSearch("Node.js performance bottlenecks 2024")` - Common issues: synchronous ops, memory leaks, N+1 queries

### Approaches Generated

1. **Database Layer**: Connection pooling, read replicas, query optimization
2. **Code Layer**: Move heavy computation to background jobs, async processing
3. **Infrastructure Layer**: Horizontal scaling, load balancing, CDN
4. **Caching Layer**: Redis for computed results, reduce DB load

### Recommendation
**Immediate**: Move report generation to async queue (BullMQ) - Highest impact/effort ratio  
**Short-term**: Add read replicas for queries  
**Long-term**: Implement caching for frequently-generated reports  

### Validation Artifact
```javascript
// Before: Synchronous in request
app.get('/report/:id', async (req, res) => {
  const report = await generateReport(req.params.id); // 30+ seconds!
  res.json(report);
});

// After: Async job
app.post('/report/:id/generate', async (req, res) => {
  const job = await reportQueue.add({ reportId: req.params.id });
  res.json({ jobId: job.id, status: 'processing' });
});

app.get('/report/:id/status', async (req, res) => {
  const job = await reportQueue.getJob(req.params.id);
  res.json({ status: job.status, progress: job.progress });
});
```

---

## Example 3: Architecture Decision

### User Request
"Should we move to microservices? Our monolith is getting hard to manage."

### Context Gathering
- Team size: 8 developers
- Codebase: 150k LOC, 2 years old
- Current pain: Deployments risky, modules tightly coupled, test suite takes 20 minutes

### Approaches Generated

1. **Stay Monolith**: Refactor into modules, improve boundaries
2. **Microservices**: Full decomposition into 8-10 services
3. **Modular Monolith**: Enforce module boundaries, prepare for extraction
4. **Strangler Pattern**: Gradually extract services starting with most independent

### Decision Guide

| Team Size | Recommendation |
|-----------|----------------|  
| < 10 devs | Modular Monolith |
| 10-30 devs | Selective Microservices (2-4 services) |
| 30+ devs | Full Microservices |

**Recommendation for this case**: **Modular Monolith** with preparation for future extraction

### Validation Artifact
```
src/
├── modules/
│   ├── users/
│   │   ├── domain/      # Business logic (no external deps)
│   │   ├── api/         # Controllers
│   │   └── infra/       # DB, external services
│   ├── billing/
│   └── reporting/
├── shared/
│   └── kernel/          # Shared primitives only
└── app.ts               # Wiring
```

Each module has:
- Clear public API (`index.ts`)
- No cross-module imports (except via public API)
- Independent tests
- Deployment ability (when ready to extract)

---

## Example 4: Interactive Mode - Hide/Show Background Feature

### User Request (Interactive Mode)
```bash
/brainstorm --interactive "hide/show background in screenshot app"
```

### Agent Response: Clarifying Questions

```markdown
## Clarifying Questions: Hide/Show Background Feature

Before generating solutions, I need to understand:

1. **State Preservation**: When hiding background, should padding and corner radius:
   a) Remain functional with transparent background
   b) Be disabled and set to 0
   c) Other preference?

2. **Re-enable Behavior**: When showing background again:
   a) Restore previous padding/corner radius values
   b) Reset to default values
   c) User manually sets again?

3. **Visual Effect**: Should the background:
   a) Fade to transparent (keep element, change opacity)
   b) Remove completely (hide element)

4. **User Expectations**: Do you anticipate different users wanting different behaviors? (e.g., some want 1a, others want 1b)

5. **Performance**: Are there any performance concerns with frequent hide/show toggling?

Please answer briefly (e.g., "1b, 2a, 3a, 4: yes") or type "auto" to let me decide.
```

### User Answers
"Hmm, actually both 1a and 1b make sense for different users. So 4: yes"

### Agent Follow-up

```markdown
Great insight! I see that different users have different needs.

**Clarification**: Should we:
- a) Provide a setting/toggle for users to choose between Mode A (transparent) and Mode B (disabled)?
- b) Create two separate buttons/controls?
- c) Default to one mode but make it easy to switch later?

This will help me design the best hybrid solution.
```

### User Answers
"a) Provide a setting"

### Generated Solutions (After Clarification)

#### Recommended: Hybrid Solution with User Preference

**Description**: Implement both modes with a setting toggle

```typescript
// Settings
interface BackgroundSettings {
  hideMode: 'transparent' | 'disable'; // User preference
  preserveState: boolean; // Restore on re-enable
}

// State management
interface BackgroundState {
  visible: boolean;
  padding: number;
  cornerRadius: number;
  // Store original values
  _previousPadding?: number;
  _previousCornerRadius?: number;
}

// Hide logic
function hideBackground(settings: BackgroundSettings, state: BackgroundState) {
  state.visible = false;
  
  if (settings.hideMode === 'disable') {
    // Mode B: Disable controls
    if (settings.preserveState) {
      state._previousPadding = state.padding;
      state._previousCornerRadius = state.cornerRadius;
    }
    state.padding = 0;
    state.cornerRadius = 0;
    disableControls(['padding', 'cornerRadius']);
  } else {
    // Mode A: Transparent background
    backgroundElement.style.opacity = '0';
    // Controls remain functional
  }
}

// Show logic
function showBackground(settings: BackgroundSettings, state: BackgroundState) {
  state.visible = true;
  
  if (settings.hideMode === 'disable') {
    // Restore state
    if (settings.preserveState && state._previousPadding !== undefined) {
      state.padding = state._previousPadding;
      state.cornerRadius = state._previousCornerRadius;
    }
    enableControls(['padding', 'cornerRadius']);
  } else {
    // Restore opacity
    backgroundElement.style.opacity = '1';
  }
}
```

**Edge Cases Handled**:
- ✅ State transitions (hide → show → hide again)
- ✅ Setting changes mid-session (switch from Mode A to Mode B)
- ✅ Default values for new users
- ✅ Migration from old version (if exists)

**Trade-offs**:
- (+) Satisfies both user groups
- (+) Flexible for future needs
- (-) Slightly more complex implementation
- (-) Need to design settings UI

**Alternatives Considered**:
1. **Mode A only**: Simpler but doesn't satisfy users who want clean screenshots
2. **Mode B only**: Cleaner but limits creative use of padding/radius
3. **Two separate buttons**: More UI clutter, confusing

**Why Hybrid Wins**: User feedback indicated real need for both modes. Small additional complexity is worth better UX.

---

## Example 5: Edge Case Discovery

### Problem
"Add dark mode toggle to app"

### Clarifying Questions (Auto-generated)

1. **State Persistence**: Should dark mode preference be:
   - Saved per user account?
   - Saved in browser localStorage?
   - Reset on browser close?

2. **Transition**: Should the theme switch be:
   - Instant?
   - Animated (fade/slide)?
   - Require page reload?

3. **System Preference**: Should we:
   - Respect OS dark mode setting?
   - Ignore OS setting, use app preference only?
   - OS default, allow override?

4. **Content Adaptation**: Are there images/assets that need dark mode versions?

5. **Third-party**: Any third-party widgets that might not support dark mode?

### Edge Cases Identified from Questions

- **Browser compatibility**: Some CSS variables not supported in old browsers
- **Flash of unstyled content**: Page loads before theme applied
- **Embedded content**: iframes, third-party widgets
- **Print mode**: Should print use light theme always?
- **Accessibility**: Ensure sufficient contrast in both modes

### Solutions Generated (With Edge Cases)

Each solution includes:
- Main implementation
- Edge case handling
- Fallback strategies
- Testing approach

---

## Template: Clarifying Questions Example

Use this template when in `--clarify` or `--interactive` mode:

```markdown
## Clarifying Questions: {{ PROBLEM }}

Before generating solutions, I need to understand:

1. **State Management**: [Question about state transitions]
   a) [Option A]
   b) [Option B]
   c) [Other?]

2. **User Expectations**: [Question about different user needs]
   - [Scenario A]
   - [Scenario B]
   - Could both scenarios exist?

3. **Edge Cases**: [Question about error/edge scenarios]
   - [What if X happens?]
   - [What if Y changes?]

4. **Dependencies**: [Question about affected features]
   - [Are there other features that depend on this?]
   - [Will this change impact X?]

5. **Assumptions**: [Question to validate assumptions]
   - [Are we solving the right problem?]
   - [Is constraint X real or assumed?]

Please answer briefly or type "auto" for best practices.
```

---

## Key Learnings from Examples

### Pattern 1: Hybrid Solutions Often Best
When users indicate multiple valid scenarios (Example 4), hybrid solutions that support both modes usually provide better UX despite slightly higher complexity.

### Pattern 2: State Transitions Critical
Always ask: "What happens when feature is re-enabled?" (Examples 1, 4)

### Pattern 3: Edge Cases Through Questions
Interactive mode reveals edge cases users haven't considered (Example 5)

### Pattern 4: Document Assumptions
When requirements aren't fully clarified, document assumptions clearly (All examples)

### Pattern 5: Validate with Artifacts
Pseudo-code/diagrams prove feasibility and reveal implementation challenges early (All examples)
