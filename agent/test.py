#!/usr/bin/env python3
__author__ = "Murphy yan"
# agent 批量导入安装

import xlrd
import json

data = xlrd.open_workbook(r'D:\google download\template_host.xlsx') # function()

table = data.sheet_by_index(0)
rows_num = table.nrows
mandatory_fields = ["hostip",'os_type','remote_port','remote_user','remote_password']
for r in range(1,rows_num):
    if len(table.row_values(r)) == len(mandatory_fields):
        hostip = table.row(r)[0]
        os_type = table.row(r)[1]
        remote_port = table.row(r)[2]
        remote_user = table.row(r)[3]
        remote_password = table.row(r)[4]