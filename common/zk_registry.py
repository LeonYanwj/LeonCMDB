# -*- coding:UTF-8 -*-
__author__ = "Leon"

import os
import socket
import time
import random
import logging
from kazoo.client import KazooClient
from kazoo.client import KazooState
from kazoo.exceptions import NodeExistsError,NoAuthError
from common.utils import ZOOKEEPER_CONFIG
from common.utils import get_local_ip

class ServiceRegister:
    """
    hosts:  the connection string for zk server, such as
            '10.0.1.1:2181,10.0.1.2:2181'

    The object should be created after service has been started successfully.
    """

    def __init__(self):
        self._hosts = ZOOKEEPER_CONFIG['host']
        self._port = ZOOKEEPER_CONFIG['port']
        self.info = get_local_ip()
        self._zk_path = ZOOKEEPER_CONFIG["zk_path"]
        self.auth_info = ZOOKEEPER_CONFIG['zk_auth_data']
        self.zk = KazooClient(
            hosts=self._hosts+":"+self._port,
            auth_data=[("digest",self.auth_info)]
        )
        self.zk.add_listener(self.conn_state_watcher)
        self.zk.start()
        self.register()

    def conn_state_watcher(self,state):
        if state == KazooState.CONNECTED:
            print("{} connect to zk server {}".format(self.info, self._hosts))
        elif state == KazooState.LOST:
            # 重新注册
            self.register()
        else:
            print("listener state %s" % state)

    def discover(self):
        ret = self.zk.get_children(self._zk_path)
        @self.zk.ChildrenWatch(self._zk_path)
        def watch_children(children):
            print("子节点变化了（需要更新服务列表了）: %s" % children)

    def register(self):
        # 创建lycmdb服务路径
        try:
            self.zk_node = self.zk.create(
                self._zk_path + "/" + self.info,
                b"",
                ephemeral=True,
                sequence=False,
                makepath=True
            )
        except NodeExistsError as s:
            pass
        except NoAuthError as e :
            error = "connect to zookeeper {} failed, authentication {} failure".format(self._hosts,self.auth_info)
            print(error)
            raise  Exception(error)

    def close(self):
        self.zk.stop()
        self.zk.close()

    def __del__(self):
        # 当关闭lycmdb服务的时候自动断开与zookeeper连接

        self.zk.close()

