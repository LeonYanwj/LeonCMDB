# -*- coding:UTF-8 -*-
#!/usr/bin/env python

import json
from asset import models

class Asset(object):

    def __init__(self,request):
        self.request = request
        self.response = {
            'error': [],
            'info': [],
            'warning': []
        }

    def mandatory_check(self,data):
        pass


    def data_is_valid_without_id(self,db_obj=None):
        if db_obj:
            data = db_obj.data
            if data:
                try:
                    data = json.loads(data)

                except Exception as e:
                    self.response['error'].append(e)
            else:
                self.response['error'].append("The reported asset data is not valid or provided")
        else:
            self.response['error'].append("current api not open")
            return False
