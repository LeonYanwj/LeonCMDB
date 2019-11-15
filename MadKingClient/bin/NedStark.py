#_*_coding:utf-8_*_
__author__ = 'Leonyan'
import os,sys,platform

#for linux
if platform.system() == "Windows":
    BASE_DIR = '\\'.join(os.path.abspath(os.path.dirname(__file__)).split('\\')[:-1])
    print(BASE_DIR)
else:
    BASE_DIR = '/'.join(os.path.abspath(os.path.dirname(__file__)).split('/')[:-1])
sys.path.append(BASE_DIR)

from core import HouseStark


if __name__ == '__main__':
    #sys.argv:命令行参数List，第一个元素是程序本身路径，第二个就是运行文本后的第一个位置参数
    HouseStark.ArgvHandler(sys.argv)