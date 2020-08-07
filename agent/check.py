#!/usr/bin/python
#-*- coding: utf-8 -*-
import re
import sys
import time
import logging
import paramiko

logging.basicConfig(
    format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',
    level=logging.INFO
)
def run(host,port,username,password,enable):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    ssh.connect(hostname=host,port=port,username=username,password=password,timeout=5)
    ssh_shell = ssh.invoke_shell()
    cmd = ["show processes mem \n    "]
    check_field = ['']
    for m in cmd:
        command = ssh_shell.sendall(m)
        time.sleep(1)
        res = ssh_shell.recv(999999)
        if "show processes mem" in m:
            print(res.split("\r\n"))
    ssh.close()


if __name__ == '__main__':
    run("10.10.109.253",22,"cisco","cisco","enable") #@
    # run(HOST,PORT,USERNAME,PASSWORD,ENABLE) #@
