import configparser
import logging
from typing import Optional

import yaml
from dotenv import dotenv_values

def load_config(env_path: str, config_path: str) -> dict:
    config = {}

    env_config = dotenv_values(env_path)
    config.update({
        'environment': dict(env_config)
    })

    config_file_path = env_config.get(config_path)

    if not config_file_path:
        raise KeyError(f'"{config_path}" is not configured in Environment.')

    # This output is before config step. So logger is not configured here. You may not see this info
    logging.info(f'Load config from: {config_file_path}')

    with open(config_file_path, "r") as f:
        yaml_config = yaml.safe_load(f)

    config.update(yaml_config)

    return config

# TODO: This is just a draft
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
