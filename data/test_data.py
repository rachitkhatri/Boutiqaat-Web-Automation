# ============================================================
# test_data.py — All test datasets for the automation framework.
# ============================================================

import time

_TS = str(int(time.time()))

# ──────────────────────────────────────────────────────────────
# ADDRESS DATA — keyed by country_city for lookup
# ──────────────────────────────────────────────────────────────
ADDRESS_DATA = {
    "kw_salmiya": {
        "full_name": "Test User",
        "area": "Salmiya",
        "block": "1",
        "street": "Salem Al Mubarak St",
        "avenue": "5",
        "villa": "12",
        "floor": "2",
        "flat": "4",
        "telephone": "50066666",
        "notes": "Test delivery notes",
    },
    "kw_hawalli": {
        "full_name": "Test User Edited",
        "area": "Hawalli",
        "block": "2",
        "street": "Tunis St",
        "avenue": "3",
        "villa": "7",
        "floor": "1",
        "flat": "2",
        "telephone": "50077777",
        "notes": "Edited delivery notes",
    },
}

# ──────────────────────────────────────────────────────────────
# E2E DATA — happy-path end-to-end flow
# ──────────────────────────────────────────────────────────────
E2E_DATA = [
    {
        "id": "e2e_kw_en_women",
        "full_name": "E2E Tester",
        "mobile_number": "50011111",
        "email": f"e2e.happy.{_TS}@mailinator.com",
        "password": "Test@1234",
        "gender": "women",
        "lang": "en",
        "country": "kw",
        "search_term": "perfume",
        "address_key": "kw_salmiya",
    },
]

# ──────────────────────────────────────────────────────────────
# E2E CANCEL DATA — cancel/failure path
# ──────────────────────────────────────────────────────────────
E2E_CANCEL_DATA = [
    {
        "id": "e2e_cancel_kw_en_women",
        "full_name": "E2E Cancel Tester",
        "mobile_number": "50022222",
        "email": f"e2e.cancel.{_TS}@mailinator.com",
        "password": "Test@1234",
        "gender": "women",
        "lang": "en",
        "country": "kw",
        "search_term": "perfume",
        "address_key": "kw_salmiya",
    },
]

# ──────────────────────────────────────────────────────────────
# REGISTRATION DATA — standalone registration test
# ──────────────────────────────────────────────────────────────
REGISTRATION_DATA = [
    {
        "id": "reg_kw_en_women",
        "full_name": "Reg Tester",
        "mobile_number": "50033333",
        "email": f"reg.{_TS}@mailinator.com",
        "password": "Test@1234",
        "gender": "women",
        "lang": "en",
        "country": "kw",
    },
]

# ──────────────────────────────────────────────────────────────
# CART DATA — cart add/remove tests
# ──────────────────────────────────────────────────────────────
CART_DATA = [
    {
        "id": "cart_kw_en_women",
        "full_name": "Cart Tester",
        "mobile_number": "50044444",
        "email": f"cart.{_TS}@mailinator.com",
        "password": "Test@1234",
        "gender": "women",
        "lang": "en",
        "country": "kw",
    },
]

# ──────────────────────────────────────────────────────────────
# WISHLIST DATA — wishlist add tests
# ──────────────────────────────────────────────────────────────
WISHLIST_DATA = [
    {
        "id": "wish_kw_en_women",
        "full_name": "Wish Tester",
        "mobile_number": "50055555",
        "email": f"wish.{_TS}@mailinator.com",
        "password": "Test@1234",
        "gender": "women",
        "lang": "en",
        "country": "kw",
        "search_term": "perfume",
    },
]
