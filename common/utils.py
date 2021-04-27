# -*- coding:UTF-8 -*-
__author__ = "Leon"

import yaml
import os
import socket

def load_yaml(yaml_file):
    """
    load the data from a yaml file
    : param yaml_file: yaml 文件路徑
    : return:
    """
    # check the yaml file exists
    if not os.path.exists(yaml_file):
        raise Exception('The yaml file: %s does not exist' % yaml_file)

    with open(yaml_file,"r",encoding="utf-8") as stream:
        data_map = yaml.load(stream, Loader=yaml.FullLoader)
        return data_map

def get_local_ip():
    ip = str(LyCMDB_LOCAL_CONFIG["host"])
    if ip == "0.0.0.0":
        ip = get_ip()
    return ip + ":" + str(LyCMDB_LOCAL_CONFIG["port"])

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("10.255.255.255",0))
        ip = s.getsockname()[0]
    except:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

LyCMDB_CONFIG_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'lycmdb.yaml')
ZOOKEEPER_CONFIG = load_yaml(LyCMDB_CONFIG_FILE)["zookeeper"]
LyCMDB_LOCAL_CONFIG = load_yaml(LyCMDB_CONFIG_FILE)["lycmdb"]