# Enhanced Logging System Guide

## Overview

The enhanced logging system provides detailed, easy-to-read logs for debugging test failures. All logs are saved to files with timestamps and include comprehensive error information.

---

## Log Files Location

```
boutiqaat-automation/
├── logs/
│   ├── test_run_20240115_143022.log  # Timestamped log file
│   └── latest.log                     # Always points to most recent run
```

- **Timestamped logs**: Unique file for each test run (never overwritten)
- **latest.log**: Always contains the most recent test run (easy to find)

---

## Log Levels

### 1. **INFO** ℹ️
General information about test execution
```python
from utils.logger import log
log("Starting search operation", "INFO")
```

### 2. **PASS** ✅
Test step or assertion passed
```python
log("Login successful", "PASS")
```

### 3. **FAIL** ❌
Test step or assertion failed
```python
log("Cart count is 0, expected > 0", "FAIL")
```

### 4. **ERROR** 🔥
Error occurred during execution
```python
log("Element not found after 30s", "ERROR")
```

### 5. **WARN** ⚠️
Warning message (non-critical)
```python
log("Retrying login due to rate limiting", "WARN")
```

### 6. **DEBUG** 🔍
Debug information for troubleshooting
```python
log("Current URL: https://...", "DEBUG")
```

### 7. **SKIP** ⏭️
Test or step was skipped
```python
log("Wallet not available, skipping", "SKIP")
```

---

## Enhanced Logging Functions

### 1. **log_error()** - Detailed Error Logging

Automatically captures stack traces and error details:

```python
from utils.logger import log_error

try:
    page.locator("#missing-element").click()
except Exception as e:
    log_error(e, "Failed to click login button")
    raise
```

**Output:**
```
======================================================================
🔥 ERROR OCCURRED
======================================================================
Time:     2024-01-15 14:30:22.123
Context:  Failed to click login button
Type:     TimeoutError
Message:  Timeout 30000ms exceeded
======================================================================
Stack Trace:
  File "test_cart.py", line 45, in test_add_to_cart
    page.locator("#missing-element").click()
  ...
======================================================================
```

### 2. **log_step()** - Test Step Tracking

Track major test steps with clear formatting:

```python
from utils.logger import log_step

log_step(1, "Register user via API", "START")
# ... registration code ...
log_step(1, "Register user via API", "COMPLETE")
```

**Output:**
```
──────────────────────────────────────────────────
▶️ STEP 1: Register user via API
──────────────────────────────────────────────────
... test actions ...
✅ STEP 1 COMPLETE: Register user via API
```

### 3. **log_test_start() / log_test_end()** - Test Boundaries

Automatically logged by pytest plugin:

```
======================================================================
🧪 TEST STARTED: tests/test_cart.py::test_add_and_remove_cart_item
======================================================================
Test ID:  test_add_and_remove_cart_item[chromium-cart_perfume_kw]
Time:     2024-01-15 14:30:22.123
======================================================================
... test execution ...
======================================================================
✅ TEST PASSED: tests/test_cart.py::test_add_and_remove_cart_item
======================================================================
Duration: 45.23s
Time:     2024-01-15 14:31:07.456
======================================================================
```

### 4. **log_debug()** - Variable Inspection

Debug variable values during test execution:

```python
from utils.logger import log_debug

cart_count = cart.get_cart_item_count()
log_debug("cart_count", cart_count)
```

**Output:**
```
🔍 DEBUG: cart_count = 0 (type: int)
```

### 5. **log_page_info()** - Page State Debugging

Log current page URL and title:

```python
from utils.logger import log_page_info

log_page_info(page, "After login")
```

**Output:**
```
📄 PAGE INFO (After login)
   URL:   https://www.boutiqaat.com/en-kw/women/
   Title: Boutiqaat - Beauty Shopping
```

### 6. **log_api_call()** - API Request Tracking

Track API calls with timing:

```python
from utils.logger import log_api_call
import time

start = time.time()
response = requests.post(url, json=data)
duration = time.time() - start

log_api_call("POST", url, response.status_code, duration)
```

**Output:**
```
🌐 API CALL
   Method:        POST
   URL:           https://www.boutiqaat.com/rest/V1/customer/register
   Status Code:   200
   Response Time: 1.234s ✅
```

### 7. **log_assertion()** - Assertion Results

Log assertion checks with expected vs actual:

```python
from utils.logger import log_assertion

expected = 1
actual = cart.get_cart_item_count()
passed = actual > 0

log_assertion("Cart should have items", f"> 0", actual, passed)
```

**Output:**
```
✅ ASSERTION PASSED
   Condition: Cart should have items
   Expected:  > 0
   Actual:    1
```

### 8. **log_screenshot()** - Screenshot Tracking

Log when screenshots are captured:

```python
from utils.logger import log_screenshot

page.screenshot(path="screenshots/error.png")
log_screenshot("screenshots/error.png", "Cart count is 0")
```

**Output:**
```
📸 Screenshot saved: screenshots/error.png - Cart count is 0
```

---

## Usage Examples

### Example 1: Enhanced Cart Test

```python
from utils.logger import log, log_step, log_debug, log_assertion, log_error

def test_add_to_cart(page, data):
    try:
        # Step 1: Login
        log_step(1, "Login to application", "START")
        login(page, data)
        log_step(1, "Login to application", "COMPLETE")
        
        # Step 2: Search
        log_step(2, "Search for product", "START")
        search = SearchPage(page)
        search.search(data["search_term"])
        log_step(2, "Search for product", "COMPLETE")
        
        # Step 3: Add to cart
        log_step(3, "Add product to cart", "START")
        cart = CartPage(page)
        cart.add_to_cart()
        log_step(3, "Add product to cart", "COMPLETE")
        
        # Step 4: Verify cart count
        log_step(4, "Verify cart count", "START")
        count = cart.get_cart_item_count()
        log_debug("cart_count", count)
        
        passed = count > 0
        log_assertion("Cart should have items", "> 0", count, passed)
        
        if not passed:
            log("Cart count is 0 after adding item", "FAIL")
            page.screenshot(path="screenshots/cart_error.png")
            log_screenshot("screenshots/cart_error.png", "Cart count is 0")
            raise AssertionError(f"Cart count is {count}, expected > 0")
        
        log_step(4, "Verify cart count", "COMPLETE")
        
    except Exception as e:
        log_error(e, "Cart test failed")
        raise
```

### Example 2: Enhanced Login with Retry

```python
from utils.logger import log, log_debug, log_error

def login_with_retry(page, email, password, max_attempts=3):
    for attempt in range(1, max_attempts + 1):
        try:
            log(f"Login attempt {attempt}/{max_attempts}", "INFO")
            
            page.goto(login_url)
            log_debug("login_url", login_url)
            
            page.locator("input[name='email']").fill(email)
            page.locator("input[name='password']").fill(password)
            page.locator("button", has_text="LOGIN").click()
            
            page.wait_for_timeout(5000)
            
            current_url = page.url
            log_debug("current_url", current_url)
            
            if "login" not in current_url:
                log("Login successful", "PASS")
                return True
            else:
                log(f"Login attempt {attempt} failed - still on login page", "WARN")
                
        except Exception as e:
            log_error(e, f"Login attempt {attempt} error")
            if attempt == max_attempts:
                raise
    
    log("All login attempts failed", "FAIL")
    return False
```

---

## Reading Log Files

### Quick Access

```bash
# View latest log
cat logs/latest.log

# View latest log with colors (if supported)
tail -f logs/latest.log

# Search for errors
grep "ERROR" logs/latest.log

# Search for failed tests
grep "FAILED" logs/latest.log

# View specific test
grep "test_add_to_cart" logs/latest.log
```

### Log File Structure

```
======================================================================
BOUTIQAAT AUTOMATION TEST RUN
======================================================================
Start Time: 2024-01-15 14:30:00
Log File:   logs/test_run_20240115_143000.log
======================================================================

======================================================================
TEST SESSION STARTED
======================================================================
[2024-01-15 14:30:01.123] [INFO] Total tests collected: 5
[2024-01-15 14:30:01.124] [INFO] Log file: logs/test_run_20240115_143000.log
======================================================================

======================================================================
🧪 TEST STARTED: tests/test_cart.py::test_add_and_remove_cart_item
======================================================================
Test ID:  test_add_and_remove_cart_item[chromium-cart_perfume_kw]
Time:     2024-01-15 14:30:01.234
======================================================================

──────────────────────────────────────────────────
▶️ STEP 1: Login to application
──────────────────────────────────────────────────
[2024-01-15 14:30:02.345] [INFO] Login attempt 1/3
[2024-01-15 14:30:05.678] [PASS] Login successful
✅ STEP 1 COMPLETE: Login to application

... more steps ...

======================================================================
✅ TEST PASSED: tests/test_cart.py::test_add_and_remove_cart_item
======================================================================
Duration: 45.23s
Time:     2024-01-15 14:30:46.456
======================================================================
```

---

## Debugging Failed Tests

### Step 1: Check Latest Log

```bash
cat logs/latest.log | grep -A 20 "ERROR\|FAILED"
```

### Step 2: Find the Failed Test

Look for:
```
❌ TEST FAILED: tests/test_cart.py::test_add_and_remove_cart_item
```

### Step 3: Review Error Details

Find the error section:
```
======================================================================
🔥 ERROR OCCURRED
======================================================================
Context:  Failed to click login button
Type:     TimeoutError
Message:  Timeout 30000ms exceeded
```

### Step 4: Check Debug Information

Look for DEBUG entries before the error:
```
🔍 DEBUG: cart_count = 0 (type: int)
📄 PAGE INFO (After add to cart)
   URL:   https://www.boutiqaat.com/en-kw/checkout/cart/
```

### Step 5: View Screenshot

Check the screenshot mentioned in logs:
```
📸 Screenshot saved: screenshots/fail_test_add_to_cart.png - Cart count is 0
```

---

## Best Practices

1. **Use log_step() for major operations**
   - Makes it easy to see where tests fail

2. **Use log_debug() for variable inspection**
   - Helps understand state when errors occur

3. **Use log_error() in exception handlers**
   - Captures full stack traces automatically

4. **Use log_assertion() for important checks**
   - Shows expected vs actual values clearly

5. **Always log_screenshot() when taking screenshots**
   - Links screenshots to specific failures

6. **Use descriptive context messages**
   - Makes debugging faster and easier

---

## Integration with Existing Code

The logging system is already integrated:

- ✅ **conftest.py** - Automatic test start/end logging
- ✅ **base_page.py** - Enhanced error logging and screenshots
- ✅ All page objects can use enhanced logging functions

No changes needed to existing tests - enhanced logging works automatically!

---

## Summary

- 📁 All logs saved to `logs/` directory
- 📝 `latest.log` always has most recent run
- 🔍 Detailed error messages with stack traces
- 📊 Test timing and step tracking
- 🐛 Easy debugging with variable inspection
- 📸 Screenshot tracking and linking
- ✅ Automatic integration with pytest
