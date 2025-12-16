# Pattern Analysis

## Description

A methodology for extracting structural, stylistic, and logical patterns from existing code to ensure consistency when implementing new features. This is the core skill for "Mimicry" development.

## When to Use

- Implementing a new feature that is "similar to X"
- Refactoring code to match a specific design pattern
- Onboarding new developers to project standards
- Ensuring UI/UX consistency across similar pages

## The Process

### Phase 1: Pattern Recognition

**Goal**: Identify the "DNA" of the reference implementation.

**Key Questions**:
1.  **Architecture**: How are files organized? (Folder structure, naming conventions)
2.  **Data Flow**: How is state managed? How is data fetched?
3.  **UI/UX**: What components are used? (Specific libraries, styling patterns)
4.  **Logic**: specific algorithms or validation rules reused?

### Phase 2: Template Extraction

**Goal**: Create a mental (or actual) template where variable parts are identified.

**Strategy**:
- Identify **Constant** parts: Boilerplate, imports, layout structure.
- Identify **Variable** parts: Entity names, specific fields, API endpoints.

**Example**:
```typescript
// Pattern:
export const [Entity]List = () => {
    const { data } = use[Entity]Query(); // Variable hook
    return <Table data={data} columns={...} /> // Constant structure
}
```

### Phase 3: Adaptation

**Goal**: Apply the pattern to the new context.

**Rules**:
- **Strictly Adhere** to structural patterns (don't invent new folder structures).
- **Strictly Adhere** to naming conventions.
- **Adapt** logic only where the business requirements differ.

## Output Format (for Analyzer Subagent)

```markdown
# Pattern Analysis: [Reference Feature]

## 1. File Structure
- `page.tsx`: Route entry
- `components/`: Local components
- `hooks/`: Custom logic

## 2. Key Patterns
- **State**: Uses generic `useQuery` wrapper.
- **Form**: Uses `react-hook-form` with Zod schema.
- **Styling**: Tailwind utility classes, specific color tokens.

## 3. Adaptation Strategy for [Target Feature]
- **Keep**: Folder structure, Form library.
- **Change**: API endpoint (`/api/users` -> `/api/products`), Validation schema.
```
