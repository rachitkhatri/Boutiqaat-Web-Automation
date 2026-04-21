# 🧪 Boutiqaat Automation Framework

**Execute the complete suite — Run the Below Command**
```bash
python3 -m pytest tests/ -v --log-cli-level=DEBUG
```

**Stop the execution**
Usually we use `Ctrl + C` but if that does not work, open a new terminal and run:
```bash
pkill -f pytest
```

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
- [Custom Pytest Plugins](#-custom-pytest-plugins)
- [Page Object Model (POM)](#-page-object-model-pom)
- [Test Data Management](#-test-data-management)
- [Configuration](#-configuration)
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
| **Requests** | REST API calls (user registration bypasses flaky T&C checkbox) |
| **python-dotenv** | Load `.env` file for environment-specific config |
| **pytest-html** | HTML report generation |
| **pytest-json-report** | JSON format test results |

### **Architecture Pattern**

**Page Object Model (POM)**
- Each web page = One Python class
- Page elements and actions = Class methods
- All page classes inherit from `BasePage` for shared utilities
- Benefits: Maintainable, reusable, readable

---

## 📂 Project Structure

```
boutiqaat-automation/
│
├── config/                          # ⚙️ Configuration
│   ├── __init__.py                 # Makes config a Python package
│   └── settings.py                 # BASE_DOMAIN, timeouts, paths (single source of truth)
│
├── data/                            # 📊 Test Data
│   ├── __init__.py                 # Makes data a Python package
│   └── test_data.py                # All datasets: E2E_DATA, CART_DATA, ADDRESS_DATA, etc.
│
├── pages/                           # 📄 Page Object Model (POM)
│   ├── __init__.py                 # Makes pages a Python package
│   ├── base_page.py                # Parent class — dismiss_overlays, type_like_user, screenshot
│   ├── login_page.py               # Login page — fill email/password, click LOGIN
│   ├── registration_page.py        # Register via REST API + login via UI (bypasses T&C)
│   ├── search_page.py              # Search overlay — type query, select from autocomplete
│   ├── cart_page.py                # Add to cart, open cart, remove item, count items
│   ├── address_page.py             # Address CRUD — fill form, save, edit, add second address
│   ├── payment_page.py             # Payment — dismiss modal, select KNET, place order, cancel
│   ├── wishlist_page.py            # Wishlist — add from PDP, count items via API
│   └── navigation_page.py          # Category pages — verify page loads with product grid
│
├── tests/                           # 🧪 Test Suites (16 tests total)
│   ├── __init__.py                 # Makes tests a Python package
│   ├── test_e2e_flow.py            # End-to-end: happy path + cancel path (2 tests)
│   ├── test_registration.py        # User registration via API + UI (1 test)
│   ├── test_cart.py                # Cart: add 2 products, remove 1 (1 test)
│   ├── test_wishlist.py            # Wishlist: add from PDP (1 test)
│   ├── test_address.py             # Address: add, edit, add second (3 tests)
│   ├── test_navigation.py          # Navigation: 8 category/search pages (8 tests)
│   └── test_markers.py             # Reusable skip markers for flaky tests
│
├── utils/                           # 🛠️ Utilities
│   ├── __init__.py                 # Makes utils a Python package
│   └── logger.py                   # Enhanced logging — file + console, icons, stack traces
│
├── logs/                            # 📝 Test Logs (auto-generated, git-ignored)
│   ├── latest.log                  # Always points to most recent log
│   └── test_run_*.log              # Timestamped log per run
│
├── reports/                         # 📊 HTML Reports (auto-generated, git-ignored)
│   ├── latest_report.html          # Most recent report
│   └── report_*.html               # Timestamped reports
│
├── screenshots/                     # 📸 Failure Screenshots (auto-generated, git-ignored)
│   └── fail_*.png                  # Auto-captured on test failure
│
├── videos/                          # 🎥 Test Videos (auto-generated, git-ignored)
│   └── *.webm                      # Playwright video recording per test
│
├── conftest.py                      # Pytest fixtures — browser config, timeouts, screenshot hook
├── pytest.ini                       # Pytest settings — markers, log format, addopts
├── pytest_html_report_plugin.py     # Custom HTML report with module coverage & POM docs
├── pytest_logging_plugin.py         # Test start/end logging with duration tracking
├── pytest_progress_plugin.py        # Real-time progress bar and ETA during execution
├── pytest_ci_plugin.py              # CI/CD-friendly unbuffered output for GitHub Actions/Jenkins
├── requirements.txt                 # Python dependencies
├── run_tests_ci.sh                  # Shell script for CI/CD pipeline execution
├── .env                             # Environment variables (git-ignored — contains credentials)
├── .gitignore                       # Excludes .env, logs/, reports/, screenshots/, videos/, __pycache__/
│
└── 📚 Documentation
    ├── README.md                    # This file
    ├── FRAMEWORK_ARCHITECTURE.md    # Detailed framework documentation
    ├── LOGGING_GUIDE.md             # Logging system guide
    ├── DEBUG_REFERENCE.md           # Debugging tips
    ├── FIXES_APPLIED.md             # Bug fixes history
    ├── GITHUB_PUSH_GUIDE.md         # GitHub instructions
    └── OPTIMIZATION_SUMMARY.md      # Optimization details
```

---

## 🚀 Setup Instructions

### **Prerequisites**

- Python 3.9 or higher
- pip (Python package manager)
- Git (for version control)

### **Step 1: Clone Repository**

```bash
git clone #Gitlab URL
```

### **Step 2: Install Python Dependencies**

```bash
pip install -r requirements.txt
```

**What gets installed:**
| Package | Why |
|---------|-----|
| `playwright` | Browser automation engine |
| `pytest` | Test runner and assertion framework |
| `pytest-playwright` | Provides `page`, `browser` fixtures to pytest |
| `pytest-html` | HTML report generation |
| `pytest-json-report` | JSON report output |
| `requests` | HTTP client for REST API registration |
| `python-dotenv` | Loads `.env` file into `os.environ` |

### **Step 3: Install Playwright Browsers**

```bash
# Install Chromium (required)
playwright install chromium

# Optional: Install all browsers
playwright install
```

### **Step 4: Create .env File**

```bash
cp .env.example .env
# Edit .env with your values if needed
```

The `.env` file controls:
- `BASE_URL` — Target site (default: `https://www.boutiqaat.com`)
- `DEFAULT_TIMEOUT` — Element wait timeout in ms (default: `30000`)
- `PAGE_SETTLE_MS` — React hydration wait in ms (default: `4000`)
- `PAYMENT_TIMEOUT` — Manual payment wait in ms (default: `180000`)

### **Step 5: Verify Installation**

```bash
# Check pytest
python3 -m pytest --version

# Check Playwright
playwright --version

# Collect all tests (should show 16)
python3 -m pytest --co -q
```

---

## 🧪 Running Tests

### **Run All Tests (16 tests)**

```bash
python3 -m pytest tests/ -v
```

### **Run with Debug Logging**

```bash
python3 -m pytest tests/ -v --log-cli-level=DEBUG
```

### **Run Specific Test Module**

```bash
# E2E flow (happy path + cancel)
python3 -m pytest tests/test_e2e_flow.py -v

# Registration only
python3 -m pytest tests/test_registration.py -v

# Cart only
python3 -m pytest tests/test_cart.py -v

# Address management
python3 -m pytest tests/test_address.py -v

# Navigation/category pages
python3 -m pytest tests/test_navigation.py -v

# Wishlist
python3 -m pytest tests/test_wishlist.py -v
```

### **Run by Marker (Test Category)**

```bash
pytest -m regression -v    # E2E regression tests
pytest -m cart -v           # Cart tests
pytest -m wishlist -v       # Wishlist tests
pytest -m address -v        # Address CRUD tests
pytest -m navigation -v     # Category page tests
pytest -m registration -v   # Registration tests
```

### **Run Specific Test by Name**

```bash
# Run one specific test
python3 -m pytest tests/test_e2e_flow.py -k "complete" -v

# Run all tests with "address" in the name
python3 -m pytest -k "address" -v
```

### **Run in CI/CD**

```bash
# Using the CI shell script
chmod +x run_tests_ci.sh
./run_tests_ci.sh

# Or run specific tests in CI
./run_tests_ci.sh tests/test_navigation.py
```

### **Stop Execution**

```bash
# Graceful stop (finishes current test)
Ctrl + C

# Force kill immediately
Ctrl + C (press twice rapidly)

# If terminal is unresponsive, open a new terminal:
pkill -f pytest
pkill -f chromium    # Also kill browser if stuck
```

---

## 📊 Test Coverage

### **Test Modules (16 Total Tests)**

| Module | Tests | Marker | Description |
|--------|-------|--------|-------------|
| `test_e2e_flow.py` | 2 | `regression` | Complete purchase flow (happy path + cancellation) |
| `test_registration.py` | 1 | `registration` | User registration via API + UI login |
| `test_cart.py` | 1 | `cart` | Add 2 products, remove 1, verify remaining |
| `test_wishlist.py` | 1 | `wishlist` | Add product to wishlist from PDP |
| `test_address.py` | 3 | `address` | Address add, edit, and add second address |
| `test_navigation.py` | 8 | `navigation` | Homepage, categories, brands, search results |

### **Functional Coverage**

✅ **User Management**
- Registration via REST API (bypasses flaky T&C checkbox)
- Login via UI (email + password)
- Session management (PHPSESSID cookie)
- Timestamp-based unique emails (no manual cleanup)

✅ **Product Discovery**
- Search overlay (click magnifier → type → autocomplete)
- Category navigation (makeup, fragrance, skincare, haircare)
- Brands page listing
- Product detail page (PDP) navigation

✅ **Shopping Cart**
- Add to cart from PDP (Buy Now button)
- Add multiple products
- Remove item via trash icon
- Cart item count verification

✅ **Wishlist**
- Add to wishlist from PDP (heart icon)
- Wishlist state persistence

✅ **Checkout Flow**
- Address form filling (area → block → street → villa → phone)
- Dynamic block dropdown (loads after area selection)
- Address save, edit, and add second address
- Continue to payment verification

✅ **Payment Gateway**
- Dismiss "Free Delivery" promotional modal
- Payment method selection (KNET, Credit Card, Tabby, Amex, Deema)
- Wallet balance selection
- Place order → redirect to KNET gateway (kpay.com.kw)
- Happy path: wait for /paymentsuccess URL
- Cancel path: click Cancel → capture OOPS screen details + screenshot

✅ **Navigation (No Login Required)**
- Homepage women section
- Makeup, Fragrance, Skincare, Haircare categories
- Brands listing page
- Search results (perfume, lipstick)
- Product grid verification (min items check)
- Page title validation (no 404/error pages)

---

## 📈 Reporting

### **HTML Report (Auto-Generated)**

Every test run automatically generates a comprehensive HTML report:

```bash
# Report is auto-generated after every run
# Open the latest report:
open reports/latest_report.html
```

**Report Includes:**
- ✅ Summary cards (total, passed, failed, skipped, duration, pass rate)
- ✅ Visual progress bar (green/red/yellow)
- ✅ Module-level coverage breakdown with test lists
- ✅ Page Object Model documentation (all classes and methods)
- ✅ Test environment info (OS, Python version, browser)
- ✅ Failed test analysis with stack traces
- ✅ Embedded failure screenshots (base64)
- ✅ Filter buttons (All / Passed / Failed / Skipped)
- ✅ Clickable rows to expand error details

### **Log Files**

```bash
# View latest log
cat logs/latest.log

# View only errors
grep "ERROR\|FAIL" logs/latest.log

# View test pass/fail summary
grep "TEST.*PASSED\|TEST.*FAILED" logs/latest.log
```

---

## 📝 Logging System

### **How It Works**

The `utils/logger.py` module provides a unified logging system that writes to both console (with emoji icons) and timestamped log files simultaneously.

### **Log Levels**

| Level | Icon | Purpose |
|-------|------|---------|
| `INFO` | ℹ️ | General information |
| `PASS` | ✅ | Test/step passed |
| `FAIL` | ❌ | Test/step failed |
| `ERROR` | 🔥 | Exception occurred |
| `WARN` | ⚠️ | Warning message |
| `DEBUG` | 🔍 | Debug information |
| `SKIP` | ⏭️ | Test/step skipped |

### **Available Log Functions**

| Function | Purpose |
|----------|---------|
| `log(message, level)` | General log with level |
| `log_error(exception, context)` | Detailed error with stack trace |
| `log_step(number, name, status)` | Numbered test step |
| `log_test_start(name, id)` | Mark test beginning |
| `log_test_end(name, status, duration)` | Mark test completion |
| `log_debug(var_name, var_value)` | Debug variable inspection |
| `log_page_info(page, context)` | Current URL and title |
| `log_api_call(method, url, status, time)` | API call details |
| `log_assertion(condition, expected, actual, passed)` | Assertion result |
| `log_screenshot(path, reason)` | Screenshot capture |
| `log_separator(title)` | Visual separator line |

### **Log File Locations**

```
logs/
├── latest.log                     # Always the most recent run
├── pytest_execution.log           # Pytest's built-in log output
└── test_run_20260420_102244.log   # Timestamped (never overwritten)
```

---

## 🔌 Custom Pytest Plugins

The framework uses 4 custom pytest plugins (registered in `conftest.py`):

### **1. pytest_logging_plugin.py — Test Lifecycle Logging**

Hooks into pytest's test lifecycle to log:
- Test start with name and ID
- Test end with PASSED/FAILED/SKIPPED status and duration
- Session start/finish summary
- Exception details when tests fail

### **2. pytest_html_report_plugin.py — Comprehensive HTML Report**

Generates a rich HTML report after each run with:
- Summary dashboard (cards + progress bar)
- Module-level coverage breakdown
- Page Object Model documentation
- Failed test analysis with embedded screenshots
- Filter/sort functionality
- Environment information

### **3. pytest_progress_plugin.py — Real-Time Progress Tracking**

Shows during execution:
- Current test number (e.g., "EXECUTING TEST 5/16")
- Percentage complete with visual progress bar
- Elapsed time and estimated time remaining
- Running pass/fail/skip counters

### **4. pytest_ci_plugin.py — CI/CD-Friendly Output**

Ensures logs work in CI environments (GitHub Actions, Jenkins, GitLab CI):
- Forces unbuffered stdout/stderr
- Detects CI environment variables
- Enables live logging
- Flushes output immediately after each log line
- Lists all collected tests at session start

---

## 📄 Page Object Model (POM)

### **Inheritance**

```
BasePage (base_page.py)
  ├── LoginPage (login_page.py)
  ├── RegistrationPage (registration_page.py)
  ├── SearchPage (search_page.py)
  ├── CartPage (cart_page.py)
  ├── AddressPage (address_page.py)
  ├── PaymentPage (payment_page.py)
  ├── WishlistPage (wishlist_page.py)
  └── NavigationPage (navigation_page.py)
```

### **Page Classes**

| Class | File | Key Methods |
|-------|------|-------------|
| **BasePage** | `base_page.py` | `dismiss_overlays()`, `type_like_user()`, `screenshot_on_failure()` |
| **LoginPage** | `login_page.py` | `open()`, `login(email, password)` |
| **RegistrationPage** | `registration_page.py` | `register_and_login(data)` — API registration + UI login with retry |
| **SearchPage** | `search_page.py` | `search(term)`, `select_first_product()` — autocomplete + fallback |
| **CartPage** | `cart_page.py` | `add_to_cart()`, `open_cart()`, `remove_first_item()`, `get_cart_item_count()` |
| **AddressPage** | `address_page.py` | `fill_address()`, `save_address()`, `edit_address()`, `add_new_address()`, `continue_to_payment()` |
| **PaymentPage** | `payment_page.py` | `dismiss_modal()`, `select_payment_method()`, `place_order()`, `cancel_payment()`, `capture_failure_details()` |
| **WishlistPage** | `wishlist_page.py` | `add_to_wishlist_from_pdp()`, `get_wishlist_count()` |
| **NavigationPage** | `navigation_page.py` | `verify_page_loads(url, name, min_items)`, `get_product_count()` |

### **Key Design Decisions**

- **API Registration**: The T&C checkbox on the registration page is unreliable across different viewport sizes. We use the REST API (`/rest/V1/customer/register`) for 100% reliable account creation, then login via UI to get a browser session. The API response body is validated for errors (not just HTTP status code) since the API can return 200 with an error message (e.g. invalid name).
- **Login Success Detection**: After clicking LOGIN, we verify the LOGIN button is no longer visible (it gets replaced by the username on successful login).
- **Overlay Dismissal**: Boutiqaat shows celebrity popups and modal backdrops that block clicks. `BasePage.dismiss_overlays()` removes them via JavaScript injection.
- **Human-Like Typing**: `type_like_user()` types character-by-character with 80ms delay to trigger keypress event handlers that `.fill()` would skip.
- **Dynamic Dropdowns**: The address form's block dropdown loads dynamically after area selection. The page object waits 2 seconds after selecting the area before filling the block.

---

## 📊 Test Data Management

### **Data-Driven Testing**

All test data lives in `data/test_data.py`. Each test module imports only what it needs:

```python
# test_e2e_flow.py imports:
from data.test_data import E2E_DATA, E2E_CANCEL_DATA, ADDRESS_DATA

# test_cart.py imports:
from data.test_data import CART_DATA

# test_address.py imports:
from data.test_data import ADDRESS_DATA
```

### **Datasets**

| Variable | Type | Used By | Purpose |
|----------|------|---------|---------|
| `ADDRESS_DATA` | `dict` | `test_address.py`, `test_e2e_flow.py` | Address form values keyed by `"{country}_{city}"` |
| `E2E_DATA` | `list[dict]` | `test_e2e_flow.py` | Happy-path purchase flow data |
| `E2E_CANCEL_DATA` | `list[dict]` | `test_e2e_flow.py` | Cancel-path flow data |
| `REGISTRATION_DATA` | `list[dict]` | `test_registration.py` | Registration-only test data |
| `CART_DATA` | `list[dict]` | `test_cart.py` | Cart operations test data |
| `WISHLIST_DATA` | `list[dict]` | `test_wishlist.py` | Wishlist test data |

### **Unique Emails**

Every dataset uses a Unix timestamp (`_TS`) in the email address:
```python
_TS = str(int(time.time()))  # e.g. "1745678901"
"email": f"e2e.happy.{_TS}@mailinator.com"
# Result: "e2e.happy.1745678901@mailinator.com"
```
This ensures each test run creates a fresh account — no manual cleanup needed.

---

## ⚙️ Configuration

### **conftest.py — Pytest Fixtures**

| Fixture | Scope | Auto | Purpose |
|---------|-------|------|---------|
| `browser_type_launch_args` | session | no | Chromium: headed mode, 100ms slow_mo, maximized |
| `browser_context_args` | session | no | No fixed viewport, video recording at 1920×1080 |
| `set_timeouts` | function | yes | 60s timeout for all interactions, overlay CSS injection |
| `capture_screenshot_on_failure` | function | yes | Auto-captures full-page PNG when test fails |

### **pytest.ini — Pytest Settings**

```ini
testpaths = tests                    # Where pytest looks for test files
addopts = -v --tb=short -p no:warnings --capture=no --log-cli-level=INFO
log_cli = true                       # Show logs in real-time during execution
log_file = logs/pytest_execution.log # Also write logs to file
```

### **Registered Markers**

```ini
markers =
    smoke:        Quick sanity checks
    regression:   Full end-to-end regression suite
    registration: Registration-specific tests
    cart:         Cart add and remove tests
    wishlist:     Wishlist add and remove tests
    address:      Address management tests (add, edit, second address)
    navigation:   Category, brand, and navigation page tests
```

### **.env — Environment Variables**

| Variable | Default | Purpose |
|----------|---------|---------|
| `BASE_URL` | `https://www.boutiqaat.com` | Target site URL |
| `DEFAULT_TIMEOUT` | `30000` | Element interaction timeout (ms) |
| `PAGE_SETTLE_MS` | `4000` | React hydration wait (ms) |
| `PAYMENT_TIMEOUT` | `180000` | Manual payment wait (ms) |
| `HEADLESS` | `false` | Run browser in headless mode |
| `CI` | `false` | CI environment flag |

---

## ➕ Adding New Tests

### **Step 1: Add Test Data**

Edit `data/test_data.py`:

```python
NEW_FEATURE_DATA = [
    {
        "id": "new_kw_en_women",
        "full_name": "New Tester",
        "mobile_number": "50099999",
        "email": f"new.{_TS}@mailinator.com",
        "password": "Test@1234",
        "gender": "women",
        "lang": "en",
        "country": "kw",
    },
]
```

### **Step 2: Add Page Object (if needed)**

Create `pages/new_page.py`:

```python
from pages.base_page import BasePage
from utils.logger import log

class NewPage(BasePage):
    def some_action(self):
        self.page.locator("#element").click()
        log("Action completed", "PASS")
```

### **Step 3: Write Test**

Create `tests/test_new_feature.py`:

```python
import pytest
from data.test_data import NEW_FEATURE_DATA
from pages.new_page import NewPage

@pytest.mark.regression
@pytest.mark.parametrize("data", NEW_FEATURE_DATA, ids=[d["id"] for d in NEW_FEATURE_DATA])
def test_new_feature(page, data):
    """Test description."""
    new_page = NewPage(page)
    new_page.some_action()
    assert True
```

### **Step 4: Register Marker (if new category)**

Add to `pytest.ini`:
```ini
markers =
    new_feature: New feature tests
```

### **Step 5: Run**

```bash
python3 -m pytest tests/test_new_feature.py -v
```

---

## 🔧 Troubleshooting

### **Common Issues**

| Problem | Solution |
|---------|----------|
| `Browser Not Found` | `playwright install chromium` |
| `Import Errors` | `pip install -r requirements.txt` |
| `Timeout Errors` | Increase `DEFAULT_TIMEOUT` in `.env` |
| `Element Not Found` | Check selector in page object, add explicit wait |
| `Login Fails` | Check API response body for errors (API may return 200 with error in body). Also check if site is rate-limiting |
| `Overlay Blocks Click` | `BasePage.dismiss_overlays()` should handle it |
| `Tests won't stop` | `pkill -f pytest && pkill -f chromium` |

### **Debug Mode**

```bash
# Verbose with all output
python3 -m pytest tests/ -v -s --log-cli-level=DEBUG

# Stop on first failure
python3 -m pytest tests/ -x

# Show only failed tests
python3 -m pytest tests/ -v --tb=short

# Run single test with full debug
python3 -m pytest tests/test_cart.py -k "cart" -v -s --log-cli-level=DEBUG
```

### **View Failure Details**

```bash
# Check failure screenshot
open screenshots/fail_test_name.png

# Check test video recording
open videos/*.webm

# Check error logs
cat logs/latest.log | grep -A 20 "ERROR"

# Check HTML report
open reports/latest_report.html
```

---

## 📚 Documentation

| File | Description |
|------|-------------|
| [README.md](README.md) | This file — complete framework guide |
| [FRAMEWORK_ARCHITECTURE.md](FRAMEWORK_ARCHITECTURE.md) | Detailed architecture documentation |
| [LOGGING_GUIDE.md](LOGGING_GUIDE.md) | Logging system guide |
| [DEBUG_REFERENCE.md](DEBUG_REFERENCE.md) | Debugging tips and tricks |
| [FIXES_APPLIED.md](FIXES_APPLIED.md) | Bug fixes history |
| [GITHUB_PUSH_GUIDE.md](GITHUB_PUSH_GUIDE.md) | GitHub push instructions |
| [OPTIMIZATION_SUMMARY.md](OPTIMIZATION_SUMMARY.md) | Code optimization details |
| [CI_INTEGRATION_GUIDE.md](CI_INTEGRATION_GUIDE.md) | CI/CD pipeline setup |

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

**Framework Version:** 1.0
**Last Updated:** April 2026
**Status:** ✅ Production Ready
