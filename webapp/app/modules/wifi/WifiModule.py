import sounddevice


class AudioModule:

    @staticmethod
    def get_audio_devices():
        return sounddevice.query_devices()

