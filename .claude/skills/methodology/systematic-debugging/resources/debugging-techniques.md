# Debugging Techniques

This document covers specific debugging techniques and tool-specific guides.

## Browser Debugging

### Chrome DevTools

#### Breakpoints
```javascript
// Line breakpoint
debugger; // Pauses execution

// Conditional breakpoint
if (user.id === 123) {
  debugger;
}

// Log point (Chrome 73+)
// Right-click line > Add logpoint
console.log('User data:', user);
```

#### Network Debugging
```javascript
// Log all fetch requests
const originalFetch = window.fetch;
window.fetch = function(...args) {
  console.log('Fetch:', args[0], args[1]);
  return originalFetch.apply(this, args);
};

// Check failed requests
// Network tab > Status filter > 4xx/5xx
```

#### Memory Debugging
```javascript
// Take heap snapshot
// DevTools > Memory > Take snapshot

// Compare snapshots
// Snapshot 1 > Snapshot 2 > Comparison view

// Find detached nodes
// Memory > Retainers > Detached HTMLDivElement
```

#### Performance Debugging
```javascript
// Record performance profile
// DevTools > Performance > Record

// Analyze flame chart
// Look for long tasks ( >50ms )

// Check render performance
// Rendering > FPS meter
```

### Firefox Developer Tools

#### Memory Debugging
```javascript
// About:memory for detailed info
about:memory

// Measure memory usage
performance.measureUserAgentSpecificMemory();
```

## Node.js Debugging

### Built-in Debugger
```bash
# Run with debug flag
node --inspect index.js

# Connect with Chrome
chrome://inspect

# Use debugger statements
debugger;
```

### VS Code Debugging
```json
// .vscode/launch.json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Debug Node",
      "type": "node",
      "request": "launch",
      "program": "${workspaceFolder}/index.js",
      "env": {
        "NODE_ENV": "development"
      }
    }
  ]
}
```

### Advanced Node Debugging
```javascript
// Trace garbage collection
node --trace-gc index.js

// Debug async operations
node --trace-async index.js

// Track promises
node --trace-promises index.js

// Debug DNS
node --trace-dns index.js
```

## Database Debugging

### PostgreSQL
```sql
-- Explain query plan
EXPLAIN ANALYZE SELECT * FROM users WHERE active = true;

-- Check locks
SELECT * FROM pg_locks WHERE NOT granted;

-- Monitor queries
SELECT query, calls, total_time
FROM pg_stat_statements
ORDER BY total_time DESC;

-- Check connections
SELECT * FROM pg_stat_activity;

-- Log all queries
ALTER SYSTEM SET log_statement = 'all';
SELECT pg_reload_conf();
```

### MongoDB
```javascript
// Explain query
db.users.find({ active: true }).explain('executionStats');

// Check index usage
db.users.getIndexes();

// Monitor operations
db.setProfilingLevel(2);
db.system.profile.find().sort({ ts: -1 }).limit(5);
```

## API Debugging

### HTTP Debugging
```bash
# Curl with verbose
curl -v https://api.example.com/users

# Check headers
curl -I https://api.example.com/users

# Follow redirects
curl -L https://api.example.com/users

# Save response
curl -o response.json https://api.example.com/users
```

### WebSocket Debugging
```javascript
// Chrome DevTools > Network > WS tab
// Shows frames, timing, errors

// WebSocket debugging
const ws = new WebSocket('ws://localhost:3000');
ws.addEventListener('message', (event) => {
  console.log('Received:', event.data);
});
```

## Performance Debugging

### CPU Profiling
```bash
# Node.js CPU profile
node --prof index.js
node --prof-process isolate-*.log > processed.txt

# Flame graph generation
npm install -g clinic
clinic doctor -- node index.js
clinic flame -- node index.js
```

### Memory Profiling
```bash
# Heap snapshots
node --inspect --heap-prof index.js

# Memory leak detection
node --inspect index.js
# In Chrome: Memory > Heap snapshot
```

## Network Debugging

### TCP/IP Debugging
```bash
# Check open ports
netstat -tulpn | grep :3000

# Trace network path
traceroute google.com

# Check DNS resolution
nslookup google.com
dig google.com

# Monitor network traffic
tcpdump -i any port 3000
```

### HTTP/HTTPS Debugging
```bash
# SSL certificate check
openssl s_client -connect google.com:443

# HTTP headers
curl -v -H "Authorization: Bearer token" api.example.com

# Response time
curl -w "@curl-format.txt" -o /dev/null -s api.example.com

# curl-format.txt:
#      time_namelookup:  %{time_namelookup}\n
#         time_connect:  %{time_connect}\n
#      time_appconnect:  %{time_appconnect}\n
#     time_pretransfer:  %{time_pretransfer}\n
#        time_redirect:  %{time_redirect}\n
#   time_starttransfer:  %{time_starttransfer}\n
#                      ----------\n
#           time_total:  %{time_total}\n
```

## Debugging Tools

### Logging Frameworks
```javascript
// Winston logging
const winston = require('winston');

const logger = winston.createLogger({
  level: 'debug',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.errors({ stack: true }),
    winston.format.json()
  ),
  transports: [
    new winston.transports.File({ filename: 'error.log', level: 'error' }),
    new winston.transports.File({ filename: 'combined.log' })
  ]
});

// Debug logging
logger.debug('Processing request', { id: req.id, user: req.user });
logger.error('Database error', { error: err.message, stack: err.stack });
```

### Debug Utilities
```javascript
// Debug module
const debug = require('debug')('app:auth');

// Set debug environment
DEBUG=app:* node index.js

// Usage
debug('User login attempt', { email, ip });

// Conditional debugging
if (process.env.DEBUG) {
  console.log('Debug info:', data);
}
```

## Git Debugging

### Find Bug Introduction
```bash
# Binary search for bug
git bisect start
git bisect bad HEAD
git bisect good v1.0.0

# Check if current commit has bug
npm test
git bisect good  # or git bisect bad

# Skip commits
git bisect skip
```

### Track Changes
```bash
# Who changed this line?
git blame src/component.js

# History of file
git log -p src/component.js

# Changes between commits
git diff commit1 commit2 -- src/component.js
```

## Container Debugging

### Docker Debugging
```bash
# Inspect container
docker inspect container_id

# Execute in container
docker exec -it container_id bash

# View logs
docker logs container_id

# Debug with docker-compose
docker-compose run --rm app bash
```

### Kubernetes Debugging
```bash
# Pod logs
kubectl logs pod_name

# Execute in pod
kubectl exec -it pod_name -- bash

# Port forward
kubectl port-forward pod_name 3000:3000

# Describe pod
kubectl describe pod pod_name
```

## Testing for Bugs

### Reproduce Bug Script
```javascript
// reproduce-bug.js
async function reproduceBug() {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();

  // Enable request interception
  await page.setRequestInterception(true);
  page.on('request', request => {
    console.log('Request:', request.url());
    request.continue();
  });

  // Navigate and trigger bug
  await page.goto('http://localhost:3000');
  await page.click('#bug-button');

  // Wait for error
  await page.waitForSelector('.error-message');

  await browser.close();
}
```

### Property-Based Testing
```javascript
// Using fast-check
import fc from 'fast-check';

test('should handle all valid inputs', async () => {
  await fc.assert(
    fc.asyncProperty(fc.record({
      name: fc.string(),
      age: fc.integer(0, 120),
      email: fc.emailAddress()
    }), async (userData) => {
      const result = await createUser(userData);
      expect(result.id).toBeDefined();
      expect(result.name).toBe(userData.name);
    }),
    { numRuns: 1000 }
  );
});
```

## Debugging Checklists

### Before Debugging
- [ ] Clear error message documented
- [ ] Steps to reproduce written
- [ ] Environment noted
- [ ] Recent changes identified
- [ ] Baseline working version known

### During Debugging
- [ ] One change at a time
- [ ] Each change tested
- [ ] Root cause confirmed
- [ ] Fix minimal
- [ ] No unnecessary changes

### After Debugging
- [ ] Test added to prevent regression
- [ ] Root cause documented
- [ ] Related issues checked
- [ ] Documentation updated
- [ ] Fix reviewed

## Debugging Anti-patterns

### 1. Print Statement Debugging Gone Wrong
```javascript
// Bad: Too many console.log
console.log('1');
console.log('2');
console.log('3');
console.log(data);

// Good: Meaningful logs
console.log('User validation failed', {
  email: userData.email,
  errors: validationErrors
});
```

### 2. Ignoring Environment Differences
```javascript
// Bad: Works on my machine
// It works locally, must be production issue

// Good: Check differences
console.log('Node version:', process.version);
console.log('Platform:', process.platform);
console.log('Environment:', process.env.NODE_ENV);
```

### 3. Shotgun Debugging
```javascript
// Bad: Changing everything at once
try {
  change1();
  change2();
  change3();
  change4();
} catch (e) {
  // Which change caused the error?
}

// Good: Isolate changes
change1();
test();
change2();
test();
change3();
test();
```

## Debugging Best Practices

### 1. Reproduce Before Fixing
Always create a reliable reproduction case before attempting to fix.

### 2. Use Source Control
Commit working state before making changes. Use `git stash` for experiments.

### 3. Document Findings
Write down what you discover during debugging.

### 4. Fix Root Cause
Don't just patch symptoms. Find and fix the underlying issue.

### 5. Add Preventive Tests
Write tests that would have caught the bug initially.

### 6. Review Code Changes
Have someone else review your fix for potential side effects.

### 7. Monitor After Fix
Keep an eye on the fixed code to ensure no regressions.