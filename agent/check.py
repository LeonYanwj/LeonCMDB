#-*-coding:utf8-*-
import requests

from concurrent.futures import ThreadPoolExecutor

class Multithreading(object):
    def __init__(self,task,*args,**kwargs):
        self.task = task
        self._args = args
        self._kwargs = kwargs

    def run_task(self,thread_num=None,):
        pool = ThreadPoolExecutor(thread_num)
        for item in self.task:
            key = item['url']
            value = item['function']
            future = pool.submit(self.download,key)
            if hasattr(self,value):
                function = getattr(self,value)
                function(future,key)
            else:
                raise KeyError

    def download(self,http_url):
        response = requests.get(http_url,timeout=5)
        return response


    def get_code(self,future,url):
        download_response = future.result()
        print("执行了get_code函数")

url_list = [
    {'url':"http://www.baidu.com",'function':'get_code'},
    {'url':"http://www.12306.cn",'function':'get_code'},
    {'url':"http://www.zimuzu.tv",'function':'get_code'},
]

M = Multithreading(url_list)
M.run_task(3)