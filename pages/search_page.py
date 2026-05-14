# ============================================================
# search_page.py — Search bar interaction and product selection.
#
# REAL SELECTORS (verified against live site):
#   Search icon  → i.s-open  (inside .searchWrapper)
#   Search input → input[placeholder='Search for products, categories, ...']
#                  (this input appears AFTER clicking the icon — different
#                   from the static .search-wrap-1 input which stays hidden)
#   Autocomplete → #Products a  (appears ~2s after typing)
#   Results page → a[href*='/p/']  (fallback after pressing Enter)
#   Results URL  → /catalogsearch/?q=<term>
# ============================================================

from pages.base_page import BasePage
from utils.logger import log


# Selector for the search input that appears after clicking the icon
_SEARCH_INPUT = "input[placeholder='Search for products, categories, ...']"


class SearchPage(BasePage):

    def search(self, term: str) -> None:
        """
        Click the search icon to reveal the input, then type the term.
        Navigates to the homepage first if the search icon is not present
        (e.g. immediately after login the page may not have the header).
        """
        # Ensure the search icon is present — navigate to homepage if not
        if self.page.locator("i.s-open").count() == 0:
            from config.settings import BASE_DOMAIN
            # Extract locale from current URL e.g. /en-kw/women/
            url = self.page.url
            import re
            match = re.search(r'/(en|ar)-([a-z]+)/([a-z]+)/', url)
            if match:
                lang, country, gender = match.groups()
                # FIX: boutiqaat keeps background requests alive causing networkidle
                # to timeout after 60s. Use domcontentloaded then attempt networkidle
                # as best-effort settle wait.
                self.page.goto(
                    f"{BASE_DOMAIN}/{lang}-{country}/{gender}/",
                    wait_until="domcontentloaded"
                )
                try:
                    self.page.wait_for_load_state("networkidle", timeout=15_000)
                except Exception:
                    pass  # Safe to continue — DOM is already loaded
            else:
                # FIX: Same domcontentloaded fix for reload.
                self.page.reload(wait_until="domcontentloaded")
                try:
                    self.page.wait_for_load_state("networkidle", timeout=15_000)
                except Exception:
                    pass  # Safe to continue — DOM is already loaded
            self.page.wait_for_timeout(2_000)

        # Click the magnifier icon to open the search overlay
        self.page.locator("i.s-open").click()

        # Wait for the overlay input — retry the click once if it doesn't appear
        try:
            self.page.wait_for_selector(_SEARCH_INPUT, state="visible", timeout=10_000)
        except Exception:
            # Overlay may not have opened — dismiss any blocking overlay and retry
            self.page.evaluate("document.querySelectorAll('.modal-backdrop, .overlay, .popup-overlay').forEach(el => el.remove())")
            self.page.wait_for_timeout(1_000)
            self.page.locator("i.s-open").click()
            self.page.wait_for_selector(_SEARCH_INPUT, state="visible", timeout=15_000)

        search_input = self.page.locator(_SEARCH_INPUT)
        self.type_like_user(search_input, term)

        # Wait for autocomplete suggestions to load
        self.page.wait_for_timeout(2_500)
        log("Search Done", "PASS")

    def select_first_product(self) -> None:
        """
        Click the first product from the autocomplete dropdown (#Products).
        Falls back to pressing Enter → navigating to results page → clicking
        the first product link if autocomplete doesn't appear.
        """
        try:
            # Autocomplete dropdown — appears inside #Products after typing
            self.page.wait_for_selector("#Products a", timeout=6_000)
            self.page.locator("#Products a").first.click()
        except Exception:
            # Fallback: submit search, wait for results page, click first product
            self.page.locator(_SEARCH_INPUT).press("Enter")
            self.page.wait_for_load_state("networkidle")
            self.page.wait_for_timeout(2_000)
            # Product links on results page contain /p/ in the href
            self.page.locator("a[href*='/p/']").first.click()

        self.page.wait_for_load_state("networkidle")
        log("Product Selected", "PASS")

    def select_product_by_index(self, index: int) -> None:
        """
        Select a product by index from autocomplete or search results.
        Falls back to results page if autocomplete doesn't have enough items.

        Args:
            index: 0-based index of the product to select
        """
        try:
            self.page.wait_for_selector("#Products a", timeout=6_000)
            products = self.page.locator("#Products a")
            if products.count() > index:
                products.nth(index).click()
            else:
                # Not enough autocomplete results, use search results page
                self.page.locator(_SEARCH_INPUT).press("Enter")
                self.page.wait_for_load_state("networkidle")
                self.page.wait_for_timeout(2_000)
                self.page.locator("a[href*='/p/']").nth(index).click()
        except Exception:
            self.page.locator(_SEARCH_INPUT).press("Enter")
            self.page.wait_for_load_state("networkidle")
            self.page.wait_for_timeout(2_000)
            results = self.page.locator("a[href*='/p/']")
            if results.count() > index:
                results.nth(index).click()
            else:
                results.first.click()

        self.page.wait_for_load_state("networkidle")
        log(f"Product Selected (index {index})", "PASS")
