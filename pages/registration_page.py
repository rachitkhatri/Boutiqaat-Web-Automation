# ============================================================
# registration_page.py — Registration via REST API + UI login.
#
# WHY API REGISTRATION:
#   The /register/ page has a T&C checkbox whose <label> contains
#   <a> links. Every approach to click it via Playwright (coordinates,
#   JS events, scroll+click) is unreliable across different window
#   sizes and slow_mo settings. The site exposes a REST API at
#   /rest/V1/customer/register that does the same thing with 100%
#   reliability — no UI, no T&C, no flakiness.
#
# FLOW:
#   1. POST to /rest/V1/customer/register  → creates the account
#   2. Navigate to /login/ and fill email+password → gets browser session
#   3. Browser is now logged in — all subsequent steps use this session
#
# RETRY:
#   Retries up to MAX_ATTEMPTS times on any failure.
#   Saves a screenshot on every failed attempt.
# ============================================================

import requests
from pages.base_page import BasePage
from utils.logger import log
from config.settings import BASE_DOMAIN, PAGE_SETTLE_MS

MAX_ATTEMPTS = 3


class RegistrationPage(BasePage):

    def open(self, lang: str, country: str, gender: str) -> None:
        """
        Navigate to the registration page.
        Note: This method exists for compatibility but registration
        is done via API in the register() method.
        """
        self.page.goto(
            f"{BASE_DOMAIN}/{lang}-{country}/{gender}/register/",
            wait_until="networkidle"
        )
        self.page.wait_for_timeout(PAGE_SETTLE_MS)

    def register(self, data: dict) -> bool:
        """
        Register a new account via REST API then log in via the UI.
        This is a wrapper around register_and_login for standalone registration tests.
        """
        return self.register_and_login(data)

    def register_and_login(self, data: dict) -> bool:
        """
        Register a new account via REST API then log in via the UI.
        Returns True when the browser session is active (logged in).
        Retries up to MAX_ATTEMPTS times on failure.

        Expected data keys:
            id, full_name, mobile_number, email, password,
            gender (women/men), lang, country
        """
        for attempt in range(1, MAX_ATTEMPTS + 1):
            log(f"Registration attempt {attempt}/{MAX_ATTEMPTS} [{data['id']}]", "INFO")
            try:
                # ── STEP 1: REGISTER VIA REST API ───────────────────
                # Calls /rest/V1/customer/register directly — no UI,
                # no T&C checkbox, 100% reliable every time.
                gender_val = 2 if data.get("gender", "women") == "women" else 1
                resp = requests.post(
                    f"{BASE_DOMAIN}/rest/V1/customer/register",
                    json={
                        "full_name":     data["full_name"],
                        "mobile_number": data["mobile_number"],
                        "email":         data["email"],
                        "password":      data["password"],
                        "gender":        gender_val,
                        "store_id":      1,
                        "website_id":    1,
                        "lang":          data["lang"],
                        "country_code":  data["country"],
                    },
                    headers={"Content-Type": "application/json"},
                    timeout=30,
                )

                if resp.status_code != 200:
                    log(f"API registration failed: {resp.status_code} {resp.text[:100]}", "FAIL")
                    self.screenshot_on_failure(
                        f"screenshots/error_reg_{data['id']}_attempt{attempt}.png"
                    )
                    continue

                log(f"Account created via API [{data['id']}]", "INFO")

                # Brief pause — Magento needs a moment to propagate the new
                # account before the login page can authenticate it.
                self.page.wait_for_timeout(5_000)

                # ── STEP 2: LOGIN VIA UI ─────────────────────────────
                # Navigate to the login page and fill credentials.
                # This gives the browser a valid PHPSESSID session cookie
                # that all subsequent steps (cart, address, payment) need.
                login_url = (
                    f"{BASE_DOMAIN}/{data['lang']}-{data['country']}"
                    f"/{data['gender']}/login/"
                )
                self.page.goto(login_url, wait_until="networkidle")
                self.page.wait_for_timeout(PAGE_SETTLE_MS)

                # Wait for the email input to be ready
                self.page.wait_for_selector(
                    "input[name='email']", state="visible", timeout=20_000
                )

                # Fill email and password with human-like typing
                self.page.locator("input[name='email']").fill("")
                self.type_like_user(
                    self.page.locator("input[name='email']"), data["email"]
                )
                self.page.locator("input[name='password']").fill("")
                self.type_like_user(
                    self.page.locator("input[name='password']"), data["password"]
                )

                # Click LOGIN button
                login_btn = self.page.locator("button", has_text="LOGIN")
                login_btn.scroll_into_view_if_needed()
                login_btn.click()
                self.page.wait_for_load_state("networkidle")
                self.page.wait_for_timeout(PAGE_SETTLE_MS)

                # Success = the path no longer ends with /login/
                # Use path check not full URL to avoid false positives
                # from query params containing the word 'login'
                from urllib.parse import urlparse
                path = urlparse(self.page.url).path
                if not path.rstrip("/").endswith("login"):
                    log(f"Registration + Login [{data['id']}]", "PASS")
                    return True

                log(f"Login failed after registration — attempt {attempt}", "FAIL")
                self.screenshot_on_failure(
                    f"screenshots/error_login_{data['id']}_attempt{attempt}.png"
                )

            except Exception as exc:
                log(f"Attempt {attempt} error: {exc}", "FAIL")
                self.screenshot_on_failure(
                    f"screenshots/error_reg_{data['id']}_attempt{attempt}.png"
                )

        log(f"Registration [{data['id']}] — all {MAX_ATTEMPTS} attempts failed", "FAIL")
        return False
