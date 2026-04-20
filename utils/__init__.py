# ============================================================
# utils/__init__.py
#
# PURPOSE:
#   This file marks the 'utils' directory as a Python package.
#
# WHAT DOES IT DO?
#   Enables importing utility functions and classes from
#   the utils package.
#
# EXAMPLE USAGE:
#   from utils.logger import log
#   from utils.logger import log_error
#   from utils.logger import log_screenshot
#
# UTILITIES IN THIS PACKAGE:
#   - logger.py → Enhanced logging system with multiple levels
#                 (INFO, PASS, FAIL, ERROR, WARN, DEBUG, SKIP)
#
# WHY IS IT EMPTY?
#   We import utilities directly from their modules.
#   No initialization code is needed for the utils package.
#
# WHAT IF THIS FILE DIDN'T EXIST?
#   You would get: "ModuleNotFoundError: No module named 'utils'"
#   All files using the logger would fail to import.
#
# ALTERNATIVE APPROACH (not used in this project):
#   You could add imports here to simplify usage:
#
#   from .logger import log, log_error, log_screenshot
#   __all__ = ['log', 'log_error', 'log_screenshot']
#
#   Then users could do:
#   from utils import log, log_error
#
#   Instead of:
#   from utils.logger import log, log_error
#
# ============================================================
