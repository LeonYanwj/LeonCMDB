from django.apps import AppConfig
from common.utils import LyCMDB_CONFIG_FILE

class AssetConfig(AppConfig):
    name = 'asset'

    def ready(self):
        import threading
        from common.zk_registry import ServiceRegister
        zk = ServiceRegister()
        zk_thread = threading.Thread(target=zk.start_zk)
        zk_thread.setName('zk-thread')
        zk_thread.setDaemon(True)
        zk_thread.start()