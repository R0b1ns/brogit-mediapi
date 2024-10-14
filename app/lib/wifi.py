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
    known_networks = [] # Does not work get_known_networks()  # Get the list of known networks

    params = {
        'SSID',
        'BSSID',
        'FREQ',
        'BARS',
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

            network = zip(params, fields)

            print(network)
            networks.append({
                'ssid': network.get('SSID'),
                'mac': network.get('BSSID'),
                'bars': network.get('BARS'),
                'band': "2.4 GHz" if int(network['FREQ'].split()[0]) < 2500 else "5 GHz",
                'protected': False if network.get('SECURITY', '') == "" else True,
                'connected': network.get('IN-USE') == '*',
                'known': network.get('SSID') in known_networks
            })

    except subprocess.CalledProcessError as e:
        print(f"Error scanning WiFi networks: {e}")

    return networks
