# ============================================================
# test_cart.py — Cart regression tests.
#
# TEST FLOW:
#   test_add_two_products_and_remove_one
#     Register → Login →
#     Search "perfume" → Add to cart (retry up to 3 products if sold out) →
#     Search "puff" → Add to cart (retry up to 3 products if sold out) →
#     Go to cart → Remove one item → Verify 1 item remains
#
# Run: pytest tests/test_cart.py -v
# ============================================================

import pytest
from data.test_data import CART_DATA
from pages.registration_page import RegistrationPage
from pages.search_page import SearchPage
from pages.cart_page import CartPage
from utils.logger import log

MAX_PRODUCT_ATTEMPTS = 3


def _search_and_add_to_cart(search, cart, term):
    """
    Search for a term and add a product to cart.
    If the first product is sold out, tries the next product (up to MAX_PRODUCT_ATTEMPTS).
    """
    for attempt in range(MAX_PRODUCT_ATTEMPTS):
        search.search(term)
        search.select_product_by_index(attempt)

        if not cart.is_sold_out():
            cart.add_to_cart()
            log(f"'{term}' product (index {attempt}) added to cart", "PASS")
            return

        log(f"'{term}' product (index {attempt}) is sold out, trying next", "WARN")

    # If all attempts exhausted, fail with clear message
    raise AssertionError(
        f"All {MAX_PRODUCT_ATTEMPTS} products for '{term}' are sold out"
    )


@pytest.mark.cart
@pytest.mark.parametrize("data", CART_DATA, ids=[d["id"] for d in CART_DATA])
def test_add_two_products_and_remove_one(page, data):
    """
    Test cart functionality with multiple products:
    1. Search "perfume" and add first available product to cart
    2. Search "puff" and add first available product to cart
    3. Go to cart page
    4. Remove one item using trash icon
    5. Verify 1 item remains in cart
    """
    reg = RegistrationPage(page)
    assert reg.register_and_login(data), "Registration/Login failed"

    search = SearchPage(page)
    cart = CartPage(page)

    # ── STEP 1: SEARCH AND ADD PERFUME ────────────────────────────
    _search_and_add_to_cart(search, cart, "perfume")

    # ── STEP 2: SEARCH AND ADD PUFF ──────────────────────────────
    _search_and_add_to_cart(search, cart, "puff")

    # ── STEP 3: GO TO CART PAGE ──────────────────────────────────
    cart.open_cart(data["lang"], data["country"])
    page.wait_for_timeout(3_000)
    assert "/checkout/cart" in page.url, \
        f"[{data['id']}] Cart page did not load — current URL: {page.url}"
    log("Opened cart page", "INFO")

    # ── STEP 4: REMOVE ONE ITEM USING TRASH ICON ─────────────────
    trash_buttons = page.locator("button:has(i.icon-trash)")
    trash_count = trash_buttons.count()
    log(f"Found {trash_count} items in cart with trash icons", "INFO")
    assert trash_count == 2, (
        f"[{data['id']}] Expected 2 items in cart before removal, "
        f"but found {trash_count}"
    )

    trash_buttons.nth(1).click()
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(3_000)
    log("Item removed from cart", "INFO")

    # Reload cart for fresh DOM
    cart.open_cart(data["lang"], data["country"])
    page.wait_for_timeout(3_000)
    assert "/checkout/cart" in page.url, \
        f"[{data['id']}] Cart page did not reload after removal — URL: {page.url}"
    log("Cart reloaded after item removal", "INFO")

    # ── STEP 5: VERIFY 1 ITEM REMAINS IN CART ────────────────────
    remaining_items = page.locator("button:has(i.icon-trash)").count()
    log(f"Remaining items in cart: {remaining_items}", "INFO")
    assert remaining_items == 1, (
        f"[{data['id']}] Expected 1 item in cart after removing 1 of 2, "
        f"but found {remaining_items}"
    )
    log("Cart operation completed - Added 2 items, removed 1, verified 1 remains", "PASS")
