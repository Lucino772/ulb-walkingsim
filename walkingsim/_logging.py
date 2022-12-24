import sys

from loguru import logger

# logger.add("logs/genotype.log", format="{time} {level} {message}", level="DEBUG", rotation="1 MB")
# logger.add(sys.stderr, format="{time} {level} {message}", level="INFO")
logger.add(sys.stdout, format="{level} {message}", level="DEBUG")
logger.add(sys.stdout, format="{level} {message}", level="INFO")
