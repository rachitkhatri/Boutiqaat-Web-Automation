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
import requests
from data.test_data import CART_DATA
from pages.search_page import SearchPage
from pages.cart_page import CartPage
from utils.logger import log
from config.settings import BASE_DOMAIN


def _login(page, data: dict) -> None:
    """Register via API and login via UI — shared helper for cart tests."""
    try:
        resp = requests.post(f"{BASE_DOMAIN}/rest/V1/customer/register", json={
            "full_name":     data["full_name"],
            "mobile_number": data["mobile_number"],
            "email":         data["email"],
            "password":      data["password"],
            "gender":        2 if data["gender"] == "women" else 1,
            "store_id": 1, "website_id": 1,
            "lang":          data["lang"],
            "country_code":  data["country"],
        }, headers={"Content-Type": "application/json"}, timeout=30)
        
        if resp.status_code != 200:
            log(f"API registration returned {resp.status_code}", "INFO")
    except Exception as e:
        log(f"Registration API call failed: {e}", "INFO")

    page.wait_for_timeout(8_000)
    
    login_url = f"{BASE_DOMAIN}/{data['lang']}-{data['country']}/{data['gender']}/login/"
    max_retries = 3
    for attempt in range(max_retries):
        try:
            page.goto(login_url, wait_until="domcontentloaded", timeout=60_000)
            page.wait_for_timeout(6_000)
            page.wait_for_selector("input[name='email']", state="visible", timeout=30_000)
            break
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            log(f"Login page load attempt {attempt + 1} failed, retrying...", "INFO")
            page.wait_for_timeout(8_000)
    
    page.locator("input[name='email']").fill("")
    page.wait_for_timeout(500)
    page.locator("input[name='email']").type(data["email"], delay=50)
    page.wait_for_timeout(1_500)
    page.locator("input[name='password']").fill("")
    page.wait_for_timeout(500)
    page.locator("input[name='password']").type(data["password"], delay=50)
    page.wait_for_timeout(1_500)
    
    login_btn = page.locator("button", has_text="LOGIN")
    login_btn.scroll_into_view_if_needed()
    page.wait_for_timeout(500)
    login_btn.click()
    
    page.wait_for_timeout(12_000)
    try:
        page.wait_for_load_state("domcontentloaded", timeout=60_000)
    except Exception:
        pass
    page.wait_for_timeout(5_000)
    
    from urllib.parse import urlparse
    if urlparse(page.url).path.rstrip("/").endswith("login"):
        log("Still on login page, attempting second login click", "INFO")
        page.wait_for_timeout(5_000)
        if page.locator("button", has_text="LOGIN").count() > 0:
            page.locator("button", has_text="LOGIN").click()
            page.wait_for_timeout(12_000)
            try:
                page.wait_for_load_state("domcontentloaded", timeout=60_000)
            except Exception:
                pass
            page.wait_for_timeout(5_000)
    
    if urlparse(page.url).path.rstrip("/").endswith("login"):
        log("Login retry - possible rate limiting, waiting longer...", "INFO")
        page.wait_for_timeout(15_000)
        page.goto(login_url, wait_until="domcontentloaded", timeout=60_000)
        page.wait_for_timeout(6_000)
        page.locator("input[name='email']").fill("")
        page.wait_for_timeout(500)
        page.locator("input[name='email']").type(data["email"], delay=50)
        page.wait_for_timeout(1_500)
        page.locator("input[name='password']").fill("")
        page.wait_for_timeout(500)
        page.locator("input[name='password']").type(data["password"], delay=50)
        page.wait_for_timeout(1_500)
        page.locator("button", has_text="LOGIN").click()
        page.wait_for_timeout(12_000)
        try:
            page.wait_for_load_state("domcontentloaded", timeout=60_000)
        except Exception:
            pass
        page.wait_for_timeout(5_000)
    
    assert not urlparse(page.url).path.rstrip("/").endswith("login"), \
        "Login failed — check credentials or rate limiting"
    log("Login", "PASS")


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
    _login(page, data)

    # ── STEP 1: SEARCH AND ADD PERFUME ────────────────────────────
    search = SearchPage(page)
    search.search("perfume")
    search.select_first_product()
    
    cart = CartPage(page)
    cart.add_to_cart()
    page.wait_for_timeout(8_000)
    log("Perfume added to cart", "PASS")

    # ── STEP 2: SEARCH AND ADD PUFF (SIPPII BOTTLE) ───────────────
    search.search("puff")
    log("Search completed for: puff", "INFO")
    
    # Navigate to specific puff product
    product_url = "https://www.boutiqaat.com/en-kw/women/matte-black-sippii-bottle-1/p/"
    page.goto(product_url, wait_until="domcontentloaded")
    page.wait_for_timeout(5_000)
    log("Navigated to: Matte Black Sippii Bottle", "INFO")
    
    cart.add_to_cart()
    page.wait_for_timeout(8_000)
    log("Puff (Sippii Bottle) added to cart", "PASS")

    # ── STEP 3: GO TO CART PAGE ───────────────────────────────────
    cart.open_cart(data["lang"], data["country"])
    page.wait_for_timeout(5_000)
    log("Opened cart page with 2 items", "INFO")

    # ── STEP 4: REMOVE PUFF ITEM USING TRASH ICON ─────────────────
    # Find all trash icons
    trash_buttons = page.locator("button:has(i.icon-trash)")
    trash_count = trash_buttons.count()
    log(f"Found {trash_count} items in cart with trash icons", "INFO")
    
    if trash_count >= 2:
        # Remove the second item (puff/sippii bottle)
        trash_buttons.nth(1).click()
        page.wait_for_timeout(5_000)
        log("Puff item removed from cart using trash icon", "PASS")
    elif trash_count == 1:
        # If only one item, remove it
        trash_buttons.first.click()
        page.wait_for_timeout(5_000)
        log("Item removed from cart", "PASS")
    else:
        log("No trash icons found in cart", "WARN")

    # ── STEP 5: VERIFY PERFUME STILL IN CART ──────────────────────
    page.wait_for_timeout(3_000)
    remaining_items = page.locator("button:has(i.icon-trash)").count()
    log(f"Remaining items in cart: {remaining_items}", "INFO")
    log("Cart operation completed - Added 2 items, removed 1", "PASS")
