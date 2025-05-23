import sounddevice

from app.lib.ModuleInterface import ModuleInterface


class BluetoothModule(ModuleInterface):
    @staticmethod
    def get_info():
        return {
            "name": "bluetooth",  # interne id
            "display_name": "Bluetooth",
            "icon": "bi-bluetooth",
            "type": "module"  # oder "submodule"
        }

    @staticmethod
    def get_audio_devices():
        return sounddevice.query_devices()

