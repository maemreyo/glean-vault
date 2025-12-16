# Debugging Examples

This document provides detailed real-world examples of systematic debugging in action.

## Example 1: Production API Timeout Error

### Initial Report
"API endpoint /api/users is timing out in production"

### Phase 1: Root Cause Investigation

#### Error Analysis
```bash
Error: Request timeout of 30000ms exceeded
  at Promise.timeout (/app/node_modules/axios/lib/helpers/timeout.js:32:11)
  at /app/src/api/users.js:45:20
  at processTicksAndRejections (internal/process/task_queues.js:97:5)

Stack trace shows:
- Timeout occurs in axios request
- Location: src/api/users.js:45
- No specific error message, just timeout
```

#### Reproduction Steps
```markdown
Steps to reproduce:
1. Call GET /api/users?page=10
2. Request takes >30 seconds
3. Returns timeout error
4. Only affects pages 8-12
5. Earlier pages work fine
```

#### Recent Changes Analysis
```bash
# Check recent deployments
git log --oneline --since="2 days ago"
a1b2c3d (HEAD) feat: Add user filtering
d4e5f6g fix: Update database indexes
h7i8j9k refactor: Optimize user queries
```

#### Evidence Gathering
```bash
# Database query log
SELECT * FROM users WHERE active = true LIMIT 100 OFFSET 800;
-- Execution time: 45.2 seconds

# Database indexes
SHOW INDEX FROM users;
-- No index on 'active' column
-- No composite index on (active, created_at)
```

### Phase 2: Pattern Analysis

#### Find Working Reference
```javascript
// Working endpoint: GET /api/recent-users
// Code: src/api/recent-users.js
async function getRecentUsers() {
  const query = `
    SELECT * FROM users
    WHERE created_at > NOW() - INTERVAL '7 days'
    AND active = true
    ORDER BY created_at DESC
    LIMIT 50
  `;
  // Uses index on created_at
  // Returns in 50ms
}
```

#### Key Differences Identified
1. Working query uses `created_at` index
2. Broken query uses `OFFSET` without proper indexing
3. No index on `active` column
4. Query optimizer does full table scan

### Phase 3: Hypothesis Testing

#### Hypothesis
"Query timeout occurs because OFFSET pagination without proper indexing causes full table scan on large dataset"

#### Test Hypothesis
```sql
-- Explain query plan
EXPLAIN ANALYZE SELECT * FROM users WHERE active = true LIMIT 100 OFFSET 800;
-- Result: Seq Scan on users (cost=0.00..12345.67 rows=100 width=245)
--          Filter: (active = true)
--          Rows Removed by Filter: 987654
--          Actual time: 0.123..45234.567

-- Test with index
CREATE INDEX CONCURRENTLY idx_users_active_created ON users(active, created_at);
EXPLAIN ANALYZE SELECT * FROM users WHERE active = true LIMIT 100 OFFSET 800;
-- Result: Index Scan using idx_users_active_created
--          Actual time: 0.123..12.456
```

### Phase 4: Implementation

#### Write Test First
```javascript
describe('User API Pagination', () => {
  it('should return page 10 within 1 second', async () => {
    const start = Date.now();
    const response = await request(app)
      .get('/api/users?page=10')
      .expect(200);
    const duration = Date.now() - start;
    expect(duration).toBeLessThan(1000);
    expect(response.body.users).toBeDefined();
  });
});
```

#### Implement Fix
```javascript
// src/api/users.js - Add cursor-based pagination
async function getUsers(page = 1, cursor = null) {
  const limit = 100;
  let query = `
    SELECT * FROM users
    WHERE active = true
  `;

  if (cursor) {
    query += ` AND created_at < '${cursor}'`;
  }

  query += ` ORDER BY created_at DESC LIMIT ${limit}`;

  return await db.query(query);
}
```

#### Verify No Regressions
```bash
npm test -- test/api/users.test.js
# All tests pass

# Load test
artillery run load-test.yml
# 99th percentile: 120ms (previously 30s timeout)
```

## Example 2: Frontend Memory Leak

### Initial Report
"Application becomes unresponsive after 30 minutes of use"

### Phase 1: Root Cause Investigation

#### Error Analysis
```javascript
// Browser console errors
Error: Out of memory
  at allocate (native)
  at Array.push (<anonymous>)

// Performance tab shows:
- Heap size: 1.2GB and growing
- Retained nodes: 2.3M
- 50,000+ detached DOM nodes
```

#### Reproduction Steps
```markdown
Steps to reproduce:
1. Open dashboard page
2. Navigate between tabs every 30 seconds
3. Memory increases by ~50MB per navigation
4. After 30 minutes, tab freezes
```

#### Evidence Gathering
```javascript
// Added memory debugging
setInterval(() => {
  const nodes = document.querySelectorAll('*').length;
  const memory = performance.memory;
  console.log(`Nodes: ${nodes}, Memory: ${memory.usedJSHeapSize / 1024 / 1024}MB`);
}, 5000);

// Output shows steady increase:
// Nodes: 15000, Memory: 45MB
// Nodes: 30000, Memory: 95MB
// Nodes: 45000, Memory: 145MB
```

### Phase 2: Pattern Analysis

#### Find Working Reference
```javascript
// Working page: Settings page
// Uses component lifecycle cleanup
class SettingsComponent extends React.Component {
  componentWillUnmount() {
    this.subscriptions.forEach(sub => sub.unsubscribe());
    this.timer = clearInterval(this.timer);
  }
}
```

#### Key Differences Identified
1. Dashboard components don't clean up subscriptions
2. Event listeners added but never removed
3. WebSocket connections accumulate
4. No component unmount cleanup

### Phase 3: Hypothesis Testing

#### Hypothesis
"Memory leak caused by accumulating event listeners and subscriptions without cleanup"

#### Test Hypothesis
```javascript
// Test component cleanup
function createTestComponent() {
  const component = mount(<DashboardComponent />);
  const initialListeners = getEventListenerCount();

  component.unmount();

  const finalListeners = getEventListenerCount();
  expect(finalListeners).toBe(initialListeners);
}

// Test fails - listeners remain
```

### Phase 4: Implementation

#### Write Test First
```javascript
describe('Component Memory Management', () => {
  it('should clean up all subscriptions on unmount', () => {
    const component = mount(<DashboardComponent />);
    const initialSubscriptions = getSubscriptionCount();

    component.unmount();
    const finalSubscriptions = getSubscriptionCount();

    expect(finalSubscriptions).toBe(initialSubscriptions);
  });
});
```

#### Implement Fix
```javascript
// src/components/Dashboard.jsx
class DashboardComponent extends React.Component {
  constructor(props) {
    super(props);
    this.subscriptions = [];
    this.timers = [];
  }

  componentDidMount() {
    // Track all subscriptions
    this.dataSub = dataService.subscribe(this.handleDataUpdate);
    this.subscriptions.push(this.dataSub);

    // Track all timers
    this.refreshTimer = setInterval(this.refreshData, 30000);
    this.timers.push(this.refreshTimer);
  }

  componentWillUnmount() {
    // Clean up all resources
    this.subscriptions.forEach(sub => sub.unsubscribe());
    this.timers.forEach(timer => clearInterval(timer));

    this.subscriptions = [];
    this.timers = [];
  }
}
```

#### Verify No Regressions
```javascript
// Memory test
async function memoryTest() {
  for (let i = 0; i < 100; i++) {
    const component = mount(<DashboardComponent />);
    component.unmount();
  }

  const finalMemory = performance.memory.usedJSHeapSize;
  expect(finalMemory).toBeLessThan(100 * 1024 * 1024); // <100MB
}
```

## Example 3: Intermittent Test Failure

### Initial Report
"Integration test fails randomly, 1 in 10 runs"

### Phase 1: Root Cause Investigation

#### Error Analysis
```bash
FAIL test/integration/payment.test.js
  Payment Flow
    ✕ Should process payment successfully (123ms)

  Expected: "success"
  Received: "timeout"
  at PaymentService.process (test/integration/payment.test.js:45:28)

# Stack trace varies between runs
# Sometimes fails at different assertions
```

#### Reproduction Pattern
```bash
# Run test 100 times
for i in {1..100}; do
  npm test -- test/integration/payment.test.js
done

# Results:
# 90 passes, 10 failures
# Failures occur at random points
# No pattern in timing
```

#### Evidence Gathering
```javascript
// Added timing instrumentation
describe('Payment Flow', () => {
  beforeEach(() => {
    this.startTime = Date.now();
  });

  afterEach(() => {
    const duration = Date.now() - this.startTime;
    console.log(`Test duration: ${duration}ms`);
  });
});

// Output shows wide variance:
// Test duration: 45ms
// Test duration: 234ms
// Test duration: 567ms
// Test duration: 1203ms  <-- failures occur here
```

### Phase 2: Pattern Analysis

#### Find Working Reference
```javascript
// Working stable test: test/integration/auth.test.js
// Uses explicit waits and cleanup
afterEach(async () => {
  await cleanupDatabase();
  await resetMockServers();
  await clearCaches();
});
```

#### Key Differences Identified
1. Payment test doesn't clean up database
2. Race condition between test setup
3. Mock responses sometimes delayed
4. No explicit wait for async operations

### Phase 3: Hypothesis Testing

#### Hypothesis
"Test fails due to race condition between database cleanup and test setup"

#### Test Hypothesis
```javascript
// Add explicit waits
test('should process payment successfully', async () => {
  // Ensure clean state
  await ensureDatabaseClean();
  await waitForMocksReady();

  const result = await paymentService.process(testPayment);
  expect(result.status).toBe('success');
});

// Test passes 100/100 times
```

### Phase 4: Implementation

#### Write Test First
```javascript
describe('Payment Flow', () => {
  beforeEach(async () => {
    await setupCleanTestEnvironment();
    await startMockServers();
  });

  afterEach(async () => {
    await cleanupDatabase();
    await stopMockServers();
    await verifyNoPendingOperations();
  });
});
```

#### Implement Fix
```javascript
// test/helpers/setup.js
export async function setupCleanTestEnvironment() {
  // Clear all async operations
  await Promise.all([
    clearDatabase(),
    resetMocks(),
    clearEventLoop(),
    clearCache()
  ]);

  // Wait for all to complete
  await new Promise(resolve => setImmediate(resolve));
}

// test/integration/payment.test.js
test('should process payment successfully', async () => {
  // Add explicit wait for services
  await waitForServicesReady();

  const result = await paymentService.process(testPayment);

  // Wait for all async operations
  await waitForAllPromises();

  expect(result.status).toBe('success');
});
```

#### Verify No Regressions
```bash
# Run 1000 times
npm run test:stable payment
# 1000/1000 passes

# Check test duration
# Now consistent: 45-55ms range
```

## Example 4: Database Deadlock

### Initial Report
"Random database errors during high load: 'deadlock detected'"

### Phase 1: Root Cause Investigation

#### Error Analysis
```sql
ERROR: deadlock detected
DETAIL: Process 12345 waits for ShareLock on transaction 67890;
         blocked by process 54321.
CONTEXT: while updating tuple in table "orders"
SQL statement: UPDATE orders SET status = 'processed' WHERE id = $1
```

#### Reproduction Pattern
```javascript
// Load test that triggers deadlock
async function simulateLoad() {
  const promises = [];
  for (let i = 0; i < 100; i++) {
    promises.push(updateOrder(i));
    promises.push(updateOrderInventory(i));
  }
  await Promise.all(promises);
}

// Fails ~30% of time
```

#### Evidence Gathering
```sql
-- Check query order
SELECT query FROM pg_stat_activity WHERE state = 'active';
-- Shows: UPDATE orders... and UPDATE inventory... running simultaneously

-- Check locks
SELECT * FROM pg_locks WHERE NOT granted;
-- Shows conflicting lock types
```

### Phase 2: Pattern Analysis

#### Find Working Reference
```sql
-- Working transaction pattern
BEGIN;
UPDATE inventory SET reserved = reserved + 1 WHERE product_id = 1;
UPDATE orders SET status = 'confirmed' WHERE id = 123;
COMMIT;

-- Always uses same order: inventory first, then orders
```

#### Key Differences Identified
1. Deadlock occurs when updating orders first
2. Working code always updates inventory first
3. No consistent ordering across operations
4. Multiple code paths with different update orders

### Phase 3: Hypothesis Testing

#### Hypothesis
"Deadlock occurs because different code paths update tables in different orders"

#### Test Hypothesis
```sql
-- Test consistent ordering
BEGIN;
UPDATE inventory SET quantity = quantity - 1 WHERE product_id = 1;
UPDATE orders SET status = 'processed' WHERE id = 123;
COMMIT;

-- No deadlock in 1000 attempts
```

### Phase 4: Implementation

#### Write Test First
```javascript
describe('Database Transaction Ordering', () => {
  it('should always update inventory before orders', async () => {
    const tx1 = db.transaction();
    const tx2 = db.transaction();

    // Both should follow same order
    await Promise.all([
      updateWithCorrectOrder(tx1, order1),
      updateWithCorrectOrder(tx2, order2)
    ]);

    expect(tx1.completed).toBe(true);
    expect(tx2.completed).toBe(true);
  });
});
```

#### Implement Fix
```javascript
// src/services/order.js
class OrderService {
  async processOrder(orderId) {
    const tx = await db.transaction();

    try {
      // Always lock inventory first
      await tx.query(
        'UPDATE inventory SET reserved = reserved + 1 WHERE product_id = $1',
        [order.productId]
      );

      // Then update order
      await tx.query(
        'UPDATE orders SET status = $1 WHERE id = $2',
        ['processed', orderId]
      );

      await tx.commit();
    } catch (error) {
      await tx.rollback();
      throw error;
    }
  }
}

// Create abstraction for consistent ordering
class TransactionManager {
  async updateInventoryAndOrder(order) {
    return this.withTransaction(async (tx) => {
      await this.lockInventory(tx, order.productId);
      await this.updateOrder(tx, order.id);
    });
  }
}
```

#### Verify No Regressions
```bash
# Load test with 10x normal load
npm run test:load-deadlock
# 0 deadlocks in 10,000 operations

# Performance impact
# Transaction time: 45ms (previously 40ms)
# Acceptable trade-off
```

## Common Debugging Patterns Summary

### 1. Divide and Conquer
- Isolate components
- Test individually
- Narrow down source

### 2. Working Backwards
- Start from error
- Trace execution path
- Identify deviation point

### 3. Pattern Matching
- Find working reference
- Compare implementations
- Identify key differences

### 4. Scientific Method
- Form hypothesis
- Create experiment
- Test and iterate

### 5. Binary Search
- Use git bisect
- Test incremental changes
- Find breaking change

### 6. Instrumentation
- Add logging at boundaries
- Measure performance
- Track resource usage