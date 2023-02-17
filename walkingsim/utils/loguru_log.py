# This file should contain any additionnal logger.
# For more info checkout the documetation at:
# https://loguru.readthedocs.io/en/stable/index.html

import os

# Do not show DEBUG messages
os.environ["LOGURU_LEVEL"] = "INFO"

from loguru import logger
