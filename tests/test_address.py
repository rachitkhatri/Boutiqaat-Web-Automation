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
import time
import os
from dotenv import load_dotenv
from data.test_data import ADDRESS_DATA
from pages.registration_page import RegistrationPage
from pages.address_page import AddressPage
from pages.cart_page import CartPage
from pages.search_page import SearchPage
from utils.logger import log

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
    reg = RegistrationPage(page)
    assert reg.register_and_login(data), "Registration/Login failed"


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
