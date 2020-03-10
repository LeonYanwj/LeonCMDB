#_*_conding:utf-8_*_
__author__ = 'Leonyan'


import os,sys,subprocess
import re
import psutil


def collect():
    filter_keys = ['Manufacturer','Serial Number','Product Name',"UUID",'Wake-up Type']
    raw_data = {}

    for key in filter_keys:
        try:
            cmd_res = subprocess.Popen(
                "sudo dmidecode -t system|grep '%s'"%key,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            ).stdout.read().decode('utf8').strip()
            res_to_list = cmd_res.split(':')
            if len(res_to_list) > 1:
                raw_data[key] = res_to_list[1].strip()
            else:
                raw_data[key] = -1
        except Exception as e:
            print(e)
            raw_data[key] = -2

    data = {"asset_type":'server'}
    data['manufactory'] = raw_data['Manufacturer']
    data['sn'] = raw_data['Serial Number']
    data['model'] = raw_data['Product Name']
    data['uuid'] = raw_data['UUID']
    data['wake_up_type'] = raw_data['Wake-up Type']

    data.update(cpuinfo())
    data.update(osinfo())
    data.update(raminfo())
    data.update(nicinfo())
    data.update(diskinfo())
    return data


def diskinfo():
    '''
    dic_data: 存放获取到的磁盘信息
    disk_list: 所有的磁盘设备名称
    :return: {'physical_disk_driver':data}
    '''
    f = subprocess.Popen('fdisk -l',shell=True,stdout=subprocess.PIPE).stdout.read().decode('utf-8')
    disk_data = f.split("\n\nDisk")
    dic_data = {}
    disk_dict = {}
    raw_data = []
    for partition in disk_data:
        disk_obj = re.findall(r"\/dev\/[a-z]{3}",partition)
        disk_obj = list(set(disk_obj))
        disk_name = disk_obj[0]
        slot_obj = re.findall(r"Disk identifier: .+",partition)
        slot = slot_obj[0].split(":")[1]
        disk_dict[disk_name] = slot

    for disk in disk_dict.keys():
        res = subprocess.Popen(
            'smartctl --all %s'%disk,
            shell=True,
            stdout=subprocess.PIPE,
            stdin=subprocess.PIPE
        ).stdout.read().decode('utf-8')
        if "%s: Unable to detect device type"%disk in res:
            size = subprocess.Popen("fdisk -l %s |grep Disk |sed -n 1p|awk  '{print $3}'"%disk,shell=True,stdout=subprocess.PIPE).stdout.read().decode('utf-8').strip()
            size_str = size
            dic_data["capacity"] = size_str
            dic_data["model"] = "Cloud"
            dic_data['slot'] = disk_dict.get(disk)
            raw_data.append(dic_data)
            dic_data = {}
        else:
            for line in res.split('\n'):
                if line.startswith("Vendor"):
                    dic_data['model'] = line.split(":")[1].strip()
                elif line.startswith("User Capacity"):
                    desc_disk = line.split(":")[1]
                    str_disk = desc_disk.split()[0]
                    size_b = int("".join(re.findall(r'\d+',str_disk)))
                    size_gb = size_b / 1024 / 1024 / 1024
                    dic_data['capacity'] = size_gb
                    dic_data['slot'] = disk_dict.get(disk)
            raw_data.append(dic_data)
            dic_data = {}
    return {'physical_disk_driver': raw_data}


def nicinfo():
    dic_data = {}
    nic_list = []
    nic_dic = psutil.net_if_addrs()

    for device_name,info in nic_dic.items():
        if "lo" not in device_name:
            ipv4 = info[0].address
            netmask = info[0].netmask
            for item in info:
                if item.family.name in {'AF_LINK','AF_PACKET'}:
                    mac = item.address
            dic_data['name'] = device_name
            dic_data['ipaddress'] = ipv4
            dic_data['macaddress'] = mac
            dic_data['netmask'] = netmask
            dic_data['model'] = 'unknown'
            nic_list.append(dic_data)
            dic_data = {}
    return {'nic': nic_list}


def raminfo():
    f = subprocess.Popen("dmidecode -t 17", shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    data = f.stdout.read().decode('utf-8')
    raw_data = data.split('\n')
    raw_ram_list = []  # 拿到的是每一个"Memory Device列表"
    item_list = []  # 在循环的最后一次拿到的是Memory Device信息

    for line in raw_data:
        if line.startswith("Memory Device"):
            raw_ram_list.append(item_list)  # 将数据归档
            item_list = []  # 数据格式化
        else:
            item_list.append(line.strip())

    raw_ram_list.append(item_list)
    raw_list = []

    for item in raw_ram_list:
        item_ram_size = 0
        ram_item_to_dic = {}
        for i in item:
            data = i.split(":")
            if len(data) == 2:
                key, v = data
                if key == 'Size':
                    # print key ,v
                    if v.strip() != "No Module Installed":
                        ram_item_to_dic['capacity'] = v.split()[0].strip()  # e.g split "1024 MB"
                        item_ram_size = int(v.split()[0])
                    else:
                        ram_item_to_dic['capacity'] = 0
                if key == 'Type':
                    ram_item_to_dic['model'] = v.strip()
                if key == 'Manufacturer':
                    ram_item_to_dic['manufactory'] = v.strip()
                if key == 'Serial Number':
                    ram_item_to_dic['sn'] = v.strip()
                if key == 'Asset Tag':
                    ram_item_to_dic['asset_tag'] = v.strip()
                if key == 'Locator':
                    ram_item_to_dic['slot'] = v.strip()
        if item_ram_size == 0:  # empty slot , need to report this
            pass
        else:
            raw_list.append(ram_item_to_dic)

    ram_data = {'ram': raw_list}
    meminfo = subprocess.Popen("cat /proc/meminfo",shell=True,stdout=subprocess.PIPE,stdin=subprocess.PIPE)
    data = meminfo.stdout.read().decode('utf-8')
    mem_list = re.findall(r'MemTotal.*',data)
    memtotal = mem_list[0].split(":")[1].split()[0].strip()  #通过此方式获取到的内存是以KB为单位
    int_memtotal = int(int(memtotal) / 1024)
    ram_data['ram_size'] = int_memtotal

    return ram_data


def osinfo():
    os_info = subprocess.Popen(
        'cat /etc/centos-release',
        shell=True,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE
    ).stdout.read().decode('utf-8')
    data_dic ={
        "os_distribution": os_info.split()[0],
        "os_release":os_info.split("\n")[0],
        "os_type": "Linux",
    }
    return data_dic


def cpuinfo():
    base_cmd = 'cat /proc/cpuinfo'

    raw_data = {
        'cpu_model' : "%s |grep 'model name' |head -1 " % base_cmd,
        'cpu_count' :  "%s |grep  'processor'|wc -l " % base_cmd,
        'cpu_core_count' : "%s |grep 'cpu cores' |awk -F: '{SUM +=$2} END {print SUM}'" % base_cmd,
    }

    for k,cmd in raw_data.items():
        try:
            cmd_res = subprocess.Popen(
                cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            ).stdout.read().decode('utf8')
            raw_data[k] = cmd_res.strip()

        #except Exception,e:
        except ValueError as e:
            print(e)

    data = {
        "cpu_count": raw_data["cpu_count"],
        "cpu_core_count": raw_data["cpu_core_count"]
    }
    cpu_model = raw_data["cpu_model"].split(":")
    if len(cpu_model) > 1:
        data["cpu_model"] = cpu_model[1].strip()
    else:
        data["cpu_model"] = -1

    return data


if __name__=="__main__":
    print(collect())
