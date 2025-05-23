import subprocess
import re
from collections import defaultdict
from typing import Optional

class DNSManager:
    """
    Manage DNS servers per network interface using systemd-resolved (resolvectl).

    Args:
        config (dict): Configuration dictionary with optional keys:
            - 'resolvectl_path' (str): Path to resolvectl binary (default: 'resolvectl')
            - 'default_interface' (str): Default interface name fallback (default: None)
    """

    def __init__(self, config: dict):
        self.config = config
        self.resolvectl = config.get('resolvectl_path', 'resolvectl')
        self.default_interface = config.get('default_interface', None)

    def get_dns_per_interface(self) -> dict[str, list[str]]:
        """
        Get DNS servers for all interfaces.

        Returns:
            dict[str, list[str]]: Mapping interface -> list of DNS server IPs.
        """
        dns_map = defaultdict(list)
        try:
            result = subprocess.run([self.resolvectl, 'status'], capture_output=True, text=True, check=True)
            current_iface = None
            for line in result.stdout.splitlines():
                iface_match = re.match(r'Link \d+ \((\S+)\)', line)
                if iface_match:
                    current_iface = iface_match.group(1)
                elif "DNS Servers" in line and current_iface:
                    servers = line.split(":", 1)[1].strip().split()
                    dns_map[current_iface].extend(servers)
        except Exception:
            pass
        return dict(dns_map)

    def set_dns(self, interface: Optional[str], dns_servers: list[str]) -> bool:
        """
        Set DNS servers for a specific interface.

        Args:
            interface (str|None): Network interface; uses default_interface if None.
            dns_servers (list[str]): DNS servers to set.

        Returns:
            bool: True if successful.
        """
        iface = interface or self.default_interface
        if not iface:
            return False
        try:
            subprocess.run(['sudo', self.resolvectl, 'dns', iface] + dns_servers, check=True)
            return True
        except subprocess.CalledProcessError:
            return False

    def clear_dns(self, interface: Optional[str]) -> bool:
        """
        Revert DNS to default for a specific interface.

        Args:
            interface (str|None): Network interface; uses default_interface if None.

        Returns:
            bool: True if successful.
        """
        iface = interface or self.default_interface
        if not iface:
            return False
        try:
            subprocess.run(['sudo', self.resolvectl, 'revert', iface], check=True)
            return True
        except subprocess.CalledProcessError:
            return False
