import os
import subprocess
from typing import Optional

class SystemProxy:
    """
    Manage system-wide proxy settings via /etc/environment.

    Args:
        config (dict): Configuration dictionary with optional keys:
            - 'env_file' (str): Path to environment file (default: '/etc/environment')
    """

    def __init__(self, config: dict):
        self.config = config
        self.env_file = config.get('env_file', '/etc/environment')

    def get_proxy(self) -> dict[str, Optional[str]]:
        """
        Read current proxy settings from environment file.

        Returns:
            dict[str, Optional[str]]: Proxy settings for http, https, ftp, no_proxy.
        """
        proxies = {"http": None, "https": None, "ftp": None, "no_proxy": None}
        try:
            with open(self.env_file) as f:
                for line in f:
                    for key in proxies:
                        if line.strip().startswith(f"{key}_proxy="):
                            value = line.split("=", 1)[1].strip().strip('"').strip("'")
                            proxies[key] = value
        except Exception:
            pass
        return proxies

    def set_proxy(
        self,
        http: Optional[str] = None,
        https: Optional[str] = None,
        ftp: Optional[str] = None,
        no_proxy: Optional[str] = None,
    ) -> bool:
        """
        Set or update proxy settings in environment file.

        Args:
            http (str|None): HTTP proxy URL.
            https (str|None): HTTPS proxy URL.
            ftp (str|None): FTP proxy URL.
            no_proxy (str|None): Domains/IPs to exclude.

        Returns:
            bool: True on success, False otherwise.
        """
        try:
            env_lines = []
            existing = self.get_proxy()
            updates = {
                "http_proxy": http if http is not None else existing["http"],
                "https_proxy": https if https is not None else existing["https"],
                "ftp_proxy": ftp if ftp is not None else existing["ftp"],
                "no_proxy": no_proxy if no_proxy is not None else existing["no_proxy"],
            }
            # Preserve unrelated lines
            if os.path.exists(self.env_file):
                with open(self.env_file) as f:
                    for line in f:
                        if not any(line.strip().startswith(k) for k in updates):
                            env_lines.append(line.rstrip())

            # Add/replace proxy lines
            for key, val in updates.items():
                if val:
                    env_lines.append(f'{key}="{val}"')

            with open(self.env_file, "w") as f:
                f.write("\n".join(env_lines) + "\n")

            return True
        except Exception:
            return False

    def clear_proxy(self) -> bool:
        """
        Remove all proxy-related entries from environment file.

        Returns:
            bool: True on success, False otherwise.
        """
        try:
            if not os.path.exists(self.env_file):
                return True
            with open(self.env_file) as f:
                lines = f.readlines()
            with open(self.env_file, "w") as f:
                for line in lines:
                    if not any(line.strip().startswith(k) for k in ["http_proxy", "https_proxy", "ftp_proxy", "no_proxy"]):
                        f.write(line)
            return True
        except Exception:
            return False

    def reload_environment(self) -> None:
        """
        Reload systemd user environment to apply changes.

        Note: A full logout/login or reboot might be required for system-wide effect.
        """
        subprocess.run(["systemctl", "--user", "daemon-reexec"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["systemctl", "--user", "import-environment"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
