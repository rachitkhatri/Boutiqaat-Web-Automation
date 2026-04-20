# ============================================================
# settings.py — Single source of truth for all configuration.
# 
# PURPOSE:
#   Centralized configuration file for the entire test framework.
#   All URLs, timeouts, and paths are defined here to avoid
#   hardcoding values throughout the codebase.
#
# USAGE:
#   from config.settings import BASE_DOMAIN, DEFAULT_TIMEOUT
#
# MAINTENANCE:
#   Change environment, timeouts, or browser options here only.
#   All tests will automatically use the updated values.
# ============================================================

import os  # Operating system interface for file/directory operations
from dotenv import load_dotenv  # Load environment variables from .env file

# Load environment variables from .env file
# This reads .env file and makes variables available via os.getenv()
load_dotenv()

# ──────────────────────────────────────────────────────────────
# BASE CONFIGURATION
# ──────────────────────────────────────────────────────────────

# Base website URL - Target application under test
# This is the root domain for boutiqaat.com
# All page URLs are built from this base
# Can be overridden via .env file: BASE_URL=https://staging.boutiqaat.com
BASE_DOMAIN = os.getenv("BASE_URL", "https://www.boutiqaat.com")

# ──────────────────────────────────────────────────────────────
# TIMEOUT CONFIGURATION (in milliseconds)
# ──────────────────────────────────────────────────────────────

# Default timeout for element interactions and page loads
# 30 seconds is generous because boutiqaat.com can be slow
# Used by: Playwright's default_timeout setting
# Can be overridden via .env file: DEFAULT_TIMEOUT=60000
DEFAULT_TIMEOUT = int(os.getenv("DEFAULT_TIMEOUT", "30000"))

# Extra wait after page load for React/JavaScript to finish rendering
# Boutiqaat uses React which needs time to hydrate after page load
# This prevents "element not found" errors on dynamic content
# Used by: All page objects after navigation
# Can be overridden via .env file: PAGE_SETTLE_MS=2000
PAGE_SETTLE_MS = int(os.getenv("PAGE_SETTLE_MS", "4000"))

# Payment success wait timeout
# KNET payment gateway session expires after ~5 minutes
# We wait 3 minutes for manual payment completion
# Used by: payment_page.py wait_for_payment_success()
# Can be overridden via .env file: PAYMENT_TIMEOUT=180000
PAYMENT_TIMEOUT = int(os.getenv("PAYMENT_TIMEOUT", "180000"))

# ──────────────────────────────────────────────────────────────
# OUTPUT DIRECTORIES
# ──────────────────────────────────────────────────────────────

# Video recording output folder
# Playwright records video of each test execution
# Videos are saved here automatically
# Used by: conftest.py browser_context_args fixture
VIDEO_DIR = "videos/"

# Screenshots folder
# Failure screenshots are saved here automatically
# Each failed test gets a screenshot with test name
# Used by: conftest.py capture_screenshot_on_failure fixture
SCREENSHOTS_DIR = "screenshots/"

# Legacy single screenshot path
# Fallback path for manual screenshot captures
# Used by: base_page.py screenshot_on_failure() method
FAILURE_SCREENSHOT = "error.png"

# ──────────────────────────────────────────────────────────────
# DIRECTORY INITIALIZATION
# ──────────────────────────────────────────────────────────────

# Create output directories at import time
# This ensures directories exist before any test runs
# exist_ok=True prevents errors if directories already exist
# This runs once when settings.py is first imported
os.makedirs(VIDEO_DIR,       exist_ok=True)  # Create videos/ folder
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)  # Create screenshots/ folder

# ──────────────────────────────────────────────────────────────
# HELPER FUNCTIONS
# ──────────────────────────────────────────────────────────────

def build_url(lang: str, country: str, gender: str) -> str:
    """
    Build the landing page URL from language, country, and gender.
    
    Boutiqaat URL structure: /{lang}-{country}/{gender}/
    Example: /en-kw/women/ (English, Kuwait, Women's section)
    
    Args:
        lang (str): Language code (en=English, ar=Arabic)
        country (str): Country code (kw=Kuwait, sa=Saudi Arabia, ae=UAE)
        gender (str): Gender section (women, men, kids)
    
    Returns:
        str: Complete URL for the landing page
        
    Example:
        >>> build_url("en", "kw", "women")
        'https://www.boutiqaat.com/en-kw/women/'
    """
    # Concatenate base domain with locale and gender path
    return f"{BASE_DOMAIN}/{lang}-{country}/{gender}/"
