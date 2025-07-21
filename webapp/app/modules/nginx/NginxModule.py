import subprocess

from app.lib.ModuleInterface import ModuleInterface
from app.lib.env_config import EnvConfig


class NginxModule(ModuleInterface):
    def __init__(self, config):
        super().__init__(config)
        self.__module_config = config.get('nginx')

        # self.env_config = EnvConfig(self.__module_config.get('config_path'))

    @staticmethod
    def get_info():
        return {
            "name": "nginx",  # interne id
            "display_name": "Nginx",
            "icon": "bi-cog",
            "type": "submodule",
            'has_settings': True
        }