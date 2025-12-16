# TDD Language Examples

This document provides TDD examples specific to different programming languages and frameworks.

## TypeScript/JavaScript

### Jest Testing Framework

#### Basic Unit Test
```typescript
// calculator.test.ts
import { Calculator } from './calculator';

describe('Calculator', () => {
  let calculator: Calculator;

  beforeEach(() => {
    calculator = new Calculator();
  });

  // RED: Test doesn't compile yet
  it('should add two numbers', () => {
    expect(calculator.add(2, 3)).toBe(5);
  });

  it('should subtract two numbers', () => {
    expect(calculator.subtract(5, 3)).toBe(2);
  });
});
```

#### Implementation
```typescript
// calculator.ts
export class Calculator {
  add(a: number, b: number): number {
    return a + b;
  }

  subtract(a: number, b: number): number {
    return a - b;
  }
}
```

#### Async Testing
```typescript
describe('UserService', () => {
  it('should fetch user by id', async () => {
    const userService = new UserService();
    const user = await userService.findById(1);

    expect(user.id).toBe(1);
    expect(user.name).toBeDefined();
  });
});
```

#### Mock Testing
```typescript
import { UserService } from './UserService';
import { UserRepository } from './UserRepository';

describe('UserService', () => {
  let userService: UserService;
  let mockRepository: jest.Mocked<UserRepository>;

  beforeEach(() => {
    mockRepository = {
      findById: jest.fn(),
      save: jest.fn()
    } as any;
    userService = new UserService(mockRepository);
  });

  it('should find user by id', async () => {
    const mockUser = { id: 1, name: 'Test User' };
    mockRepository.findById.mockResolvedValue(mockUser);

    const user = await userService.findById(1);

    expect(user).toEqual(mockUser);
    expect(mockRepository.findById).toHaveBeenCalledWith(1);
  });
});
```

### React Component Testing

#### Component Test
```typescript
// UserProfile.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import { UserProfile } from './UserProfile';

describe('UserProfile', () => {
  it('should display user name', () => {
    const user = { id: 1, name: 'John Doe', email: 'john@example.com' };

    render(<UserProfile user={user} />);

    expect(screen.getByText('John Doe')).toBeInTheDocument();
    expect(screen.getByText('john@example.com')).toBeInTheDocument();
  });

  it('should call onEdit when edit button clicked', () => {
    const user = { id: 1, name: 'John Doe' };
    const onEdit = jest.fn();

    render(<UserProfile user={user} onEdit={onEdit} />);

    fireEvent.click(screen.getByRole('button', { name: /edit/i }));

    expect(onEdit).toHaveBeenCalledWith(1);
  });
});
```

#### Custom Hook Testing
```typescript
// useCounter.test.ts
import { renderHook, act } from '@testing-library/react-hooks';
import { useCounter } from './useCounter';

describe('useCounter', () => {
  it('should initialize with count', () => {
    const { result } = renderHook(() => useCounter(5));

    expect(result.current.count).toBe(5);
  });

  it('should increment count', () => {
    const { result } = renderHook(() => useCounter());

    act(() => {
      result.current.increment();
    });

    expect(result.current.count).toBe(1);
  });
});
```

## Python

### Pytest Framework

#### Basic Test
```python
# test_calculator.py
import pytest
from calculator import Calculator

class TestCalculator:
    def setup_method(self):
        self.calculator = Calculator()

    def test_add_two_numbers(self):
        assert self.calculator.add(2, 3) == 5

    def test_subtract_two_numbers(self):
        assert self.calculator.subtract(5, 3) == 2
```

#### Implementation
```python
# calculator.py
class Calculator:
    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b
```

#### Parametrized Tests
```python
import pytest

@pytest.mark.parametrize("input,expected", [
    ("test@example.com", True),
    ("invalid-email", False),
    ("", False),
    (None, False),
])
def test_email_validation(input, expected):
    from validators import is_valid_email
    assert is_valid_email(input) == expected
```

#### Mock Testing
```python
from unittest.mock import Mock, patch
from user_service import UserService

def test_get_user_by_id():
    # Arrange
    mock_repo = Mock()
    mock_repo.get_by_id.return_value = {"id": 1, "name": "Test"}
    service = UserService(mock_repo)

    # Act
    user = service.get_user(1)

    # Assert
    assert user["name"] == "Test"
    mock_repo.get_by_id.assert_called_once_with(1)
```

#### Async Testing
```python
import pytest
from httpx import AsyncClient
from app import app

@pytest.mark.asyncio
async def test_create_user():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/users",
            json={"name": "Test User", "email": "test@example.com"}
        )

    assert response.status_code == 201
    assert response.json()["name"] == "Test User"
```

## Java

### JUnit 5

#### Basic Test
```java
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class CalculatorTest {
    private Calculator calculator;

    @BeforeEach
    void setUp() {
        calculator = new Calculator();
    }

    @Test
    void addTwoNumbers() {
        assertEquals(5, calculator.add(2, 3));
    }

    @Test
    void subtractTwoNumbers() {
        assertEquals(2, calculator.subtract(5, 3));
    }
}
```

#### Implementation
```java
public class Calculator {
    public int add(int a, int b) {
        return a + b;
    }

    public int subtract(int a, int b) {
        return a - b;
    }
}
```

#### Mock Testing with Mockito
```java
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class UserServiceTest {
    @Mock
    private UserRepository userRepository;

    @Test
    void shouldCreateUser() {
        // Arrange
        UserService userService = new UserService(userRepository);
        User newUser = new User("test@example.com", "password");

        // Act
        userService.createUser(newUser);

        // Assert
        verify(userRepository).save(newUser);
    }
}
```

#### Spring Boot Testing
```java
@SpringBootTest
@AutoConfigureTestDatabase
class UserControllerIntegrationTest {
    @Autowired
    private TestRestTemplate restTemplate;

    @Test
    void shouldCreateUser() {
        UserRequest request = new UserRequest("test@example.com", "password");

        ResponseEntity<User> response = restTemplate.postForEntity(
            "/api/users",
            request,
            User.class
        );

        assertEquals(HttpStatus.CREATED, response.getStatusCode());
        assertNotNull(response.getBody().getId());
    }
}
```

## C#/.NET

### xUnit Framework

#### Basic Test
```csharp
using Xunit;

public class CalculatorTests
{
    private readonly Calculator _calculator;

    public CalculatorTests()
    {
        _calculator = new Calculator();
    }

    [Fact]
    public void Add_TwoNumbers_ReturnsSum()
    {
        // Arrange
        int a = 2;
        int b = 3;

        // Act
        int result = _calculator.Add(a, b);

        // Assert
        Assert.Equal(5, result);
    }

    [Theory]
    [InlineData(2, 3, 5)]
    [InlineData(-1, 1, 0)]
    [InlineData(0, 0, 0)]
    public void Add_VariousNumbers_ReturnsCorrectSum(int a, int b, int expected)
    {
        int result = _calculator.Add(a, b);
        Assert.Equal(expected, result);
    }
}
```

#### Mock Testing with Moq
```csharp
using Moq;
using Xunit;

public class UserServiceTests
{
    [Fact]
    public void CreateUser_ValidUser_CallsRepository()
    {
        // Arrange
        var mockRepository = new Mock<IUserRepository>();
        var userService = new UserService(mockRepository.Object);
        var user = new User { Email = "test@example.com" };

        // Act
        userService.CreateUser(user);

        // Assert
        mockRepository.Verify(r => r.Save(user), Times.Once);
    }
}
```

## Go

### Testing Package

#### Basic Test
```go
package calculator

import (
    "testing"
)

func TestAdd(t *testing.T) {
    calculator := NewCalculator()

    result := calculator.Add(2, 3)

    if result != 5 {
        t.Errorf("Expected 5, got %d", result)
    }
}

func TestTableDriven(t *testing.T) {
    tests := []struct {
        name     string
        a, b     int
        expected int
    }{
        {"positive", 2, 3, 5},
        {"negative", -1, -2, -3},
        {"zero", 0, 0, 0},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            calculator := NewCalculator()
            result := calculator.Add(tt.a, tt.b)
            if result != tt.expected {
                t.Errorf("Expected %d, got %d", tt.expected, result)
            }
        })
    }
}
```

#### Mock Testing with Testify
```go
package user

import (
    "testing"
    "github.com/stretchr/testify/assert"
    "github.com/stretchr/testify/mock"
)

type MockRepository struct {
    mock.Mock
}

func (m *MockRepository) Save(user *User) error {
    args := m.Called(user)
    return args.Error(0)
}

func TestUserService_CreateUser(t *testing.T) {
    // Arrange
    mockRepo := new(MockRepository)
    service := NewUserService(mockRepo)
    user := &User{Name: "Test", Email: "test@example.com"}

    mockRepo.On("Save", user).Return(nil)

    // Act
    err := service.CreateUser(user)

    // Assert
    assert.NoError(t, err)
    mockRepo.AssertExpectations(t)
}
```

## Rust

### Built-in Testing

#### Basic Test
```rust
// src/calculator.rs
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_add() {
        let calculator = Calculator::new();
        assert_eq!(calculator.add(2, 3), 5);
    }

    #[test]
    #[should_panic(expected = "Division by zero")]
    fn test_divide_by_zero() {
        let calculator = Calculator::new();
        calculator.divide(10, 0);
    }
}
```

#### Mock Testing with Mockall
```rust
#[cfg(test)]
mod tests {
    use super::*;
    use mockall::mock;

    mock! {
        UserRepository {}

        fn save(&self, user: User) -> Result<User, Error>;
        fn find_by_id(&self, id: u32) -> Result<Option<User>, Error>;
    }

    #[test]
    fn test_create_user() {
        let mut mock_repo = MockUserRepository::new();
        let user = User { id: 1, name: "Test".to_string() };

        mock_repo
            .expect_save()
            .withf(|u| u.name == "Test")
            .return_once(|_| Ok(user.clone()));

        let service = UserService::new(Box::new(mock_repo));
        let result = service.create_user("Test").unwrap();

        assert_eq!(result.name, "Test");
    }
}
```

## Ruby

### RSpec Framework

#### Basic Test
```ruby
# spec/calculator_spec.rb
RSpec.describe Calculator do
  let(:calculator) { Calculator.new }

  describe '#add' do
    it 'returns the sum of two numbers' do
      expect(calculator.add(2, 3)).to eq(5)
    end

    it 'handles negative numbers' do
      expect(calculator.add(-1, 1)).to eq(0)
    end
  end

  context 'when dividing by zero' do
    it 'raises an error' do
      expect { calculator.divide(10, 0) }.to raise_error(ZeroDivisionError)
    end
  end
end
```

#### Mock Testing
```ruby
# spec/user_service_spec.rb
RSpec.describe UserService do
  let(:repository) { double('UserRepository') }
  let(:service) { UserService.new(repository) }

  describe '#create_user' do
    it 'saves the user to repository' do
      user_data = { name: 'John', email: 'john@example.com' }
      user = User.new(user_data)

      expect(repository).to receive(:save).with(user)

      service.create_user(user_data)
    end
  end
end
```

## Swift

### XCTest Framework

#### Basic Test
```swift
import XCTest
@testable import MyProject

class CalculatorTests: XCTestCase {
    var calculator: Calculator!

    override func setUp() {
        super.setUp()
        calculator = Calculator()
    }

    func testAdd() {
        let result = calculator.add(2, 3)
        XCTAssertEqual(result, 5)
    }

    func testPerformanceAdd() {
        measure {
            for _ in 0..<1000 {
                _ = calculator.add(2, 3)
            }
        }
    }
}
```

## Framework-Specific Patterns

### Next.js Testing
```typescript
import { render, screen } from '@testing-library/react'
import { useRouter } from 'next/router'
import HomePage from '../pages/index'

jest.mock('next/router')

describe('HomePage', () => {
  it('should display welcome message', () => {
    ;(useRouter as jest.Mock).mockReturnValue({
      pathname: '/',
      push: jest.fn()
    })

    render(<HomePage />)

    expect(screen.getByText('Welcome')).toBeInTheDocument()
  })
})
```

### Express.js Testing
```typescript
import request from 'supertest'
import app from '../app'

describe('User API', () => {
  it('should create user', async () => {
    const response = await request(app)
      .post('/api/users')
      .send({
        name: 'John Doe',
        email: 'john@example.com'
      })
      .expect(201)

    expect(response.body.name).toBe('John Doe')
  })
})
```

### Django Testing
```python
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient

class UserAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_get_user_profile(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/profile/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['username'], 'testuser')
```

### Flask Testing
```python
import pytest
from app import create_app

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_create_user(client):
    response = client.post('/users', json={
        'name': 'Test User',
        'email': 'test@example.com'
    })

    assert response.status_code == 201
    assert response.json['name'] == 'Test User'
```

## Language-Specific Best Practices

### TypeScript
- Use strict type checking
- Test with type safety
- Mock with jest.mock

### Python
- Use pytest fixtures
- Leverage parametrize for data-driven tests
- Mock with unittest.mock

### Java
- Use JUnit 5 features
- Mock with Mockito
- Test Spring components with @SpringBootTest

### C#
- Use xUnit theories for data-driven tests
- Mock with Moq
- Test ASP.NET Core with WebApplicationFactory

### Go
- Use table-driven tests
- Leverage testify for assertions and mocks
- Test interfaces for mockability

### Rust
- Use built-in testing
- Mock with mockall crate
- Test Result and Option types

### Ruby
- Use RSpec's expressive DSL
- Leverage shared examples
- Mock with rspec-mocks