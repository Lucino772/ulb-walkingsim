import csv
import datetime
import os
import pickle
import re
import sys

from loguru import logger


class DataManager:
    def __init__(self):
        # TODO utiliser os.path pour cross-platform
        self.__root_dir = "solutions/"
        self.__data_dir = self.__root_dir + self._generate_data_dirname()
        self.__log_dir = self.__data_dir + "logs/"
        self._create_data_dir()

    @property
    def root_dir(self):
        return self.__root_dir

    @staticmethod
    def _generate_data_dirname():
        """
        Format: YYYYMMDD-HHMMSS
        """
        date_now = str(datetime.datetime.now())
        date_now = re.sub("\..*|-|:", "", date_now)
        date_now = re.sub(" ", "-", date_now)

        return date_now + "/"

    def _create_data_dir(self):
        try:
            os.mkdir(self.__data_dir)
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

    def save_local_dat_file(self, filename: str, obj):
        with open(self.__data_dir + filename, "wb") as fp:
            pickle.dump(obj, fp)
            logger.info(f"Saved {obj} in {self.__data_dir}{filename}")

    def save_global_dat_file(self, filename: str, obj):
        with open(self.__root_dir + filename, "wb") as fp:
            pickle.dump(obj, fp)
            logger.info(f"Saved {obj} in {self.__data_dir}{filename}")

    def save_log_file(self, filename: str, headers, data):
        file_path = self.__log_dir + filename
        with open(file_path, "a", newline="") as csvfile:
            fieldnames = headers
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if os.path.getsize(file_path) == 0:
                writer.writeheader()
            writer.writerow(data)
