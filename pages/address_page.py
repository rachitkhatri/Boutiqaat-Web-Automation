# ============================================================
# address_page.py — Checkout address page interactions.
#
# REAL FORM FIELDS (verified on live site):
#   #firstname        — full name
#   #region_area      — area dropdown (132 options, select FIRST)
#   #addr_block       — block dropdown (loads after area is selected)
#   #addr_street      — street
#   #addr_avenue      — avenue (optional)
#   #addr_villa       — house / building number
#   #addr_floornumber — floor number (optional)
#   #addr_flatenumber — flat number (optional)
#   #telephone        — phone number
#   #notes            — delivery notes (optional)
#
# ADDRESS MANAGEMENT SELECTORS (verified on live site):
#   Address page URL  → /en-kw/checkout/customeraddress/
#   Edit button       → a text='Edit Address'
#   Add New button    → text='Add New Address'
#   SAVE button       → button text='SAVE'
#   Cancel button     → button text='Cancel'
#   CONTINUE button   → button text='CONTINUE TO PAYMENT'
#
# NOTE: /en-kw/customer/address/ redirects to login — use
#       /en-kw/checkout/customeraddress/ for all address management.
# ============================================================

from pages.base_page import BasePage
from utils.logger import log
from config.settings import BASE_DOMAIN


class AddressPage(BasePage):

    def open(self, lang: str, country: str, gender: str) -> None:
        """
        Navigate to the checkout address page.
        Requires an active logged-in session with items in the cart.
        """
        self.page.goto(
            f"{BASE_DOMAIN}/{lang}-{country}/checkout/customeraddress/",
            wait_until="domcontentloaded",
        )
        try:
            self.page.wait_for_load_state("networkidle", timeout=15_000)
        except Exception:
            pass
        log("Address Page", "PASS")

    def open_management(self, lang: str, country: str, gender: str) -> None:
        """
        Navigate to the address management page (no cart required).
        Uses the checkout address URL which works without cart items.
        """
        self.page.goto(
            f"{BASE_DOMAIN}/{lang}-{country}/checkout/customeraddress/",
            wait_until="domcontentloaded",
        )
        try:
            self.page.wait_for_load_state("networkidle", timeout=15_000)
        except Exception:
            pass
        log("Address Management Page", "PASS")

    def _fill_form(self, data: dict) -> None:
        """Internal helper — fills all address form fields."""
        try:
            self.page.wait_for_selector("#firstname", state="visible", timeout=30_000)
        except Exception:
            add_new_btn = self.page.locator("text=Add New Address")
            if add_new_btn.count() > 0:
                add_new_btn.click()
                self.page.wait_for_selector("#firstname", state="visible", timeout=20_000)
            self.page.wait_for_selector("#firstname", state="visible", timeout=20_000)
        
        self.page.locator("#firstname").fill(data["full_name"])
        self.page.select_option("#region_area", label=data["area"])
        # Dynamic dropdown — block options load after area selection
        self.page.wait_for_timeout(2_000)
        self.page.select_option("#addr_block", value=data["block"])
        self.page.locator("#addr_street").fill(data["street"])
        if data.get("avenue"):
            self.page.locator("#addr_avenue").fill(data["avenue"])
        self.page.locator("#addr_villa").fill(data["villa"])
        if data.get("floor"):
            self.page.locator("#addr_floornumber").fill(data["floor"])
        if data.get("flat"):
            self.page.locator("#addr_flatenumber").fill(data["flat"])
        self.page.locator("#telephone").fill(data["telephone"])
        if data.get("notes"):
            self.page.locator("#notes").fill(data["notes"])

    def fill_address(self, data: dict) -> None:
        """Fill the address form that is already visible on page load."""
        self._fill_form(data)
        log("Address Form Filled", "PASS")

    def save_address(self) -> None:
        """Click SAVE and wait for the page to confirm."""
        self.page.locator("button", has_text="SAVE").click()
        self.page.wait_for_load_state("networkidle")
        # Wait for React to re-render the saved address view
        self.page.wait_for_timeout(3_000)
        log("Address Saved", "PASS")

    def add_new_address(self, data: dict) -> None:
        """
        Click 'Add New Address', fill the form, and save.
        Used when a saved address already exists and you want to add another.
        """
        add_btn = self.page.locator("text=Add New Address")
        add_btn.wait_for(state="visible", timeout=10_000)
        add_btn.click()
        self.page.wait_for_selector("#firstname", state="visible", timeout=15_000)
        self._fill_form(data)
        self.save_address()
        log("New Address Added", "PASS")

    def edit_address(self, data: dict) -> None:
        """
        Click 'Edit Address' on the existing address, update fields, save.
        Selector: a text='Edit Address'
        """
        # Reload page to ensure fresh state
        try:
            self.page.reload(wait_until="domcontentloaded")
            try:
                self.page.wait_for_load_state("networkidle", timeout=15_000)
            except Exception:
                pass
        except Exception:
            pass
        
        # Try multiple selectors for edit button
        edit_selectors = [
            "a:has-text('Edit Address')",
            "a:has-text('Edit')",
            "button:has-text('Edit')",
            "[class*='edit']",
        ]
        
        edit_btn = None
        for selector in edit_selectors:
            btn = self.page.locator(selector)
            if btn.count() > 0:
                edit_btn = btn
                break
        
        if edit_btn is None:
            log("Edit button not found - address may already be in edit mode", "INFO")
            # Try to fill form directly if already in edit mode
            if self.page.locator("#firstname").count() > 0:
                self._fill_form(data)
                self.save_address()
                log("Address Updated (direct form fill)", "PASS")
                return
            raise Exception("Edit button not found and form not visible")
        
        edit_btn.first.wait_for(state="visible", timeout=20_000)
        edit_btn.first.click()
        # Wait for form to appear
        self.page.wait_for_selector("#firstname", state="visible", timeout=30_000)
        # Clear and refill the form
        self._fill_form(data)
        self.save_address()
        log("Address Updated", "PASS")

    def has_saved_address(self) -> bool:
        """
        Returns True if at least one saved address exists.
        Checks for the CONTINUE TO PAYMENT button which only appears
        when an address is saved.
        """
        return self.page.locator("button", has_text="CONTINUE TO PAYMENT").count() > 0

    def has_edit_button(self) -> bool:
        """Returns True if the Edit Address button is visible."""
        try:
            self.page.wait_for_timeout(5_000)
            # Reload page to ensure fresh state
            try:
                self.page.reload(wait_until="domcontentloaded")
                try:
                    self.page.wait_for_load_state("networkidle", timeout=15_000)
                except Exception:
                    pass
            except Exception:
                pass
            
            # Try multiple selectors for edit button
            edit_selectors = [
                "a:has-text('Edit Address')",
                "button:has-text('Edit')",
                "a:has-text('Edit')",
                "[class*='edit']",
                "a[href*='edit']",
            ]
            for selector in edit_selectors:
                if self.page.locator(selector).count() > 0:
                    return True
            return False
        except Exception:
            return False

    def continue_to_payment(self, gender: str) -> None:
        """Click CONTINUE TO PAYMENT and wait for the payment page."""
        ctp = self.page.locator("button", has_text="CONTINUE TO PAYMENT")
        ctp.wait_for(state="visible", timeout=10_000)
        ctp.click()
        self.page.wait_for_url(f"**/{gender}/checkout/payment/**", timeout=20_000)
        log("Payment Page", "PASS")
