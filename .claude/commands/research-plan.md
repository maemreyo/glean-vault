# /research-plan - Research-Driven Planning for New Features

**Required Skill**: `deep-research`
**Reference**: `.claude/skills/methodology/deep-research/SKILL.md`

## Purpose

Dành cho **feature mới** cần research từ đầu (không có old code):
- Research best practices từ web
- Đọc documentation
- Tìm hiểu APIs, libraries
- Design architecture
- Generate implementation plan

**Use cases**:
- Implement OAuth 2.0 authentication
- Add payment gateway integration
- Build real-time notifications
- Integrate third-party APIs
- Implement new design patterns

---

## Core Flow

```
User: /research-plan "OAuth 2.0 with PKCE"
  ↓
┌─────────────────────────────────────┐
│ Phase 1: RESEARCH (Subagent 1)     │
│ - Search web for best practices    │
│ - Read official docs                │
│ - Find examples & tutorials         │
│ - Understand security concerns      │
│ Returns: Research Report            │
└────────────┬────────────────────────┘
             │
    ┌────────▼────────┐
    │ Review Gate     │
    │ Enough info? Y/N│
    └────────┬────────┘
             │ YES
             ▼
┌─────────────────────────────────────┐
│ Phase 2: DESIGN (Subagent 2)       │
│ - Architecture design               │
│ - Choose libraries/tools            │
│ - Security considerations           │
│ - Data flow design                  │
│ Returns: Design Document            │
└────────────┬────────────────────────┘
             │
    ┌────────▼────────┐
    │ Review Gate     │
    │ Design OK? Y/N  │
    └────────┬────────┘
             │ YES
             ▼
┌─────────────────────────────────────┐
│ Phase 3: PLAN (Subagent 3)         │
│ - Generate task breakdown          │
│ - Add implementation details        │
│ - Include code examples             │
│ - Add testing strategy              │
│ Returns: Executable Plan            │
└────────────┬────────────────────────┘
             │
             ▼
             │
             ▼
    ┌─────────────────────────┐
    │ Save Artifacts          │
    │ - Write Research Report │
    │ - Write Design Doc      │
    │ - Write Executable Plan │
    │ to `docs/` folders      │
    └─────────────────────────┘
```

---

## Subagent 1: Research

**Task**: Gather information from web, docs, examples

```markdown
Research Goals:
1. **Internal Context Audit (MUST DO FIRST)**:
   - **Dependencies**: Read `package.json`. What relevant libraries are already installed? (e.g., don't research state libs if `Zustand` is present).
   - **Patterns**: Search `src/` for similar features. How is it done currently?
   - **Config**: Check `.env` for available constraints/secrets.
   - **Goal**: consistent implementation, reuse existing tools.

2. **Official Documentation**:
   - Search: "OAuth 2.0 PKCE official RFC"
   - Read: OAuth 2.0 specification
   - Key sections: PKCE flow, security

2. **Best Practices**:
   - Search: "OAuth PKCE implementation guide"
   - Find: Security recommendations
   - Common pitfalls to avoid

3. **Code Examples**:
   - Search: "OAuth PKCE React example"
   - Find: Working implementations
   - Library recommendations

4. **Integration Guides**:
   - Provider-specific guides (Google, Auth0, etc.)
   - Token storage best practices
   - Refresh token handling

Execute for: **$ARGUMENTS**

**Auto-Generated Paths** (if not specified):
- Folder: `docs/[feature-slug]/`
- Plan: `docs/[feature-slug]/plan.md`
- Research: `docs/[feature-slug]/research.md`
- Design: `docs/[feature-slug]/design.md`

**Action**: Verify `docs/[feature-slug]/` folder exists. If not, create it.

{{ if --output provided }}
**Override Plan Path**: `$OUTPUT_PATH`
{{ endif }}

Output:
- Research summary
- Key findings
- Recommended libraries
- Security checklist
- Reference links
```

**Example Output**:
```markdown
Research Report: OAuth 2.0 with PKCE

Internal Context:
- ✅ Project uses `axios` (v1.6) -> Will use for HTTP requests.
- ✅ Existing `AuthContext` found in `src/contexts` -> Will extend this.
- ⚠️ `NextAuth` is NOT installed -> Will verify if we should add it or build custom.

Key Findings:
✅ PKCE: Proof Key for Code Exchange (RFC 7636)
✅ Security: Prevents authorization code interception
✅ Flow: code_verifier → code_challenge → token exchange

Recommended Libraries:
1. @auth/core - Universal auth library
2. NextAuth.js - For Next.js apps
3. react-oauth2-code-pkce - Lightweight React solution

Security Requirements:
⚠️  Store tokens in httpOnly cookies (NOT localStorage)
⚠️  Use 43-128 char random code_verifier
⚠️  Validate state parameter
⚠️  Implement token refresh logic

Best Practices:
- Use authorization code flow (not implicit)
- Implement CSRF protection
- Handle token expiration
- Secure redirect URIs

Code Examples Found:
- Auth0 PKCE guide: [link]
- Google OAuth setup: [link]
- React implementation: [link]

Reference Documentation:
- RFC 7636: https://...
- OAuth 2.0 Security: https://...
```

---

## Subagent 2: Design

**Task**: Design architecture based on research

```markdown
Design Goals:
1. **Architecture**:
   - Component structure
   - State management approach
   - API integration design

2. **Technology Choices**:
   - Library selection (from research)
   - Framework integration
   - Storage strategy

3. **Security Design**:
   - Token storage approach
   - CSRF protection
   - Secure communication

4. **Error Handling**:
   - Network failures
   - Token expiration
   - Invalid states

Output:
- Architecture diagram
- Component breakdown
- Data flow
- Security measures
- Technology stack
```

**Example Output**:
```markdown
Design Document: OAuth PKCE Implementation

Architecture:
```
┌─────────────────────────────────┐
│ React Components                │
├─────────────────────────────────┤
│ - LoginButton                   │
│ - AuthCallback                  │
│ - ProtectedRoute                │
└──────────┬──────────────────────┘
           │
┌──────────▼──────────────────────┐
│ Auth Context (React Context)    │
├─────────────────────────────────┤
│ - user state                    │
│ - login()                       │
│ - logout()                      │
│ - refreshToken()                │
└──────────┬──────────────────────┘
           │
┌──────────▼──────────────────────┐
│ Auth Service                    │
├─────────────────────────────────┤
│ - generatePKCE()                │
│ - exchangeCodeForToken()        │
│ - refreshAccessToken()          │
└──────────┬──────────────────────┘
           │
┌──────────▼──────────────────────┐
│ Secure Storage                  │
├─────────────────────────────────┤
│ - httpOnly cookies              │
│ - encrypted localStorage (state)│
└─────────────────────────────────┘
```

Technology Stack:
- Auth Library: @auth/core v5
- HTTP Client: axios with interceptors
- Storage: js-cookie + crypto-js
- Router: Next.js App Router

Security Measures:
1. Token Storage:
   - Access token: httpOnly cookie
   - Refresh token: httpOnly cookie
   - State/verifier: sessionStorage (temporary)

2. CSRF Protection:
   - Random state parameter
   - Validate on callback

3. Token Refresh:
   - Auto-refresh 5min before expiry
   - Retry logic with exponential backoff

Data Flow:
1. User clicks login
2. Generate code_verifier + code_challenge
3. Redirect to OAuth provider
4. Provider redirects back with code
5. Exchange code + verifier for tokens
6. Store tokens securely
7. Set up auto-refresh
```

---

## Subagent 3: Planner

**Task**: Generate executable implementation plan

```markdown
Planning Goals:
1. **Task Breakdown**:
   - Micro-tasks (2-5 min each)
   - Clear dependencies
   - File paths specified

2. **Implementation Details**:
   - Reference research findings
   - Include code examples
   - Add security notes

3. **Testing Strategy**:
   - Unit tests
   - Integration tests
   - Security tests

4. **Acceptance Criteria**:
   - Functional requirements
   - Security requirements
   - Performance benchmarks

Output:
- Complete execution plan
- Ready for /execute-plan
```

**Example Output** (excerpt):
```markdown
# Implementation Plan: OAuth 2.0 PKCE Authentication

## Metadata
- Phases: 6
- Tasks: 38 micro-tasks
- Estimate: 8-10 hours
- Risk: Medium-High (security-critical)

---

## Phase 1: Setup & Dependencies

### Task 1.1: Install Dependencies (5m)

**File**: `package.json`

**Dependencies**:
```json
{
  "@auth/core": "^0.18.0",
  "axios": "^1.6.0",
  "js-cookie": "^3.0.5"
}
```

**Acceptance**: ✅ Packages installed, no conflicts

---

### Task 1.2: Environment Configuration (5m)

**File**: `.env.local`

**Variables**:
```env
NEXT_PUBLIC_OAUTH_CLIENT_ID=your_client_id
NEXT_PUBLIC_OAUTH_REDIRECT_URI=http://localhost:3000/auth/callback
OAUTH_TOKEN_URL=https://oauth.provider.com/token
```

**Security Note**: Never commit real credentials!

---

## Phase 2: Auth Service

### Task 2.1: PKCE Generator (15m)

**File**: `src/lib/auth/pkce.ts`

**Context**: From research - RFC 7636 spec

**Implementation Strategy**:
1. Generate random code_verifier (43-128 chars)
2. Hash with SHA-256
3. Base64 URL encode → code_challenge

**Code Example** (from research):
```typescript
// Generate cryptographically secure random string
const generateCodeVerifier = (): string => {
  const array = new Uint8Array(32);
  crypto.getRandomValues(array);
  return base64UrlEncode(array);
};

// Generate code challenge
const generateCodeChallenge = async (
  verifier: string
): Promise<string> => {
  const encoder = new TextEncoder();
  const data = encoder.encode(verifier);
  const hash = await crypto.subtle.digest('SHA-256', data);
  return base64UrlEncode(new Uint8Array(hash));
};
```

**Testing**:
- [ ] Verifier length 43-128 chars
- [ ] Challenge is valid SHA-256 hash
- [ ] URL-safe base64 encoding

**Acceptance**: ✅ Generates valid PKCE pair

---

### Task 2.2: OAuth Client Service (30m)

**File**: `src/lib/auth/oauth-client.ts`

**Context**: 
- Design: Token exchange flow
- Security: Store in httpOnly cookies

**Key Methods**:
```typescript
class OAuthClient {
  // Initiate OAuth flow
  async login(): Promise<void>
  
  // Handle callback
  async handleCallback(code: string): Promise<User>
  
  // Exchange code for tokens
  private async exchangeCode(code: string): Promise<Tokens>
  
  // Refresh access token
  async refreshToken(): Promise<void>
}
```

**Security Requirements**:
⚠️  MUST validate state parameter
⚠️  MUST use code_verifier in token exchange
⚠️  MUST store tokens in httpOnly cookies

**Testing**:
- [ ] Login redirects to OAuth provider
- [ ] Callback handles valid code
- [ ] Token exchange works
- [ ] Refresh token flow works

---

## Phase 3: React Components

### Task 3.1: Auth Context Provider (20m)

**File**: `src/contexts/AuthContext.tsx`

**Context**: 
- Design: Global auth state
- Pattern: React Context + Custom Hook

**State Management**:
```typescript
interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: Error | null;
}

interface AuthContextValue extends AuthState {
  login: () => Promise<void>;
  logout: () => Promise<void>;
  refreshToken: () => Promise<void>;
}
```

**Implementation Notes**:
- Use useReducer for state
- Implement auto-refresh on mount
- Handle token expiration

---

[... 35 more tasks ...]

---

## Phase 6: Testing & Security Audit

### Task 6.1: Security Tests (45m)

**Files**: `src/__tests__/auth-security.test.ts`

**Test Cases**:
1. PKCE Flow:
   - [ ] Verifier stored securely (not in URL)
   - [ ] Challenge matches verifier
   - [ ] Tokens not exposed in URLs

2. CSRF Protection:
   - [ ] State parameter validated
   - [ ] Invalid state rejected

3. Token Storage:
   - [ ] Access token in httpOnly cookie
   - [ ] Refresh token in httpOnly cookie
   - [ ] No tokens in localStorage

4. Token Refresh:
   - [ ] Auto-refresh before expiry
   - [ ] Handles network failures
   - [ ] Logout on refresh failure

**Security Checklist** (from research):
- [ ] No tokens in localStorage
- [ ] HTTPS enforced in production
- [ ] CSRF tokens validated
- [ ] Code verifier never sent to server
- [ ] Secure redirect URIs configured

---

## References

Research Sources:
- RFC 7636: https://...
- OAuth 2.0 Security Best Practices: https://...
- @auth/core docs: https://...
- Example implementation: https://...

Design Documents:
- Architecture diagram: see Phase 2 output
- Security design: see Phase 2 output

---

## Execution

Ready for: `/execute-plan plans/oauth-pkce.md`
```

---

## Usage Examples

### Example 1: New Feature Research

```bash
/research-plan "implement Stripe payment integration"

# Flow:
# 1. Research: Stripe API, webhooks, best practices
# 2. Design: Payment flow, error handling, security
# 3. Plan: Step-by-step implementation
```

### Example 2: API Integration

```bash
/research-plan "integrate Twilio SMS API" \
  --output=plans/twilio-integration.md \
  --research=docs/twilio-research.md
```

### Example 3: Complex Feature

```bash
/research-plan "real-time chat with Socket.io and Redis" \
  --type=fullstack \
  --output=plans/chat-feature.md
```

---

## Flags

| Flag | Description | Example |
|------|-------------|---------|
| `--output=path` | Save plan to file | `--output=plans/feature.md` |
| `--research=path` | Save research to file | `--research=docs/research.md` |
| `--design=path` | Save design doc to file | `--design=docs/design.md` |
| `--type=TYPE` | Hint: api/fullstack/frontend | `--type=api` |
| `--focus=AREA` | Focus research area | `--focus=security` |

---

## Key Differences

| Feature | /auto-plan | /research-plan |
|---------|------------|----------------|
| **Input** | Old codebase | Feature description |
| **Phase 1** | Explore old code | Research from web/docs |
| **Phase 2** | Analyze patterns | Design architecture |
| **Phase 3** | Plan migration | Plan implementation |
| **Use Case** | Migration/reimplementation | New features from scratch |
| **References** | Old code | Documentation, examples |

---

## When to Use

**Use `/auto-plan`** when:
- ✅ You have old code to migrate
- ✅ Need to preserve business logic
- ✅ Reimplementing existing features

**Use `/research-plan`** when:
- ✅ Building new features
- ✅ Need to research best practices
- ✅ Integrating third-party services
- ✅ No existing implementation

---

## Success Criteria

- [ ] Command created: `/research-plan.md`
- [ ] Always runs research → design → plan
- [ ] Uses 3 fresh subagents
- [ ] Review gates between phases
- [ ] Web search integration
- [ ] Documentation reading
- [ ] Security considerations included
- [ ] Ready for `/execute-plan`