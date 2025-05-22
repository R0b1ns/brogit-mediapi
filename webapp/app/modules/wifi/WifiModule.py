

class WifiModule:

    def is_connected(self) -> bool:
        if self.get_connection_info():
            return True
        else:
            return False

    def get_connection_info(self):
        pass