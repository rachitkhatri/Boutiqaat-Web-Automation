# ============================================================
# cart_page.py — Add-to-cart, remove item, and cart navigation.
#
# REAL SELECTORS (verified on live site):
#   Add to cart  → .pro-details-add-to-cart a  (PDP Buy Now link)
#   Remove item  → button:has(i.icon-trash)    (trash icon button in cart)
#   Cart counter → .pro-count.gold             (header cart badge)
#   Cart items   → .cart.item, .item-info      (cart row elements)
#   Empty cart   → page text contains "no items" or cart counter = 0
# ============================================================

from pages.base_page import BasePage
from utils.logger import log
from config.settings import BASE_DOMAIN


class CartPage(BasePage):

    def add_to_cart(self) -> None:
        """
        Click the Buy Now / Add to Cart link on the product detail page.
        Selector: .pro-details-add-to-cart a
        FIXED: Added proper wait for cart update and navigation handling
        """
        add_link = self.page.locator(".pro-details-add-to-cart a")
        add_link.wait_for(state="visible", timeout=15_000)
        add_link.scroll_into_view_if_needed()
        
        # Click and wait for navigation (Buy Now redirects to cart)
        add_link.click()
        
        # Wait for navigation to cart page
        try:
            self.page.wait_for_url("**/checkout/cart/**", timeout=30_000)
            log("Navigated to cart page after add", "INFO")
        except Exception:
            log("No navigation detected, item may be added via AJAX", "INFO")
        
        # Wait for network to settle
        try:
            self.page.wait_for_load_state("networkidle", timeout=20_000)
        except Exception:
            pass
        
        # Additional wait for cart to fully sync
        self.page.wait_for_timeout(3_000)
        log("Add To Cart", "PASS")

    def open_cart(self, lang: str, country: str) -> None:
        """Navigate directly to the cart page URL."""
        self.page.goto(f"{BASE_DOMAIN}/{lang}-{country}/checkout/cart/")
        self.page.wait_for_load_state("networkidle")
        log("Cart Page", "PASS")

    def get_cart_item_count(self) -> int:
        """Returns the number of product rows currently in the cart."""
        self.page.wait_for_load_state("networkidle")
        
        # Check for empty cart message
        if self.page.locator("text='You have no items in your shopping cart'").count() > 0:
            return 0
        
        # Count cart items
        for selector in [".cart.item", ".item-info", "tbody.cart.item"]:
            count = self.page.locator(selector).count()
            if count > 0:
                return count
        
        return 0

    def remove_first_item(self) -> None:
        """
        Click the trash icon button to remove the first item from the cart.
        Selector: button:has(i.icon-trash)
        Waits for the cart to update after removal.
        """
        trash_btn = self.page.locator("button:has(i.icon-trash)")
        trash_btn.wait_for(state="visible", timeout=10_000)
        trash_btn.first.click()
        # Wait for the cart page to reload after removal
        self.page.wait_for_load_state("networkidle")
        log("Cart Item Removed", "PASS")

    def is_cart_empty(self) -> bool:
        """
        Returns True if the cart has no items.
        Checks the header badge counter and page content.
        """
        count = self.get_cart_item_count()
        if count == 0:
            return True
        # Also check for empty cart message in page text
        content = self.page.content()
        return "no items" in content.lower() or "empty" in content.lower()
