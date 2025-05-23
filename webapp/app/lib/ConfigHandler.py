import configparser
from typing import Optional

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
