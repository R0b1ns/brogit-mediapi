import subprocess
import asyncio
import os
import logging
from typing import Optional, Dict, List

logger = logging.getLogger(__name__)


class NetworkInterfaceManager:
    """
    Interface to manage Linux network interfaces via a shell script.

    Supports checking link status, retrieving IP information,
    setting static IPs, and enabling DHCP — both synchronously and asynchronously.

    Args:
        config (dict): YAML-loaded dictionary. Expects:
            network:
              network_manager:
                script_path: str (path to shell script)
                default_interface: Optional[str]
                timeout: Optional[int] (seconds)
    """

    def __init__(self, config: dict):
        net_config = config.get('network', {}).get('network_manager', {})
        self.script_path = os.path.abspath(net_config.get(
            'script_path',
            os.path.join(os.path.dirname(__file__), 'network_manager.sh')
        ))
        self.default_interface = net_config.get('default_interface')
        self.timeout = net_config.get('timeout', 5)

        if not os.path.isfile(self.script_path) or not os.access(self.script_path, os.X_OK):
            raise FileNotFoundError(f"Script not found or not executable: {self.script_path}")

    def _get_interface(self, interface: Optional[str]) -> str:
        iface = interface or self.default_interface
        if not iface:
            raise ValueError("No network interface specified.")
        return iface

    def _build_cmd(self, action: str, iface: str, *args: str) -> List[str]:
        return [self.script_path, action, iface] + list(args)

    def _parse_ip_output(self, output: str) -> Dict[str, Optional[str]]:
        result = {'ip': None, 'subnet': None, 'gateway': None, 'method': None}
        for line in output.splitlines():
            if '=' in line:
                key, value = line.strip().split('=', 1)
                if key in result:
                    result[key] = value or None
        return result

    def _run(self, action: str, iface: str, *args: str) -> str:
        cmd = self._build_cmd(action, iface, *args)
        logger.debug(f"Running sync: {' '.join(cmd)}")
        result = subprocess.run(
            cmd, capture_output=True, text=True,
            timeout=self.timeout, check=False
        )
        if result.returncode != 0:
            raise RuntimeError(f"{action} failed: {result.stderr.strip()}")
        return result.stdout.strip()

    async def _run_async(self, action: str, iface: str, *args: str) -> str:
        cmd = self._build_cmd(action, iface, *args)
        logger.debug(f"Running async: {' '.join(cmd)}")
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        try:
            stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=self.timeout)
        except asyncio.TimeoutError:
            proc.kill()
            raise TimeoutError(f"Command '{action}' timed out")

        if proc.returncode != 0:
            raise RuntimeError(f"{action} failed: {stderr.decode().strip()}")
        return stdout.decode().strip()

    # Sync Methods
    def is_connected(self, interface: Optional[str] = None) -> bool:
        """
        Returns True if the interface has carrier/link.
        """
        output = self._run("is_connected", self._get_interface(interface))
        return output == "1"

    def get_ip_info(self, interface: Optional[str] = None) -> Dict[str, Optional[str]]:
        """
        Returns a dictionary with keys: ip, subnet, gateway, method (manual|dhcp).
        """
        output = self._run("get_ip_info", self._get_interface(interface))
        return self._parse_ip_output(output)

    def set_static_ip(self, interface: Optional[str], ip: str, subnet: str, gateway: Optional[str] = None) -> bool:
        """
        Sets a static IP configuration on the interface.
        """
        args = [ip, subnet] + ([gateway] if gateway else [])
        self._run("set_static_ip", self._get_interface(interface), *args)
        return True

    def enable_dhcp(self, interface: Optional[str] = None) -> bool:
        """
        Enables DHCP on the interface using NetworkManager.
        """
        self._run("enable_dhcp", self._get_interface(interface))
        return True

    # Async Methods
    async def is_connected_async(self, interface: Optional[str] = None) -> bool:
        output = await self._run_async("is_connected", self._get_interface(interface))
        return output == "1"

    async def get_ip_info_async(self, interface: Optional[str] = None) -> Dict[str, Optional[str]]:
        output = await self._run_async("get_ip_info", self._get_interface(interface))
        return self._parse_ip_output(output)

    async def set_static_ip_async(self, interface: Optional[str], ip: str, subnet: str, gateway: Optional[str] = None) -> bool:
        args = [ip, subnet] + ([gateway] if gateway else [])
        await self._run_async("set_static_ip", self._get_interface(interface), *args)
        return True

    async def enable_dhcp_async(self, interface: Optional[str] = None) -> bool:
        await self._run_async("enable_dhcp", self._get_interface(interface))
        return True
