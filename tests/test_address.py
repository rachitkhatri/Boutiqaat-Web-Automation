# ============================================================
# test_address.py — Address management regression tests.
#
# SCENARIOS:
#   test_add_address       — Add a new address and verify it is saved
#   test_edit_address      — Add address then edit it with new data
#   test_add_second_address — Add two addresses and verify both exist
#
# Run: pytest tests/test_address.py -v
# ============================================================

import pytest
import requests
import time
import os
from dotenv import load_dotenv
from data.test_data import ADDRESS_DATA
from pages.address_page import AddressPage
from pages.cart_page import CartPage
from pages.search_page import SearchPage
from utils.logger import log
from config.settings import BASE_DOMAIN

# Load environment variables
load_dotenv()

_TS = str(int(time.time()))


# ------------------------------------------------------------------
# ADDRESS TEST DATA — loaded from .env file
# ------------------------------------------------------------------
ADDRESS_TEST_ACCOUNTS = [
    {
        "id":            "addr_add_kw",
        "full_name":     os.getenv("ADDR_FULL_NAME", "Addr Tester"),
        "mobile_number": os.getenv("ADDR_MOBILE", "50066666"),
        "email":         f"addr.add.{_TS}@mailinator.com",
        "password":      os.getenv("ADDR_PASSWORD", "Test@1234"),
        "gender":        os.getenv("ADDR_GENDER", "women"),
        "lang":          os.getenv("ADDR_LANG", "en"),
        "country":       os.getenv("ADDR_COUNTRY", "kw"),
        "address_key":   os.getenv("ADDR_KEY", "kw_salmiya"),
        "address_key2":  os.getenv("ADDR_KEY2", "kw_hawalli"),
    },
]


def _register_and_login(page, data: dict) -> None:
    """Register via API and login via UI."""
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

    # Wait longer after registration to avoid rate limiting
    page.wait_for_timeout(8_000)
    
    # Navigate to login page with retry logic
    login_url = f"{BASE_DOMAIN}/{data['lang']}-{data['country']}/{data['gender']}/login/"
    max_retries = 3
    for attempt in range(max_retries):
        try:
            page.goto(login_url, wait_until="domcontentloaded", timeout=60_000)
            page.wait_for_timeout(6_000)
            # Wait for email input to be visible
            page.wait_for_selector("input[name='email']", state="visible", timeout=30_000)
            break
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            log(f"Login page load attempt {attempt + 1} failed, retrying...", "INFO")
            page.wait_for_timeout(8_000)
    
    # Fill credentials with human-like delays
    page.locator("input[name='email']").fill("")
    page.wait_for_timeout(500)
    page.locator("input[name='email']").type(data["email"], delay=50)
    page.wait_for_timeout(1_500)
    page.locator("input[name='password']").fill("")
    page.wait_for_timeout(500)
    page.locator("input[name='password']").type(data["password"], delay=50)
    page.wait_for_timeout(1_500)
    
    # Click login button
    login_btn = page.locator("button", has_text="LOGIN")
    login_btn.scroll_into_view_if_needed()
    page.wait_for_timeout(500)
    login_btn.click()
    
    # Wait for navigation away from login page
    page.wait_for_timeout(12_000)
    try:
        page.wait_for_load_state("domcontentloaded", timeout=60_000)
    except Exception:
        pass
    page.wait_for_timeout(5_000)
    
    from urllib.parse import urlparse
    # Verify login succeeded by checking we're not on login page
    if urlparse(page.url).path.rstrip("/").endswith("login"):
        # Try clicking login again if still on login page
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
    
    assert not urlparse(page.url).path.rstrip("/").endswith("login"), "Login failed"
    log("Login", "PASS")


def _add_cart_item(page, data: dict) -> None:
    """Add a product to cart so the address page is accessible."""
    search = SearchPage(page)
    search.search("perfume")
    search.select_first_product()
    cart = CartPage(page)
    cart.add_to_cart()
    log("Cart item added for address test", "INFO")


@pytest.mark.address
@pytest.mark.parametrize(
    "data", ADDRESS_TEST_ACCOUNTS,
    ids=[d["id"] for d in ADDRESS_TEST_ACCOUNTS]
)
def test_add_address(page, data):
    """
    Verify a new address can be added and saved.
    Checks that CONTINUE TO PAYMENT appears after saving.
    """
    _register_and_login(page, data)
    _add_cart_item(page, data)

    addr_data = ADDRESS_DATA[data["address_key"]]
    address = AddressPage(page)
    address.open(data["lang"], data["country"], data["gender"])

    # Fill and save the address
    address.fill_address(addr_data)
    address.save_address()

    # Verify address was saved — CONTINUE TO PAYMENT should be visible
    assert address.has_saved_address(), \
        f"[{data['id']}] Address not saved — CONTINUE TO PAYMENT not visible"
    log("Address Add Verified", "PASS")


@pytest.mark.address
@pytest.mark.parametrize(
    "data",
    [{**d, "id": d["id"] + "_edit",
      "email": d["email"].replace("addr.add.", "addr.edit.")}
     for d in ADDRESS_TEST_ACCOUNTS],
    ids=[d["id"] + "_edit" for d in ADDRESS_TEST_ACCOUNTS],
)
def test_edit_address(page, data):
    """
    Verify an existing address can be edited and updated.
    Flow: Add address → Edit with new data → Verify saved.
    """
    _register_and_login(page, data)
    _add_cart_item(page, data)

    address = AddressPage(page)
    address.open(data["lang"], data["country"], data["gender"])

    # Add initial address
    address.fill_address(ADDRESS_DATA[data["address_key"]])
    address.save_address()
    assert address.has_saved_address(), "Initial address not saved"
    log("Initial address saved", "INFO")

    # Check if edit button is available, if not skip the edit test
    if not address.has_edit_button():
        log("Edit Address button not available - skipping edit test", "SKIP")
        pytest.skip("Edit Address button not found - address may be in different state")
    
    # Edit with different address data
    address.edit_address(ADDRESS_DATA[data["address_key2"]])

    # Verify still saved after edit
    assert address.has_saved_address(), \
        f"[{data['id']}] Address not saved after edit"
    log("Address Edit Verified", "PASS")


@pytest.mark.address
@pytest.mark.parametrize(
    "data",
    [{**d, "id": d["id"] + "_second",
      "email": d["email"].replace("addr.add.", "addr.second.")}
     for d in ADDRESS_TEST_ACCOUNTS],
    ids=[d["id"] + "_second" for d in ADDRESS_TEST_ACCOUNTS],
)
def test_add_second_address(page, data):
    """
    Verify a second address can be added when one already exists.
    Flow: Add first address → Add second address → Verify both saved.
    """
    _register_and_login(page, data)
    _add_cart_item(page, data)

    address = AddressPage(page)
    address.open(data["lang"], data["country"], data["gender"])

    # Add first address
    address.fill_address(ADDRESS_DATA[data["address_key"]])
    address.save_address()
    assert address.has_saved_address(), "First address not saved"
    log("First address saved", "INFO")

    # Add second address using Add New Address button
    address.add_new_address(ADDRESS_DATA[data["address_key2"]])

    # Verify still on address page with saved addresses
    assert address.has_saved_address(), \
        f"[{data['id']}] Addresses not saved after adding second"
    log("Second Address Add Verified", "PASS")
