import pygad
from _logging import logger
import numpy as np
import networkx as nx
from creature.genotype import Genotype
from walkingsim.auto_indent import AutoIndent
import sys

logger.debug("Starting genetic_algorithm.py")
sys.stdout = AutoIndent(sys.stdout)
