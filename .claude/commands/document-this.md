# /document-this (The Historian) 📚

## Purpose

Intelligent documentation generation that focuses on **Context and Business Logic**, not just API signatures. It explains the "Why" and "How" using a "Reverse Engineering" approach.

**Required Skills**: `documentation-synthesis`
**References**:
- `.claude/skills/methodology/documentation-synthesis/SKILL.md`

## Usage

```bash
/document-this "Explain the Payment Module" --target=src/modules/payment
/document-this --readme --target=.
```

## Workflow

### Phase 1: UNDERSTAND (Explorer Subagent) 📖

**Goal**: Build a mental model of the code.

#### Subtask 1.1: Entity & Relationship Mapping (15 min)

**Context**:
- Code is a graph of entities. Document the graph.

**Steps**:
1. Scan target files.
2. Identify **Core Entities**: Classes, Interfaces, DB Models.
3. Trace **Relationships**: "Order *has many* Items", "User *belongs to* Org".
4. Identify **Services**: Who manipulates these entities?

**Example Output**:
```markdown
Entity Map:
- `Order` (Core)
- `PaymentGateway` (Service) - Processes Orders
- `InventoryService` (Service) - Deduced items
```

#### Subtask 1.2: Flow Tracing (15 min)

**Steps**:
1. Identify **Key Workflows** (e.g., "Checkout", "Refund").
2. Trace the entry point -> logic -> database/api.
3. Note identifying characteristics (async, transactions).

---

### Phase 2: SYNTHESIZE (Analyzer Subagent) ✍️

**Goal**: Structure the narrative.

#### Subtask 2.1: Logic Translation (20 min)

**Guidance**: Use `documentation-synthesis` skill.

**Steps**:
1. Translate **Code Logic** (`if (balance < amount) throw`) -> **Business Rule** ("Insufficient funds prevents checkout").
2. Identify **Consensus Algorithms** or complex math.
3. Identify **"Gotchas"**: Non-obvious constraints.

**Example Output**:
```markdown
Business Logic:
1. Refunds are only allowed within 30 days (Source: `RefundPolicy.ts:40`).
2. Admin approval required for >$10k (Source: `ApprovalService.ts`).
```

#### Subtask 2.2: Diagram Generation (5-10 min)

**Action**: Create Mermaid.js diagram definition for the Data Flow.

> **REVIEW GATE**: Does the documentation explain *Why* things happen, or just *What* code does? If just "It calls function A", RETRY.

---

### Phase 3: NARRATE (Writer Subagent) 🗣️

**Goal**: Polish and Format.

#### Subtask 3.1: Drafting (20 min)

**Steps**:
1. Write the **Overview**: One-paragraph summary (The "Elevator Pitch").
2. Write **Key Concepts**: Definitions.
3. Write **Usage**: Code examples.
4. Write **Architecture/Flow**: Insert Mermaid diagram.

#### Subtask 3.2: Formatting (10 min)

**Steps**:
1. Apply standardized Markdown formatting.
2. Link to actual source files (`[Link](file:...)`).
3. Add "Warning" callouts for Gotchas.

## Output Types

- **Standard**: Technical explanation of a module.
- **Onboarding**: "How to start working on this module".
- **API**: Endpoints, Contracts, Error Codes.
- **Architectural**: High-level design principles.

## Success Criteria

- [ ] Documentation covers "Why" and "How".
- [ ] Business logic extracted and explained.
- [ ] Diagrams included for complex flows.
- [ ] Code examples provided.
