from app.lib.ModuleInterface import ModuleInterface


class Backend:
    _instance = None

    def __init__(self, config = None):
        if self.config is None:
            raise Exception('Backend is configured without config')
            # self.config = config

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.modules = {}
            cls._instance.config = args[0]
        return cls._instance

    def add_module(self, name, module_class):
        if not issubclass(module_class, ModuleInterface):
            raise TypeError(f"{module_class.__name__} is not a subclass of ModuleInterface")

        self.modules[name] = module_class(self.config)

    def list_modules(self):
        return self.modules.keys()

    def get(self, name):
        if name in self.modules:
            return self.modules[name]
        raise AttributeError(f"Modul {name} not found.")

    def __getattr__(self, name):
        return self.get(name)
