import logging

from app.lib.Policies import policy_validate_device_name
from app.lib.SystemEnvModule import SystemEnvModule


class GmrenderResurrectModule(SystemEnvModule):
    def __init__(self, config):
        super().__init__(config)
        self.__module_config = config.get('gmrender-resurrect')

        policy_config = config.get('policies')

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

    @staticmethod
    def get_info():
        return {
            "name": "gmrender-resurrect",  # interne id
            "display_name": "GmrenderResurrect",
            "icon": "bi-cog",
            "type": "submodule",
            'has_settings': True
        }

    def get_license(self):
        try:
            return open('../modules/gmrender-resurrect/repositories/gmrender-resurrect/COPYING').read()
        except:
            if self.get('INSTALLED'):
                logging.warning("Module is marked as installed, but licence is not available. So module will be removed...")
                self.uninstall(True)
                return "Unable to open LICENCE. Module was removed."

            return "Unable to open LICENCE. Module is not installed yet"