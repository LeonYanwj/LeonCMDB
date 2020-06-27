# -*- coding:UTF-8 -*-
#!/usr/bin/env python

import json
from asset import models
from corefunc.assetCheck import AssetCheck

class Asset(AssetCheck):

    def __init__(self,request):
        AssetCheck.__init__(self,request)
        self.mandatory_fields = ["service_ip","name"]
        self.response = {
            'error': [],
            'info': [],
            'warning': []
        }

    def mandatory_check(self, data,sn):
        """合法性检查，要求客户端发过来的数据必须包括指定的字段"""
        for field in self.mandatory_fields:
            if field not in data:
                self.response["error"].append( "Datafielderror: %s"% field)

        else:
            if self.response['error']:
                return False
        try:
            asset_obj = models.HostBasicInformation.objects.filter(sn=sn)
            if not asset_obj:
                self.save_new_asset(sn)
            else:
                pass
            return True
        except Exception as e:
            self.response['error'].append("AssetdataInvalid: not found asset sn id")
            print(self.response)
            return False

    def data_is_valid(self,db_obj=None):
        if db_obj:
            data = db_obj.data
            if data:
                try:
                    sn = db_obj.sn # 添加一个唯一标识符
                    data = json.loads(data)
                    self.clean_data = data
                    self.mandatory_check(data,sn)
                    if not self.response['error']:
                        # 如果资产信息存在是否需要更新，这个需要考虑是否在此处添加更新接口
                        return True
                except Exception as e:
                    self.response['error'].append(e)
            else:
                self.response['error'].append("The reported asset data is not valid or provided")
        else:
            self.response['error'].append("current api not open")
            return False

    def save_new_asset(self,sn):
        print(123456)

        try:
            models.HostBasicInformation.objects.create(
                name=self.clean_data.get("name"),
                serviceIp=self.clean_data.get("service_ip"),
                serviceMac=self.clean_data.get("serviceMac"),
                os_type=self.clean_data.get("os_type"),
                os_name=self.clean_data.get("os_name"),
                os_version=self.clean_data.get("os_version"),
                os_bits=self.clean_data.get("os_bits"),
                cpu_logic_count=self.clean_data.get("cpu_logic_count"),
                cpu_model=self.clean_data.get("cpu_model"),
                mem_size=self.clean_data.get("mem_size"),
                disk_size=self.clean_data.get("disk_size"),
                sn=sn
            )
        except Exception as e:
            print(e)
