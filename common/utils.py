# -*- coding:UTF-8 -*-
__author__ = "Leon"

import yaml
import os

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

LyCMDB_CONFIG_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'lycmdb.yaml')
ZOOKEEPER_CONFIG = load_yaml(LyCMDB_CONFIG_FILE)["zookeeper"]