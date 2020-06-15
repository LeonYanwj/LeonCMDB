# -*- coding:UTF-8 -*-
#!/usr/bin/env python

import json
from asset import models
from corefunc.assetCheck import AssetCheck

class Asset(AssetCheck):

    def __init__(self,request):
        AssetCheck.__init__(self,request)
        self.mandatory_fields = ["service_ip"]

    def data_is_valid(self,db_obj=None):
        if db_obj:
            data = db_obj.data
            if data:
                try:
                    data = json.loads(data)
                    asset_obj = models.Server.objects.filter(serviceIp=data.get("service_ip"))
                    if not asset_obj:
                        pass
                    if not self.response['error']:
                        return True
                except Exception as e:
                    self.response['error'].append(e)
            else:
                self.response['error'].append("The reported asset data is not valid or provided")
        else:
            self.response['error'].append("current api not open")
            return False
