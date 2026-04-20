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

import os                        # File/directory operations
from dotenv import load_dotenv   # Read .env file into os.environ

# Load .env file so os.getenv() can read values like BASE_URL, DEFAULT_TIMEOUT
load_dotenv()

# ── BASE URL ──────────────────────────────────────────────────
# Root domain of the application under test.
# Override via .env: BASE_URL=https://staging.boutiqaat.com
BASE_DOMAIN = os.getenv("BASE_URL", "https://www.boutiqaat.com")

# ── TIMEOUTS (milliseconds) ──────────────────────────────────
# Max wait for element interactions (.click, .fill, .wait_for_selector)
DEFAULT_TIMEOUT = int(os.getenv("DEFAULT_TIMEOUT", "30000"))

# Extra pause after page.goto() for React hydration to finish
PAGE_SETTLE_MS = int(os.getenv("PAGE_SETTLE_MS", "4000"))

# How long to wait for manual payment completion on KNET gateway
PAYMENT_TIMEOUT = int(os.getenv("PAYMENT_TIMEOUT", "180000"))

# ── OUTPUT DIRECTORIES ────────────────────────────────────────
VIDEO_DIR       = "videos/"       # Playwright video recordings per test
SCREENSHOTS_DIR = "screenshots/"  # Failure screenshots (auto-captured)
FAILURE_SCREENSHOT = "error.png"  # Legacy fallback screenshot path

# Create output dirs at import time so they exist before any test runs
os.makedirs(VIDEO_DIR,       exist_ok=True)
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

# ── HELPER ────────────────────────────────────────────────────
def build_url(lang: str, country: str, gender: str) -> str:
    """
    Build a boutiqaat landing page URL.

    URL pattern: /{lang}-{country}/{gender}/
    Example:     /en-kw/women/

    Args:
        lang:    Language code  (en | ar)
        country: Country code   (kw | sa | ae)
        gender:  Site section   (women | men | kids)

    Returns:
        Full URL string, e.g. https://www.boutiqaat.com/en-kw/women/
    """
    return f"{BASE_DOMAIN}/{lang}-{country}/{gender}/"
