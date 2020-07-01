# -*- coding:UTF-8 -*-
__author__ = "Leon"

import json
from asset import models
from salt import runner
from salt import config

def realtimeinformation():
    master_config = config.master_config("/etc/salt/master")
    status_runer = runner.RunnerClient(master_config)
    print(dir(models))
    try:
        minion_dict = status_runer.cmd("manage.status")
        minion_live_set = set(minion_dict.get('up'))
        Host_set = set(models.HostBasicInformation.objects.values_list("serviceIp",flat=True))
        execute_host_set = Host_set & minion_live_set
        down_host_set = Host_set - minion_live_set
        models.EventLog.objects.create(text=json.dumps(execute_host_set))

    except Exception as e:
        pass
