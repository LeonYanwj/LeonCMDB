#!/usr/bin/env python3

import xlrd
import time
import json


class UploadFile(object):

    def __init__(self,fileobj):
        self.fileobj = fileobj
        self.mandatory_fields = ["hostip",'os_type','remote_port','remote_user','remote_password']

    def __save_file(self,file_obj):
        timesrp = time.time()
        agent_file_name = str(timesrp).split(".")[0]
        if file_obj.name.endswith('.xlsx'):
            with open(r"static\Deploy_agent\%s"%agent_file_name,'wb') as destination:
                for chunk in file_obj.chunks():
                    destination.write(chunk)
        else:
            pass

    def save_sql(self):
        self.__save_file(self.fileobj)


