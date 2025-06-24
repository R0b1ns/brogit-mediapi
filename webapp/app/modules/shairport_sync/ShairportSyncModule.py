import logging
import subprocess

from app.lib.ModuleInterface import ModuleInterface
from app.lib.env_config import EnvConfig


class ShairportSyncModule(ModuleInterface):
    def __init__(self, config):
        super().__init__(config)
        self.__module_config = config.get('shairport-sync')

        self.env_config = EnvConfig(self.__module_config.get('config_path'))

    @staticmethod
    def get_info():
        return {
            "name": "shairport-sync",  # interne id
            "display_name": "ShairPort-Sync",
            "icon": "bi-cog",
            "type": "submodule",
            'has_settings': True
        }

    @staticmethod
    def get_license():
        try:
            return open('../modules/shairport-sync/repositories/shairport-sync/LICENSES').read()
        except:
            return "Unable to open LICENCE. Module is not installed yet"

    def get(self, key: str = None):
        if not key:
            return self.env_config
        return self.env_config.get(key)

    def install(self, confirm: bool = False) -> bool:
        if not confirm:
            return False

        install_path = self.__module_config.get('install_path')

        if not install_path:
            raise ValueError("Install path not configured.")

        try:
            subprocess.run([install_path], check=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Install script failed with exit code {e.returncode}") from e

        self.env_config['INSTALLED'] = True
        return True

    def uninstall(self, confirm: bool = False) -> bool:
        if not confirm:
            return False

        uninstall_path = self.__module_config.get('uninstall_path')

        if not uninstall_path:
            raise ValueError("Install path not configured.")

        try:
            subprocess.run([uninstall_path], check=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Uninstall script failed with exit code {e.returncode}") from e

        self.env_config['INSTALLED'] = False
        return True

    def update(self, k, v) -> bool:
        if self.get('INSTALLED') is True:
            update_path = self.__module_config.get('update_path')

            if not update_path:
                raise ValueError("Update path not configured.")

            try:
                subprocess.run([update_path], check=True)
            except subprocess.CalledProcessError as e:
                raise RuntimeError(f"Deploy script failed with exit code {e.returncode}") from e

            return True

        logging.info("Skip deploy cause module is not installed")
        return False