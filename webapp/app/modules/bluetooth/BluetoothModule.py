import logging
import re
import subprocess

from app.lib.Backend import Backend
from app.lib.ModuleInterface import ModuleInterface
from app.lib.env_config import EnvConfig


class BluetoothModule(ModuleInterface):
    def __init__(self, config):
        super().__init__(config)
        module_config = config.get('bluetooth')
        self.__module_config = module_config

        self.env_config = EnvConfig(module_config.get('config_path'))
        for k in module_config.get('deploy_on'):
            self.env_config.register_callback(k, self.deploy)

        self.device_class_mapping = module_config.get('device_class_mapping')

    def set(self, key, value):

        # Keys and validator lambda
        valid_options = {
            'DEVICE_CLASS': lambda v: v in self.__module_config.get('device_class_mapping'),
            'DISCOVERABLE': lambda v: v in (True, False),
            # TODO: Empty for default device
            'BLUETOOTH_DEVICE': lambda v: v in Backend().bluetooth.list_hci_devices(),
            'SOUND_ENABLED': lambda v: v in (True, False),
            'VOICE_ENABLED': lambda v: v in (True, False),
            # XXX: Here we have to be very careful. Because we write directly text into the config
            'DEVICE_NAME': lambda v: v == "" or (isinstance(v, str) and 1 <= len(v.strip()) <= int(self.__module_config.get('max_device_name_len', 50)) and re.fullmatch(r'[a-zA-Z0-9 _\-]+', v.strip()) is not None),
        }

        option_mapping = {
            'DISCOVERABLE': {
                True: 'on',
                False: 'off'
            },
        }

        validator = valid_options.get(key)

        if not validator:
            logging.debug(f'No validator for key={key}')
            return None

        if validator(value):
            transformation = option_mapping.get(key)

            if transformation:
                self.env_config[key] = transformation.get(value)
            else:
                self.env_config[key] = value

            return True
        else:
            logging.info(f'Failed to validate. key={key}')

        return False

    def get_config(self):
        return self.env_config

    def get_device_class_mapping(self):
        return self.device_class_mapping

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

    def deploy(self, k, v) -> bool:
        if self.get_config().get('INSTALLED') is True:
            deploy_path = self.__module_config.get('deploy_path')

            if not deploy_path:
                raise ValueError("Deploy path not configured.")

            try:
                subprocess.run([deploy_path], check=True)
            except subprocess.CalledProcessError as e:
                raise RuntimeError(f"Deploy script failed with exit code {e.returncode}") from e

            return True

        logging.info("Skip deploy cause module is not installed")
        return False

    import subprocess
    import logging

    @staticmethod
    def list_hci_devices():
        try:
            output = subprocess.check_output(["hciconfig"], text=True)
            return [line.split(":")[0] for line in output.splitlines() if line.startswith("hci")]
        except subprocess.CalledProcessError as e:
            logging.error(f"Failed to execute 'hciconfig': {e}")
            return []
        except FileNotFoundError:
            logging.error("'hciconfig' command not found. Is BlueZ installed?")
            return []
        except Exception as e:
            logging.error(f"An unexpected error occurred while listing HCI devices: {e}")
            return []

    @staticmethod
    def get_info():
        return {
            "name": "bluetooth",  # interne id
            "display_name": "Bluetooth",
            "icon": "bi-bluetooth",
            "type": "module",  # oder "submodule"
            'has_settings': True
        }
