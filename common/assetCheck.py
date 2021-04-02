# -*- coding:UTF-8 -*-


class AssetCheck(object):

    def __init__(self,request):
        """
        mandatory_fields: 必要字段
        requests: 客户端请求信息
        :param request:
        """
        self.request = request
        self.mandatory_fields = ["ids"]
        self.response = {
            'error': [],
            'info': [],
            'warning': []
        }

        def mandatory_check(self, data, only_check_sn=False):
            """合法性检查，要求客户端发过来的数据必须包括指定的字段"""
            for field in self.mandatory_fields:
                if field not in data:
                    self.response["error"].append("Datafielderror: %s" % field)

            else:
                if self.response['error']:
                    return False