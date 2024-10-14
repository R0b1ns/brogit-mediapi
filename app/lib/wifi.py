import subprocess


def scan_wifi():
    """Scan for WiFi networks and return detailed information."""
    networks = []
    try:
        # Scan for available WiFi networks with their frequencies and active status
        result = subprocess.run(['nmcli', '-t', '-f', 'ACTIVE,SSID,FREQ', 'dev', 'wifi'], stdout=subprocess.PIPE)
        output = result.stdout.decode('utf-8')

        # Get known (saved) WiFi connections
        known_connections_result = subprocess.run(['nmcli', '-t', '-f', 'NAME', 'connection', 'show'],
                                                  stdout=subprocess.PIPE)
        known_connections = known_connections_result.stdout.decode('utf-8').split('\n')

        for line in output.split('\n'):
            if line.strip():
                active, ssid, freq = line.split(':')
                band = '2.4 GHz' if freq.startswith('2') else '5 GHz'

                # Create a structured dictionary for each network
                network_info = {
                    'ssid': ssid,
                    'band': band,
                    'connected': active == 'yes',
                    'known': ssid in known_connections
                }
                networks.append(network_info)
    except Exception as e:
        print(f"Error scanning WiFi networks: {e}")
    return networks
