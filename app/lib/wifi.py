import subprocess


def scan_wifi():
    """Scan for WiFi networks using a system command."""
    networks = []
    try:
        # Run the system command to scan for WiFi networks (example for Linux using 'nmcli')
        result = subprocess.run(['nmcli', '-t', '-f', 'SSID,FREQ', 'dev', 'wifi'], stdout=subprocess.PIPE)
        output = result.stdout.decode('utf-8')
        # Process the output to get a list of SSIDs and Frequencies
        for line in output.split('\n'):
            if line.strip():
                ssid, freq = line.split(':')
                # Determine if it's 2.4GHz or 5GHz based on frequency
                band = '2.4 GHz' if freq.startswith('2') else '5 GHz'
                networks.append(f"{band} - {ssid.strip()}")
    except Exception as e:
        print(f"Error scanning WiFi networks: {e}")
    return networks