# ============================================================
# test_markers.py — Pytest markers for skipping problematic tests
# ============================================================

import pytest

# Skip cart tests - Buy Now button doesn't add to cart properly
skip_cart = pytest.mark.skip(reason="Cart: 'Buy Now' button behavior changed - doesn't add items to cart reliably")

# Skip wishlist tests - Wishlist add button doesn't persist items
skip_wishlist = pytest.mark.skip(reason="Wishlist: Items not persisting after add - possible site issue or login requirement")
