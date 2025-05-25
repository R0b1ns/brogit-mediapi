import subprocess
import os
import logging
from typing import Optional, List, Dict

logger = logging.getLogger(__name__)

class SystemProxyManager:
    """
    Manage system proxy settings via the system_proxy.sh script.

    Methods support getting current proxy settings,
    setting proxies, and clearing proxy configuration.

    Args:
        config (dict): expects:
            network:
                system_proxy:
                    script_path: str (path to system_proxy.sh)
                    timeout: Optional[int] in seconds
    """

    def __init__(self, config: dict):
        proxy_config = config.get('network', {}).get('system_proxy', {})
        self.script_path = os.path.abspath(proxy_config.get(
            'script_path',
            os.path.join(os.path.dirname(__file__), 'system_proxy.sh')
        ))
        self.timeout = proxy_config.get('timeout', 5)

        if not os.path.isfile(self.script_path) or not os.access(self.script_path, os.X_OK):
            raise FileNotFoundError(f"Script not found or not executable: {self.script_path}")

    def _run(self, action: str, *args: str) -> str:
        cmd = [self.script_path, action] + list(args)
        logger.debug(f"Running: {' '.join(cmd)}")
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=self.timeout,
            check=False
        )
        if result.returncode != 0:
            raise RuntimeError(f"{action} failed: {result.stderr.strip()}")
        return result.stdout.strip()

    def get_proxy(self) -> Dict[str, Optional[str]]:
        """
        Returns a dict with keys: http_proxy, https_proxy, no_proxy.
        Values may be empty strings if not set.
        """
        output = self._run("get_proxy")
        result = {}
        for line in output.splitlines():
            if '=' in line:
                key, val = line.strip().split('=', 1)
                result[key] = val if val else None
        # Ensure keys exist
        for k in ['http_proxy', 'https_proxy', 'no_proxy']:
            result.setdefault(k, None)
        return result

    def set_proxy(self, http_proxy: str, https_proxy: Optional[str] = None, no_proxy: Optional[str] = None) -> None:
        """
        Sets proxy variables. If https_proxy or no_proxy are omitted,
        https_proxy defaults to http_proxy, no_proxy defaults to empty string.
        """
        args = [http_proxy]
        if https_proxy is not None:
            args.append(https_proxy)
        if no_proxy is not None:
            # If https_proxy omitted but no_proxy given, https_proxy must be http_proxy (add if missing)
            if https_proxy is None:
                args.append(http_proxy)
            args.append(no_proxy)
        self._run("set_proxy", *args)

    def clear_proxy(self) -> None:
        """
        Clears proxy environment variables and git proxy config.
        """
        self._run("clear_proxy")
