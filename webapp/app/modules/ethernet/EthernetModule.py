class EthernetModule:
    def __init__(self):
        # Beispiel interner Status
        self.settings = {
            "dhcp": True,
            "ip": "192.168.0.100",
            "netmask": "255.255.255.0",
            "gateway": "192.168.0.1",
            "connected": True,
        }

    @staticmethod
    def get_info():
        return {
            "name": "ethernet",  # interne id
            "display_name": "Ethernet",
            "icon": "bi-ethernet",
            "type": "module"  # oder "submodule"
        }

    def get_settings(self) -> dict:
        return self.settings

    def set_settings(self, data: dict) -> bool:
        # Validierung (vereinfachtes Beispiel)
        if "dhcp" in data:
            self.settings["dhcp"] = bool(data["dhcp"])
        if not self.settings["dhcp"]:
            for key in ("ip", "netmask", "gateway"):
                if key in data:
                    self.settings[key] = data[key]
        # Hier könntest du Netzwerk-Konfiguration tatsächlich anwenden
        return True

    def action_restart(self, data: dict) -> bool:
        # Beispiel: Netzwerkinterface neu starten
        print("Restarting Ethernet interface...")
        # Hier Neustart-Logik einfügen
        return True

    def action_scan(self, data: dict) -> dict:
        # Beispiel: Netzwerke scannen (Fake-Daten)
        return {
            "available_networks": [
                {"ssid": "Netzwerk1", "strength": 80},
                {"ssid": "Netzwerk2", "strength": 60},
            ]
        }
