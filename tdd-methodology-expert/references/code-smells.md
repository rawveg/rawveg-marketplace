# Code Smells That Indicate Test-After Development

This document catalogs code smells and anti-patterns that strongly suggest tests were written after implementation rather than following TDD methodology.

## Understanding Code Smells in TDD Context

When developers write tests after code (test-after), they tend to produce different code structures than when following TDD. This is because:

1. **TDD enforces small steps**: Each test drives minimal implementation
2. **TDD encourages refactoring**: The refactor phase continuously improves structure
3. **TDD requires testability**: Code must be designed for easy testing from the start
4. **TDD prevents over-engineering**: Only write code needed to pass tests

Test-after code often shows signs of:
- Solving problems that don't exist yet (premature optimization)
- Complex structures built all at once (big bang implementation)
- Difficult-to-test designs (retrofitted testability)
- Accumulated technical debt (skipped refactoring)

## High-Severity Code Smells

### 1. Deeply Nested Conditionals

**Description**: Multiple levels of if/elif/else statements nested within each other.

**Why it indicates test-after**:
- TDD would break this down into separate, testable functions
- Each branch would have its own test, encouraging extraction
- Refactor phase would identify and eliminate deep nesting

**Example (Bad)**:
```python
def process_order(order):
    if order.customer:
        if order.customer.is_active:
            if order.items:
                if order.total > 0:
                    if order.payment_method:
                        if order.payment_method == "credit_card":
                            if order.customer.credit_limit >= order.total:
                                # Process credit card payment
                                return "processed"
                            else:
                                return "insufficient_credit"
                        else:
                            # Process other payment
                            return "processed"
                    else:
                        return "no_payment_method"
                else:
                    return "invalid_total"
            else:
                return "no_items"
        else:
            return "inactive_customer"
    else:
        return "no_customer"
```

**TDD Alternative**:
```python
def process_order(order):
    _validate_order(order)
    _validate_customer(order.customer)
    _validate_payment(order)
    return _execute_payment(order)

def _validate_order(order):
    if not order.items:
        raise OrderValidationError("Order must have items")
    if order.total <= 0:
        raise OrderValidationError("Order total must be positive")

def _validate_customer(customer):
    if not customer:
        raise OrderValidationError("Order must have a customer")
    if not customer.is_active:
        raise OrderValidationError("Customer is inactive")

def _validate_payment(order):
    if not order.payment_method:
        raise OrderValidationError("Payment method required")

def _execute_payment(order):
    payment_processor = PaymentProcessorFactory.create(order.payment_method)
    return payment_processor.process(order)
```

**How to detect**: Look for 3+ levels of nested if/else statements.

### 2. Long Methods/Functions

**Description**: Methods exceeding 20-30 lines of code.

**Why it indicates test-after**:
- TDD naturally produces small functions (5-15 lines)
- Each test typically drives one small piece of functionality
- Long methods suggest big-bang implementation

**Example (Bad)**:
```python
def generate_invoice(order_id):
    # 80+ lines of mixed responsibilities:
    # - Database queries
    # - Business logic
    # - Calculations
    # - Formatting
    # - File generation
    # - Email sending
    order = db.query(Order).filter_by(id=order_id).first()
    if not order:
        return None

    total = 0
    for item in order.items:
        if item.discount:
            price = item.price * (1 - item.discount)
        else:
            price = item.price
        total += price * item.quantity

    tax = total * 0.1
    shipping = 10 if total < 50 else 0
    grand_total = total + tax + shipping

    # ... 50 more lines of formatting and sending
```

**TDD Alternative**:
```python
def generate_invoice(order_id):
    order = _fetch_order(order_id)
    invoice_data = _calculate_invoice_totals(order)
    formatted_invoice = _format_invoice(order, invoice_data)
    _send_invoice(order.customer.email, formatted_invoice)
    return formatted_invoice

def _fetch_order(order_id):
    order = db.query(Order).filter_by(id=order_id).first()
    if not order:
        raise OrderNotFoundError(f"Order {order_id} not found")
    return order

def _calculate_invoice_totals(order):
    subtotal = sum(_calculate_line_total(item) for item in order.items)
    tax = _calculate_tax(subtotal)
    shipping = _calculate_shipping(subtotal)
    return InvoiceTotals(subtotal, tax, shipping)

def _calculate_line_total(item):
    price = item.price * (1 - item.discount) if item.discount else item.price
    return price * item.quantity
```

**How to detect**: Count lines in methods. Flag anything over 20 lines.

### 3. Complex Boolean Conditions

**Description**: Conditional expressions with multiple AND/OR operators.

**Why it indicates test-after**:
- TDD encourages extracting complex conditions into named methods
- Each condition part would have its own test
- Refactor phase would identify complexity and extract it

**Example (Bad)**:
```python
if (user.age >= 18 and user.has_license and
    user.years_experience >= 2 and
    (user.state == "CA" or user.state == "NY") and
    not user.has_violations and user.insurance_valid):
    # Allow to rent car
    pass
```

**TDD Alternative**:
```python
def can_rent_car(user):
    return (is_eligible_driver(user) and
            is_in_service_area(user) and
            has_clean_record(user))

def is_eligible_driver(user):
    return user.age >= 18 and user.has_license and user.years_experience >= 2

def is_in_service_area(user):
    return user.state in ["CA", "NY"]

def has_clean_record(user):
    return not user.has_violations and user.insurance_valid
```

**How to detect**: Count AND/OR operators. Flag conditions with 3+ logical operators.

### 4. God Objects/Classes

**Description**: Classes with too many responsibilities and methods.

**Why it indicates test-after**:
- TDD enforces Single Responsibility Principle through testing
- Each test focuses on one behavior, encouraging focused classes
- Testing god objects is painful, encouraging decomposition

**Example (Bad)**:
```python
class UserManager:
    def authenticate(self, username, password): pass
    def create_user(self, user_data): pass
    def update_user(self, user_id, data): pass
    def delete_user(self, user_id): pass
    def send_welcome_email(self, user): pass
    def send_password_reset(self, user): pass
    def validate_email(self, email): pass
    def validate_password(self, password): pass
    def log_user_activity(self, user, action): pass
    def generate_report(self, user_id): pass
    def export_user_data(self, user_id): pass
    def import_users(self, file_path): pass
    # ... 20 more methods
```

**TDD Alternative**:
```python
class AuthenticationService:
    def authenticate(self, username, password): pass

class UserRepository:
    def create(self, user): pass
    def update(self, user_id, data): pass
    def delete(self, user_id): pass
    def find_by_id(self, user_id): pass

class EmailService:
    def send_welcome_email(self, user): pass
    def send_password_reset(self, user): pass

class UserValidator:
    def validate_email(self, email): pass
    def validate_password(self, password): pass

class UserReportGenerator:
    def generate_report(self, user_id): pass
```

**How to detect**: Count methods in class. Flag classes with 10+ methods.

## Medium-Severity Code Smells

### 5. Type Checking Instead of Polymorphism

**Description**: Using `isinstance()`, `typeof`, or type switches instead of polymorphic design.

**Why it indicates test-after**:
- TDD encourages interface-based design through mocking
- Polymorphism emerges naturally when testing behaviors
- Type checking makes testing harder, encouraging better design

**Example (Bad)**:
```python
def calculate_area(shape):
    if isinstance(shape, Circle):
        return 3.14159 * shape.radius ** 2
    elif isinstance(shape, Rectangle):
        return shape.width * shape.height
    elif isinstance(shape, Triangle):
        return 0.5 * shape.base * shape.height
    else:
        raise ValueError("Unknown shape type")
```

**TDD Alternative**:
```python
class Shape(ABC):
    @abstractmethod
    def calculate_area(self):
        pass

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def calculate_area(self):
        return 3.14159 * self.radius ** 2

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def calculate_area(self):
        return self.width * self.height

# Usage:
def process_shape(shape: Shape):
    return shape.calculate_area()
```

**How to detect**: Search for `isinstance()`, `typeof`, or type switch patterns.

### 6. Duplicate Code Blocks

**Description**: Same or similar code repeated in multiple places.

**Why it indicates test-after**:
- TDD's refactor phase explicitly targets duplication
- Each cycle includes time to eliminate redundancy
- Test-after often skips refactoring altogether

**Example (Bad)**:
```python
def calculate_discount_price_for_books(price, quantity):
    if quantity >= 10:
        discount = 0.2
    elif quantity >= 5:
        discount = 0.1
    else:
        discount = 0
    return price * (1 - discount)

def calculate_discount_price_for_electronics(price, quantity):
    if quantity >= 10:
        discount = 0.15
    elif quantity >= 5:
        discount = 0.08
    else:
        discount = 0
    return price * (1 - discount)
```

**TDD Alternative**:
```python
def calculate_discount_price(price, quantity, discount_tiers):
    discount = _get_discount_for_quantity(quantity, discount_tiers)
    return price * (1 - discount)

def _get_discount_for_quantity(quantity, tiers):
    for min_qty, discount in sorted(tiers.items(), reverse=True):
        if quantity >= min_qty:
            return discount
    return 0

# Usage:
BOOK_DISCOUNTS = {10: 0.2, 5: 0.1}
ELECTRONICS_DISCOUNTS = {10: 0.15, 5: 0.08}

book_price = calculate_discount_price(29.99, 12, BOOK_DISCOUNTS)
```

**How to detect**: Use code duplication analysis tools (>6 lines duplicated).

### 7. Primitive Obsession

**Description**: Using primitive types instead of small objects to represent concepts.

**Why it indicates test-after**:
- TDD encourages creating types that make tests clearer
- Value objects emerge naturally when expressing test intent
- Primitives make tests verbose and unclear

**Example (Bad)**:
```python
def create_appointment(patient_id, doctor_id, date_str, time_str, duration_mins):
    # Working with primitives throughout
    date = datetime.strptime(date_str, "%Y-%m-%d")
    time = datetime.strptime(time_str, "%H:%M")
    # ... complex validation and manipulation
```

**TDD Alternative**:
```python
@dataclass
class AppointmentTime:
    date: datetime.date
    time: datetime.time
    duration: timedelta

    def __post_init__(self):
        if self.duration <= timedelta(0):
            raise ValueError("Duration must be positive")

    def end_time(self):
        start = datetime.combine(self.date, self.time)
        return start + self.duration

def create_appointment(patient_id, doctor_id, appointment_time: AppointmentTime):
    # Working with rich domain objects
    pass
```

**How to detect**: Look for functions with many primitive parameters (4+).

### 8. Comments Explaining What Code Does

**Description**: Comments that explain the mechanics of the code rather than the "why".

**Why it indicates test-after**:
- TDD produces self-documenting code through clear naming
- Tests serve as documentation for behavior
- Need for "what" comments suggests unclear code

**Example (Bad)**:
```python
def process(data):
    # Loop through each item in data
    for item in data:
        # Check if item value is greater than 100
        if item.value > 100:
            # Multiply value by 1.5
            item.value = item.value * 1.5
        # Check if item is active
        if item.is_active:
            # Add item to results list
            results.append(item)
```

**TDD Alternative**:
```python
def process_high_value_active_items(items):
    return [apply_premium_pricing(item)
            for item in items
            if is_premium_eligible(item)]

def is_premium_eligible(item):
    return item.value > 100 and item.is_active

def apply_premium_pricing(item):
    item.value *= PREMIUM_MULTIPLIER
    return item
```

**How to detect**: Look for comments explaining mechanics; good comments explain "why".

## Low-Severity Code Smells

### 9. Magic Numbers

**Description**: Unexplained numeric literals scattered throughout code.

**Example (Bad)**:
```python
def calculate_shipping(weight):
    if weight < 5:
        return 10
    elif weight < 20:
        return 25
    else:
        return 50
```

**TDD Alternative**:
```python
LIGHT_PACKAGE_THRESHOLD = 5
MEDIUM_PACKAGE_THRESHOLD = 20
LIGHT_PACKAGE_RATE = 10
MEDIUM_PACKAGE_RATE = 25
HEAVY_PACKAGE_RATE = 50

def calculate_shipping(weight):
    if weight < LIGHT_PACKAGE_THRESHOLD:
        return LIGHT_PACKAGE_RATE
    elif weight < MEDIUM_PACKAGE_THRESHOLD:
        return MEDIUM_PACKAGE_RATE
    else:
        return HEAVY_PACKAGE_RATE
```

### 10. Long Parameter Lists

**Description**: Methods accepting many parameters (4+).

**Example (Bad)**:
```python
def create_user(first_name, last_name, email, phone, address, city, state, zip, country):
    pass
```

**TDD Alternative**:
```python
@dataclass
class UserProfile:
    first_name: str
    last_name: str
    email: str
    phone: str

@dataclass
class Address:
    street: str
    city: str
    state: str
    zip: str
    country: str

def create_user(profile: UserProfile, address: Address):
    pass
```

## Detection Strategy

### Automated Checks

Run these checks regularly to identify test-after patterns:

1. **Cyclomatic Complexity**: Flag methods with complexity > 10
2. **Method Length**: Flag methods > 20 lines
3. **Class Size**: Flag classes with > 10 methods
4. **Nesting Depth**: Flag code with > 3 levels of nesting
5. **Duplication**: Flag blocks of > 6 duplicated lines
6. **Parameter Count**: Flag methods with > 4 parameters

### Manual Review

Look for these patterns during code review:

1. Large commits with code and tests together
2. Tests that test implementation rather than behavior
3. Absence of refactoring commits
4. Complex code without corresponding complex tests
5. Tests that mock internal methods

## Refactoring from Test-After to TDD

If you inherit test-after code:

1. **Add characterization tests**: Cover existing behavior
2. **Identify smells**: Use automated and manual detection
3. **Extract methods**: Break down large methods
4. **Introduce types**: Replace primitives with value objects
5. **Apply patterns**: Use polymorphism, strategy, etc.
6. **Write tests first for new features**: Start TDD from now

Remember: The goal isn't perfect code, but continuously improving code quality through TDD discipline.
