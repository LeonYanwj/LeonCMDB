from asset import models
import json
class PageInfo(object):
    def __init__(self,current_page,per_page_num,all_count,base_url,page_range=7):
        """
        :param current_page: 获取到的页码
        :param per_page_num: 获取到上一下的页码
        :param all_count: 在数据库中总共查询到的数据条目数
        :param base_url: 拼接数的URL
        :param page_range: 页码范围
        """
        try:
            current_page = int(current_page)
        except Exception as e:
            current_page_page = int(1)
        self.current_page = current_page
        self.per_page_num = per_page_num
        self.all_count = all_count
        a,b = divmod(all_count,per_page_num)
        if b != 0:
            #self.all_page 是总页数
            self.all_page = a + 1
        else:
            self.all_count = a
        self.base_url = base_url
        self.page_range = page_range

    def start(self):
        return (self.current_page - 1) * self.per_page_num

    def end(self):
        return self.current_page * self.per_page_num

    def page_str(self):
        """
        在HTML页面中显示页码信息
        :return:
        """
        page_list = []
        if self.current_page <= 1:
            prev = '<li><a href="#">上一页</a></li>'
        else:
            prev = '<li><a href="%s?p=%s">上一页</a></li>'%(self.base_url,self.current_page - 1)

        if self.all_page <= self.page_range:
            start = 1
            end = self.all_page + 1
        else:
            if self.current_page > int(self.page_range / 2):
                if self.current_page + int(self.page_range / 2) > self.all_page:
                    start = self.all_page - self.page_range + 1
                    end = self.all_page + 1
                else:
                    start = self.current_page - int(self.page_range / 2)
                    end = self.current_page + int(self.page_range / 2) +1
            else:
                start = 1
                end = self.page_range
        for i in range(start,end):
            tmp = '<li><a href="%s?p=%s">%s</a></li>'%(self.base_url,i,i)
            page_list.append(tmp)
        if self.current_page >= self.all_page:
            nex = '<li><a href="#">下一页</a></li>'
        else:
            nex = '<li><a href="%s?p=%s">下一页</a></li>'%(self.base_url, self.current_page+1)
        page_list.append(nex)

        return " ".join(page_list)


class ExAasset(object):
    def __init__(self,request,):
        self.request = request
        self.mandatory_fields = ['sn', 'asset_id', 'asset_type']
        self.response = {
            'error': [],
            'info': [],
            'warning': []
        }

    def response_msg(self, msg_type, key, msg):
        if msg_type in self.response:
            self.response[msg_type].append({key: msg})
        else:
            raise ValueError

    def mandatory_check(self, data, only_check_sn=False):
        """检查客户端传递过来的数据,检查特定字段是否包含"""
        for field in self.mandatory_fields:
            if field not in data:
                "传过来的字典中不包含sn，asset_type等key"
                self.response_msg(
                    'error', 'MandatoryCheckFailed',
                    "The field [%s] is mandatory and not provided in your reporting data" % field
                )
        if self.response['error']:
            return False



    def data_is_valid_without_id(self,db_obj=None):
        '''when there's no asset id in reporting data ,goes through this function fisrt'''
        if db_obj:
            #新资产走这一步，db.obj.data==asset所有数据
            data = db_obj.data
        else:
            data = self.request.POST.get("asset_data")

        if data:
            try:
                data = json.loads(data)
                asset_obj = models.Asset.objects.get_or_create(sn=data.get('sn'), name=data.get(
                    'sn'))  # push asset id into reporting data before doing the mandatory check
                data['asset_id'] = asset_obj[0].id
                self.mandatory_check(data)
                self.clean_data = data
                if not self.response['error']:
                    return True
            except ValueError as e:
                self.response_msg('error', 'AssetDataInvalid', str(e))
        else:
            self.response_msg('error', 'AssetDataInvalid', "The reported asset data is not valid or provided")