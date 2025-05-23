from app.lib.ModuleInterface import ModuleInterface


class GmrenderResurrectModule(ModuleInterface):
    @staticmethod
    def get_info():
        return {
            "name": "gmrender-resurrect",  # interne id
            "display_name": "GmrenderResurrect",
            "icon": "bi-cog",
            "type": "submodule"  # oder "submodule"
        }

    @staticmethod
    def get_license():
        return open('../modules/gmrender-resurrect/COPYING').read()
