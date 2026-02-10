import subprocess

from app.lib.ModuleInterface import ModuleInterface
from app.lib.env_config import EnvConfig


class NginxModule(ModuleInterface):
    def __init__(self, config):
        super().__init__(config)

        # TODO: Move that to interface. Also methods install / uninstall
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

    def is_installed(self) -> bool:
        detect_path = self.__module_config.get('detect_path')

        if not detect_path:
            raise ValueError("Detect path not configured.")

        config_path = self.__module_config.get('config_path')

        if not config_path:
            raise ValueError("Config path not configured.")

        try:
            subprocess.run([detect_path, config_path], check=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Detect script failed with exit code {e.returncode}") from e

        return True

    def update_available(self):
        update_available_path = self.__module_config.get('update_apt_available_path')

        if not update_available_path:
            raise ValueError("Update APT Available path not configured.")

        try:
            subprocess.run([update_available_path, 'nginx'], check=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Update APT Available failed with exit code {e.returncode}") from e

        return True

    def update(self):
        update_apt_path = self.__module_config.get('update_apt_path')

        if not update_apt_path:
            raise ValueError("Update APT path not configured.")

        try:
            subprocess.run([update_apt_path, 'nginx'], check=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Update APT failed with exit code {e.returncode}") from e

        return True

    def install(self, confirm: bool = False) -> bool:
        if not confirm:
            return False

        install_path = self.__module_config.get('install_path')

        if not install_path:
            raise ValueError("Install path not configured.")

        config_path = self.__module_config.get('config_path')

        if not config_path:
            raise ValueError("Config path not configured.")

        try:
            subprocess.run([install_path, config_path], check=True)
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