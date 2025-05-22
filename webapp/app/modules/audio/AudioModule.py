import subprocess

import sounddevice


class AudioModule:

    @staticmethod
    def get_audio_device1():
        return sounddevice.query_devices()

    @staticmethod
    def get_audio_devices():
        # Use 'arecord' or 'aplay' to list audio devices on Linux
        try:
            result = subprocess.run(["aplay", "-l"], capture_output=True, text=True)
            if result.returncode == 0:
                print(result.stdout)
            else:
                print("Error retrieving audio devices:", result.stderr)
        except FileNotFoundError:
            print("'arecord' tool is not installed. Please install 'alsa-utils'.")
