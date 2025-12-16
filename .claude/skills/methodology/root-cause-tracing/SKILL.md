---
name: root-cause-tracing
description: Advanced debugging technique for deep execution stack bugs. Systematically trace backward through call chains to identify original triggers, not just symptoms. Core principle: "The error location is rarely the bug location." Use when errors occur far from entry points, data corruption has unclear source, or "it was already wrong by the time it got here."
---

# Root Cause Tracing

## Quick Start

1. Document the error message and location
2. Trace backward through the call chain level by level
3. Find where the problem originated (not where it appeared)
4. Fix at the source and add validation to prevent recurrence

## Instructions

### When to Use This Skill
✅ **Perfect for**:
- Errors occur far from entry points
- Data corruption with unclear source
- "It was already wrong by the time it got here"
- Stack traces show multiple levels of indirection

❌ **NOT for**:
- Simple syntax errors (fix directly)
- Missing dependencies (install directly)
- Clear, single-location issues

### Core Principle
**"The error location is rarely the bug location."**

Always trace backward until you find the original trigger.

### Step-by-Step Process

#### Step 1: Document the Error
Capture exactly what you observe:
```markdown
Error: "Cannot insert NULL into column 'user_id'"
Location: database-repository.ts:156
Stack trace: [full trace]
Context: [what was happening]
```

#### Step 2: Find Immediate Cause
Locate the code directly responsible:
```typescript
// database-repository.ts:156
async function insertOrder(order: Order) {
  await db.insert('orders', {
    user_id: order.userId,  // <- This is NULL
    // ...
  });
}
```

#### Step 3: Trace One Level Up
Who called this? What did they pass?
```typescript
// order-service.ts:89
async function createOrder(orderData: OrderData) {
  const order = new Order(orderData);
  await repository.insertOrder(order);  // <- Called from here
}
```

#### Step 4: Continue Tracing Back
Keep going up the call chain until entry point:
```typescript
// order-controller.ts:45
async function handleCreateOrder(req: Request) {
  const orderData = req.body;  // <- Missing validation here!
  await orderService.createOrder(orderData);
}
```

#### Step 5: Identify Root Cause
The actual bug is often at the entry point:
- No input validation
- Missing null checks
- Incorrect data transformation
- Wrong assumptions about input

### Instrumentation When Stuck

If manual tracing fails, add diagnostic logging:

#### Strategic Console.error
```typescript
console.error('[TRACE] Entering function:', {
  functionName: 'createOrder',
  input: orderData,
  hasUserId: !!orderData.userId,
  stack: new Error().stack
});
```

#### Stack Trace Capture
```typescript
function setUserId(id: string | null) {
  if (id === null) {
    console.error('[TRACE] userId set to null from:', new Error().stack);
  }
  this.userId = id;
}
```

### Find the Output
```bash
# Run and grep for traces
npm test 2>&1 | grep "\[TRACE\]"
```

### Apply the Fix

1. **Fix at the source** - Don't patch symptoms
2. **Add validation** - Prevent recurrence
3. **Add tests** - Prove the fix works
4. **Consider defense-in-depth** - Validate at multiple layers

## Examples

### Example 1: Database Constraint Error
```typescript
// Error: "Cannot insert NULL into column 'user_id'"
// Appears in: database-repository.ts:156

// ❌ WRONG FIX - Patch the symptom
async function insertOrder(order: Order) {
  if (!order.userId) {
    order.userId = 'default'; // This treats symptom!
  }
  await db.insert('orders', order);
}

// ✅ RIGHT FIX - Find and fix root cause
// Traced back to: controller.ts missing validation
async function handleCreateOrder(req: Request) {
  if (!req.body.userId) {
    throw new ValidationError('userId is required');
  }
  const order = await orderService.createOrder(req.body);
  return order;
}
```

### Example 2: Type Error in Service
```typescript
// Error: "Cannot read property 'name' of undefined"
// Appears in: user-service.ts:89

// Tracing backward:
// 1. user-service.ts:89 - console.log(user.name)
// 2. api-client.ts:45 - return user
// 3. database.ts:123 - SELECT * FROM users WHERE id = ?

// Root cause: Database query returned no rows, but code expected user

// Fix:
async function getUser(id: string): Promise<User> {
  const user = await db.query('SELECT * FROM users WHERE id = ?', [id]);
  if (!user) {
    throw new NotFoundError(`User ${id} not found`);
  }
  return user;
}
```

### Example 3: Memory Leak from Event Listener
```typescript
// Error: "Maximum call stack size exceeded"
// Appears in: random-component.ts after 1000 clicks

// Tracing reveals:
// Component adds listener on mount but never removes it
// Each click creates new listener

// Fix:
useEffect(() => {
  const handleClick = () => { /* ... */ };
  element.addEventListener('click', handleClick);

  // Cleanup on unmount
  return () => {
    element.removeEventListener('click', handleClick);
  };
}, []);
```

## Best Practices

### 🎯 Always Start with Documentation
- Write down the exact error message
- Capture full stack trace
- Note the context and conditions

### 🔍 Follow the Data Flow
- Don't jump to conclusions
- Trace step by step through the call chain
- Each step up might reveal more context

### 🛠️ Use Instrumentation Wisely
- Add `[TRACE]` tags for easy grepping
- Include function names and key variables
- Capture stack traces when values change unexpectedly

### ✅ Fix at the Source
- Never patch symptoms
- The goal is prevention, not treatment
- A single source fix prevents all future occurrences

### 🛡️ Add Defense-in-Depth
After finding root cause, add validation at multiple layers:
- Entry point: Validate user input
- Service layer: Assert invariants
- Database layer: Final safety checks

### 📝 Document Your Findings
- Write a brief RCA (Root Cause Analysis)
- Include the tracing path
- Note why symptoms appeared where they did
- This helps future debugging

## Requirements

### Prerequisites
- Access to full stack traces
- Ability to add temporary logging
- Understanding of the codebase architecture
- Permission to modify code at various layers

### Dependencies
- `defense-in-depth` skill (for adding validation layers)
- `systematic-debugging` skill (for general debugging approach)

### Tools
- IDE with "Go to Definition" support
- Grep/Find in files capability
- Debug console or terminal

## Common Root Cause Patterns

| Error Location | Likely Root Cause | Fix Strategy |
|----------------|-------------------|--------------|
| Database constraint | Missing input validation | Add validation at entry |
| Type error in service | API returned unexpected format | Add response validation |
| Null reference | Optional field not handled | Add null checks |
| Memory leak | Event listener not removed | Add cleanup on unmount |
| Timeout error | Missing error handling | Add retry/backoff logic |

---

## Core Principle

**"Trace backward through the call chain until you find the original trigger, then fix at the source."**

The error location is rarely the bug location:

```
User Input → Validation → Service → Repository → Database
    ^                                    ^
    |                                    |
 Bug HERE                         Error appears HERE
 (bad input allowed)              (constraint violation)
```

Fixing at the database layer treats the symptom. Fixing at validation prevents the bug.

---

## The Tracing Methodology

### Step 1: Identify Observable Error

Document exactly what you see:

```markdown
Error: "Cannot insert NULL into column 'user_id'"
Location: database-repository.ts:156
Stack trace: [full trace]
```

### Step 2: Locate Immediate Cause

Find the code directly responsible:

```typescript
// database-repository.ts:156
async function insertOrder(order: Order) {
  await db.insert('orders', {
    user_id: order.userId,  // <- This is NULL
    // ...
  });
}
```

### Step 3: Trace One Level Up

Who called this function? What did they pass?

```typescript
// order-service.ts:89
async function createOrder(orderData: OrderData) {
  const order = new Order(orderData);
  await repository.insertOrder(order);  // <- Called from here
}
```

### Step 4: Continue Tracing

Keep going up the call chain:

```typescript
// order-controller.ts:45
async function handleCreateOrder(req: Request) {
  const orderData = req.body;  // <- userId might be missing here
  await orderService.createOrder(orderData);
}
```

### Step 5: Find Original Source

Reach the entry point where the problem originated:

```typescript
// The real bug: No validation at entry point
// req.body.userId was never validated
```

---

## Instrumentation Techniques

When manual analysis fails, add diagnostic logging:

### Strategic Console.error

```typescript
// Add before suspicious operations
console.error('[TRACE] order-service.createOrder input:', {
  orderData,
  hasUserId: !!orderData.userId,
  stack: new Error().stack
});
```

### Stack Trace Capture

```typescript
// Capture where a value came from
function setUserId(id: string | null) {
  if (id === null) {
    console.error('[TRACE] userId set to null from:', new Error().stack);
  }
  this.userId = id;
}
```

### Boundary Logging

```typescript
// Log at every system boundary
async function callExternalApi(params) {
  console.error('[TRACE] API request:', params);
  const response = await fetch(url, params);
  console.error('[TRACE] API response:', response.status, await response.text());
  return response;
}
```

### Environment/Context Logging

```typescript
console.error('[TRACE] Context:', {
  env: process.env.NODE_ENV,
  timestamp: new Date().toISOString(),
  requestId: context.requestId,
  userId: context.user?.id
});
```

---

## Finding the Instrumentation Output

After adding logging:

```bash
# Run tests and grep for traces
npm test 2>&1 | grep "\[TRACE\]"

# Or run specific test
npm test -- --grep "failing test" 2>&1 | grep "\[TRACE\]"
```

---

## Common Root Cause Locations

| Where Error Appears | Where Bug Often Is |
|--------------------|--------------------|
| Database constraint | Input validation |
| Type error in service | Data transformation |
| Null reference | Optional field handling |
| API timeout | Connection pool config |
| Memory error | Resource cleanup |

---

## Defense-in-Depth Integration

After finding root cause, add validation at multiple layers:

```typescript
// Layer 1: Entry point
function handleRequest(req) {
  if (!req.body.userId) {
    throw new ValidationError('userId required');
  }
}

// Layer 2: Service
function createOrder(data) {
  assert(data.userId, 'userId must be provided to createOrder');
}

// Layer 3: Repository
function insertOrder(order) {
  assert(order.userId, 'Cannot insert order without userId');
}
```

See `defense-in-depth` skill for comprehensive approach.

---

## Critical Warning

**"NEVER fix just where the error appears."**

Fixing at the error location:
- Treats symptom, not cause
- Leaves bug available to trigger from other paths
- Creates false confidence
- Guarantees the bug will return

Fixing at the source:
- Prevents the bug entirely
- Protects all code paths
- Creates robust system
- Actually solves the problem

---

## Tracing Checklist

- [ ] Error message and location documented
- [ ] Immediate cause identified
- [ ] Call chain traced backward
- [ ] Original source found
- [ ] Instrumentation added if needed
- [ ] Fix applied at source (not symptom)
- [ ] Defense-in-depth validation added
- [ ] Test proves fix works

---
