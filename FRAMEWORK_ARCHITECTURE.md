# Framework & Architecture Documentation

## 🎯 Frameworks & Technologies Used

### **Core Testing Frameworks**

1. **Playwright** (Browser Automation)
   - Version: Latest
   - Purpose: Cross-browser automation for web testing
   - Features: Auto-wait, network interception, video recording
   - Why: Modern, fast, reliable browser automation with built-in waiting mechanisms

2. **Pytest** (Test Runner)
   - Version: 7.4.3+
   - Purpose: Test execution, fixtures, parametrization
   - Features: Powerful fixtures, parallel execution, rich plugins
   - Why: Industry standard Python testing framework with excellent plugin ecosystem

3. **pytest-playwright** (Integration Plugin)
   - Purpose: Bridges Pytest and Playwright
   - Features: Browser fixtures, automatic cleanup, context management
   - Why: Seamless integration between Pytest and Playwright

### **Reporting & Logging**

4. **Custom HTML Report Plugin** (pytest_html_report_plugin.py)
   - Purpose: Generate comprehensive HTML test reports
   - Features: Module coverage, page object documentation, failure screenshots
   - Why: Custom-built for detailed boutiqaat.com test reporting

5. **Custom Logging Plugin** (pytest_logging_plugin.py)
   - Purpose: Enhanced test execution logging
   - Features: Timestamped logs, test duration tracking, error capture
   - Why: Detailed debugging and audit trail

6. **Python Logging Module** (utils/logger.py)
   - Purpose: Structured logging with multiple levels
   - Features: File + console output, colored logs, error tracking
   - Why: Professional logging for production-grade test automation

### **HTTP & API Testing**

7. **Requests Library**
   - Purpose: REST API calls (user registration)
   - Features: Simple HTTP client, session management
   - Why: Faster registration via API instead of UI

### **Additional Libraries**

8. **python-dotenv**
   - Purpose: Environment variable management
   - Features: Load secrets from .env files
   - Why: Secure credential management

9. **pytest-html**
   - Purpose: Fallback HTML reporting
   - Features: Basic HTML reports
   - Why: Backup reporting option

10. **pytest-json-report**
    - Purpose: JSON format test results
    - Features: Machine-readable test output
    - Why: Integration with CI/CD pipelines

---

## 🏗️ Architecture Pattern

### **Page Object Model (POM)**

**What is POM?**
- Design pattern that creates object repository for web UI elements
- Each web page is represented as a class
- Page elements and actions are methods in the class

**Why POM?**
- ✅ Reduces code duplication
- ✅ Easy maintenance (change in one place)
- ✅ Improved readability
- ✅ Reusable components

**Our Implementation:**
```
pages/
├── base_page.py         # Parent class with common methods
├── login_page.py        # Login page actions
├── registration_page.py # Registration actions
├── search_page.py       # Search functionality
├── cart_page.py         # Cart operations
├── address_page.py      # Address management
├── payment_page.py      # Payment gateway
├── wishlist_page.py     # Wishlist operations
└── navigation_page.py   # Navigation verification
```

---

## 📂 Project Structure Explained

```
boutiqaat-automation/
│
├── config/                      # Configuration files
│   ├── __init__.py             # Makes config a Python package
│   └── settings.py             # Base URL, timeouts, paths (single source of truth)
│
├── data/                        # Test data (separated from test logic)
│   ├── __init__.py             # Makes data a Python package
│   └── test_data.py            # All test datasets (registration, login, address)
│
├── pages/                       # Page Object Model (POM) classes
│   ├── __init__.py             # Makes pages a Python package
│   ├── base_page.py            # Parent class with shared methods
│   ├── login_page.py           # Login page interactions
│   ├── registration_page.py    # User registration (API + UI)
│   ├── search_page.py          # Product search and selection
│   ├── cart_page.py            # Shopping cart operations
│   ├── address_page.py         # Delivery address CRUD
│   ├── payment_page.py         # Payment gateway interactions
│   ├── wishlist_page.py        # Wishlist add/remove
│   └── navigation_page.py      # Category page verification
│
├── tests/                       # Test suites (actual test cases)
│   ├── __init__.py             # Makes tests a Python package
│   ├── test_e2e_flow.py        # End-to-end purchase flow
│   ├── test_registration.py    # User registration tests
│   ├── test_cart.py            # Cart functionality tests
│   ├── test_wishlist.py        # Wishlist tests
│   ├── test_address.py         # Address management tests
│   ├── test_navigation.py      # Navigation/category tests
│   └── test_markers.py         # Pytest marker definitions
│
├── utils/                       # Utility functions
│   ├── __init__.py             # Makes utils a Python package
│   └── logger.py               # Enhanced logging system
│
├── logs/                        # Test execution logs (auto-generated)
│   ├── latest.log              # Symlink to most recent log
│   └── test_run_*.log          # Timestamped log files
│
├── reports/                     # HTML test reports (auto-generated)
│   ├── latest_report.html      # Most recent report
│   └── report_*.html           # Timestamped reports
│
├── screenshots/                 # Failure screenshots (auto-generated)
│   └── fail_*.png              # Screenshots on test failure
│
├── videos/                      # Test execution videos (auto-generated)
│   └── *.webm                  # Video recordings of tests
│
├── conftest.py                  # Pytest configuration (fixtures, hooks)
├── pytest.ini                   # Pytest settings (markers, options)
├── pytest_html_report_plugin.py # Custom HTML report generator
├── pytest_logging_plugin.py     # Custom logging plugin
├── requirements.txt             # Python dependencies
├── .gitignore                   # Git exclusions
│
└── Documentation/
    ├── README.md                # Main project documentation
    ├── LOGGING_GUIDE.md         # Logging system guide
    ├── DEBUG_REFERENCE.md       # Debugging tips
    ├── FIXES_APPLIED.md         # Bug fixes history
    ├── GITHUB_PUSH_GUIDE.md     # GitHub instructions
    ├── OPTIMIZATION_SUMMARY.md  # Optimization details
    └── FRAMEWORK_ARCHITECTURE.md # This file
```

---

## 🔄 Test Execution Flow

```
1. pytest starts
   ↓
2. conftest.py loads (fixtures, hooks)
   ↓
3. pytest_logging_plugin.py initializes (logging)
   ↓
4. pytest_html_report_plugin.py initializes (reporting)
   ↓
5. Test collection (discovers all test_*.py files)
   ↓
6. For each test:
   a. Setup fixtures (browser, page)
   b. Execute test steps
   c. Capture logs
   d. On failure: screenshot + video
   e. Teardown fixtures
   ↓
7. Generate HTML report
   ↓
8. Save logs
   ↓
9. Exit with status code
```

---

## 🎨 Design Principles

### **1. DRY (Don't Repeat Yourself)**
- Common actions in BasePage
- Reusable page objects
- Shared fixtures in conftest.py

### **2. Single Responsibility**
- Each page class handles one page
- Each test file tests one feature
- Each function does one thing

### **3. Separation of Concerns**
- Test logic ≠ Test data
- Page objects ≠ Test cases
- Configuration ≠ Implementation

### **4. Maintainability**
- Clear naming conventions
- Comprehensive comments
- Modular structure

### **5. Scalability**
- Easy to add new tests
- Easy to add new pages
- Easy to add new data

---

## 🔧 Key Features

### **1. Auto-Retry Mechanism**
- Registration retries up to 3 times
- Login retries on rate limiting
- Handles transient failures

### **2. Smart Waiting**
- Playwright auto-wait (no explicit sleeps needed)
- Custom waits for dynamic content
- Network idle detection

### **3. Failure Handling**
- Automatic screenshot on failure
- Video recording of entire test
- Detailed error logs with stack traces

### **4. Data-Driven Testing**
- Parametrized tests
- External test data files
- Easy to add new scenarios

### **5. Comprehensive Reporting**
- HTML report with module coverage
- Page object documentation
- Embedded screenshots
- Duration tracking
- Pass/fail statistics

---

## 📊 Test Coverage

### **Functional Areas Covered**

1. **User Management**
   - Registration (API + UI)
   - Login/Logout
   - Session management

2. **Product Discovery**
   - Search functionality
   - Category navigation
   - Product detail pages

3. **Shopping Cart**
   - Add to cart
   - Remove from cart
   - Cart persistence

4. **Wishlist**
   - Add to wishlist
   - Wishlist persistence

5. **Checkout Flow**
   - Address management (CRUD)
   - Payment method selection
   - Order placement

6. **Payment Gateway**
   - KNET integration
   - Payment success flow
   - Payment cancellation flow

7. **Navigation**
   - Homepage
   - Category pages
   - Brand pages
   - Search results

---

## 🚀 Running Tests

### **Run All Tests**
```bash
pytest tests/ -v
```

### **Run Specific Module**
```bash
pytest tests/test_e2e_flow.py -v
```

### **Run by Marker**
```bash
pytest -m regression -v
pytest -m cart -v
```

### **Generate Report**
```bash
pytest tests/
open reports/latest_report.html
```

### **View Logs**
```bash
cat logs/latest.log
```

---

## 🎯 Best Practices Implemented

1. ✅ **Page Object Model** - Maintainable and reusable
2. ✅ **Data-Driven Testing** - Scalable test scenarios
3. ✅ **Fixtures** - Clean setup/teardown
4. ✅ **Parametrization** - Multiple scenarios, one test
5. ✅ **Explicit Waits** - Reliable synchronization
6. ✅ **Error Handling** - Graceful failure management
7. ✅ **Logging** - Comprehensive audit trail
8. ✅ **Reporting** - Detailed test results
9. ✅ **Version Control** - Git with proper .gitignore
10. ✅ **Documentation** - Clear and comprehensive

---

## 📚 Learning Resources

### **Playwright**
- Official Docs: https://playwright.dev/python/
- API Reference: https://playwright.dev/python/docs/api/class-playwright

### **Pytest**
- Official Docs: https://docs.pytest.org/
- Fixtures: https://docs.pytest.org/en/stable/fixture.html

### **Page Object Model**
- Martin Fowler: https://martinfowler.com/bliki/PageObject.html
- Selenium Guide: https://www.selenium.dev/documentation/test_practices/encouraged/page_object_models/

---

## 🤝 Contributing

When adding new tests:
1. Create page object if needed (pages/)
2. Add test data (data/test_data.py)
3. Write test (tests/test_*.py)
4. Add marker if needed (pytest.ini)
5. Update documentation

---

**Framework Version:** 1.0  
**Last Updated:** April 2026  
**Maintained By:** Boutiqaat QA Team
