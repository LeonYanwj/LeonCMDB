#!/usr/bin/env python3

import xlrd
import time
import json
import os
import winrm
from saltapi import models
from salt import config
from salt import wheel
from salt import client
from asset.models import NewAssetApprovalZone
from concurrent.futures import ThreadPoolExecutor,as_completed
from gevent.socket import wait_read
from paramiko import SSHClient
from paramiko import AutoAddPolicy


class UploadFile(object):

    def __init__(self,fileobj):
        self.fileobj = fileobj
        self.mandatory_fields = ["hostip",'os_type','remote_port','remote_user','remote_password']
        self.response = {
            "error": [],
            "info": [],
            "warning": []
        }

    def __save_file(self,file_obj):
        timesrp = time.time()
        agent_file_name = str(timesrp).split(".")[0]
        if file_obj.name.endswith('.xlsx'):
            with open(r"static/Deploy_agent/%s.xlsx"%agent_file_name,'wb') as destination:
                for chunk in file_obj.chunks():
                    destination.write(chunk)
            return agent_file_name
        else:
            self.response['error'].append("Only Upload xlsx File")
            return False

    def save_sql(self):
        agent_file_name = self.__save_file(self.fileobj)
        if agent_file_name != False:
            data = xlrd.open_workbook(r"static/Deploy_agent/%s.xlsx"%agent_file_name,)
            agent_data_file = r"static/Deploy_agent/%s.xlsx"%agent_file_name
            if os.path.exists(agent_data_file):
                os.remove(agent_data_file)
            table = data.sheet_by_index(0)
            rows_num = table.nrows
            data_list = []
            for r in range(1, rows_num):
                if len(table.row_values(r)) == len(self.mandatory_fields):
                    data_set = {
                        "hostip": table.row(r)[0].value,
                        "os_type": table.row(r)[1].value.upper(),
                        "remote_port": table.row(r)[2].value,
                        "remote_user": table.row(r)[3].value,
                        "remote_password": table.row(r)[4].value
                    }
                    data_list.append(data_set)
                else:
                    # excel文件中数据存在问题
                    self.response['error'].append("There is a problem with excel data")
                    return self.response

            for sqldata in data_list:
                hostip = sqldata.get('hostip')
                host_obj = models.AgentDeployHostMess.objects.filter(hostip=hostip)
                if not host_obj:
                    obj = models.AgentDeployHostMess(**sqldata)
                    obj.save()
        else:
            return self.response


class SaltCtrl(object):

    def __init__(self,request):
        """
        mandatory_fields: 必要字段
        requests: 客户端请求信息
        :param request:
        """
        self.request = request
        self.mandatory_fields = ["ids"]
        self.response = {
            'status': 0,
            'error': [],
            'info': [],
            'warning': []
        }
        self.accept_host = []
        self.SshConnectErrorHost = []
        self.nginx_server = "39.97.104.43:80"

    def mandatory_check(self, data, only_check_sn=False):
        """合法性检查，要求客户端发过来的数据必须包括指定的字段"""
        for field in self.mandatory_fields:
            if field not in data:
                self.response["error"].append( "Datafielderror: %s"% field)

        else:
            if self.response['error']:
                return False

    def data_is_valid(self):
        data = self.request.POST.get('deploy_data')
        if data:
            try:
                data = json.loads(data)
                self.mandatory_check(data)   # False
                self.clean_data = data
                if not self.response.get('error'):
                    return True
            except ValueError as e:
                self.response['error'].append("AssetDataInvalid: %s"%str(e))
        else:
            self.response['error'].append("data not found: The reported asset data is not valid or provided")

    def thread_pool(self,thread_num=5):
        deploy_pool = ThreadPoolExecutor(thread_num)
        if self.clean_data.get("ids") and not self.response.get("error"):
            runtime_list = []
            for id in self.clean_data.get("ids"):
                runtime = deploy_pool.submit(self.__deploy_agent,id)
                runtime_list.append(runtime)
            for future in as_completed(runtime_list):
                future.result()
        else:
            self.response['error'].append("check_error: mandatory_check fields error")

    def __deploy_agent(self,id):
        """
        1. 需要获取到主机的信息，self.clean_data
        2. 判断主机是那种系统
        3. 通过反射系统名称
        :return:
        """
        models_obj = models.AgentDeployHostMess.objects.filter(id=int(id)).first()
        os_type = models_obj.os_type
        os_data = {
            "os_type":os_type,
            "hostip":models_obj.hostip,
            "remote_port":models_obj.remote_port,
            "remote_user":models_obj.remote_user,
            "remote_password":models_obj.remote_password
        }
        func = getattr(self,"_deploy_%s"%os_type.upper())
        func(os_data)
        if not self.response.get('error') and os_data['hostip'] not in self.SshConnectErrorHost:
            self.response["info"].append("agent部署完毕")
            try:
                models_obj.state = 0
                models_obj.save()
                self.response["info"].append("数据库更新完毕")
                self.accept_host.append(os_data['hostip'])
                # self.__newAssetApprovalZoneAppend(os_data['hostip'])
            except Exception as e:
                self.response['warning'].append("数据库更新失败")
        else:
            # 安装失败
            models_obj.state = 3
            models_obj.save()

    def publicKeyAccept(self,count=0,timeout=2):
        """
        实现功能： 将agent安装的数据同步到cmdb中间表中
        1. 查看资产中间表中是否有这条数据
        """
        time.sleep(2)  # 需要等待一秒钟salt-minion才能启动
        opts = config.master_config("/etc/salt/master")
        salt_wheel = wheel.WheelClient(opts)
        accept_host_str = ",".join(self.accept_host)
        minion_dict = salt_wheel.cmd('key.accept',[accept_host_str])
        while count <= 10:
            if not minion_dict.get("minions"):
                minion_dict = salt_wheel.cmd('key.accept', [accept_host_str])
                count += 1
                time.sleep(timeout)
            else:
                break
        if len(minion_dict.get("minions")) == len(self.accept_host):
            # 通过公钥认证的服务器数量和选择的主机一致
            self.__newAssetApprovalZoneAppend()
        else:
            accept_host_list = accept_host_str.split(",")
            self.__newAssetApprovalZoneAppend(accept_host_list)
        return self.response

    def __newAssetApprovalZoneAppend(self,host_list=None):
        """
        1. host_list为主机列表['10.20.10.11','10.20.110.11']
        2. host_list如何为None的时候默认按照self.host_appect中的主机安装，这个代表是所有主机检测公钥成功了
        """
        time.sleep(10)
        local = client.LocalClient()
        if host_list == None:
            host_Allmess = local.cmd(self.accept_host,"grains.items",tgt_type='list')
        else:
            host_Allmess = local.cmd(host_list,"grains.items",tgt_type='list')
        for ipaddr in self.accept_host:
            host_mess = host_Allmess.get(ipaddr)
            if host_mess:
                if host_mess.get("kernel").lower() == "windows":
                    sn = host_mess.get("serialnumber")
                    disk_info = local.cmd(ipaddr, "disk.usage")
                    disk_total = 0
                    for disk in disk_info.get(ipaddr):
                        disk_total += int(disk_info[ipaddr][disk]["1K-blocks"] / 1024 / 1024)
                else:
                    # 这里Linux不适用serialnumber的原因是在测试环境中所有虚拟机的sn一致，导致只能使用uuid
                    disks = host_mess.get("disks")
                    disk_total = 0
                    for v in disks:
                        disk_info = local.cmd(ipaddr, 'disk.dump', ['/dev/%s' % v])
                        disk_size = int(disk_info[ipaddr].get("getsize64"))
                        disk_size_GB = disk_size / (1024 * 1024 * 1024)
                        disk_total += disk_size_GB
                    sn = host_mess.get('uuid')
                data = {
                    "name": host_mess.get('fqdn'),
                    "service_ip": ipaddr,
                    "os_type": host_mess.get('kernel'),
                    "os_name": host_mess.get("osfullname"),
                    "os_version": host_mess.get("osrelease"),
                    "os_bits": host_mess.get("osarch"),
                    "cpu_logic_count": host_mess.get("num_cpus"),
                    "cpu_model": host_mess.get("cpu_model"),
                    "mem_size": host_mess.get("mem_total"),
                }
                interface = host_mess.get("ip4_interfaces")
                interface_list = [k for k, v in interface.items() if ipaddr in v]
                interface_name = interface_list[0]
                serviceMac = host_mess["hwaddr_interfaces"].get(interface_name)
                data["disk_size"] = disk_total
                data["serviceMac"] = serviceMac
                new_asset = {
                    "internal_ipaddr": ipaddr,
                    "sn": sn,
                    "data": json.dumps(data)
                }
                asset_obj = NewAssetApprovalZone.objects.filter(internal_ipaddr=ipaddr,sn=sn)
                if not asset_obj:
                    NewAssetApprovalZone.objects.get_or_create(**new_asset)
                    self.response['info'].append("%s Has been added to NewAssetApprovalZone"%ipaddr)
                else:
                    asset_obj.update(data=json.dumps(data))
                    self.response['info'].append("%s Has been update"%ipaddr)
            else:
                self.response['error'].append("%s unknown mistake" % ipaddr)

    def executor(self,command,os_data,powershell=False):
        try:
            __host = os_data.get("hostip")
            __port = os_data.get("remote_port")
            __user = os_data.get("remote_user")
            __password = os_data.get("remote_password")
            __os_type = os_data.get("os_type")
        except Exception as e:
            self.response['error'].append("KeyError: Unable to get the specified data")
            return False
        if __os_type.lower() == "linux":
            try:
                ssh_client = SSHClient()
                ssh_client.set_missing_host_key_policy(AutoAddPolicy())
                try:
                    ssh_client.connect(__host, __port, __user, __password, timeout=5)
                    stdin, stdout, stderr = ssh_client.exec_command(command, get_pty=True)
                    while True:
                        next_line = stdout.readline()
                        print(next_line.strip())
                        if not next_line:
                            break
                    status = stdout.channel.recv_exit_status()
                    if status != 0:
                        self.response['error'].append("ExecuteError: execute shell return code is not 0")
                    ssh_client.close()
                except Exception as e:
                    self.SshConnectErrorHost.append(__host)
                    self.response['warning'].append("DeployError: %s" % str(e))
            except Exception as e:
                self.response['error'].append("SshConnectError: 连接服务器失败")
        elif __os_type.lower() == "windows":
            try:
                winHost = winrm.Session("http://%s:5985/wsman"%__host,(__user,__password))
                if powershell == True:
                    execute_command = winHost.run_ps(command)
                else:
                    execute_command = winHost.run_cmd(command)
            except Exception as e:
                self.response['error'].append("ConnectHostError: can not connect windows host")
        elif __os_type.lower() == "aix":
            pass
        else:
            self.response['warning'].append("SystemError: %s Does not support current system type installation agent"%__os_type)

    def _deploy_LINUX(self,os_data):
        '''
        args: os_data，包含了本次需要操作的主机、用户名、密码等信息
        '''
        self.executor("curl -o /tmp/linux_agent_pro.sh http://%s/download/linux_agent_pro.sh"%self.nginx_server,os_data)
        self.executor("dos2unix /tmp/linux_agent_pro.sh && bash /tmp/linux_agent_pro.sh -m client -g %s -A 10.20.1.51"%self.nginx_server,os_data)
        # self.__runCode("which sdfsdf",args)

    def _deploy_WINDOWS(self,os_data):
        '''
        1. 需要安装pywinrm
        2. windows机器上需要开启winrm的一些配置
        '''
        self.executor(r"rd C:\tmpsalt",os_data)
        self.executor(r"md C:\tmpsalt",os_data)
        self.executor(r"(New-Object System.Net.WebClient).DownloadFile('http://%s/download/windows_agent.bat','C:\tmpsalt\windows_agent.bat')"%self.nginx_server,os_data,powershell=True)
        self.executor(
            r"(New-Object System.Net.WebClient).DownloadFile('http://%s/download/Salt-Minion-3000.2-Py2-AMD64-Setup.exe','C:\tmpsalt\Salt-Minion-3000.2-Py2-AMD64-Setup.exe')"%self.nginx_server,
            os_data,
            powershell=True
        )
        self.executor(r"C:\tmpsalt\windows_agent.bat %s"%("10.20.1.27"),os_data)

    def _deploy_AIX(self):
        pass


class MySSHClient(SSHClient):
    # 实现paramiko动态输出结果，因为此方法输出结果不是我想要，所以已经被弃用
    def _forward_bound(self, channel, callback, *args):
        try:
            while True:
                wait_read(channel.fileno())
                data = channel.recv(1024).decode("utf-8")
                if not len(data):
                    return
                callback(data,*args)
        finally:
            self.close()

    def run(self,command,callback,*args):
        stdin,stdout,stderr = self.exec_command(
            command,get_pty=True
        )
        self._forward_bound(stdout.channel,callback,*args)

        return stdin,stdout,stderr