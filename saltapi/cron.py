# -*- coding:UTF-8 -*-
__author__ = "Leon"

from asset import models
from salt import runner
from salt import config
from salt import client

class SaltGet(object):
    pass

def realtimeinformation():
    '''
    1 先获取主机资源
    2. minion_dict: 查看所有salt-minion状态
    3 minion_live_set：所有存活minion主机集合
    4 Host_set 审批后主机列表中的主机
    down_host_set: minion关闭的主机
    execute_host_set: 存活的minion主机
    __version__: 测试执行版本
    '''
    master_config = config.master_config("/etc/salt/master")
    status_runer = runner.RunnerClient(master_config)
    try:
        minion_dict = status_runer.cmd("manage.status")
        minion_live_set = set(minion_dict.get('up'))
        Host_set = set(models.HostBasicInformation.objects.values_list("serviceIp",flat=True))
        execute_host_set = Host_set & minion_live_set
        down_host_set = Host_set - minion_live_set
        local = client.LocalClient()
        data = local.cmd(
            list(execute_host_set),
            ["disk.usage","ps.cpu_percent","ps.virtual_memory"],
            [[],[],[]],
            tgt_type="list",
        )
        for host in list(execute_host_set):
            related_host = models.HostBasicInformation.objects.get(serviceIp=host)
            host_data = data.get(host)
            cpu_usage = host_data.get("ps.cpu_percent")
            used_disk_size = 0
            total_disk_size = 0
            for disk in host_data.get("disk.usage"):
                used_disk_size += int(host_data['disk.usage'][disk]["used"])
                total_disk_size += int(host_data['disk.usage'][disk]["1K-blocks"])
            disk_usage = round(used_disk_size * 100 / total_disk_size,2)
            mem_usage = float(host_data["ps.virtual_memory"]["percent"])
            monitor_data = {
                "cpu_usage": cpu_usage,
                "mem_usage": mem_usage,
                "disk_usage": disk_usage,
                "hostbasicinformation": related_host
            }
            models.RealTimeInformation.objects.create(**monitor_data)
    except Exception as e:
        print(e)