import subprocess

from app.lib.ModuleInterface import ModuleInterface
from app.lib.env_config import EnvConfig


class NginxModule(ModuleInterface):
    def __init__(self, config):
        super().__init__(config)
        self.__module_config = config.get('nginx')

        self.env_config = EnvConfig(self.__module_config.get('config_path'))

    @staticmethod
    def get_info():
        return {
            "name": "nginx",  # interne id
            "display_name": "Nginx",
            "icon": "bi-cog",
            "type": "submodule",
            'has_settings': True
        }

    def get(self, key: str = None):
        if not key:
            return self.env_config
        return self.env_config.get(key)

    def update_certificate(self, public_key: str, private_key: str):
        # TODO: Add update_certificate functionality
        raise NotImplementedError()

    def install(self, confirm: bool = False) -> bool:
        # TODO: Run installation script
        raise NotImplementedError()

    def uninstall(self, confirm: bool = False) -> bool:
        # TODO: Run uninstallation script
        raise NotImplementedError()