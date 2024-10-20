import logging
import subprocess
import time


def get_known_networks():
    known_networks = set()
    try:
        # Use nmcli to list saved WiFi connections
        result = subprocess.run(['nmcli', '-t', '-f', 'SSID', 'connection'], stdout=subprocess.PIPE)
        output = result.stdout.decode('utf-8').strip().split('\n')

        for line in output:
            known_networks.add(line.strip())  # Add each known SSID to the set

    except subprocess.CalledProcessError as e:
        print(f"Error retrieving known WiFi networks: {e}")

    return known_networks


# Scan for available WiFi networks
def scan_wifi():
    networks = []
    known_networks = []  # Does not work get_known_networks()  # Get the list of known networks

    # TODO: Remove dev
    # time.sleep(1)
    # return [{'ssid': 'WLAN-12358', 'mac': '3C-37-12-08-8F-D7', 'signal': '99', 'band': '2.4 GHz', 'protected': True, 'connected': False, 'known': False}, {'ssid': 'WLAN-85321', 'mac': '3E-37-12-08-8F-D7', 'signal': '99', 'band': '2.4 GHz', 'protected': True, 'connected': False, 'known': False}, {'ssid': 'WLAN-85321', 'mac': '3E-37-12-08-8F-D8', 'signal': '57', 'band': '5 GHz', 'protected': True, 'connected': False, 'known': False}, {'ssid': 'WLAN-12358', 'mac': '3C-37-12-08-8F-D8', 'signal': '57', 'band': '5 GHz', 'protected': True, 'connected': True, 'known': False}, {'ssid': 'DIRECT-9x-EPSON-ET-2870 Series', 'mac': '66-C6-D2-22-72-B9', 'signal': '50', 'band': '2.4 GHz', 'protected': True, 'connected': False, 'known': False}, {'ssid': 'Home S.A 2,4G', 'mac': '98-9B-CB-08-4D-50', 'signal': '35', 'band': '2.4 GHz', 'protected': True, 'connected': False, 'known': False}, {'ssid': 'FRITZ!Box 7530 VI', 'mac': '0C-72-74-0E-29-42', 'signal': '40', 'band': '2.4 GHz', 'protected': True, 'connected': False, 'known': False}, {'ssid': 'MagentaWLAN-WYMW', 'mac': '4C-22-F3-3D-08-0E', 'signal': '32', 'band': '2.4 GHz', 'protected': True, 'connected': False, 'known': False}, {'ssid': 'Eischbi Gast', 'mac': 'E2-28-6D-26-FF-62', 'signal': '20', 'band': '2.4 GHz', 'protected': True, 'connected': False, 'known': False}]

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


def connect_to_wifi(ssid, password=None):
    try:
        # Trennen Sie alle bestehenden Verbindungen
        subprocess.run(['nmcli', 'device', 'disconnect', 'wlan0'], check=True)

        # Verbindung ohne Passwort (für offene Netzwerke)
        if password is None or password == "":
            result = subprocess.run(['nmcli', 'device', 'wifi', 'connect', ssid],
                                    check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:
            # Verbindung mit Passwort (für geschützte Netzwerke)
            result = subprocess.run(['nmcli', 'device', 'wifi', 'connect', ssid, 'password', password],
                                    check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Überprüfen Sie das Ergebnis und verarbeiten Sie Fehler
        if result.returncode != 0:
            raise Exception(result.stderr.decode('utf-8'))

        print(f"Successfully connected to {ssid}")
    except subprocess.CalledProcessError as e:
        raise Exception(f"nmcli error: {e.stderr.decode('utf-8')}")
    except Exception as e:
        raise Exception(f"Failed to connect: {str(e)}")