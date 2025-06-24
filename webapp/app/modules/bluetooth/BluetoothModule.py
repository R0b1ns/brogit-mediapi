import logging

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
            # TODO: get_audio_devices not just has names. Improve that
            'AUDIO_DEVICE': lambda v: v in Backend().audio.get_audio_devices(),
            'SOUND_ENABLED': lambda v: v in (True, False),
            'VOICE_ENABLED': lambda v: v in (True, False),
        }

        option_mapping = {
            'DISCOVERABLE': {
                True: 'on',
                False: 'off'
            },
            'SOUND_ENABLED': {
                True: 'True',
                False: 'False'
            },
            'VOICE_ENABLED': {
                True: 'True',
                False: 'False'
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

        return False

    def get_config(self):
        return self.env_config

    def get_device_class_mapping(self):
        return self.device_class_mapping

    def install(self):
        pass

    def uninstall(self):
        pass

    def deploy(self, k, v):
        # TODO: Execute deploy script
        print("Deployyyy")

    @staticmethod
    def get_info():
        return {
            "name": "bluetooth",  # interne id
            "display_name": "Bluetooth",
            "icon": "bi-bluetooth",
            "type": "module",  # oder "submodule"
            'has_settings': True
        }
