# ============================================================
# logger.py — Enhanced logging with file output and debugging
# ============================================================

import os
import sys
import traceback
from datetime import datetime
from pathlib import Path

# Create logs directory
LOGS_DIR = "logs"
os.makedirs(LOGS_DIR, exist_ok=True)

# Log file with timestamp
LOG_FILE = os.path.join(LOGS_DIR, f"test_run_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

# Keep reference to latest log for easy access
LATEST_LOG = os.path.join(LOGS_DIR, "latest.log")


def _get_timestamp():
    """Returns formatted timestamp for log entries."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]


def _write_to_file(message: str):
    """Write message to both timestamped log and latest.log."""
    try:
        # Write to timestamped log
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(message + "\n")
        
        # Also write to latest.log for easy access
        with open(LATEST_LOG, "a", encoding="utf-8") as f:
            f.write(message + "\n")
    except Exception:
        pass  # Don't crash if logging fails


def log(message: str, level: str = "INFO"):
    """
    Enhanced logging with console output and file writing.
    
    Args:
        message: The message to log
        level: Log level (INFO, PASS, FAIL, WARN, ERROR, DEBUG, SKIP)
    
    Levels:
        INFO  → General information (blue)
        PASS  → Test passed (green checkmark)
        FAIL  → Test failed (red X)
        WARN  → Warning (yellow)
        ERROR → Error occurred (red)
        DEBUG → Debug information (gray)
        SKIP  → Test skipped (yellow)
    """
    timestamp = _get_timestamp()
    
    # Console output with colors
    icons = {
        "PASS":  "✅",
        "FAIL":  "❌",
        "INFO":  "ℹ️ ",
        "WARN":  "⚠️ ",
        "ERROR": "🔥",
        "DEBUG": "🔍",
        "SKIP":  "⏭️ ",
    }
    
    icon = icons.get(level.upper(), "ℹ️ ")
    console_msg = f"[{timestamp}] {icon} [{level.upper()}] {message}"
    
    # File output (plain text, no emojis)
    file_msg = f"[{timestamp}] [{level.upper()}] {message}"
    
    # Print to console
    print(console_msg)
    
    # Write to file
    _write_to_file(file_msg)


def log_error(error: Exception, context: str = ""):
    """
    Log detailed error information with stack trace.
    
    Args:
        error: The exception object
        context: Additional context about where the error occurred
    """
    timestamp = _get_timestamp()
    
    error_type = type(error).__name__
    error_msg = str(error)
    
    # Get stack trace
    tb = traceback.format_exc()
    
    # Console output
    console_output = f"""
{'='*70}
🔥 ERROR OCCURRED
{'='*70}
Time:     {timestamp}
Context:  {context}
Type:     {error_type}
Message:  {error_msg}
{'='*70}
Stack Trace:
{tb}
{'='*70}
"""
    print(console_output)
    
    # File output
    file_output = f"""
{'='*70}
ERROR OCCURRED
{'='*70}
Time:     {timestamp}
Context:  {context}
Type:     {error_type}
Message:  {error_msg}
{'='*70}
Stack Trace:
{tb}
{'='*70}
"""
    _write_to_file(file_output)


def log_step(step_number: int, step_name: str, status: str = "START"):
    """
    Log test step with clear formatting.
    
    Args:
        step_number: Step number (1, 2, 3...)
        step_name: Name of the step
        status: START, COMPLETE, or FAILED
    """
    timestamp = _get_timestamp()
    
    if status == "START":
        icon = "▶️"
        separator = "─" * 50
        msg = f"\n{separator}\n{icon} STEP {step_number}: {step_name}\n{separator}"
    elif status == "COMPLETE":
        icon = "✅"
        msg = f"{icon} STEP {step_number} COMPLETE: {step_name}"
    elif status == "FAILED":
        icon = "❌"
        msg = f"{icon} STEP {step_number} FAILED: {step_name}"
    else:
        icon = "ℹ️"
        msg = f"{icon} STEP {step_number}: {step_name} - {status}"
    
    console_msg = f"[{timestamp}] {msg}"
    file_msg = f"[{timestamp}] STEP {step_number}: {step_name} - {status}"
    
    print(console_msg)
    _write_to_file(file_msg)


def log_test_start(test_name: str, test_id: str = ""):
    """Log the start of a test case."""
    timestamp = _get_timestamp()
    separator = "=" * 70
    
    msg = f"""
{separator}
🧪 TEST STARTED: {test_name}
{separator}
Test ID:  {test_id}
Time:     {timestamp}
{separator}
"""
    print(msg)
    _write_to_file(msg)


def log_test_end(test_name: str, status: str, duration: float = 0):
    """
    Log the end of a test case.
    
    Args:
        test_name: Name of the test
        status: PASSED, FAILED, or SKIPPED
        duration: Test duration in seconds
    """
    timestamp = _get_timestamp()
    separator = "=" * 70
    
    icons = {
        "PASSED": "✅",
        "FAILED": "❌",
        "SKIPPED": "⏭️"
    }
    
    icon = icons.get(status.upper(), "ℹ️")
    
    msg = f"""
{separator}
{icon} TEST {status.upper()}: {test_name}
{separator}
Duration: {duration:.2f}s
Time:     {timestamp}
{separator}
"""
    print(msg)
    _write_to_file(msg)


def log_debug(variable_name: str, variable_value, show_type: bool = True):
    """
    Log debug information about variables.
    
    Args:
        variable_name: Name of the variable
        variable_value: Value of the variable
        show_type: Whether to show the type of the variable
    """
    timestamp = _get_timestamp()
    
    type_info = f" (type: {type(variable_value).__name__})" if show_type else ""
    msg = f"🔍 DEBUG: {variable_name} = {variable_value}{type_info}"
    
    console_msg = f"[{timestamp}] {msg}"
    file_msg = f"[{timestamp}] DEBUG: {variable_name} = {variable_value}{type_info}"
    
    print(console_msg)
    _write_to_file(file_msg)


def log_page_info(page, context: str = ""):
    """
    Log current page information for debugging.
    
    Args:
        page: Playwright page object
        context: Additional context
    """
    try:
        url = page.url
        title = page.title()
        
        msg = f"""
📄 PAGE INFO {f'({context})' if context else ''}
   URL:   {url}
   Title: {title}
"""
        print(msg)
        _write_to_file(msg.strip())
    except Exception as e:
        log(f"Could not get page info: {e}", "WARN")


def log_api_call(method: str, url: str, status_code: int = None, response_time: float = None):
    """
    Log API call details.
    
    Args:
        method: HTTP method (GET, POST, etc.)
        url: API endpoint URL
        status_code: Response status code
        response_time: Response time in seconds
    """
    timestamp = _get_timestamp()
    
    status_icon = "✅" if status_code and 200 <= status_code < 300 else "❌"
    
    msg = f"""
🌐 API CALL
   Method:        {method}
   URL:           {url}
   Status Code:   {status_code if status_code else 'N/A'}
   Response Time: {response_time:.3f}s {status_icon if status_code else ''}
"""
    
    console_msg = f"[{timestamp}] {msg}"
    file_msg = f"[{timestamp}] API: {method} {url} - Status: {status_code} - Time: {response_time}s"
    
    print(console_msg)
    _write_to_file(file_msg)


def log_assertion(condition: str, expected, actual, passed: bool):
    """
    Log assertion results.
    
    Args:
        condition: What is being asserted
        expected: Expected value
        actual: Actual value
        passed: Whether assertion passed
    """
    timestamp = _get_timestamp()
    icon = "✅" if passed else "❌"
    status = "PASSED" if passed else "FAILED"
    
    msg = f"""
{icon} ASSERTION {status}
   Condition: {condition}
   Expected:  {expected}
   Actual:    {actual}
"""
    
    console_msg = f"[{timestamp}] {msg}"
    file_msg = f"[{timestamp}] ASSERTION {status}: {condition} - Expected: {expected}, Actual: {actual}"
    
    print(console_msg)
    _write_to_file(file_msg)


def log_screenshot(path: str, reason: str = ""):
    """
    Log screenshot capture.
    
    Args:
        path: Path where screenshot was saved
        reason: Reason for taking screenshot
    """
    timestamp = _get_timestamp()
    reason_text = f" - {reason}" if reason else ""
    
    msg = f"📸 Screenshot saved: {path}{reason_text}"
    console_msg = f"[{timestamp}] {msg}"
    file_msg = f"[{timestamp}] SCREENSHOT: {path}{reason_text}"
    
    print(console_msg)
    _write_to_file(file_msg)


def log_separator(title: str = ""):
    """Print a visual separator in logs."""
    separator = "=" * 70
    if title:
        msg = f"\n{separator}\n{title.center(70)}\n{separator}"
    else:
        msg = f"\n{separator}"
    
    print(msg)
    _write_to_file(msg)


def get_log_file_path():
    """Returns the path to the current log file."""
    return LOG_FILE


def get_latest_log_path():
    """Returns the path to the latest.log file."""
    return LATEST_LOG


# Initialize log file with header
def _init_log():
    """Initialize log file with header information."""
    header = f"""
{'='*70}
BOUTIQAAT AUTOMATION TEST RUN
{'='*70}
Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Log File:   {LOG_FILE}
{'='*70}
"""
    _write_to_file(header)


# Initialize on import
_init_log()
