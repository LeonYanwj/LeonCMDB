#_*_coding:utf-8_*_
__author__ = 'Alex Li'

import sys
from plugins.linux import sysinfo
from plugins.linux import sysinfo_v3

def LinuxSysInfo():
    if sys.version_info < (3,4):
        return  sysinfo.collect()
    else:
        return sysinfo_v3.collect()

def WindowsSysInfo():
    from plugins.windows import sysinfo as win_sysinfo
    return win_sysinfo.collect()
