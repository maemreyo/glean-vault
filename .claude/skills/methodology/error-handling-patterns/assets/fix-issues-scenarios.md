# Fix Issues - Complete Error Scenarios Catalog

This document catalogs every possible error scenario in the `/fix-issues` command workflow, with recovery strategies and example code.

## Quick Reference

| Scenario | Phase | Severity | Recovery | Auto/Manual |
|----------|-------|----------|----------|-------------|
| Git not found | Discovery | Critical | None | Fail |
| Analysis missing | Discovery | High | Fallback to latest | Auto |
| Dirty working dir | Discovery | Medium | Stash or abort | Manual |
| Circular dependency | Planning | Medium | Remove from batch | Auto |
| Timeout exceeded | Execution | Medium | Save & resume | Auto |
| Tests fail after fix | Execution | High | Rollback | Auto |
| Network failure | Execution | Medium | Retry with backoff | Auto |
| Commit failed | Reporting | Low | Save patch | Auto |
| Out of memory | Any | Critical | Abort | Fail |

---

## Phase 0: Discovery & Triage

### Scenario 1: Not in Git Repository

**Error Type**: `ValidationError`  
**Severity**: Critical  
**Recovery**: None - hard requirement

```python
# Detection
def check_git_repository():
    if not Path('.git').exists():
        raise ValidationError(
            "Not a git repository",
            code="GIT_NOT_FOUND",
            details={
                "cwd": os.getcwd(),
                "suggestion": "Run 'git init' or navigate to a git repository"
            }
        )

# Error Message
"""
❌ Error: Not a git repository

Current directory: /home/user/project
Suggestion: Run 'git init' or cd to a git repository

The /fix-issues command requires a git repository to:
- Create checkpoints before fixes
- Commit changes after successful fixes
- Rollback on failures
"""

# User Action Required
cd /path/to/git/repo  # or  git init
```

---

### Scenario 2: Analysis File Not Found

**Error Type**: `FileNotFoundError`  
**Severity**: High  
**Recovery**: Auto-fallback to latest artifact

```python
# Detection & Recovery
def load_analysis(from_path: Optional[str] = None):
    if from_path:
        # User specified file
        if not Path(from_path).exists():
            raise FileNotFoundError(f"Analysis file not found: {from_path}")
        return parse_file(from_path)
    else:
        # Try to find latest artifact
        artifacts = sorted(
            Path('.claude/artifacts').glob('recent-changes-*.md'),
            key=lambda p: p.stat().st_mtime,
            reverse=True
        )
        
        if not artifacts:
            raise FileNotFoundError(
                "No recent changes analysis found. Run /how-recent-changes first."
            )
        
        latest = artifacts[0]
        logger.info(f"Using latest analysis: {latest.name}")
        return parse_file(latest)

# Error Message (no recovery)
"""
❌ Error: No analysis found

No recent changes analysis found in .claude/artifacts/

Next steps:
1. Run /how-recent-changes to analyze your code
2. Then run /fix-issues to address the issues

Example:
  > /how-recent-changes --deep
  > /fix-issues
"""

# Success Message (with recovery)
"""
ℹ️  No --from specified, using latest analysis
   File: .claude/artifacts/recent-changes-2024-01-15-1430.md
   Age: 15 minutes ago
   
Proceeding with 12 issues found...
"""
```

---

### Scenario 3: Required Tool Missing

**Error Type**: `ToolNotFoundError`  
**Severity**: Critical (for required), High (for optional)  
**Recovery**: None - user must install

```python
# Detection
def validate_tools():
    required_tools = {
        'git': 'https://git-scm.com',
        'npm': 'https://nodejs.org'  # if JS project
    }
    
    optional_tools = {
        'eslint': 'npm install -g eslint',
        'prettier': 'npm install -g prettier'
    }
    
    missing_required = []
    missing_optional = []
    
    for tool, hint in required_tools.items():
        if not shutil.which(tool):
            missing_required.append((tool, hint))
    
    for tool, hint in optional_tools.items():
        if not shutil.which(tool):
            missing_optional.append((tool, hint))
    
    if missing_required:
        raise ToolNotFoundError(
            "Required tools missing",
            tools=missing_required
        )
    
    if missing_optional:
        logger.warning(f"Optional tools missing: {[t for t, _ in missing_optional]}")

# Error Message
"""
❌ Error: Required tools not found

Missing tools:
  • npm - Install from https://nodejs.org
  • eslint - Run: npm install -g eslint

These tools are required for:
  • npm: Running tests, installing dependencies
  • eslint: Code quality fixes

⚠️  Optional tools missing (can continue):
  • prettier - Run: npm install -g prettier
"""
```

---

### Scenario 4: Dirty Working Directory

**Error Type**: `DirtyWorkingDirectoryError`  
**Severity**: Medium  
**Recovery**: Interactive - stash, abort, or continue

```python
# Detection
def check_working_directory():
    result = subprocess.run(
        ['git', 'status', '--porcelain'],
        capture_output=True,
        text=True
    )
    
    if result.stdout.strip():
        uncommitted = parse_git_status(result.stdout)
        
        if is_interactive_mode():
            return handle_dirty_directory_interactive(uncommitted)
        else:
            raise DirtyWorkingDirectoryError(
                "Working directory has uncommitted changes",
                files=uncommitted
            )

def handle_dirty_directory_interactive(files: list[str]):
    print(f"""
⚠️  Working directory has uncommitted changes:
{chr(10).join(f"  • {f}" for f in files[:5])}
{f"  ... and {len(files) - 5} more" if len(files) > 5 else ""}

The /fix-issues command will make changes to your code.
Having uncommitted changes can make rollback difficult.

What would you like to do?
  1. Stash changes and continue (recommended)
  2. Abort - let me commit first
  3. Continue anyway (risky - no rollback possible)
    """)
    
    choice = input("Enter choice (1-3): ").strip()
    
    if choice == '1':
        subprocess.run(['git', 'stash', 'push', '-u', '-m', 'Auto-stash by /fix-issues'])
        print("✅ Changes stashed. You can restore them later with: git stash pop")
        return True
    elif choice == '2':
        raise UserAbortError("Aborted by user")
    else:  # choice == '3'
        print("⚠️  Continuing with uncommitted changes (rollback disabled)")
        return False  # Disable rollback feature

# Error Message (non-interactive)
"""
❌ Error: Working directory has uncommitted changes

Modified files:
  • src/auth/login.js
  • src/api/users.js
  • tests/auth.test.js

The /fix-issues command will modify code and needs a clean state for:
  • Creating checkpoints before fixes
  • Rolling back on failures
  • Committing fixes after success

Please commit or stash your changes first:
  git commit -am "WIP: current changes"
  # or
  git stash push -m "WIP"
  
Then run /fix-issues again.
"""
```

---

### Scenario 5: No Issues Found in Analysis

**Error Type**: `NoIssuesFoundError`  
**Severity**: Low (informational)  
**Recovery**: Exit gracefully

```python
def extract_issues(analysis: AnalysisData) -> list[Issue]:
    issues = parse_issues_from_analysis(analysis)
    
    if not issues:
        print("""
✅ No issues found!

Your recent changes look good:
  • No bugs detected
  • No missing tests
  • No security vulnerabilities
  • No code quality issues

Keep up the great work! 🎉
        """)
        sys.exit(0)
    
    return issues
```

---

## Phase 1: Planning & Strategy

### Scenario 6: Circular Dependency Detected

**Error Type**: `CircularDependencyError`  
**Severity**: Medium  
**Recovery**: Auto - remove circular issues from batch

```python
# Detection
def resolve_dependencies(issues: list[Issue]) -> list[Issue]:
    graph = build_dependency_graph(issues)
    
    try:
        return topological_sort(issues, graph)
    except CycleDetected as e:
        return handle_circular_dependencies(issues, e.cycle)

def handle_circular_dependencies(
    issues: list[Issue],
    cycle: list[str]
) -> list[Issue]:
    """Remove circular dependencies and continue with rest."""
    
    logger.warning(f"Circular dependency detected: {' -> '.join(cycle)}")
    
    # Issues in cycle
    circular = [i for i in issues if i.id in cycle]
    safe = [i for i in issues if i.id not in cycle]
    
    # Save circular issues for manual review
    save_for_manual_review(circular, reason="circular_dependency")
    
    # Display warning
    print(f"""
⚠️  Circular dependency detected

Issues forming a cycle:
{chr(10).join(f"  • {i.id}: {i.title}" for i in circular)}

These issues depend on each other and cannot be automatically ordered.

Action taken:
  ✅ Saved to .claude/manual-review/circular-deps.json
  ✅ Continuing with {len(safe)} other issues
  
You'll need to manually resolve these issues after the batch completes.
    """)
    
    return safe

# Manual Review File
"""
{
  "reason": "circular_dependency",
  "cycle": ["ISS-003", "ISS-007", "ISS-012"],
  "issues": [
    {
      "id": "ISS-003",
      "title": "Refactor auth module",
      "depends_on": ["ISS-007"],
      "description": "..."
    },
    {
      "id": "ISS-007",
      "title": "Update user model",
      "depends_on": ["ISS-012"],
      "description": "..."
    },
    {
      "id": "ISS-012",
      "title": "Fix session handling",
      "depends_on": ["ISS-003"],
      "description": "..."
    }
  ],
  "recommendation": "Break the cycle by implementing ISS-007 first without depending on ISS-012"
}
"""
```

---

### Scenario 7: Strategy Generation Failed

**Error Type**: `StrategyGenerationError`  
**Severity**: Medium  
**Recovery**: Auto - fallback to templates or manual

```python
# Multi-level fallback
def generate_fix_strategy(issue: Issue) -> FixStrategy:
    # Level 1: AI-powered strategy
    try:
        return generate_ai_strategy(issue)
    except (NetworkError, APIError) as e:
        logger.warning(f"AI strategy failed: {e}")
    
    # Level 2: Template-based strategy
    try:
        return get_template_strategy(issue.type, issue.severity)
    except TemplateNotFoundError:
        logger.warning(f"No template for {issue.type}")
    
    # Level 3: Mark for manual review
    return FixStrategy(
        type="manual",
        can_auto_execute=False,
        description="Requires manual review - no automated strategy available"
    )

@retry(max_attempts=3, backoff_factor=2.0)
def generate_ai_strategy(issue: Issue) -> FixStrategy:
    """Generate strategy with retry logic."""
    response = ai_service.generate_strategy(
        issue_type=issue.type,
        context=issue.context,
        files=issue.files,
        timeout=30
    )
    return parse_strategy(response)

# Status Message
"""
⚠️  Strategy generation warnings:

  • ISS-003: AI service timeout - using template strategy
  • ISS-009: No template available - marked for manual review
  • ISS-014: AI service error - using template strategy

Proceeding with:
  ✅ 9 issues with AI strategies
  ✅ 3 issues with template strategies
  ⏭️  1 issue marked for manual review
"""
```

---

## Phase 2: Execution

### Scenario 8: Tests Fail After Fix

**Error Type**: `TestFailureError`  
**Severity**: High  
**Recovery**: Auto - rollback fix

```python
def execute_fix_with_validation(issue: Issue) -> FixResult:
    # Create checkpoint
    checkpoint = create_checkpoint(f"before-{issue.id}")
    
    try:
        # Apply fix
        apply_fix(issue)
        
        # Run tests
        test_result = run_tests()
        
        if not test_result.success:
            # Rollback and analyze
            failed_tests = test_result.failed_tests
            
            # Check if failures are related to our fix
            is_related = analyze_test_failures(failed_tests, issue.files)
            
            if is_related:
                rollback(checkpoint)
                raise TestFailureError(
                    f"Fix for {issue.id} broke tests",
                    issue_id=issue.id,
                    failed_tests=failed_tests,
                    fix_rolled_back=True
                )
            else:
                # Tests were already broken
                logger.warning(f"Tests were already broken (unrelated to fix)")
                return FixResult(
                    status="success_with_warnings",
                    issue_id=issue.id,
                    warnings=[f"Pre-existing test failures: {failed_tests}"]
                )
        
        return FixResult(status="success", issue_id=issue.id)
        
    except Exception as e:
        rollback(checkpoint)
        raise

# Error Message
"""
❌ Fix rolled back: ISS-003 - Memory leak in WebSocket

Tests failed after applying fix:
  ✗ test_websocket_connection (expected 'connected', got 'closed')
  ✗ test_message_handling (WebSocket is not defined)
  ✗ test_cleanup (TypeError: Cannot read property 'close' of null)

Root cause analysis:
  The fix introduced a breaking change in the WebSocket API.
  The 'connect' method now returns a Promise instead of being synchronous.

Action taken:
  ✅ Fix has been rolled back
  ✅ Code restored to previous state
  ✅ Issue saved for manual review

Recommendation:
  Update tests to handle async connect() before reapplying fix.
"""
```

---

### Scenario 9: Fix Timeout

**Error Type**: `TimeoutError`  
**Severity**: Medium  
**Recovery**: Auto - save progress and continue

```python
async def execute_fix_with_timeout(issue: Issue) -> FixResult:
    try:
        result = await asyncio.wait_for(
            execute_fix(issue),
            timeout=1800  # 30 minutes
        )
        return result
        
    except asyncio.TimeoutError:
        # Save progress
        checkpoint = create_checkpoint(f"timeout-{issue.id}")
        
        save_resume_point({
            'issue_id': issue.id,
            'checkpoint': checkpoint,
            'partial_work': gather_partial_work(),
            'resume_hint': 'Run: /fix-issues --resume=ISS-003'
        })
        
        return FixResult(
            status="timeout",
            issue_id=issue.id,
            can_resume=True,
            resume_command=f"/fix-issues --resume={issue.id}"
        )

# Status Message
"""
⏱️  Timeout: ISS-003 exceeded 30-minute limit

Issue: Memory leak in WebSocket
Progress: 
  ✅ Identified leak source
  ✅ Implemented cleanup logic
  ⏳ Writing tests (interrupted)

Action taken:
  ✅ Progress saved to .claude/checkpoints/ISS-003.json
  ✅ Can resume with: /fix-issues --resume=ISS-003
  ✅ Continuing with next issue...

Recommendation:
  This fix may need to be broken into smaller issues:
  1. Fix memory leak (done)
  2. Add tests (remaining)
"""
```

---

### Scenario 10: Network Failure During External Call

**Error Type**: `NetworkError`  
**Severity**: Medium  
**Recovery**: Auto - retry with exponential backoff

```python
@retry(
    max_attempts=3,
    backoff_factor=2.0,
    exceptions=(NetworkError, ConnectionError, TimeoutError)
)
async def fetch_dependency_info(package: str) -> DependencyInfo:
    """Fetch with automatic retry."""
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"https://registry.npmjs.org/{package}",
            timeout=aiohttp.ClientTimeout(total=10)
        ) as response:
            if response.status == 429:  # Rate limited
                retry_after = int(response.headers.get('Retry-After', 60))
                raise RateLimitError(retry_after)
            
            response.raise_for_status()
            return await response.json()

# With circuit breaker for repeated failures
circuit_breaker = CircuitBreaker(failure_threshold=5)

def safe_fetch_dependency(package: str) -> Optional[DependencyInfo]:
    try:
        return circuit_breaker.call(
            lambda: fetch_dependency_info(package)
        )
    except CircuitBreakerOpen:
        logger.error("Circuit breaker open - npm registry unavailable")
        return None  # Continue without dependency info

# Status Message
"""
⚠️  Network issues detected

Attempt 1/3 failed: Connection timeout to registry.npmjs.org
  Retrying in 2 seconds...
  
Attempt 2/3 failed: Connection timeout to registry.npmjs.org
  Retrying in 4 seconds...
  
✅ Attempt 3/3 succeeded: Fetched dependency info

Continuing with fix...
"""
```

---

### Scenario 11: Out of Memory

**Error Type**: `MemoryError`  
**Severity**: Critical  
**Recovery**: None - abort gracefully

```python
def execute_batch_with_memory_monitoring(issues: list[Issue]):
    memory_threshold = 0.90  # 90% of available memory
    
    for i, issue in enumerate(issues):
        # Check memory before each fix
        memory_usage = psutil.virtual_memory().percent / 100
        
        if memory_usage > memory_threshold:
            logger.critical(f"Memory usage critical: {memory_usage:.1%}")
            
            # Save progress
            save_batch_progress(
                completed=i,
                remaining=len(issues) - i,
                checkpoint=create_checkpoint("memory-critical")
            )
            
            raise MemoryError(
                f"Out of memory: {memory_usage:.1%} used",
                completed_issues=i,
                total_issues=len(issues)
            )
        
        # Execute fix
        try:
            execute_fix(issue)
        except MemoryError as e:
            # Last resort - save and exit
            emergency_save()
            raise

# Error Message
"""
❌ Critical: Out of Memory

Memory usage: 95% (13.2 GB / 14 GB)

Progress saved:
  ✅ Completed: 7/12 issues
  ✅ Checkpoint: .claude/checkpoints/memory-critical.stash
  ✅ Remaining: 5 issues

The system is running out of memory and cannot continue safely.

Recommendations:
  1. Close other applications to free memory
  2. Increase system memory if possible
  3. Run fixes in smaller batches: /fix-issues --max-fixes=3
  
Resume with: /fix-issues --resume=memory-critical
"""
```

---

### Scenario 12: Permission Denied

**Error Type**: `PermissionError`  
**Severity**: High  
**Recovery**: Skip file, continue with others

```python
def apply_fix_to_file(filepath: str, changes: str):
    try:
        # Check write permission
        if not os.access(filepath, os.W_OK):
            raise PermissionError(f"No write permission for {filepath}")
        
        with open(filepath, 'w') as f:
            f.write(changes)
            
    except PermissionError as e:
        logger.error(f"Permission denied: {filepath}")
        
        # Try with sudo (interactive only)
        if is_interactive_mode():
            use_sudo = prompt_yes_no(
                f"File {filepath} requires elevated permissions. Use sudo?"
            )
            if use_sudo:
                subprocess.run(['sudo', 'tee', filepath], input=changes.encode())
                return
        
        # Save changes to patch file
        patch_file = f".claude/patches/{Path(filepath).name}.patch"
        save_patch(patch_file, filepath, changes)
        
        raise FixExecutionError(
            f"Cannot write to {filepath}",
            recovery_action=f"Apply manually: patch < {patch_file}"
        )

# Error Message
"""
⚠️  Permission denied: ISS-005

Cannot write to system files:
  • /etc/nginx/nginx.conf
  • /usr/local/bin/deploy.sh

Action taken:
  ✅ Changes saved to .claude/patches/
  ⏭️  Skipped 2 files, continued with others

To apply manually:
  sudo patch /etc/nginx/nginx.conf < .claude/patches/nginx.conf.patch
  sudo patch /usr/local/bin/deploy.sh < .claude/patches/deploy.sh.patch
"""
```

---

## Phase 3: Reporting & Commit

### Scenario 13: Git Commit Failed

**Error Type**: `CommitError`  
**Severity**: Low  
**Recovery**: Auto - save patch files

```python
def create_commit(fix_type: str, fixes: list[FixResult]):
    message = generate_commit_message(fix_type, fixes)
    
    # Stage files
    for fix in fixes:
        for file in fix.files_changed:
            subprocess.run(['git', 'add', file], check=True)
    
    # Try commit
    try:
        subprocess.run(
            ['git', 'commit', '-m', message],
            check=True,
            capture_output=True
        )
        return CommitResult(status="success")
        
    except subprocess.CalledProcessError as e:
        logger.error(f"Commit failed: {e.stderr.decode()}")
        
        # Fallback: Save as patch
        patch_content = subprocess.run(
            ['git', 'diff', '--cached'],
            capture_output=True,
            text=True
        ).stdout
        
        patch_file = f".claude/patches/fix-{fix_type}-{int(time.time())}.patch"
        Path(patch_file).write_text(patch_content)
        
        # Also save commit message
        message_file = f"{patch_file}.msg"
        Path(message_file).write_text(message)
        
        return CommitResult(
            status="patch_saved",
            patch_file=patch_file,
            message_file=message_file
        )

# Status Message
"""
⚠️  Commit failed - changes saved as patch

Git commit failed with error:
  "hooks/pre-commit: line 15: eslint: command not found"

Action taken:
  ✅ Changes saved to .claude/patches/fix-security-1705324800.patch
  ✅ Message saved to .claude/patches/fix-security-1705324800.patch.msg

To commit manually:
  1. Fix the pre-commit hook issue
  2. Apply patch: git apply .claude/patches/fix-security-1705324800.patch
  3. Commit with: git commit -F .claude/patches/fix-security-1705324800.patch.msg
"""
```

---

### Scenario 14: Report Generation Failed

**Error Type**: `ReportError`  
**Severity**: Low  
**Recovery**: Auto - progressively simpler formats

```python
def generate_report(results: BatchResult) -> Report:
    # Level 1: Rich markdown with charts
    try:
        return generate_rich_report(results)
    except Exception as e:
        logger.warning(f"Rich report failed: {e}")
    
    # Level 2: Simple markdown
    try:
        return generate_simple_report(results)
    except Exception as e:
        logger.warning(f"Simple report failed: {e}")
    
    # Level 3: Plain text
    try:
        return generate_text_report(results)
    except Exception as e:
        logger.error(f"Text report failed: {e}")
    
    # Level 4: JSON dump
    return Report(
        format="json",
        content=json.dumps(results.to_dict(), indent=2)
    )

# Status Message
"""
⚠️  Report generation warning

Rich markdown report failed: UnicodeEncodeError
  Falling back to simple markdown...
  
✅ Report generated successfully (simple format)
   Saved to: .claude/artifacts/fix-issues-report-2024-01-15.md
"""
```

---

## Error Recovery Decision Tree

```
Error Occurred
│
├─ Is it a validation error? (git missing, file not found)
│  ├─ Yes → Fail fast with clear message
│  └─ No → Continue
│
├─ Can we recover automatically?
│  ├─ Yes → Apply recovery strategy
│  │  ├─ Retry (network issues)
│  │  ├─ Fallback (AI → template → manual)
│  │  ├─ Rollback (test failures)
│  │  ├─ Skip (permission denied)
│  │  └─ Degrade (report format)
│  └─ No → Request user input (if interactive)
│
├─ Is it safe to continue?
│  ├─ Yes (medium/low severity) → Log, continue with next
│  └─ No (critical) → Abort, save progress
│
└─ Should we aggregate or fail?
   ├─ Multiple operations → Aggregate errors
   └─ Single critical operation → Fail immediately
```

---

## Summary Statistics

### By Phase
- **Discovery**: 5 scenarios (3 critical, 2 high)
- **Planning**: 2 scenarios (both medium)
- **Execution**: 5 scenarios (2 high, 3 medium)
- **Reporting**: 2 scenarios (both low)

### By Recovery Type
- **No Recovery** (fail): 3 scenarios
- **Automatic**: 9 scenarios
- **Interactive**: 2 scenarios
- **Degraded**: 2 scenarios

### By Severity
- **Critical**: 3 scenarios (git missing, tool missing, out of memory)
- **High**: 3 scenarios (analysis missing, tests fail, permission denied)
- **Medium**: 6 scenarios (dirty dir, circular deps, timeout, network)
- **Low**: 2 scenarios (commit failed, report failed)