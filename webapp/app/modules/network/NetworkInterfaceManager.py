import subprocess
import re
from typing import Optional, Dict

class NetworkInterfaceManager:
    """
    Manage network interfaces: check status, get/set IP, subnet mask, gateway,
    and enable DHCP.

    Args:
        config (dict): Configuration dictionary with optional keys:
            - 'ip_cmd' (str): Path to ip command (default: 'ip')
            - 'nmcli_cmd' (str): Path to nmcli command (default: 'nmcli')
            - 'default_interface' (str): Default interface if none provided (default: None)
    """

    def __init__(self, config: dict):
        self.config = config
        self.ip_cmd = config.get('ip_cmd', 'ip')
        self.nmcli_cmd = config.get('nmcli_cmd', 'nmcli')
        self.default_interface = config.get('default_interface', None)

    def _get_interface(self, interface: Optional[str]) -> Optional[str]:
        return interface or self.default_interface

    def is_connected(self, interface: Optional[str]) -> bool:
        """
        Check if the interface is connected (carrier detected).

        Args:
            interface (str|None): Interface name.

        Returns:
            bool: True if connected, False otherwise.
        """
        iface = self._get_interface(interface)
        if not iface:
            return False
        try:
            result = subprocess.run([self.ip_cmd, 'link', 'show', iface], capture_output=True, text=True, check=True)
            # look for "state UP" and "LOWER_UP" indicating connected
            return 'state UP' in result.stdout and 'LOWER_UP' in result.stdout
        except subprocess.CalledProcessError:
            return False

    def get_ip_info(self, interface: Optional[str]) -> Dict[str, Optional[str]]:
        """
        Get IP address, subnet mask (CIDR), and gateway of the interface.

        Args:
            interface (str|None): Interface name.

        Returns:
            dict: { 'ip': str|None, 'subnet': str|None, 'gateway': str|None }
        """
        iface = self._get_interface(interface)
        if not iface:
            return {'ip': None, 'subnet': None, 'gateway': None}

        ip_addr = None
        subnet = None
        gateway = None

        try:
            # Get IP address and subnet CIDR
            result = subprocess.run([self.ip_cmd, '-o', '-f', 'inet', 'addr', 'show', iface],
                                    capture_output=True, text=True, check=True)
            # Output example: "2: eth0    inet 192.168.1.100/24 brd 192.168.1.255 scope global dynamic eth0\n"
            for line in result.stdout.splitlines():
                parts = line.split()
                if 'inet' in parts:
                    idx = parts.index('inet')
                    ip_cidr = parts[idx + 1]
                    ip_addr, subnet = ip_cidr.split('/')
                    break

            # Get gateway via nmcli or ip route
            # Try nmcli first
            try:
                gw_result = subprocess.run([self.nmcli_cmd, '-t', '-f', 'IP4.GATEWAY', 'device', 'show', iface],
                                           capture_output=True, text=True, check=True)
                for line in gw_result.stdout.splitlines():
                    if line.strip():
                        gateway = line.strip()
                        break
            except subprocess.CalledProcessError:
                # fallback to ip route
                route_result = subprocess.run([self.ip_cmd, 'route', 'show', 'dev', iface],
                                              capture_output=True, text=True, check=True)
                for line in route_result.stdout.splitlines():
                    if line.startswith('default via '):
                        gateway = line.split()[2]
                        break
        except Exception:
            pass

        return {'ip': ip_addr, 'subnet': subnet, 'gateway': gateway}

    def set_static_ip(self, interface: Optional[str], ip: str, subnet: str, gateway: Optional[str] = None) -> bool:
        """
        Set static IP, subnet mask (CIDR) and optionally gateway for an interface.

        Args:
            interface (str|None): Interface name.
            ip (str): IP address (e.g. '192.168.1.100').
            subnet (str): Subnet mask as CIDR (e.g. '24').
            gateway (str|None): Gateway IP.

        Returns:
            bool: True if successful.
        """
        iface = self._get_interface(interface)
        if not iface:
            return False

        try:
            # Delete existing IPs on iface
            subprocess.run(['sudo', self.ip_cmd, 'addr', 'flush', 'dev', iface], check=True)
            # Add new IP + subnet
            subprocess.run(['sudo', self.ip_cmd, 'addr', 'add', f'{ip}/{subnet}', 'dev', iface], check=True)
            # Bring interface up
            subprocess.run(['sudo', self.ip_cmd, 'link', 'set', iface, 'up'], check=True)

            # Set gateway if provided
            if gateway:
                # Delete default route if exists
                subprocess.run(['sudo', self.ip_cmd, 'route', 'del', 'default'], check=False)
                subprocess.run(['sudo', self.ip_cmd, 'route', 'add', 'default', 'via', gateway, 'dev', iface], check=True)

            return True
        except subprocess.CalledProcessError:
            return False

    def enable_dhcp(self, interface: Optional[str]) -> bool:
        """
        Enable DHCP on the interface via NetworkManager.

        Args:
            interface (str|None): Interface name.

        Returns:
            bool: True if successful.
        """
        iface = self._get_interface(interface)
        if not iface:
            return False
        try:
            # Use nmcli to set IPv4 method to auto (DHCP)
            subprocess.run(['sudo', self.nmcli_cmd, 'con', 'mod', iface, 'ipv4.method', 'auto'], check=True)
            subprocess.run(['sudo', self.nmcli_cmd, 'con', 'up', iface], check=True)
            return True
        except subprocess.CalledProcessError:
            return False
