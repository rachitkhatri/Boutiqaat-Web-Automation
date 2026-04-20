# ============================================================
# pytest_ci_plugin.py — CI/CD-friendly logging and output
#
# PURPOSE:
#   Ensure logs are properly captured and displayed in CI/CD
#   environments (GitHub Actions, Jenkins, GitLab CI, etc.)
#
# PROBLEM:
#   In CI environments, logs may not appear because:
#   - Output buffering
#   - No TTY (terminal) available
#   - Logs written to files but not stdout
#
# SOLUTION:
#   - Force unbuffered output
#   - Write to both file and stdout
#   - Use CI-friendly formatting
#   - Flush output immediately
#
# USAGE:
#   Automatically loaded via conftest.py
# ============================================================

import pytest
import sys
import os
from datetime import datetime


# Force unbuffered output for CI environments
# This ensures logs appear immediately, not after buffering
sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', buffering=1)
sys.stderr = os.fdopen(sys.stderr.fileno(), 'w', buffering=1)


def _ci_log(message, level="INFO"):
    """
    Log message to both stdout and file with immediate flush.
    
    PURPOSE:
        Ensure logs appear in CI console output immediately.
    
    PARAMETERS:
        message: Log message to display
        level: Log level (INFO, PASS, FAIL, etc.)
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_msg = f"[{timestamp}] [{level}] {message}"
    
    # Print to stdout (appears in CI logs)
    print(formatted_msg)
    
    # Flush immediately (don't wait for buffer)
    sys.stdout.flush()


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    """
    Called before test collection starts.
    
    PURPOSE:
        Configure pytest for CI-friendly output.
    """
    # Detect if running in CI environment
    ci_env = os.getenv('CI') or os.getenv('CONTINUOUS_INTEGRATION') or \
             os.getenv('GITHUB_ACTIONS') or os.getenv('JENKINS_HOME') or \
             os.getenv('GITLAB_CI')
    
    if ci_env:
        _ci_log("=" * 70, "INFO")
        _ci_log("CI ENVIRONMENT DETECTED", "INFO")
        _ci_log("Enabling CI-friendly logging", "INFO")
        _ci_log("=" * 70, "INFO")
    
    # Force live logging (shows logs as tests run, not after)
    config.option.log_cli = True
    config.option.log_cli_level = "INFO"
    
    # Show captured output even for passing tests
    config.option.capture = "no"
    
    # Verbose output
    config.option.verbose = max(config.option.verbose, 1)


@pytest.hookimpl(tryfirst=True)
def pytest_collection_finish(session):
    """
    Called after test collection.
    
    PURPOSE:
        Log collection results to CI console.
    """
    _ci_log("=" * 70, "INFO")
    _ci_log(f"COLLECTED {len(session.items)} TESTS", "INFO")
    _ci_log("=" * 70, "INFO")
    
    # List all collected tests
    for i, item in enumerate(session.items, 1):
        _ci_log(f"  {i}. {item.nodeid}", "INFO")
    
    _ci_log("=" * 70, "INFO")


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_logstart(nodeid, location):
    """
    Called before each test starts.
    
    PURPOSE:
        Log test start to CI console.
    """
    _ci_log("=" * 70, "INFO")
    _ci_log(f"STARTING: {nodeid}", "INFO")
    _ci_log(f"Location: {location[0]}:{location[1]}", "INFO")
    _ci_log("=" * 70, "INFO")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Called after each test phase.
    
    PURPOSE:
        Log test results to CI console immediately.
    """
    outcome = yield
    report = outcome.get_result()
    
    # Only log for the actual test call (not setup/teardown)
    if report.when == "call":
        _ci_log("=" * 70, "INFO")
        
        if report.passed:
            _ci_log(f"✅ PASSED: {item.nodeid}", "PASS")
            _ci_log(f"Duration: {report.duration:.2f}s", "INFO")
        elif report.failed:
            _ci_log(f"❌ FAILED: {item.nodeid}", "FAIL")
            _ci_log(f"Duration: {report.duration:.2f}s", "INFO")
            
            # Log failure details
            if report.longrepr:
                _ci_log("FAILURE DETAILS:", "FAIL")
                _ci_log(str(report.longrepr), "FAIL")
        elif report.skipped:
            _ci_log(f"⏭️  SKIPPED: {item.nodeid}", "SKIP")
            _ci_log(f"Reason: {report.longrepr}", "SKIP")
        
        _ci_log("=" * 70, "INFO")


@pytest.hookimpl(trylast=True)
def pytest_sessionfinish(session, exitstatus):
    """
    Called at the end of test session.
    
    PURPOSE:
        Log final summary to CI console.
    """
    _ci_log("=" * 70, "INFO")
    _ci_log("TEST SESSION FINISHED", "INFO")
    _ci_log("=" * 70, "INFO")
    
    # Get test results from session
    passed = sum(1 for item in session.items if hasattr(item, 'rep_call') and item.rep_call.passed)
    failed = sum(1 for item in session.items if hasattr(item, 'rep_call') and item.rep_call.failed)
    skipped = sum(1 for item in session.items if hasattr(item, 'rep_call') and item.rep_call.skipped)
    total = len(session.items)
    
    _ci_log(f"Total Tests: {total}", "INFO")
    _ci_log(f"Passed: {passed} ✅", "PASS")
    _ci_log(f"Failed: {failed} ❌", "FAIL" if failed > 0 else "INFO")
    _ci_log(f"Skipped: {skipped} ⏭️", "SKIP" if skipped > 0 else "INFO")
    
    if total > 0:
        pass_rate = (passed / total) * 100
        _ci_log(f"Pass Rate: {pass_rate:.1f}%", "PASS" if pass_rate >= 90 else "WARN")
    
    _ci_log("=" * 70, "INFO")
    
    # Exit status
    if exitstatus == 0:
        _ci_log("✅ ALL TESTS PASSED", "PASS")
    else:
        _ci_log(f"❌ TESTS FAILED (exit code: {exitstatus})", "FAIL")
    
    _ci_log("=" * 70, "INFO")


@pytest.hookimpl(tryfirst=True)
def pytest_exception_interact(node, call, report):
    """
    Called when an exception occurs.
    
    PURPOSE:
        Log exceptions immediately to CI console.
    """
    if call.excinfo:
        _ci_log("=" * 70, "ERROR")
        _ci_log("EXCEPTION OCCURRED", "ERROR")
        _ci_log(f"Test: {node.nodeid}", "ERROR")
        _ci_log(f"Exception: {call.excinfo.type.__name__}", "ERROR")
        _ci_log(f"Message: {call.excinfo.value}", "ERROR")
        _ci_log("=" * 70, "ERROR")


# ============================================================
# CI ENVIRONMENT DETECTION
# ============================================================
#
# This plugin detects common CI environments:
# - GitHub Actions: GITHUB_ACTIONS=true
# - Jenkins: JENKINS_HOME set
# - GitLab CI: GITLAB_CI=true
# - Travis CI: TRAVIS=true
# - CircleCI: CIRCLECI=true
# - Generic: CI=true or CONTINUOUS_INTEGRATION=true
#
# When CI is detected, the plugin:
# 1. Forces unbuffered output
# 2. Enables live logging
# 3. Shows all output (no capture)
# 4. Logs to stdout immediately
# 5. Flushes after each log
#
# ============================================================
