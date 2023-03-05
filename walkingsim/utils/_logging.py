# This file should contain any additionnal logger.
# For more info checkout the documetation at:
# https://loguru.readthedocs.io/en/stable/index.html

import os

# os.environ["LOGURU_LEVEL"] = "INFO"
os.environ["LOGURU_LEVEL"] = "ERROR"

from loguru import logger
from tqdm import tqdm

# Interoperability with tqdm iterations
# https://loguru.readthedocs.io/en/stable/resources/recipes.html#interoperability-with-tqdm-iterations
logger.remove()
logger.add(lambda msg: tqdm.write(msg, end=""), colorize=True)
