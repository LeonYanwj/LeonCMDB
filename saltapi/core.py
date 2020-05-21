#!/usr/bin/env python3

import xlrd
import time
import json
import os
import threading
from saltapi import models
from django.db.models import Q
from django.conf import settings
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
        self.nginx_server = "172.104.181.64:80"

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

    def deploy_agent(self):
        """
        1. 需要获取到主机的信息，self.clean_data
        2. 判断主机是那种系统
        3. 通过反射系统名称
        :return:
        """
        if self.clean_data.get('ids') and not self.response.get('error'):
            for id in self.clean_data.get('ids'):
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
                self.response["info"].append("agent部署完毕")
                if not self.response.get('error'):
                    try:
                        models_obj.state = 0
                        models_obj.save()
                        self.response["info"].append("数据库更新完毕")
                    except Exception as e:
                        self.response['warning'].append("数据库更新失败")
                else:
                    # 安装失败
                    models_obj.state = 3
                    models_obj.save()
        else:
            return False



    def __runCode(self,command,*args,**kwargs):
        """
        1. paramiko执行
        :return:
        """
        host_info = args[0][0]
        try:
            __host = host_info.get("hostip")
            __port = host_info.get("remote_port")
            __user = host_info.get("remote_user")
            __password = host_info.get("remote_password")
        except Exception as e:
            self.response["error"].append( "KeyError:传递的主机信息中有错误")
            return False
        try:
            ssh_client = SSHClient()
            ssh_client.set_missing_host_key_policy(AutoAddPolicy())
            try:
                ssh_client.connect(__host,__port,__user,__password,timeout=5)
                stdin, stdout, stderr = ssh_client.exec_command(command, get_pty=True)
                while True:
                    next_line = stdout.readline().strip()
                    print(next_line)
                    if not next_line:
                        break
                ssh_client.close()
            except Exception as e:
                self.response['error'].append("DeployError: %s"%str(e))
        except Exception as e:
            self.response['error'].append("SshConnectError: 连接服务器失败")

    def _deploy_LINUX(self,*args,**kwargs):
        self.__runCode("mkdir -p /tmp/agents/",args)
        self.__runCode("curl -o /tmp/agents/salt-agent-linux-x86_64.tgz http://172.104.181.64/download/salt-agent-linux-x86_64.tgz",args)
        self.__runCode("tar xf /tmp/agents/salt-agent-linux-x86_64.tgz -C /tmp/agents",args)
        self.__runCode("yum install /tmp/agents/*.rpm -y",args)

    def _deploy_WINDOWS(self):
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