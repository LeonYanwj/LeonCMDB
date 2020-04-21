#!/usr/bin/env python3


import requests
import json

# 使用requests请求https出现警告，做的设置
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


salt_api = "https://10.20.10.24:8000/"


class SaltApi:
    """
    定义salt api接口的类
    初始化获得token
    """
    def __init__(self, url):
        self.url = url
        self.username = "saltapi"
        self.password = "adminapi"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36",
            "Content-type": "application/json"
        }
        # self.params = {'client': 'local', 'fun': '', 'tgt': ''}
        self.login_url = salt_api + "login"
        self.login_params = {'username': self.username, 'password': self.password, 'eauth': 'pam'}
        try:
            self.token = self.get_data(self.login_url, self.login_params)['token']
            self.headers['X-Auth-Token'] = self.token
        except Exception as e:
            print("账号或者是用户名出错")
            exit(2)

    def get_data(self, url, params):
        send_data = json.dumps(params)
        request = requests.post(url, data=send_data, headers=self.headers, verify=False)
        response = request.json()
        result = dict(response)
        return result['return'][0]

    def salt_command(self, tgt, method, arg=None):
        """远程执行命令，相当于salt 'client1' cmd.run 'free -m'"""
        if arg:
            params = {'client': 'local', 'fun': method, 'tgt': tgt, 'arg': arg}
        else:
            params = {'client': 'local', 'fun': method, 'tgt': tgt}
        result = self.get_data(self.url, params)
        return result

def main():
    salt = SaltApi(salt_api)
    salt_client = '*'
    salt_test = 'test.ping'
    result1 = salt.salt_command(salt_client, salt_test)
    print(result1)

if __name__ == '__main__':
    main()