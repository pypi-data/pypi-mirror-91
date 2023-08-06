from typing import Optional

import yaml


DEFAULT_CONFIG = {
    "goodbye": "Adios!",
}


class Greeter:
    def __init__(self, user_name: str, config_file: Optional[str] = None):
        self.user_name = user_name
        self.config_file = config_file
        if config_file:
            self.config = self._read_config()
        else:
            self.config = DEFAULT_CONFIG.copy()

    def _read_config(self):
        with open(self.config_file) as file_pointer:
            return yaml.safe_load(file_pointer)

    def greet(self):
        print(f"Hola {self.user_name}")
        print(self.config["goodbye"])
