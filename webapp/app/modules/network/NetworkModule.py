import subprocess


def get_dns_servers_full() -> list[str]:
    try:
        result = subprocess.run(['resolvectl', 'status'], capture_output=True, text=True, check=True)
        lines = result.stdout.splitlines()
        dns = []
        for line in lines:
            if "DNS Servers" in line:
                dns.extend(line.split(":", 1)[1].strip().split())
        return dns
    except Exception:
        return []

import subprocess

def set_dns(interface: str, dns_servers: list[str]) -> bool:
    """
    Set DNS servers for a specific network interface using systemd-resolved (resolvectl).

    This command overrides the DNS configuration for the given interface at runtime.
    It does not persist across reboots unless also configured in the system's network manager (e.g. Netplan or NetworkManager).

    Args:
        interface (str): The network interface (e.g. 'eth0', 'wlan0').
        dns_servers (list[str]): A list of DNS server IPs to assign.

    Returns:
        bool: True if the DNS settings were successfully applied, False otherwise.
    """
    try:
        subprocess.run(['sudo', 'resolvectl', 'dns', interface] + dns_servers, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def clear_dns(interface: str) -> bool:
    """
    Revert DNS configuration for a specific network interface to its default (typically DHCP-assigned).

    This undoes any manual DNS settings applied via resolvectl and returns the interface to its original state.

    Args:
        interface (str): The network interface to reset (e.g. 'eth0').

    Returns:
        bool: True if the DNS settings were successfully reverted, False otherwise.
    """
    try:
        subprocess.run(['sudo', 'resolvectl', 'revert', interface], check=True)
        return True
    except subprocess.CalledProcessError:
        return False


