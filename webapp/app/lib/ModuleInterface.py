# Author: Robin Biegel
# Version: 2026.02.10
import logging


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
        if event_name not in self.global_callbacks:
            self.__class__.global_callbacks.update({event_name: [callback,]})
        else:
            self.__class__.global_callbacks[event_name].append(callback)

        logging.debug(f"Registered callback {self.__class__.__name__}.on({event_name}, {callback})")
        print(f"Registered callback {self.__class__.__name__}.on({event_name}, {callback})")

    def trigger(self, event_name: str, event_data = None):
        """
        Execute registered callbacks for events
        """
        result = []

        callbacks = self.__class__.global_callbacks[event_name]

        logging.debug(f"{self.__class__.__name__}.trigger({event_name}, {event_data})")
        logging.debug(f"{callbacks}")

        for callback in callbacks:
            try:
                result.append(callback(event_data))
            except Exception as e:
                result.append(f"Failed to execute callback: {str(e)}")

        return result


if __name__ == "__main__":
    # TODO: Test on and trigger method
    m = ModuleInterface()
    n = ModuleInterface()

    def cb(event_data):
        print(event_data)
    m.on('set_hostname', cb)
    n.on('set_hostname', cb)

    m.trigger('set_hostname', "Hallo Welt")
