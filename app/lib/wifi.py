import subprocess


def scan_wifi():
    """Scan for WiFi networks using a system command."""
    networks = []
    try:
        # Run the system command to scan for WiFi networks (example for Linux using 'nmcli')
        result = subprocess.run(['nmcli', '-t', '-f', 'SSID', 'dev', 'wifi'], stdout=subprocess.PIPE)
        output = result.stdout.decode('utf-8')
        # Process the output to get a list of SSIDs
        networks = [line.strip() for line in output.split('\n') if line.strip()]
    except Exception as e:
        print(f"Error scanning WiFi networks: {e}")
    return networks