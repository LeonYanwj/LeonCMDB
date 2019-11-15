#!/usr/bin/env python
import re
import subprocess

def diskinfo():
    '''
    dic_data: 存放获取到的磁盘信息
    disk_list: 所有的磁盘设备名称
    :return: {'physical_disk_driver':data}
    '''
    f = subprocess.Popen('fdisk -l',shell=True,stdout=subprocess.PIPE).stdout.read().decode('utf-8')
    disk_list = []
    raw_data = []
    grep_pattern = ['Vendor', 'Product', 'User Capacity', 'Logical block size', ]
    dic_data = {}
    for line in f.split("\n"):
        if line.startswith('Disk'):
            data = re.findall(r'Disk \/dev\/[a-z]{3}:',line)
            if data:
                disk_device_name = re.search(r'(Disk) (?P<name>\/dev\/[a-z]{3})',line)
                disk_dic = disk_device_name.groupdict()
                disk_name = disk_dic.get('name')
                disk_list.append(disk_name)
    # 第三方共有云在获取磁盘信息的时候使用smartctl无法取值。只能使用fdisk拉取基本属性
    for disk in disk_list:
        res = subprocess.Popen(
            'smartctl  --all %s'%disk,
            shell=True,
            stdout=subprocess.PIPE,
            stdin=subprocess.PIPE
        ).stdout.read().decode('utf-8')
    #通过测试已经获取到了res的信息，进行下一步的验证
        if "%s: Unable to detect device type"%disk in res:
            size = subprocess.Popen("fdisk -l %s |grep Disk |sed -n 1p|awk  '{print $3}'"%disk,shell=True,stdout=subprocess.PIPE).stdout.read().decode('utf-8').strip()
            size_str = size + "GB"
            dic_data["User Capacity"] = size_str
            dic_data["Vendor"] = "Cloud"
            raw_data.append(dic_data)
            dic_data = None
        else:
            for line in res.split('\n'):
                for filter_line in grep_pattern:
                    if line.startswith(filter_line):
                        dic_data[line.split(':')[0].strip()] = line.split(':')[1].strip()
            raw_data.append(dic_data)
            dic_data = None
    return {'physical_disk_driver': raw_data}