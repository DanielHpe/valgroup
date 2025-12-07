import os

import yaml

from src.utils.constants import STATIC_VALUES_PATH


class Environment:
    def __init__(self):
        return

    def __read_env_values__(self) -> dict:
        file_path = STATIC_VALUES_PATH
        with open(file_path) as values_yaml:
            dict_values = yaml.load(values_yaml, Loader=yaml.FullLoader)
            return dict_values["env"]

    def __save_env__(self, variable: dict) -> None:
        os.environ[variable["name"]] = str(variable["value"])

    def setup_env(self) -> None:
        env_vars = self.__read_env_values__()
        [self.__save_env__(env_var) for env_var in env_vars]

