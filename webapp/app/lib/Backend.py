class Backend:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
            cls._instance.modules = {}
        return cls._instance

    def add_module(self, name, module_class):
        self.modules[name] = module_class()

    def list_modules(self):
        return self.modules.keys()

    def get(self, name):
        if name in self.modules:
            return self.modules[name]
        raise AttributeError(f"Modul {name} not found.")

    def __getattr__(self, name):
        return self.get(name)
