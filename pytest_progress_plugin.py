# ============================================================
# pytest_progress_plugin.py — Real-time execution progress tracking
#
# PURPOSE:
#   Track test execution progress and show percentage completion
#   in real-time during test runs.
#
# FEATURES:
#   - Shows X% complete after each test
#   - Logs execution progress to console and file
#   - Displays estimated time remaining
#   - Shows current test being executed
#   - Summary at the end with total time
#
# USAGE:
#   Automatically loaded via conftest.py
#   No manual intervention needed
# ============================================================

import pytest
import time
from datetime import datetime, timedelta
from utils.logger import log, log_separator

# Global variables to track progress
_total_tests = 0
_completed_tests = 0
_failed_tests = 0
_passed_tests = 0
_skipped_tests = 0
_session_start_time = 0
_test_start_times = {}


@pytest.hookimpl(tryfirst=True)
def pytest_collection_finish(session):
    """
    Called after test collection is complete.
    
    PURPOSE:
        Store the total number of tests collected so we can
        calculate percentage completion.
    
    PARAMETERS:
        session: Pytest session object containing collected tests
    """
    global _total_tests
    _total_tests = len(session.items)
    
    log_separator("TEST COLLECTION COMPLETE")
    log(f"Total tests collected: {_total_tests}", "INFO")
    log(f"Test execution will begin shortly...", "INFO")
    log_separator()


@pytest.hookimpl(tryfirst=True)
def pytest_sessionstart(session):
    """
    Called at the start of the test session.
    
    PURPOSE:
        Record session start time for total duration calculation.
    """
    global _session_start_time
    _session_start_time = time.time()
    
    log_separator("TEST EXECUTION STARTED")
    log(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", "INFO")
    log(f"Total tests to execute: {_total_tests}", "INFO")
    log_separator()


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_logstart(nodeid, location):
    """
    Called before each test starts execution.
    
    PURPOSE:
        Log which test is about to run and track start time.
    
    PARAMETERS:
        nodeid: Unique test identifier (e.g., tests/test_cart.py::test_add_to_cart)
        location: Tuple of (file, line, test_name)
    """
    global _test_start_times, _completed_tests
    
    # Store test start time
    _test_start_times[nodeid] = time.time()
    
    # Calculate progress
    progress_pct = (_completed_tests / _total_tests * 100) if _total_tests > 0 else 0
    
    # Extract test name from nodeid
    test_name = nodeid.split("::")[-1] if "::" in nodeid else nodeid
    
    log_separator()
    log(f"▶️  EXECUTING TEST {_completed_tests + 1}/{_total_tests} ({progress_pct:.1f}% complete)", "INFO")
    log(f"Test: {test_name}", "INFO")
    log(f"Location: {location[0]}:{location[1]}", "INFO")
    log_separator()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Called after each test phase (setup, call, teardown).
    
    PURPOSE:
        Track test results and update progress counters.
    """
    global _completed_tests, _passed_tests, _failed_tests, _skipped_tests
    
    outcome = yield
    report = outcome.get_result()
    
    # Only process the actual test call (not setup/teardown)
    if report.when == "call":
        nodeid = item.nodeid
        
        # Calculate test duration
        test_duration = time.time() - _test_start_times.get(nodeid, time.time())
        
        # Update counters based on result
        if report.passed:
            _passed_tests += 1
            status = "PASSED ✅"
            level = "PASS"
        elif report.failed:
            _failed_tests += 1
            status = "FAILED ❌"
            level = "FAIL"
        elif report.skipped:
            _skipped_tests += 1
            status = "SKIPPED ⏭️"
            level = "SKIP"
        else:
            status = "UNKNOWN"
            level = "INFO"
        
        # Increment completed counter
        _completed_tests += 1
        
        # Calculate progress
        progress_pct = (_completed_tests / _total_tests * 100) if _total_tests > 0 else 0
        
        # Calculate elapsed and estimated remaining time
        elapsed_time = time.time() - _session_start_time
        avg_time_per_test = elapsed_time / _completed_tests if _completed_tests > 0 else 0
        remaining_tests = _total_tests - _completed_tests
        estimated_remaining = avg_time_per_test * remaining_tests
        
        # Format times
        elapsed_str = str(timedelta(seconds=int(elapsed_time)))
        remaining_str = str(timedelta(seconds=int(estimated_remaining)))
        
        # Log test completion
        log_separator()
        log(f"Test Result: {status}", level)
        log(f"Test Duration: {test_duration:.2f}s", "INFO")
        log(f"Progress: {_completed_tests}/{_total_tests} tests ({progress_pct:.1f}% complete)", "INFO")
        log(f"Passed: {_passed_tests} | Failed: {_failed_tests} | Skipped: {_skipped_tests}", "INFO")
        log(f"Elapsed Time: {elapsed_str}", "INFO")
        log(f"Estimated Remaining: {remaining_str}", "INFO")
        log_separator()
        
        # Show progress bar
        _show_progress_bar(progress_pct)


def _show_progress_bar(percentage):
    """
    Display a visual progress bar in the console.
    
    PARAMETERS:
        percentage: Completion percentage (0-100)
    
    EXAMPLE OUTPUT:
        Progress: [████████████░░░░░░░░] 60.0%
    """
    bar_length = 20
    filled_length = int(bar_length * percentage / 100)
    bar = '█' * filled_length + '░' * (bar_length - filled_length)
    
    log(f"Progress: [{bar}] {percentage:.1f}%", "INFO")


@pytest.hookimpl(trylast=True)
def pytest_sessionfinish(session, exitstatus):
    """
    Called at the end of the test session.
    
    PURPOSE:
        Display final summary with all statistics.
    """
    global _session_start_time, _total_tests, _passed_tests, _failed_tests, _skipped_tests
    
    # Calculate total duration
    total_duration = time.time() - _session_start_time
    duration_str = str(timedelta(seconds=int(total_duration)))
    
    # Calculate pass rate
    pass_rate = (_passed_tests / _total_tests * 100) if _total_tests > 0 else 0
    
    log_separator("TEST EXECUTION COMPLETE")
    log(f"End time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", "INFO")
    log(f"Total Duration: {duration_str}", "INFO")
    log_separator()
    
    log_separator("FINAL SUMMARY")
    log(f"Total Tests:    {_total_tests}", "INFO")
    log(f"Passed:         {_passed_tests} ✅", "PASS")
    log(f"Failed:         {_failed_tests} ❌", "FAIL" if _failed_tests > 0 else "INFO")
    log(f"Skipped:        {_skipped_tests} ⏭️", "SKIP" if _skipped_tests > 0 else "INFO")
    log(f"Pass Rate:      {pass_rate:.1f}%", "PASS" if pass_rate >= 90 else "WARN")
    log_separator()
    
    # Show final progress bar (should be 100%)
    _show_progress_bar(100.0)
    
    # Exit status message
    if exitstatus == 0:
        log("✅ All tests completed successfully!", "PASS")
    elif _failed_tests > 0:
        log(f"❌ {_failed_tests} test(s) failed. Check logs for details.", "FAIL")
    else:
        log(f"⚠️  Test execution completed with exit status: {exitstatus}", "WARN")
    
    log_separator()


# ============================================================
# SUMMARY
# ============================================================
#
# This plugin provides:
# 1. Real-time progress tracking (X/Y tests, Z% complete)
# 2. Visual progress bar
# 3. Elapsed time tracking
# 4. Estimated time remaining
# 5. Per-test duration logging
# 6. Final summary with statistics
# 7. Pass rate calculation
#
# Example output during execution:
#
# ══════════════════════════════════════════════════════════════════
# ▶️  EXECUTING TEST 5/16 (25.0% complete)
# Test: test_add_to_cart[chromium-cart_puff_sippii_bottle]
# Location: tests/test_cart.py:45
# ══════════════════════════════════════════════════════════════════
#
# ... test execution ...
#
# ══════════════════════════════════════════════════════════════════
# Test Result: PASSED ✅
# Test Duration: 95.31s
# Progress: 5/16 tests (31.3% complete)
# Passed: 5 | Failed: 0 | Skipped: 0
# Elapsed Time: 0:07:23
# Estimated Remaining: 0:16:45
# ══════════════════════════════════════════════════════════════════
# Progress: [██████░░░░░░░░░░░░░░] 31.3%
# ══════════════════════════════════════════════════════════════════
#
# ============================================================
