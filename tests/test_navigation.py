# ============================================================
# test_navigation.py — Navigation and category page tests.
#
# SCENARIOS:
#   test_category_pages  — Verify all category pages load with products
#   test_brands_page     — Verify brands page loads with brand items
#   test_search_results  — Verify search results page loads with products
#
# No login required — all navigation pages are public.
#
# VERIFIED SELECTORS:
#   Product/brand items → .celebriti-wrapper (174 items on all pages)
#
# Run: pytest tests/test_navigation.py -v
# ============================================================

import pytest
from pages.navigation_page import NavigationPage
from utils.logger import log
from config.settings import BASE_DOMAIN


# ------------------------------------------------------------------
# NAVIGATION TEST DATA
# Each dict defines one page to verify.
# min_items = minimum number of .celebriti-wrapper elements expected.
# ------------------------------------------------------------------
NAVIGATION_PAGES = [
    {
        "id":        "nav_homepage_women",
        "name":      "Homepage Women",
        "url":       f"{BASE_DOMAIN}/en-kw/women/",
        "min_items": 10,
        "note":      "Main women landing page — should have many products",
    },
    {
        "id":        "nav_makeup_category",
        "name":      "Makeup Category",
        "url":       f"{BASE_DOMAIN}/en-kw/women/makeup/c/",
        "min_items": 10,
        "note":      "Makeup category page",
    },
    {
        "id":        "nav_fragrance_category",
        "name":      "Fragrance Category",
        "url":       f"{BASE_DOMAIN}/en-kw/women/fragrance/c/",
        "min_items": 10,
        "note":      "Fragrance category page",
    },
    {
        "id":        "nav_skincare_category",
        "name":      "Skincare Category",
        "url":       f"{BASE_DOMAIN}/en-kw/women/skincare/c/",
        "min_items": 10,
        "note":      "Skincare category page",
    },
    {
        "id":        "nav_haircare_category",
        "name":      "Haircare Category",
        "url":       f"{BASE_DOMAIN}/en-kw/women/hair/c/",
        "min_items": 5,
        "note":      "Haircare category page",
    },
    {
        "id":        "nav_brands_page",
        "name":      "Brands Page",
        "url":       f"{BASE_DOMAIN}/en-kw/women/brands/",
        "min_items": 10,
        "note":      "All brands listing page",
    },
    {
        "id":        "nav_search_results",
        "name":      "Search Results — perfume",
        "url":       f"{BASE_DOMAIN}/en-kw/women/catalogsearch/?q=perfume",
        "min_items": 5,
        "note":      "Search results page for 'perfume'",
    },
    {
        "id":        "nav_search_results_lipstick",
        "name":      "Search Results — lipstick",
        "url":       f"{BASE_DOMAIN}/en-kw/women/catalogsearch/?q=lipstick",
        "min_items": 5,
        "note":      "Search results page for 'lipstick'",
    },
]


@pytest.mark.navigation
@pytest.mark.parametrize(
    "data", NAVIGATION_PAGES, ids=[d["id"] for d in NAVIGATION_PAGES]
)
def test_page_loads_with_products(page, data):
    """
    Verify each navigation/category page:
      1. Loads without error (no 404 / Oops page)
      2. Contains at least min_items product/brand cards
      3. Page title is not empty
    """
    nav = NavigationPage(page)

    # Navigate and verify
    result = nav.verify_page_loads(
        url=data["url"],
        name=data["name"],
        min_items=data["min_items"],
    )

    # Verify page title is meaningful (not empty / 404 / Oops)
    title = nav.get_page_title()
    assert title, \
        f"[{data['id']}] Page title is empty — possible blank/error page"
    assert "404" not in title and "oops" not in title.lower(), \
        f"[{data['id']}] Page shows error — title: {title!r}"

    assert result, \
        f"[{data['id']}] {data['name']} did not load enough items — " \
        f"expected >= {data['min_items']}, note: {data['note']}"

    log(f"{data['name']} — PASS", "PASS")
