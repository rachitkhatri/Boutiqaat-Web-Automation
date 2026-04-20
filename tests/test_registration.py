# ============================================================
# test_registration.py — Standalone registration smoke test ONLY.
#
# Uses REGISTRATION_DATA — completely separate from E2E_DATA.
# Running the full suite (pytest tests/) will NOT duplicate registration.
#
# Run: pytest tests/test_registration.py -v
# ============================================================

import pytest
from data.test_data import REGISTRATION_DATA
from pages.registration_page import RegistrationPage


@pytest.mark.registration
@pytest.mark.parametrize(
    "data",
    REGISTRATION_DATA,
    ids=[d["id"] for d in REGISTRATION_DATA],
)
def test_user_registration(page, data):
    """
    Verify a new user can register successfully.
    Retries up to 3 times — screenshot saved on each failed attempt.
    """
    reg = RegistrationPage(page)
    reg.open(data["lang"], data["country"], data["gender"])
    assert reg.register(data), (
        f"Registration failed for [{data['id']}] after all retries — "
        f"check screenshots/ folder"
    )
