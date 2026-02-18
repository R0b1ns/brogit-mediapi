import logging
import os
import subprocess
from pathlib import Path

from app.lib.ModuleInterface import ModuleInterface
from app.lib.env_config import EnvConfig


class SystemEnvModule(ModuleInterface):
    def __init__(self, config, name):
        super().__init__(config)

        self.__system_module_config = config.get('modules')
        self.__module_config = config.get(name)
        self.__module_name = name

        self.__env_config = EnvConfig(self.__path_builder('config_file_name'))

        # TODO: Add something to detect from module config if we have:
        #  install,update,remove -> apt (package_manager)
        #  start,stop,status -> service (run_manager)
        #  deploy/configure = always manually via script


        # TODO: Here the apply config script should be executed
        #  But dont forget the callbacks like in Bluethooth

        #         for k in module_config.get('deploy_on'):
        #             self.__env_config.register_callback(k, self.deploy)

        self._valid_options = {}
        self._option_mapping = {}

    def __path_builder(self, config_name):
        abs_path = Path(self.__system_module_config['modules_path']) / self.__module_name / self.__system_module_config[config_name]

        if not abs_path.exists():
            raise FileNotFoundError(f"File {abs_path} does not exist")
        return abs_path

    def get_config(self):
        return self.__env_config

    def get(self, key: str = None):
        if not key:
            return self.__env_config
        return self.__env_config.get(key)

    def set(self, k: str, v):
        return self.__env_config.validated_update(k, v, self._valid_options, self._option_mapping)

    def field(self, name: str, callback, validator_lambda, transformation_dict = None, trigger_name: str = None, trigger_accept = None):
        # e.g.
        #         self.field(
        #             name='DEVICE_NAME',
        #             callback=self.apply_config,
        #             validator_lambda=lambda v: policy_validate_device_name(policy_config, v),
        #             transformation_dict={
        #                 'DEVICE_NAME': {
        #                     "": '%H',
        #                 },
        #             },
        #         )

        # Register callback
        self.__env_config.register_callback(name, callback)

        # Set / Overwrite validator for field name
        self._valid_options.update({
            name: validator_lambda
        })

        # Set / Overwrite Value Transformations
        if transformation_dict:
            self._option_mapping.update({
                name: transformation_dict,
            })

        if trigger_name:
            def trigger_callback(event_data):
                # When the trigger is accepted based on trigger_accept callback.
                # Execute the set method, which will at the end maybe also call a trigger
                if trigger_accept is None or (trigger_accept and trigger_accept(event_data)):
                    logging.debug(f"{self.__class__.__name__} Trigger '{trigger_name}' was accepted")
                    self.set(name, event_data)
                else:
                    logging.debug(f"{self.__class__.__name__} Trigger '{trigger_name}' was rejected")

            self.on(trigger_name, trigger_callback)

    def execute_script(self, name, requirements, args = None) -> bool:
        for r in requirements:
            if not r:
                return False

        if args is None:
            args = []
        script_path = self.__path_builder(name)

        run_params = [script_path, *args]

        try:
            subprocess.run(run_params, check=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Error executing script {script_path}: {e.returncode}") from e

        return True

    def gather_facts(self):
        # TODO: Get informations of current configuration and installation state. So we can check in future mismatch between config and systems current state
        pass

    def validate_module(self):
        # TODO: Validate all paths / scripts

        # TODO: Validate config vs facts
        pass

    def install(self, confirm: bool = False) -> bool:
        if self.execute_script(self.__path_builder('script_install'), [confirm,]):
            self.__env_config['INSTALLED'] = True
            return True
        return False

    def deploy(self) -> bool:
        if self.execute_script(self.__path_builder('script_deploy'), [self.get_config().get('INSTALLED') is True]):
            return True
        logging.info("Skip deploy cause module is not installed")
        return False

    def apply_config(self) -> bool:
        if self.execute_script(self.__path_builder('script_apply_config'), [self.get_config().get('INSTALLED') is True]):
            return True
        logging.info("Skip apply config cause module is not installed")
        return False

    def update(self) -> bool:
        if self.execute_script(self.__path_builder('script_update'), [self.get_config().get('INSTALLED') is True]):
            return True
        logging.info("Skip update cause module is not installed")
        return False

    def uninstall(self, confirm: bool = False) -> bool:
        if self.execute_script(self.__path_builder('script_uninstall'), [confirm]):
            self.__env_config['INSTALLED'] = False
        return True

    # TODO: Add methods for service start status stop