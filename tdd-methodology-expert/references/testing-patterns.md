# Testing Patterns for TDD

This document provides language-agnostic testing patterns and best practices that support effective Test-Driven Development across different programming environments.

## Test Structure Patterns

### The AAA Pattern (Arrange-Act-Assert)

The most fundamental testing pattern. Every test should follow this three-part structure:

```
Arrange: Set up the test data and preconditions
Act: Execute the behavior being tested
Assert: Verify the expected outcome
```

**Example (Python)**:
```python
def test_should_add_item_to_shopping_cart():
    # Arrange
    cart = ShoppingCart()
    item = Item("Book", price=29.99)

    # Act
    cart.add_item(item)

    # Assert
    assert len(cart.items) == 1
    assert cart.items[0] == item
```

**Example (JavaScript)**:
```javascript
test('should add item to shopping cart', () => {
    // Arrange
    const cart = new ShoppingCart();
    const item = new Item("Book", 29.99);

    // Act
    cart.addItem(item);

    // Assert
    expect(cart.items).toHaveLength(1);
    expect(cart.items[0]).toBe(item);
});
```

### Given-When-Then (BDD Style)

An alternative to AAA, commonly used in Behavior-Driven Development:

```
Given: Preconditions and context
When: The action or event
Then: Expected outcomes
```

**Example (Ruby)**:
```ruby
describe 'Shopping Cart' do
  it 'adds item to cart' do
    # Given a cart and an item
    cart = ShoppingCart.new
    item = Item.new("Book", 29.99)

    # When adding the item
    cart.add_item(item)

    # Then the cart should contain the item
    expect(cart.items.length).to eq(1)
    expect(cart.items[0]).to eq(item)
  end
end
```

## Test Organization Patterns

### Test Fixture Pattern

Use setup/teardown to create consistent test preconditions:

**Example (Python with pytest)**:
```python
import pytest

@pytest.fixture
def cart():
    """Create a fresh shopping cart for each test"""
    return ShoppingCart()

@pytest.fixture
def sample_items():
    """Create sample items for testing"""
    return [
        Item("Book", 29.99),
        Item("Pen", 1.99),
        Item("Notebook", 5.99)
    ]

def test_should_calculate_correct_total(cart, sample_items):
    for item in sample_items:
        cart.add_item(item)

    total = cart.calculate_total()

    assert total == 37.97
```

**Example (JavaScript with Jest)**:
```javascript
describe('ShoppingCart', () => {
    let cart;

    beforeEach(() => {
        cart = new ShoppingCart();
    });

    test('should calculate correct total', () => {
        cart.addItem(new Item("Book", 29.99));
        cart.addItem(new Item("Pen", 1.99));

        const total = cart.calculateTotal();

        expect(total).toBe(31.98);
    });
});
```

### Test Builder Pattern

Create fluent APIs for complex test data setup:

**Example (Java)**:
```java
public class OrderBuilder {
    private Customer customer;
    private List<Item> items = new ArrayList<>();
    private PaymentMethod paymentMethod;

    public OrderBuilder withCustomer(String name, String email) {
        this.customer = new Customer(name, email);
        return this;
    }

    public OrderBuilder withItem(String name, double price) {
        this.items.add(new Item(name, price));
        return this;
    }

    public OrderBuilder withPayment(PaymentMethod method) {
        this.paymentMethod = method;
        return this;
    }

    public Order build() {
        Order order = new Order(customer);
        items.forEach(order::addItem);
        order.setPaymentMethod(paymentMethod);
        return order;
    }
}

// Usage in tests:
@Test
public void shouldProcessOrderSuccessfully() {
    Order order = new OrderBuilder()
        .withCustomer("John Doe", "john@example.com")
        .withItem("Book", 29.99)
        .withItem("Pen", 1.99)
        .withPayment(PaymentMethod.CREDIT_CARD)
        .build();

    OrderResult result = processor.process(order);

    assertEquals(OrderStatus.COMPLETED, result.getStatus());
}
```

### Object Mother Pattern

Centralized factory for creating common test objects:

**Example (Python)**:
```python
class CustomerMother:
    """Factory for creating test customers"""

    @staticmethod
    def create_standard_customer():
        return Customer(
            name="John Doe",
            email="john@example.com",
            is_active=True
        )

    @staticmethod
    def create_vip_customer():
        return Customer(
            name="Jane Smith",
            email="jane@example.com",
            is_active=True,
            membership_level="VIP"
        )

    @staticmethod
    def create_inactive_customer():
        return Customer(
            name="Bob Wilson",
            email="bob@example.com",
            is_active=False
        )

# Usage in tests:
def test_should_apply_vip_discount():
    customer = CustomerMother.create_vip_customer()
    cart = ShoppingCart(customer)

    cart.add_item(Item("Book", 100))
    total = cart.calculate_total()

    assert total == 80  # 20% VIP discount
```

## Assertion Patterns

### Single Assertion Principle

**Guideline**: Each test should verify one logical concept (though may have multiple assertion statements for clarity).

**Good**:
```python
def test_should_create_user_with_correct_attributes():
    user = create_user("john@example.com", "John Doe")

    # Multiple assertions verifying one concept: user creation
    assert user.email == "john@example.com"
    assert user.name == "John Doe"
    assert user.is_active is True
```

**Better (when concepts are truly separate)**:
```python
def test_should_create_user_with_provided_email():
    user = create_user("john@example.com", "John Doe")
    assert user.email == "john@example.com"

def test_should_create_user_with_provided_name():
    user = create_user("john@example.com", "John Doe")
    assert user.name == "John Doe"

def test_should_create_active_user_by_default():
    user = create_user("john@example.com", "John Doe")
    assert user.is_active is True
```

### Custom Assertion Methods

Create domain-specific assertions for clarity:

**Example (JavaScript)**:
```javascript
function assertValidOrder(order) {
    expect(order.customer).toBeDefined();
    expect(order.items).not.toHaveLength(0);
    expect(order.total).toBeGreaterThan(0);
    expect(order.status).toBe('pending');
}

test('should create valid order from cart', () => {
    const cart = createSampleCart();

    const order = cart.checkout();

    assertValidOrder(order);
});
```

## Test Doubles (Mocking) Patterns

### Stub Pattern

Replace dependencies with simplified implementations:

**Example (Python)**:
```python
class StubEmailService:
    """Stub that tracks calls without sending real emails"""
    def __init__(self):
        self.sent_emails = []

    def send(self, to, subject, body):
        self.sent_emails.append({
            'to': to,
            'subject': subject,
            'body': body
        })

def test_should_send_welcome_email_on_registration():
    email_service = StubEmailService()
    user_service = UserService(email_service)

    user = user_service.register("john@example.com", "password")

    assert len(email_service.sent_emails) == 1
    assert email_service.sent_emails[0]['to'] == "john@example.com"
    assert "Welcome" in email_service.sent_emails[0]['subject']
```

### Mock Pattern

Verify interactions with dependencies:

**Example (JavaScript with Jest)**:
```javascript
test('should call payment gateway with correct amount', () => {
    const mockGateway = {
        charge: jest.fn().mockResolvedValue({ success: true })
    };
    const processor = new PaymentProcessor(mockGateway);

    processor.processPayment(customer, 100.00);

    expect(mockGateway.charge).toHaveBeenCalledWith(
        customer.paymentToken,
        100.00
    );
});
```

### Fake Pattern

Provide working implementations with shortcuts:

**Example (Python)**:
```python
class FakeUserRepository:
    """In-memory repository for testing"""
    def __init__(self):
        self.users = {}
        self.next_id = 1

    def save(self, user):
        if not user.id:
            user.id = self.next_id
            self.next_id += 1
        self.users[user.id] = user
        return user

    def find_by_id(self, user_id):
        return self.users.get(user_id)

def test_should_persist_user_with_generated_id():
    repo = FakeUserRepository()
    user = User(name="John")

    saved_user = repo.save(user)

    assert saved_user.id is not None
    assert repo.find_by_id(saved_user.id) == saved_user
```

## Parameterized Testing Pattern

Test multiple cases with the same structure:

**Example (Python with pytest)**:
```python
import pytest

@pytest.mark.parametrize("input,expected", [
    (0, 0),
    (1, 1),
    (2, 2),
    (3, 6),
    (4, 24),
    (5, 120),
])
def test_factorial_calculation(input, expected):
    result = factorial(input)
    assert result == expected
```

**Example (JavaScript with Jest)**:
```javascript
test.each([
    [0, 0],
    [1, 1],
    [2, 2],
    [3, 6],
    [4, 24],
    [5, 120],
])('factorial(%i) should equal %i', (input, expected) => {
    const result = factorial(input);
    expect(result).toBe(expected);
});
```

## Exception Testing Pattern

Test error conditions explicitly:

**Example (Python)**:
```python
def test_should_raise_error_when_withdrawing_too_much():
    account = Account(balance=100)

    with pytest.raises(InsufficientFundsError) as exc_info:
        account.withdraw(150)

    assert "Insufficient funds" in str(exc_info.value)
    assert exc_info.value.available == 100
    assert exc_info.value.requested == 150
```

**Example (JavaScript)**:
```javascript
test('should throw error when withdrawing too much', () => {
    const account = new Account(100);

    expect(() => {
        account.withdraw(150);
    }).toThrow(InsufficientFundsError);

    expect(() => {
        account.withdraw(150);
    }).toThrow('Insufficient funds');
});
```

## Property-Based Testing Pattern

Test properties that should always hold:

**Example (Python with hypothesis)**:
```python
from hypothesis import given
import hypothesis.strategies as st

@given(st.lists(st.integers()))
def test_reversing_twice_gives_original(lst):
    result = reverse(reverse(lst))
    assert result == lst

@given(st.integers(min_value=0))
def test_factorial_is_positive(n):
    result = factorial(n)
    assert result > 0
```

## State-Based vs. Interaction-Based Testing

### State-Based Testing (Preferred)

Verify final state rather than how it was achieved:

**Example**:
```python
def test_should_remove_item_from_cart():
    cart = ShoppingCart()
    item = Item("Book", 29.99)
    cart.add_item(item)

    cart.remove_item(item)

    assert len(cart.items) == 0  # Verify state
```

### Interaction-Based Testing

Verify interactions when state is not observable:

**Example**:
```python
def test_should_log_failed_login_attempt():
    logger = Mock()
    auth = AuthService(logger)

    auth.login("user", "wrong_password")

    logger.warning.assert_called_once_with(
        "Failed login attempt for user: user"
    )
```

## Test Naming Patterns

### Should-Style Naming

```
test_should_<expected_behavior>_when_<condition>
```

**Examples**:
- `test_should_return_empty_list_when_no_matches_found`
- `test_should_throw_exception_when_amount_is_negative`
- `test_should_apply_discount_when_quantity_exceeds_ten`

### Behavior-Style Naming

```
test_<subject>_<scenario>_<expected_result>
```

**Examples**:
- `test_cart_with_multiple_items_calculates_correct_total`
- `test_user_registration_with_invalid_email_fails`
- `test_payment_processing_with_insufficient_funds_raises_error`

## Test Data Patterns

### Obvious Data

Use self-documenting test data:

**Bad**:
```python
def test_calculation():
    result = calculate(10, 5, 3)
    assert result == 8
```

**Good**:
```python
def test_should_calculate_average_correctly():
    value1 = 10
    value2 = 20
    value3 = 30
    expected_average = 20

    result = calculate_average([value1, value2, value3])

    assert result == expected_average
```

### Boundary Value Testing

Test edges of valid ranges:

```python
def test_age_validation():
    validator = AgeValidator(min_age=18, max_age=100)

    # Below minimum
    assert not validator.is_valid(17)

    # At minimum boundary
    assert validator.is_valid(18)

    # Normal value
    assert validator.is_valid(50)

    # At maximum boundary
    assert validator.is_valid(100)

    # Above maximum
    assert not validator.is_valid(101)
```

## TDD-Specific Patterns

### Triangulation

Build generality through multiple test cases:

**Step 1 - Specific case**:
```python
def test_should_add_two_numbers():
    assert add(2, 3) == 5

# Implementation:
def add(a, b):
    return 5  # Hardcoded - simplest thing that works
```

**Step 2 - Add another case to force generalization**:
```python
def test_should_add_two_numbers():
    assert add(2, 3) == 5

def test_should_add_different_numbers():
    assert add(4, 7) == 11

# Implementation:
def add(a, b):
    return a + b  # Now forced to generalize
```

### Fake It Till You Make It

Start with simple/hardcoded implementations:

```python
# Test
def test_should_return_greeting():
    assert greet("World") == "Hello, World!"

# First implementation (fake it)
def greet(name):
    return "Hello, World!"

# Add another test to force real implementation
def test_should_return_greeting_with_different_name():
    assert greet("Alice") == "Hello, Alice!"

# Real implementation
def greet(name):
    return f"Hello, {name}!"
```

### Obvious Implementation

When the implementation is obvious, just write it:

```python
# Test
def test_should_calculate_rectangle_area():
    assert calculate_area(width=5, height=3) == 15

# Implementation (obvious, no need to fake)
def calculate_area(width, height):
    return width * height
```

## Summary: Testing Pattern Selection

- **Use AAA** for clarity in most tests
- **Use fixtures** to eliminate setup duplication
- **Use builders** for complex object creation
- **Use test doubles** when dependencies are expensive or unpredictable
- **Prefer state-based** testing over interaction-based
- **Use parameterized tests** for multiple similar cases
- **Test boundaries** explicitly
- **Name tests** to describe behavior
- **Keep tests independent** of each other
- **Make tests readable** - they're documentation

Remember: Tests are first-class citizens in TDD. Treat them with the same care as production code.
