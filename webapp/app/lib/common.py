import logging
import sys


def setup_logging(level: int = logging.INFO):
    logging.basicConfig(
        level=level,
        format="%(levelname)s [%(processName)s]::%(threadName)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        stream=sys.stdout
    )