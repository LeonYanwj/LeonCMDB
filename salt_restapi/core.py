#!/usr/bin/env python3

import xlrd
import time
import json
import paramiko
from salt_restapi import  models

class UploadFile(object):

    def __init__(self,fileobj):
        self.fileobj = fileobj
        self.mandatory_fields = ["hostip",'os_type','remote_port','remote_user','remote_password']
        self.response = {
            "errors": [],
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
            self.response['errors'].append("Only Upload xlsx File")
            return False

    def save_sql(self):
        agent_file_name = self.__save_file(self.fileobj)
        if agent_file_name != False:
            data = xlrd.open_workbook(r"static/Deploy_agent/%s.xlsx"%agent_file_name,)
            table = data.sheet_by_index(0)
            rows_num = table.nrows
            data_list = []
            for r in range(1, rows_num):
                if len(table.row_values(r)) == len(self.mandatory_fields):
                    data_set = {
                        "hostip": table.row(r)[0].value,
                        "os_type": table.row(r)[0].value,
                        "remote_port": table.row(r)[2].value,
                        "remote_user": table.row(r)[3].value,
                        "remote_password": table.row(r)[4].value
                    }
                    data_list.append(data_set)
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
        self.mandatory_fields = ["hostip","os_type","remote_port","remote_user","remote_password"]
        self.response = {
            'status': 0,
            'error': [],
            'info': [],
            'warning': []
        }

    def mandatory_check(self, data, only_check_sn=False):
        """合法性检查，要求客户端发过来的数据必须包括指定的字段"""
        for field in self.mandatory_fields:
            if field not in data:
                self.response["error"].apeend( "MandatoryCheckFailed The field [%s] is mandatory and not provided in your reporting data"% field)

        else:
            if self.response['error']:
                return False

    def get