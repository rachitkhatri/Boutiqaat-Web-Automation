# ============================================================
# base_page.py — Shared low-level actions used by every page.
#
# PURPOSE:
#   Parent class for all page objects. Common behaviour like
#   typing, overlay dismissal, and screenshots is written once
#   here and inherited by every page class.
#
# PATTERN:
#   Page Object Model (POM) — each web page = one class.
#   All page classes inherit BasePage:
#     class LoginPage(BasePage): ...
#     class CartPage(BasePage):  ...
#
# USAGE:
#   from pages.base_page import BasePage
#   class MyPage(BasePage):
#       def do_something(self):
#           self.page.click("#btn")  # self.page = Playwright page
# ============================================================

from utils.logger import log, log_error, log_screenshot  # Logging helpers
from config.settings import FAILURE_SCREENSHOT             # Default screenshot path


class BasePage:
    """Base class that every page object inherits from."""

    def __init__(self, page):
        # Store the Playwright page object — all child pages use self.page
        # to interact with the browser (click, fill, goto, etc.)
        self.page = page

    def dismiss_overlays(self) -> None:
        """
        Remove popups/modals that block element interactions.

        Boutiqaat shows celebrity popups, modal backdrops, and overlays
        that intercept pointer events. This JS removes them so the
        actual page elements become clickable.
        """
        try:
            # Run JavaScript in the browser to hide/remove overlay elements
            self.page.evaluate("""
                document.querySelectorAll(
                    '.celebriti-content, .modal-backdrop, .popup-overlay, .overlay'
                ).forEach(el => {
                    el.style.display = 'none';  // Hide the element
                    el.remove();                 // Remove from DOM entirely
                });
            """)
            self.page.wait_for_timeout(300)  # Brief pause for DOM to settle
        except Exception:
            pass  # Silently continue — overlay removal is best-effort

    def type_like_user(self, locator, text: str, delay: int = 80) -> None:
        """
        Simulate realistic human typing into an input field.

        Args:
            locator: Playwright locator pointing to the input element
            text:    Text to type
            delay:   Milliseconds between each keystroke (default 80ms)

        Why not just .fill()?
            Some sites validate on keypress events. Typing character
            by character triggers those events like a real user would.
        """
        try:
            self.dismiss_overlays()          # Clear any blocking overlays first
            try:
                locator.click(timeout=5000)  # Focus the input field
            except Exception:
                locator.click(force=True)    # Force-click if overlay still blocks
            locator.fill("")                 # Clear any existing text
            locator.type(text, delay=delay)  # Type each character with delay
        except Exception as e:
            log_error(e, f"Failed to type text: {text[:20]}...")
            raise

    def screenshot_on_failure(self, path: str = FAILURE_SCREENSHOT) -> None:
        """
        Save a full-page PNG screenshot when a step fails.

        Args:
            path: File path to save the screenshot (default: error.png)
        """
        try:
            self.page.screenshot(path=path)      # Capture current page state
            log_screenshot(path, "Test failure")  # Log the screenshot path
        except Exception:
            pass  # Don't crash if screenshot fails (e.g. browser already closed)
