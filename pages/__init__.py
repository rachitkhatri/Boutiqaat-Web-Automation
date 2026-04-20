# ============================================================
# pages/__init__.py
#
# PURPOSE:
#   This file marks the 'pages' directory as a Python package.
#
# WHAT DOES IT DO?
#   Enables importing Page Object Model (POM) classes from
#   the pages package.
#
# EXAMPLE USAGE:
#   from pages.login_page import LoginPage
#   from pages.cart_page import CartPage
#   from pages.payment_page import PaymentPage
#   from pages.address_page import AddressPage
#
# PAGE OBJECTS IN THIS PACKAGE:
#   - base_page.py         → BasePage (parent class)
#   - login_page.py        → LoginPage
#   - registration_page.py → RegistrationPage
#   - search_page.py       → SearchPage
#   - cart_page.py         → CartPage
#   - address_page.py      → AddressPage
#   - payment_page.py      → PaymentPage
#   - wishlist_page.py     → WishlistPage
#   - navigation_page.py   → NavigationPage
#
# WHY IS IT EMPTY?
#   We import page objects directly from their modules.
#   No initialization code is needed for the pages package.
#
# WHAT IF THIS FILE DIDN'T EXIST?
#   You would get: "ModuleNotFoundError: No module named 'pages'"
#   All test files would fail to import page objects.
#
# ALTERNATIVE APPROACH (not used in this project):
#   You could add imports here to simplify usage:
#
#   from .login_page import LoginPage
#   from .cart_page import CartPage
#   __all__ = ['LoginPage', 'CartPage']
#
#   Then users could do:
#   from pages import LoginPage, CartPage
#
#   Instead of:
#   from pages.login_page import LoginPage
#   from pages.cart_page import CartPage
#
# ============================================================
