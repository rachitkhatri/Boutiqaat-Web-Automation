# ============================================================
# pytest_logging_plugin.py — Pytest hooks for enhanced logging
# ============================================================

import pytest
import time
from utils.logger import (
    log_test_start, 
    log_test_end, 
    log_separator,
    log,
    log_error,
    log_screenshot,
    get_log_file_path
)


class TestTimer:
    """Helper class to track test execution time."""
    def __init__(self):
        self.start_time = None
        self.end_time = None
    
    def start(self):
        self.start_time = time.time()
    
    def stop(self):
        self.end_time = time.time()
    
    def duration(self):
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        return 0


# Store test timers
test_timers = {}


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_setup(item):
    """Called before each test starts."""
    test_name = item.nodeid
    test_id = item.name
    
    # Start timer
    timer = TestTimer()
    timer.start()
    test_timers[test_name] = timer
    
    # Log test start
    log_test_start(test_name, test_id)


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_teardown(item, nextitem):
    """Called after each test completes."""
    test_name = item.nodeid
    
    # Stop timer
    if test_name in test_timers:
        test_timers[test_name].stop()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Called to create test report - captures pass/fail status."""
    outcome = yield
    report = outcome.get_result()
    
    # Only log for the actual test call (not setup/teardown)
    if report.when == "call":
        test_name = item.nodeid
        
        # Get duration
        duration = 0
        if test_name in test_timers:
            duration = test_timers[test_name].duration()
        
        # Determine status
        if report.passed:
            status = "PASSED"
        elif report.failed:
            status = "FAILED"
            
            # Log the failure details
            if report.longrepr:
                log_separator("TEST FAILURE DETAILS")
                log(str(report.longrepr), "ERROR")
                log_separator()
        elif report.skipped:
            status = "SKIPPED"
        else:
            status = "UNKNOWN"
        
        # Log test end
        log_test_end(test_name, status, duration)
        
        # Clean up timer
        if test_name in test_timers:
            del test_timers[test_name]


@pytest.hookimpl(tryfirst=True)
def pytest_sessionstart(session):
    """Called at the start of the test session."""
    log_separator("TEST SESSION STARTED")
    log(f"Total tests collected: {len(session.items) if hasattr(session, 'items') else 'Unknown'}", "INFO")
    log(f"Log file: {get_log_file_path()}", "INFO")
    log_separator()


@pytest.hookimpl(tryfirst=True)
def pytest_sessionfinish(session, exitstatus):
    """Called at the end of the test session."""
    log_separator("TEST SESSION FINISHED")
    
    # Get test results summary
    if hasattr(session, 'testscollected'):
        log(f"Total tests: {session.testscollected}", "INFO")
    
    if hasattr(session, 'testsfailed'):
        log(f"Failed: {session.testsfailed}", "FAIL" if session.testsfailed > 0 else "INFO")
    
    if hasattr(session, 'testspassed'):
        log(f"Passed: {session.testspassed}", "PASS")
    
    # Exit status
    status_messages = {
        0: "All tests passed ✅",
        1: "Some tests failed ❌",
        2: "Test execution interrupted ⚠️",
        3: "Internal error occurred 🔥",
        4: "pytest command line usage error ⚠️",
        5: "No tests collected ⚠️",
    }
    
    status_msg = status_messages.get(exitstatus, f"Unknown exit status: {exitstatus}")
    log(status_msg, "INFO")
    
    log(f"Log file saved: {get_log_file_path()}", "INFO")
    log_separator()


@pytest.hookimpl(tryfirst=True)
def pytest_exception_interact(node, call, report):
    """Called when an exception is raised during test execution."""
    if call.excinfo:
        exc_type = call.excinfo.type.__name__
        exc_value = str(call.excinfo.value)
        
        log_separator("EXCEPTION CAUGHT")
        log(f"Test: {node.nodeid}", "ERROR")
        log(f"Exception Type: {exc_type}", "ERROR")
        log(f"Exception Message: {exc_value}", "ERROR")
        log_separator()
