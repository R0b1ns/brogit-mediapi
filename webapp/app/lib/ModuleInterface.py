# Author: Robin Biegel
# Version: 2026.02.10

class ModuleInterface:
    global_callbacks = {}

    def __init__(self, config = None):
        pass

    @staticmethod
    def get_info():
        return {
            "name": __name__,  # interne id
            "display_name": __name__,
            "icon": "bi-cog",
            "type": "module"  # oder "submodule"
        }

    def install(self, confirm: bool = False) -> bool:
        raise NotImplementedError()

    def uninstall(self, confirm: bool = False) -> bool:
        raise NotImplementedError()

    def on(self, event_name: str, callback):
        """
        Register a callback to be executed when an event is triggered.
        """
        self.__class__.global_callbacks[event_name].append(callback)

    def trigger(self, event_name: str, event_data = None):
        """
        Execute registered callbacks for events
        """
        result = []

        for callback in self.__class__.global_callbacks[event_name]:
            try:
                result.append(callback(event_data))
            except Exception as e:
                result.append(f"Failed to execute callback: {str(e)}")

        return result