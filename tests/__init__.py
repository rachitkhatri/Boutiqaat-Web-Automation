# ============================================================
# tests/__init__.py
#
# PURPOSE:
#   This file marks the 'tests' directory as a Python package.
#
# WHAT DOES IT DO?
#   Enables pytest to discover and import test modules.
#   Allows tests to import from other test modules if needed.
#
# TEST MODULES IN THIS PACKAGE:
#   - test_e2e_flow.py     → End-to-end purchase flow tests
#   - test_registration.py → User registration tests
#   - test_cart.py         → Shopping cart tests
#   - test_wishlist.py     → Wishlist tests
#   - test_address.py      → Address management tests
#   - test_navigation.py   → Navigation and category tests
#   - test_markers.py      → Pytest marker definitions
#
# WHY IS IT EMPTY?
#   Pytest automatically discovers test files (test_*.py).
#   No initialization code is needed for test discovery.
#
# WHAT IF THIS FILE DIDN'T EXIST?
#   - Pytest would still discover tests (pytest doesn't require it)
#   - But it's best practice to include it for consistency
#   - Allows tests to import from each other if needed
#
# PYTEST DISCOVERY:
#   Pytest finds tests by:
#   1. Looking for test_*.py or *_test.py files
#   2. Looking for Test* classes
#   3. Looking for test_* functions
#
#   This file doesn't affect pytest discovery, but it's
#   good practice to include it.
#
# ============================================================
