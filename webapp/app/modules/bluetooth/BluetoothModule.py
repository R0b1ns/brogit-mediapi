import sounddevice


class BluetoothModule:

    @staticmethod
    def get_audio_devices():
        return sounddevice.query_devices()

