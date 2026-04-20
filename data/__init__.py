# ============================================================
# data/__init__.py
#
# PURPOSE:
#   This file marks the 'data' directory as a Python package.
#
# WHAT DOES IT DO?
#   Enables importing test data from the data package.
#
# EXAMPLE USAGE:
#   from data.test_data import E2E_DATA
#   from data.test_data import REGISTRATION_DATA
#   from data.test_data import ADDRESS_DATA
#
# WHY IS IT EMPTY?
#   The data package doesn't need any initialization code.
#   Test data is defined in test_data.py and imported directly.
#
# WHAT IF THIS FILE DIDN'T EXIST?
#   You would get: "ModuleNotFoundError: No module named 'data'"
#   All test files would fail to import test data.
#
# ============================================================
