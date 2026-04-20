# ============================================================
# payment_page.py — Payment page interactions.
#
# REAL PAGE STRUCTURE (verified on live site):
#
#   BOUTIQAAT PAYMENT PAGE:
#     URL: /{lang}-{country}/{gender}/checkout/payment/
#     Modal: "Enjoy Free Delivery!" popup — MUST be dismissed first
#     Payment methods (radio name="optradio"):
#       #myfatoorah_kn      → KNET (default, Kuwait debit)
#       #myfatoorah_vm      → Credit Card (Visa/Master)
#       #tabby_installments → Tabby (4 interest-free)
#       #amex               → American Express
#       #deema_payment      → Deema
#     PAY button: <a id="btnStatus">PAY</a>
#
#   KNET GATEWAY (kpay.com.kw):
#     The PAY button navigates to the KNET gateway page.
#     Cancel button: input#cancel  (value="Cancel", onclick="cancelPage()")
#     The gateway is the MAIN page (not an iframe).
#
#   OOPS / FAILURE SCREEN (boutiqaat.com/en-kw/checkout/paymentfail/):
#     After cancel, redirected back to boutiqaat with all details in URL:
#       invoiceReference, orderId, transactionStatus, authorizationId,
#       transactionDate, customerName, referenceId, paymentError,
#       createdDate, paymentid, invoiceId, customerMobile, paymentGateway
#     Page shows:
#       Title:            "OOPS!"
#       Message:          "Payment has been declined..."
#       Transaction Status, Payment ID, Transaction ID,
#       Track ID, Reference NO, Date
#     CSS classes: .titel (heading), .payment (details block)
# ============================================================

import urllib.parse
from pages.base_page import BasePage
from utils.logger import log
from config.settings import PAYMENT_TIMEOUT, SCREENSHOTS_DIR


class PaymentPage(BasePage):

    def dismiss_modal(self) -> None:
        """
        Dismiss the "Enjoy Free Delivery!" promotional modal.
        This modal intercepts all pointer events — it MUST be closed
        before any other element on the payment page can be clicked.
        """
        modal = self.page.locator("div.modal.show")
        if modal.count() > 0 and modal.first.is_visible():
            ok_btn = self.page.locator("div.modal.show button", has_text="OK")
            if ok_btn.count() > 0:
                ok_btn.first.click()
                # Wait for the modal animation to finish
                self.page.wait_for_selector(
                    "div.modal.show", state="hidden", timeout=5_000
                )
                log("Promotional Modal Dismissed", "PASS")
        else:
            log("No Modal Present", "INFO")

    def select_payment_method(self, method_id: str = "myfatoorah_kn") -> None:
        """
        Select a payment method radio button.

        Available IDs (verified on live site):
            myfatoorah_kn      → KNET (default, Kuwait debit card)
            myfatoorah_vm      → Credit Card (Visa / Mastercard)
            tabby_installments → Tabby (4 interest-free payments)
            amex               → American Express
            deema_payment      → Deema
        """
        radio = self.page.locator(f"#{method_id}")
        if radio.count() > 0:
            radio.click()
            log(f"Payment Method Selected: {method_id}", "PASS")
        else:
            log(f"Payment method #{method_id} not found — using default", "SKIP")

    def select_wallet(self) -> None:
        """
        Tick the wallet checkbox if available.
        Skipped silently if not present — not a failure.
        """
        try:
            wallet = self.page.locator("#use-wallet")
            if wallet.count() > 0 and wallet.is_visible():
                wallet.check()
                log("Wallet Selected", "PASS")
            else:
                log("Wallet", "SKIP")
        except Exception:
            log("Wallet", "SKIP")

    def place_order(self) -> None:
        """
        Click the PAY button and wait for the KNET gateway redirect.
        Uses expect_navigation to properly capture the redirect to kpay.com.kw.
        """
        pay_btn = self.page.locator("#btnStatus")
        pay_btn.wait_for(state="visible", timeout=10_000)
        pay_btn.scroll_into_view_if_needed()

        # expect_navigation captures the redirect to the KNET gateway
        with self.page.expect_navigation(timeout=30_000):
            pay_btn.click()

        self.page.wait_for_load_state("networkidle")
        log("Redirected to Payment Gateway", "PASS")

    def cancel_payment(self) -> None:
        """
        Click the Cancel button on the KNET gateway page.

        KNET gateway selector: input#cancel (id="cancel", value="Cancel")
        The button is temporarily DISABLED by JS during page load and
        payment processing. We must wait for it to become enabled before
        clicking — otherwise the click is silently ignored.

        After cancel, boutiqaat redirects to /checkout/paymentfail/
        with all transaction details in the URL query string.
        """
        # Wait for the KNET gateway page to fully load
        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_timeout(2_000)

        # Screenshot of the gateway before cancelling
        self.page.screenshot(
            path=f"{SCREENSHOTS_DIR}knet_gateway.png", full_page=True
        )
        log("KNET Gateway Screenshot Saved", "INFO")

        # Wait for #cancel to exist AND be enabled
        # The button is disabled by JS during page init — must wait for enabled state
        self.page.wait_for_selector(
            "#cancel:not([disabled])", timeout=20_000
        )
        self.page.wait_for_timeout(500)

        cancel_btn = self.page.locator("#cancel")
        if cancel_btn.count() > 0:
            cancel_btn.click()
            log("Cancel Button Clicked on KNET Gateway", "PASS")
        else:
            # Fallback — find by value attribute
            fallback = self.page.locator("input[value='Cancel']:not([disabled])")
            if fallback.count() > 0:
                fallback.first.click()
                log("Cancel Button Clicked (fallback by value)", "PASS")
            else:
                log("Cancel button not found on gateway", "FAIL")
                return

        # Wait for redirect back to boutiqaat paymentfail page
        self.page.wait_for_url("**/checkout/paymentfail/**", timeout=30_000)
        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_timeout(2_000)

    def capture_failure_details(self) -> dict:
        """
        Capture all key-value details from the OOPS / failure screen.

        The failure URL contains all transaction details as query params:
            invoiceReference, orderId, transactionStatus, authorizationId,
            transactionDate, customerName, referenceId, paymentError,
            createdDate, paymentid, invoiceId, customerMobile, paymentGateway

        The page also shows structured text in .titel and .payment divs.

        Returns a dict of all captured key-value pairs.
        Saves a full-page screenshot to screenshots/payment_failed.png.
        """
        # Parse all query parameters from the failure URL
        parsed   = urllib.parse.urlparse(self.page.url)
        params   = urllib.parse.parse_qs(parsed.query)
        # Flatten single-value lists
        details  = {k: v[0] if len(v) == 1 else v for k, v in params.items()}

        # Also read the structured text from the page
        page_details = {}
        try:
            # Main heading — "OOPS!"
            heading = self.page.locator(".titel").first
            if heading.count() > 0:
                page_details["heading"] = heading.inner_text().strip()

            # Transaction details block — "Transaction Status: ERROR" etc.
            payment_block = self.page.locator(".payment").first
            if payment_block.count() > 0:
                block_text = payment_block.inner_text().strip()
                # Parse each "Key: Value" line
                for line in block_text.split("\n"):
                    if ":" in line:
                        key, _, val = line.partition(":")
                        page_details[key.strip()] = val.strip()
        except Exception:
            pass

        # Merge URL params + page text into one dict
        all_details = {**details, **page_details}

        # Log every key-value pair for the test report
        log("=== PAYMENT FAILURE DETAILS ===", "FAIL")
        for key, value in all_details.items():
            log(f"  {key}: {value}", "INFO")

        # Save full-page screenshot of the oops screen
        screenshot_path = f"{SCREENSHOTS_DIR}payment_failed.png"
        self.page.screenshot(path=screenshot_path, full_page=True)
        log(f"Oops Screen Screenshot Saved → {screenshot_path}", "INFO")

        return all_details

    def wait_for_payment_success(self) -> None:
        """
        Wait for the payment success URL after manual payment.
        Handles three outcomes:
          1. User completes payment  → /paymentsuccess  → PASS
          2. Gateway expires/cancel  → /paymentfail     → captures details, raises AssertionError
          3. Browser closed manually → TargetClosedError → raises clear AssertionError
        """
        print("\n\U0001f4b3 Complete payment manually in the browser window...")
        try:
            # Wait for either success OR failure URL — whichever comes first
            self.page.wait_for_url(
                lambda url: "paymentsuccess" in url or "paymentfail" in url,
                timeout=PAYMENT_TIMEOUT,
            )
        except Exception as exc:
            # Covers TargetClosedError (browser closed) and TimeoutError
            raise AssertionError(
                f"Payment did not complete — browser may have been closed or timed out: {exc}"
            )

        # Check which URL we landed on
        if "paymentsuccess" in self.page.url:
            log("Payment Success", "PASS")
        else:
            # Gateway expired or was cancelled — capture all details
            details = self.capture_failure_details()
            raise AssertionError(
                f"Payment failed/cancelled — "
                f"paymentError: {details.get('paymentError', 'unknown')} | "
                f"orderId: {details.get('orderId', 'unknown')}"
            )
