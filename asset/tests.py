from django.test import TestCase

# Create your tests here.
import os
import time
from kazoo.client import KazooClient
from kazoo.client import ChildrenWatch
from kazoo.client import KazooState
from kazoo.exceptions import NodeExistsError,NoAuthError

class ServiceRegister:
    """
    hosts: 连接的zookeeper主机地址，例如:
        '192.168.10.2:2181,192.168.10.3:2181'
    """
    def __init__(self):
        self.zk = KazooClient(hosts="10.10.47.150:2181",auth_data=[("digest","bocloud:bocloud")])
        self.info = "10.40.10.160:18092"
        self.zk_node = None
        self.node_path = os.path.join('bocloud','services','lycmdb')
        self.children_watch = ChildrenWatch(client=self.zk,path=self.node_path,func=self.watcher)
        self.zk.add_listener(self.conn_state_watcher)
        self.zk.start()
        self.workers = []
        self.is_master = False
        self.running = True
        self.register()

    def __del__(self):
        # 当关闭lycmdb应用时自动关闭zk连接
        self.zk.close()

    def watcher(self,children):
        pass

    def register(self):
        # 创建服务路径
        try:
            self.zk_node = self.zk.create(
                self.node_path + "/" + self.info,
                "",
                ephemeral=True,
                sequence=False,
                makepath=True
            )
        except NodeExistsError as s:
            pass
        except NoAuthError as e :
            error = "connect to zookeeper {} failed, authentication {} failure".format("10.10.47.150:2181", "bocloud")
            print(error)
            self.running = False
            raise Exception(error)

    def close(self):
        self.zk.stop()
        self.zk.close()
        self.running = False

    def conn_state_watcher(self,state):
        if state == KazooState.CONNECTED:
            print("{} connect to zk server {}".format(self.info, "10.10.47.150:2181"))
            if self.zk_node is None:
                print("must call register method first")
                return
