# Author: Robin Biegel
# Version: 2026.2.15

# config_loader.py
import logging
from typing import Union

from dotenv import dotenv_values, set_key
from pathlib import Path
from collections import defaultdict

from app.lib.common import universal_bool


class EnvConfig(dict):
    def __init__(self, path):
        self.path = Path(path)
        self._env = dotenv_values(self.path)

        # Transform a str:bool into bool
        for k, v in self._env.items():
            r = universal_bool(v, detect=True)
            if r is None:
                continue
            self._env[k] = r

        super().__init__(self._env)
        self._callbacks = defaultdict(list)

    def __setitem__(self, key, value):
        old_value = self.get(key)
        super().__setitem__(key, value)
        self._update_env_file(key, value)
        if old_value != value:
            self._run_callbacks(key, value)

    def update(self, *args, **kwargs):
        for k, v in dict(*args, **kwargs).items():
            self[k] = v  # __setitem__ handles everything

    def _update_env_file(self, key, value):
        set_key(str(self.path), key, str(value))

    def register_callback(self, key, callback):
        """Register a function to be called when a specific key is updated."""
        self._callbacks[key].append(callback)

    def _run_callbacks(self, key, value):
        for callback in self._callbacks.get(key, []):
            callback(key, value)

    def validated_update(self, k, v, valid_options, option_mapping = None) -> Union[bool, None]:
        logging.debug(f"Validating {k}={v}")

        if option_mapping is None:
            option_mapping = {}

        validator = valid_options.get(k)

        if not validator:
            logging.warning(f'No validator for key={k}')
            return None

        if not validator(v):
            logging.warning(f'Failed to validate. key={k}')
            return False

        transformation = option_mapping.get(k)

        if transformation:
            # If transformation result is none, fallback to v
            self[k] = transformation.get(v, v)
        else:
            self[k] = v

        return True


if __name__ == '__main__':
    # TODO: Test me!
    cnf = EnvConfig('../../../modules/shairport-sync/config.env')

    print(cnf.get('DEVICE_NAME'))
    cnf.validated_update('DEVICE_NAME', 'Test', {
        'DEVICE_NAME': lambda v: True,
    })
    print(cnf.get('DEVICE_NAME'))