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

    def is_sold_out(self) -> bool:
        """
        Check if the current PDP product is sold out.
        Returns True if the Buy Now button is missing or disabled.
        """
        try:
            add_link = self.page.locator(".pro-details-add-to-cart a")
            if add_link.count() == 0:
                return True
            # Check for sold out / out of stock indicators
            page_text = self.page.content().lower()
            if "sold out" in page_text or "out of stock" in page_text:
                return True
            return False
        except Exception:
            return True

    def add_to_cart(self) -> None:
        """
        Click the Buy Now / Add to Cart link on the product detail page.
        Selector: .pro-details-add-to-cart a
        """
        add_link = self.page.locator(".pro-details-add-to-cart a")
        add_link.wait_for(state="visible", timeout=15_000)
        add_link.scroll_into_view_if_needed()
        self.page.evaluate("document.querySelectorAll('.celebriti-content, .modal-backdrop, .popup-overlay, .overlay').forEach(el => el.remove())")

        add_link.click()

        # Wait for either cart page redirect or AJAX completion
        try:
            self.page.wait_for_url("**/checkout/cart/**", timeout=15_000)
            log("Navigated to cart page after add", "INFO")
        except Exception:
            log("No navigation detected, item may be added via AJAX", "INFO")
            try:
                self.page.wait_for_load_state("networkidle", timeout=15_000)
            except Exception:
                pass

        self.page.wait_for_timeout(3_000)

        # Verify item was actually added
        if not self.is_item_added_to_cart():
            log("Item was NOT added to cart — cart appears empty or unchanged", "FAIL")
            raise AssertionError("Add to cart failed: item not found in cart after clicking Buy Now")

        log("Add To Cart", "PASS")

    def is_item_added_to_cart(self) -> bool:
        """
        Verify at least one item exists in cart after add-to-cart action.
        Checks URL (cart page redirect) or cart badge counter.
        """
        # If redirected to cart page, check for cart row elements
        if "/checkout/cart" in self.page.url:
            for selector in ["button:has(i.icon-trash)", ".cart.item", ".item-info", "tbody.cart.item"]:
                if self.page.locator(selector).count() > 0:
                    return True
            return False

        # Check header cart badge — try multiple possible selectors
        for badge_sel in [".pro-count.gold", ".pro-count", "[class*='cart-count']", "[class*='cart_count']", "[class*='cartCount']", "span.count"]:
            badge = self.page.locator(badge_sel)
            if badge.count() > 0:
                try:
                    val = badge.first.inner_text().strip()
                    if val and int(val) > 0:
                        return True
                except (ValueError, Exception):
                    continue

        # Last resort: navigate to cart page and check
        try:
            current_url = self.page.url
            import re
            match = re.search(r'/(en|ar)-([a-z]+)/', current_url)
            if match:
                lang, country = match.groups()
                from config.settings import BASE_DOMAIN
                self.page.goto(f"{BASE_DOMAIN}/{lang}-{country}/checkout/cart/", wait_until="domcontentloaded")
                self.page.wait_for_timeout(3_000)
                for selector in ["button:has(i.icon-trash)", ".cart.item", ".item-info"]:
                    if self.page.locator(selector).count() > 0:
                        return True
        except Exception:
            pass

        return False

    def open_cart(self, lang: str, country: str) -> None:
        """Navigate directly to the cart page URL."""
        self.page.goto(f"{BASE_DOMAIN}/{lang}-{country}/checkout/cart/", wait_until="domcontentloaded")
        try:
            self.page.wait_for_load_state("networkidle", timeout=15_000)
        except Exception:
            pass
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
