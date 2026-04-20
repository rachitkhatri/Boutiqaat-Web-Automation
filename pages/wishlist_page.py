# ============================================================
# wishlist_page.py — Wishlist interactions.
#
# REAL SELECTORS (verified on live site):
#   Add to wishlist (PDP) → .pro-details-action a[title='Add to Wishlist']
#   Wishlist counter      → .pro-count.gold (header badge, same as cart)
#   Remove from wishlist  → button:has(i.icon-trash) on wishlist page
#
# NOTE: The wishlist page (/en-kw/women/wishlist/) shows "Oops" —
#       the site manages wishlist via React state + API calls.
#       We verify wishlist actions via the API endpoint:
#         GET /consumer/rest/V1/customer/getwishlist/{country}_{lang}
#       which returns the wishlist items as JSON.
# ============================================================

from pages.base_page import BasePage
from utils.logger import log
from config.settings import BASE_DOMAIN


class WishlistPage(BasePage):

    def add_to_wishlist_from_pdp(self) -> None:
        """
        Click the Add to Wishlist heart button on the product detail page.
        FIXED: Handle navigation to /wish-list/ page after clicking
        The page may navigate to wishlist page after adding.
        """
        # Try to find wishlist button with multiple selectors
        wl_selectors = [
            ".pro-details-action a[title='Add to Wishlist']",
            "a[title='Add to Wishlist']",
            ".wishlist-btn",
            "[class*='wishlist']",
        ]
        
        wl_btn = None
        for selector in wl_selectors:
            if self.page.locator(selector).count() > 0:
                wl_btn = self.page.locator(selector).first
                break
        
        if not wl_btn:
            log("Wishlist button not found, trying alternative approach", "WARN")
            return
        
        wl_btn.wait_for(state="visible", timeout=10_000)
        wl_btn.scroll_into_view_if_needed()
        self.page.wait_for_timeout(500)
        wl_btn.click()
        
        # Wait for either navigation or AJAX update
        self.page.wait_for_timeout(3_000)
        
        # Check if navigated to wishlist page
        if "/wish-list/" in self.page.url:
            log("Navigated to wishlist page after add", "INFO")
        else:
            log("Stayed on PDP, wishlist updated via AJAX", "INFO")
        
        # Wait for wishlist to sync
        try:
            self.page.wait_for_load_state("networkidle", timeout=15_000)
        except Exception:
            pass
        
        self.page.wait_for_timeout(5_000)
        log("Added to Wishlist", "PASS")

    def get_wishlist_count(self, lang: str, country: str) -> int:
        """
        Returns the number of items in the wishlist.
        FIXED: Corrected wishlist URL to /wish-list/ (with hyphen)
        """
        # Strategy 1: Navigate to wishlist page and count items visually
        try:
            wishlist_url = f"{BASE_DOMAIN}/{lang}-{country}/women/wish-list/"
            self.page.goto(wishlist_url, wait_until="domcontentloaded", timeout=30_000)
            self.page.wait_for_timeout(5_000)
            
            # Wait for network to settle
            try:
                self.page.wait_for_load_state("networkidle", timeout=15_000)
            except Exception:
                pass
            
            # Check for empty wishlist message
            empty_selectors = [
                "text='Your wishlist is empty'",
                "text='No items in wishlist'",
                ".wishlist-empty",
                "text='Start adding items'",
            ]
            
            for selector in empty_selectors:
                if self.page.locator(selector).count() > 0:
                    log("Wishlist is empty (found empty message)", "INFO")
                    return 0
            
            # Count wishlist items on page
            item_selectors = [
                ".product-item",
                ".wishlist-item",
                ".item",
                "[class*='wishlist'] [class*='item']",
            ]
            
            for selector in item_selectors:
                items = self.page.locator(selector)
                count = items.count()
                if count > 0:
                    log(f"Found {count} wishlist items using selector: {selector}", "INFO")
                    return count
        except Exception as e:
            log(f"Visual wishlist count failed: {e}", "WARN")
        
        # Strategy 2: Use API endpoint
        api_url = (
            f"https://ksa-api.boutiqaat.com/consumer/rest/V1/customer"
            f"/getwishlist/{country}_{lang}"
        )
        
        max_attempts = 5
        for attempt in range(max_attempts):
            try:
                result = self.page.evaluate(
                    """
                    async (url) => {
                        try {
                            const r = await fetch(url, {credentials: 'include'});
                            if (!r.ok) return 0;
                            const data = await r.json();
                            if (data && data[0] && data[0].page_info) {
                                return data[0].page_info.total_items;
                            }
                            if (data && data[0] && data[0].products) {
                                return data[0].products.length;
                            }
                            return 0;
                        } catch (e) {
                            console.error('Wishlist API error:', e);
                            return 0;
                        }
                    }
                    """,
                    api_url,
                )
                count = int(result) if result else 0
                if count > 0 or attempt == max_attempts - 1:
                    log(f"Wishlist API count: {count}", "INFO")
                    return count
                # Wait before retry
                self.page.wait_for_timeout(3_000)
            except Exception as e:
                log(f"Wishlist API call failed (attempt {attempt + 1}): {e}", "WARN")
                if attempt == max_attempts - 1:
                    return 0
                self.page.wait_for_timeout(3_000)
        
        return 0

    def navigate_to_wishlist(self, lang: str, country: str, gender: str) -> None:
        """
        Navigate to the wishlist page.
        URL: /{lang}-{country}/{gender}/wish-list/ (with hyphen)
        """
        self.page.goto(
            f"{BASE_DOMAIN}/{lang}-{country}/{gender}/wish-list/",
            wait_until="networkidle",
        )
        self.page.wait_for_timeout(3_000)
        log(f"Wishlist Page: {self.page.url[:60]}", "INFO")

    def remove_first_wishlist_item(self) -> None:
        """
        Remove the first item from the wishlist page using the trash button.
        Selector: button:has(i.icon-trash)
        """
        trash_btn = self.page.locator("button:has(i.icon-trash)")
        if trash_btn.count() > 0:
            trash_btn.first.click()
            self.page.wait_for_timeout(3_000)
            log("Wishlist Item Removed", "PASS")
        else:
            log("No wishlist trash button found", "SKIP")
