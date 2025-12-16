---
name: pytest
description: Python testing framework with fixtures, parametrization, mocking, and plugins. Covers test discovery, assertions, conftest.py, markers, and unittest.mock integration. Use when writing Python tests, setting up test infrastructure, implementing fixtures, or creating test suites with complex setup requirements.
---

# pytest

Powerful Python testing framework with expressive syntax and rich plugin ecosystem.

## Quick Start

```bash
# Install pytest with common plugins
pip install pytest pytest-mock pytest-cov pytest-asyncio

# Run tests
pytest                     # Discover and run all tests
pytest -v                  # Verbose output
pytest -k "test_name"       # Run specific tests
pytest --cov=src          # Run with coverage
pytest -x                  # Stop on first failure
```

## Test Structure

```python
# test_module.py
import pytest
from mymodule import calculate

def test_calculate_basic():
    """Tests basic functionality"""
    assert calculate(2, 3) == 5

class TestCalculateAdvanced:
    """Group related tests in a class"""

    @pytest.mark.parametrize("a,b,expected", [
        (1, 2, 3),
        (-1, 1, 0),
        (0, 0, 0),
    ])
    def test_calculate_cases(self, a, b, expected):
        assert calculate(a, b) == expected
```

## Fixtures

### Basic Fixtures
```python
@pytest.fixture
def sample_data():
    """Simple fixture returning data"""
    return {"name": "test", "value": 42}

def test_with_data(sample_data):
    assert sample_data["name"] == "test"
```

### Fixture with Setup/Teardown
```python
@pytest.fixture
def database():
    """Fixture with setup and cleanup"""
    db = Database(":memory:")
    db.create_tables()
    yield db
    db.close()

def test_database_operations(database):
    # Use database fixture
    result = database.query("SELECT 1")
    assert result is not None
```

### Fixture Scopes
```python
@pytest.fixture(scope="module")  # Created once per module
def api_client():
    return TestClient()

@pytest.fixture(scope="session")  # Created once per test session
def test_environment():
    setup_test_env()
    yield
    cleanup_test_env()

# Default scope="function" - created for each test
@pytest.fixture
def temp_file(tmp_path):
    file = tmp_path / "test.txt"
    file.write_text("content")
    return file
```

### Using conftest.py
```python
# conftest.py - Shared fixtures for all tests
import pytest
import pandas as pd

@pytest.fixture
def sample_dataframe():
    """DataFrame available to all tests"""
    return pd.DataFrame({
        "id": [1, 2, 3],
        "name": ["A", "B", "C"]
    })

@pytest.fixture(autouse=True)
def setup_test_environment():
    """Automatically used for all tests"""
    # Setup
    old_env = os.environ.get("TEST_ENV")
    os.environ["TEST_ENV"] = "testing"

    yield

    # Cleanup
    if old_env:
        os.environ["TEST_ENV"] = old_env
    else:
        del os.environ["TEST_ENV"]
```

## Parametrization

### Basic Parametrization
```python
@pytest.mark.parametrize("input,expected", [
    ("hello", "HELLO"),
    ("world", "WORLD"),
    ("", ""),
    ("123", "123"),  # Numbers stay the same
])
def test_uppercase(input, expected):
    assert input.upper() == expected
```

### Multiple Parameters
```python
@pytest.mark.parametrize("x,y,operation,expected", [
    (1, 2, "+", 3),
    (5, 3, "-", 2),
    (4, 3, "*", 12),
    (10, 2, "/", 5),
])
def test_calculator(x, y, operation, expected):
    if operation == "+":
        assert x + y == expected
    elif operation == "-":
        assert x - y == expected
    elif operation == "*":
        assert x * y == expected
    elif operation == "/":
        assert x / y == expected
```

### Parametrize with IDs
```python
@pytest.mark.parametrize(
    "user_input,status_code",
    [
        ("valid@email.com", 200),
        ("invalid-email", 400),
        ("", 400),
        ("@domain.com", 400),
    ],
    ids=["valid", "invalid_format", "empty", "missing_local"]
)
def test_email_validation(user_input, status_code):
    response = validate_email(user_input)
    assert response.status_code == status_code
```

## Mocking and Patching

### Using pytest-mock
```python
def test_with_mock_fixture(mocker):
    """Use the mocker fixture for easy mocking"""
    # Mock a function
    mock_func = mocker.patch("module.function")
    mock_func.return_value = 42

    result = module.function()
    assert result == 42
    mock_func.assert_called_once()

def test_mock_object(mocker):
    """Create mock objects"""
    mock_service = mocker.Mock()
    mock_service.get_data.return_value = {"id": 1, "value": "test"}

    client = Client(mock_service)
    result = client.fetch_data()

    assert result["id"] == 1
    mock_service.get_data.assert_called_once()
```

### Patching External Dependencies
```python
@pytest.mark.parametrize("http_status", [200, 404, 500])
@patch("requests.get")
def test_api_responses(mock_get, http_status):
    """Test different API response scenarios"""
    mock_get.return_value.status_code = http_status

    if http_status == 200:
        mock_get.return_value.json.return_value = {"data": "success"}

    response = fetch_api_data()

    if http_status == 200:
        assert response["data"] == "success"
    else:
        assert response is None

@patch("builtins.open", new_callable=mock_open,
       read_data='{"config": "value"}')
def test_file_loading(mock_file):
    """Mock file operations"""
    config = load_config("config.json")
    assert config["config"] == "value"
```

### Async Testing with pytest-asyncio
```python
import pytest
import asyncio

@pytest.mark.asyncio
async def test_async_function():
    """Test async functions"""
    result = await async_operation()
    assert result is not None

@pytest.mark.asyncio
async def test_async_context_manager(async_client):
    """Test with async fixtures"""
    response = await async_client.get("/api/data")
    assert response.status_code == 200
```

## Assertions and Markers

### Rich Assertions
```python
def test_assertions():
    """pytest provides rich assertion messages"""
    # Collections
    assert [1, 2, 3] == [1, 2, 3]
    assert "hello" in ["hello", "world"]

    # Dictionaries
    data = {"name": "test", "age": 25}
    assert "name" in data
    assert data.get("age") == 25

    # Exceptions
    with pytest.raises(ValueError, match="must be positive"):
        calculate_age(-5)

    # Warnings
    with pytest.warns(DeprecationWarning):
        deprecated_function()

    # Approximate values
    assert 0.1 + 0.2 == pytest.approx(0.3)
```

### Custom Markers
```python
# pytest.ini or conftest.py
pytest_markers = {
    "slow": "marks tests as slow (deselect with '-m \"not slow\"')",
    "integration": "marks tests as integration tests",
    "unit": "marks tests as unit tests",
}

# Usage in tests
@pytest.mark.slow
def test_slow_operation():
    time.sleep(5)  # Slow operation
    assert True

@pytest.mark.integration
@pytest.mark.external_api
def test_api_integration():
    response = requests.get("https://api.example.com")
    assert response.status_code == 200
```

## Test Organization

### Directory Structure
```
project/
├── src/
│   └── mymodule/
├── tests/
│   ├── unit/
│   │   ├── test_core.py
│   │   └── test_utils.py
│   ├── integration/
│   │   ├── test_api.py
│   │   └── test_database.py
│   ├── conftest.py
│   └── fixtures/
│       ├── sample_data.json
│       └── test_config.yaml
```

### Test Configuration
```python
# conftest.py
import pytest
import os

def pytest_configure(config):
    """Custom configuration"""
    os.environ["TESTING"] = "true"

def pytest_collection_modifyitems(config, items):
    """Modify test collection"""
    for item in items:
        # Add markers based on file location
        if "unit/" in str(item.fspath):
            item.add_marker(pytest.mark.unit)
        elif "integration/" in str(item.fspath):
            item.add_marker(pytest.mark.integration)

def pytest_runtest_setup(item):
    """Setup before each test"""
    print(f"\nRunning: {item.name}")
```

## Testing Patterns

### Data-Driven Tests
```python
# Load test data from CSV
import csv

def load_test_cases():
    with open("test_cases.csv") as f:
        reader = csv.DictReader(f)
        return [(row["input"], row["expected"]) for row in reader]

@pytest.mark.parametrize("input_val,expected", load_test_cases())
def test_data_driven(input_val, expected):
    assert process(input_val) == expected
```

### Test Factories
```python
@pytest.fixture
def user_factory():
    """Factory fixture for creating test users"""
    def _create_user(**kwargs):
        defaults = {"id": 1, "name": "Test User", "email": "test@example.com"}
        defaults.update(kwargs)
        return User(**defaults)
    return _create_user

def test_with_factory(user_factory):
    user = user_factory(id=42, name="Custom User")
    assert user.id == 42
    assert user.name == "Custom User"
```

### Environment Testing
```python
@pytest.fixture(params=["sqlite", "postgres", "mysql"])
def db_connection(request):
    """Test against multiple databases"""
    if request.param == "sqlite":
        connection = create_sqlite_connection()
    elif request.param == "postgres":
        connection = create_postgres_connection()
    elif request.param == "mysql":
        connection = create_mysql_connection()

    yield connection
    connection.close()

def test_database_operations(db_connection):
    """Test works with all configured databases"""
    result = db_connection.execute("SELECT 1")
    assert result is not None
```

## Best Practices

### 1. Test Isolation
```python
# Good: Each test is independent
def test_create_user():
    user = User(name="Test")
    assert user.name == "Test"

def test_user_validation():
    user = User(name="")  # Fresh instance
    assert not user.is_valid()

# Bad: Tests share state
user = User()  # Shared - anti-pattern!
def test_user_create():
    user.name = "Test"

def test_user_validate():
    assert user.name == "Test"  # Depends on previous test
```

### 2. Descriptive Test Names
```python
# Good: Clear what's being tested
def test_user_creation_with_valid_data_succeeds():
    pass

def test_email_validation_rejects_invalid_format():
    pass

# Avoid: Generic names
def test_user():
    pass

def test_validation():
    pass
```

### 3. Use Fixtures Effectively
```python
# Good: Fixtures encapsulate setup logic
@pytest.fixture
def authenticated_client(client, user):
    """Create authenticated client for API tests"""
    client.force_login(user)
    return client

def test_protected_endpoint(authenticated_client):
    response = authenticated_client.get("/api/profile")
    assert response.status_code == 200
```

### 4. Test Error Conditions
```python
def test_api_error_handling(mocker):
    """Test how code handles errors"""
    mocker.patch("external_api.get", side_effect=ConnectionError())

    with pytest.raises(ServiceUnavailable):
        fetch_external_data()
```

## Running Tests

### Command Line Options
```bash
# Basic commands
pytest                          # Run all tests
pytest -v                       # Verbose output
pytest -s                       # Show print statements
pytest -q                       # Quiet mode
pytest -x                       # Stop on first failure
pytest --lf                     # Run last failed tests

# Filtering
pytest -k "user"                # Run tests with "user" in name
pytest -m "not slow"             # Skip slow tests
pytest --ignore=tests/integration/  # Skip directory

# Coverage
pytest --cov=src                # Coverage report
pytest --cov=src --cov-report=html  # HTML report
pytest --cov-fail-under=80        # Fail if coverage < 80%

# Parallel execution
pytest -n auto                   # Run with all CPUs
pytest -n 4                      # Run with 4 workers
```

### Configuration Files
```ini
# pytest.ini
[tool:pytest]
minversion = 6.0
addopts = -ra -q --strict-markers
testpaths = tests
python_files = test_*.py *_test.py
python_classes = Test*
python_functions = test_*
markers =
    slow: marks tests as slow (deselect with '-m "not slow"')
    integration: marks tests as integration tests
```

## Resources

- [pytest Documentation](https://docs.pytest.org/)
- [pytest-mock](https://github.com/pytest-dev/pytest-mock)
- [pytest-cov](https://github.com/pytest-dev/pytest-cov)
- [pytest-asyncio](https://github.com/pytest-dev/pytest-asyncio)
