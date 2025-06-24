from app.lib.ModuleInterface import ModuleInterface


class GmrenderResurrectModule(ModuleInterface):
    @staticmethod
    def get_info():
        return {
            "name": "gmrender-resurrect",  # interne id
            "display_name": "GmrenderResurrect",
            "icon": "bi-cog",
            "type": "submodule",
            'has_settings': True
        }

    @staticmethod
    def get_license():
        return open('../modules/gmrender-resurrect/repositories/gmrender-resurrect/COPYING').read()
