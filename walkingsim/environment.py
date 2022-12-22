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

import pychrono.core as chrono
from loguru import logger


class EnvironmentLoader:
    """
    Class to load environments from JSON files.
    Environments can be described in JSON files in an agnostic way, completely
    independently of the physics engine used.

    The available engines are: 'chrono'
    """

    def __init__(self, __datapath: str, __engine: str):
        self.__datapath = __datapath
        self.__engine = __engine

        self.__loaders = {"chrono": self._load_environment_chrono}

    def load_environment(self, __env: str):
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

        logger.success(f'Environment "{__env}" loaded successfully !')
        return self.__loaders[self.__engine](config)

    def _load_environment_chrono(self, __config: dict):
        env = Environment(__config)
        return env


class Environment(chrono.ChSystemNSC):
    """
    Represents a physics environment
    """
    def __init__(self, config: dict):
        super().__init__()
        self.Set_G_acc(chrono.ChVectorD(*config.get("gravity")))
        chrono.ChCollisionModel.SetDefaultSuggestedEnvelope(0.001)
        chrono.ChCollisionModel.SetDefaultSuggestedMargin(0.001)
