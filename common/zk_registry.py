# -*- coding:UTF-8 -*-
__author__ = "Leon"

import kazoo
from common.utils import ZOOKEEPER_CONFIG

class ServiceRegister(object):
    """
    hosts: the connection string for zk server, such as
            '10.0.1.1:2181,10.0.1.2:2181'
    The object should be created after service has been started successful
    """

    def __init__(self):
        self._hosts = ZOOKEEPER_CONFIG['host']
        self._zk_path = ZOOKEEPER_CONFIG['zk_path']

    def start_zk(self):
        pass