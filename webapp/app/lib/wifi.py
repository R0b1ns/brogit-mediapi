import logging
import subprocess
import time
from datetime import datetime, timedelta


class WifiHelper:
    _instance = None  # Klassenvariable, um die Singleton-Instanz zu speichern

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(WifiHelper, cls).__new__(cls)
            cls._instance.value = "Initialer Wert"
        return cls._instance

    @staticmethod
    def get_instance():
        if WifiHelper._instance is None:
            WifiHelper()
        return WifiHelper._instance

    def __init__(self):
        self.connected_info = {
            'ssid': None,
            'connected': False,
            'expire_time': datetime.now() + timedelta(seconds=60)
        }

    def is_connected(self) -> bool:
        if self.get_connection_info():
            return True
        else:
            return False

    def get_connection_info(self):
        connected_entries = [item for item in self.scan() if item['connected']]
        len_connected_entries = len(connected_entries)

        if len_connected_entries == 0:
            return False
        elif len_connected_entries == 1:
            return connected_entries[0]
        else:
            logging.error("System error: Unable to be connected with more than one wifi network on the same device")
            return None

    @staticmethod
    def get_known_networks():
        known_networks = set()
        try:
            # Use nmcli to list saved WiFi connections
            result = subprocess.run(['nmcli', '-t', '-f', 'NAME', 'connection'], stdout=subprocess.PIPE)
            output = result.stdout.decode('utf-8').strip().split('\n')

            for line in output:
                known_networks.add(line.strip())  # Add each known SSID to the set

        except subprocess.CalledProcessError as e:
            print(f"Error retrieving known WiFi networks: {e}")

        return known_networks

    def scan(self):
        networks = []
        # Get the list of known networks
        known_networks = self.get_known_networks()

        params = {
            'SSID',
            'BSSID',
            'FREQ',
            'SIGNAL',
            'SECURITY',
            'IN-USE'
        }

        try:
            # Use nmcli to scan for WiFi networks with security info
            result = subprocess.run(['nmcli', '-t', '-f', ','.join(params), 'dev', 'wifi'],
                                    stdout=subprocess.PIPE)
            output = result.stdout.decode('utf-8').strip().split('\n')

            for line in output:
                # Fix for macaddress
                line = line.replace('\\:', '-')
                fields = line.split(':')

                network = dict(zip(params, fields))

                networks.append({
                    'ssid': network.get('SSID'),
                    'mac': network.get('BSSID'),
                    'signal': network.get('SIGNAL'),
                    'band': "2.4 GHz" if int(network['FREQ'].split()[0]) < 2500 else "5 GHz",
                    'protected': False if network.get('SECURITY', '') == "" else True,
                    'connected': network.get('IN-USE') == '*',
                    'known': network.get('SSID') in known_networks
                })

        except subprocess.CalledProcessError as e:
            print(f"Error scanning WiFi networks: {e}")

        return networks

    def connect(self, ssid: str, password: str = None):
        logging.info(f"Connect to SSID: {ssid}")

        # Find out where were connected to
        connection_info = self.get_connection_info()
        # TODO: Connect to this network when reconnect fails

        # Disconnect existing connection
        try:
            subprocess.run(['nmcli', 'device', 'disconnect', 'wlan0'], check=True, text=True, stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)
        except subprocess.CalledProcessError as e:
            # If return code is 6. Then there is no connection.
            # That is okay. Not in other cases

            if e.returncode != 6:
                raise Exception("nmcli error: {} \n=> {}".format(e, e.stderr))

        try:
            # Connect without password. For open or known passwords
            if password is None or password == "":
                result = subprocess.run(['nmcli', 'device', 'wifi', 'connect', ssid],
                                        check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            else:
                # Connect with Passwort (for secured networks)
                result = subprocess.run(
                    ['nmcli', 'device', 'wifi', 'connect', ssid, '--ask'],
                    input=f"{password}\n",
                    check=True,
                    text=True,
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE
                )

            # Überprüfen Sie das Ergebnis und verarbeiten Sie Fehler
            if result.returncode != 0 and result.stderr:
                raise Exception(result.stderr)

            print(f"Successfully connected to {ssid}")
        except subprocess.CalledProcessError as e:
            if e.stderr:
                raise Exception("nmcli error: {} \n=> {}".format(e, e.stderr))
            raise Exception("nmcli error: {}".format(e))
        except FileNotFoundError as e:
            raise FileNotFoundError(e)
        except Exception as e:
            raise Exception(f"Failed to connect: {str(e)}")

        # TODO: Only insert into right exception
        if connection_info:
            result = subprocess.run(['nmcli', 'device', 'wifi', 'connect', connection_info.get('ssid')],
                                    check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
