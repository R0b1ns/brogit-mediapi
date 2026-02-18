import logging

from app.lib.Policies import policy_validate_device_name
from app.lib.SystemEnvModule import SystemEnvModule


class ShairportSyncModule(SystemEnvModule):
    def __init__(self, config):
        super().__init__(config, 'shairport-sync')

        policy_config = config.get('policies')

        # Configure Fields (Preferred way)
        self.field(
            name='DEVICE_NAME',
            callback=self.apply_config,
            validator_lambda=lambda v: policy_validate_device_name(policy_config, v),
            transformation_dict={
                'DEVICE_NAME': {
                    "": '%H',
                },
            },
            trigger_name='set_hostname',
            trigger_accept=lambda v: self.get('DEVICE_NAME') == "" or self.get('DEVICE_NAME') != v,
        )

        ### Manual configuration ###

        ## Configure callbacks

        # e.g. (not required, cause this is made in field)
        # self.__env_config.register_callback('DEVICE_NAME', self.apply_config)

        ## Keys and validator lambda

        # e.g. (not required, cause this is made in field)
        # self._valid_options = {
        #     'DEVICE_NAME': lambda v: policy_validate_device_name(policy_config, v),
        # }

        ## Value Transformations

        # e.g. (not required, cause this is made in field)
        # self._option_mapping = {
        #     'DEVICE_NAME': {
        #         "": '%H',
        #     },
        # }

    @staticmethod
    def get_info():
        return {
            "name": "shairport-sync",  # interne id
            "display_name": "ShairPort-Sync",
            "icon": "bi-cog",
            "type": "submodule",
            'has_settings': True
        }

    def get_license(self):
        try:
            return open('../modules/shairport-sync/repositories/shairport-sync/LICENSES').read()
        except:
            if self.get_config().get('INSTALLED'):
                logging.warning("Module is marked as installed, but licence is not available. So module will be removed...")
                self.uninstall(True)
                return "Unable to open LICENCE. Module was removed."

            return "Unable to open LICENCE. Module is not installed yet"
