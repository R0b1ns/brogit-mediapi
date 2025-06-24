from app.lib.ModuleInterface import ModuleInterface


class ShairportSyncModule(ModuleInterface):
    @staticmethod
    def get_info():
        return {
            "name": "shairport-sync",  # interne id
            "display_name": "ShairPort-Sync",
            "icon": "bi-cog",
            "type": "submodule",
            'has_settings': True
        }

    @staticmethod
    def get_license():
        return open('../modules/shairport-sync/repositories/shairport-sync/LICENSES').read()
