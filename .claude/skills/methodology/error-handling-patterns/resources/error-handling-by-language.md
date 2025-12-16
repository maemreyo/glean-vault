# Error Handling by Language

Language-specific error handling patterns and best practices.

## TypeScript/JavaScript

### Async/Await Error Handling
```typescript
// Always use try-catch with async/await
async function fetchData(id: string) {
  try {
    const response = await fetch(`/api/data/${id}`);
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }
    return await response.json();
  } catch (error) {
    // Preserve error type and context
    throw new Error(`Failed to fetch data for ${id}: ${error.message}`, {
      cause: error,
      id
    });
  }
}

// Wrapper for consistent error handling
class Result<T, E = Error> {
  constructor(
    public success: boolean,
    public data?: T,
    public error?: E
  ) {}

  static ok<T>(data: T): Result<T> {
    return new Result(true, data);
  }

  static err<E>(error: E): Result<never, E> {
    return new Result(false, undefined, error);
  }

  map<U>(fn: (data: T) => U): Result<U, E> {
    if (this.success && this.data) {
      return Result.ok(fn(this.data));
    }
    return Result.err(this.error!);
  }

  flatMap<U>(fn: (data: T) => Result<U, E>): Result<U, E> {
    if (this.success && this.data) {
      return fn(this.data);
    }
    return Result.err(this.error!);
  }
}
```

### Error Boundaries in React
```typescript
interface ErrorBoundaryState {
  hasError: boolean;
  error?: Error;
}

interface ErrorBoundaryProps {
  fallback?: React.ComponentType<{ error?: Error }>;
  onError?: (error: Error, errorInfo: React.ErrorInfo) => void;
}

class ErrorBoundary extends Component<ErrorBoundaryProps, ErrorBoundaryState> {
  constructor(props: ErrorBoundaryProps) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error: Error): ErrorBoundaryState {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    console.error('Error caught by boundary:', error, errorInfo);
    this.props.onError?.(error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      const FallbackComponent = this.props.fallback || DefaultErrorFallback;
      return <FallbackComponent error={this.state.error} />;
    }
    return this.props.children;
  }
}
```

### Node.js Error Handling
```typescript
// Global error handlers
process.on('uncaughtException', (error) => {
  console.error('Uncaught Exception:', error);
  // Perform cleanup
  process.exit(1);
});

process.on('unhandledRejection', (reason, promise) => {
  console.error('Unhandled Rejection at:', promise, 'reason:', reason);
});

// Express error handling middleware
const errorHandler: ErrorRequestHandler = (
  error,
  req,
  res,
  next
) => {
  // Don't leak error details in production
  const message = process.env.NODE_ENV === 'production'
    ? 'Internal server error'
    : error.message;

  const status = error.status || 500;

  res.status(status).json({
    error: {
      message,
      timestamp: new Date().toISOString(),
      requestId: req.id
    }
  });
};
```

## Python

### Exception Hierarchy
```python
class AppError(Exception):
    """Base exception for application"""
    def __init__(self, message: str, context: dict = None):
        super().__init__(message)
        self.context = context or {}
        self.timestamp = datetime.utcnow()

class ValidationError(AppError):
    """Validation related errors"""
    pass

class NotFoundError(AppError):
    """Resource not found errors"""
    pass

class DatabaseError(AppError):
    """Database operation errors"""
    def __init__(self, message: str, query: str = None, **kwargs):
        super().__init__(message, **kwargs)
        self.query = query

class ExternalServiceError(AppError):
    """External service errors"""
    def __init__(self, message: str, service: str = None, retry_after: int = None, **kwargs):
        super().__init__(message, **kwargs)
        self.service = service
        self.retry_after = retry_after
```

### Context Manager for Error Handling
```python
from contextlib import contextmanager
from typing import Type, Tuple

@contextmanager
def error_handler(
    error_types: Tuple[Type[Exception], ...] = (Exception,),
    fallback: Any = None,
    logger: logging.Logger = None
):
    """Context manager for consistent error handling"""
    try:
        yield
    except error_types as e:
        if logger:
            logger.error(f"Error in context: {e}", exc_info=True)

        if fallback is not None:
            return fallback
        raise

# Usage
with error_handler((ValueError, TypeError), fallback=None, logger=logger):
    data = process_input(user_input)
    result = transform_data(data)
```

### Result Type in Python
```python
from typing import TypeVar, Generic, Union

T = TypeVar('T')
E = TypeVar('E', bound=Exception)

class Result(Generic[T, E]):
    def __init__(self, success: bool, value: T = None, error: E = None):
        self.success = success
        self._value = value
        self._error = error

    @property
    def value(self) -> T:
        if not self.success:
            raise ValueError("No value available for failed result")
        return self._value

    @property
    def error(self) -> E:
        if self.success:
            raise ValueError("No error available for successful result")
        return self._error

    @classmethod
    def ok(cls, value: T) -> 'Result[T, E]':
        return cls(True, value=value)

    @classmethod
    def err(cls, error: E) -> 'Result[T, E]':
        return cls(False, error=error)

    def map(self, fn):
        if self.success:
            try:
                return Result.ok(fn(self._value))
            except Exception as e:
                return Result.err(e)
        return Result.err(self._error)

    def flat_map(self, fn):
        if self.success:
            try:
                return fn(self._value)
            except Exception as e:
                return Result.err(e)
        return Result.err(self._error)

# Usage
def parse_int(value: str) -> Result[int, ValueError]:
    try:
        return Result.ok(int(value))
    except ValueError as e:
        return Result.err(e)
```

### Decorator for Error Handling
```python
from functools import wraps
from typing import Type, Tuple, Callable, Any

def handle_errors(
    error_types: Tuple[Type[Exception], ...] = (Exception,),
    fallback: Any = None,
    logger: logging.Logger = None
):
    """Decorator for error handling"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except error_types as e:
                if logger:
                    logger.error(f"Error in {func.__name__}: {e}", exc_info=True)

                if fallback is not None:
                    return fallback
                raise
        return wrapper
    return decorator

# Usage
@handle_errors((ValueError, TypeError), fallback=0)
def calculate_total(items: List[dict]) -> float:
    return sum(item['price'] for item in items)
```

## Java

### Custom Exception Hierarchy
```java
public abstract class AppException extends Exception {
    private final ErrorCode errorCode;
    private final Map<String, Object> context;

    public AppException(ErrorCode errorCode, String message, Throwable cause) {
        super(message, cause);
        this.errorCode = errorCode;
        this.context = new HashMap<>();
    }

    public AppException(ErrorCode errorCode, String message) {
        this(errorCode, message, null);
    }

    public AppException withContext(String key, Object value) {
        this.context.put(key, value);
        return this;
    }

    public ErrorCode getErrorCode() {
        return errorCode;
    }

    public Map<String, Object> getContext() {
        return Collections.unmodifiableMap(context);
    }
}

public class ValidationException extends AppException {
    private final Map<String, String> fieldErrors;

    public ValidationException(Map<String, String> fieldErrors) {
        super(ErrorCode.VALIDATION_ERROR, "Validation failed");
        this.fieldErrors = fieldErrors;
    }

    public Map<String, String> getFieldErrors() {
        return fieldErrors;
    }
}

public class ResourceNotFoundException extends AppException {
    public ResourceNotFoundException(String resource, String id) {
        super(ErrorCode.NOT_FOUND,
              String.format("%s with id %s not found", resource, id));
    }
}
```

### Either Monad for Error Handling
```java
public final class Either<L, R> {
    private final L left;
    private final R right;
    private final boolean isRight;

    private Either(L left, R right, boolean isRight) {
        this.left = left;
        this.right = right;
        this.isRight = isRight;
    }

    public static <L, R> Either<L, R> left(L value) {
        return new Either<>(value, null, false);
    }

    public static <L, R> Either<L, R> right(R value) {
        return new Either<>(null, value, true);
    }

    public <T> Either<L, T> map(Function<R, T> mapper) {
        if (isRight) {
            return Either.right(mapper.apply(right));
        }
        return Either.left(left);
    }

    public <T> Either<L, T> flatMap(Function<R, Either<L, T>> mapper) {
        if (isRight) {
            return mapper.apply(right);
        }
        return Either.left(left);
    }

    public R orElse(R defaultValue) {
        return isRight ? right : defaultValue;
    }

    public Optional<R> toOptional() {
        return isRight ? Optional.of(right) : Optional.empty();
    }
}
```

### Try-with-Resources Pattern
```java
public class ResourceHandler {
    public <T, R extends AutoCloseable> Either<AppException, T> withResource(
        Supplier<R> resourceSupplier,
        Function<R, Either<AppException, T>> operation
    ) {
        try (R resource = resourceSupplier.get()) {
            return operation.apply(resource);
        } catch (Exception e) {
            return Either.left(new AppException(ErrorCode.RESOURCE_ERROR,
                                            "Resource operation failed", e));
        }
    }
}
```

## C#/.NET

### Result Pattern
```csharp
public class Result<T>
{
    public bool IsSuccess { get; }
    public bool IsFailure => !IsSuccess;
    public T Value { get; }
    public Error Error { get; }

    private Result(bool isSuccess, T value, Error error)
    {
        IsSuccess = isSuccess;
        Value = value;
        Error = error;
    }

    public static Result<T> Success(T value) => new Result<T>(true, value, null);
    public static Result<T> Failure(Error error) => new Result<T>(false, default, error);

    public TResult Match<TResult>(
        Func<T, TResult> onSuccess,
        Func<Error, TResult> onFailure)
    {
        return IsSuccess ? onSuccess(Value) : onFailure(Error);
    }

    public Result<TNext> Map<TNext>(Func<T, TNext> mapper)
    {
        return IsSuccess
            ? Result.Success(mapper(Value))
            : Result.Failure(Error);
    }

    public async Task<Result<TNext>> MapAsync<TNext>(Func<T, Task<TNext>> mapper)
    {
        return IsSuccess
            ? Result.Success(await mapper(Value))
            : Result.Failure(Error);
    }
}

public class Error
{
    public string Code { get; }
    public string Message { get; }
    public Exception Exception { get; }

    public Error(string code, string message, Exception exception = null)
    {
        Code = code;
        Message = message;
        Exception = exception;
    }

    public static Error Validation(string message) =>
        new Error("VALIDATION_ERROR", message);

    public static Error NotFound(string resource) =>
        new Error("NOT_FOUND", $"{resource} not found");

    public static Error Internal(Exception exception) =>
        new Error("INTERNAL_ERROR", "An internal error occurred", exception);
}
```

### Async Error Handling
```csharp
public static class AsyncErrorHandling
{
    public static async Task<Result<T>> SafeExecute<T>(
        Func<Task<T>> operation,
        Func<Exception, Error> errorMapper = null)
    {
        try
        {
            var result = await operation();
            return Result.Success(result);
        }
        catch (Exception ex)
        {
            var error = errorMapper?.Invoke(ex) ?? Error.Internal(ex);
            return Result.Failure(error);
        }
    }

    public static async Task<Result<T>> WithRetry<T>(
        Func<Task<T>> operation,
        int maxAttempts = 3,
        TimeSpan? delay = null)
    {
        var attempt = 0;
        var actualDelay = delay ?? TimeSpan.FromSeconds(1);

        while (attempt < maxAttempts)
        {
            attempt++;

            try
            {
                var result = await operation();
                return Result.Success(result);
            }
            catch when (attempt < maxAttempts)
            {
                await Task.Delay(actualDelay);
                actualDelay = TimeSpan.FromSeconds(actualDelay.TotalSeconds * 2);
            }
        }

        return Result.Failure(Error.Internal(
            new Exception($"Operation failed after {maxAttempts} attempts")));
    }
}
```

## Go

### Error Types and Wrapping
```go
package errors

import (
    "fmt"
    "net/http"
)

type ErrorCode string

const (
    ErrCodeValidation ErrorCode = "VALIDATION_ERROR"
    ErrCodeNotFound    ErrorCode = "NOT_FOUND"
    ErrCodeInternal    ErrorCode = "INTERNAL_ERROR"
    ErrCodeUnauthorized ErrorCode = "UNAUTHORIZED"
)

type AppError struct {
    Code    ErrorCode
    Message string
    Cause   error
    Context map[string]interface{}
}

func (e *AppError) Error() string {
    if e.Cause != nil {
        return fmt.Sprintf("%s: %s (caused by: %v)", e.Code, e.Message, e.Cause)
    }
    return fmt.Sprintf("%s: %s", e.Code, e.Message)
}

func (e *AppError) Unwrap() error {
    return e.Cause
}

func NewAppError(code ErrorCode, message string, cause error) *AppError {
    return &AppError{
        Code:    code,
        Message: message,
        Cause:   cause,
        Context: make(map[string]interface{}),
    }
}

func (e *AppError) WithContext(key string, value interface{}) *AppError {
    e.Context[key] = value
    return e
}

// Helper functions
func ValidationError(message string) *AppError {
    return NewAppError(ErrCodeValidation, message, nil)
}

func NotFoundError(resource string) *AppError {
    return NewAppError(ErrCodeNotFound, fmt.Sprintf("%s not found", resource), nil)
}

func InternalError(cause error) *AppError {
    return NewAppError(ErrCodeInternal, "An internal error occurred", cause)
}
```

### Result Type in Go
```go
package result

type Result[T any] struct {
    value T
    err   error
}

func Ok[T any](value T) Result[T] {
    return Result[T]{value: value}
}

func Err[T any](err error) Result[T] {
    var zero T
    return Result[T]{err: err}
}

func (r Result[T]) IsOk() bool {
    return r.err == nil
}

func (r Result[T]) IsErr() bool {
    return r.err != nil
}

func (r Result[T]) Unwrap() T {
    if r.err != nil {
        panic("called Unwrap on Err result")
    }
    return r.value
}

func (r Result[T]) UnwrapOr(defaultValue T) T {
    if r.err != nil {
        return defaultValue
    }
    return r.value
}

func (r Result[T]) Map(fn func(T) T) Result[T] {
    if r.err != nil {
        return Err[T](r.err)
    }
    return Ok(fn(r.value))
}

func (r Result[T]) FlatMap(fn func(T) Result[T]) Result[T] {
    if r.err != nil {
        return Err[T](r.err)
    }
    return fn(r.value)
}
```

### Error Handling Middleware
```go
package middleware

import (
    "encoding/json"
    "net/http"
)

type ErrorResponse struct {
    Error struct {
        Code    string                 `json:"code"`
        Message string                 `json:"message"`
        Context map[string]interface{} `json:"context,omitempty"`
    } `json:"error"`
    Timestamp string `json:"timestamp"`
}

func ErrorHandler(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        defer func() {
            if err := recover(); err != nil {
                var appErr *AppError
                var ok bool

                if appErr, ok = err.(*AppError); !ok {
                    appErr = InternalError(fmt.Errorf("panic: %v", err))
                }

                switch appErr.Code {
                case ErrCodeNotFound:
                    w.WriteHeader(http.StatusNotFound)
                case ErrCodeValidation:
                    w.WriteHeader(http.StatusBadRequest)
                case ErrCodeUnauthorized:
                    w.WriteHeader(http.StatusUnauthorized)
                default:
                    w.WriteHeader(http.StatusInternalServerError)
                }

                response := ErrorResponse{
                    Error: struct {
                        Code    string                 `json:"code"`
                        Message string                 `json:"message"`
                        Context map[string]interface{} `json:"context,omitempty"`
                    }{
                        Code:    string(appErr.Code),
                        Message: appErr.Message,
                        Context: appErr.Context,
                    },
                    Timestamp: time.Now().UTC().Format(time.RFC3339),
                }

                json.NewEncoder(w).Encode(response)
            }
        }()

        next.ServeHTTP(w, r)
    })
}
```

## Rust

### Custom Error Types
```rust
use std::fmt;
use std::error::Error;

#[derive(Debug)]
pub enum AppError {
    Validation(String),
    NotFound(String),
    Database(String),
    ExternalService(String),
    Internal(String),
}

impl fmt::Display for AppError {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        match self {
            AppError::Validation(msg) => write!(f, "Validation error: {}", msg),
            AppError::NotFound(resource) => write!(f, "Resource not found: {}", resource),
            AppError::Database(msg) => write!(f, "Database error: {}", msg),
            AppError::ExternalService(msg) => write!(f, "External service error: {}", msg),
            AppError::Internal(msg) => write!(f, "Internal error: {}", msg),
        }
    }
}

impl Error for AppError {}

// Conversion from other error types
impl From<sqlx::Error> for AppError {
    fn from(err: sqlx::Error) -> Self {
        AppError::Database(err.to_string())
    }
}

impl From<reqwest::Error> for AppError {
    fn from(err: reqwest::Error) -> Self {
        AppError::ExternalService(err.to_string())
    }
}
```

### Result Type with Context
```rust
use std::result::Result as StdResult;

type Result<T> = StdResult<T, AppError>;

trait ResultExt<T> {
    fn with_context<F>(self, f: F) -> Result<T>
    where
        F: FnOnce() -> String;
}

impl<T, E> ResultExt<T> for StdResult<T, E>
where
    E: Into<AppError>,
{
    fn with_context<F>(self, f: F) -> Result<T>
    where
        F: FnOnce() -> String,
    {
        self.map_err(|e| {
            let app_err = e.into();
            match app_err {
                AppError::Internal(msg) => {
                    AppError::Internal(format!("{}: {}", f(), msg))
                }
                _ => app_err,
            }
        })
    }
}

// Usage
fn find_user(id: u64) -> Result<User> {
    sqlx::query_as::<_, User>("SELECT * FROM users WHERE id = $1")
        .bind(id)
        .fetch_one(&pool)
        .await
        .with_context(|| format!("Failed to find user with id {}", id))
}
```

### Error Handling in Async Functions
```rust
use tokio::time::{timeout, Duration};

pub async fn fetch_with_timeout(url: &str) -> Result<String> {
    let fetch_future = async {
        reqwest::get(url)
            .await
            .map_err(|e| AppError::ExternalService(e.to_string()))?
            .text()
            .await
            .map_err(|e| AppError::ExternalService(e.to_string()))
    };

    timeout(Duration::from_secs(5), fetch_future)
        .await
        .map_err(|_| AppError::ExternalService("Request timed out".to_string()))?
}

pub async fn process_with_retry<F, T, Fut>(
    operation: F,
    max_retries: usize,
    delay: Duration,
) -> Result<T>
where
    F: Fn() -> Fut,
    Fut: std::future::Future<Output = Result<T>>,
{
    let mut retries = 0;

    loop {
        match operation().await {
            Ok(result) => return Ok(result),
            Err(AppError::ExternalService(msg)) if retries < max_retries => {
                retries += 1;
                tokio::time::sleep(delay * retries).await;
            }
            Err(e) => return Err(e),
        }
    }
}
```

## Language-Specific Best Practices

### TypeScript/JavaScript
- Use union types for error discrimination
- Leverage async/await with proper error boundaries
- Implement global error handlers in Node.js
- Use React Error Boundaries for UI errors

### Python
- Create clear exception hierarchies
- Use context managers for resource management
- Implement proper logging with structured data
- Use decorators for cross-cutting error concerns

### Java
- Use checked exceptions for recoverable errors
- Create custom exception types with context
- Implement proper resource cleanup with try-with-resources
- Use Optional to avoid null pointer exceptions

### C#
- Leverage the Result pattern for method returns
- Use async/await with proper exception handling
- Implement global exception handling in ASP.NET
- Use Polly for resilience patterns

### Go
- Create explicit error types with wrapping
- Use error interfaces for consistent handling
- Implement proper error propagation
- Use context for request-scoped error handling

### Rust
- Use Result<T, E> for fallible operations
- Create custom error types with proper traits
- Leverage ? operator for error propagation
- Use context for additional error information