# ============================================================
# base_page.py — Shared low-level actions used by every page.
# All page classes inherit from BasePage so common behaviour
# (typing, clicking, screenshots) is written only once.
# ============================================================

from utils.logger import log, log_error, log_screenshot
from config.settings import FAILURE_SCREENSHOT


class BasePage:
    def __init__(self, page):
        # Store the Playwright page object so all child pages can use it
        self.page = page

    def dismiss_overlays(self) -> None:
        """Remove overlays/popups that might block interactions."""
        try:
            self.page.evaluate("""
                document.querySelectorAll('.celebriti-content, .modal-backdrop, .popup-overlay, .overlay').forEach(el => {
                    el.style.display = 'none';
                    el.remove();
                });
            """)
            self.page.wait_for_timeout(300)
        except Exception:
            pass

    def type_like_user(self, locator, text: str, delay: int = 80) -> None:
        """Simulates realistic human typing."""
        try:
            self.dismiss_overlays()
            try:
                locator.click(timeout=5000)
            except Exception:
                locator.click(force=True)
            locator.fill("")
            locator.type(text, delay=delay)
        except Exception as e:
            log_error(e, f"Failed to type text: {text[:20]}...")
            raise

    def screenshot_on_failure(self, path: str = FAILURE_SCREENSHOT) -> None:
        """Saves a PNG when a step fails."""
        try:
            self.page.screenshot(path=path)
            log_screenshot(path, "Test failure")
        except Exception:
            pass
