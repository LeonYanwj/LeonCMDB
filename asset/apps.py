from django.apps import AppConfig
from common.utils import LyCMDB_CONFIG_FILE

class AssetConfig(AppConfig):
    name = 'asset'

    def ready(self):
        import threading

        print("123456")