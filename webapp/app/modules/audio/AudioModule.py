import locale
import os
import socket
import subprocess


class SystemModule:

    @staticmethod
    def get_hostname():
        return socket.gethostname()

    @staticmethod
    def list_installed_languages():
        b = locale.getlocale()
        a = locale.getdefaultlocale()

        print(a)

        print(b)


if __name__ == '__main__':
    SystemModule().list_installed_languages()

    import sounddevice as sd

    # Liste aller verfügbaren Audiogeräte
    devices = sd.query_devices()
    print(devices)
