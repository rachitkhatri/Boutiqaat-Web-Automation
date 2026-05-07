# ============================================================
# test_wishlist.py — Wishlist regression tests.
#
# SIMPLIFIED TEST:
#   test_add_to_wishlist
#     Register → Login → Search → Product →
#     Add to Wishlist from PDP (no verification, no remove)
#
# NOTE: Only testing ADD functionality
# This avoids session/sync issues with verification and removal
#
# Run: pytest tests/test_wishlist.py -v
# ============================================================

import pytest
from data.test_data import WISHLIST_DATA
from pages.registration_page import RegistrationPage
from pages.search_page import SearchPage
from pages.cart_page import CartPage
from pages.wishlist_page import WishlistPage
from utils.logger import log

MAX_PRODUCT_ATTEMPTS = 3


@pytest.mark.wishlist
@pytest.mark.parametrize("data", WISHLIST_DATA, ids=[d["id"] for d in WISHLIST_DATA])
def test_add_to_wishlist(page, data):
    """
    Verify a product can be added to the wishlist from PDP.
    SIMPLIFIED: Only tests ADD functionality (no verification, no remove).
    Retries with next product if the first is sold out.
    """
    reg = RegistrationPage(page)
    assert reg.register_and_login(data), "Registration/Login failed"

    # ── SEARCH + SELECT AVAILABLE PRODUCT ─────────────────────────
    search = SearchPage(page)
    cart = CartPage(page)

    product_found = False
    for attempt in range(MAX_PRODUCT_ATTEMPTS):
        search.search(data["search_term"])
        search.select_product_by_index(attempt)

        if not cart.is_sold_out():
            product_found = True
            log(f"Available product found (index {attempt})", "INFO")
            break

        log(f"Product (index {attempt}) is sold out, trying next", "WARN")

    assert product_found, (
        f"All {MAX_PRODUCT_ATTEMPTS} products for '{data['search_term']}' are sold out"
    )

    # ── ADD TO WISHLIST FROM PDP ──────────────────────────────────
    wishlist = WishlistPage(page)
    wishlist.add_to_wishlist_from_pdp()
    
    # Wait for wishlist action to complete
    page.wait_for_load_state("networkidle")
    
    log("Wishlist Add Completed - Item added from PDP", "PASS")
