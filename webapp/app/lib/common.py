import ipaddress
import logging
import sys


def setup_logging(level: int = logging.INFO):
    logging.basicConfig(
        level=level,
        format="%(levelname)s [%(processName)s]::%(threadName)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        stream=sys.stdout
    )

def netmask_to_cidr(netmask):
    try:
        return ipaddress.IPv4Network(f'0.0.0.0/{netmask}').prefixlen
    except ValueError:
        return None

def is_valid_ip(value):
    try:
        ip_address(value)
        return True
    except ValueError:
        return False