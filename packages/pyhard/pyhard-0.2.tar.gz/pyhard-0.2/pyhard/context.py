import os
from .utils import load_yaml_file


class Configuration:
    _CONFIG_PATH = '../conf/config.yaml'

    def __init__(self):
        _my_path = os.path.abspath(os.path.dirname(__file__))
        self._config_file = os.path.join(_my_path, self._CONFIG_PATH)

        if not os.path.isfile(self._config_file):
            raise FileNotFoundError("Configuration file 'config.yaml' not found in 'conf/'.")

    def __enter__(self):
        self.content = load_yaml_file(self._config_file)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.content.clear()

    def get(self, key):
        if isinstance(key, str):
            return self.content.get(key)
        elif isinstance(key, list):
            return {k: self.content.get(k) for k in key}
