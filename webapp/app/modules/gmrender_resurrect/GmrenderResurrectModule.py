import subprocess

from app.lib.ModuleInterface import ModuleInterface
from app.lib.env_config import EnvConfig


class GmrenderResurrectModule(ModuleInterface):
    def __init__(self, config):
        super().__init__(config)
        self.__module_config = config.get('gmrender-resurrect')

        self.env_config = EnvConfig(self.__module_config.get('config_path'))

    @staticmethod
    def get_info():
        return {
            "name": "gmrender-resurrect",  # interne id
            "display_name": "GmrenderResurrect",
            "icon": "bi-cog",
            "type": "submodule",
            'has_settings': True
        }

    @staticmethod
    def get_license():
        try:
            return open('../modules/gmrender-resurrect/repositories/gmrender-resurrect/COPYING').read()
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