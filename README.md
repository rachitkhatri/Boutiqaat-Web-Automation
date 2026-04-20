# 🧪 Boutiqaat Automation Framework

**Execute the complete suite - Run the Below Command**
python3 -m pytest tests/ -v --log-cli-level=DEBUG

**Stop the execution**
Ususally we use the cntrl C but if he does not work use this command - pkill -f pytest

**Comprehensive E2E test automation framework for boutiqaat.com**

[![Framework](https://img.shields.io/badge/Framework-Playwright-45ba4b?style=flat-square)](https://playwright.dev/)
[![Test Runner](https://img.shields.io/badge/Test%20Runner-Pytest-0A9EDC?style=flat-square)](https://pytest.org/)
[![Language](https://img.shields.io/badge/Language-Python%203.9+-3776AB?style=flat-square&logo=python)](https://python.org/)
[![Pattern](https://img.shields.io/badge/Pattern-Page%20Object%20Model-orange?style=flat-square)](https://martinfowler.com/bliki/PageObject.html)

---

## 📋 Table of Contents

- [Frameworks & Technologies](#-frameworks--technologies)
- [Project Structure](#-project-structure)
- [Setup Instructions](#-setup-instructions)
- [Running Tests](#-running-tests)
- [Test Coverage](#-test-coverage)
- [Reporting](#-reporting)
- [Logging System](#-logging-system)
- [Adding New Tests](#-adding-new-tests)
- [Troubleshooting](#-troubleshooting)

---

## 🎯 Frameworks & Technologies

### **Core Frameworks**

| Framework | Version | Purpose | Why We Use It |
|-----------|---------|---------|---------------|
| **Playwright** | Latest | Browser automation | Modern, fast, reliable with auto-wait mechanisms |
| **Pytest** | 7.4.3+ | Test runner | Industry standard with powerful fixtures and plugins |
| **pytest-playwright** | Latest | Integration | Seamless Pytest + Playwright integration |

### **Additional Libraries**

| Library | Purpose |
|---------|---------|
| **Requests** | REST API calls (user registration) |
| **python-dotenv** | Environment variable management |
| **pytest-html** | HTML report generation |
| **pytest-json-report** | JSON format test results |

### **Architecture Pattern**

**Page Object Model (POM)**
- Each web page = One Python class
- Page elements and actions = Class methods
- Benefits: Maintainable, reusable, readable

---

## 📂 Project Structure

```
boutiqaat-automation/
│
├── config/                      # ⚙️ Configuration
│   ├── __init__.py             # Makes config a Python package
│   └── settings.py             # Base URL, timeouts, paths (single source of truth)
│
├── data/                        # 📊 Test Data
│   ├── __init__.py             # Makes data a Python package
│   └── test_data.py            # All test datasets (registration, login, address)
│
├── pages/                       # 📄 Page Object Model (POM)
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
├── tests/                       # 🧪 Test Suites
│   ├── __init__.py             # Makes tests a Python package
│   ├── test_e2e_flow.py        # End-to-end purchase flow (2 tests)
│   ├── test_registration.py    # User registration tests (1 test)
│   ├── test_cart.py            # Cart functionality tests (1 test)
│   ├── test_wishlist.py        # Wishlist tests (1 test)
│   ├── test_address.py         # Address management tests (3 tests)
│   ├── test_navigation.py      # Navigation/category tests (8 tests)
│   └── test_markers.py         # Pytest marker definitions
│
├── utils/                       # 🛠️ Utilities
│   ├── __init__.py             # Makes utils a Python package
│   └── logger.py               # Enhanced logging system
│
├── logs/                        # 📝 Test Logs (auto-generated)
│   ├── latest.log              # Symlink to most recent log
│   └── test_run_*.log          # Timestamped log files
│
├── reports/                     # 📊 HTML Reports (auto-generated)
│   ├── latest_report.html      # Most recent report
│   └── report_*.html           # Timestamped reports
│
├── screenshots/                 # 📸 Failure Screenshots (auto-generated)
│   └── fail_*.png              # Screenshots on test failure
│
├── videos/                      # 🎥 Test Videos (auto-generated)
│   └── *.webm                  # Video recordings of tests
│
├── conftest.py                  # Pytest configuration (fixtures, hooks)
├── pytest.ini                   # Pytest settings (markers, options)
├── pytest_html_report_plugin.py # Custom HTML report generator
├── pytest_logging_plugin.py     # Custom logging plugin
├── requirements.txt             # Python dependencies
├── .gitignore                   # Git exclusions
│
└── 📚 Documentation
    ├── README.md                # This file
    ├── FRAMEWORK_ARCHITECTURE.md # Detailed framework documentation
    ├── LOGGING_GUIDE.md         # Logging system guide
    ├── DEBUG_REFERENCE.md       # Debugging tips
    ├── FIXES_APPLIED.md         # Bug fixes history
    ├── GITHUB_PUSH_GUIDE.md     # GitHub instructions
    └── OPTIMIZATION_SUMMARY.md  # Optimization details
```

---

## 🚀 Setup Instructions

### **Prerequisites**

- Python 3.9 or higher
- pip (Python package manager)
- Git (for version control)

### **Step 1: Clone Repository**

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/boutiqaat-automation.git

# Navigate to project directory
cd boutiqaat-automation
```

### **Step 2: Install Python Dependencies**

```bash
# Install all required Python packages
pip install -r requirements.txt
```

**What gets installed:**
- `playwright` - Browser automation framework
- `pytest` - Test runner
- `pytest-playwright` - Pytest + Playwright integration
- `pytest-html` - HTML report generation
- `pytest-json-report` - JSON report generation
- `requests` - HTTP library for API calls
- `python-dotenv` - Environment variable management

### **Step 3: Install Playwright Browsers**

```bash
# Install Chromium browser (only needed once)
playwright install chromium

# Optional: Install all browsers (Chromium, Firefox, WebKit)
playwright install
```

### **Step 4: Configure Test Data**

Open `data/test_data.py` and update test credentials:

```python
# Example: Update email addresses with your test accounts
E2E_DATA = [
    {
        "email": "your_test_email@example.com",  # ← Replace with your email
        "password": "YourPassword123",            # ← Replace with your password
        # ... rest of the configuration
    }
]
```

**Note:** The framework uses timestamp-based email generation by default, so you don't need real emails for most tests.

### **Step 5: Verify Installation**

```bash
# Verify pytest is installed
pytest --version

# Verify Playwright is installed
playwright --version

# Collect tests (should show 16 tests)
pytest --co -q
```

---

## 🧪 Running Tests

### **Run All Tests**

```bash
# Run the complete test suite (16 tests)
pytest tests/ -v
```

### **Run Specific Test Module**

```bash
# Run only E2E flow tests
pytest tests/test_e2e_flow.py -v

# Run only registration tests
pytest tests/test_registration.py -v

# Run only cart tests
pytest tests/test_cart.py -v

# Run only address tests
pytest tests/test_address.py -v

# Run only navigation tests
pytest tests/test_navigation.py -v
```

### **Run by Marker (Test Category)**

```bash
# Run only regression tests
pytest -m regression -v

# Run only cart tests
pytest -m cart -v

# Run only wishlist tests
pytest -m wishlist -v

# Run only address tests
pytest -m address -v

# Run only navigation tests
pytest -m navigation -v
```

### **Run Specific Test by Name**

```bash
# Run a specific test scenario
pytest tests/test_e2e_flow.py -k "e2e_kw_en_women" -v

# Run all tests containing "address" in name
pytest -k "address" -v
```

### **Generate HTML Report**

```bash
# Run tests and generate HTML report
pytest tests/

# Open the report in browser
open reports/latest_report.html
```

---

## 📊 Test Coverage

### **Test Modules (16 Total Tests)**

| Module | Tests | Description |
|--------|-------|-------------|
| **test_e2e_flow.py** | 2 | Complete purchase flow (happy path + cancellation) |
| **test_registration.py** | 1 | User registration via API + UI |
| **test_cart.py** | 1 | Add/remove items from cart |
| **test_wishlist.py** | 1 | Add items to wishlist |
| **test_address.py** | 3 | Address CRUD (add, edit, multiple) |
| **test_navigation.py** | 8 | Category pages, search results |

### **Functional Coverage**

✅ **User Management**
- Registration (API + UI)
- Login/Logout
- Session management

✅ **Product Discovery**
- Search functionality
- Category navigation
- Product detail pages

✅ **Shopping Cart**
- Add to cart
- Remove from cart
- Cart persistence

✅ **Wishlist**
- Add to wishlist
- Wishlist persistence

✅ **Checkout Flow**
- Address management (CRUD)
- Payment method selection
- Order placement

✅ **Payment Gateway**
- KNET integration
- Payment success flow
- Payment cancellation flow

✅ **Navigation**
- Homepage, categories, brands, search

---

## 📈 Reporting

### **HTML Report**

After running tests, a comprehensive HTML report is automatically generated:

```bash
# Report location
reports/latest_report.html

# Open in browser
open reports/latest_report.html
```

**Report Includes:**
- ✅ Test summary (passed/failed/skipped)
- ✅ Duration and pass rate
- ✅ Module coverage details
- ✅ Page object documentation
- ✅ Failure screenshots (embedded)
- ✅ Error messages and stack traces
- ✅ Environment information

### **Log Files**

Detailed logs are saved for every test run:

```bash
# View latest log
cat logs/latest.log

# View only errors
grep "ERROR\|FAIL" logs/latest.log

# View test summary
grep "TEST.*PASSED\|TEST.*FAILED" logs/latest.log
```

---

## 📝 Logging System

### **Log Levels**

| Level | Icon | Purpose |
|-------|------|---------|
| **INFO** | ℹ️ | General information |
| **PASS** | ✅ | Test/step passed |
| **FAIL** | ❌ | Test/step failed |
| **ERROR** | 🔥 | Error occurred |
| **WARN** | ⚠️ | Warning message |
| **DEBUG** | 🔍 | Debug information |
| **SKIP** | ⏭️ | Test/step skipped |

### **What's Logged**

- ✅ Test start/end with duration
- 📝 Every test step with timestamps
- 🔍 Debug information (variables, page state)
- 🌐 API calls with response times
- ❌ Detailed error messages with stack traces
- 📸 Screenshot captures with reasons
- ⚡ Assertions with expected vs actual values

### **Log File Locations**

```
logs/
├── latest.log                     # Symlink to most recent log
└── test_run_20260420_102244.log  # Timestamped log (never overwritten)
```

---

## ➕ Adding New Tests

### **Step 1: Add Test Data**

Edit `data/test_data.py`:

```python
# Add new scenario to existing data list
E2E_DATA = [
    # ... existing scenarios ...
    {
        "id": "e2e_sa_ar_men",  # Unique ID
        "full_name": "Test User",
        "mobile_number": "50012345",
        "email": f"test.{_TS}@mailinator.com",
        "password": "Test@1234",
        "gender": "men",
        "lang": "ar",
        "country": "sa",
        "search_term": "watch",
        "address_key": "sa_riyadh",
    },
]
```

### **Step 2: Add Page Object (if needed)**

If testing a new page, create a new page object in `pages/`:

```python
# pages/new_page.py
from pages.base_page import BasePage

class NewPage(BasePage):
    def some_action(self):
        # Implement page actions
        pass
```

### **Step 3: Write Test**

Create or update test file in `tests/`:

```python
# tests/test_new_feature.py
import pytest
from data.test_data import NEW_DATA
from pages.new_page import NewPage

@pytest.mark.regression
@pytest.mark.parametrize("data", NEW_DATA, ids=[d["id"] for d in NEW_DATA])
def test_new_feature(page, data):
    """Test description"""
    new_page = NewPage(page)
    new_page.some_action()
    assert True  # Add assertions
```

### **Step 4: Run New Test**

```bash
pytest tests/test_new_feature.py -v
```

---

## 🔧 Troubleshooting

### **Common Issues**

**1. Browser Not Found**
```bash
# Solution: Install Playwright browsers
playwright install chromium
```

**2. Import Errors**
```bash
# Solution: Install dependencies
pip install -r requirements.txt
```

**3. Timeout Errors**
```bash
# Solution: Increase timeout in config/settings.py
DEFAULT_TIMEOUT = 60_000  # Increase to 60 seconds
```

**4. Element Not Found**
```bash
# Solution: Check selector in page object
# Add wait before interaction
page.wait_for_selector("selector", state="visible")
```

### **Debug Mode**

Run tests with verbose output:

```bash
# Show detailed output
pytest tests/ -v -s

# Show only failed tests
pytest tests/ -v --tb=short

# Stop on first failure
pytest tests/ -x
```

### **View Failure Details**

```bash
# Check screenshot
open screenshots/fail_test_name.png

# Check video
open videos/test_video.webm

# Check log
cat logs/latest.log | grep -A 20 "ERROR"
```

---

## 📚 Documentation

- **[FRAMEWORK_ARCHITECTURE.md](FRAMEWORK_ARCHITECTURE.md)** - Detailed framework documentation
- **[LOGGING_GUIDE.md](LOGGING_GUIDE.md)** - Complete logging system guide
- **[DEBUG_REFERENCE.md](DEBUG_REFERENCE.md)** - Debugging tips and tricks
- **[FIXES_APPLIED.md](FIXES_APPLIED.md)** - Bug fixes history
- **[GITHUB_PUSH_GUIDE.md](GITHUB_PUSH_GUIDE.md)** - GitHub push instructions
- **[OPTIMIZATION_SUMMARY.md](OPTIMIZATION_SUMMARY.md)** - Code optimization details

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-test`)
3. Add your changes
4. Commit with clear message (`git commit -m "Add: New test for feature X"`)
5. Push to branch (`git push origin feature/new-test`)
6. Create Pull Request

---

## 📄 License

This project is for internal use only.

---

## 👥 Team

**QA Automation Team**  
Boutiqaat E-commerce Platform

---

## 📞 Support

For issues or questions:
1. Check [DEBUG_REFERENCE.md](DEBUG_REFERENCE.md)
2. Review logs in `logs/latest.log`
3. Check screenshots in `screenshots/`
4. Contact QA team

---

**Framework Version:** 1.0  
**Last Updated:** April 2026  
**Status:** ✅ Production Ready

