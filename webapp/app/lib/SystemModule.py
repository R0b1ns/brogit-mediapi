import logging
import os
import subprocess
from pathlib import Path

from app.lib.ModuleInterface import ModuleInterface
from app.lib.env_config import EnvConfig


class SystemModule(ModuleInterface):
    def __init__(self, config, name):
        super().__init__(config)

        self.__system_module_config = config.get('modules')
        self.__module_config = config.get(name)

        self.__env_config = EnvConfig(self.__path_builder('config_file_name'))

    def __path_builder(self, config_name):
        abs_path = Path(self.__system_module_config['modules_path']) / self.__system_module_config[config_name]

        if not abs_path.exists():
            raise FileNotFoundError(f"File {abs_path} does not exist")
        return abs_path


    def get_config(self):
        return self.__env_config

    def execute_script(self, name, args=None):
        if args is None:
            args = []
        script_path = self.__path_builder(name)

        run_params = [script_path, *args]

        try:
            subprocess.run(run_params, check=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Error executing script {script_path}: {e.returncode}") from e

    def install(self, confirm: bool = False) -> bool:
        if not confirm:
            return False

        self.execute_script(self.__path_builder('script_install'))

        self.__env_config['INSTALLED'] = True
        return True

    def deploy(self) -> bool:
        if self.get_config().get('INSTALLED') is True:
            self.execute_script(self.__path_builder('script_deploy'))

            return True

        logging.info("Skip deploy cause module is not installed")
        return False

    def uninstall(self, confirm: bool = False) -> bool:
        if not confirm:
            return False

        self.execute_script(self.__path_builder('script_uninstall'))

        self.env_config['INSTALLED'] = False
        return True

    # TODO: Add methods for service start status stop