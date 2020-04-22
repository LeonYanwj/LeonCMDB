#!/usr/bin/env python3

import xlrd
import time
import json

data = xlrd.open_workbook(r'D:\google download\template_host.xlsx') # function()

class UploadFile(object):

    def __init__(self,file):
        self.file = file
        self.mandatory_fields = ["hostip",'os_type','remote_port','remote_user','remote_password']

    def save_file(self):
        agent_file_name = time.time()
        with open(r"static\Deploy_agent\%s"%agent_file_name,'wb') as destination:
            for chunk in self.file.chunks():
                destination.write(chunk)



