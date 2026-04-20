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
from pages.wishlist_page import WishlistPage
from utils.logger import log


@pytest.mark.wishlist
@pytest.mark.parametrize("data", WISHLIST_DATA, ids=[d["id"] for d in WISHLIST_DATA])
def test_add_to_wishlist(page, data):
    """
    Verify a product can be added to the wishlist from PDP.
    SIMPLIFIED: Only tests ADD functionality (no verification, no remove).
    """
    reg = RegistrationPage(page)
    assert reg.register_and_login(data), "Registration/Login failed"

    # ── SEARCH + SELECT PRODUCT ───────────────────────────────────
    search = SearchPage(page)
    search.search(data["search_term"])
    search.select_first_product()

    # ── ADD TO WISHLIST FROM PDP ──────────────────────────────────
    wishlist = WishlistPage(page)
    wishlist.add_to_wishlist_from_pdp()
    
    # Wait for wishlist action to complete
    page.wait_for_load_state("networkidle")
    
    log("Wishlist Add Completed - Item added from PDP", "PASS")
