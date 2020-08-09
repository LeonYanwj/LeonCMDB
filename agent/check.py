#!/usr/bin/python
#-*- coding: utf-8 -*-
import re
import os
import time
import logging
import paramiko

logging.basicConfig(
    format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',
    level=logging.INFO
)
def run(host,port,username,password,enable):
    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    ssh.connect(hostname=host,port=port,username=username,password=password,timeout=5)
    ssh_shell = ssh.invoke_shell()
    cmd = ["show interface stats  \n       "]
    check_field = ['']
    for m in cmd:
        command = ssh_shell.sendall(m)
        time.sleep(1)
        res = ssh_shell.recv(999999).strip()
        with open("interface.out",'wb') as f:
            f.write(res)
            lines = open("interface.out").readlines()
            open("interface.out", 'wb').writelines(lines[1:])
            f.close()
        interface = open("interface.out","rb").read()
        search = re.findall(r"(^[A-Z]{1}.*)\s*\w+\s*\w+\s*\w+\s*\w+\s*\w+\s*\w+\s*\w+\s*\w+\s*\w+\s*\w+\s*\w+\s*\w+\s*\w+\s*\w+\s*\w+\s*\w+\s*\w+\s*\w+\s*\w+\s*\w+\s*\w+\s*\w+\s*\w+\s*(\w+)\s*\w+\s*(\w+)",interface, re.M)
        for item in search:
            access = item[0].split("\r")[0]
            try:
                in_charts = int(item[1]) / 1024
            except Exception as e :
                in_charts = 0
            try:
                out_charts = int(item[2]) / 1024
            except Exception as e:
                out_charts = 0
            print("当前交换机IP地址：%s, 端口%s,进站流量%skb,出站流量%skb"%(host,access,in_charts,out_charts))
            #https://blog.51cto.com/cisco130/1061432
    os.remove("interface.out")
    ssh.close()


if __name__ == '__main__':
    run("10.10.109.253",22,"cisco","cisco","enable") #@
    "".strip()
    # run(HOST,PORT,USERNAME,PASSWORD,ENABLE) #@
