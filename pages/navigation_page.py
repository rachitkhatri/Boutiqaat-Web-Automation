# ============================================================
# navigation_page.py — Navigation and category page verification.
#
# REAL SELECTORS (verified on live site):
#   Product items  → .celebriti-wrapper  (174 items on category pages)
#   Brand items    → .celebriti-wrapper  (same selector on brands page)
#   Category links → nav a[href*='/c/'] or nav a[href*='/l/']
#
# VERIFIED URLS (all return 174 items with .celebriti-wrapper):
#   Homepage     → /en-kw/women/
#   Makeup       → /en-kw/women/makeup/c/
#   Fragrance    → /en-kw/women/fragrance/c/
#   Skincare     → /en-kw/women/skincare/c/
#   Brands       → /en-kw/women/brands/
# ============================================================

from pages.base_page import BasePage
from utils.logger import log
from config.settings import BASE_DOMAIN


class NavigationPage(BasePage):

    def navigate_to(self, url: str, name: str) -> None:
        """Navigate to a URL and wait for the page to load."""
        try:
            self.page.goto(url, wait_until="domcontentloaded", timeout=60_000)
            try:
                self.page.wait_for_load_state("networkidle", timeout=15_000)
            except Exception:
                log(f"{name} — networkidle timed out, continuing", "WARN")
        except Exception:
            log(f"{name} — domcontentloaded timed out, retrying", "WARN")
            self.page.goto(url, wait_until="domcontentloaded", timeout=60_000)
            self.page.wait_for_timeout(5_000)
        log(f"Navigated to {name}: {self.page.url[:60]}", "INFO")

    def get_product_count(self) -> int:
        """
        Returns the number of product/brand cards on the current page.
        Selector: .celebriti-wrapper — used for all product and brand listings.
        """
        return self.page.locator(".celebriti-wrapper").count()

    def get_page_title(self) -> str:
        """Returns the current page title."""
        return self.page.title()

    def verify_page_loads(self, url: str, name: str, min_items: int = 1) -> bool:
        """
        Navigate to a page and verify it loads with at least min_items products.
        Returns True if the page loaded correctly with items.
        """
        self.navigate_to(url, name)
        count = self.get_product_count()
        title = self.get_page_title()

        log(f"{name} — title: {title[:50]!r}, items: {count}", "INFO")

        if count >= min_items:
            log(f"{name} loaded correctly ({count} items)", "PASS")
            return True
        else:
            log(f"{name} loaded but has only {count} items (expected >= {min_items})", "FAIL")
            self.screenshot_on_failure(f"screenshots/fail_nav_{name.replace(' ', '_')}.png")
            return False
