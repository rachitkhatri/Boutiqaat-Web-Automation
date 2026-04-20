# ============================================================
# conftest.py — Pytest fixtures and hooks shared across ALL tests.
#
# PURPOSE:
#   Central configuration file for pytest test execution.
#   Defines fixtures (reusable test components) and hooks
#   (callbacks that run at specific points in test lifecycle).
#
# WHAT ARE FIXTURES?
#   Fixtures are functions that run before/after tests to set up
#   and tear down test resources (browser, page, database, etc.)
#
# WHAT ARE HOOKS?
#   Hooks are callback functions that pytest calls at specific
#   points (before test, after test, on failure, etc.)
#
# FRAMEWORK: Pytest + Playwright
# ============================================================

# Import pytest framework - provides decorators and fixtures
import pytest

import os

# Import configuration values from our settings file
from config.settings import VIDEO_DIR, DEFAULT_TIMEOUT

# Import logging utility for screenshot capture logging
from utils.logger import log_screenshot

# ──────────────────────────────────────────────────────────────────
# PLUGIN REGISTRATION
# ──────────────────────────────────────────────────────────────────

# Register custom pytest plugins
# These plugins add extra functionality to pytest
# - pytest_logging_plugin: Enhanced test execution logging
# - pytest_html_report_plugin: Comprehensive HTML report generation
# - pytest_progress_plugin: Real-time execution progress tracking
# - pytest_ci_plugin: CI/CD-friendly logging and output
pytest_plugins = ["pytest_logging_plugin", "pytest_html_report_plugin", "pytest_progress_plugin", "pytest_ci_plugin"]


# ──────────────────────────────────────────────────────────────────
# BROWSER LAUNCH CONFIGURATION
# ──────────────────────────────────────────────────────────────────

@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    """
    Configure Chromium browser launch options.
    
    SCOPE: session
        - Runs once per test session (not per test)
        - Browser settings apply to all tests
    
    PARAMETERS:
        browser_type_launch_args: Default args from pytest-playwright
    
    RETURNS:
        dict: Browser launch configuration
    
    OPTIONS EXPLAINED:
        - headless: False = Show browser window (not headless mode)
                    Useful for debugging and watching tests run
        
        - slow_mo: 100 = Add 100ms delay between actions
                   Makes tests easier to follow visually
                   Simulates human-like interaction speed
        
        - args: ["--start-maximized"] = Launch browser in fullscreen
                Ensures all elements are visible
                Prevents viewport-related issues
    """
    return {
        **browser_type_launch_args,  # Keep default args from pytest-playwright
        "headless": os.getenv("CI") == "true",  # Headless in CI, visible locally
        "slow_mo":  100,              # 100ms delay between actions (human-like)
        "args":     ["--start-maximized"],  # Launch in fullscreen mode
    }


# ──────────────────────────────────────────────────────────────────
# BROWSER CONTEXT CONFIGURATION
# ──────────────────────────────────────────────────────────────────

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """
    Configure browser context (isolated browser session) options.
    
    WHAT IS BROWSER CONTEXT?
        A browser context is like an incognito window - isolated
        cookies, storage, and cache. Each test can have its own
        context for complete isolation.
    
    SCOPE: session
        - Context settings apply to all tests in the session
    
    PARAMETERS:
        browser_context_args: Default context args from pytest-playwright
    
    RETURNS:
        dict: Browser context configuration
    
    OPTIONS EXPLAINED:
        - no_viewport: True = Don't force a fixed viewport size
                       Allows --start-maximized to control window size
                       Without this, Playwright forces 1280x720
        
        - record_video_dir: Where to save test execution videos
                           Videos are saved automatically for each test
                           Useful for debugging failures
        
        - record_video_size: Video resolution (1920x1080 = Full HD)
                            High quality for clear playback
    """
    return {
        **browser_context_args,      # Keep default args from pytest-playwright
        "no_viewport":       True,   # Don't force viewport size (use maximized)
        "record_video_dir":  VIDEO_DIR,  # Save videos to videos/ folder
        "record_video_size": {"width": 1920, "height": 1080},  # Full HD resolution
    }


# ──────────────────────────────────────────────────────────────────
# TIMEOUT AND OVERLAY HANDLING
# ──────────────────────────────────────────────────────────────────

@pytest.fixture(autouse=True)
def set_timeouts(page):
    """
    Set generous timeouts and hide blocking overlays.
    
    AUTOUSE: True
        - Runs automatically before EVERY test
        - No need to explicitly request this fixture
    
    WHY NEEDED?
        - Boutiqaat.com can be slow to load
        - Default Playwright timeout (30s) is too short
        - Overlays/popups block element interactions
    
    PARAMETERS:
        page: Playwright page object (injected by pytest-playwright)
    
    WHAT IT DOES:
        1. Sets 60-second timeout for all element interactions
        2. Sets 60-second timeout for page navigations
        3. Injects CSS to hide blocking overlays
        4. Runs JavaScript to remove overlays dynamically
    """
    
    # Set 60-second timeout for element interactions
    # This applies to all .click(), .fill(), .wait_for_selector() calls
    # Increased from default 30s because boutiqaat.com is slow
    page.set_default_timeout(60_000)  # 60,000 milliseconds = 60 seconds
    
    # Set 60-second timeout for page navigations
    # This applies to page.goto() and page.wait_for_load_state() calls
    # Prevents timeout errors on slow page loads
    page.set_default_navigation_timeout(60_000)  # 60 seconds
    
    # Inject CSS and JavaScript to hide blocking overlays
    try:
        # add_init_script() runs JavaScript on every page load
        # This ensures overlays are hidden even after navigation
        page.add_init_script("""
            // Create a <style> element to inject CSS
            const style = document.createElement('style');
            
            // CSS rules to hide common overlay elements
            // !important ensures our rules override site's CSS
            style.textContent = `
                .celebriti-content,      /* Celebrity popup */
                .modal-backdrop,         /* Modal background overlay */
                .popup-overlay,          /* Generic popup overlay */
                #mobile-main-header .overlay {  /* Mobile header overlay */
                    display: none !important;        /* Hide element */
                    visibility: hidden !important;   /* Make invisible */
                    opacity: 0 !important;           /* Fully transparent */
                    pointer-events: none !important; /* Disable clicks */
                }
            `;
            
            // Append the <style> element to page <head>
            document.head.appendChild(style);
            
            // Also remove overlays dynamically every second
            // Some overlays are added after page load via JavaScript
            setInterval(() => {
                // Find all overlay elements
                document.querySelectorAll('.celebriti-content, .modal-backdrop, .popup-overlay').forEach(el => {
                    // Hide each overlay
                    el.style.display = 'none';
                });
            }, 1000);  // Run every 1000ms (1 second)
        """)
    except Exception:
        # If script injection fails, silently continue
        # This prevents test failure if page doesn't support scripts
        pass
    
    # yield = pause here and run the test
    # After test completes, execution continues below yield
    yield
    
    # Teardown code would go here (after yield)
    # Currently no teardown needed


# ──────────────────────────────────────────────────────────────────
# AUTOMATIC SCREENSHOT ON FAILURE
# ──────────────────────────────────────────────────────────────────

@pytest.fixture(autouse=True)
def capture_screenshot_on_failure(request, page):
    """
    Automatically capture screenshot when a test fails.
    
    AUTOUSE: True
        - Runs automatically for EVERY test
        - No need to explicitly request this fixture
    
    PARAMETERS:
        request: Pytest request object (contains test metadata)
        page: Playwright page object (for taking screenshots)
    
    HOW IT WORKS:
        1. Test runs (yield)
        2. After test completes, check if it failed
        3. If failed, take full-page screenshot
        4. Save screenshot with test name
        5. Log screenshot path
    
    SCREENSHOT NAMING:
        Format: fail_{test_name}.png
        Example: fail_test_complete_flow_chromium-e2e_kw_en_women.png
    """
    
    # yield = pause here and run the test
    # After test completes, execution continues below
    yield
    
    # Check if test failed
    # request.node.rep_call is set by pytest_runtest_makereport hook below
    # rep_call.failed is True if test failed, False otherwise
    if getattr(getattr(request.node, "rep_call", None), "failed", False):
        
        # Get test name and sanitize it for filename
        # Replace [ and ] with _ to avoid filesystem issues
        # Example: "test_login[chromium-user1]" → "test_login_chromium-user1_"
        name = request.node.name.replace("[", "_").replace("]", "")
        
        # Build screenshot path
        # Format: screenshots/fail_{test_name}.png
        path = f"screenshots/fail_{name}.png"
        
        try:
            # Take full-page screenshot (scrolls to capture entire page)
            # full_page=True ensures we capture content below the fold
            page.screenshot(path=path, full_page=True)
            
            # Log screenshot capture to console and log file
            log_screenshot(path, "Test failure")
            
        except Exception:
            # If screenshot fails (e.g., browser closed), silently continue
            # Don't fail the test just because screenshot failed
            pass


# ──────────────────────────────────────────────────────────────────
# PYTEST HOOK: ATTACH TEST RESULT TO NODE
# ──────────────────────────────────────────────────────────────────

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Pytest hook that runs after each test phase (setup, call, teardown).
    
    PURPOSE:
        Attach test result to the test node so other fixtures can
        access it (e.g., capture_screenshot_on_failure needs to know
        if test failed).
    
    HOOK PARAMETERS:
        - tryfirst=True: Run this hook before other hooks
        - hookwrapper=True: Wrap around other hooks (yield pattern)
    
    PARAMETERS:
        item: Test item (contains test metadata)
        call: Test call information
    
    WHAT IT DOES:
        1. Let pytest create the test report
        2. Attach report to test node as rep_{phase}
        3. Phases: setup, call, teardown
        4. Other fixtures can now access item.rep_call.failed
    
    EXAMPLE:
        After test runs:
        - item.rep_setup = setup phase report
        - item.rep_call = test execution report (main test)
        - item.rep_teardown = teardown phase report
    """
    
    # yield = let pytest create the report
    outcome = yield
    
    # Get the report object created by pytest
    rep = outcome.get_result()
    
    # Attach report to test node
    # setattr(item, "rep_call", rep) for call phase
    # setattr(item, "rep_setup", rep) for setup phase
    # setattr(item, "rep_teardown", rep) for teardown phase
    setattr(item, f"rep_{rep.when}", rep)
    
    # Now other fixtures can access:
    # - item.rep_call.failed (True if test failed)
    # - item.rep_call.passed (True if test passed)
    # - item.rep_call.skipped (True if test skipped)


# ──────────────────────────────────────────────────────────────────
# SUMMARY
# ──────────────────────────────────────────────────────────────────
#
# This file configures:
# 1. Browser launch (visible, maximized, slow motion)
# 2. Browser context (no viewport, video recording)
# 3. Timeouts (60s for slow site)
# 4. Overlay hiding (CSS + JavaScript injection)
# 5. Screenshot on failure (automatic capture)
# 6. Test result attachment (for other fixtures to use)
#
# All tests automatically get these configurations without
# needing to explicitly request them (autouse=True).
#
# ──────────────────────────────────────────────────────────────────
