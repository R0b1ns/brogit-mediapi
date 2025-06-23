from app.lib.ModuleInterface import ModuleInterface
from app.lib.env_config import EnvConfig


class BluetoothModule(ModuleInterface):
    def __init__(self, config):
        super().__init__(config)
        module_config = config.get('bluetooth')
        self.env_config = EnvConfig(module_config.get('config_path'))
        for k in module_config.get('deploy_on'):
            self.env_config.register_callback(k, self.deploy)

    def get_config(self):
        # TODO: Remove that, just for dev purpose
        self.env_config['DISCOVERABLE'] = "off"
        return self.env_config

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
