"""
3D PyChrono muscle-based walking simulator
File: environment.py
Authors:
    BECKER Robin-Gilles
    BOURGEOIS Noé
    HENRY DE FRAHAN Antoine
    PALMISANO Luca
Description:
    Class for loading and creating the physics system (= Environment).
"""

import json
import os

from loguru import logger


class EnvironmentProps:
    """
    Class to load environments from JSON files.
    Environments can be described in JSON files in an agnostic way, completely
    independently of the physics engine used.

    The available engines are: 'chrono'
    """

    def __init__(self, __datapath: str):
        self.__datapath = __datapath

    def load(self, __env: str):
        """
        Loads an environment from a JSON file.

        :param __env: The name of the environment to load
        :return: The environment system
        """
        filename = os.path.join(self.__datapath, f"{__env}.json")

        # We do not stop the code here so that `open` will
        # raise an exception when opening the file.
        if not os.path.exists(filename):
            logger.error(f'Environment "{__env}" not found !')

        with open(filename, "r") as fp:
            config = json.load(fp)

        logger.debug(f'Environment "{__env}" loaded successfully !')
        return config
