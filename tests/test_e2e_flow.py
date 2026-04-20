# ============================================================
# test_e2e_flow.py — Complete end-to-end regression tests.
#
# TWO TEST SCENARIOS:
#
#   test_complete_flow  — Happy path
#     Register → Login → Search → Product → Cart →
#     Address → Payment page → PAY → Wait for success
#
#   test_cancel_flow    — Cancel / failure path
#     Register → Login → Search → Product → Cart →
#     Address → Payment page → PAY → Cancel on KNET gateway →
#     Capture OOPS screen details (all key-values) + screenshot
#
# PAYMENT FLOW:
#   1. Dismiss "Free Delivery" modal (blocks PAY button)
#   2. Select payment method (KNET by default)
#   3. Select wallet if available
#   4. Click PAY → redirected to KNET gateway (kpay.com.kw)
#   5a. Happy path  → wait for /paymentsuccess URL
#   5b. Cancel path → click Cancel on gateway → /paymentfail/ →
#                     capture all key-values + screenshot
#
# Run all:           pytest tests/test_e2e_flow.py -v
# Run happy path:    pytest tests/test_e2e_flow.py -k "complete"
# Run cancel path:   pytest tests/test_e2e_flow.py -k "cancel"
# ============================================================

import pytest
from data.test_data import E2E_DATA, E2E_CANCEL_DATA, ADDRESS_DATA
from pages.registration_page import RegistrationPage
from pages.search_page import SearchPage
from pages.cart_page import CartPage
from pages.address_page import AddressPage
from pages.payment_page import PaymentPage
from utils.logger import log


def _run_up_to_payment(page, data):
    """
    Shared helper — runs steps 1-8 (register through payment method selection).
    Returns a ready PaymentPage instance.
    Extracted to avoid duplicating setup in both test functions.
    """
    # ── STEP 1: REGISTER VIA API + LOGIN VIA UI ───────────────────
    # Creates account via REST API (no T&C flakiness),
    # then logs in via the login page to get a browser session.
    reg = RegistrationPage(page)
    assert reg.register_and_login(data), (
        f"[{data['id']}] Registration/Login failed — check screenshots/"
    )
    log("Session active — proceeding to purchase flow", "INFO")

    # ── STEP 2 & 3: SEARCH + SELECT PRODUCT ──────────────────────
    search = SearchPage(page)
    search.search(data["search_term"])
    search.select_first_product()

    # ── STEP 4 & 5: ADD TO CART + OPEN CART ──────────────────────
    cart = CartPage(page)
    cart.add_to_cart()
    cart.open_cart(data["lang"], data["country"])

    # ── STEP 6: FILL ADDRESS FORM ─────────────────────────────────
    # Fetches the address dataset by key from ADDRESS_DATA in test_data.py
    addr_data = ADDRESS_DATA[data["address_key"]]
    address = AddressPage(page)
    address.open(data["lang"], data["country"], data["gender"])
    address.fill_address(addr_data)
    address.save_address()

    # ── STEP 7: CONTINUE TO PAYMENT ──────────────────────────────
    address.continue_to_payment(data["gender"])

    # ── STEP 8: DISMISS MODAL + SELECT PAYMENT METHOD ────────────
    payment = PaymentPage(page)
    payment.dismiss_modal()              # Close "Free Delivery" popup
    payment.select_payment_method()      # KNET by default
    payment.select_wallet()              # Skipped if no wallet balance

    return payment


# ------------------------------------------------------------------
# HAPPY PATH — complete purchase flow
# ------------------------------------------------------------------
@pytest.mark.regression
@pytest.mark.parametrize(
    "data", E2E_DATA, ids=[d["id"] for d in E2E_DATA]
)
def test_complete_flow(page, data):
    """
    Full happy-path regression:
    Register → Login → Search → Product → Cart →
    Address → Payment → PAY → Wait for success page.

    NOTE: This test requires manual payment completion.
    The test will wait at the payment gateway for you to complete
    the payment manually. If payment is not completed within the
    timeout period, the test will be marked as skipped rather than failed.
    """
    payment = _run_up_to_payment(page, data)

    # ── STEP 9: PLACE ORDER + WAIT FOR SUCCESS ────────────────────
    payment.place_order()
    
    # Try to wait for payment success, but skip if timeout (manual payment not completed)
    try:
        payment.wait_for_payment_success()
    except AssertionError as e:
        if "timed out" in str(e).lower() or "timeout" in str(e).lower():
            pytest.skip(f"Payment not completed manually within timeout period: {e}")
        else:
            raise


# ------------------------------------------------------------------
# CANCEL / FAILURE PATH — cancel on KNET gateway, capture oops screen
# ------------------------------------------------------------------
@pytest.mark.regression
@pytest.mark.parametrize(
    "data", E2E_CANCEL_DATA, ids=[d["id"] for d in E2E_CANCEL_DATA]
)
def test_cancel_flow(page, data):
    """
    Cancel-path regression:
    Register → Login → Search → Product → Cart →
    Address → Payment → PAY → Cancel on KNET gateway →
    Capture OOPS screen (all key-values + screenshot).

    This test PASSES when the cancellation is handled correctly
    and all failure details are captured from the oops screen.
    """
    payment = _run_up_to_payment(page, data)

    # ── STEP 9: PLACE ORDER (navigate to KNET gateway) ───────────
    payment.place_order()

    # ── STEP 10: CANCEL ON KNET GATEWAY ──────────────────────────
    # Clicks input#cancel on kpay.com.kw
    # Redirects back to boutiqaat /checkout/paymentfail/
    payment.cancel_payment()

    # ── STEP 11: CAPTURE OOPS SCREEN DETAILS ─────────────────────
    # Reads all key-values from URL params + page text
    # Saves a full-page screenshot to screenshots/payment_failed.png
    failure_details = payment.capture_failure_details()

    # Assert the key fields are present in the failure details
    assert failure_details.get("transactionStatus") or \
           failure_details.get("Transaction Status"), \
        "Transaction Status missing from failure details"

    assert failure_details.get("paymentError") or \
           failure_details.get("paymentid"), \
        "Payment error details missing from failure screen"

    log("Cancel flow completed — all failure details captured", "PASS")
