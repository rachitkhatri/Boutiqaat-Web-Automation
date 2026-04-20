# ============================================================
# test_data.py — All test datasets for the automation framework.
#
# PURPOSE:
#   Central data store for every test module. Each test imports
#   only the dataset it needs, keeping test logic and test data
#   cleanly separated (data-driven testing pattern).
#
# DATASETS:
#   ADDRESS_DATA      — Delivery address details keyed by city
#   E2E_DATA          — Happy-path end-to-end purchase flow
#   E2E_CANCEL_DATA   — Cancel/failure path on KNET gateway
#   REGISTRATION_DATA — Standalone registration smoke test
#   CART_DATA         — Cart add/remove operations
#   WISHLIST_DATA     — Wishlist add from PDP
#
# NOTE:
#   _TS (Unix timestamp) is appended to every email so each
#   test run creates a unique account — no manual cleanup needed.
# ============================================================

import time  # Used to generate unique timestamps for email addresses

# Unix timestamp string — ensures every test run uses a fresh email
# Example: "1745678901" → email becomes "e2e.happy.1745678901@mailinator.com"
_TS = str(int(time.time()))

# ──────────────────────────────────────────────────────────────
# ADDRESS DATA — keyed by "{country}_{city}" for easy lookup
#
# Used by: test_address.py, test_e2e_flow.py
# Each key maps to a dict of form field values that match the
# checkout address form on boutiqaat.com.
#
# Fields match these HTML selectors:
#   full_name  → #firstname
#   area       → #region_area (dropdown label)
#   block      → #addr_block  (dropdown value, loads after area)
#   street     → #addr_street
#   avenue     → #addr_avenue (optional)
#   villa      → #addr_villa
#   floor      → #addr_floornumber (optional)
#   flat       → #addr_flatenumber (optional)
#   telephone  → #telephone
#   notes      → #notes (optional)
# ──────────────────────────────────────────────────────────────
ADDRESS_DATA = {
    # Kuwait — Salmiya area (primary address for add/e2e tests)
    "kw_salmiya": {
        "full_name": "Test User",
        "area":      "Salmiya",            # Dropdown label in #region_area
        "block":     "1",                  # Dropdown value in #addr_block
        "street":    "Salem Al Mubarak St",
        "avenue":    "5",
        "villa":     "12",
        "floor":     "2",
        "flat":      "4",
        "telephone": "50066666",           # Kuwait mobile format (8 digits)
        "notes":     "Test delivery notes",
    },
    # Kuwait — Hawalli area (used for edit/second-address tests)
    "kw_hawalli": {
        "full_name": "Test User Edited",
        "area":      "Hawalli",
        "block":     "2",
        "street":    "Tunis St",
        "avenue":    "3",
        "villa":     "7",
        "floor":     "1",
        "flat":      "2",
        "telephone": "50077777",
        "notes":     "Edited delivery notes",
    },
}

# ──────────────────────────────────────────────────────────────
# E2E DATA — happy-path end-to-end purchase flow
#
# Used by: test_e2e_flow.py → test_complete_flow
# Flow: Register → Login → Search → Product → Cart →
#       Address → Payment → PAY → Wait for success
# ──────────────────────────────────────────────────────────────
E2E_DATA = [
    {
        "id":            "e2e_kw_en_women",                    # Unique test ID (shown in report)
        "full_name":     "E2E Tester",                         # Registration full name
        "mobile_number": "50011111",                           # Kuwait mobile (8 digits)
        "email":         f"e2e.happy.{_TS}@mailinator.com",   # Unique email per run
        "password":      "Test@1234",                          # Meets site password policy
        "gender":        "women",                              # Site section (women/men)
        "lang":          "en",                                 # Language code (en/ar)
        "country":       "kw",                                 # Country code (kw/sa/ae)
        "search_term":   "perfume",                            # Product to search for
        "address_key":   "kw_salmiya",                         # Key into ADDRESS_DATA above
    },
]

# ──────────────────────────────────────────────────────────────
# E2E CANCEL DATA — cancel/failure path on KNET gateway
#
# Used by: test_e2e_flow.py → test_cancel_flow
# Flow: Same as E2E_DATA but clicks Cancel on KNET gateway
#       then captures the OOPS failure screen details.
# ──────────────────────────────────────────────────────────────
E2E_CANCEL_DATA = [
    {
        "id":            "e2e_cancel_kw_en_women",
        "full_name":     "E2E Cancel Tester",
        "mobile_number": "50022222",
        "email":         f"e2e.cancel.{_TS}@mailinator.com",
        "password":      "Test@1234",
        "gender":        "women",
        "lang":          "en",
        "country":       "kw",
        "search_term":   "perfume",
        "address_key":   "kw_salmiya",
    },
]

# ──────────────────────────────────────────────────────────────
# REGISTRATION DATA — standalone registration smoke test
#
# Used by: test_registration.py → test_user_registration
# Flow: Register via REST API → Login via UI → Verify session
# ──────────────────────────────────────────────────────────────
REGISTRATION_DATA = [
    {
        "id":            "reg_kw_en_women",
        "full_name":     "Reg Tester",
        "mobile_number": "50033333",
        "email":         f"reg.{_TS}@mailinator.com",
        "password":      "Test@1234",
        "gender":        "women",
        "lang":          "en",
        "country":       "kw",
    },
]

# ──────────────────────────────────────────────────────────────
# CART DATA — cart add/remove tests
#
# Used by: test_cart.py → test_add_two_products_and_remove_one
# Flow: Register → Login → Search "perfume" → Add to cart →
#       Search "puff" → Add Sippii Bottle → Remove one → Verify
# ──────────────────────────────────────────────────────────────
CART_DATA = [
    {
        "id":            "cart_kw_en_women",
        "full_name":     "Cart Tester",
        "mobile_number": "50044444",
        "email":         f"cart.{_TS}@mailinator.com",
        "password":      "Test@1234",
        "gender":        "women",
        "lang":          "en",
        "country":       "kw",
    },
]

# ──────────────────────────────────────────────────────────────
# WISHLIST DATA — wishlist add tests
#
# Used by: test_wishlist.py → test_add_to_wishlist
# Flow: Register → Login → Search → Product → Add to Wishlist
# ──────────────────────────────────────────────────────────────
WISHLIST_DATA = [
    {
        "id":            "wish_kw_en_women",
        "full_name":     "Wish Tester",
        "mobile_number": "50055555",
        "email":         f"wish.{_TS}@mailinator.com",
        "password":      "Test@1234",
        "gender":        "women",
        "lang":          "en",
        "country":       "kw",
        "search_term":   "perfume",                            # Product to search and wishlist
    },
]
