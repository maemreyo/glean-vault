# Error Handling for `/fix-issues` Command

This reference applies the patterns from [SKILL.md](../SKILL.md) specifically to the `/fix-issues` command workflow. Read SKILL.md first for foundational patterns.

## Overview

The `/fix-issues` command executes in 4 phases, each with distinct error handling requirements:

```
Phase 0: Discovery    → Validation errors, data loading errors
Phase 1: Planning     → Dependency resolution errors, strategy errors
Phase 2: Execution    → Fix failures, test failures, timeout errors
Phase 3: Reporting    → Commit errors, file I/O errors
```

---

## Phase 0: Discovery & Triage - Validation Errors

### Pattern: **Fail Fast** (SKILL.md)

Validate all preconditions before starting execution.

### Error Scenarios

#### 1. Git Repository Not Found

```python
class GitNotFoundError(ApplicationError):
    """Raised when not in a git repository."""
    def __init__(self, cwd: str):
        super().__init__(
            "Not a git repository",
            code="GIT_NOT_FOUND",
            details={"cwd": cwd, "suggestion": "Run 'git init' or cd to a git repo"}
        )

def validate_git_repository() -> None:
    """Fail fast if not in git repo."""
    if not Path('.git').exists():
        raise GitNotFoundError(os.getcwd())
    
    # Also check if git is functional
    result = subprocess.run(['git', 'status'], capture_output=True)
    if result.returncode != 0:
        raise GitNotFoundError(os.getcwd())
```

**Recovery**: None - this is a hard requirement. User must be in a git repo.

---

#### 2. Analysis File Not Found

```python
def load_analysis_file(from_path: Optional[str] = None) -> AnalysisData:
    """Load analysis with fallback to latest artifact."""
    
    # Pattern: Graceful Degradation (SKILL.md)
    def load_from_flag() -> AnalysisData:
        if not from_path:
            raise FileNotFoundError("No --from path specified")
        if not Path(from_path).exists():
            raise FileNotFoundError(f"Analysis file not found: {from_path}")
        return parse_analysis_file(from_path)
    
    def load_latest_artifact() -> AnalysisData:
        artifacts = sorted(
            Path('.claude/artifacts').glob('recent-changes-*.md'),
            key=lambda p: p.stat().st_mtime,
            reverse=True
        )
        if not artifacts:
            raise FileNotFoundError(
                "No analysis artifacts found. Run /how-recent-changes first."
            )
        return parse_analysis_file(artifacts[0])
    
    # Try primary, fallback to secondary
    return with_fallback(
        primary=load_from_flag,
        fallback=load_latest_artifact,
        log_error=True
    )
```

**Recovery**: Automatic fallback to latest artifact.

---

#### 3. Required Tools Missing

```python
class ToolNotFoundError(ApplicationError):
    """Raised when required CLI tool is not available."""
    def __init__(self, tool: str, install_hint: str):
        super().__init__(
            f"Required tool '{tool}' not found",
            code="TOOL_NOT_FOUND",
            details={"tool": tool, "install_hint": install_hint}
        )

def validate_required_tools() -> None:
    """Check all required tools are available."""
    errors = ErrorCollector()
    
    tools = {
        'git': 'Install from https://git-scm.com',
        'npm': 'Install Node.js from https://nodejs.org',
        'python': 'Install from https://python.org'
    }
    
    for tool, hint in tools.items():
        if not shutil.which(tool):
            errors.add(ToolNotFoundError(tool, hint))
    
    if errors.hasErrors():
        errors.throw()  # Fail fast with all missing tools
```

**Recovery**: None - user must install tools.

---

#### 4. Dirty Working Directory

```python
class DirtyWorkingDirectoryError(ApplicationError):
    """Raised when working directory has uncommitted changes."""
    def __init__(self, uncommitted_files: list[str]):
        super().__init__(
            "Working directory has uncommitted changes",
            code="DIRTY_WORKING_DIR",
            details={
                "files": uncommitted_files,
                "suggestion": "Commit or stash changes first"
            }
        )

def check_working_directory() -> None:
    """Check if working directory is clean."""
    result = subprocess.run(
        ['git', 'status', '--porcelain'],
        capture_output=True,
        text=True
    )
    
    if result.stdout.strip():
        uncommitted = [
            line.split()[-1] 
            for line in result.stdout.strip().split('\n')
        ]
        
        # Pattern: Interactive Recovery
        if is_interactive_mode():
            choice = prompt_user(
                "Working directory is dirty. What would you like to do?",
                options=[
                    "1. Stash changes and continue",
                    "2. Abort",
                    "3. Continue anyway (risky)"
                ]
            )
            
            if choice == 1:
                subprocess.run(['git', 'stash', 'push', '-m', 'Auto-stash by /fix-issues'])
                return
            elif choice == 2:
                raise DirtyWorkingDirectoryError(uncommitted)
            # choice == 3: continue
        else:
            raise DirtyWorkingDirectoryError(uncommitted)
```

**Recovery**: Interactive - offer to stash or abort.

---

## Phase 1: Planning - Strategy Errors

### Pattern: **Error Aggregation** (SKILL.md)

Collect all planning errors before failing.

### Error Scenarios

#### 1. Circular Dependency Detected

```python
class CircularDependencyError(ApplicationError):
    """Raised when issues have circular dependencies."""
    def __init__(self, cycle: list[str]):
        super().__init__(
            "Circular dependency detected in issues",
            code="CIRCULAR_DEPENDENCY",
            details={
                "cycle": cycle,
                "suggestion": "These issues require manual resolution"
            }
        )

def resolve_dependencies(issues: list[Issue]) -> list[Issue]:
    """Topologically sort issues by dependencies."""
    graph = {issue.id: issue.dependencies for issue in issues}
    
    try:
        sorted_ids = topological_sort(graph)
        return [next(i for i in issues if i.id == id) for id in sorted_ids]
    except CycleDetectedError as e:
        # Pattern: Graceful Degradation
        # Remove problematic issues from execution
        logger.warning(f"Circular dependency: {e.cycle}")
        
        safe_issues = [i for i in issues if i.id not in e.cycle]
        problematic = [i for i in issues if i.id in e.cycle]
        
        # Log for manual review
        with open('.claude/logs/circular-deps.json', 'w') as f:
            json.dump({
                'cycle': e.cycle,
                'issues': [i.to_dict() for i in problematic]
            }, f, indent=2)
        
        return safe_issues
```

**Recovery**: Remove circular issues, continue with safe ones.

---

#### 2. Strategy Generation Failed

```python
def generate_fix_strategy(issue: Issue) -> FixStrategy:
    """Generate strategy with error handling."""
    
    # Pattern: Retry with Exponential Backoff (SKILL.md)
    @retry(max_attempts=3, exceptions=(NetworkError, APIError))
    def call_ai_for_strategy():
        return ai_service.generate_strategy(issue)
    
    try:
        return call_ai_for_strategy()
    except Exception as e:
        # Pattern: Fallback Chain
        logger.warning(f"AI strategy generation failed: {e}")
        
        # Fallback 1: Use template-based strategy
        try:
            return get_template_strategy(issue.type)
        except TemplateNotFoundError:
            # Fallback 2: Mark for manual review
            return FixStrategy(
                type="manual",
                description=f"Requires manual review: {str(e)}",
                can_auto_execute=False
            )
```

**Recovery**: Multi-level fallback - AI → Template → Manual.

---

## Phase 2: Execution - Fix Failures

### Pattern: **Circuit Breaker** + **Rollback** (SKILL.md)

Prevent cascading failures and enable recovery.

### Error Scenarios

#### 1. Fix Causes Test Failures

```python
class TestFailureError(ApplicationError):
    """Raised when tests fail after applying fix."""
    def __init__(self, issue_id: str, failed_tests: list[str]):
        super().__init__(
            f"Tests failed after applying fix for {issue_id}",
            code="TEST_FAILURE_AFTER_FIX",
            details={
                "issue_id": issue_id,
                "failed_tests": failed_tests,
                "action": "Fix has been rolled back"
            }
        )

class FixExecutor:
    def __init__(self):
        self.circuit_breaker = CircuitBreaker(
            failure_threshold=3,
            timeout=timedelta(minutes=5)
        )
        self.checkpoints = {}
    
    def execute_fix(self, issue: Issue) -> FixResult:
        """Execute fix with rollback capability."""
        
        # Create checkpoint before fix
        checkpoint_id = f"fix-{issue.id}-{int(time.time())}"
        self.create_checkpoint(checkpoint_id)
        
        try:
            # Use circuit breaker to prevent cascading failures
            result = self.circuit_breaker.call(
                lambda: self._apply_fix(issue)
            )
            
            # Validate fix didn't break tests
            if not self.run_tests():
                raise TestFailureError(
                    issue.id,
                    self.get_failed_tests()
                )
            
            return FixResult(
                status="success",
                issue_id=issue.id,
                files_changed=result.files
            )
            
        except Exception as e:
            # Rollback on any error
            self.rollback_to_checkpoint(checkpoint_id)
            
            # Re-raise with context
            raise FixExecutionError(
                f"Fix failed for {issue.id}",
                issue_id=issue.id,
                files=issue.files,
                attempted_fix=issue.strategy.description,
                original_error=e
            ) from e
        finally:
            # Cleanup checkpoint after successful fix
            if checkpoint_id in self.checkpoints:
                self.cleanup_checkpoint(checkpoint_id)
    
    def create_checkpoint(self, checkpoint_id: str) -> None:
        """Create git stash checkpoint."""
        subprocess.run([
            'git', 'stash', 'push', '-u',
            '-m', f'Checkpoint: {checkpoint_id}'
        ], check=True)
        self.checkpoints[checkpoint_id] = {
            'timestamp': time.time(),
            'stash_ref': self.get_latest_stash_ref()
        }
    
    def rollback_to_checkpoint(self, checkpoint_id: str) -> None:
        """Rollback to checkpoint."""
        if checkpoint_id not in self.checkpoints:
            logger.error(f"Checkpoint {checkpoint_id} not found")
            return
        
        stash_ref = self.checkpoints[checkpoint_id]['stash_ref']
        
        # Reset working directory
        subprocess.run(['git', 'reset', '--hard', 'HEAD'], check=True)
        subprocess.run(['git', 'clean', '-fd'], check=True)
        
        # Restore from stash
        subprocess.run(['git', 'stash', 'pop', stash_ref], check=True)
        
        logger.info(f"Rolled back to checkpoint {checkpoint_id}")
```

**Recovery**: Automatic rollback to last known good state.

---

#### 2. Timeout Exceeded

```python
class TimeoutError(ApplicationError):
    """Raised when operation exceeds time budget."""
    def __init__(self, operation: str, timeout_seconds: int):
        super().__init__(
            f"Operation '{operation}' exceeded timeout",
            code="TIMEOUT_EXCEEDED",
            details={
                "operation": operation,
                "timeout_seconds": timeout_seconds,
                "suggestion": "Increase --time-budget or simplify fix"
            }
        )

async def execute_with_timeout(
    operation: Callable[[], T],
    timeout_seconds: int,
    operation_name: str
) -> T:
    """Execute operation with timeout."""
    try:
        return await asyncio.wait_for(
            operation(),
            timeout=timeout_seconds
        )
    except asyncio.TimeoutError:
        raise TimeoutError(operation_name, timeout_seconds)

# Usage in fix execution
async def apply_fix_with_timeout(issue: Issue) -> FixResult:
    try:
        result = await execute_with_timeout(
            lambda: apply_fix(issue),
            timeout_seconds=1800,  # 30 minutes
            operation_name=f"Fix for {issue.id}"
        )
        return result
    except TimeoutError as e:
        # Pattern: Save progress and pause
        save_progress({
            'issue': issue.to_dict(),
            'status': 'timeout',
            'can_resume': True,
            'checkpoint': create_checkpoint(f"timeout-{issue.id}")
        })
        
        # Continue with next issue instead of failing entire batch
        logger.warning(f"Fix timeout: {e.message}")
        return FixResult(status="timeout", issue_id=issue.id)
```

**Recovery**: Save progress, continue with next issue.

---

#### 3. Multiple Fixes Fail

```python
class BatchFixExecutor:
    def __init__(self):
        self.results: list[FixResult] = []
        self.errors = ErrorCollector()
    
    def execute_batch(self, issues: list[Issue]) -> BatchResult:
        """Execute multiple fixes with error aggregation."""
        
        for issue in issues:
            try:
                result = self.execute_fix(issue)
                self.results.append(result)
                
            except FixExecutionError as e:
                # Pattern: Error Aggregation (SKILL.md)
                self.errors.add(e)
                
                # Continue with next issue
                logger.warning(f"Fix failed for {issue.id}: {e.message}")
                continue
            
            except Exception as e:
                # Unexpected errors
                logger.exception(f"Unexpected error for {issue.id}")
                self.errors.add(ApplicationError(
                    f"Unexpected error fixing {issue.id}",
                    code="UNEXPECTED_ERROR",
                    details={"issue_id": issue.id}
                ))
        
        # Return results even if some failed
        return BatchResult(
            successful=len([r for r in self.results if r.status == "success"]),
            failed=len(self.errors.getErrors()),
            results=self.results,
            errors=self.errors.getErrors()
        )
```

**Recovery**: Continue execution, aggregate errors for final report.

---

## Phase 3: Reporting - Commit Errors

### Pattern: **Graceful Degradation** (SKILL.md)

### Error Scenarios

#### 1. Commit Failed

```python
def create_commits(results: list[FixResult]) -> CommitResult:
    """Create commits with error handling."""
    
    try:
        # Group fixes by type
        grouped = group_fixes_by_type(results)
        
        for fix_type, fixes in grouped.items():
            # Stage files
            for fix in fixes:
                for file in fix.files_changed:
                    subprocess.run(['git', 'add', file], check=True)
            
            # Create commit
            commit_message = generate_commit_message(fix_type, fixes)
            subprocess.run(
                ['git', 'commit', '-m', commit_message],
                check=True
            )
        
        return CommitResult(status="success", commits=len(grouped))
        
    except subprocess.CalledProcessError as e:
        # Pattern: Graceful Degradation
        logger.error(f"Commit failed: {e}")
        
        # Fallback: Save patch files instead
        patch_file = f'.claude/patches/fix-issues-{int(time.time())}.patch'
        subprocess.run(
            ['git', 'diff', '--cached'],
            stdout=open(patch_file, 'w')
        )
        
        return CommitResult(
            status="degraded",
            commits=0,
            patch_file=patch_file,
            message=f"Commits failed, saved patch to {patch_file}"
        )
```

**Recovery**: Save patch files if commits fail.

---

#### 2. Report Generation Failed

```python
def generate_report(results: BatchResult) -> Report:
    """Generate report with fallback formatting."""
    
    # Pattern: Multiple Fallbacks
    try:
        # Primary: Rich markdown report
        return generate_rich_markdown_report(results)
    except Exception as e:
        logger.warning(f"Rich report generation failed: {e}")
        
        try:
            # Fallback 1: Simple markdown
            return generate_simple_markdown_report(results)
        except Exception as e:
            logger.warning(f"Simple report generation failed: {e}")
            
            # Fallback 2: JSON dump
            return Report(
                format="json",
                content=json.dumps(results.to_dict(), indent=2)
            )
```

**Recovery**: Progressive degradation in report quality.

---

## Error Handling Checklist for Commands

Use this checklist when implementing any Claude command:

### Pre-Execution
- [ ] Validate git repository exists
- [ ] Check required tools are installed
- [ ] Validate input files/arguments exist
- [ ] Check for conflicting state
- [ ] Verify permissions (file write, git operations)

### During Execution
- [ ] Create checkpoints before risky operations
- [ ] Use circuit breakers for repeated operations
- [ ] Implement timeout protection
- [ ] Aggregate errors instead of failing fast
- [ ] Log errors with full context

### Error Recovery
- [ ] Define rollback mechanism for each operation
- [ ] Implement fallback strategies
- [ ] Save progress for resumability
- [ ] Provide clear error messages with suggestions

### Post-Execution
- [ ] Clean up temporary files
- [ ] Close resources (files, connections)
- [ ] Generate error report even on partial failure
- [ ] Log metrics (success rate, error types)

---

## Integration with SKILL.md Patterns

| Command Phase | SKILL.md Pattern | When to Use |
|---------------|------------------|-------------|
| Discovery | Fail Fast | Input validation, preconditions |
| Discovery | Graceful Degradation | Missing optional inputs |
| Planning | Error Aggregation | Validating multiple issues |
| Planning | Result Types | Strategy generation |
| Execution | Circuit Breaker | Repeated fix operations |
| Execution | Retry + Backoff | Network calls, flaky operations |
| Execution | Rollback | Any state-changing operation |
| Reporting | Graceful Degradation | Report generation, commits |

---

## Metrics to Track

Track these error metrics for command health:

```python
@dataclass
class ErrorMetrics:
    total_errors: int
    errors_by_phase: dict[str, int]  # discovery, planning, execution, reporting
    errors_by_type: dict[str, int]   # validation, timeout, test_failure, etc.
    recovery_success_rate: float     # successful recoveries / total errors
    rollback_count: int
    time_lost_to_errors: float       # seconds
    
def log_metrics(metrics: ErrorMetrics):
    """Log error metrics for monitoring."""
    logger.info(f"""
    Error Metrics:
      Total: {metrics.total_errors}
      By Phase: {metrics.errors_by_phase}
      By Type: {metrics.errors_by_type}
      Recovery Rate: {metrics.recovery_success_rate:.1%}
      Rollbacks: {metrics.rollback_count}
      Time Lost: {metrics.time_lost_to_errors:.1f}s
    """)
```

---

## Related References

- **[SKILL.md](../SKILL.md)**: Core error handling patterns
- **[fix-issues-scenarios.md](../../assets/fix-issues-scenarios.md)**: Complete scenario catalog
- **[exception-hierarchy-design.md](../references/exception-hierarchy-design.md)**: Error class design
- **[error-recovery-strategies.md](../references/error-recovery-strategies.md)**: Recovery patterns