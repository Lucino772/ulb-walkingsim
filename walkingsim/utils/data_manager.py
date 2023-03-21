import csv
import datetime as dt
import os
import pickle
import re
import sys

from loguru import logger


class DataManager:
    def __init__(
        self, group: str, date: str = None, fail_if_exists: bool = True
    ):
        if date is None:
            date = dt.datetime.now().strftime("%Y%m%d-%H%M%S")

        self.__date = date

        self.__root_dir = os.path.join("solutions", group)
        self.__data_dir = os.path.join(self.__root_dir, date)
        self.__log_dir = os.path.join(self.__data_dir, "logs")

    @property
    def date(self):
        return self.__date

    def _create_data_dir(self):
        try:
            os.makedirs(self.__data_dir)
        except FileExistsError:
            logger.error(f"The directory {self.__data_dir} already exists")
            sys.exit()
        except FileNotFoundError:
            logger.error(
                f"The parent directory {self.__root_dir} doesn't exist"
            )
            sys.exit()
        else:
            os.mkdir(self.__log_dir)

    def _ensure_data_dir(self):
        if os.path.exists(self.__data_dir):
            return

        self._create_data_dir()

    # path
    def get_local_path(self, filename: str):
        return os.path.join(self.__data_dir, filename)

    def get_global_path(self, filename: str):
        return os.path.join(self.__root_dir, filename)

    # save
    def save_local_dat_file(self, filename: str, obj):
        self._ensure_data_dir()
        filepath = self.get_local_path(filename)
        with open(filepath, "wb") as fp:
            pickle.dump(obj, fp)
            logger.info(f"Saved {obj} in {filepath}")

    def save_global_dat_file(self, filename: str, obj):
        self._ensure_data_dir()
        filepath = self.get_global_path(filename)
        with open(filepath, "wb") as fp:
            pickle.dump(obj, fp)
            logger.info(f"Saved {obj} in {filepath}")

    def save_log_file(self, filename: str, headers, data):
        self._ensure_data_dir()
        file_path = os.path.join(self.__log_dir, filename)
        with open(file_path, "a", newline="") as csvfile:
            fieldnames = headers
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if os.path.getsize(file_path) == 0:
                writer.writeheader()
            writer.writerow(data)

    # load
    def load_local_dat_file(self, filename: str):
        filepath = self.get_local_path(filename)
        with open(filepath, "rb") as fp:
            obj = pickle.load(fp)
            logger.info(f"Loaded {obj} in {filepath}")

        return obj

    def load_global_dat_file(self, filename: str):
        filepath = self.get_global_path(filename)
        with open(filepath, "rb") as fp:
            obj = pickle.load(fp)
            logger.info(f"Loaded {obj} in {filepath}")

        return obj
