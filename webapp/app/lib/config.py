import configparser
import os
from typing import Optional

import yaml
from dotenv import dotenv_values

# TODO: THis is a whole draft.

def load_config(env_path: str, config_path: str) -> dict:
    config = {}

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    print(BASE_DIR)

    BASE_DIR = os.getcwd()
    print(BASE_DIR)

    from pathlib import Path

    BASE_DIR = Path(__file__).resolve().parent
    print(BASE_DIR)

    env = dotenv_values('app/.env')
    # config.update(env)

    print(env)

    print(env.get('CONFIG_FILE'))

    exit()

    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)

    # # .ini laden
    # parser = configparser.ConfigParser()
    # parser.read(ini_path)
    # for section in parser.sections():
    #     for key, val in parser.items(section):
    #         config[f"{section.upper()}_{key.upper()}"] = val

    return config

class ConfigHandler:
    """
    Reads and writes configuration from an .ini file.

    Args:
        path (str): Path to the .ini config file.
    """

    def __init__(self, path: str):
        self.path = path
        self.config = configparser.ConfigParser()
        self.config.read(path)

    def get(self, section: str, key: str, fallback: Optional[str] = None) -> Optional[str]:
        """
        Get a config value with optional fallback.

        Args:
            section (str): Section name.
            key (str): Key name.
            fallback (str|None): Fallback value if not found.

        Returns:
            str|None: Value from config or fallback.
        """
        return self.config.get(section, key, fallback=fallback)

    def set(self, section: str, key: str, value: str) -> None:
        """
        Set a config value and write it to disk.

        Args:
            section (str): Section name.
            key (str): Key name.
            value (str): New value.
        """
        if not self.config.has_section(section):
            self.config.add_section(section)
        self.config.set(section, key, value)
        with open(self.path, 'w') as f:
            self.config.write(f)

    def remove(self, section: str, key: Optional[str] = None) -> None:
        """
        Remove a key or a whole section.

        Args:
            section (str): Section name.
            key (str|None): Key to remove. If None, remove entire section.
        """
        if key:
            self.config.remove_option(section, key)
        else:
            self.config.remove_section(section)
        with open(self.path, 'w') as f:
            self.config.write(f)
