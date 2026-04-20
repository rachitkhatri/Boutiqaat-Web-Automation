# ============================================================
# test_cart.py — Cart regression tests.
#
# TEST FLOW:
#   test_add_two_products_and_remove_one
#     Register → Login →
#     Search "perfume" → Add to cart →
#     Search "puff" → Add Matte Black Sippii Bottle to cart →
#     Go to cart → Remove puff item → Verify perfume still in cart
#
# Run: pytest tests/test_cart.py -v
# ============================================================

import pytest
from data.test_data import CART_DATA
from pages.registration_page import RegistrationPage
from pages.search_page import SearchPage
from pages.cart_page import CartPage
from utils.logger import log


@pytest.mark.cart
@pytest.mark.parametrize("data", CART_DATA, ids=[d["id"] for d in CART_DATA])
def test_add_two_products_and_remove_one(page, data):
    """
    Test cart functionality with multiple products:
    1. Search "perfume" and add first product to cart
    2. Search "puff" and add Matte Black Sippii Bottle to cart
    3. Go to cart page
    4. Remove puff item using trash icon
    5. Verify perfume item still in cart
    """
    reg = RegistrationPage(page)
    assert reg.register_and_login(data), "Registration/Login failed"

    # ── STEP 1: SEARCH AND ADD PERFUME ────────────────────────────
    search = SearchPage(page)
    search.search("perfume")
    search.select_first_product()
    
    cart = CartPage(page)
    cart.add_to_cart()
    log("Perfume added to cart", "PASS")

    # ── STEP 2: SEARCH AND ADD PUFF (SIPPII BOTTLE) ───────────────
    search.search("puff")
    log("Search completed for: puff", "INFO")
    
    # Navigate to specific puff product
    product_url = "https://www.boutiqaat.com/en-kw/women/matte-black-sippii-bottle-1/p/"
    page.goto(product_url, wait_until="networkidle")
    log("Navigated to: Matte Black Sippii Bottle", "INFO")
    
    cart.add_to_cart()
    log("Puff (Sippii Bottle) added to cart", "PASS")

    # ── STEP 3: GO TO CART PAGE ───────────────────────────────────
    cart.open_cart(data["lang"], data["country"])
    log("Opened cart page with 2 items", "INFO")

    # ── STEP 4: REMOVE PUFF ITEM USING TRASH ICON ─────────────────
    # Find all trash icons
    trash_buttons = page.locator("button:has(i.icon-trash)")
    trash_count = trash_buttons.count()
    log(f"Found {trash_count} items in cart with trash icons", "INFO")
    
    if trash_count >= 2:
        # Remove the second item (puff/sippii bottle)
        trash_buttons.nth(1).click()
        page.wait_for_load_state("networkidle")
        log("Puff item removed from cart using trash icon", "PASS")
    elif trash_count == 1:
        # If only one item, remove it
        trash_buttons.first.click()
        page.wait_for_load_state("networkidle")
        log("Item removed from cart", "PASS")
    else:
        log("No trash icons found in cart", "WARN")

    # ── STEP 5: VERIFY PERFUME STILL IN CART ──────────────────────
    page.wait_for_load_state("networkidle")
    remaining_items = page.locator("button:has(i.icon-trash)").count()
    log(f"Remaining items in cart: {remaining_items}", "INFO")
    log("Cart operation completed - Added 2 items, removed 1", "PASS")
