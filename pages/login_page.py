# ============================================================
# login_page.py — Login page actions.
#
# REAL SELECTORS (verified on live site):
#   email    → input[name='email']   (class="email-id")
#   password → input[name='password']
#   button   → button (text "LOGIN")
#
# URL: /{lang}-{country}/{gender}/login/
#      e.g. /en-kw/women/login/
# ============================================================

from pages.base_page import BasePage
from utils.logger import log
from config.settings import BASE_DOMAIN, PAGE_SETTLE_MS


class LoginPage(BasePage):

    def open(self, lang: str, country: str, gender: str) -> None:
        """Navigate to the login page for the given locale and gender."""
        self.page.goto(
            f"{BASE_DOMAIN}/{lang}-{country}/{gender}/login/",
            wait_until="domcontentloaded",
        )
        try:
            self.page.wait_for_load_state("networkidle", timeout=15_000)
        except Exception:
            pass
        self.page.wait_for_timeout(PAGE_SETTLE_MS)
        
        # Dismiss any overlays that appeared after page load
        self.dismiss_overlays()

    def login(self, email: str, password: str) -> bool:
        """
        Fill credentials and submit the login form.
        Returns True if login succeeded (URL changed away from /login/).
        Returns False if still on login page (wrong credentials).
        """
        # Wait for the email field — name="email", class="email-id"
        self.page.wait_for_selector(
            "input[name='email']", state="visible", timeout=20_000
        )
        
        # Dismiss overlays before interacting
        self.dismiss_overlays()

        self.type_like_user(self.page.locator("input[name='email']"), email)
        self.type_like_user(self.page.locator("input[name='password']"), password)

        # LOGIN button text is uppercase on this site
        self.page.locator("button", has_text="LOGIN").click()
        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_timeout(PAGE_SETTLE_MS)

        if "login" in self.page.url:
            log("Login", "FAIL")
            return False

        log("Login", "PASS")
        return True
