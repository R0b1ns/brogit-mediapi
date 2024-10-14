import logging
import subprocess


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

    try:
        # Use nmcli to scan for WiFi networks with security info
        result = subprocess.run(['nmcli', '-t', '-f', 'SSID,BSSID,FREQ,SECURITY,IN-USE', 'dev', 'wifi'],
                                stdout=subprocess.PIPE)
        output = result.stdout.decode('utf-8').strip().split('\n')

        for line in output:
            print(line)
            line = line.replace('\\:', '-')
            fields = line.split(':')
            if len(fields) >= 4:
                ssid = fields[0]

                mac = fields[1]

                # Extract the frequency and convert to integer
                freq_str = fields[2].split()[0]  # Get the numeric part (e.g. '2437')
                frequency = int(freq_str)

                # Determine band based on frequency
                band = "2.4 GHz" if frequency < 2500 else "5 GHz"

                security = fields[3]  # This field contains security info
                connected = fields[4] == '*'  # '*' means connected

                # Check if the network is protected (has security)
                protected = False if security == "" else True
                # Check if the network is known
                known = ssid in known_networks

                networks.append({
                    'ssid': ssid,
                    'mac': mac,
                    'band': band,
                    'protected': protected,
                    'connected': connected,
                    'known': known
                })

    except subprocess.CalledProcessError as e:
        print(f"Error scanning WiFi networks: {e}")

    return networks
