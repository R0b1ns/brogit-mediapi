import ipaddress
import logging
import sys

UNIVERSAL_TRUE_PRI = ('True', 'true', True)
UNIVERSAL_TRUE_SEC = (1, '1')

UNIVERSAL_FALSE_PRI = ('False', 'false', False)
UNIVERSAL_FALSE_SEC = (0, '0')

def universal_bool(v, detect: bool = False) -> bool or None:
    # If we are on detect mode, we can not assume that 1 or '1' is really an bool.
    if v in UNIVERSAL_TRUE_PRI:
        return True

    if v in UNIVERSAL_FALSE_PRI:
        return False

    if not detect:
        return v in UNIVERSAL_TRUE_SEC

    return None

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
        ipaddress.ip_address(value)
        return True
    except ValueError:
        return False

